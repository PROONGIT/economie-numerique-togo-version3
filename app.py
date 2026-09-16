# -*- coding: utf-8 -*-
import re, base64, json
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

from i18n import t
from theme import THEMES, inject_css
from data_loader import (load_all, aggregate_table, with_population,
                          with_geo_indicators, aggregate_geo, LEVEL_COLS)

st.set_page_config(page_title="Télécoms & Numérique — Togo",
                   page_icon="assets/sceau_togo.png",
                   layout="wide", initial_sidebar_state="expanded")

if "lang"  not in st.session_state: st.session_state.lang  = "fr"
if "theme" not in st.session_state: st.session_state.theme = "clair"

(agences, datacenters, mm, synth_pref, synth_region,
 ind_canton, geo_pref, geo_reg, kpis) = load_all()

# ── Chargement GeoJSON cantons (polygones réels)
@st.cache_data
def load_cantons_geo():
    path = Path("assets/cantons.geojson")
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)

CANTONS_GEO = load_cantons_geo()

# ── DataFrame cantons depuis le GeoJSON (toutes propriétés déjà incluses)
@st.cache_data
def cantons_df_from_geo():
    if CANTONS_GEO is None:
        return pd.DataFrame()
    rows = [feat["properties"] for feat in CANTONS_GEO["features"]]
    return pd.DataFrame(rows)

CANTONS_DF = cantons_df_from_geo()

OP_COLORS   = {"Moov": "#0072CE", "Togocom": "#F5A300", "Datacenter": "#D21034"}
GRAN_LEVELS = ["region", "prefecture", "commune", "canton"]
GRAN_LABEL_KEYS = {"region":"gran_region","prefecture":"gran_prefecture",
                   "commune":"gran_commune","canton":"gran_canton"}
REGION_COLORS = {"Maritime":"#006A4E","Plateaux":"#FFCE00",
                 "Centrale":"#D21034","Kara":"#0B3D2E","Savanes":"#7A4FA0"}

with open("assets/sceau_togo.png","rb") as _f:
    SEAL_B64 = base64.b64encode(_f.read()).decode()

# ══════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════
with st.sidebar:
    lang_is_en = st.toggle("🇫🇷 FR  ⇄  🇬🇧 EN",
                            value=(st.session_state.lang=="en"))
    st.session_state.lang = "en" if lang_is_en else "fr"
    lang = st.session_state.lang

    theme_is_dark = st.toggle(
        f"☀️ {t('theme_light',lang)}  ⇄  🌙 {t('theme_dark',lang)}",
        value=(st.session_state.theme=="sombre"))
    st.session_state.theme = "sombre" if theme_is_dark else "clair"
    theme = st.session_state.theme
    T = THEMES[theme]

    st.markdown("---")
    col1,col2,col3 = st.columns([2,1,2])
    with col2: st.image("assets/sceau_togo.png", width=90)
    st.markdown(f"<div style='text-align:center'><strong>{t('republic_name',lang)}</strong></div>",
                unsafe_allow_html=True)
    st.markdown("---")

    st.markdown(f"**{t('nav_title',lang)}**")
    page = st.radio(t("nav_title",lang),
        options=["overview","map","mm","density","coverage","services","reco"],
        format_func=lambda k:{
            "overview":t("nav_overview",lang),"map":t("nav_map",lang),
            "mm":t("nav_mm",lang),"density":t("nav_density",lang),
            "coverage":t("nav_coverage",lang),"services":t("nav_services",lang),
            "reco":t("nav_reco",lang),
        }[k], label_visibility="collapsed")

    st.markdown("---")
    st.markdown(f"**{t('filters',lang)}**")
    all_regions  = sorted(synth_pref["region"].unique())
    sel_regions  = st.multiselect(t("region_filter",lang), all_regions, default=all_regions)
    sel_operators= st.multiselect(t("operator_filter",lang), ["Moov","Togocom"],
                                   default=["Moov","Togocom"])
    sel_gran     = st.select_slider(t("granularity",lang), options=GRAN_LEVELS,
                                     value="prefecture",
                                     format_func=lambda k:t(GRAN_LABEL_KEYS[k],lang))
    st.caption(f"🗺️ {t(GRAN_LABEL_KEYS[sel_gran],lang)} · "
               f"📡 {', '.join(sel_operators) or '—'} · "
               f"🌍 {len(sel_regions)}/{len(all_regions)}")
    st.markdown("---")
    st.caption(t("source_note",lang))
    st.caption(t("author",lang))

