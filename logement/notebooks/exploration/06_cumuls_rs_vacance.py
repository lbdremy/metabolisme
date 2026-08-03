# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
# ---

# %% [markdown]
# # Exploration 06 — Dans les ZE à cumul RS + vacance, où est la vacance ?
#
# **Régime exploratoire** (méthode Métabolisme §2.1). Suite directe de
# I-05 : R-05 identifie 12 zones d'emploi cumulant plus de 20 % de
# résidences secondaires ET plus de 5 % de vacance structurelle (six
# corses, six rurales touristiques). Question infra-territoriale : à
# l'intérieur de ces ZE, la vacance est-elle dans les communes touristiques
# elles-mêmes (éviction) ou dans les communes non touristiques (déprise
# des centres et de l'arrière-pays) ?
#
# Données déjà figées : LOVAC communes (S-05, mill. 24), part RS communale
# (S-11, recensement 2022), table d'appartenance (S-06). Rappels : secret
# LOVAC sous 11 vacants (L-05 — les communes visibles seulement), parc
# privé vs parc entier (L-06).

# %%
import json
import zipfile
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

ROOT = Path.cwd()
while not (ROOT / "pyproject.toml").exists():
    ROOT = ROOT.parent
RAW = ROOT / "data" / "raw"
C1, C2 = "#2a78d6", "#eb6834"  # palette validée (dataviz)

from logement.core import lovac, rs, ze as ze_core
from logement.shell import build

# %% [markdown]
# ## 1. Base communale : vacance LOVAC × part RS × ZE

# %%
communes = lovac.parse_territories(
    pd.read_csv(RAW / build.LOVAC_COMMUNES, sep=";", encoding="cp1252", dtype=str),
    code_col="CODGEO_26", name_col="LIBGEO_26",
)
# aggregate_plm propage le secret : une commune masquée reste NaN (pas un
# faux zéro — piège attrapé à la première exécution : groupby().sum() de
# pandas transforme silencieusement NaN en 0).
VAC, STOCK = "pp_vacant_plus_2ans_2024", "ff_pp_total_2024"
lovac_com = lovac.aggregate_plm(communes, [VAC, STOCK]).rename(
    columns={VAC: "structurelle", STOCK: "parc_prive"}
)

with zipfile.ZipFile(RAW / build.CENSUS_ZIP) as zf, zf.open(build.CENSUS_CSV) as fh:
    census = rs.parse_census_housing(
        pd.read_csv(fh, sep=";", dtype=str, usecols=["CODGEO", *rs.CENSUS_COLS])
    )
census["part_rs_pct"] = census["P22_RSECOCC"] / census["P22_LOG"] * 100

with zipfile.ZipFile(RAW / build.APPARTENANCE_ZIP) as zf, zf.open(build.APPARTENANCE_XLSX) as fh:
    commune_ze = ze_core.parse_commune_ze(
        pd.read_excel(fh, sheet_name="COM", header=5, engine="calamine", dtype=str)
    )

base = (
    lovac_com.merge(census[["code", "part_rs_pct", "P22_LOG"]], on="code")
    .merge(commune_ze, on="code")
)
base["taux_structurelle_pct"] = base["structurelle"] / base["parc_prive"] * 100
visible = base.dropna(subset=["taux_structurelle_pct", "part_rs_pct"])
print(f"{len(base)} communes jointes, {len(visible)} visibles (LOVAC non secrétisé)")

# %% [markdown]
# ## 2. À l'intérieur des 12 ZE à cumul : RS communale × vacance communale

# %%
r05 = json.loads((ROOT / build.RS_OUTPUT).read_text(encoding="utf-8"))
outliers = {e["ze"]: e["name"] for e in r05["rs_and_vacancy_outliers"]}
print(f"{len(outliers)} ZE à cumul : {list(outliers.values())}")

