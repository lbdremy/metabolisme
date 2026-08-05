# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
# ---

# %% [markdown]
# # Exploration 09 — État du bâti et vacance structurelle (H-05)
#
# **Régime exploratoire** (méthode Métabolisme §2.1). Première instruction
# de l'hypothèse directrice **H-05** (inefficacités institutionnelles /
# blocages au niveau propriété). Enjeu posé par R-07/I-07 : la couverture
# du manque par le gisement (1,65) suppose que les ~472 000 logements
# structurellement vacants des zones tendues soient REMOBILISABLES — or la
# vacance structurelle est, par définition, celle qui ne revient pas
# spontanément sur le marché. Pourquoi ? I-03/I-04 pointent l'état du bâti
# et les successions.
#
# Ce que l'open data permet (décisions du 2026-08-05) :
#
# - **État du bâti, maille ZE** : âge du parc (part des RP d'avant 1946,
#   S-11) et inconfort sanitaire (part des RP SANS baignoire/douche/WC
#   intérieurs, S-11) × taux de vacance structurelle (LOVAC).
# - **État du bâti, étiquettes énergie** : extrait communal de la base DPE
#   ADEME (S-16, 15,3 M de diagnostics depuis 07/2021) — part F+G des
#   logements *diagnostiqués* par ZE. BIAIS DOCUMENTÉ : les DPE sont
#   réalisés à la vente/location, l'échantillon n'est pas le parc (l'ONRE
#   estime 13,9 % de F+G dans le parc au 01/01/2024 contre ~9,8 % des
#   diagnostics), et les logements vacants ne sont justement PAS
#   diagnostiqués tant qu'ils ne reviennent pas sur le marché.
# - **Frontières documentées** : PPPI (extraction sous convention
#   DREAL/DDT ; version open 2015 obsolète — méthodo FILOCOM abandonnée) ;
#   successions/indivisions (fichiers fonciers Cerema réservés aux acteurs
#   publics, pas de statistique notariale ouverte).
#
# Lecture : corrélations territoriales, PAS des causes au niveau logement
# (un territoire au bâti vieux peut avoir une vacance jeune, et
# inversement).

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

PLM = {"751": "75056", "6938": "69123", "132": "13055"}


def plm_parent(code: str) -> str:
    """Map a PLM arrondissement code to its parent commune, else identity."""
    return next((city for p, city in PLM.items() if code.startswith(p)), code)


def to_num(series: pd.Series) -> pd.Series:
    """Parse LOVAC numbers: nbsp thousands separators, 's' (secret) -> NaN."""
    cleaned = series.astype("string").str.replace(r"[\s\xa0]", "", regex=True)
    return pd.to_numeric(cleaned.replace("s", pd.NA), errors="coerce")


# %% [markdown]
# ## 1. Âge et inconfort du bâti par ZE (recensement 2022, S-11)

# %%
cols = ["CODGEO", "P22_RP", "P22_RP_ACHTOT", "P22_RP_ACH1919", "P22_RP_ACH1945", "P22_RP_BDWC"]
with zipfile.ZipFile(RAW / "insee-rp-base-cc-logement-2022.zip") as zf:
    with zf.open("base-cc-logement-2022.CSV") as fh:
        census = pd.read_csv(fh, sep=";", dtype=str, usecols=cols)
census = pd.DataFrame(
    {
        "code": census["CODGEO"].str.strip().map(plm_parent),
        **{c: pd.to_numeric(census[c], errors="coerce") for c in cols[1:]},
    }
).drop_duplicates(subset="code", keep="first")  # la base liste parents ET arrondissements

with zipfile.ZipFile(RAW / "insee-table-appartenance-geo-communes-2026.zip") as zf:
    with zf.open("table-appartenance-geo-communes-2026.xlsx") as fh:
        appartenance = pd.read_excel(fh, sheet_name="COM", header=5, engine="calamine", dtype=str)
