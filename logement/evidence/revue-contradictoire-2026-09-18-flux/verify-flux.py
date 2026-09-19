"""Recalcul INDÉPENDANT de R-18 (revue statistique 2026-09-18).

N'importe PAS logement.core.flux. Lit directement S-11 (recensement),
S-54 (extrait Sitadel) et S-06 (table d'appartenance) ; n'emprunte au
dépôt que la table communes → ZE (ze.parse_commune_ze, lovac.plm_parent),
le drapeau de tension R-07 (build._tension_flag_with_variants), l'indice
de coût (build._cost_frame) et les noms de ZE (build._ze_names).

Usage : cd logement && uv run python evidence/revue-contradictoire-2026-09-18-flux/verify-flux.py
"""

from __future__ import annotations

import json
import math
import zipfile
from pathlib import Path

import pandas as pd

from logement.core import lovac, ze
from logement.shell import build

ROOT = Path(".")
RAW = ROOT / "data" / "raw"
ART = json.loads((ROOT / "data" / "processed" / "flux-construction-menages-ze.json").read_text())

# ------------------------------------------------------------------ lecture

with zipfile.ZipFile(RAW / "insee-rp-base-cc-logement-2022.zip") as zf:
    census = pd.read_csv(zf.open("base-cc-logement-2022.CSV"), sep=";", dtype=str)
with zipfile.ZipFile(RAW / "insee-table-appartenance-geo-communes-2026.zip") as zf:
    membership = pd.read_excel(
        zf.open("table-appartenance-geo-communes-2026.xlsx"),
        sheet_name="COM", header=5, engine="calamine", dtype=str,
    )
sitadel = pd.read_csv(
    RAW / "sdes-sitadel2-logements-communes-annuel-2013-2026.csv", sep=";", dtype=str
)
commune_ze = ze.parse_commune_ze(membership)
cz = dict(zip(commune_ze["code"], commune_ze["ze"]))

# ---------------------------------------------------- recensement par ZE
# Indépendance : on ne prend PAS drop_duplicates(keep=first) mais on
# exclut explicitement les arrondissements (les communes PLM 75056/13055/
# 69123 sont présentes en propre) et on vérifie l'égalité commune = Σ arr.

is_arr = census["CODGEO"].str.match(r"^(751\d\d|132\d\d|6938\d)$")
for city, pat in (("75056", r"^751\d\d$"), ("13055", r"^132\d\d$"), ("69123", r"^6938\d$")):
    sub = census[census["CODGEO"].str.match(pat)]
    for col in ("P16_MEN", "P22_MEN", "P22_LOG", "P16_LOG", "P22_RSECOCC", "P22_LOGVAC"):
        s = pd.to_numeric(sub[col]).sum()
        c = float(census.loc[census["CODGEO"] == city, col].iloc[0])
        assert abs(s - c) < 1e-6, (city, col, s, c)
print("PLM : commune == somme des arrondissements pour les 6 colonnes ✔")
print("ordre du fichier : commune PLM avant ses arrondissements ?",
      all(census.index[census.CODGEO == c][0] < census.index[census.CODGEO.str.match(p)].min()
          for c, p in (("75056", r"^751\d\d$"), ("13055", r"^132\d\d$"), ("69123", r"^6938\d$"))))

com = census[~is_arr].copy()
num_cols = ["P11_MEN", "P16_MEN", "P22_MEN", "P11_LOG", "P16_LOG", "P22_LOG", "P22_RSECOCC", "P22_LOGVAC"]
for col in num_cols:
    com[col] = pd.to_numeric(com[col], errors="coerce")
com["ze"] = com["CODGEO"].map(cz)
print(f"recensement : {len(com)} communes ; sans ZE : {com['ze'].isna().sum()} ; "
      f"NA P16_MEN {com['P16_MEN'].isna().sum()} / P22_MEN {com['P22_MEN'].isna().sum()}")
na_rows = com[com[["P16_MEN", "P22_MEN", "P22_LOG", "P16_LOG"]].isna().any(axis=1)]
print("communes du recensement à valeurs manquantes :", na_rows["CODGEO"].tolist(),
      "P22_MEN =", na_rows["P22_MEN"].tolist())
