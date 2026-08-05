# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
# ---

# %% [markdown]
# # Exploration 10 — Le coût de la remobilisation du gisement (suite H-05)
#
# **Régime exploratoire** (méthode Métabolisme §2.1). R-07 a établi que le
# gisement structurel des zones tendues couvre 1,65 fois le besoin de
# détente ; R-08 que ce gisement est du bâti ancien dont la remobilisation
# a un coût. Ici on chiffre l'ordre de grandeur : **que coûterait la
# remise en usage, et comment cela se compare-t-il à construire à la
# place ?** (décisions du 2026-08-05, C-07)
#
# Modèle :
#
# `coût_logement(ZE) = [part_maison × H-09 × 114,3 m² +
#                       (1 − part_maison) × H-10 × 65,5 m²]
#                      × 1,055 (TVA, S-17) × facteur_IPEA (S-19)`
#
# - **H-09/H-10** : coûts d'une rénovation complète et performante
#   (~BBC), maison 406 € HT/m² (348-496), collectif 250 (200-300) —
#   euros 2016, S-17 (Enertech pour l'ADEME).
# - **Surfaces** : moyennes S-12 (maisons 114,3 m², appartements 65,5).
# - **Actualisation** : IPEA résidentiel (S-19), moyenne 2016 → moyenne
#   2023 (l'année du comparateur), recalculée depuis le fichier figé.
# - **Comparateur** : prix de revient moyen d'un logement social neuf en
#   2023 : 169 200 € (S-18, Banque des Territoires) — conservateur (la
#   promotion libre est plus chère).
#
# Précautions : rénovation ÉNERGÉTIQUE performante comme proxy de la
# remise en usage (ni reprises structurelles lourdes, ni simple
# rafraîchissement — sens du biais indéterminé) ; ordre de grandeur,
# pas un devis.

# %%
import re
import zipfile
from pathlib import Path

import pandas as pd

ROOT = Path.cwd()
while not (ROOT / "pyproject.toml").exists():
    ROOT = ROOT.parent
RAW = ROOT / "data" / "raw"

H08_PCT = 6.0  # seuil de fluidité (H-08)
H09_MAISON = (406.0, 348.0, 496.0)  # central, bas, haut — € HT 2016/m² (S-17)
H10_COLLECTIF = (250.0, 200.0, 300.0)
SURFACE_MAISON_M2 = 114.3  # moyennes S-12 (enquête Logement 2020)
SURFACE_APPART_M2 = 65.5
TVA_RENOVATION = 1.055  # S-17
PRIX_REVIENT_NEUF_2023 = 169_200.0  # S-18, €/logement social neuf

PLM = {"751": "75056", "6938": "69123", "132": "13055"}


def plm_parent(code: str) -> str:
    """Map a PLM arrondissement code to its parent commune, else identity."""
    return next((city for p, city in PLM.items() if code.startswith(p)), code)


def to_num(series: pd.Series) -> pd.Series:
    """Parse LOVAC numbers: nbsp thousands separators, 's' (secret) -> NaN."""
    cleaned = series.astype("string").str.replace(r"[\s\xa0]", "", regex=True)
    return pd.to_numeric(cleaned.replace("s", pd.NA), errors="coerce")


# %% [markdown]
# ## 1. Facteur d'actualisation IPEA 2016 → 2023 (S-19)

# %%
xml = (RAW / "insee-ipea-residentiel-011779962.xml").read_text(encoding="utf-8")
obs = re.findall(r'TIME_PERIOD="(\d{4})-Q[1-4]" OBS_VALUE="([\d.]+)"', xml)
ipea = pd.DataFrame(obs, columns=["annee", "valeur"]).astype({"valeur": float})
annual = ipea.groupby("annee")["valeur"].agg(["mean", "count"])
facteur_ipea = annual.loc["2023", "mean"] / annual.loc["2016", "mean"]
print(f"IPEA moyenne 2016 : {annual.loc['2016', 'mean']:.2f} "
      f"({int(annual.loc['2016', 'count'])} trim) ; 2023 : "
      f"{annual.loc['2023', 'mean']:.2f} → facteur {facteur_ipea:.3f}")

