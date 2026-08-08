# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
# ---

# %% [markdown]
# # Exploration 15 — Le coût de transaction : la barrière à la mobilité
# # de statut
#
# **Régime exploratoire** (méthode Métabolisme §2.1). Quatrième
# instruction de **H-04 (mobilités empêchées)** : R-13 montre que la
# mobilité passe par le locatif privé (19,5 % d'entrées annuelles) et
# presque pas par la propriété (5,7 %) — une des raisons candidates est
# le COÛT DE TRANSACTION : à chaque achat, droits de mutation (H-13) et
# émoluments s'ajoutent au prix. Question : combien de mois de revenu
# médian ce péage représente-t-il, ZE par ZE ?
#
# Sources : **S-30** (DVF géolocalisées, mutations 2025 complètes),
# **S-31** (taux DMTO par département au 01/02/2026, base de H-13),
# **S-32** (barème des émoluments, calcul exact), S-10 (revenus
# Filosofi), S-06 (communes → ZE).
#
# Précautions : DVF hors Alsace-Moselle et Mayotte ; une mutation =
# plusieurs lignes (convention de filtrage C-10 à poser ici) ; le coût
# calculé est un PLANCHER (ni débours, ni CSI, ni agence, S-32).

# %%
import sys
from pathlib import Path

import pandas as pd

ROOT = Path.cwd()
while not (ROOT / "pyproject.toml").exists():
    ROOT = ROOT.parent
RAW = ROOT / "data" / "raw"
sys.path.insert(0, str(ROOT / "src"))

from logement.core import cout, lovac, stats, tension, ze  # noqa: E402
from logement.shell import build  # noqa: E402

pd.set_option("display.width", 160)

# %% [markdown]
# ## 1. Filtrer les ventes de logements (convention C-10)
#
# Une mutation DVF porte plusieurs lignes (locaux, dépendances,
# parcelles) qui partagent la même `valeur_fonciere`. Convention
# proposée : ventes (`nature_mutation == "Vente"`) portant EXACTEMENT UN
# local d'habitation (une Maison ou un Appartement), sans local
# commercial/industriel dans la mutation (les dépendances sont
# admises) ; bornes de plausibilité : valeur ≥ 5 000 €, surface ≥ 10 m²,
# prix/m² entre 200 et 30 000 €.

# %%
COLS = [
    "id_mutation",
    "nature_mutation",
    "valeur_fonciere",
    "code_commune",
    "type_local",
    "surface_reelle_bati",
]
raw = pd.read_csv(RAW / "dvf-geolocalisees-2025.csv.gz", usecols=COLS, dtype={"code_commune": str})
ventes = raw[raw["nature_mutation"] == "Vente"].copy()
print(f"{len(raw):,} lignes, {len(ventes):,} lignes de vente".replace(",", " "))

is_dwelling = ventes["type_local"].isin(["Maison", "Appartement"])
is_commercial = ventes["type_local"] == "Local industriel. commercial ou assimilé"
per_mut = ventes.groupby("id_mutation").agg(
    n_logements=("type_local", lambda s: s.isin(["Maison", "Appartement"]).sum()),
    n_commerciaux=("type_local", lambda s: (s == "Local industriel. commercial ou assimilé").sum()),
)
keep_ids = per_mut[(per_mut["n_logements"] == 1) & (per_mut["n_commerciaux"] == 0)].index
sales = ventes[is_dwelling & ventes["id_mutation"].isin(keep_ids)].copy()
sales["valeur"] = pd.to_numeric(sales["valeur_fonciere"], errors="coerce")
sales["surface"] = pd.to_numeric(sales["surface_reelle_bati"], errors="coerce")
sales["prix_m2"] = sales["valeur"] / sales["surface"]
n0 = len(sales)
sales = sales[
    (sales["valeur"] >= 5_000) & (sales["surface"] >= 10) & sales["prix_m2"].between(200, 30_000)
]
print(
    f"mutations à un seul logement : {len(keep_ids):,} ; lignes retenues {n0:,} ; "
    f"après bornes de plausibilité {len(sales):,}".replace(",", " ")
)
print(sales.groupby("type_local")["valeur"].median().round(0).to_string())
print(
    f"prix médian France (ventes retenues) : {sales['valeur'].median():,.0f} € ; "
    f"prix/m² médian {sales['prix_m2'].median():,.0f} €".replace(",", " ")
)

