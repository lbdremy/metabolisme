# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
# ---

# %% [markdown]
# # Exploration 14 — Les migrations résidentielles des personnes (MIGCOM)
#
# **Régime exploratoire** (méthode Métabolisme §2.1). Troisième
# instruction de **H-04 (mobilités empêchées)** : R-11 et R-12 mesurent
# des LOGEMENTS (rotation du parc, emménagements dans le parc social) —
# le fichier détail MIGCOM mesure les PERSONNES (D-18 : logement
# différent de celui du 1er janvier de l'année précédente). Questions :
# quel taux annuel de mobilité des personnes par ZE ? qui porte la
# mobilité selon le statut d'occupation (le pont avec R-12) ? les flux
# entre ZE vident-ils ou remplissent-ils les zones tendues ?
#
# Sources : **S-29** (MIGCOM RP2022, 17,36 M obs. pondérées IPONDI,
# D-18), S-06 (communes → ZE), croisements tension R-07, coût R-04,
# rotation R-11.
#
# Précautions (D-18) : caractéristiques à la date d'ENQUÊTE (le statut
# d'un mobile est son statut d'ARRIVÉE) ; millésime 2022 = enquêtes
# 2020-2024 (fenêtres annuelles successives, dont COVID) ; IRAN = 0
# (rattachement) exclu des deux termes ; effectifs < 200 imprécis.

# %%
import sys
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

ROOT = Path.cwd()
while not (ROOT / "pyproject.toml").exists():
    ROOT = ROOT.parent
RAW = ROOT / "data" / "raw"
sys.path.insert(0, str(ROOT / "src"))

from logement.core import lovac, mobilite, rs, stats, tension, ze  # noqa: E402
from logement.shell import build  # noqa: E402

pd.set_option("display.width", 160)

# %% [markdown]
# ## 1. Charger la coupe utile et poser la mesure nationale

# %%
cut = pq.read_table(
    RAW / "insee-rp2022-migcom.parquet",
    columns=["COMMUNE", "DCRAN", "IRAN", "IPONDI", "STOCD"],
).to_pandas()
for col in ("COMMUNE", "DCRAN", "IRAN", "STOCD"):
    cut[col] = cut[col].astype("string")
print(f"{len(cut):,} observations ; poids total {cut['IPONDI'].sum() / 1e6:.2f} M".replace(",", " "))

rattachement = cut["IRAN"] == "0"
print(f"IRAN=0 (rattachement) : {cut.loc[rattachement, 'IPONDI'].sum():,.0f} personnes exclues".replace(",", " "))
base = cut[~rattachement].copy()
base["mobile"] = base["IRAN"] != "1"

pop = base["IPONDI"].sum()
mobiles = base.loc[base["mobile"], "IPONDI"].sum()
print(f"population ≥ 1 an (hors rattachement) : {pop / 1e6:.2f} M")
print(f"mobiles (logement différent il y a un an) : {mobiles / 1e6:.2f} M "
      f"soit {mobiles / pop * 100:.2f} %")
for label, codes in [
    ("autre logement, même commune", ["2"]),
    ("autre commune de France", ["3", "4", "5", "6", "7"]),
    ("depuis l'étranger", ["8", "9"]),
]:
    w = base.loc[base["IRAN"].isin(codes), "IPONDI"].sum()
    print(f"  dont {label} : {w / 1e6:.2f} M ({w / pop * 100:.2f} %)")

# %% [markdown]
# ## 2. Qui porte la mobilité ? Statut d'occupation à l'arrivée (pont R-12)
#
# STOCD est le statut à la date d'enquête : pour un mobile, c'est le
# statut du logement d'ARRIVÉE. La part de mobiles parmi les occupants
# d'un statut est donc le taux d'entrées récentes dans ce segment.

# %%
STATUTS = {
    "10": "propriétaire",
    "21": "locataire privé (vide)",
    "22": "locataire HLM",
    "23": "locataire meublé/hôtel",
    "30": "logé gratuitement",
}
seg = base[base["STOCD"] != "ZZ"].copy()
seg["statut"] = seg["STOCD"].map(STATUTS)
tab = seg.groupby("statut").apply(
    lambda g: pd.Series(
        {
            "personnes_M": g["IPONDI"].sum() / 1e6,
            "part_mobiles_pct": g.loc[g["mobile"], "IPONDI"].sum() / g["IPONDI"].sum() * 100,
        }
    ),
    include_groups=False,
)
print(tab.round(2).sort_values("part_mobiles_pct", ascending=False).to_string())

