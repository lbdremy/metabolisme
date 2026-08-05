# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
# ---

# %% [markdown]
# # Exploration 08 — Tension des usages : manque absolu et gisement vacant
#
# **Régime exploratoire** (méthode Métabolisme §2.1). Trois questions
# (décisions du 2026-08-05) :
#
# 1. **Quelles zones sont tendues ?** Deux lectures croisées : la
#    catégorie légale (zonage TLV, D-14/S-13 — « 1. Zone tendue » agglos,
#    « 2. Zone touristique et tendue ») et notre mesure de marché (taux de
#    vacance totale du recensement sous le seuil de fluidité H-08 = 6 %,
#    plage 5-7, D-15).
# 2. **Quel volume ABSOLU manque pour la détente ?** Combien de logements
#    supplémentaires il faudrait pour remonter la vacance au seuil H-08 :
#    `N = (t·P − V) / (1 − t)` (les logements ajoutés entrent au parc ET
#    dans les vacants disponibles).
# 3. **Le gisement vacant local suffirait-il ?** La vacance STRUCTURELLE
#    (LOVAC, sortie de l'usage) est comptée dans V mais ne sert pas le
#    marché. La « vacance disponible » est `V − S`. Remobiliser M
#    logements structurels ajoute M à la vacance disponible sans changer
#    le parc : le besoin de mobilisation est `M = t·P − (V − S)` et la
#    couverture est `S / M` — en NOMBRES ABSOLUS, comme le demande la
#    question (le % de la vacance ne dit rien).
#
# Précautions : vacance recensement 2022 (parc entier, D-03) vs vacance
# LOVAC mill. 24 (parc privé, fiscal) — périmètres différents (L-06), la
# vacance disponible `V − S` est donc une approximation (S sous-estime la
# vacance hors marché du parc entier → couverture plutôt SURESTIMÉE...
# mais V recensement > V fiscal dans les grandes villes, sens inverse).
# Le seuil H-08 est un ordre de grandeur d'usage (confiance basse).

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

H08_PCT = 6.0  # seuil de fluidité (H-08), plage [5, 7]
H08_RANGE = (5.0, 7.0)

PLM = {"751": "75056", "6938": "69123", "132": "13055"}


def plm_parent(code: str) -> str:
    """Map a PLM arrondissement code to its parent commune, else identity."""
    return next((city for p, city in PLM.items() if code.startswith(p)), code)


def to_num(series: pd.Series) -> pd.Series:
    """Parse LOVAC numbers: nbsp thousands separators, 's' (secret) -> NaN."""
    cleaned = series.astype("string").str.replace(r"[\s\xa0]", "", regex=True)
    return pd.to_numeric(cleaned.replace("s", pd.NA), errors="coerce")


# %% [markdown]
# ## 1. Zonage TLV (S-13) : la tension légale par commune

# %%
tlv = pd.read_csv(RAW / "zonage-tlv-decret-2025-12-22.csv", sep=";", dtype=str)
tlv = pd.DataFrame(
    {
        "code": tlv["CODGEO25"].str.strip().map(plm_parent),
        "zonage": tlv["Zonage TLV post décret 22/12/2025"].str.strip(),
    }
).drop_duplicates(subset="code", keep="first")
print(tlv["zonage"].value_counts().to_string())

# %% [markdown]
# ## 2. Recensement 2022 (S-11) : parc et vacance totale par commune → ZE

# %%
with zipfile.ZipFile(RAW / "insee-rp-base-cc-logement-2022.zip") as zf:
    with zf.open("base-cc-logement-2022.CSV") as fh:
        census = pd.read_csv(fh, sep=";", dtype=str, usecols=["CODGEO", "P22_LOG", "P22_LOGVAC"])
census = pd.DataFrame(
    {
        "code": census["CODGEO"].str.strip().map(plm_parent),
        "parc": pd.to_numeric(census["P22_LOG"], errors="coerce"),
        "vacants": pd.to_numeric(census["P22_LOGVAC"], errors="coerce"),
    }
).drop_duplicates(subset="code", keep="first")  # la base liste parents ET arrondissements

with zipfile.ZipFile(RAW / "insee-table-appartenance-geo-communes-2026.zip") as zf:
    with zf.open("table-appartenance-geo-communes-2026.xlsx") as fh:
        appartenance = pd.read_excel(fh, sheet_name="COM", header=5, engine="calamine", dtype=str)
