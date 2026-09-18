"""Independent recomputation of R-15..R-17 (session 7) from the frozen sources.

Reviewer STATISTIQUE ET ARITHMÉTIQUE, revue contradictoire 2026-09-18.

Deliberately does NOT import `logement.core.institution`: every session-7
figure is recomputed here with plain pandas/numpy from the SAME upstream
frames the diagnostic arc already published (R-07 tension, R-09 detente,
R-14 DVF medians, R-06 market rents), then compared with the committed
artifact `data/processed/scenarios-institutionnels-ze.json`.

Run from logement/:  uv run python evidence/revue-contradictoire-2026-09-18/verify-statistique.py
"""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from logement.core import cout, effort, lovac, remob, rs, tension, transaction, ze
from logement.core.lovac import plm_parent
from logement.shell import build

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
ART = json.loads((ROOT / "data" / "processed" / "scenarios-institutionnels-ze.json").read_text())

H = {hid: build._load_hypothesis(ROOT, hid) for hid in ("H-08", "H-12", "H-09", "H-10", "H-14", "H-15", "H-16", "H-17", "H-18")}


def hdr(title: str) -> None:
    print("\n" + "=" * 78 + f"\n{title}\n" + "=" * 78)


def cmp(label: str, published: float, recomputed: float, tol: float = 0.0) -> None:
    diff = recomputed - published
    ok = abs(diff) <= tol
    print(f"{label:<62} publié {published!s:>12}  recalc {recomputed!s:>14}  écart {diff:+.4g}  {'OK' if ok else 'ÉCART'}")


# ------------------------------------------------------------- upstream frames
hdr("0. Chargement des mêmes entrées figées (parsers amont, déjà revus)")
with zipfile.ZipFile(RAW / build.CENSUS_ZIP) as zf, zf.open(build.CENSUS_CSV) as fh:
    census_raw = pd.read_csv(fh, sep=";", dtype=str, usecols=["CODGEO", *rs.CENSUS_COLS])
census = rs.parse_census_housing(census_raw)
with zipfile.ZipFile(RAW / build.CENSUS_ZIP) as zf, zf.open(build.CENSUS_CSV) as fh:
    mix_raw = pd.read_csv(fh, sep=";", dtype=str, usecols=["CODGEO", *effort.CENSUS_MIX_COLS])
census_mix = effort.parse_census_mix(mix_raw)
tlv = tension.parse_tlv(pd.read_csv(RAW / build.TLV_FILE, sep=";", dtype=str))
commune_ze = ze.parse_commune_ze(build._read_membership(ROOT))
communes = lovac.parse_territories(
    build._read_lovac(ROOT, build.LOVAC_COMMUNES), code_col="CODGEO_26", name_col="LIBGEO_26"
)
tense_all = tension.tension_by_ze(
    census, tlv, communes, commune_ze, H["H-08"].central_value, H["H-12"].central_value
)
tense = tense_all[tense_all["tendue"]]
mix = (
    census_mix.merge(commune_ze, on="code", how="left").dropna(subset=["ze"]).groupby("ze")[["rp_maison", "rp_appart"]].sum()
)
part_maison = mix["rp_maison"] / (mix["rp_maison"] + mix["rp_appart"])
ze_names = build._ze_names(ROOT)
detente = remob.detente_frame(tense, part_maison, ze_names)
ipea = remob.ipea_factor(remob.parse_ipea_annual_means((RAW / build.IPEA_FILE).read_text(encoding="utf-8")))
cu = remob.unit_cost_eur(detente["part_maison"], H["H-09"].central_value, H["H-10"].central_value, ipea)
print(f"ZE tendues (R-07 central) : {len(detente)} ; besoin {detente['besoin_mobilisation'].sum():,.0f} ; "
      f"gisement effectif {detente['structurelle'].fillna(0).sum():,.0f} ; rénovables {detente['renovables'].sum():,.0f} ; "
      f"déficit {detente['deficit_neuf'].sum():,.0f} ; facteur IPEA {ipea:.4f}")

print("lecture DVF (1-2 min)…")
dvf = pd.read_csv(RAW / build.DVF_FILE, usecols=list(transaction.DVF_COLUMNS), dtype={"code_commune": str})
sales, assiette = transaction.parse_dvf_sales(dvf)
prix, couverture = transaction.prices_by_ze(sales, commune_ze)
print(f"DVF : {len(sales):,} ventes retenues ; {len(prix)} ZE avec prix ; couverture {couverture}")

