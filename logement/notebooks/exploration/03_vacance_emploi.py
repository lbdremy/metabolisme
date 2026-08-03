# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
# ---

# %% [markdown]
# # Exploration 03 — Vacance structurelle et dynamique de l'emploi (H-02)
#
# **Régime exploratoire** (méthode Métabolisme §2.1). Premier test empirique
# de l'hypothèse directrice **H-02** du cadrage (`INTRO.md` §4) : *les
# capacités disponibles sont mal localisées* — abondance relative dans
# certains territoires, tension dans d'autres, décalage entre logement et
# emploi.
#
# Protocole : agréger la vacance structurelle du parc privé (S-05, LOVAC,
# millésime de référence 24 — choix C-03) par **zone d'emploi 2020** (D-07)
# via la table d'appartenance des communes (S-06, COG 2026), puis la
# confronter à la **dynamique d'emploi total 1998-2018** par ZE (S-07).
#
# Précautions :
#
# - la série d'emploi s'arrête en 2018 (dernière publication à la maille
#   ZE) : on teste une dynamique *structurelle* de long terme, pas la
#   conjoncture ;
# - la vacance communale est secrétisée sous 11 logements (L-05) : les
#   agrégats ZE sont donc des minorants, surtout dans les petites ZE
#   rurales — à garder en tête en lisant les taux ;
# - parc privé uniquement (L-06).

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
# ## 1. Table de passage communes → zones d'emploi (S-06)

# %%
with zipfile.ZipFile(RAW / "insee-table-appartenance-geo-communes-2026.zip") as zf:
    with zf.open("table-appartenance-geo-communes-2026.xlsx") as fh:
        # header line 6 (0-based 5): the code row CODGEO/LIBGEO/...
        appartenance = pd.read_excel(fh, sheet_name="COM", header=5, engine="calamine", dtype=str)
com_ze = appartenance[["CODGEO", "LIBGEO", "ZE2020"]].dropna(subset=["CODGEO", "ZE2020"])
print(f"{len(com_ze)} communes, {com_ze['ZE2020'].nunique()} zones d'emploi")
com_ze.head(3)

# %% [markdown]
# ## 2. Vacance structurelle LOVAC agrégée par ZE (millésime 24)
#
# Piège vérifié : la feuille COM de la table d'appartenance ne contient PAS
# les arrondissements de Paris/Lyon/Marseille (ils vivent dans la feuille
# ARM), alors que LOVAC les livre comme communes (75101…). Sans
# ré-agrégation PLM, les trois plus grandes villes — dont les ~32 000
# vacants structurels de Paris — sortiraient silencieusement de la jointure.

# %%
communes = pd.read_csv(RAW / "lovac-opendata-communes26.csv", sep=";", encoding="cp1252", dtype=str)
communes.columns = [c.strip() for c in communes.columns]


def to_num(series: pd.Series) -> pd.Series:
    """Parse LOVAC numbers: nbsp thousands separators, 's' (secret) -> NaN."""
    cleaned = series.astype("string").str.replace(r"[\s\xa0]", "", regex=True)
    return pd.to_numeric(cleaned.replace("s", pd.NA), errors="coerce")


PLM_PREFIXES = {"751": "75056", "6938": "69123", "132": "13055"}


def plm_parent(code: str) -> str:
    """Map a PLM arrondissement code to its parent commune, else identity."""
    return next((city for p, city in PLM_PREFIXES.items() if code.startswith(p)), code)


lovac = pd.DataFrame(
    {
        "code": communes["CODGEO_26"].str.strip().map(plm_parent),
        "structurelle_24": to_num(communes["pp_vacant_plus_2ans_24"]),
        "parc_prive_24": to_num(communes["ff_pp_total_24"]),
    }
)
merged = lovac.merge(com_ze, left_on="code", right_on="CODGEO", how="left")
unmatched = merged[merged["ZE2020"].isna()]
print(f"communes LOVAC sans ZE : {len(unmatched)} — {unmatched['code'].unique()[:5]}")

ze_vacance = (
    merged.dropna(subset=["ZE2020"])
    .groupby("ZE2020")
    .agg(structurelle=("structurelle_24", "sum"), parc_prive=("parc_prive_24", "sum"))
)
ze_vacance["taux_structurelle"] = ze_vacance["structurelle"] / ze_vacance["parc_prive"] * 100
ze_vacance.describe().round(1)

# %% [markdown]
# ## 3. Emploi total par ZE, 1998-2018 (S-07)

# %%
# One row per ZE (no sector detail on the 'total' sheet), header on row 5.
emploi_raw = pd.read_excel(
    RAW / "insee-emploi-zone-1998-2018.xlsx",
    sheet_name="Emploi total - ZE",
    header=4,
    engine="calamine",
).rename(columns={"Zone d'emploi": "ze"})
parts = emploi_raw["ze"].astype("string").str.extract(r"^(\d{4}) - (.*)$")
per_ze = emploi_raw.assign(ze_code=parts[0], ze_nom=parts[1]).dropna(subset=["ze_code"])
per_ze = per_ze.set_index("ze_code")[["ze_nom", "1998", "2018"]]
per_ze[["1998", "2018"]] = per_ze[["1998", "2018"]].apply(pd.to_numeric, errors="coerce")
per_ze = per_ze.dropna()
per_ze["emploi_evol_pct_an"] = ((per_ze["2018"] / per_ze["1998"]) ** (1 / 20) - 1) * 100
print(f"{len(per_ze)} zones d'emploi ; emploi total 2018 : {per_ze["2018"].sum() / 1e6:.1f} M")
per_ze.sort_values("emploi_evol_pct_an").head(5)[["ze_nom", "emploi_evol_pct_an"]].round(2)

