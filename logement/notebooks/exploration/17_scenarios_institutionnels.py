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
# Vérification manuelle (après revue : tout au m², charges fixes par
# logement) : coût médian €/m² × facteur 40 ans à 2,30 % + 2 652 € /
# surface → / 12.

# %%
m_b = payload["m_b_operateur_acquisition"]
af = institution.annuity_factor(2.30, 40)
cout_m2 = m_b["central"]["cout_renove_m2_median_eur"]
print(f"facteur {af:.5f}")
print(f"loyer d'équilibre d'un appartement de 65,5 m² à {cout_m2} €/m² : "
      f"{institution.equilibrium_rent_m2(cout_m2, af, 2652.0, 65.5):.2f} €/m²/mois")
print(f"neuf S-18 : {institution.equilibrium_rent_m2(2550.0, af, 2652.0, institution.SURFACE_NEUF_M2):.2f}")
m_b["central"]

# %%
pd.DataFrame(m_b["loyer_equilibre_le_plus_haut"])

# %% [markdown]
# Le fait saillant : acheter un vacant à la valeur vénale d'une zone
# tendue puis le rénover coûte PLUS au m² qu'un logement social neuf
# (3 776 vs 2 550 €/m²) — le ratio ~2 de R-09 ne valait que pour les
# travaux (L-14 le disait : « tendrait vers ~1 » — il passe sous 1).
# La première version de ce carnet concluait « le neuf s'équilibre au
# marché » : erreur d'unité (169 200 € divisés par la surface des RP au
# lieu des 66 m² de S-18), attrapée par la revue du 2026-09-18.

# %%
pd.DataFrame(
    {k: v for k, v in m_b["sensibilite"].items() if k.startswith("h1")}
).T

# %% [markdown]
# ## M-C — le bail à réhabilitation (sans acquisition)
# Travaux seuls amortis sur 30 ans (H-19), hors TFPB : loyer d'équilibre
# ~3,7 €/m², sous le loyer social partout — mais le volume dépend du
# consentement, et la cession à la valeur vénale domine le bail (I-16).

# %%
pd.DataFrame(payload["m_c_bail_rehabilitation"]["grille_consentement"])

# %% [markdown]
# ## M-D — la bascule DMTO → détention
# 11,9 Md€ (2025, périmètre OFGL) / 34,6 M de logements du même
# périmètre = 344 €/logement/an ; le droit DÉPARTEMENTAL médian
# (~7 250 €) vaut ~21 ans de cette charge (29 ans en ZE tendues).

# %%
m_d = payload["m_d_bascule_dmto"]
{k: v for k, v in m_d.items() if not k.startswith("bascule")}

# %%
pd.DataFrame(m_d["bascule_la_plus_favorable_au_mobile"])
