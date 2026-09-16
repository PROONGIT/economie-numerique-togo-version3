# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
import json
from functools import reduce

D = "data/processed/"

LEVEL_COLS = {
    "region":     ["region"],
    "prefecture": ["region", "prefecture"],
    "commune":    ["region", "prefecture", "commune"],
    "canton":     ["region", "prefecture", "commune", "canton"],
}


@st.cache_data
def load_all():
    agences      = pd.read_csv(D + "agences.csv")
    datacenters  = pd.read_csv(D + "datacenters.csv")
    mm           = pd.read_csv(D + "mobile_money.csv")
    synth_pref   = pd.read_csv(D + "synthese_prefecture.csv")
    synth_region = pd.read_csv(D + "synthese_region.csv")
    ind_canton   = pd.read_csv(D + "indicateurs_cantonaux.csv")
    geo_pref     = pd.read_csv(D + "synthese_geo_pref.csv")
    geo_reg      = pd.read_csv(D + "synthese_geo_reg.csv")
    with open(D + "kpis_nationaux.json", encoding="utf-8") as f:
        kpis = json.load(f)
    # KPIs géoportail supplémentaires
    couv_vals = ind_canton["couverture_mobile_pct"].dropna()
    mm1_vals  = ind_canton["mm_1km_pct"].dropna()
    kpis["couverture_mobile_moy_pct"]   = round(couv_vals.mean(), 1)
    kpis["mm_1km_moy_pct"]              = round(mm1_vals.mean(), 1)
    kpis["nb_cantons_zone_blanche"]     = int((couv_vals < 50).sum())
    kpis["nb_cantons_couverture_zero"]  = int((couv_vals == 0).sum())
    kpis["nb_banques"]                  = int(ind_canton["n_banques"].sum())
    kpis["nb_mfi"]                      = int(ind_canton["n_mfi"].sum())
    kpis["nb_poste"]                    = int(ind_canton["n_poste"].sum())
    kpis["nb_distributeurs"]            = int(ind_canton["n_distributeurs"].sum())
    return agences, datacenters, mm, synth_pref, synth_region, ind_canton, geo_pref, geo_reg, kpis


def aggregate_table(agences, mm, datacenters, level):
    cols = LEVEL_COLS[level]

    def grp(df, name):
        if df.empty:
            return pd.DataFrame(columns=cols + [name])
        return df.groupby(cols).size().rename(name).reset_index()

    dfs = [
        grp(agences, "nb_agences"),
        grp(agences[agences.get("operateur", pd.Series(dtype=str)) == "Moov"], "nb_agences_moov"),
        grp(agences[agences.get("operateur", pd.Series(dtype=str)) == "Togocom"], "nb_agences_togocom"),
        grp(mm, "nb_agents_mobile_money"),
        grp(datacenters, "nb_datacenters"),
    ]
    out = reduce(lambda l, r: l.merge(r, on=cols, how="outer"), dfs)
    for c in ["nb_agences", "nb_agences_moov", "nb_agences_togocom",
              "nb_agents_mobile_money", "nb_datacenters"]:
        if c not in out.columns:
            out[c] = 0
        out[c] = out[c].fillna(0).astype(int)
    return out.sort_values("nb_agences", ascending=False).reset_index(drop=True)


def with_population(df, level, synth_pref, synth_region):
    df = df.copy()
    if level == "prefecture":
        df = df.merge(synth_pref[["region", "prefecture", "population"]],
                      on=["region", "prefecture"], how="left")
    elif level == "region":
        df = df.merge(synth_region[["region", "population"]], on="region", how="left")
    else:
        df["population"] = pd.NA
    has_pop = df["population"].notna().any()
    if has_pop:
        df["agences_pour_100k_hab"]    = (df["nb_agences"] / df["population"] * 100_000).round(2)
        df["agents_mm_pour_10k_hab"]   = (df["nb_agents_mobile_money"] / df["population"] * 10_000).round(2)
    else:
        df["agences_pour_100k_hab"]  = pd.NA
        df["agents_mm_pour_10k_hab"] = pd.NA
    return df


def with_geo_indicators(df, level, ind_canton, geo_pref, geo_reg):
    """Ajoute les indicateurs géoportail (couverture mobile, MM 1km, services) selon le niveau."""
    df = df.copy()
    if level == "canton":
        merge_cols = ["region", "prefecture", "commune", "canton"]
        geo_cols = ["couverture_mobile_pct", "mm_1km_pct", "togocom_5km_pct",
                    "habitants_par_mm", "n_banques", "n_mfi", "n_poste", "n_distributeurs"]
        avail = [c for c in merge_cols + geo_cols if c in ind_canton.columns]
        df = df.merge(ind_canton[avail], on=merge_cols, how="left")
    elif level == "prefecture":
        geo_cols = ["couverture_mobile_moy", "mm_1km_pct_moy", "togocom_5km_pct_moy",
                    "n_banques", "n_mfi", "n_poste", "n_distributeurs",
                    "n_marches", "cantons_zone_blanche"]
        avail = [c for c in ["region", "prefecture"] + geo_cols if c in geo_pref.columns]
        df = df.merge(geo_pref[avail], on=["region", "prefecture"], how="left")
    elif level == "region":
        geo_cols = ["couverture_mobile_moy", "mm_1km_pct_moy",
                    "n_banques", "n_mfi", "n_poste", "n_distributeurs",
                    "n_marches", "cantons_zone_blanche"]
        avail = [c for c in ["region"] + geo_cols if c in geo_reg.columns]
        df = df.merge(geo_reg[avail], on="region", how="left")
    return df


@st.cache_data
def region_hulls(mm):
    from scipy.spatial import ConvexHull
    hulls = {}
    for region, g in mm.groupby("region"):
        pts = g[["lon", "lat"]].dropna().values
        if len(pts) < 3:
            continue
        try:
            hull = ConvexHull(pts)
            order = list(hull.vertices) + [hull.vertices[0]]
            hulls[region] = (pts[order, 0].tolist(), pts[order, 1].tolist())
        except Exception:
            continue
    return hulls


def aggregate_geo(mm, agences, level):
    cols = LEVEL_COLS[level]
    if mm.empty and agences.empty:
        return pd.DataFrame(columns=cols + ["lat", "lon", "nb_agents_mm", "nb_agences"])
    mm_g = (mm.groupby(cols).agg(lat=("lat", "mean"), lon=("lon", "mean"),
                                  nb_agents_mm=("lat", "count")).reset_index()
            if not mm.empty else pd.DataFrame(columns=cols + ["lat", "lon", "nb_agents_mm"]))
    ag_count = (agences.groupby(cols).size().rename("nb_agences").reset_index()
                if not agences.empty else pd.DataFrame(columns=cols + ["nb_agences"]))
    out = mm_g.merge(ag_count, on=cols, how="outer")
    out["nb_agents_mm"] = out["nb_agents_mm"].fillna(0).astype(int)
    out["nb_agences"]   = out["nb_agences"].fillna(0).astype(int)
    missing = out["lat"].isna()
    if missing.any() and not agences.empty:
        ag_ll = agences.groupby(cols).agg(lat=("lat", "mean"), lon=("lon", "mean")).reset_index()
        out = out.merge(ag_ll, on=cols, how="left", suffixes=("", "_ag"))
        out["lat"] = out["lat"].fillna(out["lat_ag"])
        out["lon"] = out["lon"].fillna(out["lon_ag"])
        out = out.drop(columns=["lat_ag", "lon_ag"], errors="ignore")
    return out.dropna(subset=["lat", "lon"])
