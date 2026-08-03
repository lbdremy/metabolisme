# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
# ---

# %% [markdown]
# # Exploration 02 — Vacance territoriale (LOVAC)
#
# **Régime exploratoire** (méthode Métabolisme §2.1). Premier regard sur la
# vacance du parc privé par territoire et par durée, avec les données LOVAC
# figées (S-05). Questions du cadrage visées (`INTRO.md` §15) : où se trouve
# la vacance durable ? quelle part semble structurelle ?
#
# Cadre déjà arrêté :
#
# - **D-10** vacance structurelle = plus de 2 ans (`pp_vacant_plus_2ans`) ;
#   **D-11** vacance frictionnelle = le reste ; seuil paramétré **H-06**
#   (2 ans, plage 1-3) par le choix **C-01**.
# - **Précautions S-05** : parc privé uniquement (≠ vacance INSEE/EAPL) ;
#   secrétisation (« s » si < 11 logements vacants dans la commune) ;
#   **ruptures méthodologiques 2023** (taxe d'habitation → GMBI) **et 2025**
#   (données avant chaîne de traitement fiscale) — les niveaux ne sont pas
#   comparables d'un millésime à l'autre autour de ces ruptures.
# - Convention de lecture : le millésime N décrit la situation fiscale au
#   1er janvier N-1 (ex. millésime 26 = 01/01/2025).

# %%
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

ROOT = Path.cwd()
while not (ROOT / "pyproject.toml").exists():
    ROOT = ROOT.parent
RAW = ROOT / "data" / "raw"

C1, C2, C3, C4 = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"  # palette validée (dataviz)


def read_lovac(name: str) -> pd.DataFrame:
    """Read a LOVAC csv: cp1252, ';' separator, padded headers."""
    df = pd.read_csv(RAW / name, sep=";", encoding="cp1252", dtype=str)
    df.columns = [c.strip() for c in df.columns]
    return df


def to_num(series: pd.Series) -> pd.Series:
    """Parse LOVAC numbers: nbsp thousands separators, 's' (secret) -> NaN."""
    cleaned = series.astype("string").str.replace(r"[\s\xa0]", "", regex=True)
    return pd.to_numeric(cleaned.replace("s", pd.NA), errors="coerce")


MILLESIMES = [20, 21, 22, 23, 24, 25, 26]

# %% [markdown]
# ## 1. Niveau France : la série et ses ruptures
#
# La série nationale illustre pourquoi les niveaux ne se comparent pas entre
# millésimes : la vacance totale du parc privé chute de 3,69 M (mill. 24) à
# 2,38 M (mill. 25) puis remonte à 3,16 M (mill. 26) — un artefact des
# changements de chaîne fiscale, pas un phénomène de logement. La vacance
# structurelle (> 2 ans) est nettement moins affectée.

# %%
france = read_lovac("lovac-opendata-france26.csv")
france_series = pd.DataFrame(
    {
        "millésime": [int(m) for m in france["Millésime"]],
        "pp_vacant": to_num(france["pp_vacant"]),
        "pp_vacant_plus_2ans": to_num(france["pp_vacant_plus_2ans"]),
        "ff_pp_total": to_num(france["ff_pp_total"]),
    }
).set_index("millésime").sort_index()
france_series

# %%
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(
    france_series.index,
    france_series["pp_vacant"] / 1e6,
    color=C1,
    lw=2,
    marker="o",
    label="Vacants du parc privé",
)
ax.plot(
    france_series.index,
    france_series["pp_vacant_plus_2ans"] / 1e6,
    color=C2,
    lw=2,
    marker="o",
    label="Vacants depuis plus de 2 ans (structurelle, D-10)",
)
for rupture, note in ((23, "rupture 2023\n(TH → GMBI)"), (25, "rupture 2025\n(chaîne fiscale)")):
    ax.axvline(rupture - 0.5, color="#999999", ls="--", lw=1)
    ax.annotate(note, (rupture - 0.45, ax.get_ylim()[1] * 0.92), fontsize=8, color="#555555")