print("communes recensement absentes de Sitadel :", sorted(set(com.CODGEO) - set(sitadel.CODE_INSEE)))

zeF = com.dropna(subset=["ze"]).groupby("ze")[num_cols].sum()
zeF["formation"] = (zeF.P22_MEN - zeF.P16_MEN) / 6
zeF["croissance_parc"] = (zeF.P22_LOG - zeF.P16_LOG) / 6
zeF["part_rs"] = zeF.P22_RSECOCC / zeF.P22_LOG
zeF["part_vac"] = zeF.P22_LOGVAC / zeF.P22_LOG
zeF["lpm"] = 1 / (1 - zeF.part_rs - zeF.part_vac)
zeF["besoin"] = zeF.formation.clip(lower=0) * zeF.lpm
zeF["besoin_hrs"] = zeF.formation.clip(lower=0) / (1 - zeF.part_vac)

# ---------------------------------------------------------- Sitadel par ZE
sitadel["annee"] = sitadel["ANNEE"].astype(int)
sitadel["log_com"] = pd.to_numeric(sitadel["LOG_COM"])
sitadel["code"] = sitadel["CODE_INSEE"].map(lovac.plm_parent)
sitadel["ze"] = sitadel["code"].map(cz)
win = sitadel[(sitadel.annee >= 2017) & (sitadel.annee <= 2022)]
lon = sitadel[(sitadel.annee >= 2013) & (sitadel.annee <= 2024)]
print(f"Sitadel : {sitadel.CODE_INSEE.nunique()} codes ; total LOG_COM 2017-2022 = {int(win.log_com.sum()):,} "
      f"soit {win.log_com.sum() / 6:,.0f}/an ; sans ZE : {win.loc[win.ze.isna(), 'code'].nunique()} codes, "
      f"{int(win.loc[win.ze.isna(), 'log_com'].sum()):,} commencés perdus ({win.loc[win.ze.isna(), 'log_com'].sum() / 6:,.0f}/an, "
      f"{win.loc[win.ze.isna(), 'log_com'].sum() / win.log_com.sum() * 100:.2f} %)".replace(",", " "))
lost = win[win.ze.isna()].groupby("code").log_com.sum().sort_values(ascending=False)
print("  dont Mayotte (976) :", int(lost[lost.index.str.startswith("976")].sum()),
      "; hors Mayotte :", int(lost[~lost.index.str.startswith("976")].sum()),
      "sur", int((~lost.index.str.startswith('976')).sum()), "codes")
print("  15 plus gros codes perdus (hors Mayotte) :",
      lost[~lost.index.str.startswith("976")].head(15).to_dict())
by_year_lost = win[win.ze.isna() & ~win.code.str.startswith("976")].groupby("annee").log_com.sum()
print("  perdus par année :", by_year_lost.to_dict())
# Pertes par ZE : on rattache les codes perdus au département pour situer la perte
lost_dep = win[win.ze.isna() & ~win.code.str.startswith("976")].assign(dep=lambda d: d.code.str[:2]).groupby("dep").log_com.sum().sort_values(ascending=False)
print("  perdus par département (top 10) :", lost_dep.head(10).to_dict())
print("  codes Sitadel présents mais à 0 commencé sur 2017-2022 :", int((win.groupby('code').log_com.sum() == 0).sum()))
print("  commencés 2017-2022 de Mayotte présents dans la table mais hors cadre censitaire (ZE 0601) :",
      int(win.loc[win.ze == "0601", "log_com"].sum()))
zeF["commences"] = (win.dropna(subset=["ze"]).groupby("ze").log_com.sum() / 6).reindex(zeF.index)
zeF["commences_long"] = (lon.dropna(subset=["ze"]).groupby("ze").log_com.sum() / 12).reindex(zeF.index)
zeF["solde"] = zeF.commences - zeF.besoin
zeF["solde_hrs"] = zeF.commences - zeF.besoin_hrs
zeF["ratio"] = zeF.commences / zeF.besoin
zeF.loc[zeF.besoin <= 0, "ratio"] = float("nan")
zeF["c1000"] = zeF.commences / zeF.P22_LOG * 1000
zeF["disparitions"] = zeF.commences - zeF.croissance_parc