with zipfile.ZipFile(RAW / build.FILOSOFI_ZIP) as zf, zf.open(build.FILOSOFI_CSV) as fh:
    filosofi = pd.read_csv(fh, sep=";", dtype=str, usecols=["GEO", "GEO_OBJECT", "FILOSOFI_MEASURE", "OBS_VALUE"])
niveau_vie = cout.parse_filosofi(filosofi, geo_object="ZE2020", measure="MED_SL")
loyer_marche = build._effort_frame(ROOT)["loyer_mix_m2"]

# Social rent by ZE, recomputed by hand from the RPLS sheet (stock-weighted, C-09).
with zipfile.ZipFile(RAW / build.RPLS_ZIP) as zf, zf.open(build.RPLS_XLSX) as fh:
    rpls_raw = pd.read_excel(fh, sheet_name="COMMUNE", engine="calamine", header=5, dtype={"DEPCOM_ARM": str})
rp = pd.DataFrame({"code": rpls_raw["DEPCOM_ARM"].astype("string").str.strip().map(plm_parent)})
rp["nb_ls"] = pd.to_numeric(rpls_raw["nb_ls"], errors="coerce")
rp["loymoy"] = pd.to_numeric(rpls_raw["loymoy"], errors="coerce")
rp = rp.dropna(subset=["code", "nb_ls", "loymoy"]).merge(commune_ze, on="code", how="inner")
rp = rp[rp["nb_ls"] > 0]
loyer_social = (rp["loymoy"] * rp["nb_ls"]).groupby(rp["ze"]).sum() / rp.groupby("ze")["nb_ls"].sum()
print(f"RPLS : {rp['code'].nunique():,} communes jointes ; {len(loyer_social)} ZE avec loyer social")

rp_ze = census.merge(commune_ze, on="code", how="inner").groupby("ze")["P22_RP"].sum()
rp_total = float(rp_ze.reindex(detente.index).fillna(0).sum())

# ------------------------------------------------------------- 1. annuity + named ZE
hdr("1. Facteur d'annuité et loyers d'équilibre de ZE nommées")
r, n = H["H-16"].central_value / 100, H["H-17"].central_value
af = r / (1 - (1 + r) ** (-n))
af30 = r / (1 - (1 + r) ** (-30))
cmp("facteur d'annuité 2,30 %/40 ans (M-B)", ART["m_b_operateur_acquisition"]["annuity_factor_central"], round(af, 5), 1e-5)
cmp("facteur d'annuité 2,30 %/30 ans (M-C)", ART["m_c_bail_rehabilitation"]["annuity_factor"], round(af30, 5), 1e-5)
opex = H["H-18"].central_value
surface = detente["part_maison"] * remob.SURFACE_MAISON_M2 + (1 - detente["part_maison"]) * remob.SURFACE_APPART_M2

f = detente.join(cu.rename("cu"), how="inner").join(prix, how="inner")
f["surface"] = surface
f["loyer_marche"] = loyer_marche
f["loyer_social"] = loyer_social
f["niveau_vie"] = niveau_vie
f["unit_renove"] = f["prix_median"] * H["H-15"].central_value + f["cu"]
f["loyer_eq_renove"] = f["unit_renove"] * af / (1 - opex) / 12 / f["surface"]
f["loyer_eq_neuf"] = remob.PRIX_REVIENT_NEUF_EUR_2023 * af / (1 - opex) / 12 / f["surface"]
f["surface_implicite_dvf"] = f["prix_median"] / f["prix_m2_median"]
pub = {e["ze"]: e for e in ART["m_b_operateur_acquisition"]["loyer_equilibre_le_plus_haut"] + ART["m_b_operateur_acquisition"]["loyer_equilibre_le_plus_bas"]}
for code, name in (("8401", "Annecy"), ("7503", "Bayonne"), ("9307", "Digne-les-Bains")):
    row = f.loc[code]
    print(f"\n{name} ({code}) : prix médian DVF {row['prix_median']:,.0f} € ; prix/m² médian {row['prix_m2_median']:,.0f} €/m² "
          f"→ surface implicite des biens vendus {row['surface_implicite_dvf']:.0f} m² vs surface C-07 {row['surface']:.1f} m² "
          f"(part maison {row['part_maison']:.2f}) ; coût rénovation unitaire {row['cu']:,.0f} € ; "
          f"marché {row['loyer_marche']:.2f} ; social {row['loyer_social']:.2f}")
    cmp(f"  {name} prix d'acquisition", pub[code]["prix_acquisition_eur"], round(row["prix_median"]))
    cmp(f"  {name} coût unitaire rénové", pub[code]["cout_unitaire_renove_eur"], round(row["unit_renove"]))
    cmp(f"  {name} loyer d'équilibre rénové €/m²/mois", pub[code]["loyer_equilibre_renove_m2"], round(row["loyer_eq_renove"], 2), 0.005)
    cmp(f"  {name} loyer d'équilibre neuf €/m²/mois", pub[code]["loyer_equilibre_neuf_m2"], round(row["loyer_eq_neuf"], 2), 0.005)
    alt = row["unit_renove"] * af / (1 - opex) / 12 / row["surface_implicite_dvf"]
    print(f"  → si l'on divise par la surface IMPLICITE des biens vendus : {alt:.2f} €/m²/mois")