com_ze = appartenance[["CODGEO", "ZE2020"]].dropna().rename(
    columns={"CODGEO": "code", "ZE2020": "ze"}
)

com = census.merge(tlv, on="code", how="left").merge(com_ze, on="code", how="left")
com["zonage"] = com["zonage"].fillna("3. Non tendue")
ze = com.dropna(subset=["ze"]).groupby("ze")[["parc", "vacants"]].sum()
for cat, col in [("1. Zone tendue", "parc_tlv1"), ("2. Zone touristique et tendue", "parc_tlv2")]:
    ze[col] = (
        com[com["zonage"] == cat].dropna(subset=["ze"]).groupby("ze")["parc"].sum()
    )
ze[["parc_tlv1", "parc_tlv2"]] = ze[["parc_tlv1", "parc_tlv2"]].fillna(0)
ze["part_tlv1_pct"] = ze["parc_tlv1"] / ze["parc"] * 100
ze["part_tlv_pct"] = (ze["parc_tlv1"] + ze["parc_tlv2"]) / ze["parc"] * 100
ze["taux_vacance_pct"] = ze["vacants"] / ze["parc"] * 100
print(f"{len(ze)} ZE ; taux de vacance totale (recensement 2022) : "
      f"min {ze['taux_vacance_pct'].min():.1f} %, médiane {ze['taux_vacance_pct'].median():.1f} %, "
      f"max {ze['taux_vacance_pct'].max():.1f} %")
print(f"part du parc national en communes TLV (1+2) : "
      f"{(ze['parc_tlv1'].sum() + ze['parc_tlv2'].sum()) / ze['parc'].sum() * 100:.1f} %")

# %% [markdown]
# ## 3. Vacance structurelle LOVAC (mill. 24) par ZE

# %%
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
struct_ze = (
    lovac.merge(com_ze, on="code", how="left")
    .dropna(subset=["ze"])
    .groupby("ze")[["structurelle"]]
    .sum(min_count=1)
)
ze = ze.join(struct_ze, how="left")
ze["vacants_disponibles"] = ze["vacants"] - ze["structurelle"]
ze["taux_disponible_pct"] = ze["vacants_disponibles"] / ze["parc"] * 100
print(f"vacance structurelle agrégée : {ze['structurelle'].sum():,.0f} logements ; "
      f"taux disponible médian {ze['taux_disponible_pct'].median():.1f} %")

# %% [markdown]
# ## 4. Qui est tendu ? Croisement lecture légale × lecture marché

# %%
names = pd.read_excel(
    RAW / "insee-emploi-zone-1998-2018.xlsx", sheet_name="Emploi total - ZE",
    header=4, engine="calamine",
)["Zone d'emploi"].astype("string").str.extract(r"^(\d{4}) - (.*)$").dropna()
ze = ze.join(names.set_index(0)[1].rename("ze_nom"), how="left")

t = H08_PCT / 100
ze["tendue_marche"] = ze["taux_vacance_pct"] < H08_PCT
ze["tendue_disponible"] = ze["taux_disponible_pct"] < H08_PCT
majoritaire_tlv = ze["part_tlv_pct"] > 50
print("croisement (nombre de ZE) :")
print(pd.crosstab(
    majoritaire_tlv.rename("parc majoritairement TLV"),
    ze["tendue_marche"].rename("vacance totale < 6 %"),
).to_string())
print()
print("ZE majoritairement TLV mais NON tendues au sens vacance totale < 6 % :")
odd = ze[majoritaire_tlv & ~ze["tendue_marche"]].nlargest(8, "parc")
print(odd[["ze_nom", "taux_vacance_pct", "taux_disponible_pct", "part_tlv_pct"]]
      .round(1).to_string())
print()
print("...dont tendues au sens vacance DISPONIBLE < 6 % : "
      f"{(odd['taux_disponible_pct'] < H08_PCT).sum()} sur {len(odd)}")

# %% [markdown]
# ## 5. Le manque absolu de logements pour la détente
#
# Construction : `N = (t·P − V)/(1 − t)` — variante disponible :
# `N_disp = (t·P − (V − S))/(1 − t)`. Mobilisation du gisement structurel
# (ne change pas le parc) : besoin `M = t·P − (V − S)`, couverture `S / M`.