ax.set_title("Vacance du parc privé, France — millésimes LOVAC 2020-2026\n(millésime N = situation au 01/01/N-1 ; niveaux non comparables entre ruptures)")
ax.set_ylabel("millions de logements")
ax.set_xlabel("millésime LOVAC")
ax.grid(alpha=0.25)
ax.legend(frameon=False)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 2. Départements : où la vacance structurelle pèse-t-elle le plus ?
#
# Pour un taux cohérent (numérateur et dénominateur du même millésime), on
# utilise le **millésime 24** (situation au 01/01/2023) : dernier millésime
# complet avant la rupture 2025. Taux = vacance structurelle / parc privé.

# %%
deps = read_lovac("lovac-opendata-departements26.csv")
dep = pd.DataFrame(
    {
        "dep": deps["DEP"].str.strip(),
        "nom": deps["LIB_DEP"].str.strip(),
        "parc_prive_24": to_num(deps["ff_pp_total_24"]),
        "structurelle_24": to_num(deps["pp_vacant_plus_2ans_24"]),
        "structurelle_26": to_num(deps["pp_vacant_plus_2ans_26"]),
    }
)
dep["taux_structurelle_24"] = dep["structurelle_24"] / dep["parc_prive_24"] * 100
dep = dep.sort_values("taux_structurelle_24", ascending=False)
print(f"{len(dep)} départements ; taux structurel France (mill. 24) : "
      f"{dep['structurelle_24'].sum() / dep['parc_prive_24'].sum() * 100:.1f} %")
dep.head(12)[["dep", "nom", "taux_structurelle_24", "structurelle_24"]]

# %%
top = dep.head(12).iloc[::-1]
bottom = dep.tail(5).iloc[::-1]
fig, ax = plt.subplots(figsize=(9, 6))
ax.barh(top["nom"], top["taux_structurelle_24"], color=C2, height=0.6, label="12 taux les plus élevés")
ax.barh(bottom["nom"], bottom["taux_structurelle_24"], color=C1, height=0.6, label="5 taux les plus bas")
national = dep["structurelle_24"].sum() / dep["parc_prive_24"].sum() * 100
ax.axvline(national, color="#999999", ls="--", lw=1)
ax.annotate(f"France : {national:.1f} %", (national + 0.1, 0.2), fontsize=8, color="#555555")
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f %%"))
ax.set_title("Taux de vacance structurelle du parc privé par département\n(> 2 ans, millésime LOVAC 24 — situation au 01/01/2023)")
ax.grid(alpha=0.25, axis="x")
ax.legend(frameon=False, loc="lower right")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 3. Communes : secrétisation et concentration
#
# La donnée communale est secrétisée (« s ») sous 11 logements vacants : il
# faut mesurer ce que l'on perd avant de conclure quoi que ce soit à cette
# échelle.

# %%
communes = read_lovac("lovac-opendata-communes26.csv")
com = pd.DataFrame(
    {
        "code": communes["CODGEO_26"].str.strip(),
        "nom": communes["LIBGEO_26"].str.strip(),
        "dep": communes["DEP"].str.strip(),
        "parc_prive_24": to_num(communes["ff_pp_total_24"]),
        "structurelle_24": to_num(communes["pp_vacant_plus_2ans_24"]),
        "structurelle_26_raw": communes["pp_vacant_plus_2ans_26"].str.strip(),
    }
)
n = len(com)
masked = (com["structurelle_26_raw"] == "s").sum()
print(f"{n} communes ; vacance structurelle mill. 26 secrétisée pour {masked} ({masked / n:.0%})")

visible = com.dropna(subset=["structurelle_24", "parc_prive_24"]).copy()
couverture = visible["structurelle_24"].sum() / dep["structurelle_24"].sum()
print(f"communes visibles (mill. 24) : {len(visible)} ({len(visible) / n:.0%}) — "
      f"couvrant {couverture:.0%} de la vacance structurelle nationale")

# %%
# Paris / Lyon / Marseille sont livrées par arrondissement (75101-75120,
# 69381-69389, 13201-13216) : on les agrège en communes avant tout classement.
PLM = {"751": ("75056", "Paris", "75"), "6938": ("69123", "Lyon", "69"), "132": ("13055", "Marseille", "13")}