# ------------------------------------------------ tension, coût, noms
tendue, variants = build._tension_flag_with_variants(ROOT)
cost = build._cost_frame(ROOT)["indice_cout_pct"]
names = build._ze_names(ROOT)
zeF["tendue"] = tendue.reindex(zeF.index).fillna(False).astype(bool)
zeF["cout"] = cost.reindex(zeF.index)
zeF["name"] = names.reindex(zeF.index)
t07 = json.loads((ROOT / "data" / "processed" / "tension-manque-absolu-ze.json").read_text())
besoin_detente = float(t07["national"]["besoin_logements"])
print(f"\nZE : {len(zeF)} ; tendues {int(zeF.tendue.sum())} ; ZE sans Sitadel {int(zeF.commences.isna().sum())} ; "
      f"besoin de détente R-07 {besoin_detente:.0f} ; ZE tendues sans indice de coût {int(zeF.cout.isna().sum())}")
print("ZE de la table d'appartenance absentes du cadre censitaire :", sorted(set(commune_ze.ze) - set(zeF.index)))

# ------------------------------------------------------- statistiques
def spearman(df: pd.DataFrame, x: str, y: str) -> tuple[float, int, tuple[float, float]]:
    s = df[[x, y]].dropna()
    rho = float(s[x].rank().corr(s[y].rank()))
    n = len(s)
    z = math.atanh(rho)
    half = 1.959964 * math.sqrt((1 + rho**2 / 2) / (n - 3))
    return rho, n, (math.tanh(z - half), math.tanh(z + half))

def mann_whitney(a: pd.Series, b: pd.Series) -> float:
    a, b = a.dropna(), b.dropna()
    n1, n2 = len(a), len(b)
    comb = pd.concat([a, b], ignore_index=True)
    r = comb.rank()
    u1 = float(r.iloc[:n1].sum()) - n1 * (n1 + 1) / 2
    mu = n1 * n2 / 2
    n = n1 + n2
    ties = comb.value_counts()
    tie = float(((ties**3) - ties).sum()) / (n * (n - 1))
    sig = math.sqrt(n1 * n2 / 12 * ((n + 1) - tie))
    z = max(0.0, abs(u1 - mu) - 0.5) / sig
    return math.erfc(z / math.sqrt(2))

try:
    from scipy import stats as sps  # type: ignore
    HAVE_SCIPY = True
except Exception:
    HAVE_SCIPY = False

# ------------------------------------------------------- blocs
def bloc(sub: pd.DataFrame) -> dict[str, float | int]:
    return {
        "n_ze": len(sub),
        "menages_2016": round(sub.P16_MEN.sum()),
        "menages_2022": round(sub.P22_MEN.sum()),
        "formation_menages_an": round(sub.formation.sum()),
        "croissance_parc_an": round(sub.croissance_parc.sum()),
        "besoin_flux_an": round(sub.besoin.sum()),
        "besoin_flux_hors_rs_an": round(sub.besoin_hrs.sum()),
        "commences_an": round(sub.commences.sum()),
        "commences_an_long": round(sub.commences_long.sum()),
        "solde_flux_an": round(sub.commences.sum() - sub.besoin.sum()),
        "solde_flux_hors_rs_an": round(sub.commences.sum() - sub.besoin_hrs.sum()),
        "ratio_production": round(sub.commences.sum() / sub.besoin.sum(), 2),
        "ratio_hors_rs": round(sub.commences.sum() / sub.besoin_hrs.sum(), 2),
        "deficit_des_ze_deficitaires_an": round((-sub.solde).clip(lower=0).sum()),
        "deficit_hors_rs_des_ze_deficitaires_an": round((-sub.solde_hrs).clip(lower=0).sum()),
        "n_ze_deficitaires": int((sub.solde < 0).sum()),
        "n_ze_deficitaires_hors_rs": int((sub.solde_hrs < 0).sum()),
        "n_ze_menages_en_baisse": int((sub.formation < 0).sum()),
        "disparitions_implicites_an": round(sub.disparitions.sum()),
    }