# ------------------------------------------------------------- 2. national totals
hdr("2. Totaux nationaux M-B (re-sommation du tableau par ZE)")
f["acq"] = f["renovables"] * f["prix_median"] * H["H-15"].central_value
f["ren"] = f["renovables"] * f["cu"]
f["neuf"] = f["deficit_neuf"] * remob.PRIX_REVIENT_NEUF_EUR_2023
f["inv"] = f["acq"] + f["ren"] + f["neuf"]
f["annuite"] = f["inv"] * af
c = ART["m_b_operateur_acquisition"]["central"]
cmp("n_ze M-B", c["n_ze"], len(f))
cmp("rénovables M-B", c["logements"]["renoves"], round(f["renovables"].sum()))
cmp("neufs M-B", c["logements"]["neufs"], round(f["deficit_neuf"].sum()))
cmp("acquisition Md€", c["dont_acquisition_mdeur"], round(f["acq"].sum() / 1e9, 1), 0.05)
cmp("rénovation Md€", c["dont_renovation_mdeur"], round(f["ren"].sum() / 1e9, 1), 0.05)
cmp("neuf Md€", c["dont_neuf_mdeur"], round(f["neuf"].sum() / 1e9, 1), 0.05)
cmp("investissement Md€", c["investissement_mdeur"], round(f["inv"].sum() / 1e9, 1), 0.05)
print(f"  (non arrondi : acq {f['acq'].sum()/1e9:.3f} + ren {f['ren'].sum()/1e9:.3f} + neuf {f['neuf'].sum()/1e9:.3f} = {f['inv'].sum()/1e9:.3f} Md€)")
cmp("annuité Md€/an", c["annuite_mdeur_an"], round(f["annuite"].sum() / 1e9, 2), 0.005)
cmp("résidences principales ZE tendues", ART["perimetre"]["residences_principales_ze_tendues"], round(rp_total))
cmp("annuité par RP €/an", c["annuite_par_residence_principale_eur_an"], round(f["annuite"].sum() / rp_total))
cmp("coût unitaire rénové médian €", c["cout_unitaire_renove_median_eur"], round(f["unit_renove"].median()))
# balancing subsidy to the social rent
gap_r = (f["loyer_eq_renove"] - f["loyer_social"]).clip(lower=0)
gap_n = (f["loyer_eq_neuf"] - f["loyer_social"]).clip(lower=0)
f["sub_r"] = gap_r * f["surface"] * 12 * f["renovables"]
f["sub_n"] = gap_n * f["surface"] * 12 * f["deficit_neuf"]
cmp("subvention rénové Md€/an", c["dont_renove_mdeur_an"], round(f["sub_r"].sum() / 1e9, 2), 0.005)
cmp("subvention neuf Md€/an", c["dont_neuf_mdeur_an"], round(f["sub_n"].sum() / 1e9, 2), 0.005)
cmp("subvention totale Md€/an", c["subvention_equilibre_social_mdeur_an"], round((f["sub_r"].sum() + f["sub_n"].sum()) / 1e9, 2), 0.005)
for k, col in (("loyer_equilibre_renove_m2", "loyer_eq_renove"), ("loyer_equilibre_neuf_m2", "loyer_eq_neuf"), ("loyer_marche_m2", "loyer_marche"), ("loyer_social_m2", "loyer_social")):
    q = f[col].dropna().quantile([0, 0.25, 0.5, 0.75, 1]).round(2).tolist()
    cmp(f"{k} médiane", c[k]["median"], q[2], 0.005)
    print(f"    quantiles recalculés min/p25/med/p75/max : {q}  publié : {[c[k][x] for x in ('min','p25','median','p75','max')]}")
