# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
# ---

# %% [markdown]
# # Exploration 12 — La rotation du parc : ancienneté d'emménagement par ZE
#
# **Régime exploratoire** (méthode Métabolisme §2.1). Première instruction
# de **H-04 (mobilités empêchées)** du cadrage (`INTRO.md` §4) : si le
# système de logement fonctionne mal, une part des ménages qui voudraient
# bouger ne le peuvent pas — et la trace observable de cette friction est
# la ROTATION effective du parc, mesurée ici par l'ancienneté
# d'emménagement du recensement (D-16).
#
# Sources (registre `sources/sources.yaml`, sha256 vérifiés par
# `uv run logement validate`) :
#
# - **S-27** — RP « Logement en 2023 » (Melodi DS_RP_LOGEMENT_PRINC) :
#   résidences principales par classe d'ancienneté d'emménagement
#   (dimension européenne L_STAY, 6 classes), diffusées NATIVEMENT à la
#   maille ZE2020, trois millésimes comparables par construction
#   (2012, 2017, 2023 — concepts 2023, géographie COG 2026).
# - Croisements : tension R-07 (reconstruite depuis S-05/S-06/S-11/S-13
#   avec H-08 et H-12 centraux), vacance structurelle par ZE (S-05),
#   indice de coût résidentiel R-04 (S-09/S-10).
#
# Précautions de lecture (D-16) : la part d'emménagés récents mesure la
# rotation DU PARC, pas la mobilité DES PERSONNES ; l'ancienneté est
# datée au premier occupant arrivé ; les classes L_STAY 2023 ne se
# raccordent pas aux bases ANEM des diffusions antérieures.

# %%
from pathlib import Path

import pandas as pd
import pyarrow.compute as pc
import pyarrow.parquet as pq

ROOT = Path.cwd()
while not (ROOT / "pyproject.toml").exists():
    ROOT = ROOT.parent
RAW = ROOT / "data" / "raw"

pd.set_option("display.width", 160)

# %% [markdown]
# ## 1. Charger la mesure DWELLINGS × L_STAY (résidences principales)
#
# Le fichier S-27 croise toutes les dimensions ; la coupe utile est :
# mesure `DWELLINGS`, statut `DW_MAIN` (résidences principales), toutes
# les autres dimensions au total `_T`, détail `L_STAY`, aux niveaux
# `ZE2020` et `FRANCE`.

# %%
import pyarrow as pa

table = pq.read_table(RAW / "insee-rp-logement-princ-2023.parquet")
mask = pc.and_(
    pc.is_in(table["GEO_OBJECT"].cast("string"), value_set=pa.array(["ZE2020", "FRANCE"])),
    pc.equal(table["RP_MEASURE"].cast("string"), "DWELLINGS"),
)
cut = table.filter(mask).to_pandas()
for col in ("GEO", "GEO_OBJECT", "L_STAY", "OCS", "TDW", "NRG_SRC", "CARPARK", "NOR", "TSH", "CARS", "BUILD_END"):
    cut[col] = cut[col].astype("string")
totals = (
    (cut["OCS"] == "DW_MAIN")
    & (cut["TDW"] == "_T")
    & (cut["NRG_SRC"] == "_T")
    & (cut["CARPARK"] == "_T")
    & (cut["NOR"] == "_T")
    & (cut["TSH"] == "_T")
    & (cut["CARS"] == "_T")
    & (cut["BUILD_END"] == "_T")
)
anem = cut[totals].copy()
anem["annee"] = pd.to_datetime(anem["TIME_PERIOD"]).dt.year
wide = anem.pivot_table(
    index=["GEO_OBJECT", "GEO", "annee"], columns="L_STAY", values="OBS_VALUE", aggfunc="first"
)
print(wide.shape)
print(wide.head(3).round(0).to_string())

# %% [markdown]
# ### Contrôle interne : la somme des 6 classes recoupe-t-elle le total `_T` ?

# %%
CLASSES = ["Y_LT2", "Y2T4", "Y5T9", "Y10T19", "Y20T29", "Y_GE30"]
ecart_rel = (wide[CLASSES].sum(axis=1) - wide["_T"]).abs() / wide["_T"]
print(f"écart relatif max classes vs total : {ecart_rel.max():.2e}")
assert ecart_rel.max() < 1e-6

# %% [markdown]
# ## 2. Le niveau national : la rotation ralentit
#
# Parts de chaque classe d'ancienneté dans les résidences principales,
# France hors Mayotte, aux trois millésimes comparables du fichier.

# %%
# Deux séries nationales dans le fichier : F = France hors Mayotte (le
# périmètre de S-27), FM = France métropolitaine. On garde F, cohérent
# avec le reste de la chaîne (périmètres jamais mélangés, cf. core/stats).
fr = wide.loc[("FRANCE", "F")]
parts_fr = fr[CLASSES].div(fr["_T"], axis=0) * 100
parts_fr["moins_5_ans"] = parts_fr["Y_LT2"] + parts_fr["Y2T4"]
print(parts_fr.round(2).to_string())

