# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
# ---

# %% [markdown]
# # Exploration 07 — Taux d'effort à la relocation par zone d'emploi (D-09)
#
# **Régime exploratoire** (méthode Métabolisme §2.1). L'indice de coût de
# R-04 (« loyer annuel d'un m² en % du niveau de vie médian ») classe les
# territoires mais ne dit pas ce que coûte réellement se loger : il ignore
# la surface et la composition des ménages. Ici on construit un **taux
# d'effort à la relocation** (D-09, variante **brute** — aucune donnée
# territoriale d'aides au logement en open data), par ZE :
#
# `effort = 12 × loyer_m² × surface_ménage / revenu_ménage`
#
# avec deux décisions prises le 2026-08-05 (à consigner C-04/C-05) :
#
# - **C-04** — la surface du ménage est `H-07 (m²/personne, S-12) ×
#   personnes` et le revenu est `MED_SL (€/UC/an, S-10) × UC` ; en
#   rapportant les deux, le taux d'effort ne dépend que du ratio
#   personnes/UC **observé** de la ZE (NUM_PER/NUM_CU, S-10) — aucun
#   ménage type à choisir.
# - **C-05** — le loyer est le **mix appartement/maison** pondéré par la
#   composition des résidences principales de la ZE (S-11) : en ZE rurale
#   on se reloge en maison, pas en appartement. Variante appartement seul
#   en sensibilité (continuité R-04).
#
# Précautions : loyers d'annonce 2025 (charges comprises) vs revenus 2021 ;
# H-07 calibrée en métropole (S-12) alors que R-06 couvre aussi La
# Réunion/Martinique ; taux BRUT (avant aides) pour un ménage MÉDIAN qui
# se relogerait aux loyers d'annonce courants — pas le taux d'effort moyen
# du parc en place.

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

H07_M2_PER_PERSON = 51.2  # central (S-12) ; plage [35, 71]
H07_RANGE = (35.0, 71.0)

# %% [markdown]
# ## 1. Loyers d'annonce appartement ET maison par commune → par ZE
#
# Comme R-04 : moyenne communale pondérée par le parc privé LOVAC
# (mill. 24), arrondissements PLM ramenés à la commune parente.

# %%
PLM = {"751": "75056", "6938": "69123", "132": "13055"}


def plm_parent(code: str) -> str:
    """Map a PLM arrondissement code to its parent commune, else identity."""
    return next((city for p, city in PLM.items() if code.startswith(p)), code)


def to_num(series: pd.Series) -> pd.Series:
    """Parse LOVAC numbers: nbsp thousands separators, 's' (secret) -> NaN."""
    cleaned = series.astype("string").str.replace(r"[\s\xa0]", "", regex=True)
    return pd.to_numeric(cleaned.replace("s", pd.NA), errors="coerce")


def read_loyers(name: str) -> pd.DataFrame:
    raw = pd.read_csv(RAW / name, sep=";", encoding="cp1252", dtype=str)
    raw["loypredm2"] = pd.to_numeric(raw["loypredm2"].str.replace(",", "."), errors="coerce")
    return (
        raw.assign(code=raw["INSEE_C"].str.strip().map(plm_parent))
        .groupby("code", as_index=False)
        .agg(loypredm2=("loypredm2", "mean"))
    )


loyers_appart = read_loyers("carte-loyers-2025-appartement.csv")
loyers_maison = read_loyers("carte-loyers-2025-maison.csv")

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
        "parc_prive": to_num(communes_lovac["ff_pp_total_24"]),
    }
)
parc_by_code = lovac.groupby("code", as_index=False).agg(
    parc_prive=("parc_prive", "sum"), structurelle=("structurelle", "sum")
)