st.markdown(inject_css(theme), unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# FILTRAGE
# ══════════════════════════════════════════════════════
sel_regions_eff   = sel_regions or []
sel_operators_eff = sel_operators or []

ag_f = agences[agences["region"].isin(sel_regions_eff)
               & agences["operateur"].isin(sel_operators_eff)]
dc_f = datacenters[datacenters["region"].isin(sel_regions_eff)]

if set(sel_operators_eff) >= {"Moov","Togocom"}:
    mm_f = mm[mm["region"].isin(sel_regions_eff)]
elif sel_operators_eff:
    mask = mm["operateur"].apply(lambda x: any(op in x for op in sel_operators_eff))
    mm_f = mm[mm["region"].isin(sel_regions_eff) & mask]
else:
    mm_f = mm.iloc[0:0]

ind_f = ind_canton[ind_canton["region"].isin(sel_regions_eff)]
gp_f  = geo_pref[geo_pref["region"].isin(sel_regions_eff)]
gr_f  = geo_reg[geo_reg["region"].isin(sel_regions_eff)]

# DataFrame cantons filtrés (depuis GeoJSON — source de vérité)
cantons_f = CANTONS_DF[CANTONS_DF["region"].isin(sel_regions_eff)].copy() \
            if not CANTONS_DF.empty else pd.DataFrame()

GRAN_LABEL    = t(GRAN_LABEL_KEYS[sel_gran], lang)
OPS_LABEL     = ", ".join(sel_operators_eff) if sel_operators_eff else "—"
REGIONS_LABEL = ", ".join(sel_regions_eff) if len(sel_regions_eff) < len(all_regions) \
                else t("all",lang)

agg      = with_population(aggregate_table(ag_f,mm_f,dc_f,sel_gran),
                            sel_gran, synth_pref, synth_region)
agg      = with_geo_indicators(agg, sel_gran, ind_f, gp_f, gr_f)
agg_pref = with_population(aggregate_table(ag_f,mm_f,dc_f,"prefecture"),
                            "prefecture", synth_pref, synth_region)
agg_pref = with_geo_indicators(agg_pref,"prefecture",ind_f,gp_f,gr_f)
agg_reg  = with_population(aggregate_table(ag_f,mm_f,dc_f,"region"),
                            "region", synth_pref, synth_region)
agg_reg  = with_geo_indicators(agg_reg,"region",ind_f,gp_f,gr_f)

PLOT_KW = dict(template=T["plot_template"], paper_bgcolor=T["bg"],
               plot_bgcolor=T["bg"], font_color=T["text"])

# ══════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════
def md_to_html(text):
    return re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)

def kpi_card(col, value, label, alert=False):
    cls = "kpi-value-alert" if alert else "kpi-value"
    with col:
        st.markdown(
            f'<div class="kpi-card"><div class="{cls}">{value}</div>'
            f'<div class="kpi-label">{label}</div></div>',
            unsafe_allow_html=True)

def analysis_box(text, style="normal"):
    css = {"normal":"insight-card","warn":"insight-card-warn",
           "alert":"insight-card-alert"}.get(style,"insight-card")
    st.markdown(f'<div class="{css}">{md_to_html(text)}</div>',
                unsafe_allow_html=True)

def header(title, subtitle=None):
    sub_html = f'<p style="margin:0;opacity:0.9;">{subtitle}</p>' if subtitle else ""
    st.markdown(
        f'<div class="header-band">'
        f'<img src="data:image/png;base64,{SEAL_B64}" '
        f'style="height:56px;margin-right:16px;border-radius:6px;">'
        f'<div><h2 style="margin:0;">{title}</h2>{sub_html}</div></div>',
        unsafe_allow_html=True)

def how_to_read(what, shows):
    with st.expander(t("how_to_read",lang)):
        st.markdown(f"**{t('what_it_is',lang)}** — {what}")
        st.markdown(f"**{t('what_it_shows',lang)}** — {shows}")