# %%
delta_lt2 = parts_fr.loc[2023, "Y_LT2"] - parts_fr.loc[2012, "Y_LT2"]
delta_lt5 = parts_fr.loc[2023, "moins_5_ans"] - parts_fr.loc[2012, "moins_5_ans"]
rp_2023 = fr.loc[2023, "_T"]
manque_lt2 = -delta_lt2 / 100 * rp_2023
print(
    f"part des emménagés de moins de 2 ans : {parts_fr.loc[2012, 'Y_LT2']:.2f} % (2012) "
    f"-> {parts_fr.loc[2017, 'Y_LT2']:.2f} % (2017) -> {parts_fr.loc[2023, 'Y_LT2']:.2f} % (2023), "
    f"soit {delta_lt2:+.2f} pts"
)
print(
    f"part des emménagés de moins de 5 ans : {parts_fr.loc[2012, 'moins_5_ans']:.2f} % -> "
    f"{parts_fr.loc[2023, 'moins_5_ans']:.2f} %, soit {delta_lt5:+.2f} pts"
)
print(
    f"en volume 2023 ({rp_2023:,.0f} RP) : {manque_lt2:,.0f} emménagements récents "
    "« manquants » vs une rotation restée au niveau de 2012 (ordre de grandeur descriptif)"
)

# %% [markdown]
# ## 3. Par zone d'emploi (2023) : où le parc tourne-t-il le moins ?

# %%
ze_wide = wide.loc["ZE2020"]
ze_parts = ze_wide[CLASSES].div(ze_wide["_T"], axis=0) * 100
ze_parts["moins_2_ans"] = ze_parts["Y_LT2"]
ze_parts["moins_5_ans"] = ze_parts["Y_LT2"] + ze_parts["Y2T4"]
p23 = ze_parts.xs(2023, level="annee")
print(f"{len(p23)} ZE — part des emménagés de moins de 2 ans (2023) :")
print(p23["moins_2_ans"].describe().round(2).to_string())

# %%
import sys

sys.path.insert(0, str(ROOT / "src"))
from logement.shell import build  # noqa: E402

names = build._ze_names(ROOT)
tbl = p23[["moins_2_ans", "moins_5_ans"]].join(names, how="left")
print("rotation la plus faible (part < 2 ans) :")
print(tbl.nsmallest(10, "moins_2_ans").round(2).to_string())
print("\nrotation la plus forte :")
print(tbl.nlargest(10, "moins_2_ans").round(2).to_string())

# %% [markdown]
# ## 4. Évolution 2012 → 2023 par ZE : la chute est-elle générale ?

# %%
p12 = ze_parts.xs(2012, level="annee")
delta = (p23["moins_2_ans"] - p12["moins_2_ans"]).rename("delta_pts")
evol = pd.DataFrame({"part_2012": p12["moins_2_ans"], "part_2023": p23["moins_2_ans"], "delta_pts": delta}).join(
    names, how="left"
)
n_baisse = int((evol["delta_pts"] < 0).sum())
print(f"{n_baisse} ZE sur {len(evol)} en baisse de rotation 2012->2023")
print(evol["delta_pts"].describe().round(2).to_string())
print("\nplus fortes baisses :")
print(evol.nsmallest(10, "delta_pts").round(2).to_string())
print("\nZE en hausse :")
print(evol[evol["delta_pts"] > 0].sort_values("delta_pts", ascending=False).round(2).to_string())

# %% [markdown]
# ## 5. Croisements : la rotation faible coïncide-t-elle avec la tension,
# ## la vacance basse et le coût ?
#
# Reconstruction de la frame de tension R-07 (H-08 = 6 %, H-12 = 0,75,
# valeurs centrales du registre) et de l'indice de coût R-04, par les
# mêmes fonctions stabilisées que `reproduce`.

# %%
import zipfile  # noqa: E402

from logement.core import lovac, rs, stats, tension, ze  # noqa: E402

census_raw = None
with zipfile.ZipFile(RAW / "insee-rp-base-cc-logement-2022.zip") as zf, zf.open(
    "base-cc-logement-2022.CSV"
) as fh:
    census_raw = pd.read_csv(fh, sep=";", dtype=str, usecols=["CODGEO", *rs.CENSUS_COLS])
census = rs.parse_census_housing(census_raw)
tlv = tension.parse_tlv(pd.read_csv(RAW / "zonage-tlv-decret-2025-12-22.csv", sep=";", dtype=str))
commune_ze = ze.parse_commune_ze(build._read_membership(ROOT))
communes = lovac.parse_territories(
    pd.read_csv(RAW / "lovac-opendata-communes26.csv", sep=";", encoding="cp1252", dtype=str),
    code_col="CODGEO_26",
    name_col="LIBGEO_26",
)
h08 = build._load_hypothesis(ROOT, "H-08")
h12 = build._load_hypothesis(ROOT, "H-12")
tension_frame = tension.tension_by_ze(
    census, tlv, communes, commune_ze, h08.central_value, h12.central_value
)
vacancy_ze, _ = ze.aggregate_vacancy_by_ze(communes, commune_ze)
cost = build._cost_frame(ROOT)

