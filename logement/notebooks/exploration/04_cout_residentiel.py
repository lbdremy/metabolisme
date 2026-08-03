# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
# ---

# %% [markdown]
# # Exploration 04 — Coût résidentiel, revenus et vacance (H-03)
#
# **Régime exploratoire** (méthode Métabolisme §2.1). Première instruction de
# l'hypothèse directrice **H-03** du cadrage (`INTRO.md` §4) : *le coût
# limite davantage l'accès que la capacité physique*. R-03/I-03 a montré que
# ~85 % de la vacance structurelle est dans des ZE où l'emploi croît — le
# coût est l'une des explications candidates du blocage.
#
# Indicateur exploratoire de pression du coût : **ratio loyer/revenu** =
# loyer d'annonce annuel au m² (S-09, appartements, 2025) rapporté à la
# médiane du niveau de vie (S-10, Filosofi 2021, €/UC/an), par zone
# d'emploi. Sans hypothèse de surface ni de composition de ménage, ce ratio
# n'est PAS un taux d'effort (D-09) — c'est un indice comparatif entre
# territoires (€/m²/an de loyer par € de niveau de vie).
#
# Précautions : loyers d'annonce ≠ loyers du parc en place (biais vers la
# relocation) ; écart temporel loyers 2025 / revenus 2021 ; Guadeloupe,
# Guyane et Mayotte absentes de Filosofi.

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
# ## 1. Loyers d'annonce par commune → moyenne pondérée par ZE
#
# Pondération par le parc privé LOVAC (mill. 24) : l'indicateur reflète le
# loyer « vu par le parc », pas la commune médiane.

# %%
loyers = pd.read_csv(
    RAW / "carte-loyers-2025-appartement.csv", sep=";", encoding="cp1252", dtype=str
)
loyers["loypredm2"] = pd.to_numeric(loyers["loypredm2"].str.replace(",", "."), errors="coerce")

with zipfile.ZipFile(RAW / "insee-table-appartenance-geo-communes-2026.zip") as zf:
    with zf.open("table-appartenance-geo-communes-2026.xlsx") as fh:
        appartenance = pd.read_excel(fh, sheet_name="COM", header=5, engine="calamine", dtype=str)
com_ze = appartenance[["CODGEO", "ZE2020"]].dropna()

communes_lovac = pd.read_csv(
    RAW / "lovac-opendata-communes26.csv", sep=";", encoding="cp1252", dtype=str
)
communes_lovac.columns = [c.strip() for c in communes_lovac.columns]


def to_num(series: pd.Series) -> pd.Series:
    """Parse LOVAC numbers: nbsp thousands separators, 's' (secret) -> NaN."""
    cleaned = series.astype("string").str.replace(r"[\s\xa0]", "", regex=True)
    return pd.to_numeric(cleaned.replace("s", pd.NA), errors="coerce")


PLM = {"751": "75056", "6938": "69123", "132": "13055"}


def plm_parent(code: str) -> str:
    """Map a PLM arrondissement code to its parent commune, else identity."""
    return next((city for p, city in PLM.items() if code.startswith(p)), code)


lovac = pd.DataFrame(
    {
        "code": communes_lovac["CODGEO_26"].str.strip().map(plm_parent),
        "structurelle": to_num(communes_lovac["pp_vacant_plus_2ans_24"]),
        "parc_prive": to_num(communes_lovac["ff_pp_total_24"]),
    }
)
parc_by_code = lovac.groupby("code", as_index=False).agg(
    parc_prive=("parc_prive", "sum"), structurelle=("structurelle", "sum")
)

com = (
    loyers.assign(code=loyers["INSEE_C"].str.strip().map(plm_parent))
    .groupby("code", as_index=False)
    .agg(loypredm2=("loypredm2", "mean"))
    .merge(parc_by_code, on="code", how="inner")
    .merge(com_ze.rename(columns={"CODGEO": "code", "ZE2020": "ze"}), on="code", how="left")
    .dropna(subset=["ze", "loypredm2", "parc_prive"])
)
ze_loyer = com.groupby("ze").apply(
    lambda g: pd.Series(
        {
            "loyer_m2": (g["loypredm2"] * g["parc_prive"]).sum() / g["parc_prive"].sum(),
            "parc_prive": g["parc_prive"].sum(),
            "structurelle": g["structurelle"].sum(),
        }
    ),
    include_groups=False,
)
ze_loyer["taux_structurelle"] = ze_loyer["structurelle"] / ze_loyer["parc_prive"] * 100
print(f"{len(ze_loyer)} ZE ; loyer m² pondéré min/médian/max : "
      f"{ze_loyer['loyer_m2'].min():.1f} / {ze_loyer['loyer_m2'].median():.1f} / "
      f"{ze_loyer['loyer_m2'].max():.1f} €/m²")

# %% [markdown]
# ## 2. Niveau de vie médian par ZE (Filosofi 2021)

# %%
with zipfile.ZipFile(RAW / "insee-filosofi-2021-geo2025.zip") as zf:
    with zf.open("DS_FILOSOFI_CC_data.csv") as fh:
        filosofi = pd.read_csv(
            fh, sep=";", dtype=str,
            usecols=["GEO", "GEO_OBJECT", "FILOSOFI_MEASURE", "OBS_VALUE"],
        )