with_rents = f.dropna(subset=["loyer_marche", "loyer_social"])
cmp("n_ze_avec_loyers M-B", c["n_ze_avec_loyers"], len(with_rents))
cmp("n ZE équilibre rénové ≤ marché", c["n_ze_equilibre_renove_sous_marche"], int((with_rents["loyer_eq_renove"] <= with_rents["loyer_marche"]).sum()))
ratio_m = (with_rents["loyer_eq_renove"] / with_rents["loyer_marche"])
ratio_s = (with_rents["loyer_eq_renove"] / with_rents["loyer_social"])
cmp("ratio équilibre/marché médian", c["ratio_equilibre_renove_sur_marche"]["median"], round(ratio_m.median(), 2), 0.005)
cmp("ratio équilibre/social médian", c["ratio_equilibre_renove_sur_social"]["median"], round(ratio_s.median(), 2), 0.005)
print(f"  ratio/marché min {ratio_m.min():.4f} ({with_rents['ze_name'][ratio_m.idxmin()]}) — strictement > 1 ?", bool(ratio_m.min() > 1))

# ------------------------------------------------------------- 3. holding charge
hdr("3. Charge de détention M-D : parc du périmètre OFGL")
dep = census["code"].map(transaction.departement_of)
excl = ("75", "69", "2A", "2B", "972", "973")
in_per = ~dep.isin(excl)
tot = census["P22_LOG"].sum()
per = census.loc[in_per, "P22_LOG"].sum()
print(f"parc S-11 France entière (communes du fichier) : {tot:,.0f} ; exclu {tot-per:,.0f} ; périmètre {per:,.0f}")
print("détail des départements exclus :")
print(census.loc[~in_per].assign(dep=dep[~in_per]).groupby("dep")["P22_LOG"].agg(["sum", "size"]).to_string())
codes69 = census.loc[dep == "69", "code"]
print(f"codes commune '69' : {len(codes69)} communes, ex. {sorted(codes69)[:3]} … {sorted(codes69)[-3:]} ; "
      f"Lyon (69123) présent : {'69123' in set(codes69)} ; Villeurbanne (69266) : {'69266' in set(codes69)} ; "
      f"tout code commençant par 69M/69X ? {sorted(set(c[:3] for c in codes69))}")
print(f"codes de département présents dans le recensement (outre-mer) : {sorted(set(d for d in dep if d.startswith('97')))}")
cmp("logements du périmètre", ART["m_d_bascule_dmto"]["logements_perimetre"], round(per))
charge = 9.9e9 / per
cmp("charge €/logement/an", ART["m_d_bascule_dmto"]["charge_detention_eur_logement_an"], round(charge))
print(f"  charge non arrondie {charge:.2f} € ; sur le parc France entière elle serait {9.9e9/tot:.2f} € ; "
      f"si le 9,9 Md€ (à 4,5 % en 2024) était revalorisé au taux 5,0 % de 2025 : {9.9e9*5/4.5/per:.2f} €")

# ------------------------------------------------------------- 4. fiscal toll
hdr("4. Péage fiscal M-D (296 ZE)")
g = prix.join(niveau_vie.rename("nv"), how="left").join(ze_names.rename("ze_name"), how="left")
g["droits"] = g["prix_median"] * g["taux_dmto_pct"] / 100
g["csi"] = g["prix_median"].map(transaction.csi_eur)
g["emol"] = g["prix_median"].map(transaction.emoluments_ttc)
g["peage_fiscal"] = g["droits"] + g["csi"]
g["mois_fiscal"] = g["peage_fiscal"] / (g["nv"] / 12)
g["mois_residuel"] = g["emol"] / (g["nv"] / 12)
g["annees"] = g["peage_fiscal"] / charge
g["tendue"] = g.index.isin(detente.index)
md = ART["m_d_bascule_dmto"]
cmp("n_ze M-D", md["n_ze"], len(g))
cmp("n_ze tendues M-D", md["n_ze_tendues"], int(g["tendue"].sum()))
print(f"  ZE2020 dans la table d'appartenance : {commune_ze['ze'].nunique()} ; ZE sans prix DVF : {commune_ze['ze'].nunique() - len(g)} "
      f"(départements sans DVF : Alsace-Moselle 57/67/68 + Mayotte 976)")