T, O = zeF[zeF.tendue], zeF[~zeF.tendue]
out: dict[str, object] = {"national": bloc(zeF), "tendues": bloc(T), "autres": bloc(O)}
out["parts"] = {
    "formation": round(T.formation.clip(lower=0).sum() / zeF.formation.clip(lower=0).sum() * 100, 2),
    "formation_nette": round(T.formation.sum() / zeF.formation.sum() * 100, 2),
    "besoin": round(T.besoin.sum() / zeF.besoin.sum() * 100, 2),
    "commences": round(T.commences.sum() / zeF.commences.sum() * 100, 2),
    "parc": round(T.P22_LOG.sum() / zeF.P22_LOG.sum() * 100, 2),
    "menages_2022": round(T.P22_MEN.sum() / zeF.P22_MEN.sum() * 100, 2),
}
q = lambda s: {k: round(float(v), 3) for k, v in s.dropna().quantile([0, .25, .5, .75, 1]).items()}
out["ratio_median"] = {"toutes": q(zeF.ratio), "tendues": q(T.ratio), "autres": q(O.ratio)}
out["ratio_median_hors_rs"] = {"tendues": round(float((T.commences / T.besoin_hrs).replace([float('inf')], float('nan')).median()), 3),
                               "autres": round(float((O.commences / O.besoin_hrs).replace([float('inf')], float('nan')).median()), 3)}
out["c1000"] = {"tendues": q(T.c1000), "autres": q(O.c1000), "toutes": q(zeF.c1000)}
out["mw_p"] = round(mann_whitney(T.ratio, O.ratio), 4)
if HAVE_SCIPY:
    out["mw_p_scipy_asymptotic"] = float(sps.mannwhitneyu(T.ratio.dropna(), O.ratio.dropna(), alternative="two-sided", method="asymptotic", use_continuity=True).pvalue)
    out["mw_p_scipy_exact"] = float(sps.mannwhitneyu(T.ratio.dropna(), O.ratio.dropna(), alternative="two-sided", method="exact").pvalue)
    out["mw_p_c1000_scipy"] = float(sps.mannwhitneyu(T.c1000.dropna(), O.c1000.dropna(), alternative="two-sided").pvalue)
dom = zeF.index.str.startswith(("01", "02", "03", "04", "06"))
for label, sub in (("france_entiere", zeF), ("metropole", zeF[~dom])):
    rho, n, ci = spearman(sub, "ratio", "cout")
    out[f"spearman_{label}"] = {"rho": round(rho, 3), "n": n, "ci95": [round(ci[0], 3), round(ci[1], 3)]}
    if HAVE_SCIPY:
        s = sub[["ratio", "cout"]].dropna()
        r = sps.spearmanr(s.ratio, s.cout)
        out[f"spearman_{label}"]["scipy"] = (round(float(r.statistic), 3), round(float(r.pvalue), 3))
# Spearman restreint aux ZE au-dessus du plancher de classement (sensibilité)
rk = zeF[zeF.formation >= 200]
rho, n, ci = spearman(rk, "ratio", "cout")
out["spearman_seuil200"] = {"rho": round(rho, 3), "n": n, "ci95": [round(ci[0], 3), round(ci[1], 3)]}
rho, n, ci = spearman(zeF, "c1000", "cout")
out["spearman_c1000_vs_cout"] = {"rho": round(rho, 3), "n": n, "ci95": [round(ci[0], 3), round(ci[1], 3)]}
rho, n, ci = spearman(zeF.assign(dbl=lambda d: d.solde / d.P22_LOG * 1000), "dbl", "cout")
out["spearman_solde_pour_1000_vs_cout"] = {"rho": round(rho, 3), "n": n, "ci95": [round(ci[0], 3), round(ci[1], 3)]}