# %% [markdown]
# ## 2. Prix médians par zone d'emploi

# %%
sales["code"] = sales["code_commune"].str.zfill(5).map(lovac.plm_parent)
commune_ze = ze.parse_commune_ze(build._read_membership(ROOT))
ze_of = commune_ze.set_index("code")["ze"]
sales["ze"] = sales["code"].map(ze_of)
print(f"ventes sans ZE : {sales['ze'].isna().sum():,}".replace(",", " "))
sales = sales.dropna(subset=["ze"])

prix = sales.groupby("ze").agg(
    prix_median=("valeur", "median"),
    prix_m2_median=("prix_m2", "median"),
    n_ventes=("valeur", "size"),
)
print(
    f"{len(prix)} ZE ; ventes médianes par ZE {prix['n_ventes'].median():,.0f} "
    f"(min {prix['n_ventes'].min()})".replace(",", " ")
)
print(prix["prix_median"].describe().round(0).to_string())

# %% [markdown]
# ## 3. Coût de transaction (H-13 + barème S-32) en mois de niveau de vie
#
# Émoluments proportionnels (S-32, TTC à 20 % de TVA) calculés
# exactement ; droits H-13 au taux central 6,32 % (plage 5,09-6,32).
# Unité conforme à C-04 (aucun ménage type) : MOIS DE NIVEAU DE VIE
# MÉDIAN PAR UC (MED_SL/12, Filosofi S-10) — pour un ménage d'une UC
# c'est un mois de revenu disponible ; un ménage de 1,5 UC divise par
# 1,5.

# %%
BAREME = [
    (0, 6_500, 0.03870),
    (6_500, 17_000, 0.01596),
    (17_000, 60_000, 0.01064),
    (60_000, float("inf"), 0.00799),
]
TVA = 1.20


def emoluments_ttc(prix_eur: float) -> float:
    hors_tva = sum((min(prix_eur, hi) - lo) * taux for lo, hi, taux in BAREME if prix_eur > lo)
    return hors_tva * TVA


h13 = build._load_hypothesis(ROOT, "H-13")
import zipfile  # noqa: E402

with zipfile.ZipFile(RAW / build.FILOSOFI_ZIP) as zf, zf.open(build.FILOSOFI_CSV) as fh:
    filosofi = pd.read_csv(
        fh, sep=";", dtype=str, usecols=["GEO", "GEO_OBJECT", "FILOSOFI_MEASURE", "OBS_VALUE"]
    )
niveau_vie = cout.parse_filosofi(filosofi, geo_object="ZE2020", measure="MED_SL")
frame = prix.join(niveau_vie.rename("niveau_vie_median"), how="left")
for label, taux in [
    ("bas", h13.plausible_range[0]),
    ("central", h13.central_value),
    ("haut", h13.plausible_range[1]),
]:
    frame[f"cout_transaction_{label}"] = frame["prix_median"] * taux / 100 + frame[
        "prix_median"
    ].map(emoluments_ttc)
frame["cout_en_mois_niveau_vie"] = frame["cout_transaction_central"] / (
    frame["niveau_vie_median"] / 12
)
frame["cout_pct_prix"] = frame["cout_transaction_central"] / frame["prix_median"] * 100
print(frame[["cout_en_mois_niveau_vie", "cout_pct_prix"]].describe().round(2).to_string())

# %%
names = build._ze_names(ROOT)
tbl = frame.join(names, how="left")
print("péage le plus lourd (mois de niveau de vie médian par UC) :")
print(
    tbl.nlargest(10, "cout_en_mois_niveau_vie")[
        [
            "prix_median",
            "cout_transaction_central",
            "niveau_vie_median",
            "cout_en_mois_niveau_vie",
            "ze_name",
        ]
    ]
    .round(0)
    .to_string()
)
print("\nle plus léger :")
print(
    tbl.nsmallest(8, "cout_en_mois_niveau_vie")[
        ["prix_median", "cout_transaction_central", "cout_en_mois_niveau_vie", "ze_name"]
    ]
    .round(1)
    .to_string()
)

# %% [markdown]
# ## 4. Croisements : tension et coût locatif

# %%
with zipfile.ZipFile(RAW / build.CENSUS_ZIP) as zf, zf.open(build.CENSUS_CSV) as fh:
    census_raw = pd.read_csv(
        fh,
        sep=";",
        dtype=str,
        usecols=["CODGEO", *__import__("logement.core.rs", fromlist=["rs"]).CENSUS_COLS],
    )
