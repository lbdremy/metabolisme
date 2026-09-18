# %% [markdown]
# # 18 — Le flux : formation de ménages et construction (article 3)
#
# Carnet d'exploration du stage `flux-construction` (core/flux.py) :
# lecture de l'artefact, vérification à la main du besoin de flux, et
# la découverte qui a fait publier la variante hors RS.

# %%
from __future__ import annotations

import json

import pandas as pd

from logement.config import project_root
from logement.shell import build

ROOT = project_root()
payload = json.loads((ROOT / build.FLUX_OUTPUT).read_text(encoding="utf-8"))
pd.DataFrame({k: payload[k] for k in ("national", "tendues", "autres")})

# %% [markdown]
# Le ratio national est 1,04 : la France construit ce que ses ménages
# forment (au sens de la structure 2022). Les ZE tendues : 0,97 avec RS,
# 1,13 hors RS — le déficit est la structure touristique.

# %%
pd.DataFrame(payload["deficits_tendues"])[
    ["name", "formation_menages_an", "commences_an", "solde_flux_an", "solde_flux_hors_rs_an", "part_rs_2022_pct"]
]

# %%
payload["stock_vs_flux"]

# %% [markdown]
# Vérification à la main : Perpignan, part RS 29,9 %, part vacants ~9 % →
# 1/(1 − 0,299 − 0,09) ≈ 1,64 logement par ménage formé ; hors RS
# 1/(1 − 0,09) ≈ 1,10. Avec 2 895 ménages/an : besoin 4 750 vs 3 180.

# %%
pd.DataFrame(payload["plus_gros_surplus"])[["name", "formation_menages_an", "commences_an", "ratio_production", "tendue"]]
