# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
# ---

# %% [markdown]
# # Exploration 13 — La mobilité du parc social (RPLS) par ZE
#
# **Régime exploratoire** (méthode Métabolisme §2.1). Deuxième instruction
# de **H-04 (mobilités empêchées)** : le parc social est le segment où la
# rotation est OFFERTE par un guichet (attributions) — sa chute nationale
# (9,3 % en 2019 → 7,1 % en 2025, chiffres-titres SDES) est le phénomène
# le plus documenté du gel des mobilités. Questions : la chute est-elle
# territorialement générale ? plus forte dans les marchés tendus ? le
# parc social et le parc total (R-11) gèlent-ils aux mêmes endroits ?
#
# Sources : **S-28** (RPLS au 01/01/2025, feuille COMMUNE — séries
# annuelles tx_mob/tx_vac 2013-2025, D-17), S-06 (communes → ZE),
# croisements tension R-07, coût R-04, rotation R-11 (S-27).
#
# Précautions (D-17) : mobilité du parc social ≠ mobilité du parc privé ≠
# rotation totale (D-16) ; un taux bas peut refléter le blocage des
# SORTIES (pas d'alternative abordable) autant que la stabilité choisie ;
# le fichier publie le RATIO par commune, pas ses termes — l'agrégation
# ZE est une moyenne pondérée approchée (convention contrôlée plus bas).

# %%
import sys
import zipfile
from pathlib import Path

import pandas as pd

ROOT = Path.cwd()
while not (ROOT / "pyproject.toml").exists():
    ROOT = ROOT.parent
RAW = ROOT / "data" / "raw"
sys.path.insert(0, str(ROOT / "src"))

from logement.core import lovac, mobilite, rs, stats, tension, ze  # noqa: E402
from logement.shell import build  # noqa: E402

pd.set_option("display.width", 160)

RPLS_ZIP = "sdes-rpls-2025-resultats-territoires.zip"
RPLS_XLSX = "statistiques_sdes_resultats_rpls_2025_secret_donnees.xlsx"

# %% [markdown]
# ## 1. Charger la feuille COMMUNE et contrôler la convention d'agrégation
#
# Le taux de mobilité est publié par commune (ratio, D-17) ; les
# numérateurs ne sont pas diffusés. Convention testée : moyenne pondérée
# par le parc social du MÊME millésime (`nb_ls`, `nb_ls2019`,
# `nb_ls2013` — colonnes sans valeur manquante), contrôlée contre les
# lignes « Total France entière » de la feuille REGION.

# %%
with zipfile.ZipFile(RAW / RPLS_ZIP) as zf, zf.open(RPLS_XLSX) as fh:
    com = pd.read_excel(
        fh, sheet_name="COMMUNE", engine="calamine", header=5, dtype={"DEPCOM_ARM": str}
    )
with zipfile.ZipFile(RAW / RPLS_ZIP) as zf, zf.open(RPLS_XLSX) as fh:
    reg = pd.read_excel(fh, sheet_name="REGION", engine="calamine", header=5)
fr = reg[reg.iloc[:, 1] == "Total France entière"].iloc[0]
print(
    f"{len(com)} communes ; PLM par arrondissement "
    f"(75056 présent : {(com['DEPCOM_ARM'] == '75056').any()})"
)

for label, rate_col, w_col, target in [
    ("2025", "tx_mob", "nb_ls", float(fr["tx_mob"])),
    ("2019", "tx_mob_2019", "nb_ls2019", float(fr["tx_mob_2019"])),
    ("2013", "tx_mob_2013", "nb_ls2013", float(fr["tx_mob_2013"])),
]:
    approx = (com[rate_col] * com[w_col]).sum() / com[w_col].sum()
    print(
        f"mobilité {label} : pondérée communes {approx:.3f} % vs "
        f"France entière (REGION) {target:.3f} % — écart {approx - target:+.3f} pt"
    )

# %% [markdown]
# ## 2. La série nationale : la chute et son calendrier

# %%
serie = pd.Series(
    {
        2013: float(fr["tx_mob_2013"]),
        2014: float(fr["tx_mob_2014"]),
        2015: float(fr["tx_mob_2015"]),
        2016: float(fr["tx_mob_2016"]),
        2017: float(fr["tx_mob_2017"]),
        2018: float(fr["tx_mob_2018"]),
        2019: float(fr["tx_mob_2019"]),
        2020: float(fr["tx_mob_2020"]),
        2021: float(fr["tx_mob_2021"]),
        2022: float(fr["tx_mob_2022"]),
        2023: float(fr["tx_mob_2023"]),
        2024: float(fr["tx_mob_2024"]),
        2025: float(fr["tx_mob"]),
    }
).round(2)
print(serie.to_string())
print(
    f"\nvacance sociale 2025 : {float(fr['tx_vac']):.2f} % "
    f"(dont > 3 mois {float(fr['tx_vac3']):.2f} %) ; parc {int(fr['nb_ls']):,} "
    f"logements sociaux".replace(",", " ")
)