# %% [markdown]
# ## 4. Croisement : vacance structurelle vs dynamique d'emploi

# %%
cross = ze_vacance.join(per_ze, how="inner")
print(f"{len(cross)} ZE jointes (sur {len(ze_vacance)} côté LOVAC, {len(per_ze)} côté emploi)")
# Spearman = Pearson sur les rangs (évite une dépendance scipy).
corr = cross["taux_structurelle"].rank().corr(cross["emploi_evol_pct_an"].rank())
print(f"corrélation de Spearman taux structurel × évolution emploi : {corr:.2f}")

declining = cross["emploi_evol_pct_an"] < 0
share_vac = cross.loc[declining, "structurelle"].sum() / cross["structurelle"].sum() * 100
share_parc = cross.loc[declining, "parc_prive"].sum() / cross["parc_prive"].sum() * 100
share_emploi = cross.loc[declining, "2018"].sum() / cross["2018"].sum() * 100
print(
    f"ZE à emploi déclinant (1998-2018) : {declining.sum()}/{len(cross)} — "
    f"{share_vac:.0f} % de la vacance structurelle, {share_parc:.0f} % du parc privé, "
    f"{share_emploi:.0f} % de l'emploi 2018"
)

# %%
fig, ax = plt.subplots(figsize=(9, 6))
sizes = (cross["structurelle"] / cross["structurelle"].max() * 600).clip(lower=8)
ax.scatter(
    cross["emploi_evol_pct_an"],
    cross["taux_structurelle"],
    s=sizes,
    alpha=0.45,
    color=C1,
    edgecolors="white",
    linewidths=0.5,
)
ax.axvline(0, color="#999999", ls="--", lw=1)
ax.axhline(
    cross["structurelle"].sum() / cross["parc_prive"].sum() * 100,
    color="#999999",
    ls=":",
    lw=1,
)
for _, row in cross.nlargest(5, "taux_structurelle").iterrows():
    ax.annotate(row["ze_nom"], (row["emploi_evol_pct_an"], row["taux_structurelle"]),
                fontsize=7, color="#555555", xytext=(4, 2), textcoords="offset points")
ax.set_xlabel("évolution annuelle moyenne de l'emploi total 1998-2018 (%)")
ax.set_ylabel("taux de vacance structurelle du parc privé (%)")
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f %%"))
ax.set_title(
    "Zones d'emploi : vacance structurelle (mill. 24) × dynamique d'emploi 1998-2018\n"
    "(taille du point = volume de vacance structurelle ; pointillés = 0 % et moyenne nationale)"
)
ax.grid(alpha=0.25)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 5. Les deux extrêmes en volume

# %%
worst = cross[declining].nlargest(8, "structurelle")[
    ["ze_nom", "structurelle", "taux_structurelle", "emploi_evol_pct_an"]
]
best = cross[cross["emploi_evol_pct_an"] > 0.8].nlargest(8, "structurelle")[
    ["ze_nom", "structurelle", "taux_structurelle", "emploi_evol_pct_an"]
]
print("ZE à emploi déclinant portant le plus de vacance structurelle :")
print(worst.round(2).to_string())
print()
print("ZE très dynamiques (> +0,8 %/an) portant néanmoins de la vacance structurelle :")
print(best.round(2).to_string())

# %% [markdown]
# ## Observations provisoires (à stabiliser avant toute publication)
#
# 1. **La corrélation attendue par H-02 existe et est modérée** : Spearman
#    −0,36 entre taux de vacance structurelle et dynamique d'emploi
#    1998-2018 ; le taux médian des ZE à emploi déclinant (4,5 %) est
#    supérieur d'environ moitié à celui des ZE en croissance (2,9 %).
# 2. **Mais le gros des volumes est DANS les zones d'emploi dynamiques** :
#    les 63 ZE à emploi déclinant portent 15 % de la vacance structurelle
#    (pour 10 % du parc privé et 9 % de l'emploi 2018) — donc **85 % de la
#    vacance structurelle se trouve dans des ZE où l'emploi croît**, Paris
#    en tête (69 803, 2,5 %, +0,74 %/an), puis Marseille (17 917) et Lyon
#    (12 099).
# 3. **Lecture pour H-02** : l'hypothèse est confirmée *en intensité*
#    (sur-représentation ×1,5 de la vacance dans les territoires déclinants,
#    gradient net) mais réfutée comme *explication dominante en volume* :
#    la majorité de la capacité sortie d'usage est là où l'emploi existe et
#    croît. Les causes du blocage y sont donc ailleurs — état du bâti,
#    successions, inadéquation fine infra-ZE, coût (H-03, H-05) — ce qui
#    oriente la suite.
# 4. **Cas remarquables** : Perpignan cumule dynamique forte (+1,16 %/an)
#    et taux élevé (3,1 %, 10 526 logements) ; à l'inverse Thionville,
#    Châteauroux, Nevers, Montluçon, Troyes... combinent déclin et volumes
#    de plusieurs milliers.
# 5. Limites : emploi arrêté à 2018 (dernière maille ZE publiée),
#    agrégats ZE minorés par la secrétisation communale (L-05), une commune
#    non appariée (97127), parc privé uniquement (L-06).
#
# Prochaine étape de stabilisation : lecteurs S-06/S-07 en `core/`,
# résultat R-03 (croisement vacance × emploi par ZE) et interprétation
# I-03 dans le graphe.

# %%