# %%
tense = ze[ze["tendue_disponible"]].copy()
tense["manque_construction"] = (t * tense["parc"] - tense["vacants_disponibles"]) / (1 - t)
tense["besoin_mobilisation"] = t * tense["parc"] - tense["vacants_disponibles"]
tense["couverture_gisement"] = tense["structurelle"] / tense["besoin_mobilisation"]
cols = ["ze_nom", "parc", "taux_vacance_pct", "taux_disponible_pct",
        "structurelle", "besoin_mobilisation", "couverture_gisement"]
print(f"{len(tense)} ZE tendues (vacance disponible < {H08_PCT:.0f} %) — "
      f"parc cumulé {tense['parc'].sum() / 1e6:.1f} M logements")
print()
print("les 12 plus gros besoins absolus :")
print(tense.nlargest(12, "besoin_mobilisation")[cols].round(2).to_string())
print()
nat_besoin = tense["besoin_mobilisation"].sum()
nat_gisement = tense["structurelle"].sum()
print(f"BESOIN NATIONAL (ZE tendues) : {nat_besoin:,.0f} logements à rendre disponibles")
print(f"GISEMENT structurel dans CES MÊMES ZE : {nat_gisement:,.0f} "
      f"→ couverture {nat_gisement / nat_besoin:.2f}")
print()
suffisant = tense["couverture_gisement"] >= 1
print(f"ZE où le gisement local couvre le besoin : {suffisant.sum()} / {len(tense)} "
      f"(parc couvert {tense.loc[suffisant, 'parc'].sum() / 1e6:.1f} M ; "
      f"non couvert {tense.loc[~suffisant, 'parc'].sum() / 1e6:.1f} M)")
print()
print("les plus mal couvertes (couverture la plus basse, besoin > 1000) :")
worst = tense[tense["besoin_mobilisation"] > 1000].nsmallest(8, "couverture_gisement")
print(worst[cols].round(2).to_string())

# %% [markdown]
# ## 6. Sensibilité au seuil H-08 (plage 5-7 %)

# %%
for h in [H08_RANGE[0], H08_PCT, H08_RANGE[1]]:
    tt = h / 100
    sub = ze[ze["taux_disponible_pct"] < h].copy()
    besoin = (tt * sub["parc"] - sub["vacants_disponibles"]).sum()
    gisement = sub["structurelle"].sum()
    print(f"seuil {h:.0f} % : {len(sub)} ZE tendues, besoin {besoin:,.0f}, "
          f"gisement local {gisement:,.0f}, couverture {gisement / besoin:.2f}")

# %% [markdown]
# ## 7. Zoom communal : les communes TLV « 1. Zone tendue » visibles

# %%
zoom = (
    census.merge(tlv, on="code", how="inner")
    .query("zonage == '1. Zone tendue'")
    .merge(
        lovac.groupby("code", as_index=False).agg(structurelle=("structurelle", "sum")),
        on="code", how="left",
    )
)
zoom["taux_vacance_pct"] = zoom["vacants"] / zoom["parc"] * 100
zoom["vacants_disponibles"] = zoom["vacants"] - zoom["structurelle"]
zoom["taux_disponible_pct"] = zoom["vacants_disponibles"] / zoom["parc"] * 100
zoom["besoin_mobilisation"] = t * zoom["parc"] - zoom["vacants_disponibles"]
zoom["couverture"] = zoom["structurelle"] / zoom["besoin_mobilisation"]
big = zoom.nlargest(12, "parc")
libelles = pd.read_csv(RAW / "zonage-tlv-decret-2025-12-22.csv", sep=";", dtype=str)
libelles = libelles.assign(code=libelles["CODGEO25"].str.strip().map(plm_parent))
big = big.merge(libelles[["code", "LIBGEO"]].drop_duplicates("code"), on="code", how="left")
print("les 12 plus grosses communes en zone tendue légale :")
print(big[["LIBGEO", "parc", "taux_vacance_pct", "taux_disponible_pct",
           "structurelle", "besoin_mobilisation", "couverture"]].round(2).to_string())