def loyer_by_ze(loyers_com: pd.DataFrame) -> pd.Series:
    com = (
        loyers_com.merge(parc_by_code, on="code", how="inner")
        .merge(com_ze, on="code", how="left")
        .dropna(subset=["ze", "loypredm2", "parc_prive"])
    )
    grouped = com.groupby("ze")
    return (grouped.apply(
        lambda g: (g["loypredm2"] * g["parc_prive"]).sum() / g["parc_prive"].sum(),
        include_groups=False,
    )).rename("loyer_m2")


ze = pd.DataFrame(
    {
        "loyer_appart_m2": loyer_by_ze(loyers_appart),
        "loyer_maison_m2": loyer_by_ze(loyers_maison),
    }
)
print(f"{len(ze)} ZE ; loyer appart médian {ze['loyer_appart_m2'].median():.1f} €/m², "
      f"maison {ze['loyer_maison_m2'].median():.1f} €/m²")

# %% [markdown]
# ## 2. Mix maison/appartement des résidences principales (S-11) par ZE

# %%
with zipfile.ZipFile(RAW / "insee-rp-base-cc-logement-2022.zip") as zf:
    with zf.open("base-cc-logement-2022.CSV") as fh:
        census = pd.read_csv(
            fh, sep=";", dtype=str, usecols=["CODGEO", "P22_RPMAISON", "P22_RPAPPART"]
        )
census = pd.DataFrame(
    {
        "code": census["CODGEO"].str.strip().map(plm_parent),
        "rp_maison": pd.to_numeric(census["P22_RPMAISON"], errors="coerce"),
        "rp_appart": pd.to_numeric(census["P22_RPAPPART"], errors="coerce"),
    }
)
mix = (
    census.groupby("code", as_index=False).sum()
    .merge(com_ze, on="code", how="left")
    .dropna(subset=["ze"])
    .groupby("ze")[["rp_maison", "rp_appart"]]
    .sum()
)
mix["part_maison"] = mix["rp_maison"] / (mix["rp_maison"] + mix["rp_appart"])
ze = ze.join(mix["part_maison"], how="inner")
print(f"part maison : min {mix['part_maison'].min():.2f}, "
      f"médiane {mix['part_maison'].median():.2f}, max {mix['part_maison'].max():.2f}")

# %% [markdown]
# ## 3. Revenus, personnes et unités de consommation par ZE (Filosofi 2021)

# %%
with zipfile.ZipFile(RAW / "insee-filosofi-2021-geo2025.zip") as zf:
    with zf.open("DS_FILOSOFI_CC_data.csv") as fh:
        filosofi = pd.read_csv(
            fh, sep=";", dtype=str,
            usecols=["GEO", "GEO_OBJECT", "FILOSOFI_MEASURE", "OBS_VALUE"],
        )
filo_ze = filosofi[filosofi["GEO_OBJECT"] == "ZE2020"].copy()
filo_ze["OBS_VALUE"] = pd.to_numeric(filo_ze["OBS_VALUE"], errors="coerce")
filo = (
    filo_ze.pivot_table(
        index=filo_ze["GEO"].str.strip(), columns="FILOSOFI_MEASURE",
        values="OBS_VALUE", aggfunc="first",
    )[["MED_SL", "NUM_PER", "NUM_CU"]]
    .dropna()
)
filo["pers_per_uc"] = filo["NUM_PER"] / filo["NUM_CU"]
ze = ze.join(filo[["MED_SL", "pers_per_uc"]], how="inner")
print(f"{len(ze)} ZE croisées ; personnes/UC : min {ze['pers_per_uc'].min():.2f}, "
      f"médiane {ze['pers_per_uc'].median():.2f}, max {ze['pers_per_uc'].max():.2f}")

# %% [markdown]
# ## 4. Le taux d'effort brut à la relocation
#
# `effort = 12 × loyer_mix × H07 × (personnes/UC) / MED_SL` — le ménage
# s'élimine de la formule, seul reste le ratio observé de la ZE.

