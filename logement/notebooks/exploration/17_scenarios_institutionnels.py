# %% [markdown]
# # 17 — Scénarios institutionnels (session 7, 2026-09-18)
#
# Carnet d'exploration de la proposition : on lit l'artefact produit par
# le stage `scenarios-institutionnels` (core/institution.py) et on
# vérifie à la main les ordres de grandeur avant d'écrire les nœuds
# R-15..R-17. Le calcul stabilisé est dans `src/` ; ce carnet ne publie
# rien (INTRO §6.3). Décisions prises en chemin :
# `evidence/decisions-2026-09-18.md`.

# %%
from __future__ import annotations

import json

import pandas as pd

from logement.config import project_root
from logement.core import institution
from logement.shell import build

ROOT = project_root()
payload = json.loads((ROOT / build.INSTITUTION_OUTPUT).read_text(encoding="utf-8"))
payload["perimetre"]

# %% [markdown]
# ## M-A — le canal incitatif seul (référence)
# Grille H-14 × horizon : à 0,75 %/an (constat ZLV de la Cour des
# comptes), le canal sort ~7,5 % du gisement en dix ans — 8 % du besoin.

# %%
pd.DataFrame(payload["m_a_canal_incitatif"]["grille"])

# %% [markdown]
# ## M-B — l'opérateur qui acquiert
# Vérification manuelle du facteur d'annuité et du loyer d'équilibre
# médian : 248 k€ de coût unitaire × facteur 40 ans à 2,30 % → annuité →
# / (1 − 0,549) → / 12 / surface.

# %%
m_b = payload["m_b_operateur_acquisition"]
af = institution.annuity_factor(2.30, 40)
unit = m_b["central"]["cout_unitaire_renove_median_eur"]
annuite = unit * af
loyer_annuel = institution.equilibrium_rent(annuite, 0.549)
print(f"facteur {af:.5f}  annuité {annuite:,.0f} €  loyer net {loyer_annuel:,.0f} €/an")
print(f"soit {loyer_annuel / 12 / 65.5:.2f} €/m²/mois pour un appartement de 65,5 m²")
m_b["central"]

# %%
pd.DataFrame(m_b["loyer_equilibre_le_plus_haut"])

# %% [markdown]
# Le fait saillant : acheter un vacant à la valeur vénale d'une zone
# tendue (prix médian) puis le rénover coûte PLUS qu'un logement social
# neuf (169 200 €, foncier compris) — le ratio ~2 de R-09 ne valait que
# pour les travaux (L-14 le disait : « tendrait vers ~1 » — il passe
# sous 1). D'où le loyer d'équilibre du segment NEUF (≈ marché) plus bas
# que celui du segment rénové-acquis.

# %%
pd.DataFrame(
    {k: v for k, v in m_b["sensibilite"].items() if k.startswith("h1")}
).T

# %% [markdown]
# ## M-C — le bail à réhabilitation (sans acquisition)
# Travaux seuls amortis sur 30 ans : loyer d'équilibre ~4 €/m², sous le
# loyer social partout — mais le volume dépend du consentement.

# %%
pd.DataFrame(payload["m_c_bail_rehabilitation"]["grille_consentement"])

# %% [markdown]
# ## M-D — la bascule DMTO → détention
# 9,9 Md€ (2024, périmètre OFGL) / 34,6 M de logements du même périmètre
# = 286 €/logement/an ; le péage fiscal médian (~9 400 €) vaut ~33 ans
# de cette charge (44 ans en ZE tendues).

# %%
m_d = payload["m_d_bascule_dmto"]
{k: v for k, v in m_d.items() if not k.startswith("bascule")}

# %%
pd.DataFrame(m_d["bascule_la_plus_favorable_au_mobile"])