# %% [markdown]
# ## 2. Reconstruire les ZE tendues (R-07) et la part maison (S-11)

# %%
with zipfile.ZipFile(RAW / "insee-rp-base-cc-logement-2022.zip") as zf:
    with zf.open("base-cc-logement-2022.CSV") as fh:
        census = pd.read_csv(
            fh, sep=";", dtype=str,
            usecols=["CODGEO", "P22_LOG", "P22_LOGVAC", "P22_RPMAISON", "P22_RPAPPART"],
        )
census = pd.DataFrame(
    {
        "code": census["CODGEO"].str.strip().map(plm_parent),
        "parc": pd.to_numeric(census["P22_LOG"], errors="coerce"),
        "vacants": pd.to_numeric(census["P22_LOGVAC"], errors="coerce"),
        "rp_maison": pd.to_numeric(census["P22_RPMAISON"], errors="coerce"),
        "rp_appart": pd.to_numeric(census["P22_RPAPPART"], errors="coerce"),
    }
).drop_duplicates(subset="code", keep="first")

with zipfile.ZipFile(RAW / "insee-table-appartenance-geo-communes-2026.zip") as zf:
    with zf.open("table-appartenance-geo-communes-2026.xlsx") as fh:
        appartenance = pd.read_excel(fh, sheet_name="COM", header=5, engine="calamine", dtype=str)
com_ze = appartenance[["CODGEO", "ZE2020"]].dropna().rename(
    columns={"CODGEO": "code", "ZE2020": "ze"}
)

communes_lovac = pd.read_csv(
    RAW / "lovac-opendata-communes26.csv", sep=";", encoding="cp1252", dtype=str
)
communes_lovac.columns = [c.strip() for c in communes_lovac.columns]
lovac = pd.DataFrame(
    {
        "code": communes_lovac["CODGEO_26"].str.strip().map(plm_parent),
        "structurelle": to_num(communes_lovac["pp_vacant_plus_2ans_24"]),
    }
)

ze = census.merge(com_ze, on="code", how="left").dropna(subset=["ze"]).groupby("ze")[
    ["parc", "vacants", "rp_maison", "rp_appart"]
].sum()
ze = ze.join(
    lovac.merge(com_ze, on="code", how="left").dropna(subset=["ze"])
    .groupby("ze")[["structurelle"]].sum(min_count=1),
    how="inner",
)
ze["part_maison"] = ze["rp_maison"] / (ze["rp_maison"] + ze["rp_appart"])
ze["disponibles"] = ze["vacants"] - ze["structurelle"]
ze["taux_disponible_pct"] = ze["disponibles"] / ze["parc"] * 100
t = H08_PCT / 100
tense = ze[ze["taux_disponible_pct"] < H08_PCT].copy()
tense["besoin"] = t * tense["parc"] - tense["disponibles"]
print(f"{len(tense)} ZE tendues ; besoin total {tense['besoin'].sum():,.0f} ; "
      f"gisement {tense['structurelle'].sum():,.0f} (contrôle R-07)")

# %% [markdown]
# ## 3. Coût unitaire de remise en usage par ZE, et agrégats

# %%
names = pd.read_excel(
    RAW / "insee-emploi-zone-1998-2018.xlsx", sheet_name="Emploi total - ZE",
    header=4, engine="calamine",
)["Zone d'emploi"].astype("string").str.extract(r"^(\d{4}) - (.*)$").dropna()
tense = tense.join(names.set_index(0)[1].rename("ze_nom"), how="left")


def cout_unitaire(part_maison: pd.Series, h09: float, h10: float) -> pd.Series:
    ht_2016 = part_maison * h09 * SURFACE_MAISON_M2 + (1 - part_maison) * h10 * SURFACE_APPART_M2
    return ht_2016 * TVA_RENOVATION * facteur_ipea