rows = []
for ze_code, ze_name in outliers.items():
    sub = visible[visible["ze"] == ze_code]
    if len(sub) < 5:
        rows.append({"ze": ze_name, "n_communes_visibles": len(sub)})
        continue
    corr = sub["part_rs_pct"].rank().corr(sub["taux_structurelle_pct"].rank())
    hi_rs = sub["part_rs_pct"] > sub["part_rs_pct"].median()
    rows.append(
        {
            "ze": ze_name,
            "n_communes_visibles": len(sub),
            "spearman_rs_vacance": round(corr, 2),
            "vacance dans communes RS>médiane (%)": round(
                sub.loc[hi_rs, "structurelle"].sum() / sub["structurelle"].sum() * 100, 0
            ),
            "taux médian communes très RS": round(
                sub.loc[hi_rs, "taux_structurelle_pct"].median(), 1
            ),
            "taux médian communes peu RS": round(
                sub.loc[~hi_rs, "taux_structurelle_pct"].median(), 1
            ),
        }
    )
within = pd.DataFrame(rows)
print(within.to_string(index=False))

# %% [markdown]
# ## 3. Contexte national : la relation RS × vacance à l'échelle communale

# %%
pooled = visible["part_rs_pct"].rank().corr(visible["taux_structurelle_pct"].rank())
print(f"Spearman communal national (communes visibles) : {pooled:.2f}")
tourist_com = visible["part_rs_pct"] > 20
print(f"communes visibles > 20 % RS : {tourist_com.sum()} — taux structurel médian "
      f"{visible.loc[tourist_com, 'taux_structurelle_pct'].median():.1f} % vs "
      f"{visible.loc[~tourist_com, 'taux_structurelle_pct'].median():.1f} % ailleurs")

# %%
fig, ax = plt.subplots(figsize=(9, 5.5))
sub = visible[visible["ze"].isin(outliers)]
ax.scatter(visible["part_rs_pct"], visible["taux_structurelle_pct"], s=8, alpha=0.15,
           color="#999999", label="communes visibles (France)")
ax.scatter(sub["part_rs_pct"], sub["taux_structurelle_pct"], s=18, alpha=0.6,
           color=C2, label="communes des 12 ZE à cumul")
ax.set_xlabel("part de résidences secondaires de la commune (%)")
ax.set_ylabel("taux de vacance structurelle (%)")
ax.set_ylim(0, 25)
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f %%"))
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f %%"))
ax.set_title("Communes : part RS × vacance structurelle\n(gris : France visible ; orange : les 12 ZE à cumul RS+vacance)")
ax.grid(alpha=0.25)
ax.legend(frameon=False)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Observations provisoires — une question que l'open data ne tranche pas
#
# 1. **À l'intérieur des 12 ZE à cumul, la vacance est diffuse.** Les
#    communes très touristiques et peu touristiques y présentent des taux
#    médians également élevés (5-10 % des deux côtés dans la plupart des
#    ZE) ; les corrélations intra-ZE sont faibles et instables (−0,74 à
#    Avallon, +0,50 à Bastia/Ghisonaccia) sur de petits effectifs (3 à 27
#    communes visibles). Aucun schéma net « éviction côtière vs déprise
#    intérieure » ne se dégage à cette granularité.
# 2. **La secrétisation borne structurellement l'exercice** : dans la ZE de
#    Corte, 3 communes visibles seulement ; Propriano, 4. Les agrégats
#    intra-ZE reposent sur les seules communes à 11 vacants ou plus —
#    biais de sélection direct (L-05).
# 3. **À l'échelle communale nationale, l'association RS × vacance devient
#    positive** (+0,35 sur 6 895 communes visibles ; taux médian 3,8 %
#    au-dessus de 20 % de RS contre 3,1 %) — à rebours de l'échelle ZE
#    (+0,17, et vacance PLUS BASSE dans les ZE touristiques). Lecture
#    prudente : le biais de visibilité gonfle mécaniquement cette
#    association (être visible = avoir au moins 11 vacants).
# 4. **Conclusion méthodologique** : la question de l'éviction saisonnière
#    infra-territoriale n'est PAS tranchable avec l'open data secrétisé —
#    elle demanderait les données non secrétisées (habilitation), le
#    registre des meublés de tourisme, ou des monographies communales.
#    À consigner comme frontière de données plutôt qu'à forcer.

# %%
