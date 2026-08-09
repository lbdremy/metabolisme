# Vérification orchestrateur des recalculs allégués par le relecteur n°3 (SE-1, SE-4, SE-6).
# Lecture seule ; réutilise les mêmes constructions de frames que shell/build.py.
from pathlib import Path

import pandas as pd

from logement.core import stats
from logement.shell import build

ROOT = Path("/Volumes/Work/github/metabolisme/logement")


def partial_spearman(frame: pd.DataFrame, x: str, y: str, z: str) -> tuple[float, float, int]:
    sub = frame[[x, y, z]].dropna()
    ranks = sub.rank()
    r = ranks.corr(method="pearson")
    rxy, rxz, ryz = r.loc[x, y], r.loc[x, z], r.loc[y, z]
    partial = (rxy - rxz * ryz) / ((1 - rxz**2) ** 0.5 * (1 - ryz**2) ** 0.5)
    return float(rxy), float(partial), len(sub)


# ---- R-11 frame (même construction que build_mobilite) ----
parts = build._lstay_parts(ROOT)
from logement.core import mobilite  # noqa: E402

ze_frame = mobilite.rotation_by_ze(parts)
cost = build._cost_frame(ROOT)["indice_cout_pct"]

import zipfile  # noqa: E402

from logement.core import lovac, rs, tension, ze  # noqa: E402

raw = ROOT / "data" / "raw"
with zipfile.ZipFile(raw / build.CENSUS_ZIP) as zf, zf.open(build.CENSUS_CSV) as fh:
    census_raw = pd.read_csv(fh, sep=";", dtype=str, usecols=["CODGEO", *rs.CENSUS_COLS])
census = rs.parse_census_housing(census_raw)
tlv = tension.parse_tlv(pd.read_csv(raw / build.TLV_FILE, sep=";", dtype=str))
commune_ze = ze.parse_commune_ze(build._read_membership(ROOT))
communes = lovac.parse_territories(
    build._read_lovac(ROOT, build.LOVAC_COMMUNES), code_col="CODGEO_26", name_col="LIBGEO_26"
)
h08 = build._load_hypothesis(ROOT, "H-08")
h12 = build._load_hypothesis(ROOT, "H-12")
tension_frame = tension.tension_by_ze(
    census, tlv, communes, commune_ze, h08.central_value, h12.central_value
)

f11 = ze_frame.copy()
f11["cout"] = cost
f11["tendue"] = tension_frame["tendue"]
f11["niveau_2012"] = f11["part_recents_debut_pct"]
f11["delta_rel"] = f11["delta_pts"] / f11["niveau_2012"] * 100.0
met11 = f11[~stats.is_dom_index(f11)]

print("== SE-1 (R-11, métropole) ==")
rho, part, n = partial_spearman(met11, "delta_pts", "niveau_2012", "cout")
print(f"rho(delta, niveau_2012) = {rho:+.3f} (n={n})  [allégué −0,52]")
t = met11.dropna(subset=["tendue"])
print(
    "niveau 2012 médian tendues/autres :",
    round(float(t[t['tendue'].astype(bool)]["niveau_2012"].median()), 2),
    "/",
    round(float(t[~t['tendue'].astype(bool)]["niveau_2012"].median()), 2),
    "[allégué 12,59 / 11,78]",
)
print(
    "chute relative médiane tendues/autres :",
    round(float(t[t['tendue'].astype(bool)]["delta_rel"].median()), 1),
    "/",
    round(float(t[~t['tendue'].astype(bool)]["delta_rel"].median()), 1),
    "% [allégué −12,2 / −10,7]",
)
rho_rel, _, _ = partial_spearman(met11, "delta_rel", "cout", "niveau_2012")
print(f"rho(delta_rel, cout) = {rho_rel:+.3f}  [allégué −0,20]")
_, p_abs, n_abs = partial_spearman(met11, "delta_pts", "cout", "niveau_2012")
_, p_rel, _ = partial_spearman(met11, "delta_rel", "cout", "niveau_2012")
print(f"partial(delta, cout | niveau_2012) = {p_abs:+.3f} (n={n_abs})  [allégué −0,07]")
print(f"partial(delta_rel, cout | niveau_2012) = {p_rel:+.3f}  [allégué −0,09]")