from logement.core import rs  # noqa: E402

census = rs.parse_census_housing(census_raw)
tlv = tension.parse_tlv(pd.read_csv(RAW / build.TLV_FILE, sep=";", dtype=str))
communes = lovac.parse_territories(
    pd.read_csv(RAW / build.LOVAC_COMMUNES, sep=";", encoding="cp1252", dtype=str),
    code_col="CODGEO_26",
    name_col="LIBGEO_26",
)
h08 = build._load_hypothesis(ROOT, "H-08")
h12 = build._load_hypothesis(ROOT, "H-12")
tension_frame = tension.tension_by_ze(
    census, tlv, communes, commune_ze, h08.central_value, h12.central_value
)
cross = frame.join(tension_frame["tendue"], how="left").join(
    build._cost_frame(ROOT)["indice_cout_pct"], how="left"
)
print("médianes par statut de tension :")
print(
    cross.groupby("tendue")[["cout_en_mois_niveau_vie", "prix_median"]]
    .median()
    .round(1)
    .to_string()
)
for label, x, y in [
    (
        "coût de transaction (mois) × indice de coût locatif",
        "cout_en_mois_niveau_vie",
        "indice_cout_pct",
    ),
    ("prix médian × indice de coût locatif", "prix_median", "indice_cout_pct"),
]:
    print(label, ":", stats.spearman_by_perimeter(cross, x, y))

# %% [markdown]
# ## 5. Constats (relus depuis les sorties, exécution du 2026-08-08)
#
# 1. **L'assiette est posée** (convention C-10) : sur 3 514 036 lignes
#    de vente 2025, 733 529 mutations portent exactement un logement
#    (sans local commercial), 727 209 restent après bornes de
#    plausibilité. Prix médian France : 182 000 € (maison 200 000,
#    appartement 166 000), 2 658 €/m². 296 ZE couvertes (les 9 ZE
#    d'Alsace-Moselle sont hors DVF), 1 380 ventes médianes par ZE
#    (min 22 — prudence sur les petites ZE).
# 2. **Le taux du péage est quasi uniforme, son poids ne l'est pas** :
#    droits H-13 (6,32 % central) + émoluments exacts (S-32) = 7,43 à
#    8,02 % du prix selon la ZE (médiane 7,60 % — la part émoluments
#    décroît avec le prix). Exprimé en pouvoir d'achat local (mois de
#    niveau de vie médian par UC, C-04) : **médiane 6,1 mois**, de
#    2,8 mois (Sarrebourg, Montluçon 2,9, Guéret 3,2) à 13,2 mois
#    (L'Ouest réunionnais, Porto-Vecchio 13,0), 11 mois à Paris,
#    Bayonne, La Teste-de-Buch et dans le Sud réunionnais.
# 3. **Le péage est le plus lourd là où la mobilité est déjà la plus
#    entravée** : médiane 7,8 mois dans les ZE tendues (R-07 central)
#    contre 5,5 ailleurs ; corrélation avec l'indice de coût locatif
#    rho métropole +0,81 (IC95 [+0,77 ; +0,85], n = 278). Acheter pour
#    se loger dans une zone tendue commence par plus d'une demi-année de
#    niveau de vie en pur péage non récupérable — cohérent avec R-13 : la
#    propriété est le statut qui bouge le moins (5,7 % d'entrées par
#    an) et le locatif privé porte la mobilité.
#
# Limites à porter :
#
# - Le coût est un PLANCHER : ni débours, ni contribution de sécurité
#   immobilière, ni frais d'agence (S-32 ne les chiffre pas) ; H-13 est
#   hors primo-accédants (qui gardent 4,50 % départemental).
# - H-13 central applique le taux MAJORITAIRE (6,32 %) à toutes les ZE :
#   une dizaine de départements sont à 5,81 % et l'Indre à 5,09 % — la
#   variation est dans la plage publiée, pas territorialisée (le fichier
#   S-31 le permettrait ; à faire si un résultat en dépend).
# - Prix médian des VENTES 2025 ≠ prix du logement médian du parc (les
#   biens qui se vendent ne sont pas un échantillon aléatoire du parc).
# - 8 ZE sans niveau de vie Filosofi (n = 288 pour les mois de revenu) ;
#   Alsace-Moselle hors champ (livre foncier).
