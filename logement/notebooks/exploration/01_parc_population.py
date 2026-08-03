# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
# ---

# %% [markdown]
# # Exploration 01 — Parc de logements et ménages
#
# **Régime exploratoire** (méthode Métabolisme §2.1) : ce notebook sert à
# découvrir la structure des données figées et à donner un premier ordre de
# grandeur à la question empirique n° 1 du cadrage (`INTRO.md` §15) :
#
# > Le nombre de logements augmente-t-il au même rythme que les ménages ?
#
# Rien de ce qui suit n'est un résultat publié : les transformations retenues
# seront stabilisées dans `src/logement/` (avec tests), et les résultats
# recevront alors leurs identifiants (O-xx / T-xx / R-xx).
#
# Sources utilisées (registre `sources/sources.yaml`, fichiers sha256 vérifiés
# par `uv run logement validate`) :
#
# - **S-01** — Insee Focus n° 359, données des figures (indices base 100 en
#   1982, dont la population).
# - **S-02** — EAPL, parc par catégorie × type d'habitat, 1982-2025, milliers.
# - **S-03** — Recensement, ménages en séries longues (millésimes 1962-2022),
#   milliers.
#
# Précaution de lecture (D-05) : ménage (recensement) et résidence principale
# (EAPL) sont des concepts appariés — « il y a égalité entre nombre de ménages
# et nombre de résidences principales » — mais mesurés par des sources
# différentes ; l'écart observé est documenté plus bas, pas gommé.

# %%
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

ROOT = Path.cwd()
while not (ROOT / "pyproject.toml").exists():  # notebook launched from anywhere
    ROOT = ROOT.parent
RAW = ROOT / "data" / "raw"

# Palette catégorielle validée (skill dataviz, ordre fixe — jamais recyclée).
C1, C2, C3, C4 = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"

pd.set_option("display.width", 120)

# %% [markdown]
# ## 1. S-02 — le parc par catégorie, série annuelle 1982-2025
#
# La feuille « Données » porte les catégories en lignes (avec un sous-détail
# individuel/collectif indenté par espaces insécables) et les années en
# colonnes. On ne garde ici que les quatre lignes de niveau catégorie.

# %%
s02_raw = pd.read_excel(RAW / "insee-eapl-parc-residence-2025.xlsx", sheet_name="Données", header=3)
s02_raw = s02_raw.rename(columns={"Parc de logements": "category"})
s02_raw["category"] = s02_raw["category"].astype("string")

top_level = s02_raw[~s02_raw["category"].str.startswith("\xa0", na=True)].copy()
# Normalize the labels: INSEE mixes non-breaking and double spaces
# ('Résidences secondaires,\xa0 logements occasionnels').
top_level["category"] = (
    top_level["category"].str.replace("\xa0", " ").str.replace(r"\s+", " ", regex=True).str.strip()
)
top_level = top_level.set_index("category")
# Column headers are years, the last ones marked '2023 (p)'..'2025 (p)' (provisoires).
years = {c: int(str(c)[:4]) for c in top_level.columns if str(c)[:4].isdigit()}
parc = top_level[list(years)].apply(pd.to_numeric, errors="coerce").dropna(how="all")
parc.columns = list(years.values())
parc = parc.T  # rows = years, columns = categories, unit = thousands
provisional_years = [y for c, y in years.items() if "(p)" in str(c)]
print(f"années provisoires : {provisional_years}")
parc.head()

# %%
parc.tail()

# %% [markdown]
# Contrôle de cohérence (invariant, futur test de propriété) : la somme des
# trois catégories doit redonner l'ensemble du parc.

# %%
cats = [
    "Résidences principales",
    "Résidences secondaires, logements occasionnels",
    "Logements vacants",
]
total_col = next(c for c in parc.columns if c.lower().startswith("ensemble"))
gap = (parc[cats].sum(axis=1) - parc[total_col]).abs().max()
print(f"écart max |somme des catégories - ensemble| : {gap:.0f} millier(s)")
assert gap <= 1, "les catégories ne somment pas à l'ensemble"

