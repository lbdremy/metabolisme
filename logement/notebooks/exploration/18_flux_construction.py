# %% [markdown]
# # 18 — Le flux : formation de ménages et construction (article 3)
#
# Carnet d'exploration du stage `flux-construction` (core/flux.py),
# réécrit après la revue du 2026-09-18 : la première version lisait la
# série en date de prise en compte sans le sous-compte des déclarations
# (H-21) et écartait 2023-2024 comme « incomplètes » — deux erreurs qui
# inversaient la conclusion.

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
# Lecture estimée 2017-2022 : 1,14 en France, 1,08 en ZE tendues. Mais
# les années closes 2023-2024 : − 58 216/an dans les ZE tendues.

# %%
pd.DataFrame(payload["series_annuelles"])

# %%
pd.DataFrame(payload["deficits_tendues_2023_2024"])[
    ["name", "formation_menages_an", "besoin_flux_an", "commences_estimes_an", "solde_2023_2024_estime_an", "besoin_detente", "annees_absorption_2023_2024"]
]

# %%
payload["stock_vs_flux"]

# %% [markdown]
# Vérification à la main : H-21 = série estimée SDES / série communale
# 2017-2022 ; besoin de flux = ménages formés / (1 − part RS du neuf
# observée − part vacants 2022).

# %%
pd.DataFrame(payload["plus_gros_surplus_estimes"])[["name", "formation_menages_an", "commences_estimes_an", "ratio_estime", "tendue"]]