# ── Choroplèthe Folium (polygones réels des cantons)
def choropleth(metric, alias, colorscale="YlOrRd", height=520,
               regions=None, reverse=False):
    """Carte choroplèthe sur les polygones cantonaux réels.
    metric  : nom de la propriété dans cantons.geojson
    alias   : libellé de la légende
    regions : liste de régions à filtrer (None = toutes)
    """
    if CANTONS_GEO is None:
        st.warning("cantons.geojson introuvable dans assets/")
        return

    # Filtrer le GeoJSON si besoin
    if regions:
        geo_filtered = {
            "type": "FeatureCollection",
            "features": [f for f in CANTONS_GEO["features"]
                         if f["properties"].get("region") in regions]
        }
    else:
        geo_filtered = CANTONS_GEO

    if not geo_filtered["features"]:
        st.info("Aucun canton pour la sélection.")
        return

    # Centrer la carte sur le Togo
    m = folium.Map(location=[8.6, 1.0], zoom_start=7,
                   tiles="CartoDB positron", control_scale=True)

    # Données pour la choroplèthe
    data = pd.DataFrame([
        {"canton_id": f["properties"]["canton_id"],
         metric: f["properties"].get(metric)}
        for f in geo_filtered["features"]
    ]).dropna(subset=[metric])

    if data.empty:
        st.info(f"Pas de données pour l'indicateur '{metric}'.")
        return

    folium.Choropleth(
        geo_data=geo_filtered,
        data=data,
        columns=["canton_id", metric],
        key_on="feature.properties.canton_id",
        fill_color=colorscale,
        fill_opacity=0.80,
        line_opacity=0.25,
        line_color="#FFFFFF",
        nan_fill_color="#CCCCCC",
        legend_name=alias,
        bins=7,
    ).add_to(m)

    # Tooltip interactif sur survol
    tooltip_fields  = ["canton","prefecture","region", metric]
    tooltip_aliases = ["Canton","Préfecture","Région", alias]
    # Ajouter champs bonus selon le contexte
    extras = {
        "couverture_mobile_pct": [("mm_1km_pct","% pop <1km MM"),
                                   ("indice_acces","Indice d'accès")],
        "indice_acces":          [("couverture_mobile_pct","Couv. mobile %"),
                                   ("mm_1km_pct","% pop <1km MM")],
        "mm_1km_pct":            [("couverture_mobile_pct","Couv. mobile %"),
                                   ("mm_pour_10k","Agents/10k hab")],
        "n_agences":             [("population","Population"),
                                   ("agences_pour_100k","Agences/100k")],
        "n_mobile_money":        [("mm_pour_10k","Agents/10k hab"),
                                   ("habitants_par_mm","Hab./agent")],
    }
    for field, lbl in extras.get(metric, []):
        tooltip_fields.append(field)
        tooltip_aliases.append(lbl)
    # Toujours ajouter population en dernier
    if "population" not in tooltip_fields:
        tooltip_fields.append("population")
        tooltip_aliases.append("Population")

    folium.GeoJson(
        geo_filtered,
        style_function=lambda x: {
            "fillColor": "transparent",
            "color": "transparent",
            "weight": 0,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=tooltip_fields,
            aliases=[a+" :" for a in tooltip_aliases],
            localize=True, sticky=True,
            style="font-size:13px;font-family:sans-serif;"
        ),
    ).add_to(m)

    # Agences (points) en surcouche optionnelle
    if not ag_f.empty:
        fg = folium.FeatureGroup(name="Agences", show=False)
        for _, r in ag_f.iterrows():
            if pd.notna(r.get("lat")) and pd.notna(r.get("lon")):
                col = OP_COLORS.get(r.get("operateur",""), "#888")
                folium.CircleMarker(
                    [r["lat"], r["lon"]], radius=5,
                    color=col, fill=True, fill_color=col,
                    fill_opacity=0.9, weight=1.2,
                    tooltip=f"{r.get('nom','—')} · {r.get('operateur','')}"
                ).add_to(fg)
        fg.add_to(m)
        folium.LayerControl(collapsed=True).add_to(m)

    st_folium(m, width="100%", height=height, returned_objects=[])


# ══════════════════════════════════════════════════════
# PAGE : VUE D'ENSEMBLE
# ══════════════════════════════════════════════════════
if page == "overview":
    header(t("app_title",lang), t("app_subtitle",lang))
    st.markdown(t("ov_welcome",lang))
    st.markdown("###")

    c1,c2,c3,c4 = st.columns(4)
    kpi_card(c1, f"{kpis['population_totale']:,.0f}".replace(",",""),
             t("kpi_population",lang))
    kpi_card(c2, kpis["nb_agences_total"], t("kpi_agences",lang))
    kpi_card(c3, kpis["nb_datacenters"],   t("kpi_datacenters",lang))
    kpi_card(c4, f"{kpis['nb_agents_mobile_money']:,}".replace(",",""),
             t("kpi_mm",lang))

    c5,c6,c7,c8 = st.columns(4)
    kpi_card(c5, f"{kpis['couverture_mobile_moy_pct']}%", t("kpi_couv_mobile",lang))
    kpi_card(c6, f"{kpis['mm_1km_moy_pct']}%",           t("kpi_mm_1km",lang))
    kpi_card(c7, f"{kpis['nb_cantons_zone_blanche']} / 396",
             t("kpi_zones_blanches",lang), alert=True)
    kpi_card(c8, f"{kpis['nb_cantons_sans_agence']} / 396",
             t("kpi_cantons_sans_agence",lang), alert=True)

    st.markdown("###")
    col_map, col_chart = st.columns([1.3, 1])

    with col_map:
        st.markdown(f"##### {'Indice composite d\'accès numérique par canton' if lang=='fr' else 'Composite digital access index by canton'}")
        choropleth("indice_acces",
                   "Indice d'accès numérique" if lang=="fr" else "Digital access index",
                   colorscale="YlGn",
                   regions=sel_regions_eff, height=480)

    with col_chart:
        st.markdown(f"##### {'Couverture mobile et accès MM par région' if lang=='fr' else 'Mobile coverage and MM access by region'}")
        if not gr_f.empty and "couverture_mobile_moy" in gr_f.columns:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=gr_f["region"], y=gr_f["couverture_mobile_moy"],
                name="Couv. mobile %", marker_color=T["green"], marker_corner_radius=4))
            fig.add_trace(go.Bar(
                x=gr_f["region"], y=gr_f["mm_1km_pct_moy"],
                name="% pop <1km MM", marker_color=T["yellow"], borderradius=4))
            fig.update_layout(**PLOT_KW, height=300, barmode="group",
                              legend=dict(orientation="h", y=1.08))
            fig.update_yaxes(range=[0,100], ticksuffix="%")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("###")
        st.subheader(t("ov_findings_title",lang))
        for k in ["ov_f1","ov_f2","ov_f3","ov_f4","ov_f5"]:
            style = "alert" if k in ("ov_f1","ov_f4") \
                    else ("warn" if k in ("ov_f2","ov_f3") else "normal")
            analysis_box(t(k,lang), style)