# %% [markdown]
# ## 2. S-03 — les ménages aux millésimes censitaires
#
# Feuille « France » (France hors Mayotte, cohérente avec S-01/S-02) : on lit
# la ligne « Total » du bloc « Nombre de ménages selon le nombre de
# personnes ». 1968 est indisponible (n.d.).

# %%
s03_raw = pd.read_excel(
    RAW / "insee-rp-menages-series-longues-2022.xlsx", sheet_name="France", header=None
)
year_row = s03_raw.iloc[2, 1:].tolist()
totals_row = s03_raw[s03_raw[0].astype("string").str.strip() == "Total"].iloc[0, 1:].tolist()
menages = (
    pd.Series(totals_row, index=[int(y) for y in year_row], name="ménages (milliers)")
    .apply(pd.to_numeric, errors="coerce")
    .dropna()
)
menages

# %% [markdown]
# ## 3. Logements et ménages : évolutions indexées (base 100 en 1982)
#
# Un seul axe, séries indexées sur une base commune (1982, première année
# commune aux trois sources). La population vient de S-01 (Figure 2), déjà en
# indice base 100 en 1982.

# %%
s01_fig2 = pd.read_excel(
    RAW / "insee-focus-359-parc-logements-2025.xlsx", sheet_name="Figure 2", header=2
).rename(columns={"Année": "year"})
# Years arrive as text, sometimes suffixed ('2025p' provisoire) or as footnotes.
s01_fig2["year"] = pd.to_numeric(
    s01_fig2["year"].astype("string").str.extract(r"^(\d{4})")[0], errors="coerce"
)
population_idx = (
    s01_fig2.dropna(subset=["year"])
    .astype({"year": int})
    .set_index("year")["Population"]
    .apply(pd.to_numeric, errors="coerce")
    .dropna()
)

idx = pd.DataFrame(
    {
        "Ensemble des logements": parc[total_col] / parc.loc[1982, total_col] * 100,
        "Résidences principales": parc[cats[0]] / parc.loc[1982, cats[0]] * 100,
        "Population (S-01)": population_idx,
    }
)
menages_idx = menages[menages.index >= 1982] / menages[1982] * 100

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(idx.index, idx["Ensemble des logements"], color=C1, lw=2, label="Ensemble des logements")
ax.plot(idx.index, idx["Résidences principales"], color=C2, lw=2, label="Résidences principales")
ax.plot(idx.index, idx["Population (S-01)"], color=C3, lw=2, label="Population")
ax.plot(
    menages_idx.index,
    menages_idx.values,
    color=C4,
    lw=0,
    marker="o",
    ms=7,
    label="Ménages (millésimes RP)",
)
ax.set_title("Logements, ménages, population — indice base 100 en 1982\n(S-01, S-02, S-03 ; France hors Mayotte)")
ax.set_ylabel("indice (100 = 1982)")
ax.grid(alpha=0.25)
ax.legend(frameon=False)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 4. Taux de croissance annuels moyens par période intercensitaire

# %%
vintages = [y for y in menages.index if y >= 1982]
rows = []
for start, end in zip(vintages[:-1], vintages[1:], strict=True):
    n = end - start
    rows.append(
        {
            "période": f"{start}-{end}",
            "logements (%/an)": ((parc.loc[end, total_col] / parc.loc[start, total_col]) ** (1 / n) - 1) * 100,
            "rés. principales (%/an)": ((parc.loc[end, cats[0]] / parc.loc[start, cats[0]]) ** (1 / n) - 1) * 100,
            "ménages (%/an)": ((menages[end] / menages[start]) ** (1 / n) - 1) * 100,
        }
    )
growth = pd.DataFrame(rows).set_index("période").round(2)
growth