td = float((-T.solde).clip(lower=0).sum())
tdh = float((-T.solde_hrs).clip(lower=0).sum())
out["stock_vs_flux"] = {
    "besoin_detente": besoin_detente,
    "solde_tendues": round(T.solde.sum()),
    "deficit_tendues_deficitaires": round(td),
    "annees": round(besoin_detente / td, 2),
    "deficit_hors_rs": round(tdh),
    "annees_hors_rs": round(besoin_detente / tdh, 2),
    "formation_tendues": round(T.formation.sum()),
    "annees_formation": round(besoin_detente / T.formation.sum(), 3),
    "n_ze_tendues_deficitaires_hors_rs": int((T.solde_hrs < 0).sum()),
}
out["n_ze_sous_seuil"] = int((zeF.formation < 200).sum())
out["n_ze_sous_seuil_dont_tendues"] = int(((zeF.formation < 200) & zeF.tendue).sum())
out["variantes_h08"] = {
    k: {"n": int(v.reindex(zeF.index).fillna(False).sum()),
        "solde": round(zeF.loc[v.reindex(zeF.index).fillna(False).astype(bool), "solde"].sum()),
        "med_t": round(float(zeF.loc[v.reindex(zeF.index).fillna(False).astype(bool), "ratio"].median()), 3),
        "med_o": round(float(zeF.loc[~v.reindex(zeF.index).fillna(False).astype(bool), "ratio"].median()), 3)}
    for k, v in variants.items()
}
print("\n=== RECALCUL ===")
print(json.dumps(out, indent=1, ensure_ascii=False))

# ------------------------------------------------------- entrées nommées
cols = ["name", "formation", "besoin", "commences", "solde", "solde_hrs", "part_rs", "ratio", "tendue", "c1000", "P22_LOG"]
ranked = zeF[zeF.formation >= 200]
print("\n12 plus gros déficits (plancher 200) :")
print(ranked.sort_values("solde")[cols].head(12).round(3).to_string())
print("\n8 plus gros surplus :")
print(ranked.sort_values("solde", ascending=False)[cols].head(8).round(3).to_string())
print("\nDéficits en ZE tendues (12) :")
print(ranked[ranked.tendue & (ranked.solde < 0)].sort_values("solde")[cols].head(12).round(3).to_string())
print("\nZE sous le plancher mais à gros solde absolu (exclues des classements) :")
under = zeF[zeF.formation < 200]
print(under.reindex(under.solde.abs().sort_values(ascending=False).index)[cols].head(8).round(3).to_string())
print("\nZE tendues DÉFICITAIRES hors RS (les vraies exceptions) :")
print(T[T.solde_hrs < 0].sort_values("solde_hrs")[cols].round(3).to_string())
print("\nRatio max (69,79) :")
print(zeF.sort_values("ratio", ascending=False)[cols].head(3).round(3).to_string())

# ------------------------------------------------------- comparaison artefact
print("\n=== ÉCARTS ARTEFACT vs RECALCUL ===")
diffs = 0
for blk in ("national", "tendues", "autres"):
    for k, v in ART[blk].items():
        mine = out[blk].get(k)
        if mine is None:
            continue
        if isinstance(v, float) or isinstance(mine, float):
            ok = abs(float(v) - float(mine)) < 0.006
        else:
            ok = v == mine
        if not ok:
            diffs += 1
            print(f"  {blk}.{k}: artefact {v} vs recalcul {mine}")
for blk, entries in (("plus_gros_deficits", ranked.sort_values("solde").head(12)),
                     ("plus_gros_surplus", ranked.sort_values("solde", ascending=False).head(8)),
                     ("deficits_tendues", ranked[ranked.tendue & (ranked.solde < 0)].sort_values("solde").head(12))):
    for e, (zcode, row) in zip(ART[blk], entries.iterrows()):
        if e["ze"] != zcode:
            diffs += 1; print(f"  {blk}: ordre {e['ze']} vs {zcode}")
        for ak, mk in (("formation_menages_an", "formation"), ("besoin_flux_an", "besoin"), ("commences_an", "commences"),
                       ("solde_flux_an", "solde"), ("solde_flux_hors_rs_an", "solde_hrs")):
            if e[ak] != round(float(row[mk])):
                diffs += 1; print(f"  {blk} {e['name']} {ak}: {e[ak]} vs {round(float(row[mk]))}")
        if e["ratio_production"] != round(float(row["ratio"]), 2) or e["part_rs_2022_pct"] != round(float(row["part_rs"]) * 100, 1):
            diffs += 1; print(f"  {blk} {e['name']} ratio/rs: {e['ratio_production']}/{e['part_rs_2022_pct']} vs {round(float(row['ratio']),2)}/{round(float(row['part_rs'])*100,1)}")