# ══════════════════════════════════════════════════════
# PAGE : AGENCES & DATACENTERS
# ══════════════════════════════════════════════════════
elif page == "map":
    header(t("nav_map",lang))
    st.markdown(t("map_intro",lang))

    col_map, col_chart = st.columns([1.3,1])

    with col_map:
        st.markdown(f"##### {'Nombre d\'agences par canton (polygones réels)' if lang=='fr' else 'Agencies by canton (real polygons)'}")
        choropleth("n_agences",
                   "Nb agences" if lang=="fr" else "Nb agencies",
                   colorscale="Blues",
                   regions=sel_regions_eff, height=500)

    with col_chart:
        # Agences par région et opérateur
        st.markdown(f"##### {'Agences par région et opérateur' if lang=='fr' else 'Agencies by region and operator'}")
        if not agg_reg.empty:
            fig = go.Figure()
            for col_name, color, label in [
                ("nb_agences_moov", OP_COLORS["Moov"], "Moov"),
                ("nb_agences_togocom", OP_COLORS["Togocom"], "Togocom"),
            ]:
                if col_name in agg_reg.columns:
                    fig.add_trace(go.Bar(
                        x=agg_reg["region"], y=agg_reg[col_name],
                        name=label, marker_color=color, borderradius=4))
            fig.update_layout(**PLOT_KW, height=300, barmode="group",
                              legend=dict(orientation="h", y=1.08))
            st.plotly_chart(fig, use_container_width=True)

        # Analyse dynamique
        nb_ag   = len(ag_f)
        nb_moov = (ag_f["operateur"]=="Moov").sum()
        nb_tgc  = (ag_f["operateur"]=="Togocom").sum()
        concentration = ""
        if not ag_f.empty:
            rc = ag_f.groupby("region").size().sort_values(ascending=False)
            top_r, top_c = rc.index[0], rc.iloc[0]
            concentration = t("map_concentration_txt",lang).format(
                top_region=top_r, top_pct=round(top_c/nb_ag*100))
        analysis_box(t("map_dynamic_insight",lang).format(
            regions=REGIONS_LABEL, ops=OPS_LABEL,
            nb_ag=nb_ag, nb_moov=nb_moov, nb_togocom=nb_tgc,
            nb_dc=len(dc_f),
            n_units=agg[LEVEL_COLS[sel_gran][-1]].nunique() if not agg.empty else 0,
            level=GRAN_LABEL.lower(), concentration=concentration))

    how_to_read(t("map_how_what",lang), t("map_how_shows",lang))

    st.subheader(t("table_title_dynamic",lang).format(level=GRAN_LABEL))
    show_cols = LEVEL_COLS[sel_gran] + ["nb_agences_moov","nb_agences_togocom",
                                         "nb_agences","nb_datacenters"]
    if "population" in agg.columns and agg["population"].notna().any():
        show_cols += ["population"]
    st.dataframe(agg[show_cols] if not agg.empty else agg,
                 use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════
# PAGE : MOBILE MONEY
# ══════════════════════════════════════════════════════
elif page == "mm":
    header(t("nav_mm",lang))
    st.markdown(t("mm_intro",lang))

    col_map, col_chart = st.columns([1.3,1])

    with col_map:
        st.markdown(f"##### {'% population à < 1 km d\'un agent MM par canton' if lang=='fr' else '% population within 1 km of MM agent by canton'}")
        choropleth("mm_1km_pct",
                   "% pop <1km MM",
                   colorscale="YlGn",
                   regions=sel_regions_eff, height=500)

    with col_chart:
        # Camembert opérateurs
        st.markdown(f"##### {'Agents par opérateur' if lang=='fr' else 'Agents by operator'}")
        if not mm_f.empty:
            op_c = mm_f["operateur"].value_counts().reset_index()
            op_c.columns = ["operateur","count"]
            fig = px.pie(op_c, names="operateur", values="count", hole=0.5,
                         color_discrete_sequence=[T["green"],T["yellow"],T["red"],"#7E57C2"])
            fig.update_layout(**PLOT_KW, height=240, showlegend=True,
                              legend=dict(orientation="h", y=-0.1))
            st.plotly_chart(fig, use_container_width=True)

        # Agents/10k par région
        has_pop = "agents_mm_pour_10k_hab" in agg_reg.columns \
                  and agg_reg["agents_mm_pour_10k_hab"].notna().any()
        if has_pop:
            st.markdown(f"##### {'Agents MM / 10 000 hab. par région' if lang=='fr' else 'MM agents / 10k inhab. by region'}")
            d = agg_reg.sort_values("agents_mm_pour_10k_hab")
            fig2 = px.bar(d, x="agents_mm_pour_10k_hab", y="region",
                          orientation="h",
                          color="agents_mm_pour_10k_hab",
                          color_continuous_scale=["#D21034",T["yellow"],T["green"]])
            fig2.update_layout(**PLOT_KW, height=240, coloraxis_showscale=False)
            st.plotly_chart(fig2, use_container_width=True)

        # Analyse dynamique
        nb_mm = len(mm_f)
        tot_pop = agg_reg["population"].sum() if not agg_reg.empty else 0
        rate = round(nb_mm/tot_pop*10000,1) if tot_pop else 0
        national_rate = round(kpis["nb_agents_mobile_money"]/kpis["population_totale"]*10000,1)
        mm1km_moy = round(ind_f["mm_1km_pct"].mean(),1) if not ind_f.empty else "—"
        gap_txt = above_txt = ""
        if has_pop:
            r = agg_reg.dropna(subset=["agents_mm_pour_10k_hab"]).sort_values("agents_mm_pour_10k_hab")
            if len(r)>1:
                ratio = round(r.iloc[-1]["agents_mm_pour_10k_hab"]/
                              max(r.iloc[0]["agents_mm_pour_10k_hab"],0.1),1)
                gap_txt = t("mm_gap_txt",lang).format(
                    min_reg=r.iloc[0]["region"], min_rate=r.iloc[0]["agents_mm_pour_10k_hab"],
                    max_reg=r.iloc[-1]["region"], max_rate=r.iloc[-1]["agents_mm_pour_10k_hab"],
                    ratio=ratio)
        analysis_box(t("mm_dynamic_insight",lang).format(
            rate=rate, national_rate=national_rate, nb_mm=nb_mm,
            gap_txt=gap_txt, above_national_txt=above_txt, mm1km_moy=mm1km_moy))

    how_to_read(t("mm_how_what",lang), t("mm_how_shows",lang))

# ══════════════════════════════════════════════════════
# PAGE : DENSITÉ vs INFRASTRUCTURES
# ══════════════════════════════════════════════════════
elif page == "density":
    header(t("nav_density",lang))
    st.markdown(t("density_intro",lang))
    st.info(t("density_gran_note",lang))

    no_ag_df  = agg_pref[agg_pref["nb_agences"]==0]
    no_ag_pop = no_ag_df["population"].sum()
    c1,c2 = st.columns(2)
    kpi_card(c1, f"{no_ag_pop:,.0f}".replace(",",""),
             t("no_agency_pop",lang), alert=True)
    kpi_card(c2, len(no_ag_df),
             t("gran_prefecture",lang)+" — 0 agences", alert=True)
    st.markdown("###")

    col_map, col_chart = st.columns([1.3,1])

    with col_map:
        st.markdown(f"##### {'Densité de population par canton (hab/km²)' if lang=='fr' else 'Population density by canton (pop/km²)'}")
        choropleth("densite_hab_km2",
                   "Densité hab/km²" if lang=="fr" else "Density pop/km²",
                   colorscale="OrRd",
                   regions=sel_regions_eff, height=500)

    with col_chart:
        st.markdown(f"##### {t('scatter_title',lang)}")
        if not agg_pref.empty:
            fig = px.scatter(agg_pref, x="population", y="nb_agences",
                size="nb_agents_mobile_money", color="region", hover_name="prefecture",
                size_max=45,
                color_discrete_sequence=[T["green"],T["yellow"],T["red"],"#1E88E5","#7A4FA0"])
            fig.update_layout(**PLOT_KW, height=480)
            st.plotly_chart(fig, use_container_width=True)
        how_to_read(t("scatter_how_what",lang), t("scatter_how_shows",lang))

    # Analyse dynamique
    n_pref = len(agg_pref); n_zero = len(no_ag_df)
    tot_pop = agg_pref["population"].sum() or 1
    pct_zero = round(no_ag_pop/tot_pop*100) if tot_pop else 0
    golfe = agg_pref[agg_pref["prefecture"]=="Golfe"]
    agoe  = agg_pref[agg_pref["prefecture"]=="Agoè-Nyivé"]
    nb_top2 = (golfe["nb_agences"].sum() if not golfe.empty else 0) + \
              (agoe["nb_agences"].sum()  if not agoe.empty else 0)
    pct_top2 = round(nb_top2/agg_pref["nb_agences"].sum()*100) \
               if agg_pref["nb_agences"].sum()>0 else 0
    ratio_golfe = (golfe["population"].iloc[0]/golfe["nb_agences"].iloc[0]
                   if not golfe.empty and golfe["nb_agences"].iloc[0]>0 else 0)
    ratio_nat = kpis["population_totale"]/kpis["nb_agences_total"] \
                if kpis["nb_agences_total"]>0 else 0
    pop_tand = agg_pref[agg_pref["prefecture"]=="Tandjoaré"]["population"].sum()
    pop_estm = agg_pref[agg_pref["prefecture"]=="Est-Mono"]["population"].sum()
    analysis_box(t("density_dynamic_insight",lang).format(
        n_pref=n_pref, n_zero=n_zero,
        pop_zero=f"{no_ag_pop:,.0f}".replace(",",""), pct_zero=pct_zero,
        pct_top2=pct_top2, ratio_golfe=ratio_golfe, ratio_national=ratio_nat,
        pop_tandjoare=f"{int(pop_tand):,}".replace(",","") if isinstance(pop_tand,(int,float)) else "—",
        pop_estmono=f"{int(pop_estm):,}".replace(",","") if isinstance(pop_estm,(int,float)) else "—"))

    st.subheader(t("table_density",lang))
    st.dataframe(agg_pref.sort_values("population",ascending=False),
                 use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════
# PAGE : COUVERTURE RÉSEAU
# ══════════════════════════════════════════════════════
elif page == "coverage":
    header(t("nav_coverage",lang))
    st.markdown(t("coverage_intro",lang))

    couv_sel = ind_f["couverture_mobile_pct"].dropna()
    mm1_sel  = ind_f["mm_1km_pct"].dropna()
    n_zb     = int((couv_sel<50).sum())
    n_zero   = int((couv_sel==0).sum())
    couv_moy = round(couv_sel.mean(),1) if len(couv_sel) else 0
    mm1_moy  = round(mm1_sel.mean(),1)  if len(mm1_sel)  else 0

    c1,c2,c3 = st.columns(3)
    kpi_card(c1, f"{couv_moy}%", t("kpi_couv_mobile",lang))
    kpi_card(c2, f"{n_zb} / {len(couv_sel)}", t("coverage_kpi_zb",lang), alert=True)
    kpi_card(c3, f"{mm1_moy}%", t("coverage_kpi_mm1",lang))
    st.markdown("###")

    tab_couv, tab_mm1 = st.tabs([
        "📶 Couverture mobile %" if lang=="fr" else "📶 Mobile coverage %",
        "📱 % pop < 1 km MM"
    ])

    with tab_couv:
        col_map, col_chart = st.columns([1.3,1])
        with col_map:
            st.markdown(f"##### {'Couverture réseau mobile par canton (PRISE 2021/2022)' if lang=='fr' else 'Mobile network coverage by canton (PRISE 2021/2022)'}")
            choropleth("couverture_mobile_pct",
                       "Couverture mobile %" if lang=="fr" else "Mobile coverage %",
                       colorscale="RdYlGn",
                       regions=sel_regions_eff, height=500)
        with col_chart:
            st.markdown(f"##### {'Par préfecture (moy. des cantons)' if lang=='fr' else 'By prefecture (canton avg.)'}")
            if not gp_f.empty and "couverture_mobile_moy" in gp_f.columns:
                d = gp_f.sort_values("couverture_mobile_moy")
                fig = px.bar(d, x="couverture_mobile_moy", y="prefecture",
                             orientation="h", color="couverture_mobile_moy",
                             color_continuous_scale=["#D21034","#FFCE00","#006A4E"],
                             range_color=[0,100],
                             hover_data={"region":True,"cantons_zone_blanche":True})
                fig.update_layout(**PLOT_KW, height=max(420,28*len(d)),
                                  coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)

    with tab_mm1:
        col_map2, col_chart2 = st.columns([1.3,1])
        with col_map2:
            st.markdown(f"##### {'% population à < 1 km d\'un agent MM par canton' if lang=='fr' else '% population within 1 km of MM agent by canton'}")
            choropleth("mm_1km_pct",
                       "% pop <1km MM",
                       colorscale="YlGn",
                       regions=sel_regions_eff, height=500)
        with col_chart2:
            st.markdown(f"##### {'Double vulnérabilité : faible couverture ET faible MM' if lang=='fr' else 'Double vulnerability: low coverage AND low MM'}")
            if not gp_f.empty:
                critique = gp_f[(gp_f["couverture_mobile_moy"]<60) &
                                (gp_f["mm_1km_pct_moy"]<45)]
                normale  = gp_f[~((gp_f["couverture_mobile_moy"]<60) &
                                  (gp_f["mm_1km_pct_moy"]<45))]
                fig3 = go.Figure()
                fig3.add_trace(go.Scatter(
                    x=normale["couverture_mobile_moy"], y=normale["mm_1km_pct_moy"],
                    mode="markers", name="Normale",
                    marker=dict(color=T["green"]+"99", size=9),
                    text=normale["prefecture"],
                    hovertemplate="<b>%{text}</b><br>Couv: %{x:.1f}%<br>MM<1km: %{y:.1f}%<extra></extra>"))
                fig3.add_trace(go.Scatter(
                    x=critique["couverture_mobile_moy"], y=critique["mm_1km_pct_moy"],
                    mode="markers+text", name="⚠️ Critique",
                    marker=dict(color="#D21034CC", size=12, symbol="diamond"),
                    text=critique["prefecture"], textposition="top center",
                    hovertemplate="<b>%{text}</b><br>Couv: %{x:.1f}%<br>MM<1km: %{y:.1f}%<extra></extra>"))
                fig3.update_layout(**PLOT_KW, height=450,
                    xaxis_title="Couverture mobile %",
                    yaxis_title="% pop <1km MM",
                    shapes=[
                        dict(type="line",x0=60,x1=60,y0=0,y1=100,
                             line=dict(color="#D21034",dash="dash",width=1)),
                        dict(type="line",x0=0,x1=100,y0=45,y1=45,
                             line=dict(color="#D21034",dash="dash",width=1)),
                    ])
                st.plotly_chart(fig3, use_container_width=True)

    how_to_read(t("coverage_how_what",lang), t("coverage_how_shows",lang))

    # Analyse dynamique
    pref_min_row = gp_f.loc[gp_f["couverture_mobile_moy"].idxmin()] \
                   if not gp_f.empty and "couverture_mobile_moy" in gp_f.columns else None
    pref_min = pref_min_row["prefecture"] if pref_min_row is not None else "—"
    couv_min = pref_min_row["couverture_mobile_moy"] if pref_min_row is not None else 0
    mm1_min  = pref_min_row.get("mm_1km_pct_moy",0) if pref_min_row is not None else 0

    couv_c = gr_f.loc[gr_f["region"]=="Centrale","couverture_mobile_moy"].values
    couv_m = gr_f.loc[gr_f["region"]=="Maritime","couverture_mobile_moy"].values
    region_insight = ""
    if len(couv_c) and len(couv_m) and couv_m[0]>0:
        region_insight = t("coverage_region_insight",lang).format(
            couv_centrale=couv_c[0], couv_maritime=couv_m[0],
            ratio=round(couv_m[0]/max(couv_c[0],0.1),1))

    analysis_box(t("coverage_dynamic_insight",lang).format(
        level=GRAN_LABEL.lower(), couv_moy=couv_moy, n_zb=n_zb, n_zero=n_zero,
        region_insight=region_insight, pref_min=pref_min,
        couv_min=couv_min, mm1km_min=mm1_min),
        style="alert" if n_zb>20 else "warn")

# ══════════════════════════════════════════════════════
# PAGE : SERVICES FINANCIERS
# ══════════════════════════════════════════════════════
elif page == "services":
    header(t("nav_services",lang))
    st.markdown(t("services_intro",lang))

    n_banques = int(ind_f["n_banques"].sum())
    n_mfi     = int(ind_f["n_mfi"].sum())
    n_poste   = int(ind_f["n_poste"].sum())
    n_distrib = int(ind_f["n_distributeurs"].sum())
    c1,c2,c3,c4 = st.columns(4)
    kpi_card(c1, n_banques, "Banques" if lang=="fr" else "Banks")
    kpi_card(c2, n_mfi,     "Microfinances")
    kpi_card(c3, n_poste,   "Points Poste")
    kpi_card(c4, n_distrib, "Distributeurs / ATM")
    st.markdown("###")

    tab_bank, tab_mfi = st.tabs([
        "🏦 Banques & distributeurs" if lang=="fr" else "🏦 Banks & ATMs",
        "🤝 Microfinance & Poste"
    ])

    with tab_bank:
        col_map, col_chart = st.columns([1.3,1])
        with col_map:
            st.markdown(f"##### {'Banques par canton' if lang=='fr' else 'Banks by canton'}")
            choropleth("n_banques",
                       "Nb banques" if lang=="fr" else "Nb banks",
                       colorscale="Blues",
                       regions=sel_regions_eff, height=500)
        with col_chart:
            if not gr_f.empty and "n_banques" in gr_f.columns:
                fig = px.bar(gr_f, x="region", y=["n_banques","n_distributeurs"],
                             barmode="group",
                             color_discrete_sequence=[T["green"],T["yellow"]])
                fig.update_layout(**PLOT_KW, height=400,
                                  legend=dict(orientation="h",y=1.05))
                st.plotly_chart(fig, use_container_width=True)

    with tab_mfi:
        col_map2, col_chart2 = st.columns([1.3,1])
        with col_map2:
            st.markdown(f"##### {'Microfinances par canton' if lang=='fr' else 'Microfinance by canton'}")
            choropleth("n_mfi",
                       "Nb microfinances",
                       colorscale="Greens",
                       regions=sel_regions_eff, height=500)
        with col_chart2:
            if not gr_f.empty and "n_mfi" in gr_f.columns:
                fig2 = px.bar(gr_f, x="region", y=["n_mfi","n_poste"],
                              barmode="group",
                              color_discrete_sequence=[T["green"],T["yellow"]])
                fig2.update_layout(**PLOT_KW, height=400,
                                   legend=dict(orientation="h",y=1.05))
                st.plotly_chart(fig2, use_container_width=True)

    # Analyse dynamique
    mar_b  = ind_canton[ind_canton["region"]=="Maritime"]["n_banques"].sum()
    mar_d  = ind_canton[ind_canton["region"]=="Maritime"]["n_distributeurs"].sum()
    tot_b  = ind_canton["n_banques"].sum()
    tot_d  = ind_canton["n_distributeurs"].sum()
    mfi_hm = int(ind_f[ind_f["region"]!="Maritime"]["n_mfi"].sum())
    tot_mfi= int(ind_canton["n_mfi"].sum())
    pct_mfi= round(mfi_hm/tot_mfi*100) if tot_mfi else 0

    analysis_box(t("services_dynamic_insight",lang).format(
        n_banques=n_banques, n_mfi=n_mfi, n_poste=n_poste, n_distrib=n_distrib,
        concentration_txt=t("services_concentration_txt",lang).format(
            pct_banques_maritime=round(mar_b/tot_b*100) if tot_b else 0,
            pct_distrib_maritime=round(mar_d/tot_d*100) if tot_d else 0),
        n_mfi_hors_maritime=mfi_hm, pct_mfi_hors=pct_mfi,
        n_distrib_maritime=int(mar_d), n_distrib_total=int(tot_d)))

    # Ratio services financiers / population par région
    if not agg_reg.empty and "population" in agg_reg.columns:
        st.markdown("###")
        st.markdown(f"##### {'Ratio services financiers pour 100 000 habitants' if lang=='fr' else 'Financial services per 100,000 inhabitants'}")
        merged = agg_reg.merge(gr_f[["region","n_banques","n_mfi","n_poste","n_distributeurs"]],
                               on="region", how="left")
        for col_s, lbl in [("n_banques","Banques"),("n_mfi","MFI"),
                            ("n_poste","Poste"),("n_distributeurs","ATM")]:
            if col_s in merged.columns:
                merged[col_s+"_100k"] = (merged[col_s]/merged["population"]*100000).round(1)
        ratio_cols = [c for c in merged.columns if c.endswith("_100k")]
        if ratio_cols:
            fig3 = go.Figure()
            colors_svc = [T["green"],T["yellow"],T["red"],"#7A4FA0"]
            for i,(col_s,lbl) in enumerate([("n_banques_100k","Banques"),
                                             ("n_mfi_100k","MFI"),
                                             ("n_poste_100k","Poste"),
                                             ("n_distributeurs_100k","ATM")]):
                if col_s in merged.columns:
                    fig3.add_trace(go.Bar(
                        x=merged["region"], y=merged[col_s],
                        name=lbl, marker_color=colors_svc[i], borderradius=4))
            fig3.update_layout(**PLOT_KW, height=360, barmode="group",
                               yaxis_title="Pour 100 000 hab.",
                               legend=dict(orientation="h",y=1.05))
            st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Détail par préfecture" if lang=="fr" else "Detail by prefecture")
    svc_cols = [c for c in ["region","prefecture","n_banques","n_mfi","n_poste",
                              "n_distributeurs","n_marches"] if c in gp_f.columns]
    st.dataframe(gp_f[svc_cols].sort_values("n_banques",ascending=False),
                 use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════
# PAGE : RECOMMANDATIONS
# ══════════════════════════════════════════════════════
elif page == "reco":
    header(t("nav_reco",lang))
    st.markdown(t("reco_intro",lang))
    st.markdown("###")

    recos = [(f"reco{i}_title", f"reco{i}_body") for i in range(1,9)]
    for title_k, body_k in recos:
        st.markdown(
            f'<div class="reco-card"><h4>{t(title_k,lang)}</h4>'
            f'<p>{t(body_k,lang)}</p></div>',
            unsafe_allow_html=True)

st.markdown("---")
st.caption(t("footer_note",lang))