# %% [markdown]
# ## 3. Par zone d'emploi : taux de mobilité des personnes, flux entre ZE

# %%
commune_ze = ze.parse_commune_ze(build._read_membership(ROOT))
ze_of = commune_ze.set_index("code")["ze"]
base["ze"] = base["COMMUNE"].map(ze_of)
print(f"communes sans ZE : {base.loc[base['ze'].isna(), 'COMMUNE'].nunique()} "
      f"(poids {base.loc[base['ze'].isna(), 'IPONDI'].sum():,.0f})".replace(",", " "))
base = base.dropna(subset=["ze"])

per_ze = base.groupby("ze")["IPONDI"].sum().rename("population")
mob_ze = base[base["mobile"]].groupby("ze")["IPONDI"].sum().rename("mobiles")
frame = pd.concat([per_ze, mob_ze], axis=1)
frame["taux_mobilite_pct"] = frame["mobiles"] / frame["population"] * 100

# flux entre ZE : mobiles venant d'une autre commune de France
movers = base[base["IRAN"].isin(["3", "4", "5", "6", "7"])].copy()
movers["ze_origine"] = movers["DCRAN"].map(lovac.plm_parent).map(ze_of)
print(f"mobiles inter-communes sans ZE d'origine : "
      f"{movers.loc[movers['ze_origine'].isna(), 'IPONDI'].sum():,.0f}".replace(",", " "))
inter = movers.dropna(subset=["ze_origine"])
inter = inter[inter["ze_origine"] != inter["ze"]]
frame["entrants"] = inter.groupby("ze")["IPONDI"].sum()
frame["sortants"] = inter.groupby("ze_origine")["IPONDI"].sum()
frame[["entrants", "sortants"]] = frame[["entrants", "sortants"]].fillna(0.0)
frame["solde"] = frame["entrants"] - frame["sortants"]
frame["solde_pct_pop"] = frame["solde"] / frame["population"] * 100
frame["taux_entree_pct"] = frame["entrants"] / frame["population"] * 100

print(f"\n{len(frame)} ZE — taux de mobilité annuel des personnes :")
print(frame["taux_mobilite_pct"].describe().round(2).to_string())
print(f"\nflux inter-ZE totaux : {inter['IPONDI'].sum() / 1e6:.2f} M de personnes")

# %%
names = build._ze_names(ROOT)
tbl = frame.join(names, how="left")
print("mobilité des personnes la plus faible :")
print(tbl.nsmallest(8, "taux_mobilite_pct")[["taux_mobilite_pct", "solde_pct_pop", "ze_name"]].round(2).to_string())
print("\nla plus forte :")
print(tbl.nlargest(8, "taux_mobilite_pct")[["taux_mobilite_pct", "solde_pct_pop", "ze_name"]].round(2).to_string())
print("\nsoldes migratoires inter-ZE les plus négatifs (en % de la population) :")
print(tbl.nsmallest(8, "solde_pct_pop")[["taux_mobilite_pct", "entrants", "sortants", "solde_pct_pop", "ze_name"]].round(2).to_string())
print("\nles plus positifs :")
print(tbl.nlargest(8, "solde_pct_pop")[["taux_mobilite_pct", "entrants", "sortants", "solde_pct_pop", "ze_name"]].round(2).to_string())

# %% [markdown]
# ## 4. Croisements : tension, coût, rotation des logements (R-11)

# %%
import zipfile  # noqa: E402

with zipfile.ZipFile(RAW / build.CENSUS_ZIP) as zf, zf.open(build.CENSUS_CSV) as fh:
    census_raw = pd.read_csv(fh, sep=";", dtype=str, usecols=["CODGEO", *rs.CENSUS_COLS])
census = rs.parse_census_housing(census_raw)
tlv = tension.parse_tlv(pd.read_csv(RAW / build.TLV_FILE, sep=";", dtype=str))
communes = lovac.parse_territories(
    pd.read_csv(RAW / build.LOVAC_COMMUNES, sep=";", encoding="cp1252", dtype=str),
    code_col="CODGEO_26", name_col="LIBGEO_26",
)
h08 = build._load_hypothesis(ROOT, "H-08")
h12 = build._load_hypothesis(ROOT, "H-12")
tension_frame = tension.tension_by_ze(census, tlv, communes, commune_ze,
                                      h08.central_value, h12.central_value)
cost = build._cost_frame(ROOT)
rotation = mobilite.rotation_by_ze(build._lstay_parts(ROOT))