print(f"écarts détectés : {diffs}")

# ------------------------------------------------------- invariants
print("\n=== INVARIANTS ===")
print("ratio ≥ 0 partout :", bool((zeF.ratio.dropna() >= 0).all()))
print("solde = commencés − besoin partout :", bool(((zeF.commences - zeF.besoin - zeF.solde).abs() < 1e-9).all()))
print("besoin hors RS ≤ besoin partout :", bool((zeF.besoin_hrs <= zeF.besoin + 1e-9).all()))
print("solde hors RS ≥ solde partout :", bool((zeF.solde_hrs >= zeF.solde - 1e-9).all()))
print("lpm ≥ 1 partout :", bool((zeF.lpm >= 1).all()), "max", round(float(zeF.lpm.max()), 3), zeF.lpm.idxmax(), zeF.name.get(zeF.lpm.idxmax()))
print("part_rs + part_vac < 1 partout :", bool(((zeF.part_rs + zeF.part_vac) < 1).all()))
print("tendues + autres = national (n, formation, besoin, commencés) :",
      out["tendues"]["n_ze"] + out["autres"]["n_ze"] == out["national"]["n_ze"],
      T.formation.sum() + O.formation.sum() == zeF.formation.sum() or abs(T.formation.sum() + O.formation.sum() - zeF.formation.sum()) < 1e-6,
      abs(T.besoin.sum() + O.besoin.sum() - zeF.besoin.sum()) < 1e-6,
      abs(T.commences.sum() + O.commences.sum() - zeF.commences.sum()) < 1e-6)
print("ZE tendues à ménages en baisse :", int((T.formation < 0).sum()))
print("part formation (clip 0) tendues + autres = 100 :", round(T.formation.clip(lower=0).sum() / zeF.formation.clip(lower=0).sum() * 100 + O.formation.clip(lower=0).sum() / zeF.formation.clip(lower=0).sum() * 100, 3))
print("Σ formation clip 0 (national) vs Σ formation nette :", round(zeF.formation.clip(lower=0).sum()), round(zeF.formation.sum()))
print("national formation 275 284 = (30 888 593 − 29 236 888)/6 ?", round((30888593 - 29236888) / 6, 2))
print("disparitions nationales = commencés − croissance :", round(zeF.commences.sum() - zeF.croissance_parc.sum()))
print("ratio national hors RS :", round(zeF.commences.sum() / zeF.besoin_hrs.sum(), 3), "; tendues hors RS :", round(T.commences.sum() / T.besoin_hrs.sum(), 3))
print("10,6 = 194 488 / 18 279 →", round(besoin_detente / td, 3), "; 37,5 →", round(besoin_detente / tdh, 3), "; 1,3 →", round(besoin_detente / T.formation.sum(), 3))
print("Paris 35 015 / 19 001 =", round(35015 / 19001, 3))
# Besoin implicite « structure constante » agrégé vs sommé : le national de l'artefact somme des besoins par ZE
print("besoin national recalculé à structure NATIONALE (pas Σ ZE) :",
      round(zeF.formation.sum() / (1 - zeF.P22_RSECOCC.sum() / zeF.P22_LOG.sum() - zeF.P22_LOGVAC.sum() / zeF.P22_LOG.sum())))
# Sensibilité : fenêtre 2016-2021 / 2018-2023 des commencés
for a, b in ((2016, 2021), (2018, 2023), (2017, 2023)):
    w = sitadel[(sitadel.annee >= a) & (sitadel.annee <= b)].dropna(subset=["ze"])
    c = (w.groupby("ze").log_com.sum() / (b - a + 1)).reindex(zeF.index)
    ct = c[zeF.tendue]
    print(f"fenêtre {a}-{b} : national {c.sum():,.0f}/an, ratio {c.sum()/zeF.besoin.sum():.3f} ; tendues {ct.sum():,.0f}/an, "
          f"ratio {ct.sum()/T.besoin.sum():.3f}, solde {ct.sum()-T.besoin.sum():,.0f}, déficit ZE déf. {(-(ct - T.besoin)).clip(lower=0).sum():,.0f}".replace(",", " "))