# ---- R-12 frame (même construction que build_social) ----
from logement.core import social  # noqa: E402

with zipfile.ZipFile(raw / build.RPLS_ZIP) as zf, zf.open(build.RPLS_XLSX) as fh:
    commune_raw = pd.read_excel(
        fh, sheet_name="COMMUNE", engine="calamine", header=5, dtype={"DEPCOM_ARM": str}
    )
communes_rpls = social.parse_rpls_communes(commune_raw)
social_ze = social.social_by_ze(communes_rpls, commune_ze)
f12 = social_ze[social_ze["parc_2025"] >= 500].copy() if "parc_2025" in social_ze else social_ze.copy()
print("\ncolonnes social_ze:", list(social_ze.columns))
seuil_col = [c for c in social_ze.columns if "parc" in c or "nb_ls" in c]
print("colonnes parc:", seuil_col)
f12 = social_ze.copy()
if "parc_2025" in f12.columns:
    f12 = f12[f12["parc_2025"] >= 500]
elif "nb_ls" in f12.columns:
    f12 = f12[f12["nb_ls"] >= 500]
f12["cout"] = cost
f12["delta_rel"] = f12["delta_2019_2025"] / f12["tx_mob_2019"] * 100.0
met12 = f12[~stats.is_dom_index(f12)]

print("\n== SE-4 (R-12, métropole, parc >= 500) ==")
rho_n, _, n12 = partial_spearman(met12, "delta_2019_2025", "tx_mob_2019", "cout")
print(f"rho(delta, niveau_2019) = {rho_n:+.3f} (n={n12})  [allégué −0,51]")
_, p12_abs, _ = partial_spearman(met12, "delta_2019_2025", "cout", "tx_mob_2019")
_, p12_rel, _ = partial_spearman(met12, "delta_rel", "cout", "tx_mob_2019")
print(f"partial(delta, cout | niveau_2019) = {p12_abs:+.3f}  [allégué −0,50]")
print(f"partial(delta_rel, cout | niveau_2019) = {p12_rel:+.3f}  [allégué −0,51]")
t12 = met12.dropna(subset=["delta_rel"])
tt = t12.join(tension_frame["tendue"], how="left").dropna(subset=["tendue"])
print(
    "chute relative médiane tendues/autres :",
    round(float(tt[tt['tendue'].astype(bool)]["delta_rel"].median()), 1),
    "/",
    round(float(tt[~tt['tendue'].astype(bool)]["delta_rel"].median()), 1),
    "% [allégué −26,0 / −22,4]",
)

# rho 2013/2019/2025 vs coût (SE-5)
print("\n== SE-5 (rho mobilité sociale × coût par millésime, métropole) ==")
for col in ("tx_mob_2013", "tx_mob_2019", "tx_mob_2025"):
    sub = met12[[col, "cout"]].dropna()
    r = sub.rank().corr().iloc[0, 1]
    print(f"rho({col}, cout) = {r:+.3f} (n={len(sub)})")

# ---- SE-6 : partial(mob sociale 2025, rotation R-11 | coût) ----
print("\n== SE-6 (métropole) ==")
f6 = met12.join(ze_frame["part_recents_pct"], how="inner")
rho6, p6, n6 = partial_spearman(f6, "tx_mob_2025", "part_recents_pct", "cout")
print(f"rho(mob sociale, rotation) = {rho6:+.3f} (n={n6})  [publié −0,20]")
print(f"partial(mob sociale, rotation | cout) = {p6:+.3f}  [allégué +0,21]")
