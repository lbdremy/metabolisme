# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
# ---

# %% [markdown]
# # Exploration 11 — Le foncier immobilisé : friches d'activité en zones tendues
#
# **Régime exploratoire** (méthode Métabolisme §2.1). Nouvelle question
# ouverte par Rémy (2026-08-05) : quelle disponibilité de FONCIER, dans
# les zones tendues, est aujourd'hui immobilisée par des bâtiments vacants
# à usage non résidentiel (ateliers, stockage, artisanat, industrie…) ?
#
# Source ouverte : **Cartofriches** (S-20, Cerema) — 36 241 sites.
# Décisions (2026-08-05) : gisement central = « friche sans projet »
# (hors bâti résidentiel connu), variante haute + « friche potentielle » ;
# surfaces plafonnées à 50 ha par site (au-delà, un site n'est pas un
# projet résidentiel unique) ; conversion en capacité de logements par la
# **densité de référence haussmannienne** (H-11) — choisie par Rémy comme
# étalon d'un tissu résidentiel+commerces équilibré, marchable, où
# l'autonomie sans voiture est possible — DÉRIVÉE des données figées :
# logements par arrondissement parisien (S-11) / superficie (S-21), sur
# les arrondissements au bâti majoritairement d'avant 1919.
#
# Frontières : les bureaux vacants « en marché » (immobilier
# d'entreprise, ORIE/brokers) ne sont dans aucune donnée ouverte fine ;
# l'inventaire Cartofriches est PARTIEL et hétérogène — les totaux sont
# des planchers.

# %%
import zipfile
from pathlib import Path

import pandas as pd

ROOT = Path.cwd()
while not (ROOT / "pyproject.toml").exists():
    ROOT = ROOT.parent
RAW = ROOT / "data" / "raw"

H08_PCT = 6.0  # seuil de fluidité (H-08) — reconstruit les ZE tendues de R-07
HAUSSMANN_PRE1919_MIN_PCT = 60.0  # critère de sélection des arrondissements
CAP_SURFACE_M2 = 500_000.0  # plafond de 50 ha par site

PLM = {"751": "75056", "6938": "69123", "132": "13055"}


def plm_parent(code: str) -> str:
    """Map a PLM arrondissement code to its parent commune, else identity."""
    return next((city for p, city in PLM.items() if code.startswith(p)), code)


def to_num(series: pd.Series) -> pd.Series:
    """Parse LOVAC numbers: nbsp thousands separators, 's' (secret) -> NaN."""
    cleaned = series.astype("string").str.replace(r"[\s\xa0]", "", regex=True)
    return pd.to_numeric(cleaned.replace("s", pd.NA), errors="coerce")


# %% [markdown]
# ## 1. La densité de référence haussmannienne (H-11), dérivée de S-11 × S-21

# %%
cols = ["CODGEO", "P22_LOG", "P22_RP_ACHTOT", "P22_RP_ACH1919"]
with zipfile.ZipFile(RAW / "insee-rp-base-cc-logement-2022.zip") as zf:
    with zf.open("base-cc-logement-2022.CSV") as fh:
        census = pd.read_csv(fh, sep=";", dtype=str, usecols=cols)
paris = census[census["CODGEO"].str.match(r"^751\d\d$")].copy()
for c in cols[1:]:
    paris[c] = pd.to_numeric(paris[c], errors="coerce")
paris["part_avant_1919_pct"] = paris["P22_RP_ACH1919"] / paris["P22_RP_ACHTOT"] * 100

with zipfile.ZipFile(RAW / "insee-comparateur-territoires-2026.zip") as zf:
    with zf.open("comparateur.csv") as fh:
        comp = pd.read_csv(
            fh, sep=";", dtype=str,
            usecols=["GEO_OBJECT", "GEO", "TIME_PERIOD", "TAB_MEASURE", "OBS_VALUE"],
        )
sup = comp[
    (comp["GEO_OBJECT"] == "ARM") & (comp["TAB_MEASURE"] == "SUP")
    & (comp["GEO"].str.match(r"^751\d\d$"))
].copy()
sup["km2"] = pd.to_numeric(sup["OBS_VALUE"], errors="coerce")
sup = sup.sort_values("TIME_PERIOD").groupby("GEO")["km2"].last()

paris = paris.set_index("CODGEO").join(sup.rename("km2"), how="inner")
paris["densite_logts_ha"] = paris["P22_LOG"] / (paris["km2"] * 100)
haussmann = paris[paris["part_avant_1919_pct"] >= HAUSSMANN_PRE1919_MIN_PCT]
print(f"{len(paris)} arrondissements ; {len(haussmann)} retenus "
      f"(part RP avant 1919 ≥ {HAUSSMANN_PRE1919_MIN_PCT:.0f} %)")