missing = set(commune_ze["ze"]) - set(g.index)
print(f"  ZE absentes : {sorted(missing)} → {[ze_names.get(z, '?') for z in sorted(missing)]}")
q = lambda s, d: s.dropna().quantile([0, 0.25, 0.5, 0.75, 1]).round(d).tolist()  # noqa: E731
cmp("péage fiscal médian €", md["peage_fiscal_eur"]["median"], q(g["peage_fiscal"], 0)[2], 0.5)
print(f"    quantiles {q(g['peage_fiscal'], 0)}")
cmp("péage fiscal mois de niveau de vie (médiane)", md["peage_fiscal_mois_niveau_vie"]["median"], q(g["mois_fiscal"], 2)[2], 0.005)
cmp("péage résiduel mois (médiane)", md["peage_residuel_mois_niveau_vie"]["median"], q(g["mois_residuel"], 2)[2], 0.005)
cmp("années équivalentes médiane", md["annees_equivalentes"]["median"], q(g["annees"], 1)[2], 0.05)
print(f"    quantiles {q(g['annees'], 1)}")
cmp("années équivalentes ZE tendues (médiane)", md["annees_equivalentes_tendues"]["median"], q(g.loc[g['tendue'], "annees"], 1)[2], 0.05)
cmp("années équivalentes autres (médiane)", md["annees_equivalentes_autres"]["median"], q(g.loc[~g['tendue'], "annees"], 1)[2], 0.05)
print(f"  n ZE avec niveau de vie manquant : {int(g['nv'].isna().sum())}")
# --- what is actually shifted: only the DEPARTMENTAL share (L-28 (2)).
# taux_dmto_pct = départemental × 1.0237 + 1.20 → départemental = (taux − 1.20)/1.0237.
g["taux_dep"] = (g["taux_dmto_pct"] - transaction.COMMUNAL_TAX_PCT) / transaction.ASSESSMENT_FEE_FACTOR
g["droits_dep"] = g["prix_median"] * g["taux_dep"] / 100
g["annees_dep"] = g["droits_dep"] / charge
g["residuel_apres_bascule"] = g["peage_fiscal"] - g["droits_dep"] + g["emol"]
g["mois_residuel_apres_bascule"] = g["residuel_apres_bascule"] / (g["nv"] / 12)
print("\n  Numérateur cohérent avec « seule la part départementale est basculée » (L-28 (2)) :")
print(f"    part départementale des droits dans le péage fiscal (médiane) : {(g['droits_dep']/g['peage_fiscal']).median():.3f}")
print(f"    années équivalentes = droits DÉPARTEMENTAUX / charge : quantiles {q(g['annees_dep'], 1)} ; "
      f"tendues {q(g.loc[g['tendue'], 'annees_dep'], 1)[2]} ; autres {q(g.loc[~g['tendue'], 'annees_dep'], 1)[2]}")
print(f"    péage résiduel APRÈS bascule (communal 1,20 % + frais d'assiette + CSI + émoluments), mois : {q(g['mois_residuel_apres_bascule'], 2)}")
print(f"    taux DMTO territorialisés présents : {sorted(g['taux_dmto_pct'].round(2).unique())}")
print(f"    ZE avec taux moyen non entier (ZE à cheval sur des départements à taux différents) : {int((~g['taux_dmto_pct'].round(2).isin([6.32, 5.81, 5.09])).sum())}")
for e in md["bascule_la_plus_favorable_au_mobile"][:3] + md["bascule_la_moins_favorable_au_mobile"][:2]:
    row = g.loc[e["ze"]]
    cmp(f"  {e['name'].strip()} années équivalentes", e["annees_equivalentes"], round(row["annees"], 1), 0.05)
print(f"  Paris (1109) : 72,2 ans publié — mais 75 est HORS du périmètre de la charge (communes 75 : "
      f"{int((commune_ze[commune_ze['ze']=='1109']['code'].str[:2]=='75').sum())} sur {int((commune_ze['ze']=='1109').sum())} communes de la ZE)")

