# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
# ---

# %% [markdown]
# # Soldes migratoires par âge — instruction de SE-8 (revue du 2026-08-09)
#
# La revue contradictoire (SE-8) établit que le solde interne négatif des
# cœurs chers (Paris −1,40 %/an, R-13) est sous-déterminé : cycle de vie
# métropolitain (départs choisis des familles et des retraités, arrivées
# étudiantes) ou éviction (départs contraints par le marché) ? La
# décomposition par âge (AGEREVQ, présent dans S-29) est l'observation qui
# tranche EN PARTIE, calculable immédiatement : un profil « entrées 15-24,
# sorties nettes concentrées aux âges famille/retraite » est celui du
# cycle de vie ; des sorties anormalement étalées en âge (ou croissantes
# aux âges actifs sans enfants) renforceraient la lecture éviction.
#
# Périmètre : migrations INTERNES entre ZE (comme les soldes de R-13,
# IRAN 3-7), champ hors rattachement (D-18).

# %%
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

from logement.core import ze
from logement.core.lovac import plm_parent
from logement.shell import build

root = Path("..") / ".."
cut = pq.read_table(
    root / "data" / "raw" / "insee-rp2022-migcom.parquet",
    columns=["COMMUNE", "DCRAN", "IRAN", "IPONDI", "AGEREVQ"],
).to_pandas()
for col in ("COMMUNE", "DCRAN", "IRAN", "AGEREVQ"):
    cut[col] = cut[col].astype("string").str.strip()
cut["IPONDI"] = pd.to_numeric(cut["IPONDI"])
base = cut[cut["IRAN"] != "0"].copy()
base["age"] = pd.to_numeric(base["AGEREVQ"])
len(base), float(base["IPONDI"].sum())

# %% [markdown]
# ## Taux de mobilité annuelle par âge
#
# Le gradient attendu : maximal à 20-29 ans (~24 %), décroissant ensuite.
# C'est aussi l'ingrédient du shift-share démographique de SE-2 (le taux
# par âge quinquennal, croisé avec la structure par âges S-38).

# %%
GROUPS = ((0, 14, "0-14"), (15, 24, "15-24"), (25, 39, "25-39"), (40, 59, "40-59"), (60, 200, "60+"))


def groupe(age: float) -> str:
    for lo, hi, label in GROUPS:
        if lo <= age <= hi:
            return label
    raise ValueError(age)


base["groupe"] = base["age"].map(groupe)
mobile = base["IRAN"] != "1"
tot = base.groupby("groupe")["IPONDI"].sum()
mob = base[mobile].groupby("groupe")["IPONDI"].sum()
(mob / tot * 100).round(2)
# 0-14: 10,49 · 15-24: 17,86 · 25-39: 17,71 · 40-59: 6,77 · 60+: 3,78

# %%
tq = base.groupby("age")["IPONDI"].sum()
mq = base[mobile].groupby("age")["IPONDI"].sum()
(mq / tq * 100).round(2).head(20)
# Pic à 20-24 et 25-29 (24,2 %) ; au-delà de 95 ans les classes sont
# minuscules et bruitées (7-12 % sur quelques centaines de personnes
# pondérées) — à agréger en 95+ pour tout usage aval.

# %% [markdown]
# ## Paris (ZE 1109) : entrants, sortants et soldes internes par âge

# %%
commune_ze = ze.parse_commune_ze(build._read_membership(root))
ze_of = commune_ze.set_index("code")["ze"]
base["ze"] = base["COMMUNE"].map(ze_of)
movers = base[base["IRAN"].isin(("3", "4", "5", "6", "7"))].copy()
movers["ze_origine"] = movers["DCRAN"].map(plm_parent).map(ze_of)
inter = movers.dropna(subset=["ze", "ze_origine"])
inter = inter[inter["ze"] != inter["ze_origine"]]
PARIS = "1109"
tbl = pd.DataFrame(
    {
        "entrants": inter[inter["ze"] == PARIS].groupby("groupe")["IPONDI"].sum(),
        "sortants": inter[inter["ze_origine"] == PARIS].groupby("groupe")["IPONDI"].sum(),
        "population": base[base["ze"] == PARIS].groupby("groupe")["IPONDI"].sum(),
    }
)
tbl["solde"] = tbl["entrants"] - tbl["sortants"]
tbl["solde_pct_pop_groupe"] = (tbl["solde"] / tbl["population"] * 100).round(2)
tbl.round(0)

# %% [markdown]
# Résultat (pondéré) :
#
# | groupe | entrants | sortants | solde |
# |---|---|---|---|
# | 0-14 | 9 867 | 35 020 | −25 153 |
# | 15-24 | 53 967 | 35 798 | **+18 169** |
# | 25-39 | 50 252 | 87 119 | −36 868 |
# | 40-59 | 12 929 | 40 385 | −27 456 |
# | 60+ | 6 357 | 27 582 | −21 226 |
#
# Le SEUL groupe à solde positif est 15-24 (arrivées étudiantes/jeunes
# actifs) ; les sorties nettes se répartissent 0-14 : 22,7 %, 25-39 :
# 33,3 %, 40-59 : 24,8 %, 60+ : 19,2 % — les âges « famille » (25-39 +
# enfants 0-14) portent 56 % des sorties nettes, le reste est aux âges
# 40+ (dont retraite). C'est le profil CLASSIQUE du cycle de vie
# métropolitain (SE-8 : INSEE Analyses IdF n°59 documentait le même
# profil dès 2012).
#
# **Verdict pour I-13(3)** : la décomposition NE RENFORCE PAS la lecture
# « partir n'est pas toujours choisi » — le profil par âge est celui des
# départs de cycle de vie ; l'éviction n'est pas RÉFUTÉE (un départ de
# famille peut être contraint par les prix — l'âge ne dit pas le motif),
# mais le solde négatif parisien ne peut pas être publié comme indice de
# blocage. I-13(3) doit être requalifiée : solde = fait de cycle de vie,
# éviction = question ouverte (motifs non observables en open data).

# %% [markdown]
# ## Ce qui part en stabilisation
#
# - `migrations.py` : AGEREVQ entre dans le champ requis ; taux de
#   mobilité par groupe d'âge au national ; bloc Paris entrants/sortants/
#   solde par groupe publié dans l'artefact R-13.
# - Claims : O-xx (profil par âge), requalification I-13(3) (task 7).