com_ze = appartenance[["CODGEO", "ZE2020"]].dropna().rename(
    columns={"CODGEO": "code", "ZE2020": "ze"}
)

bati = (
    census.merge(com_ze, on="code", how="left")
    .dropna(subset=["ze"])
    .groupby("ze")[cols[1:]]
    .sum()
)
bati["part_avant_1946_pct"] = (
    (bati["P22_RP_ACH1919"] + bati["P22_RP_ACH1945"]) / bati["P22_RP_ACHTOT"] * 100
)
# PIÈGE VÉRIFIÉ : P22_RP_BDWC vaut 0 dans TOUTE la métropole (somme nulle sur
# 31,9 M de RP) — la question sanitaire n'est posée qu'aux DOM (761 934 sur
# 788 458 RP renseignées). L'inconfort n'est donc une lentille QUE pour les DOM.
bati["part_inconfort_pct"] = (1 - bati["P22_RP_BDWC"] / bati["P22_RP"]) * 100
dom_ze = bati.index.astype(str).str.startswith(("01", "02", "03", "04"))  # ZE DOM
# (les ZE « 00xx » sont les ZE métropolitaines multi-régions, pas des DOM)
bati.loc[~dom_ze, "part_inconfort_pct"] = float("nan")
print(f"{len(bati)} ZE ; part RP avant 1946 : min {bati['part_avant_1946_pct'].min():.1f} %, "
      f"médiane {bati['part_avant_1946_pct'].median():.1f} %, "
      f"max {bati['part_avant_1946_pct'].max():.1f} %")
print(f"part RP sans bain/douche/WC (DOM seulement, {int(dom_ze.sum())} ZE) : "
      f"min {bati['part_inconfort_pct'].min():.2f} %, "
      f"max {bati['part_inconfort_pct'].max():.2f} %")

# %% [markdown]
# ## 2. Croisement avec la vacance structurelle (LOVAC mill. 24)

# %%
communes_lovac = pd.read_csv(
    RAW / "lovac-opendata-communes26.csv", sep=";", encoding="cp1252", dtype=str
)
communes_lovac.columns = [c.strip() for c in communes_lovac.columns]
lovac = pd.DataFrame(
    {
        "code": communes_lovac["CODGEO_26"].str.strip().map(plm_parent),
        "structurelle": to_num(communes_lovac["pp_vacant_plus_2ans_24"]),
        "parc_prive": to_num(communes_lovac["ff_pp_total_24"]),
    }
)
vac = (
    lovac.merge(com_ze, on="code", how="left")
    .dropna(subset=["ze"])
    .groupby("ze")[["structurelle", "parc_prive"]]
    .sum(min_count=1)
)
vac["taux_structurelle_pct"] = vac["structurelle"] / vac["parc_prive"] * 100

names = pd.read_excel(
    RAW / "insee-emploi-zone-1998-2018.xlsx", sheet_name="Emploi total - ZE",
    header=4, engine="calamine",
)["Zone d'emploi"].astype("string").str.extract(r"^(\d{4}) - (.*)$").dropna()

cross = bati.join(vac, how="inner").join(names.set_index(0)[1].rename("ze_nom"), how="left")
cross = cross.dropna(subset=["taux_structurelle_pct"])
cross["dom"] = cross.index.astype(str).str.startswith(("01", "02", "03", "04"))
print(f"{len(cross)} ZE croisées (dont {int(cross['dom'].sum())} DOM)")
rho_all = cross["part_avant_1946_pct"].rank().corr(cross["taux_structurelle_pct"].rank())
metro = cross[~cross["dom"]]
rho_metro = metro["part_avant_1946_pct"].rank().corr(metro["taux_structurelle_pct"].rank())
print(f"Spearman part avant 1946 × vacance structurelle : {rho_all:.2f} "
      f"(toutes ZE) ; {rho_metro:.2f} (métropole seule)")