# Sensibilité : commencés perdus réaffectés (majorant) aux ZE tendues ? on ne peut pas sans table ; on donne la borne.
lost_hm = float(lost[~lost.index.str.startswith("976")].sum()) / 6
print(f"borne : commencés perdus hors Mayotte {lost_hm:,.0f}/an = {lost_hm / zeF.commences.sum() * 100:.2f} % du national ; "
      f"si tous en ZE tendues, solde tendues {T.solde.sum() + lost_hm:,.0f}".replace(",", " "))
# Autre lecture : formation 2011-2016 vs 2016-2022
print("formation 2011-2016 nationale :", round(((zeF.P16_MEN - zeF.P11_MEN) / 5).sum()), "/an ; 2016-2022 :", round(zeF.formation.sum()))
# Sitadel LOG_AUT (autorisés) comme borne haute
wa = win.dropna(subset=["ze"]).assign(log_aut=pd.to_numeric(win.dropna(subset=["ze"]).LOG_AUT))
aut = (wa.groupby("ze").log_aut.sum() / 6).reindex(zeF.index)
print("autorisés 2017-2022 : national", round(aut.sum()), "/an ; tendues", round(aut[zeF.tendue].sum()))

# ======================================================= contrôles complémentaires
import numpy as np

print("\n=== COMPLÉMENTS ===")
# (a) communes du recensement à valeurs manquantes : sommées comme 0 par groupby.sum
na_ze = na_rows.assign(bias=lambda d: d.P22_MEN.fillna(0) / 6 - d.P16_MEN.fillna(0) / 6).groupby("ze").bias.sum()
print("biais brut de formation par ZE des communes à NA (ménages/an) :", na_ze.round(1).to_dict())
for parent, child in (("14712", "14666"), ("85084", "85165")):
    p = com.set_index("CODGEO").loc[parent]
    print(f"  parente {parent} : P16_MEN {p.P16_MEN:.0f} → P22_MEN {p.P22_MEN:.0f} (porte les ménages 2016 de {child} : biais ZE nul)")
# (b) codes Sitadel obsolètes : chronologie
lost_all = sitadel[sitadel.ze.isna() & ~sitadel.code.str.startswith("976")]
print("commencés sous code obsolète, par année (2013-2026) :", lost_all.groupby("annee").log_com.sum().astype(int).to_dict())
for code in ("85166", "85060", "74011", "74268", "93059", "49069"):
    print(f"  {code} :", lost_all[lost_all.code == code].set_index("annee").log_com.astype(int).to_dict())
fix = {"5214": ["85166", "85060"], "8401": ["74011", "74268", "74182"], "1109": ["93059"]}
for zcode, codes in fix.items():
    add = sum(lost.get(c, 0) for c in codes) / 6
    r = zeF.loc[zcode]
    print(f"  ZE {zcode} {r['name'].strip()} : commencés {r.commences:.0f} → {r.commences + add:.0f} (+{add:.0f}/an) ; "
          f"solde {r.solde:.0f} → {r.solde + add:.0f} ; hors RS {r.solde_hrs:.0f} → {r.solde_hrs + add:.0f} ; "
          f"ratio {r.ratio:.2f} → {(r.commences + add) / r.besoin:.2f}")
# (c) médianes et Mann-Whitney avec les 20 ZE à besoin nul (ratio = +inf, rang maximal)
ratio_inf = zeF.commences / zeF.besoin
Ti, Oi = ratio_inf[zeF.tendue], ratio_inf[~zeF.tendue]
print(f"médiane autres sans les {int(np.isinf(Oi).sum())} ZE à besoin nul : {O.ratio.median():.3f} ; avec (rang max) : {Oi.median():.3f} ; tendues {Ti.median():.3f}")

def mw_pairs(a: pd.Series, b: pd.Series) -> tuple[float, int, int]:
    a, b = np.asarray(a.dropna()), np.asarray(b.dropna())
    u = float(sum((a[i] > b).sum() + 0.5 * (a[i] == b).sum() for i in range(len(a))))
    return u, len(a), len(b)