# %% [markdown]
# ## 5. L'écart entre le parc et les ménages : où va la différence ?
#
# Si le parc croît plus vite que les ménages, l'écart se loge par construction
# dans les catégories hors résidence principale : résidences secondaires /
# logements occasionnels et logements vacants (D-01, quatre catégories).

# %%
hors_rp = parc[[cats[1], cats[2]]]
share = hors_rp.div(parc[total_col], axis=0) * 100

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharex=True)
axes[0].plot(parc.index, parc[cats[2]], color=C1, lw=2)
axes[0].set_title("Logements vacants (milliers)")
axes[1].plot(share.index, share[cats[2]], color=C1, lw=2, label="Logements vacants")
axes[1].plot(share.index, share[cats[1]], color=C2, lw=2, label="Rés. secondaires et occasionnels")
axes[1].set_title("Part dans l'ensemble du parc (%)")
axes[1].yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f %%"))
axes[1].legend(frameon=False)
for ax in axes:
    ax.grid(alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 6. Ménages vs résidences principales aux millésimes (précaution D-05)
#
# Les deux séries devraient coïncider par définition (« égalité entre nombre de
# ménages et nombre de résidences principales ») ; l'écart mesure la différence
# entre les deux appareils de mesure (recensement vs synthèse EAPL), pas un
# phénomène de logement.

# %%
compare = pd.DataFrame(
    {
        "ménages RP (milliers)": menages[vintages],
        "rés. principales EAPL (milliers)": parc.loc[vintages, cats[0]],
    }
)
compare["écart (%)"] = (
    (compare["rés. principales EAPL (milliers)"] - compare["ménages RP (milliers)"])
    / compare["ménages RP (milliers)"]
    * 100
).round(2)
compare

# %% [markdown]
# ## Observations provisoires (à stabiliser avant toute publication)
#
# 1. **Sur 40 ans, le parc suit les ménages, pas la population.** Indices 2022
#    (base 100 en 1982) : logements 156,2 · ménages 155,2 · population 121,9.
#    La croissance du parc a essentiellement accompagné la multiplication des
#    ménages, elle-même portée par la décohabitation (taille moyenne : 2,72
#    personnes en 1982 → 2,15 en 2022) bien plus que par la population.
# 2. **Le régime change vers 2005-2006.** De 1990 à 2006, les ménages
#    croissent *plus vite* que le parc (1,15-1,33 %/an contre 1,04-1,19) : le
#    parc se tend et la part des logements vacants tombe de 7,9 % (1982) à
#    6,2 % (2005). Après 2006, c'est l'inverse (parc 1,08-1,16 %/an, ménages
#    0,84-0,99) : la vacance remonte à 7,7 % en 2025 — 2 962 milliers de
#    logements vacants contre 1 895 en 1982. Depuis 2016, les deux rythmes
#    convergent (~0,9 %/an).
# 3. **La part des résidences secondaires et logements occasionnels est
#    stable** sur la période (9,5 % → 9,8 %) : au niveau national, la
#    remontée de la capacité hors résidence principale depuis 2006 est un
#    phénomène de vacance, pas de résidences secondaires — la concentration
#    territoriale de ces dernières reste à examiner (INTRO §7, capacité
#    saisonnière retirée).
# 4. **Ménages (RP) et résidences principales (EAPL) coïncident à ±0,3 %**
#    aux millésimes — les deux appareils de mesure se recoupent bien ;
#    l'écart résiduel est documenté, il n'est pas un phénomène de logement
#    (D-05/D-06, changement de concept au 31/08/2025).
# 5. Ces constats sont des **ordres de grandeur exploratoires** sur séries
#    nationales, dont 2023-2025 provisoires : la question « où » (répartition
#    territoriale de la vacance) attend LOVAC (choix C-02).
#
# Prochaine étape de stabilisation : extraire les lectures de S-02/S-03 en
# fonctions testées (`src/logement/core/`), avec l'invariant de sommation en
# test de propriété, puis enregistrer O-xx/T-xx/R-xx dans `evidence/claims.yaml`.