med = filosofi[
    (filosofi["GEO_OBJECT"] == "ZE2020") & (filosofi["FILOSOFI_MEASURE"] == "MED_SL")
].copy()
med["niveau_vie_median"] = pd.to_numeric(med["OBS_VALUE"], errors="coerce")
med = med.set_index(med["GEO"].str.strip())["niveau_vie_median"].dropna()
print(f"{len(med)} ZE avec niveau de vie médian ; min/médian/max : "
      f"{med.min():.0f} / {med.median():.0f} / {med.max():.0f} €/UC/an")

# %% [markdown]
# ## 3. L'indice loyer/revenu et son lien avec la vacance

# %%
cross = ze_loyer.join(med, how="inner")
# Indice : loyer annuel d'un m² rapporté au niveau de vie médian (en %).
cross["indice_cout"] = cross["loyer_m2"] * 12 / cross["niveau_vie_median"] * 100
names = pd.read_excel(
    RAW / "insee-emploi-zone-1998-2018.xlsx", sheet_name="Emploi total - ZE",
    header=4, engine="calamine",
)["Zone d'emploi"].astype("string").str.extract(r"^(\d{4}) - (.*)$").dropna()
cross = cross.join(names.set_index(0)[1].rename("ze_nom"), how="left")
print(f"{len(cross)} ZE croisées")
corr = cross["indice_cout"].rank().corr(cross["taux_structurelle"].rank())
print(f"corrélation de Spearman indice de coût × taux de vacance structurelle : {corr:.2f}")
print()
print("indice de coût le plus élevé :")
print(cross.nlargest(6, "indice_cout")[["ze_nom", "loyer_m2", "niveau_vie_median", "indice_cout", "taux_structurelle"]].round(2).to_string())
print()
print("indice de coût le plus bas :")
print(cross.nsmallest(6, "indice_cout")[["ze_nom", "loyer_m2", "niveau_vie_median", "indice_cout", "taux_structurelle"]].round(2).to_string())

# %%
fig, ax = plt.subplots(figsize=(9, 6))
sizes = (cross["structurelle"] / cross["structurelle"].max() * 600).clip(lower=8)
ax.scatter(cross["indice_cout"], cross["taux_structurelle"], s=sizes, alpha=0.45,
           color=C1, edgecolors="white", linewidths=0.5)
for _, row in pd.concat([cross.nlargest(3, "indice_cout"), cross.nlargest(3, "structurelle")]).iterrows():
    ax.annotate(row["ze_nom"], (row["indice_cout"], row["taux_structurelle"]),
                fontsize=7, color="#555555", xytext=(4, 2), textcoords="offset points")
ax.set_xlabel("indice de coût : loyer annuel du m² / niveau de vie médian (%)")
ax.set_ylabel("taux de vacance structurelle du parc privé (%)")
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f %%"))
ax.set_title("Zones d'emploi : pression du coût résidentiel × vacance structurelle\n"
             "(loyers 2025, revenus 2021, vacance mill. 24 ; taille = volume de vacance)")
ax.grid(alpha=0.25)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Observations provisoires (à stabiliser avant toute publication)
#
# 1. **La pression du coût et la vacance structurelle varient en sens
#    inverse** : Spearman −0,42 sur 297 ZE ; taux de vacance médian de
#    2,5 % dans la moitié des ZE à indice de coût élevé contre 4,0 % dans
#    la moitié à coût faible. Le loyer pondéré va de 8,0 à 27,2 €/m²
#    (Paris), le niveau de vie médian de 14 970 à 33 100 €/UC/an.
# 2. **Lecture pour H-03 : le coût est un marqueur de tension, pas la cause
#    de la vacance.** Là où le coût relatif est élevé (Paris 1,28 %,
#    Roissy, Menton), le parc est presque entièrement utilisé — le coût y
#    limite l'accès *des ménages* (à instruire avec un vrai taux d'effort,
#    D-09) mais pas l'usage du parc. Là où la vacance est forte
#    (Bar-le-Duc 6,1 %, Cosne-Cours-sur-Loire 7,3 %), le coût est bas :
#    le blocage n'y est pas économique côté demande solvable locale.
# 3. **Exception remarquable : les DOM** (CORRECTION — d'abord identifiés
#    à tort comme ZE corses ; la vérification des codes montre que 0401
#    L'Est, 0402 L'Ouest, 0404 Le Sud sont des ZE de La Réunion et 0205
#    Le Sud de Martinique). Elles cumulent indice de coût parmi les plus
#    élevés de France (1,01-1,16 — revenus faibles bien plus que loyers
#    élevés) ET vacance structurelle au-dessus de la moyenne — prolongement
#    du constat DOM de R-02, sans lien avec les résidences secondaires
#    (voir exploration 05).
# 4. Limites : loyers d'annonce 2025 (relocation) vs revenus 2021 ;
#    l'indice n'est pas un taux d'effort (pas de surface ni de composition
#    de ménage) ; 8 ZE absentes (Guadeloupe, Guyane hors Filosofi) ;
#    licence du millésime loyers 2025 à confirmer avant publication.
#
# Prochaine étape de stabilisation : R-04 (indice de coût par ZE et son
# croisement avec R-03) + interprétation I-04 dans le graphe.

# %%