# %% [markdown]
# ## 3. Agrégation par zone d'emploi (PLM → commune parente, S-06)

# %%
com["code"] = com["DEPCOM_ARM"].str.strip().map(lovac.plm_parent)
commune_ze = ze.parse_commune_ze(build._read_membership(ROOT))
merged = com.merge(commune_ze, on="code", how="left")
unmatched = merged.loc[merged["ze"].isna(), "code"].unique()
print(f"{len(unmatched)} communes RPLS sans ZE : {sorted(unmatched)[:8]}")
merged = merged.dropna(subset=["ze"])


def weighted_rate(frame: pd.DataFrame, rate: str, weight: str) -> pd.Series:
    num = (frame[rate] * frame[weight]).groupby(frame["ze"]).sum()
    den = frame.groupby("ze")[weight].sum()
    return num / den


social = pd.DataFrame(
    {
        "tx_mob_2025": weighted_rate(merged, "tx_mob", "nb_ls"),
        "tx_mob_2019": weighted_rate(merged, "tx_mob_2019", "nb_ls2019"),
        "tx_mob_2013": weighted_rate(merged, "tx_mob_2013", "nb_ls2013"),
        "tx_vac_2025": weighted_rate(merged, "tx_vac", "nb_ls"),
        "tx_vac3_2025": weighted_rate(merged, "tx_vac3", "nb_ls"),
        "parc_social": merged.groupby("ze")["nb_ls"].sum(),
    }
)
social["delta_2019_2025"] = social["tx_mob_2025"] - social["tx_mob_2019"]
social["delta_2013_2025"] = social["tx_mob_2025"] - social["tx_mob_2013"]
print(
    f"{len(social)} ZE ; parc social médian {social['parc_social'].median():,.0f} "
    f"logements (min {social['parc_social'].min():,.0f})".replace(",", " ")
)

# %% [markdown]
# Les ZE à parc social minuscule rendent le taux instable : on garde un
# seuil de parc ≥ 500 logements pour les classements et corrélations
# (seuil affiché, sensibilité vérifiable en le changeant ici).

# %%
SEUIL_PARC = 500
petit = social["parc_social"] < SEUIL_PARC
print(
    f"{int(petit.sum())} ZE sous {SEUIL_PARC} logements sociaux — écartées "
    f"des classements ({', '.join(sorted(social.index[petit])[:8])}…)"
)
soc = social[~petit].copy()
print(f"reste {len(soc)} ZE — mobilité 2025 :")
print(soc["tx_mob_2025"].describe().round(2).to_string())

# %%
names = build._ze_names(ROOT)
tbl = soc.join(names, how="left")
print(
    f"{int((soc['delta_2019_2025'] < 0).sum())} ZE sur {len(soc)} en baisse "
    "de mobilité sociale 2019->2025 "
    f"({int((soc['delta_2013_2025'] < 0).sum())} sur 2013->2025)"
)
print("\nmobilité 2025 la plus faible :")
print(
    tbl.nsmallest(10, "tx_mob_2025")[
        ["tx_mob_2025", "tx_mob_2019", "delta_2019_2025", "parc_social", "ze_name"]
    ]
    .round(2)
    .to_string()
)
print("\nmobilité 2025 la plus forte :")
print(
    tbl.nlargest(10, "tx_mob_2025")[
        ["tx_mob_2025", "tx_mob_2019", "delta_2019_2025", "parc_social", "ze_name"]
    ]
    .round(2)
    .to_string()
)
print("\nplus fortes baisses 2019->2025 :")
print(
    tbl.nsmallest(10, "delta_2019_2025")[
        ["tx_mob_2019", "tx_mob_2025", "delta_2019_2025", "ze_name"]
    ]
    .round(2)
    .to_string()
)

# %% [markdown]
# ## 4. Croisements : tension, coût, vacance privée, rotation totale (R-11)

# %%
with zipfile.ZipFile(RAW / build.CENSUS_ZIP) as zf, zf.open(build.CENSUS_CSV) as fh:
    census_raw = pd.read_csv(fh, sep=";", dtype=str, usecols=["CODGEO", *rs.CENSUS_COLS])
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
vacancy_ze, _ = ze.aggregate_vacancy_by_ze(communes, commune_ze)
cost = build._cost_frame(ROOT)

import pyarrow.parquet as pq  # noqa: E402

cut = pq.read_table(
    RAW / build.MOBILITE_FILE,
    columns=["GEO_OBJECT", "GEO", "TIME_PERIOD", "L_STAY", "OBS_VALUE"],
    filters=[
        ("GEO_OBJECT", "in", {"ZE2020", "FRANCE"}),
        ("RP_MEASURE", "=", "DWELLINGS"),
        ("OCS", "=", "DW_MAIN"),
        ("TDW", "=", "_T"),
        ("NRG_SRC", "=", "_T"),
        ("CARPARK", "=", "_T"),
        ("NOR", "=", "_T"),
        ("TSH", "=", "_T"),
        ("CARS", "=", "_T"),
        ("BUILD_END", "=", "_T"),
    ],
).to_pandas()
rotation = mobilite.rotation_by_ze(mobilite.rotation_parts(mobilite.parse_lstay(cut)))

