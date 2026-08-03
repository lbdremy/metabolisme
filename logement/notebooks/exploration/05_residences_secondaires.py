# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
# ---

# %% [markdown]
# # Exploration 05 — Résidences secondaires, coût et vacance (capacité saisonnière)
#
# **Régime exploratoire** (méthode Métabolisme §2.1). Instruction de l'axe
# ouvert par I-02 et I-04 : la « capacité saisonnière retirée » (INTRO §7).
# L'exception corse de R-04 (coût élevé ET vacance élevée) suggère que la
# part de résidences secondaires structure certains marchés locaux.
#
# Question : la part de résidences secondaires (recensement 2022, S-11)
# explique-t-elle une partie de la géographie du coût (R-04) et de la
# vacance structurelle (R-02/R-03) par zone d'emploi ?
#
# Précautions : parc entier côté recensement vs parc privé côté LOVAC
# (L-06) ; COG 2025 (S-11) vs COG 2026 (table d'appartenance) — écarts
# marginaux ; rappel V-01 : les résidences secondaires sont des usages
# réels, pas un gisement — on mesure une structure de marché, pas une
# « réserve ».

# %%
import zipfile
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

ROOT = Path.cwd()
while not (ROOT / "pyproject.toml").exists():
    ROOT = ROOT.parent
RAW = ROOT / "data" / "raw"
C1, C2, C3, C4 = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"  # palette validée (dataviz)

# %% [markdown]
# ## 1. Part des résidences secondaires par zone d'emploi (recensement 2022)

# %%
with zipfile.ZipFile(RAW / "insee-rp-base-cc-logement-2022.zip") as zf:
    with zf.open("base-cc-logement-2022.CSV") as fh:
        rp = pd.read_csv(
            fh, sep=";", dtype=str,
            usecols=["CODGEO", "P22_LOG", "P22_RP", "P22_RSECOCC", "P22_LOGVAC"],
        )
for col in ("P22_LOG", "P22_RP", "P22_RSECOCC", "P22_LOGVAC"):
    rp[col] = pd.to_numeric(rp[col], errors="coerce")

PLM = {"751": "75056", "6938": "69123", "132": "13055"}


def plm_parent(code: str) -> str:
    """Map a PLM arrondissement code to its parent commune, else identity."""
    return next((city for p, city in PLM.items() if code.startswith(p)), code)


rp["code"] = rp["CODGEO"].str.strip().map(plm_parent)
# The base lists both PLM parent communes and arrondissements: drop the
# arrondissement rows once mapped (they duplicate the parent totals).
rp = rp.drop_duplicates(subset="code", keep="first")

with zipfile.ZipFile(RAW / "insee-table-appartenance-geo-communes-2026.zip") as zf:
    with zf.open("table-appartenance-geo-communes-2026.xlsx") as fh:
        appartenance = pd.read_excel(fh, sheet_name="COM", header=5, engine="calamine", dtype=str)
com_ze = appartenance[["CODGEO", "ZE2020"]].dropna().rename(
    columns={"CODGEO": "code", "ZE2020": "ze"}
)

merged = rp.merge(com_ze, on="code", how="inner")
print(f"{len(rp)} communes recensement, {len(merged)} appariées à une ZE "
      f"({len(rp) - len(merged)} perdues, COG 2025 vs 2026)")
ze_rs = merged.groupby("ze")[["P22_LOG", "P22_RP", "P22_RSECOCC", "P22_LOGVAC"]].sum()
ze_rs["part_rs_pct"] = ze_rs["P22_RSECOCC"] / ze_rs["P22_LOG"] * 100
ze_rs["part_vac_rp_pct"] = ze_rs["P22_LOGVAC"] / ze_rs["P22_LOG"] * 100
print(f"part RS nationale : {ze_rs['P22_RSECOCC'].sum() / ze_rs['P22_LOG'].sum() * 100:.1f} % ; "
      f"médiane ZE {ze_rs['part_rs_pct'].median():.1f} % ; max {ze_rs['part_rs_pct'].max():.1f} %")

# %% [markdown]
# ## 2. Croisement avec le coût (R-04) et la vacance structurelle (R-03)
#
# On réutilise les artefacts publiés (mêmes chiffres que les documents de
# preuve) plutôt que de recalculer.

# %%
import json

r04 = json.loads((ROOT / "data" / "processed" / "cout-residentiel-ze.json").read_text())
# Rebuild the per-ZE cost frame quickly from the stabilized core (same code as R-04).
from logement.core import cout, lovac, ze as ze_core
from logement.shell import build

