"""Compléments du recalcul indépendant (revue statistique 2026-09-18).

Part 1 : ZE de M-D hors du périmètre OFGL de la charge (ST-3).
Part 2 : base de surface des loyers d'équilibre M-B (ST-1) — variantes surface C-07 / surface implicite DVF / tout-par-m².

Run from logement/:  uv run python evidence/revue-contradictoire-2026-09-18/verify-statistique-complements.py
"""

# ---------------------------------------------------------------- Part 1
import json, zipfile
import pandas as pd
from pathlib import Path
from logement.core import rs, ze, transaction, cout
from logement.shell import build
ROOT = Path("/Volumes/Work/github/metabolisme/logement"); RAW = ROOT/"data"/"raw"
ART = json.loads((ROOT/"data/processed/scenarios-institutionnels-ze.json").read_text())
commune_ze = ze.parse_commune_ze(build._read_membership(ROOT))
with zipfile.ZipFile(RAW/build.CENSUS_ZIP) as zf, zf.open(build.CENSUS_CSV) as fh:
    census = rs.parse_census_housing(pd.read_csv(fh, sep=";", dtype=str, usecols=["CODGEO", *rs.CENSUS_COLS]))
m = census.merge(commune_ze, on="code")
m["dep"] = m["code"].map(transaction.departement_of)
m["excl"] = m["dep"].isin(("75","69","2A","2B","972","973"))
by = m.groupby("ze").apply(lambda d: pd.Series({"log": d["P22_LOG"].sum(), "log_excl": d.loc[d["excl"],"P22_LOG"].sum()}))
by["share_excl"] = by["log_excl"]/by["log"]
names = build._ze_names(ROOT)
md = ART["m_d_bascule_dmto"]
listed = {e["ze"] for e in md["bascule_la_plus_favorable_au_mobile"]+md["bascule_la_moins_favorable_au_mobile"]}
full = by[by["share_excl"]>=0.999]; part = by[(by["share_excl"]>0.001)&(by["share_excl"]<0.999)]
print("ZE entièrement hors périmètre :", len(full), [(z, names.get(z,'?'), round(by.loc[z,'share_excl'],2)) for z in full.index])
print("ZE partiellement hors périmètre :", len(part), [(z, names.get(z,'?'), round(by.loc[z,'share_excl'],2)) for z in part.index])
print("dont dans les listes publiées de R-17 :", [(z, names.get(z,'?'), round(by.loc[z,'share_excl'],2)) for z in listed if by.loc[z,'share_excl']>0])
# ZE with prix but no niveau de vie
with zipfile.ZipFile(RAW/build.FILOSOFI_ZIP) as zf, zf.open(build.FILOSOFI_CSV) as fh:
    filo = pd.read_csv(fh, sep=";", dtype=str, usecols=["GEO","GEO_OBJECT","FILOSOFI_MEASURE","OBS_VALUE"])
nv = cout.parse_filosofi(filo, geo_object="ZE2020", measure="MED_SL")
prix_ze = json.loads((ROOT/"data/processed/cout-transaction-ze.json").read_text())
print("clés cout-transaction:", list(prix_ze.keys())[:12])

# ---------------------------------------------------------------- Part 2
import json, zipfile
import pandas as pd
from pathlib import Path
from logement.core import rs, ze, transaction, effort, tension, lovac, remob
from logement.core.lovac import plm_parent
from logement.shell import build
ROOT = Path("/Volumes/Work/github/metabolisme/logement"); RAW = ROOT/"data"/"raw"
H = {h: build._load_hypothesis(ROOT, h) for h in ("H-08","H-12","H-09","H-10")}
with zipfile.ZipFile(RAW/build.CENSUS_ZIP) as zf, zf.open(build.CENSUS_CSV) as fh:
    census = rs.parse_census_housing(pd.read_csv(fh, sep=";", dtype=str, usecols=["CODGEO", *rs.CENSUS_COLS]))
with zipfile.ZipFile(RAW/build.CENSUS_ZIP) as zf, zf.open(build.CENSUS_CSV) as fh:
    census_mix = effort.parse_census_mix(pd.read_csv(fh, sep=";", dtype=str, usecols=["CODGEO", *effort.CENSUS_MIX_COLS]))