cross = (
    p23[["moins_2_ans", "moins_5_ans"]]
    .join(tension_frame["tendue"], how="left")
    .join(vacancy_ze["structural_rate_pct"], how="left")
    .join(cost["indice_cout_pct"], how="left")
    .join(delta, how="left")
)
print(cross.head(3).round(2).to_string())

# %%
med = cross.groupby("tendue")[["moins_2_ans", "delta_pts"]].median().round(2)
print("médianes par statut de tension (2023) :")
print(med.to_string())

# %%
print("part < 2 ans × taux de vacance structurelle :")
print(stats.spearman_by_perimeter(cross, "moins_2_ans", "structural_rate_pct"))
print("part < 2 ans × indice de coût résidentiel :")
print(stats.spearman_by_perimeter(cross, "moins_2_ans", "indice_cout_pct"))
print("chute 2012->2023 × indice de coût :")
print(stats.spearman_by_perimeter(cross, "delta_pts", "indice_cout_pct"))
print("chute 2012->2023 × vacance structurelle :")
print(stats.spearman_by_perimeter(cross, "delta_pts", "structural_rate_pct"))

# %% [markdown]
# ## 6. Constats (relus depuis les sorties ci-dessus, exécution du
# ## 2026-08-08)
#
# 1. **La rotation du parc ralentit au niveau national** : la part des
#    résidences principales occupées depuis moins de 2 ans passe de
#    13,14 % (2012) à 12,89 % (2017) puis 11,97 % (2023) — la chute
#    s'accélère (−0,25 pt en 5 ans, puis −0,92 pt en 6 ans). Rapportée au
#    parc 2023 (31,2 M RP), la rotation perdue vaut ~364 000
#    emménagements récents (ordre de grandeur descriptif, pas un flux
#    annuel). La baisse se concentre sur la classe « moins de 2 ans » :
#    la part « moins de 5 ans » ne perd que 0,43 pt (la classe 2-4 ans
#    GAGNE 0,74 pt — les ménages entrés ne re-bougent plus aussi vite).
# 2. **La chute est quasi générale : 293 ZE sur 305 en baisse**
#    (médiane −1,36 pt, quartiles −1,77 / −0,93). Les rares hausses sont
#    des territoires singuliers (Corte +2,24, Ouest-Guyanais +2,19,
#    Est-littoral +1,67, puis Saclay +0,52 et des hausses ≤ 0,31 pt).
# 3. **Le NIVEAU de rotation reflète la fonction du territoire, pas la
#    détente du marché** : rotation la plus forte dans les ZE
#    étudiantes/métropolitaines chères (Corte 23,5 %, Toulouse 16,9,
#    Montpellier 16,1, Rennes 15,5, Lille 15,0, Bordeaux 14,9) ;
#    corrélation POSITIVE part < 2 ans × indice de coût (rho métropole
#    +0,40, IC95 [+0,30, +0,49], n = 287) et NÉGATIVE avec la vacance
#    structurelle (rho métropole −0,22, IC95 [−0,33, −0,11], n = 287) :
#    les marchés détendus (Antilles, Sarreguemines, Vallée de la
#    Bresle, Abbeville — parts < 2 ans de 6 à 8,3 %) tournent PEU.
# 4. **La CHUTE, elle, est plus forte là où le logement est cher et la
#    vacance rare** : delta 2012→2023 × indice de coût rho métropole
#    −0,29 (IC95 [−0,39, −0,18]) ; delta × vacance structurelle rho
#    +0,25 (IC95 [+0,14, +0,36]) ; médiane du delta −1,54 pt dans les
#    97 ZE tendues (R-07 central) contre −1,27 pt ailleurs. C'est le
#    signal attendu de H-04 : le gel de la rotation se concentre dans
#    les marchés verrouillés — pendant que dans les marchés détendus la
#    rotation, déjà faible, baisse moins.
#
# Limites à porter avec ces constats (pour la stabilisation) :
#
# - **Effet de composition démographique non contrôlé** : le
#   vieillissement élève mécaniquement l'ancienneté (les ménages âgés
#   déménagent peu) — une partie de la chute nationale est
#   démographique, pas un blocage. Le GRADIENT territorial de la chute
#   (constat 4) est le signal le moins exposé à cette critique (le
#   vieillissement est national), mais les structures d'âge diffèrent
#   aussi entre ZE.
# - La classe « moins de 2 ans » du millésime 2023 recouvre des
#   emménagements ~2021-2023 (collecte EAR 2021-2025) : période
#   post-COVID atypique.
# - Rotation du parc ≠ mobilité des personnes (D-16) : un marché peut
#   gonfler sa rotation par les seules premières installations
#   (étudiants) sans que les ménages en place puissent bouger.
# - Périmètres : corrélations coût sur n = 297 (loyers absents de
#   certaines ZE), vacance sur n = 305 ; lecture métropole vs France
#   entière jamais mélangée (core/stats).