for label, h09, h10 in [
    ("bas", H09_MAISON[1], H10_COLLECTIF[1]),
    ("central", H09_MAISON[0], H10_COLLECTIF[0]),
    ("haut", H09_MAISON[2], H10_COLLECTIF[2]),
]:
    cu = cout_unitaire(tense["part_maison"], h09, h10)
    cout_detente = (tense["besoin"] * cu).sum()
    cout_gisement = (tense["structurelle"] * cu).sum()
    print(f"{label:8s} coût unitaire moyen pondéré {cu.mul(tense['besoin']).sum() / tense['besoin'].sum():,.0f} € TTC 2023 ; "
          f"détente {cout_detente / 1e9:.1f} Md€ ; gisement entier {cout_gisement / 1e9:.1f} Md€")

cu_central = cout_unitaire(tense["part_maison"], H09_MAISON[0], H10_COLLECTIF[0])
cout_detente_central = (tense["besoin"] * cu_central).sum()
cout_neuf = tense["besoin"].sum() * PRIX_REVIENT_NEUF_2023
print()
print(f"CONSTRUIRE À LA PLACE (S-18) : {tense['besoin'].sum():,.0f} logements × "
      f"{PRIX_REVIENT_NEUF_2023:,.0f} € = {cout_neuf / 1e9:.1f} Md€")
print(f"ratio neuf / remobilisation (central) : {cout_neuf / cout_detente_central:.1f}")

# %%
tense["cout_detente_meur"] = tense["besoin"] * cu_central / 1e6
top = tense.nlargest(10, "cout_detente_meur")
print("les 10 plus gros coûts de détente (hypothèses centrales, M€ TTC 2023) :")
print(top[["ze_nom", "besoin", "part_maison", "cout_detente_meur"]]
      .assign(cout_neuf_meur=top["besoin"] * PRIX_REVIENT_NEUF_2023 / 1e6)
      .round(1).to_string())

# %% [markdown]
# ## Observations provisoires (vérifiées depuis les sorties ci-dessus)
#
# 1. **L'ordre de grandeur de la détente par remobilisation : ~12,5 Md€**
#    (hypothèses centrales ; 10,6-15,3 Md€ sur les plages H-09/H-10),
#    soit un coût unitaire moyen pondéré de ~43 900 € TTC 2023 par
#    logement rendu disponible (rénovation complète performante, surfaces
#    moyennes S-12, mix maison/appartement de chaque ZE, actualisation
#    IPEA ×1,267).
# 2. **Construire les mêmes 285 665 logements coûterait ~48,3 Md€** au
#    prix de revient du logement social 2023 (comparateur conservateur :
#    la promotion libre est plus chère) — **la remobilisation est ~3,9
#    fois moins chère que la construction neuve**, et le ratio tient sur
#    toute la plage (3,2 à 4,6). Remobiliser la totalité du gisement
#    structurel des ZE tendues (472 022 logements) coûterait ~20,2 Md€
#    (17,0-24,5).
# 3. **La géographie du coût suit le besoin** : Bordeaux (509 M€), Toulon
#    (462), Nantes (411), Marseille (348)… — dans chacune, le neuf
#    coûterait 3 à 4 fois plus (Bordeaux 2 010 M€, Toulon 2 065).
# 4. Limites à porter avec le chiffre : la rénovation complète
#    performante est un PROXY de la remise en usage (elle ne couvre ni
#    les reprises structurelles lourdes ni le foncier/acquisition, mais
#    dépasse le strict minimum de louabilité — sens du biais
#    indéterminé) ; coûts Enertech observés sur des opérations
#    volontaires (sélection) ; le chiffre est un ordre de grandeur
#    d'INVESTISSEMENT, pas un coût public (les aides n'en sont qu'une
#    fraction) ; et R-08 rappelle que le verrou n'est pas seulement
#    financier (blocages de propriété, DOM).
#
# Prochaine étape de stabilisation : R-09 + I-09 + C-07 + L-14 dans le
# graphe.

# %%