# ------------------------------------------------------------- 5. grids
hdr("5. Grilles M-A et M-C")
gis = detente["structurelle"].fillna(0).sum()
besoin = detente["besoin_mobilisation"].sum()
ma = ART["m_a_canal_incitatif"]
cmp("gisement effectif", ma["gisement_effectif"], round(gis))
cmp("besoin", ma["besoin"], round(besoin))
for gpub in ma["grille"]:
    share = min(1.0, gpub["taux_pct_an"] / 100 * gpub["horizon_ans"])
    cmp(f"  M-A {gpub['taux']} {gpub['horizon_ans']} ans sorties", gpub["sorties"], round(gis * share), 1)
    cmp(f"  M-A {gpub['taux']} {gpub['horizon_ans']} ans couverture", gpub["couverture_besoin"], round(gis * share / besoin, 3), 0.0005)
print(f"  H-14 : 6 700 sorties / 4 ans ≈ 3 % ⇒ stock ciblé implicite {6700/0.03:,.0f} ; 0,75 %/an × 10 ans = 7,5 % du gisement")
travaux = (detente["renovables"] * cu).sum()
neuf_c = detente["deficit_neuf"].sum() * remob.PRIX_REVIENT_NEUF_EUR_2023
mc = ART["m_c_bail_rehabilitation"]
cmp("M-C travaux plein Md€", mc["investissement_travaux_plein_mdeur"], round(travaux / 1e9, 1), 0.05)
cmp("M-C neuf Md€", mc["investissement_neuf_mdeur"], round(neuf_c / 1e9, 1), 0.05)
ren_all = detente["renovables"].sum()
for gpub in mc["grille_consentement"]:
    cc = gpub["consentement_pct"] / 100
    cmp(f"  M-C {gpub['consentement_pct']} % logements rénovés", gpub["logements_renoves"], round(ren_all * cc), 1)
    cmp(f"  M-C {gpub['consentement_pct']} % couverture", gpub["couverture_besoin"], round((ren_all * cc + detente["deficit_neuf"].sum()) / besoin, 2), 0.005)
    cmp(f"  M-C {gpub['consentement_pct']} % invest total Md€", gpub["investissement_total_mdeur"], round((travaux * cc + neuf_c) / 1e9, 1), 0.05)
print(f"  → à 10 % de consentement, {detente['deficit_neuf'].sum()/ (ren_all*0.1 + detente['deficit_neuf'].sum()):.0%} de la couverture 0,37 vient du NEUF (déficit), pas du bail")
h = detente.join(cu.rename("cu"), how="inner")
h["surface"] = surface
h["loyer_travaux"] = h["cu"] * af30 / (1 - opex) / 12 / h["surface"]
h["loyer_social"] = loyer_social
h["loyer_marche"] = loyer_marche
cmp("M-C loyer travaux médian €/m²", mc["loyer_equilibre_travaux_m2"]["median"], round(h["loyer_travaux"].median(), 2), 0.005)
print(f"    quantiles {q(h['loyer_travaux'], 2)}")
hw = h.dropna(subset=["loyer_social", "loyer_marche"])
cmp("M-C n_ze_avec_loyers", mc["n_ze_avec_loyers"], len(hw))
cmp("M-C n ZE travaux ≤ social", mc["n_ze_travaux_sous_social"], int((hw["loyer_travaux"] <= hw["loyer_social"]).sum()))

# ------------------------------------------------------------- 6. sensitivities
hdr("6. Sensibilités une-à-une et coins (M-B)")


def run(disc: float, rate: float, years: float, ox: float) -> dict[str, float]:
    rr = rate / 100
    a = rr / (1 - (1 + rr) ** (-years))
    unit = f["prix_median"] * disc + f["cu"]
    inv = f["renovables"] * unit + f["neuf"]
    ler = unit * a / (1 - ox) / 12 / f["surface"]
    len_ = remob.PRIX_REVIENT_NEUF_EUR_2023 * a / (1 - ox) / 12 / f["surface"]
    sub = ((ler - f["loyer_social"]).clip(lower=0) * f["surface"] * 12 * f["renovables"]).sum() + (
        (len_ - f["loyer_social"]).clip(lower=0) * f["surface"] * 12 * f["deficit_neuf"]
    ).sum()
    wr = f.dropna(subset=["loyer_marche", "loyer_social"]).index
    return {
        "investissement_mdeur": round(inv.sum() / 1e9, 1),
        "annuite_mdeur_an": round(inv.sum() * a / 1e9, 2),
        "loyer_equilibre_renove_median_m2": round(ler.median(), 2),
        "n_ze_equilibre_renove_sous_marche": int((ler[wr] <= f.loc[wr, "loyer_marche"]).sum()),
        "subvention_equilibre_social_mdeur_an": round(sub / 1e9, 2),
    }