def mw_normal_p(u: float, n1: int, n2: int) -> float:
    mu, sd = n1 * n2 / 2, math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    return math.erfc(abs(u - mu) / sd / math.sqrt(2))

u, n1, n2 = mw_pairs(T.ratio, O.ratio)
print(f"MW ratio (comptage de paires) : U {u:.0f}, n {n1}/{n2}, AUC {u / (n1 * n2):.3f}, p normal {mw_normal_p(u, n1, n2):.4f}")
rng = np.random.default_rng(20260918)
pool = np.concatenate([T.ratio.dropna().values, O.ratio.dropna().values])
obs = abs(u - n1 * n2 / 2); cnt = 0; N = 20000
for _ in range(N):
    rng.shuffle(pool)
    rk = pd.Series(pool).rank().values
    cnt += abs(rk[:n1].sum() - n1 * (n1 + 1) / 2 - n1 * n2 / 2) >= obs - 1e-9
print(f"MW ratio p par permutation ({N}) : {cnt / N:.4f}")
u2, m1, m2 = mw_pairs(Ti, Oi)
print(f"MW ratio AVEC les ZE à besoin nul : n {m1}/{m2}, AUC {u2 / (m1 * m2):.3f}, p normal {mw_normal_p(u2, m1, m2):.4f}")
u3, k1, k2 = mw_pairs(T.c1000, O.c1000)
print(f"MW commencés pour 1 000 : AUC {u3 / (k1 * k2):.3f}, p normal {mw_normal_p(u3, k1, k2):.2e}")
# (d) Spearman ratio × coût : bootstrap et plancher de classement
s = zeF[["ratio", "cout"]].dropna()
boot = []
for _ in range(3000):
    ss = s.iloc[rng.integers(0, len(s), len(s))]
    boot.append(ss.ratio.rank().corr(ss.cout.rank()))
print(f"Spearman ratio × coût : n {len(s)} (= 305 − {int(zeF.ratio.isna().sum())} ratio NaN − {int(zeF.cout.isna().sum())} coût NaN + {int((zeF.ratio.isna() & zeF.cout.isna()).sum())} communs), "
      f"rho {s.ratio.rank().corr(s.cout.rank()):.3f}, bootstrap 95 % {np.round(np.percentile(boot, [2.5, 97.5]), 3)}")
for floor in (0, 100, 200, 300, 500, 1000):
    ss = zeF[zeF.formation >= floor][["ratio", "cout"]].dropna()
    rho = ss.ratio.rank().corr(ss.cout.rank()); z = math.atanh(rho); half = 1.959964 * math.sqrt((1 + rho**2 / 2) / (len(ss) - 3))
    print(f"  plancher {floor:>4} ménages/an : n {len(ss)}, rho {rho:+.3f} [{math.tanh(z - half):+.2f} ; {math.tanh(z + half):+.2f}]")
ss = zeF[["ratio", "cout", "formation"]].dropna()
print(f"  Spearman ratio × formation {ss.ratio.rank().corr(ss.formation.rank()):+.3f} ; coût × formation {ss.cout.rank().corr(ss.formation.rank()):+.3f}")
print("ZE tendues sans indice de coût :", T[T.cout.isna()].name.tolist())
# (e) arrondis et lectures du texte
print(f"médiane commencés/1 000 tendues : {T.c1000.median():.4f} (1 décimale : {T.c1000.median():.1f}) ; autres {O.c1000.median():.4f}")
p = zeF.loc["1109"]
print(f"Paris : commencés/besoin {p.ratio:.2f} ; commencés/formation {p.commences / p.formation:.2f}")
print("ZE tendues déficitaires :", int((T.solde < 0).sum()), "; redevenant ≥ 0 hors RS :", int(((T.solde < 0) & (T.solde_hrs >= 0)).sum()),
      "; restant déficitaires hors RS :", int((T.solde_hrs < 0).sum()))
d = T[T.solde < 0]
print(f"part RS des ZE tendues déficitaires : min {d.part_rs.min() * 100:.1f} %, médiane {d.part_rs.median() * 100:.1f} %, max {d.part_rs.max() * 100:.1f} %")
print("O-41 totaux annuels Sitadel :", sitadel.groupby("annee").log_com.sum().astype(int).to_dict())