dom_only = cross[cross["dom"]]
rho_dom = dom_only["part_inconfort_pct"].rank().corr(dom_only["taux_structurelle_pct"].rank())
print(f"Spearman (DOM seulement, n={len(dom_only)}) inconfort sanitaire × vacance : {rho_dom:.2f}")

# %%
old_half = cross["part_avant_1946_pct"] > cross["part_avant_1946_pct"].median()
print(f"taux structurel médian : ZE au bâti le plus ancien {cross.loc[old_half, 'taux_structurelle_pct'].median():.1f} % "
      f"vs ZE au bâti le plus récent {cross.loc[~old_half, 'taux_structurelle_pct'].median():.1f} %")
print()
print("ZE au bâti le plus ancien (part avant 1946) :")
print(cross.nlargest(8, "part_avant_1946_pct")[
    ["ze_nom", "part_avant_1946_pct", "part_inconfort_pct", "taux_structurelle_pct"]
].round(2).to_string())
print()
print("ZE à la vacance structurelle la plus forte :")
print(cross.nlargest(8, "taux_structurelle_pct")[
    ["ze_nom", "part_avant_1946_pct", "part_inconfort_pct", "taux_structurelle_pct"]
].round(2).to_string())

# %%
fig, ax = plt.subplots(figsize=(9, 6))
sizes = (cross["structurelle"] / cross["structurelle"].max() * 600).clip(lower=8)
ax.scatter(cross["part_avant_1946_pct"], cross["taux_structurelle_pct"], s=sizes,
           alpha=0.45, color=C1, edgecolors="white", linewidths=0.5)
for _, row in pd.concat(
    [cross.nlargest(3, "part_avant_1946_pct"), cross.nlargest(3, "taux_structurelle_pct")]
).iterrows():
    ax.annotate(row["ze_nom"], (row["part_avant_1946_pct"], row["taux_structurelle_pct"]),
                fontsize=7, color="#555555", xytext=(4, 2), textcoords="offset points")
ax.set_xlabel("part des résidences principales construites avant 1946 (%)")
ax.set_ylabel("taux de vacance structurelle du parc privé (%)")
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f %%"))
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f %%"))
ax.set_title("Zones d'emploi : ancienneté du bâti × vacance structurelle\n"
             "(recensement 2022, LOVAC mill. 24 ; taille = volume de vacance)")
ax.grid(alpha=0.25)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 3. Étiquettes énergie des logements diagnostiqués par ZE (S-16)
#
# (section exécutée une fois l'extrait ADEME figé — voir en-tête pour le
# biais d'échantillon)

# %%
dpe_path = RAW / "ademe-dpe-existants-communes-etiquettes.csv"
if dpe_path.exists():
    # Format long produit par `logement acquire-dpe` : comptages agrégés par
    # l'API (commune × étiquette) — sans perte vs l'extrait ligne à ligne.
    dpe = pd.read_csv(dpe_path, sep=";", dtype=str).dropna(subset=["code_insee_ban"])
    dpe["code"] = dpe["code_insee_ban"].astype("string").str.strip().map(plm_parent)
    dpe["n"] = pd.to_numeric(dpe["n_dpe"], errors="coerce")
    counts = (
        dpe.groupby(["code", "etiquette_dpe"])["n"].sum().unstack(fill_value=0)
    )
    counts_ze = (
        counts.reset_index().merge(com_ze, on="code", how="left")
        .dropna(subset=["ze"]).groupby("ze")[list("ABCDEFG")].sum()
    )
    counts_ze["n_dpe"] = counts_ze.sum(axis=1)
    counts_ze["part_fg_pct"] = (counts_ze["F"] + counts_ze["G"]) / counts_ze["n_dpe"] * 100
    cross2 = cross.join(counts_ze[["n_dpe", "part_fg_pct"]], how="inner")
    print(f"{len(cross2)} ZE ; part F+G des diagnostiqués : "
          f"min {cross2['part_fg_pct'].min():.1f} %, médiane {cross2['part_fg_pct'].median():.1f} %, "
          f"max {cross2['part_fg_pct'].max():.1f} %")
    rho = cross2["part_fg_pct"].rank().corr(cross2["taux_structurelle_pct"].rank())
    print(f"Spearman part F+G × taux de vacance structurelle : {rho:.2f}")
    rho_age = cross2["part_fg_pct"].rank().corr(cross2["part_avant_1946_pct"].rank())
    print(f"Spearman part F+G × part avant 1946 : {rho_age:.2f}")
    print()
    print("ZE à la part F+G la plus forte :")
    print(cross2.nlargest(10, "part_fg_pct")[
        ["ze_nom", "part_fg_pct", "n_dpe", "part_avant_1946_pct", "taux_structurelle_pct"]
    ].round(2).to_string())