# %%
ze["loyer_mix_m2"] = (
    ze["part_maison"] * ze["loyer_maison_m2"]
    + (1 - ze["part_maison"]) * ze["loyer_appart_m2"]
)
ze["surface_per_uc"] = H07_M2_PER_PERSON * ze["pers_per_uc"]
ze["effort_brut_pct"] = 12 * ze["loyer_mix_m2"] * ze["surface_per_uc"] / ze["MED_SL"] * 100
ze["effort_appart_pct"] = (
    12 * ze["loyer_appart_m2"] * ze["surface_per_uc"] / ze["MED_SL"] * 100
)

names = pd.read_excel(
    RAW / "insee-emploi-zone-1998-2018.xlsx", sheet_name="Emploi total - ZE",
    header=4, engine="calamine",
)["Zone d'emploi"].astype("string").str.extract(r"^(\d{4}) - (.*)$").dropna()
ze = ze.join(names.set_index(0)[1].rename("ze_nom"), how="left")

q = ze["effort_brut_pct"].quantile([0, 0.1, 0.25, 0.5, 0.75, 0.9, 1]).round(1)
print("distribution du taux d'effort brut à la relocation (%) :")
print(q.to_string())
print()
cols = ["ze_nom", "loyer_mix_m2", "part_maison", "MED_SL", "pers_per_uc", "effort_brut_pct"]
print("taux d'effort les plus élevés :")
print(ze.nlargest(8, "effort_brut_pct")[cols].round(2).to_string())
print()
print("taux d'effort les plus bas :")
print(ze.nsmallest(5, "effort_brut_pct")[cols].round(2).to_string())

# %% [markdown]
# ## 5. Sensibilités : plage H-07 et variante appartement seul

# %%
lo, hi = H07_RANGE
for label, factor in [("H-07 basse (35 m²/pers)", lo), ("H-07 haute (71 m²/pers)", hi)]:
    variant = ze["effort_brut_pct"] * factor / H07_M2_PER_PERSON
    print(f"{label} : médiane {variant.median():.1f} %, max {variant.max():.1f} %")
print(f"appartement seul : médiane {ze['effort_appart_pct'].median():.1f} % "
      f"(mix : {ze['effort_brut_pct'].median():.1f} %)")
rank_shift = (
    ze["effort_brut_pct"].rank() - ze["effort_appart_pct"].rank()
).abs()
print(f"écart de rang mix vs appartement : médian {rank_shift.median():.0f}, "
      f"max {rank_shift.max():.0f} — Spearman "
      f"{ze['effort_brut_pct'].rank().corr(ze['effort_appart_pct'].rank()):.3f}")

# %% [markdown]
# ## 6. Croisement avec la vacance structurelle (continuité R-04)

# %%
vac = (
    lovac.merge(com_ze, on="code", how="left")
    .dropna(subset=["ze"])
    .groupby("ze")[["structurelle", "parc_prive"]]
    .sum(min_count=1)
)
vac["taux_structurelle"] = vac["structurelle"] / vac["parc_prive"] * 100
cross = ze.join(vac, how="inner")
corr = cross["effort_brut_pct"].rank().corr(cross["taux_structurelle"].rank())
print(f"{len(cross)} ZE ; Spearman effort × vacance structurelle : {corr:.2f}")
high = cross["effort_brut_pct"] >= cross["effort_brut_pct"].median()
print(f"vacance médiane des ZE à effort élevé : "
      f"{cross.loc[high, 'taux_structurelle'].median():.1f} % ; "
      f"à effort bas : {cross.loc[~high, 'taux_structurelle'].median():.1f} %")

# %%
fig, ax = plt.subplots(figsize=(9, 6))
sizes = (cross["structurelle"] / cross["structurelle"].max() * 600).clip(lower=8)
ax.scatter(cross["effort_brut_pct"], cross["taux_structurelle"], s=sizes, alpha=0.45,
           color=C1, edgecolors="white", linewidths=0.5)
for _, row in pd.concat(
    [cross.nlargest(4, "effort_brut_pct"), cross.nlargest(3, "structurelle")]
).iterrows():
    ax.annotate(row["ze_nom"], (row["effort_brut_pct"], row["taux_structurelle"]),
                fontsize=7, color="#555555", xytext=(4, 2), textcoords="offset points")