cost_ze = cout.cost_index_by_ze(
    cout.parse_loyers(pd.read_csv(RAW / build.LOYERS_FILE, sep=";", encoding="cp1252", dtype=str)),
    lovac.parse_territories(
        pd.read_csv(RAW / build.LOVAC_COMMUNES, sep=";", encoding="cp1252", dtype=str),
        code_col="CODGEO_26", name_col="LIBGEO_26",
    ),
    com_ze,
    cout.parse_filosofi(
        pd.read_csv(
            zipfile.ZipFile(RAW / build.FILOSOFI_ZIP).open(build.FILOSOFI_CSV),
            sep=";", dtype=str, usecols=["GEO", "GEO_OBJECT", "FILOSOFI_MEASURE", "OBS_VALUE"],
        ),
        geo_object="ZE2020", measure="MED_SL",
    ),
)
names = ze_core.parse_emploi_ze(
    pd.read_excel(RAW / build.EMPLOI_ZE_FILE, sheet_name="Emploi total - ZE", header=4,
                  engine="calamine")
)["ze_name"]
cross = ze_rs.join(cost_ze, how="inner").join(names, how="left")
print(f"{len(cross)} ZE croisées")
for a, b in [("part_rs_pct", "taux_structurelle_pct"), ("part_rs_pct", "indice_cout_pct")]:
    corr = cross[a].rank().corr(cross[b].rank())
    print(f"Spearman {a} × {b} : {corr:.2f}")

touristic = cross["part_rs_pct"] > 20
print(f"\nZE à plus de 20 % de résidences secondaires : {touristic.sum()}")
print("  vacance structurelle médiane :",
      round(cross.loc[touristic, 'taux_structurelle_pct'].median(), 1), "% vs",
      round(cross.loc[~touristic, 'taux_structurelle_pct'].median(), 1), "% ailleurs")
print("  indice de coût médian :",
      round(cross.loc[touristic, 'indice_cout_pct'].median(), 2), "vs",
      round(cross.loc[~touristic, 'indice_cout_pct'].median(), 2), "ailleurs")
print("\nTop part RS :")
print(cross.nlargest(8, "part_rs_pct")[["ze_name", "part_rs_pct", "indice_cout_pct", "taux_structurelle_pct"]].round(2).to_string())

# %%
fig, ax = plt.subplots(figsize=(9, 6))
ax.scatter(cross["part_rs_pct"], cross["indice_cout_pct"], s=30, alpha=0.5, color=C1,
           edgecolors="white", linewidths=0.5, label="ZE")
hi = cross[cross["part_rs_pct"] > 30]
for _, row in hi.iterrows():
    ax.annotate(row["ze_name"], (row["part_rs_pct"], row["indice_cout_pct"]),
                fontsize=7, color="#555555", xytext=(4, 2), textcoords="offset points")
ax.set_xlabel("part des résidences secondaires et logements occasionnels (%)")
ax.set_ylabel("indice de coût (loyer annuel m² / niveau de vie médian, %)")
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f %%"))
ax.set_title("Zones d'emploi : part de résidences secondaires × pression du coût\n"
             "(recensement 2022, loyers 2025, revenus 2021)")
ax.grid(alpha=0.25)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Observations provisoires (à stabiliser avant toute publication)
#
# 1. **CORRECTION de l'interprétation de R-04** : les ZE à coût élevé ET
#    vacance élevée (0401 L'Est, 0402 L'Ouest, 0404 Le Sud, 0205 Le Sud)
#    sont des ZE de **La Réunion et de Martinique**, pas de Corse (codes
#    vérifiés dans la table d'appartenance : dep 974/972). Le cumul est un
#    phénomène ultramarin de revenus faibles, prolongeant R-02 — pas un
#    phénomène de résidences secondaires (leur part RS y est de 2,7-12,9 %,
#    sous la médiane nationale).
# 2. **À l'échelle ZE, la part de résidences secondaires n'explique ni la
#    vacance ni le coût** : Spearman +0,17 avec le taux de vacance
#    structurelle, −0,05 avec l'indice de coût. Les 56 ZE à plus de 20 % de
#    RS ont même une vacance structurelle PLUS BASSE (médiane 2,6 % contre
#    3,3 %) et un coût à peine supérieur (0,67 vs 0,59) : les marchés
#    touristiques (Briançon 65,5 % de RS, Tarentaise, Maurienne,
#    Mont-Blanc, Sainte-Maxime) gardent leur parc en usage — comme
#    résidence secondaire précisément.
# 3. **La « capacité saisonnière retirée » (INTRO §7) ne se lit donc pas
#    dans la vacance ni dans notre indice de coût à cette échelle** : elle
#    est dans la catégorie RS elle-même (9,7 % du parc national, jusqu'à
#    65 % localement) et dans ses effets d'éviction infra-territoriaux —
#    l'accès des résidents permanents (prix d'achat, offre locative à
#    l'année) n'est pas mesuré par nos indicateurs actuels.
#    Avec un critère explicite (RS > 20 % ET vacance > 5 %, stabilisé en
#    R-05), **12 ZE cumulent RS et vacance** — dont six corses (Corte
#    39 %/10,4 %, Ghisonaccia, Porto-Vecchio, Propriano, Ajaccio, Bastia)
#    et des ZE rurales touristiques (Sarlat, Millau, Ussel, Saint-Flour) :
#    le cumul existe, il est corse et rural-touristique, pas alpin.
# 4. Limites : parc entier (recensement) vs parc privé (LOVAC) pour les
#    taux (L-06) ; COG 2025 vs 2026 (0 commune perdue à la jointure) ;
#    rappel V-01 — la RS est un usage réel, pas un gisement.
#
# Prochaine étape de stabilisation : R-05 (part RS par ZE et croisements)
# + I-05 (correction DOM et non-effet RS à l'échelle ZE) dans le graphe.

# %%