sens = ART["m_b_operateur_acquisition"]["sensibilite"]
cen = (H["H-15"].central_value, H["H-16"].central_value, H["H-17"].central_value, H["H-18"].central_value)
cases = {}
for d in (0.5, 0.75, 1.0):
    cases[f"h15_decote/{d:g}"] = (sens["h15_decote"][f"{d:g}"], run(d, cen[1], cen[2], cen[3]))
for rt in (1.5, 2.3, 2.81):
    cases[f"h16_taux_pct/{rt:g}"] = (sens["h16_taux_pct"][f"{rt:g}"], run(cen[0], rt, cen[2], cen[3]))
for y in (30, 40, 50):
    cases[f"h17_duree_ans/{y:g}"] = (sens["h17_duree_ans"][f"{y:g}"], run(cen[0], cen[1], y, cen[3]))
for o in (0.4, 0.549, 0.6):
    cases[f"h18_charges/{o:g}"] = (sens["h18_charges"][f"{o:g}"], run(cen[0], cen[1], cen[2], o))
cases["favorable"] = (sens["favorable"], run(0.5, 1.5, 50, 0.4))
cases["defavorable"] = (sens["defavorable"], run(1.0, 2.81, 30, 0.6))
for name, (p, rc) in cases.items():
    for k in rc:
        cmp(f"  {name} {k}", p[k], rc[k], 0.0051 if isinstance(rc[k], float) else 0)
print(f"\n  Variante S-40 stricte : annuités = 43,8 % du loyer net (et non 1 − 0,549 = 45,1 %) → loyer médian "
      f"{(f['unit_renove'] * af / 0.438 / 12 / f['surface']).median():.2f} €/m² (+{(0.451/0.438-1)*100:.1f} %)")

# ------------------------------------------------------------- 7. internal coherences
hdr("7. Cohérences internes")
missing_dvf = detente.index.difference(prix.index)
for z in missing_dvf:
    row = detente.loc[z]
    print(f"ZE tendue SANS prix DVF : {z} {row['ze_name']} — rénovables {row['renovables']:.0f}, déficit {row['deficit_neuf']:.0f}, "
          f"besoin {row['besoin_mobilisation']:.0f} ; département(s) : {sorted(set(commune_ze[commune_ze['ze']==z]['code'].str[:2]))}")
print(f"→ 136 544 − {detente.loc[missing_dvf, 'renovables'].sum():.0f} = {136544 - detente.loc[missing_dvf, 'renovables'].sum():.0f} (publié M-B : 136 353)")
print(f"   part de l'investissement M-B hors champ (si l'on valorisait cette ZE au coût unitaire médian) : "
      f"{detente.loc[missing_dvf, 'renovables'].sum() * f['unit_renove'].median() / 1e9:.2f} Md€ ; "
      f"son déficit au neuf {detente.loc[missing_dvf, 'deficit_neuf'].sum():.0f} × 169 200 = {detente.loc[missing_dvf, 'deficit_neuf'].sum()*169200/1e9:.3f} Md€ "
      f"— absents des 44,6 (mais présents dans les 15,8 de M-C/R-09)")
no_soc = f[f["loyer_social"].isna()]
no_mar = f[f["loyer_marche"].isna()]
print(f"\nZE M-B sans loyer social : {len(no_soc)} → {[(z, n) for z, n in zip(no_soc.index, no_soc['ze_name'])]}")
print(f"ZE M-B sans loyer de marché : {len(no_mar)} → {[(z, n) for z, n in zip(no_mar.index, no_mar['ze_name'])]}")
print(f"  rénovables dans les ZE sans loyer social : {no_soc['renovables'].sum():.0f} ; déficit neuf : {no_soc['deficit_neuf'].sum():.0f} ; "
      f"leur loyer d'équilibre rénové : {no_soc['loyer_eq_renove'].round(2).tolist()}")