print(haussmann[["part_avant_1919_pct", "km2", "densite_logts_ha"]]
      .sort_values("densite_logts_ha").round(1).to_string())
h11_central = haussmann["densite_logts_ha"].median()
h11_lo, h11_hi = haussmann["densite_logts_ha"].min(), haussmann["densite_logts_ha"].max()
print(f"\nH-11 (logements/ha, brut voirie comprise) : centre {h11_central:.0f}, "
      f"plage [{h11_lo:.0f}, {h11_hi:.0f}]")

# %% [markdown]
# ## 2. Friches par ZE tendue (S-20 × R-07)

# %%
friches = pd.read_csv(RAW / "cerema-cartofriches-2026-06-15.csv", sep=";", dtype=str,
                      na_values=["NA"])
friches["code"] = friches["comm_insee"].astype("string").str.strip().map(plm_parent)
friches["surface_m2"] = pd.to_numeric(friches["unite_fonciere_surface"], errors="coerce")
residentiel = friches["bati_type"].str.lower().str.startswith("r", na=False)
capped = friches["surface_m2"] > CAP_SURFACE_M2
friches["surface_capee_m2"] = friches["surface_m2"].clip(upper=CAP_SURFACE_M2)
print(f"{len(friches)} sites ; {int(residentiel.sum())} à bâti résidentiel connu (exclus) ; "
      f"{int(capped.sum())} plafonnés à 50 ha")
base = friches[~residentiel & friches["surface_m2"].notna()]

with zipfile.ZipFile(RAW / "insee-table-appartenance-geo-communes-2026.zip") as zf:
    with zf.open("table-appartenance-geo-communes-2026.xlsx") as fh:
        appartenance = pd.read_excel(fh, sheet_name="COM", header=5, engine="calamine", dtype=str)
com_ze = appartenance[["CODGEO", "ZE2020"]].dropna().rename(
    columns={"CODGEO": "code", "ZE2020": "ze"}
)

# ZE tendues : reconstruction R-07 (vacance disponible < H-08)
with zipfile.ZipFile(RAW / "insee-rp-base-cc-logement-2022.zip") as zf:
    with zf.open("base-cc-logement-2022.CSV") as fh:
        logvac = pd.read_csv(fh, sep=";", dtype=str, usecols=["CODGEO", "P22_LOG", "P22_LOGVAC"])
logvac = pd.DataFrame(
    {
        "code": logvac["CODGEO"].str.strip().map(plm_parent),
        "parc": pd.to_numeric(logvac["P22_LOG"], errors="coerce"),
        "vacants": pd.to_numeric(logvac["P22_LOGVAC"], errors="coerce"),
    }
).drop_duplicates(subset="code", keep="first")
communes_lovac = pd.read_csv(
    RAW / "lovac-opendata-communes26.csv", sep=";", encoding="cp1252", dtype=str
)
communes_lovac.columns = [c.strip() for c in communes_lovac.columns]
lovac = pd.DataFrame(
    {
        "code": communes_lovac["CODGEO_26"].str.strip().map(plm_parent),
        "structurelle": to_num(communes_lovac["pp_vacant_plus_2ans_24"]),
    }
)
ze = logvac.merge(com_ze, on="code", how="left").dropna(subset=["ze"]).groupby("ze")[
    ["parc", "vacants"]
].sum()
ze = ze.join(
    lovac.merge(com_ze, on="code", how="left").dropna(subset=["ze"])
    .groupby("ze")[["structurelle"]].sum(min_count=1),
    how="inner",
)
ze["taux_disponible_pct"] = (ze["vacants"] - ze["structurelle"]) / ze["parc"] * 100
tendues = set(ze.index[ze["taux_disponible_pct"] < H08_PCT])
ze["besoin"] = (H08_PCT / 100 * ze["parc"] - (ze["vacants"] - ze["structurelle"]))
besoin_total = float(ze.loc[list(tendues), "besoin"].sum())
print(f"{len(tendues)} ZE tendues (contrôle R-07) ; besoin {besoin_total:,.0f}")

# %%
fr_ze = base.merge(com_ze, on="code", how="left").dropna(subset=["ze"])
fr_tendues = fr_ze[fr_ze["ze"].isin(tendues)]
central = fr_tendues[fr_tendues["site_statut"] == "friche sans projet"]
haute = fr_tendues[fr_tendues["site_statut"].isin(["friche sans projet", "friche potentielle"])]
for label, sub in [("central (sans projet)", central), ("haute (+ potentielles)", haute)]:
    ha = sub["surface_capee_m2"].sum() / 1e4
    brut = sub["surface_m2"].sum() / 1e4
    print(f"{label}: {len(sub)} sites, {ha:,.0f} ha plafonnés ({brut:,.0f} ha bruts), "
          f"dans {sub['ze'].nunique()} ZE tendues")