cross = (
    soc.join(tension_frame["tendue"], how="left")
    .join(vacancy_ze["structural_rate_pct"], how="left")
    .join(cost["indice_cout_pct"], how="left")
    .join(
        rotation[["part_recents_pct", "delta_pts"]].rename(
            columns={"part_recents_pct": "rotation_rp_pct", "delta_pts": "delta_rotation_rp"}
        ),
        how="left",
    )
)
med = cross.groupby("tendue")[["tx_mob_2025", "delta_2019_2025", "tx_vac_2025"]].median().round(2)
print("médianes par statut de tension (R-07 central) :")
print(med.to_string())

# %%
for label, x, y in [
    ("mobilité sociale 2025 × indice de coût", "tx_mob_2025", "indice_cout_pct"),
    ("mobilité sociale 2025 × vacance structurelle privée", "tx_mob_2025", "structural_rate_pct"),
    ("mobilité sociale 2025 × rotation totale RP 2023 (R-11)", "tx_mob_2025", "rotation_rp_pct"),
    ("chute sociale 2019→2025 × chute rotation RP (R-11)", "delta_2019_2025", "delta_rotation_rp"),
    ("chute sociale 2019→2025 × indice de coût", "delta_2019_2025", "indice_cout_pct"),
    ("mobilité sociale 2025 × vacance sociale 2025", "tx_mob_2025", "tx_vac_2025"),
]:
    print(label, ":", stats.spearman_by_perimeter(cross, x, y))

# %% [markdown]
# ## 5. Constats (relus depuis les sorties, exécution du 2026-08-08)
#
# 1. **La chute nationale est quasi continue et s'accélère en fin de
#    période** : 9,87 % (2013) → 9,29 % (2019) → 7,11 % (2025). Érosion
#    lente avant COVID (−0,58 pt en 6 ans), choc 2021 (7,55), rebond
#    partiel 2022 (8,54), puis chute rapide : −1,43 pt sur 2022-2025.
#    Vacance sociale 2025 : 2,12 % (dont 1,05 % > 3 mois) — le parc
#    social est à la fois saturé et de moins en moins mobile.
# 2. **La chute est générale (286 ZE sur 303) et UNIFORME dans son
#    ampleur** : médiane −2,40 pt dans les ZE tendues vs −2,45 ailleurs ;
#    chute × coût rho +0,03 (IC95 [−0,09 ; +0,14], compatible avec zéro).
#    CONTRASTE avec R-11 : la chute de la rotation TOTALE se concentre
#    dans les marchés chers, la chute de la mobilité SOCIALE est
#    partout — la file d'attente s'allonge sur tout le territoire.
# 3. **Le NIVEAU, lui, est le miroir du marché** : mobilité sociale ×
#    indice de coût rho métropole **−0,80** (IC95 [−0,84 ; −0,76],
#    n = 285) — la corrélation la plus forte de toute la chaîne à ce
#    jour ; +0,48 avec la vacance structurelle privée. Médiane 6,74 %
#    en ZE tendues vs 8,88 ailleurs ; aux extrêmes : Porto-Vecchio
#    2,6 %, Sainte-Maxime 3,6, Menton 3,9, Nice 4,1, Roissy 4,3,
#    Marseille 4,7 (un logement social s'y libère environ une fois
#    tous les 20-25 ans) contre ~12-13 % dans le rural détendu (Mende,
#    Avallon, Argentan). La vacance sociale médiane en zone tendue est
#    de 1,63 % (2,79 ailleurs).
# 4. **Les deux segments divergent** : mobilité sociale × rotation
#    totale RP (R-11) rho métropole **−0,20** (IC95 [−0,31 ; −0,09]) —
#    NÉGATIF. Les métropoles chères cumulent rotation totale élevée
#    (étudiants, parc privé) et parc social gelé : le gel social est
#    plus profond que ce que la rotation d'ensemble laisse voir. Les
#    chutes, elles, sont faiblement co-localisées (+0,19
#    [+0,07 ; +0,30]).
#
# Limites à porter avec ces constats :
#
# - Agrégation par ratio publié (D-17) : moyenne pondérée par le parc
#   du millésime, CONTRÔLÉE au national (écarts ≤ 0,01 pt aux trois
#   millésimes testés) mais approchée par construction.
# - Petits parcs volatils : les plus fortes « chutes » (Issoire
#   −13,2 pt) sont des petits parcs ruraux ; le seuil de 500 logements
#   écarte les cas extrêmes, les médianes restent l'indicateur robuste.
# - Un taux bas ne sépare pas blocage des sorties et stabilité choisie
#   (D-17) ; les mutations internes et le neuf sont hors numérateur.
# - Périmètre France entière AVEC Mayotte (ZE 0601, sans nom dans
#   S-07) — contrairement à S-27 (hors Mayotte) ; le masque DOM de
#   `core/stats` a été étendu (01-04 + 06) pour que le périmètre
#   métropole reste honnête.