ax.set_xlabel("taux d'effort brut à la relocation, ménage médian (%)")
ax.set_ylabel("taux de vacance structurelle du parc privé (%)")
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f %%"))
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f %%"))
ax.set_title("Zones d'emploi : taux d'effort à la relocation × vacance structurelle\n"
             "(loyers 2025, revenus 2021, H-07 = 51,2 m²/pers ; taille = volume de vacance)")
ax.grid(alpha=0.25)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Observations provisoires (vérifiées depuis les sorties ci-dessus)
#
# 1. **Le niveau absolu dépend fortement de H-07, la structure territoriale
#    non.** Avec la valeur centrale (51,2 m²/pers, parc moyen en place), le
#    taux d'effort brut médian à la relocation est de 40,1 % — de 27,4 %
#    (borne basse 35 m²/pers, surface des 30-39 ans) à 55,6 % (borne
#    haute). Le taux d'effort étant linéaire en H-07, le CLASSEMENT des ZE
#    est invariant : seuls les niveaux publiés doivent porter la plage.
#    À la borne basse, l'écart reste béant : de ~20 % (ZE les moins chères)
#    à 63,9 % (Paris).
# 2. **La géographie de la tension : Paris et les DOM.** Taux les plus
#    élevés : Paris 93,5 %, puis L'Ouest-Réunion 85,1 %, Roissy 82,9 %,
#    Menton 78,7 %, Le Sud-Martinique 77,4 %, et les trois autres ZE
#    réunionnaises à ~75 %. Le cumul DOM de R-04/I-04 se confirme dans une
#    unité parlante : au loyer d'annonce courant, un ménage médian
#    réunionnais y consacrerait les 3/4 de son revenu — la relocation est
#    hors de portée du ménage médian local (revenus faibles bien plus que
#    loyers extrêmes). À l'autre bout, ~29 % dans le rural en déclin
#    (Avallon, Mayenne, Loches, Chaumont, Ussel).
# 3. **L'anticorrélation coût × vacance persiste en vrai taux d'effort** :
#    Spearman −0,40 (R-04 : −0,42), vacance structurelle médiane de 2,6 %
#    dans la moitié des ZE à effort élevé contre 3,9 % dans l'autre. La
#    montée en réalisme (surface, composition, mix maison/appart) ne change
#    pas la lecture : le coût marque la tension, il n'explique pas la
#    vacance.
# 4. **Le mix maison/appartement (C-05) compte localement, pas
#    globalement** : part maison médiane des RP par ZE = 0,74 (l'appartement
#    seul de R-04 était non représentatif du parc de la plupart des ZE) ;
#    effort médian mix 40,1 % vs 43,8 % appartement seul ; Spearman des
#    classements 0,959 mais décalages jusqu'à 83 rangs — le mix est
#    nécessaire pour qualifier UNE ZE, pas pour la structure d'ensemble.
# 5. **Le pont personnes/UC observé (C-04) est peu dispersé** (1,35-1,58,
#    médiane 1,43) : il territorialise à la marge sans piloter le résultat.
# 6. Limites : taux BRUT (aides non déductibles faute de source
#    territoriale) ; loyers d'annonce 2025 vs revenus 2021 ; H-07 calibrée
#    en métropole (S-12) appliquée aux ZE DOM — leur niveau est donc une
#    convention, leur position relative reste robuste (déjà en tête dans
#    R-04 sans surface) ; 8 ZE hors Filosofi (Guadeloupe/Guyane) absentes ;
#    licence loyers 2025 à confirmer (L-09).
#
# Prochaine étape de stabilisation : R-06 (taux d'effort brut à la
# relocation par ZE, avec plage H-07 et variante appartement) +
# interprétation I-06 + choix C-04/C-05 dans le graphe.

# %%