tlv = tension.parse_tlv(pd.read_csv(RAW/build.TLV_FILE, sep=";", dtype=str))
commune_ze = ze.parse_commune_ze(build._read_membership(ROOT))
communes = lovac.parse_territories(build._read_lovac(ROOT, build.LOVAC_COMMUNES), code_col="CODGEO_26", name_col="LIBGEO_26")
t = tension.tension_by_ze(census, tlv, communes, commune_ze, H["H-08"].central_value, H["H-12"].central_value)
mix = census_mix.merge(commune_ze, on="code", how="left").dropna(subset=["ze"]).groupby("ze")[["rp_maison","rp_appart"]].sum()
pm = mix["rp_maison"]/(mix["rp_maison"]+mix["rp_appart"])
det = remob.detente_frame(t[t["tendue"]], pm, build._ze_names(ROOT))
ipea = remob.ipea_factor(remob.parse_ipea_annual_means((RAW/build.IPEA_FILE).read_text(encoding="utf-8")))
cu = remob.unit_cost_eur(det["part_maison"], H["H-09"].central_value, H["H-10"].central_value, ipea)
dvf = pd.read_csv(RAW/build.DVF_FILE, usecols=list(transaction.DVF_COLUMNS), dtype={"code_commune": str})
sales, _ = transaction.parse_dvf_sales(dvf)
prix, _ = transaction.prices_by_ze(sales, commune_ze)
with zipfile.ZipFile(RAW/build.RPLS_ZIP) as zf, zf.open(build.RPLS_XLSX) as fh:
    r = pd.read_excel(fh, sheet_name="COMMUNE", engine="calamine", header=5, dtype={"DEPCOM_ARM": str})
rp = pd.DataFrame({"code": r["DEPCOM_ARM"].astype("string").str.strip().map(plm_parent), "nb_ls": pd.to_numeric(r["nb_ls"], errors="coerce"), "loymoy": pd.to_numeric(r["loymoy"], errors="coerce")}).dropna().merge(commune_ze, on="code")
rp = rp[rp.nb_ls>0]; soc = (rp.loymoy*rp.nb_ls).groupby(rp.ze).sum()/rp.groupby("ze").nb_ls.sum()
mar = build._effort_frame(ROOT)["loyer_mix_m2"]
f = det.join(cu.rename("cu")).join(prix, how="inner"); f["soc"]=soc; f["mar"]=mar
af = 0.023/(1-1.023**-40); opex=0.549
f["s07"] = f.part_maison*114.3+(1-f.part_maison)*65.5
f["simp"] = f.prix_median/f.prix_m2_median
f["unit"] = f.prix_median+f.cu
for lab, s in (("C-07", f.s07), ("implicite DVF", f.simp)):
    ler = f.unit*af/(1-opex)/12/s; len_ = 169200*af/(1-opex)/12/s
    sub = ((ler-f.soc).clip(lower=0)*s*12*f.renovables).sum()+((len_-f.soc).clip(lower=0)*s*12*f.deficit_neuf).sum()
    wr = f.dropna(subset=["mar","soc"]).index
    print(f"surface {lab}: loyer rénové médian {ler.median():.2f} (ratio/marché médian {(ler[wr]/f.loc[wr,'mar']).median():.2f}), "
          f"neuf médian {len_.median():.2f} (ratio/marché {(len_[wr]/f.loc[wr,'mar']).median():.2f}, n ZE neuf ≤ marché {(len_[wr]<=f.loc[wr,'mar']).sum()}/{len(wr)}), "
          f"subvention {sub/1e9:.2f} Md€/an ; ratio/social médian sur 96 : {(ler/f.soc).median():.2f}, sur 93 : {(ler[wr]/f.loc[wr,'soc']).median():.2f}")
# subsidy in € per dwelling is surface-free for the annuity part: show the € per dwelling social revenue
print(f"loyer social médian ×12× surface C-07 médiane = {6.43*12*f.s07.median():,.0f} €/an vs à la surface implicite {6.43*12*f.simp.median():,.0f} €/an ; surface C-07 médiane {f.s07.median():.1f}, implicite médiane {f.simp.median():.1f}")
nv_missing = prix.index.difference(build._effort_frame(ROOT).index)
print("ZE M-D sans niveau de vie :", len(nv_missing))
# surface-free variant: everything per m² (DVF price/m² + renovation cost per m² at the C-07 mix), no dwelling surface at all
ler_m2 = (f.prix_m2_median + f.cu/f.s07)*af/(1-opex)/12
wr = f.dropna(subset=["mar","soc"]).index
print(f"variante tout-par-m² (prix_m2_median + cu/m²) : loyer rénové médian {ler_m2.median():.2f} €/m² ; ratio/marché médian {(ler_m2[wr]/f.loc[wr,'mar']).median():.2f} ; "
      f"Annecy {ler_m2['8401']:.2f} ; Bayonne {ler_m2['7503']:.2f} ; Digne {ler_m2['9307']:.2f}")
for s in (65.5, 70.0):
    len_ = 169200*af/(1-opex)/12/s
    print(f"neuf S-18 à {s} m² : {len_:.2f} €/m² (uniforme) ; n ZE ≤ marché {(len_<=f.loc[wr,'mar']).sum()}/{len(wr)}")