# %% [markdown]
# ## 3. Capacité de logements à densité haussmannienne, vs besoin R-07

# %%
names = pd.read_excel(
    RAW / "insee-emploi-zone-1998-2018.xlsx", sheet_name="Emploi total - ZE",
    header=4, engine="calamine",
)["Zone d'emploi"].astype("string").str.extract(r"^(\d{4}) - (.*)$").dropna()

for label, sub in [("central (sans projet)", central), ("haute (+ potentielles)", haute)]:
    ha = sub["surface_capee_m2"].sum() / 1e4
    for dens_label, dens in [("bas", h11_lo), ("central", h11_central), ("haut", h11_hi)]:
        capacite = ha * dens
        print(f"{label} × densité {dens_label} ({dens:.0f}/ha) : "
              f"{capacite:,.0f} logements ({capacite / besoin_total:.1f} × le besoin)")
    print()

top = (central.groupby("ze")["surface_capee_m2"].agg(["sum", "count"])
       .join(names.set_index(0)[1].rename("ze_nom")))
top["ha"] = top["sum"] / 1e4
top["capacite_centrale"] = top["ha"] * h11_central
top = top.join(ze["besoin"], how="left")
print("les 10 plus gros gisements fonciers (ZE tendues, sans projet, plafonné) :")
print(top.nlargest(10, "ha")[["ze_nom", "count", "ha", "capacite_centrale", "besoin"]]
      .round(0).to_string())

# %%
couvertes = (top["capacite_centrale"] >= top["besoin"]).sum()
print(f"ZE tendues avec ≥ 1 friche sans projet : {len(top)} / {len(tendues)}")
print(f"...dont capacité centrale ≥ besoin : {int(couvertes)}")

# %% [markdown]
# ## Observations provisoires (vérifiées depuis les sorties ci-dessus)
#
# 1. **La densité de référence haussmannienne (H-11) dérivée des données
#    figées** : 7 arrondissements parisiens au bâti ≥ 60 % d'avant 1919
#    (1ᵉʳ, 2ᵉ, 3ᵉ, 4ᵉ, 6ᵉ, 8ᵉ, 9ᵉ) ; densité brute (voirie comprise) de
#    70,6 (8ᵉ — quartier de bureaux) à 225,7 logements/ha (3ᵉ), médiane
#    **147,2 logements/ha**. Les 16ᵉ/17ᵉ ne passent pas le critère
#    objectif (extensions 1920-30) — le critère est traçable, pas
#    esthétique.
# 2. **Le gisement foncier des zones tendues est massif même au sens le
#    plus strict** : 4 052 friches « sans projet » à bâti non résidentiel
#    dans 134 des 142 ZE tendues, **22 328 ha plafonnés** (80 196 ha
#    bruts — le plafond de 50 ha/site écrête 72 % des surfaces brutes,
#    1 048 sites plafonnés au national).
# 3. **Converti à densité haussmannienne : ~3,3 M de logements de
#    capacité, soit 11,5 × le besoin de détente R-07** (5,5 × à la
#    densité basse, 17,6 × à la haute ; variante + potentielles :
#    jusqu'à 36 ×). 115 des 134 ZE tendues pourvues couvriraient leur
#    besoin par leurs seules friches sans projet — y compris Paris
#    (578 ha → ~85 000 logements vs besoin 8 649), Marseille et
#    Bordeaux. **Le foncier immobilisé n'est pas la contrainte de la
#    détente ; la contrainte est ailleurs (remobilisation, blocages,
#    coût — R-08/R-09).**
# 4. **La géographie du foncier est industrielle** : les plus gros
#    gisements sont Lens (1 726 ha — legs minier), Tarbes-Lourdes, Caen,
#    Rouen, Thionville — pas les métropoles les plus tendues ; mais
#    celles-ci ont quand même largement de quoi couvrir leur besoin.
# 5. Limites majeures (L-15) : inventaire Cartofriches PARTIEL et
#    hétérogène (les totaux sont des planchers, les comparaisons fines
#    entre ZE non fiables) ; surface d'unité foncière ≠ surface
#    constructible (pollution BASIAS, zonage, rétention) ; la capacité
#    est un POTENTIEL d'urbanisme à densité de référence, pas un
#    programme (coûts de dépollution/démolition non chiffrés) ; les
#    bureaux vacants en marché restent hors champ (frontière ORIE/privé).
#
# Prochaine étape de stabilisation : H-11 au registre + R-10/I-10/C-08/
# L-15 dans le graphe.

# %%