# %%
fig, ax = plt.subplots(figsize=(9, 6))
sizes = (ze["parc"] / ze["parc"].max() * 600).clip(lower=8)
colors = ze["part_tlv_pct"].fillna(0)
sc = ax.scatter(ze["taux_disponible_pct"], ze["structurelle"].clip(lower=1), s=sizes,
                c=colors, cmap="coolwarm", alpha=0.55, edgecolors="white", linewidths=0.5)
ax.axvline(H08_PCT, color="#999999", ls="--", lw=1)
ax.annotate(f"seuil H-08 : {H08_PCT:.0f} %", (H08_PCT + 0.1, 2), fontsize=8, color="#555555")
ax.set_yscale("log")
for _, row in ze.nlargest(5, "structurelle").iterrows():
    ax.annotate(row["ze_nom"], (row["taux_disponible_pct"], row["structurelle"]),
                fontsize=7, color="#555555", xytext=(4, 2), textcoords="offset points")
ax.set_xlabel("taux de vacance disponible (totale − structurelle) (%)")
ax.set_ylabel("gisement structurel (logements, échelle log)")
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f %%"))
ax.set_title("Zones d'emploi : tension de marché × gisement mobilisable\n"
             "(recensement 2022, LOVAC mill. 24 ; couleur = part du parc en communes TLV)")
fig.colorbar(sc, ax=ax, label="part du parc en communes TLV (%)")
ax.grid(alpha=0.25)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Observations provisoires (vérifiées depuis les sorties ci-dessus)
#
# 1. **Le test « vacance totale < 6 % » échoue au contrôle de cohérence.**
#    La vacance totale du recensement est haute partout (médiane ZE
#    8,6 %) : aucune grande métropole TLV n'en sort « tendue » (Paris
#    7,7 %, Lyon 7,2 %, Marseille 7,1 %, Nice 10,2 %) alors qu'elles
#    cumulent zonage légal, loyers extrêmes et taux d'effort R-06
#    maximaux. En retranchant la vacance STRUCTURELLE (hors marché par
#    construction, D-10), 7 de ces 8 métropoles repassent sous le seuil :
#    la **vacance disponible** (totale − structurelle) est la mesure de
#    tension cohérente avec le zonage légal ET avec R-06. → décision à
#    confirmer avant stabilisation (modifie le choix « seuil sur vacance
#    totale » pris en début de session).
# 2. **En vacance disponible : 142 ZE tendues (23,8 M de logements de
#    parc).** Besoin absolu national pour la détente : **285 665
#    logements à rendre disponibles** ; gisement structurel dans ces
#    mêmes ZE : **472 022** → couverture **1,65**. La réponse à la
#    question est donc OUI à l'échelle nationale et dans 101 ZE sur 142
#    (17,3 M de parc) — mais NON dans 41 ZE (6,5 M de parc).
# 3. **Robuste au seuil H-08** : couverture 1,90 (seuil 5 %), 1,65 (6 %),
#    1,15 (7 %) — le gisement excède le besoin sur toute la plage.
# 4. **Les zones mal couvertes sont littorales/touristiques** (Les
#    Sables-d'Olonne 0,20, Pornic 0,27, Calvi 0,33, Challans, Le Mont
#    Blanc, Briançon, Royan, Fréjus ≤ 0,45) : là, le parc hors RP est en
#    résidences secondaires (R-05), pas en vacance — il n'y a presque
#    rien à remobiliser. La tension touristique (catégorie 2 TLV) ne se
#    résout pas par la vacance. À l'inverse, Paris (couverture 8,1),
#    Marseille (1,7), Lille (1,1), Montpellier (1,05) ont le gisement.
# 5. **Limites sérieuses du croisement (L-06)** : la vacance recensement
#    surestime l'offre réellement disponible dans les centres denses
#    (Paris commune : 9,8 % de vacance totale, 7,5 % « disponible » —
#    incompatible avec le marché observé) → le besoin est plutôt
#    SOUS-estimé dans les métropoles ; la secrétisation LOVAC ampute le
#    gisement (843 765 structurels visibles par communes vs ~1,15 M au
#    national) → couverture plutôt sous-estimée là où les communes sont
#    petites ; à Ajaccio la structurelle LOVAC excède les vacants
#    recensés (taux disponible −0,9 % : artefact de périmètres).
#
# Prochaine étape : confirmer le passage au test « vacance disponible »
# (correction tracée du choix de session), puis stabiliser R-07 +
# I-07 + C-06 + L-12.

# %%