med_soc = f["loyer_social"].median()
sub_missing = (((no_soc["loyer_eq_renove"] - med_soc).clip(lower=0) * no_soc["surface"] * 12 * no_soc["renovables"]).sum()
               + ((no_soc["loyer_eq_neuf"] - med_soc).clip(lower=0) * no_soc["surface"] * 12 * no_soc["deficit_neuf"]).sum())
print(f"  subvention comptée pour ces ZE : 0 (fillna) ; au loyer social médian {med_soc:.2f} €/m² elle vaudrait {sub_missing/1e6:.1f} M€/an "
      f"({sub_missing/2.38e9*100:.1f} % des 2,38 Md€)")
print(f"  ZE M-C (97) sans loyer social : {int(h['loyer_social'].isna().sum())} ; sans marché : {int(h['loyer_marche'].isna().sum())}")

print("\nMédianes simples vs pondérées (loyer d'équilibre rénové) :")


def wmedian(v: pd.Series, w: pd.Series) -> float:
    m = v.notna() & w.notna()
    v, w = v[m], w[m]
    o = np.argsort(v.to_numpy())
    cv = np.cumsum(w.to_numpy()[o])
    return float(v.to_numpy()[o][np.searchsorted(cv, cv[-1] / 2)])


print(f"  médiane simple (1 ZE = 1 poids) : {f['loyer_eq_renove'].median():.2f} ; pondérée par rénovables : {wmedian(f['loyer_eq_renove'], f['renovables']):.2f} ; "
      f"moyenne pondérée par rénovables : {(f['loyer_eq_renove']*f['renovables']).sum()/f['renovables'].sum():.2f} ; "
      f"pondérée par les RP : {wmedian(f['loyer_eq_renove'], rp_ze.reindex(f.index)):.2f}")
print(f"  ratio équilibre/marché : simple {ratio_m.median():.2f} ; pondéré rénovables {wmedian(ratio_m, f.loc[with_rents.index, 'renovables']):.2f}")
print(f"  M-D années équivalentes : médiane simple {g['annees'].median():.1f} ; pondérée par le parc de logements des ZE "
      f"{wmedian(g['annees'], census.merge(commune_ze, on='code').groupby('ze')['P22_LOG'].sum().reindex(g.index)):.1f} ; "
      f"pondérée par les ventes DVF {wmedian(g['annees'], g['n_ventes']):.1f}")
print(f"  M-D péage fiscal : médiane simple {g['peage_fiscal'].median():.0f} € ; pondérée par ventes {wmedian(g['peage_fiscal'], g['n_ventes']):.0f} €")
print(f"  M-C loyer travaux : simple {h['loyer_travaux'].median():.2f} ; pondéré rénovables {wmedian(h['loyer_travaux'], h['renovables']):.2f}")
print(f"\nSurface implicite DVF vs surface C-07 (96 ZE) : ratio médian {(f['surface_implicite_dvf']/f['surface']).median():.2f} "
      f"(min {(f['surface_implicite_dvf']/f['surface']).min():.2f}, max {(f['surface_implicite_dvf']/f['surface']).max():.2f}) ; "
      f"loyer d'équilibre rénové médian à la surface implicite : {(f['unit_renove']*af/(1-opex)/12/f['surface_implicite_dvf']).median():.2f} €/m²")
print(f"NaN structurelle dans les ZE tendues (gisement inconnu, secret LOVAC) : {int(detente['structurelle'].isna().sum())}")
print(f"Somme de contrôle : rénovables + déficit = besoin ? {abs((detente['renovables']+detente['deficit_neuf']-detente['besoin_mobilisation']).abs().max()) < 1e-6}")
print(f"Somme de contrôle M-B : dont_acq + dont_ren + dont_neuf (arrondis) = {c['dont_acquisition_mdeur']+c['dont_renovation_mdeur']+c['dont_neuf_mdeur']:.1f} vs investissement {c['investissement_mdeur']}")
print(f"Somme de contrôle subvention : {c['dont_renove_mdeur_an']+c['dont_neuf_mdeur_an']:.2f} vs {c['subvention_equilibre_social_mdeur_an']}")
print("\nFIN")