else:
    print("extrait ADEME absent ou incomplet — exécuter `uv run logement acquire-dpe`")

# %% [markdown]
# ## Observations provisoires (vérifiées depuis les sorties ci-dessus)
#
# 1. **En métropole, l'ancienneté du bâti est le corrélat territorial le
#    plus fort de la vacance structurelle relevé par la chaîne** :
#    Spearman 0,56 (contre −0,42 pour le coût, −0,36 pour l'emploi) ;
#    0,35 seulement quand on inclut les DOM (qui anticorrèlent). Taux
#    structurel médian 3,8 % dans la moitié des ZE au bâti le plus ancien
#    contre 2,7 %. Le haut du classement d'ancienneté est la diagonale
#    rurale déjà vue en R-02/R-03 (Avallon 52,4 % d'avant-1946,
#    Cosne-Cours-sur-Loire 46,9 %, Autun, Guéret…).
# 2. **Le proxy énergie converge** : part F+G des logements diagnostiqués
#    médiane 10,9 % par ZE, Spearman 0,40 avec la vacance structurelle en
#    métropole et 0,62 avec l'ancienneté — les deux mesures d'état du
#    bâti pointent les mêmes territoires (Ussel 37,3 % de F+G,
#    Saint-Flour, Avallon, Guéret, Tulle). Réserves : biais d'échantillon
#    (diagnostiqués ≠ parc, et les vacants durables ne sont pas
#    diagnostiqués) ; effet climat/altitude sur l'étiquette (Gap : 25,9 %
#    de F+G mais 2,2 % de vacance).
# 3. **Le contraste DOM inverse la lecture** : vacance médiane 11,0 % sur
#    un bâti récent (part avant 1946 médiane 1,9 %) et majoritairement
#    pourvu du confort sanitaire (inconfort médian 1,9 % ; jusqu'à 44,7 %
#    en Guyane) — l'état du bâti n'y explique pas la vacance record. La
#    piste restante du cadrage (H-05 : blocages de propriété, successions
#    et indivisions) devient donc la candidate par élimination — et c'est
#    précisément la frontière de données (fichiers fonciers restreints,
#    pas de statistique notariale ouverte) : à instruire, pas à affirmer.
#    Les DPE sont en outre quasi absents des DOM (obligation
#    récente outre-mer : Guyane 104 diagnostics, ZE 0303 zéro — seule ZE
#    perdue de la jointure).
# 4. **Frontières actées pour H-05** : PPPI (extraction sous convention
#    DREAL/DDT ; open data 2015 obsolète), fichiers fonciers/successions
#    (Cerema, acteurs publics), successions notariales (rien d'ouvert).
# 5. **Lecture H-05 (premier faisceau, corrélations territoriales, pas
#    causes logement par logement)** : en métropole, la vacance
#    structurelle est un phénomène du bâti ancien rural — la
#    remobilisation du gisement R-07 passe par l'état du bâti (coût de
#    remise en usage, rénovation énergétique) ; aux DOM, le verrou
#    présumé est le droit de propriété (successions), non mesurable en
#    open data à ce jour.
#
# Prochaine étape de stabilisation : R-08 (état du bâti × vacance par
# ZE) + I-08 + L-13 dans le graphe.

# %%