cross = (
    frame.join(tension_frame["tendue"], how="left")
    .join(cost["indice_cout_pct"], how="left")
    .join(rotation["part_recents_pct"].rename("rotation_rp_pct"), how="left")
)
med = cross.groupby("tendue")[["taux_mobilite_pct", "solde_pct_pop", "taux_entree_pct"]].median().round(2)
print("médianes par statut de tension (R-07 central) :")
print(med.to_string())

# %%
for label, x, y in [
    ("mobilité des personnes × rotation des logements (R-11)", "taux_mobilite_pct", "rotation_rp_pct"),
    ("mobilité des personnes × indice de coût", "taux_mobilite_pct", "indice_cout_pct"),
    ("solde inter-ZE × indice de coût", "solde_pct_pop", "indice_cout_pct"),
    ("taux d'entrée × indice de coût", "taux_entree_pct", "indice_cout_pct"),
]:
    print(label, ":", stats.spearman_by_perimeter(cross, x, y))

# %% [markdown]
# ## 5. Constats (relus depuis les sorties, exécution du 2026-08-08)
#
# 1. **La mesure des personnes est posée** : 9,87 % des personnes (≥ 1 an,
#    hors rattachement) résident dans un logement différent de celui
#    d'il y a un an — 3,18 % dans la même commune, 6,25 % depuis une
#    autre commune de France, 0,44 % depuis l'étranger. Par ZE :
#    médiane 9,42 %, minimum aux Antilles (Nord-Atlantique 3,51 %),
#    maximum dans les ZE étudiantes (Rennes 12,82, Toulouse 12,80,
#    Montpellier 12,66).
# 2. **La mobilité est portée par le locatif privé** — la part de
#    mobiles (= entrés dans l'année) parmi les occupants actuels :
#    meublé/hôtel 32,98 %, **locatif privé vide 19,51 %**, logé
#    gratuitement 13,38 %, **HLM 8,34 %**, propriétaire 5,73 %. Le
#    segment privé tourne 2,3 × plus vite que le parc social et 3,4 ×
#    plus vite que la propriété occupante. Le 8,34 % HLM recoupe le taux
#    de mobilité RPLS des millésimes couverts par les enquêtes 2020-2024
#    (8,5 % en 2022, 8,0 % en 2023, R-12) : VALIDATION EXTERNE de R-12
#    par une source indépendante.
# 3. **Validation croisée logements/personnes** : mobilité des personnes
#    (MIGCOM 2022) × rotation des logements (S-27, R-11) rho métropole
#    **+0,80** (IC95 [+0,76 ; +0,84], n = 287) — deux sources et deux
#    unités différentes racontent la même géographie de la rotation.
# 4. **Les flux internes vident les cœurs chers** : 2,09 M de personnes
#    changent de ZE dans l'année ; les soldes les plus négatifs (en % de
#    population) sont Paris (**−1,40 %/an** : 133 371 entrants pour
#    225 906 sortants), Roissy (−1,11), Evry (−0,96) — les plus positifs
#    le littoral et l'ouest (Les Sables-d'Olonne +1,91, Brignoles +1,81,
#    La Rochelle +1,43, Dinan +1,41). Solde × coût rho France entière
#    −0,15 (IC95 [−0,26 ; −0,04] ; métropole −0,11 [−0,22 ; +0,01],
#    borderline) : les zones chères perdent en net aux migrations
#    INTERNES — le déficit parisien est compensé hors de cette mesure
#    (étranger, naissances).
# 5. **Le niveau de mobilité annuelle ne montre PAS de gel spécifique
#    aux zones tendues** (médianes 9,5 vs 9,4 ; taux d'entrée × coût
#    ≈ 0) : sur une fenêtre d'UN an dominée par les flux étudiants et
#    jeunes actifs vers les métropoles, le blocage se voit dans QUI
#    bouge (constat 2) et dans les SOLDES (constat 4), pas dans le
#    volume brut — cohérent avec R-11 où le gel apparaît dans la
#    dynamique 2012→2023, pas dans le niveau.
#
# Limites à porter :
#
# - Statut d'occupation mesuré à l'ARRIVÉE (D-18) : le « taux de
#   mobilité des locataires privés » est un taux d'entrées dans le
#   segment, pas la propension à partir des locataires en place.
# - Millésime 2022 = enquêtes 2020-2024 (fenêtres annuelles moyennées,
#   dont COVID).
# - Soldes = migrations INTERNES seulement (l'étranger, IRAN 8-9, est
#   dans le taux de mobilité mais pas dans les flux origine-destination).
# - 67 communes de résidence sans ZE (poids 79 331 — écarts de COG
#   2022/2026) et 11 406 mobiles sans ZE d'origine : exclus, publiés.