def plm_city(code: str) -> str | None:
    """Return the parent-city code of a PLM arrondissement, else None."""
    for prefix, (city_code, _, _) in PLM.items():
        if code.startswith(prefix):
            return city_code
    return None


visible["ville"] = visible["code"].map(lambda c: plm_city(c) or c)
grouped = visible.groupby("ville", as_index=False).agg(
    structurelle_24=("structurelle_24", "sum"), parc_prive_24=("parc_prive_24", "sum")
)
names = dict(zip(visible["ville"], visible["nom"])) | {c: n for c, (n, *_ ) in
    {code: (name, dep) for _, (code, name, dep) in PLM.items()}.items()}
deps_by_city = dict(zip(visible["ville"], visible["dep"])) | {
    code: dep for _, (code, _, dep) in PLM.items()
}
grouped["nom"] = grouped["ville"].map(names)
grouped["dep"] = grouped["ville"].map(deps_by_city)
grouped["taux_24"] = grouped["structurelle_24"] / grouped["parc_prive_24"] * 100
top_communes = grouped.nlargest(10, "structurelle_24")[
    ["ville", "nom", "dep", "structurelle_24", "taux_24"]
]
top_communes.round(1)

# %%
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.hist(grouped["taux_24"].clip(upper=25), bins=50, color=C1)
ax.set_title("Distribution des taux communaux de vacance structurelle (mill. 24,\ncommunes non secrétisées ; borne d'affichage à 25 %)")
ax.set_xlabel("taux de vacance structurelle (%)")
ax.set_ylabel("nombre de communes")
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f %%"))
ax.grid(alpha=0.25, axis="y")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Observations provisoires (à stabiliser avant toute publication)
#
# 1. **La vacance structurelle du parc privé est de l'ordre de 1,1 à 1,2
#    million de logements** (1 179 845 au millésime 26, situation 01/01/2025)
#    et cet ordre de grandeur est à peu près stable sur 2020-2026 — alors que
#    la vacance totale saute de 3,69 M à 2,38 M puis 3,16 M au passage des
#    ruptures 2023/2025 : **seule la structurelle est raisonnablement robuste
#    aux ruptures**, la totale ne doit pas être lue en évolution.
# 2. **Le taux de vacance structurelle (mill. 24) est de 3,5 % du parc privé
#    national, avec un gradient territorial d'un ordre de grandeur** : Mayotte
#    26,9 %, Guyane 11,5 %, Guadeloupe 10,7 %, Martinique 10,4 %, puis la
#    diagonale des faibles densités (Creuse 9,5 %, Nièvre 7,9 %, Allier
#    7,6 %, Meuse 7,4 %) — contre 1,4-1,7 % en zones tendues et sur le
#    littoral ouest (Vendée, Loire-Atlantique, Yvelines, Essonne,
#    Hauts-de-Seine). Premier indice cohérent avec **H-02** (capacités mal
#    localisées).
# 3. **En volume, les grandes villes dominent** (Paris 32 091, Marseille
#    14 529, Nice 6 227, Toulouse 6 040 — PLM agrégées), mais à des taux
#    proches de la moyenne (2-4 %) ; les taux élevés sont ruraux et
#    ultramarins (Fort-de-France 12,9 %, Les Abymes 16,4 %). « Où est la
#    vacance » n'a donc pas une réponse unique : stock urbain vs intensité
#    rurale/DOM.
# 4. **La secrétisation borne l'échelle communale** : 51 % des communes sont
#    masquées au millésime 26 ; les communes visibles au millésime 24 ne sont
#    que 20 % du total mais portent 73 % de la vacance structurelle nationale.
#    L'échelle communale est utilisable pour les volumes, pas pour une
#    couverture exhaustive du territoire (biais vers les communes à vacance
#    non négligeable).
# 5. Limites : parc privé uniquement (≠ INSEE), millésime 24 utilisé pour
#    les taux (dernier complet avant la rupture 2025), pas encore de
#    croisement avec les zones d'emploi (D-07) ni les bassins de vie (D-08).
#
# Prochaine étape de stabilisation : lecteur LOVAC en `core/` (parsing 's',
# agrégation PLM, choix de millésime), résultat R-02 (vacance structurelle
# nationale et distribution départementale) et test de régression.

# %%
