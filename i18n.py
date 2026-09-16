# -*- coding: utf-8 -*-
TR = {
    # --- Général ---
    "republic_name":   {"fr": "République Togolaise", "en": "Republic of Togo"},
    "app_title":       {"fr": "Accès aux Télécoms & Services Numériques — Togo", "en": "Telecom & Digital Services Access — Togo"},
    "app_subtitle":    {"fr": "Diagnostic des infrastructures et recommandations stratégiques d'inclusion numérique", "en": "Infrastructure diagnostic and strategic digital inclusion recommendations"},
    "nav_title":       {"fr": "Navigation", "en": "Navigation"},
    "nav_overview":    {"fr": "🏠 Vue d'ensemble", "en": "🏠 Overview"},
    "nav_map":         {"fr": "🗼 Agences & Datacenters", "en": "🗼 Agencies & Datacenters"},
    "nav_mm":          {"fr": "📱 Mobile Money", "en": "📱 Mobile Money"},
    "nav_density":     {"fr": "👥 Densité vs Infrastructures", "en": "👥 Density vs Infrastructure"},
    "nav_coverage":    {"fr": "📶 Couverture réseau", "en": "📶 Network Coverage"},
    "nav_services":    {"fr": "🏦 Services financiers", "en": "🏦 Financial Services"},
    "nav_reco":        {"fr": "🎯 Recommandations", "en": "🎯 Recommendations"},
    "theme_light":     {"fr": "Clair", "en": "Light"},
    "theme_dark":      {"fr": "Sombre", "en": "Dark"},
    "filters":         {"fr": "Filtres", "en": "Filters"},
    "granularity":     {"fr": "Granularité géographique", "en": "Geographic granularity"},
    "gran_region":     {"fr": "Région", "en": "Region"},
    "gran_prefecture": {"fr": "Préfecture", "en": "Prefecture"},
    "gran_commune":    {"fr": "Commune", "en": "Commune"},
    "gran_canton":     {"fr": "Canton", "en": "Canton"},
    "region_filter":   {"fr": "Région(s)", "en": "Region(s)"},
    "operator_filter": {"fr": "Opérateur(s)", "en": "Operator(s)"},
    "operators_all":   {"fr": "tous", "en": "all"},
    "all":             {"fr": "Toutes", "en": "All"},
    "how_to_read":     {"fr": "❓ Comment lire ce graphique", "en": "❓ How to read this chart"},
    "what_it_is":      {"fr": "De quoi il s'agit", "en": "What this is"},
    "what_it_shows":   {"fr": "Ce que ça montre", "en": "What it shows"},
    "source":          {"fr": "Source", "en": "Source"},
    "source_note":     {"fr": "Sources : Géoportail Togo (api.geodata.gouv.tg) — Campagne PRISE 2021/2022 · RGPH-5 INSEED 2022.", "en": "Sources: Togo Geoportal (api.geodata.gouv.tg) — PRISE Campaign 2021/2022 · RGPH-5 INSEED 2022."},
    "author":          {"fr": "Auteur : AZIAGBEDO KOKOU SODJINE — Data & IA", "en": "Author: AZIAGBEDO KOKOU SODJINE — Data & AI"},
    "table_title_dynamic": {"fr": "Tableau — {level}", "en": "Table — {level}"},

    # --- Overview ---
    "ov_welcome": {
        "fr": "Ce tableau de bord dresse un diagnostic complet de l'accès aux télécommunications et services numériques au Togo, à partir des données ouvertes du Géoportail national (api.geodata.gouv.tg). Utilisez les filtres de la barre latérale pour explorer par région, opérateur et granularité.",
        "en": "This dashboard provides a comprehensive diagnostic of access to telecommunications and digital services in Togo, based on open data from the national Geoportal (api.geodata.gouv.tg). Use the sidebar filters to explore by region, operator and granularity.",
    },
    "kpi_population":         {"fr": "Population totale (RGPH-5)", "en": "Total population (census)"},
    "kpi_agences":            {"fr": "Agences Moov + Togocom", "en": "Moov + Togocom agencies"},
    "kpi_datacenters":        {"fr": "Datacenters", "en": "Datacenters"},
    "kpi_mm":                 {"fr": "Agents mobile money", "en": "Mobile money agents"},
    "kpi_couv_mobile":        {"fr": "Couverture mobile nationale (moy. cantons)", "en": "National mobile coverage (canton avg.)"},
    "kpi_mm_1km":             {"fr": "Pop. à < 1 km d'un agent MM (moy. cantons)", "en": "Pop. within 1 km of MM agent (canton avg.)"},
    "kpi_zones_blanches":     {"fr": "Cantons en zone blanche (couv. < 50%)", "en": "Cantons with low coverage (< 50%)"},
    "kpi_cantons_sans_agence":{"fr": "Cantons sans agence opérateur", "en": "Cantons without operator agency"},
    "ov_findings_title":      {"fr": "Les 5 constats analytiques majeurs", "en": "5 major analytical findings"},

    "ov_f1": {
        "fr": "🔴 <b>Fracture régionale : la Centrale à 42% de couverture mobile</b> — L'indicateur géoportail (Campagne PRISE) révèle que la région Centrale n'est couverte par un réseau mobile qu'à <b>42%</b> de ses cantons en moyenne, contre <b>96%</b> pour la Maritime. 33 de ses 64 cantons sont en zone blanche (couverture < 50%).",
        "en": "🔴 <b>Regional divide: Centrale at 42% mobile coverage</b> — The geoportal indicator (PRISE Campaign) reveals that the Centrale region has mobile network coverage in only <b>42%</b> of its cantons on average, versus <b>96%</b> for Maritime. 33 of its 64 cantons are in a dead zone (coverage < 50%).",
    },
    "ov_f2": {
        "fr": "🟡 <b>75 cantons en zone blanche, 41 à couverture nulle</b> — Sur 384 cantons analysés, <b>75 (19,5%)</b> ont une couverture réseau mobile inférieure à 50% et <b>41 cantons</b> sont entièrement non desservis (0%). Ces zones se concentrent en Centrale, Kara et Savanes.",
        "en": "🟡 <b>75 cantons in dead zones, 41 with zero coverage</b> — Of 384 cantons analysed, <b>75 (19.5%)</b> have mobile network coverage below 50% and <b>41 cantons</b> are entirely unserved (0%). These areas are concentrated in Centrale, Kara and Savanes.",
    },
    "ov_f3": {
        "fr": "🟡 <b>Le mobile money compense partiellement : 55% de la population à < 1 km d'un agent</b> — En moyenne nationale par canton, <b>55,2%</b> de la population réside à moins d'1 km d'un agent mobile money. Ce taux tombe à <b>45%</b> en Centrale et <b>44%</b> aux Savanes, révélant un double déficit réseau + service.",
        "en": "🟡 <b>Mobile money partially compensates: 55% of population within 1 km of an agent</b> — On national average by canton, <b>55.2%</b> of the population lives within 1 km of a mobile money agent. This rate drops to <b>45%</b> in Centrale and <b>44%</b> in Savanes, revealing a double network + service deficit.",
    },
    "ov_f4": {
        "fr": "🔴 <b>Hyperconcentration des infrastructures formelles à Lomé</b> — Les 3 datacenters sont tous dans la préfecture du Golfe. La Maritime concentre <b>57%</b> des agences opérateurs, <b>60%</b> des banques et <b>52%</b> des microfinances du pays, pour 44% de la population nationale.",
        "en": "🔴 <b>Hyperconcentration of formal infrastructure in Lomé</b> — All 3 datacenters are in Golfe prefecture. Maritime concentrates <b>57%</b> of operator agencies, <b>60%</b> of banks and <b>52%</b> of microfinance institutions nationwide, for 44% of the national population.",
    },
    "ov_f5": {
        "fr": "🟢 <b>Le mobile money est le réseau le plus décentralisé : présent dans 100% des cantons</b> — Avec 19 788 agents répartis sur l'ensemble des cantons, le mobile money constitue l'infrastructure numérique la plus équitablement distribuée. Cependant, le taux d'agents pour 10 000 habitants varie de <b>4,6 à Kpendjal</b> à <b>39 au Golfe</b>, signalant des disparités d'intensité à corriger.",
        "en": "🟢 <b>Mobile money is the most decentralised network: present in 100% of cantons</b> — With 19,788 agents spread across all cantons, mobile money is the most equitably distributed digital infrastructure. However, the rate of agents per 10,000 inhabitants ranges from <b>4.6 in Kpendjal</b> to <b>39 in Golfe</b>, signalling intensity disparities to address.",
    },

    # --- Map ---
    "map_intro": {
        "fr": "Chaque point représente une agence (Moov ou Togocom) ou un datacenter. Les données ouvertes ne contiennent aucune agence CANAL+ géoréférencée : selon le site officiel CANAL+ Togo, 859 boutiques existent mais ne sont pas encore dans les données ouvertes. Utilisez les filtres pour explorer par région/opérateur.",
        "en": "Each point represents an agency (Moov or Togocom) or a datacenter. Open data contains no geo-referenced CANAL+ agency: according to the official CANAL+ Togo website, 859 stores exist but are not yet in open data. Use filters to explore by region/operator.",
    },
    "map_how_what":  {"fr": "Carte de points géolocalisés des agences Moov (bleu), Togocom (orange) et des datacenters (étoile rouge).", "en": "Geolocated point map of Moov (blue), Togocom (orange) agencies and datacenters (red star)."},
    "map_how_shows": {"fr": "La concentration des agences autour de Lomé, contrastant avec la rareté des points au Nord.", "en": "Agency concentration around Lomé, contrasting with sparse coverage in the North."},
    "map_dynamic_insight": {
        "fr": "**Analyse** — Sélection : {regions} · {ops} · **{nb_ag} agences** ({nb_moov} Moov + {nb_togocom} Togocom) · **{nb_dc} datacenter(s)** sur {n_units} {level}(s). {concentration} Les préfectures de **Kpendjal, Kpendjal-Ouest, Binah, Mô, Akébou et Tandjoaré** ne comptent aucune agence Moov/Togocom dans les données ouvertes — représentant collectivement plus de **700 000 habitants** sans point de service physique opérateur.",
        "en": "**Analysis** — Selection: {regions} · {ops} · **{nb_ag} agencies** ({nb_moov} Moov + {nb_togocom} Togocom) · **{nb_dc} datacenter(s)** across {n_units} {level}(s). {concentration} Prefectures of **Kpendjal, Kpendjal-Ouest, Binah, Mô, Akébou and Tandjoaré** have no Moov/Togocom agency in open data — collectively representing over **700,000 inhabitants** with no physical operator service point.",
    },
    "map_concentration_txt": {
        "fr": "La région **{top_region}** concentre **{top_pct}%** des agences sélectionnées. ",
        "en": "The **{top_region}** region accounts for **{top_pct}%** of selected agencies. ",
    },
    "table_title_dynamic": {"fr": "Agences, agents MM et datacenters — {level}", "en": "Agencies, MM agents and datacenters — {level}"},

    # --- Mobile money ---
    "mm_intro": {
        "fr": "Le mobile money est le canal numérique le plus décentralisé du pays. Cette section évalue son adéquation démographique et sa distribution entre territoires.",
        "en": "Mobile money is the country's most decentralised digital channel. This section assesses its demographic fit and distribution across territories.",
    },
    "mm_by_operator":    {"fr": "Répartition des agents par opérateur pris en charge", "en": "Distribution of agents by supported operator"},
    "mm_rate_title":     {"fr": "Agents mobile money pour 10 000 habitants, par {level}", "en": "Mobile money agents per 10,000 inhabitants, by {level}"},
    "mm_how_what":       {"fr": "Diagramme circulaire (opérateurs) et barres horizontales (taux agents/10 000 hab. par unité géographique).", "en": "Pie chart (operators) and horizontal bars (agent rate per 10,000 inhabitants by geographic unit)."},
    "mm_how_shows":      {"fr": "Les unités où le taux est le plus faible relativement à leur population — cibles prioritaires pour renforcer le réseau d'agents.", "en": "Units with the lowest coverage rate relative to population — priority targets for agent network reinforcement."},
    "mm_no_pop_note":    {"fr": "ℹ️ La population est connue au niveau **préfecture** et **région** uniquement (RGPH-5). Au niveau {level}, le graphique affiche un **nombre brut d'agents**.", "en": "ℹ️ Population is known at **prefecture** and **region** level only (census). At {level} level, the chart shows a **raw agent count**."},
    "mm_raw_count_title":{"fr": "Nombre d'agents mobile money par {level} (top 20)", "en": "Mobile money agents by {level} (top 20)"},
    "mm_dynamic_insight": {
        "fr": "**Analyse** — Sélection : **{nb_mm} agents** · taux moyen {rate}/10 000 hab. (national : **{national_rate}**). {gap_txt}{above_national_txt} L'indicateur géoportail confirme que **{mm1km_moy}%** de la population (moy. par canton) réside à moins d'1 km d'un agent MM sur la sélection — mais ce taux cache des zones à **moins de 30%** dans les préfectures de Blitta, Kéran et Kpendjal.",
        "en": "**Analysis** — Selection: **{nb_mm} agents** · average rate {rate}/10,000 inhab. (national: **{national_rate}**). {gap_txt}{above_national_txt} The geoportal indicator confirms that **{mm1km_moy}%** of the population (canton avg.) lives within 1 km of an MM agent in this selection — but this rate hides areas at **less than 30%** in Blitta, Kéran and Kpendjal prefectures.",
    },
    "mm_gap_txt": {
        "fr": "L'écart entre **{min_reg}** ({min_rate}/10k) et **{max_reg}** ({max_rate}/10k) représente un rapport de **{ratio}x** — déséquilibre structurel entre territoires. ",
        "en": "The gap between **{min_reg}** ({min_rate}/10k) and **{max_reg}** ({max_rate}/10k) represents a ratio of **{ratio}x** — a structural imbalance between territories. ",
    },
    "mm_above_national_txt": {
        "fr": "**{pct}% des {level}s** de la sélection atteignent ou dépassent la moyenne nationale ({national_rate}/10k). ",
        "en": "**{pct}% of {level}s** in the selection reach or exceed the national average ({national_rate}/10k). ",
    },

    # --- Density ---
    "density_intro": {
        "fr": "Cette analyse croise la population par préfecture (RGPH-5, 2022) avec le nombre d'agences et d'agents mobile money, pour identifier les zones sur- ou sous-équipées relativement à leur poids démographique.",
        "en": "This analysis cross-references prefecture population (RGPH-5, 2022) with the number of agencies and mobile money agents, to identify areas over- or under-equipped relative to their demographic weight.",
    },
    "density_gran_note": {"fr": "ℹ️ Cette page utilise toujours le niveau **préfecture** (seul niveau infra-régional où la population RGPH-5 est disponible).", "en": "ℹ️ This page always uses the **prefecture** level (the only sub-regional level where RGPH-5 population is available)."},
    "scatter_title":    {"fr": "Population vs nombre d'agences par préfecture", "en": "Population vs number of agencies by prefecture"},
    "scatter_how_what": {"fr": "Nuage de points : population (X) vs agences (Y), taille bulle = agents MM.", "en": "Scatter plot: population (X) vs agencies (Y), bubble size = MM agents."},
    "scatter_how_shows":{"fr": "Les préfectures en bas à droite (population élevée, peu d'agences) sont les plus sous-dotées.", "en": "Prefectures bottom-right (high population, few agencies) are the most under-served."},
    "no_agency_pop":    {"fr": "Population dans une préfecture sans aucune agence opérateur", "en": "Population in prefectures with no operator agency"},
    "table_density":    {"fr": "Tableau détaillé par préfecture", "en": "Detailed table by prefecture"},
    "density_dynamic_insight": {
        "fr": "**Analyse** — Sur **{n_pref} préfectures**, **{n_zero} n'ont aucune agence** opérateur Moov/Togocom dans les données ouvertes, représentant **{pop_zero} habitants** ({pct_zero}% de la population sélectionnée). Les préfectures du **Golfe et d'Agoè-Nyivé** concentrent à elles seules **{pct_top2}%** des agences, avec un ratio de **{ratio_golfe:.0f} habitants par agence** au Golfe contre une moyenne nationale de **{ratio_national:.0f}**. Parmi les préfectures sans agence, **Tandjoaré** ({pop_tandjoare} hab.) et **Est-Mono** ({pop_estmono} hab.) cumulent les plus fortes populations non desservies par un point physique opérateur.",
        "en": "**Analysis** — Of **{n_pref} prefectures**, **{n_zero} have no operator agency** (Moov/Togocom in open data), representing **{pop_zero} inhabitants** ({pct_zero}% of selected population). **Golfe and Agoè-Nyivé** alone concentrate **{pct_top2}%** of agencies, with a ratio of **{ratio_golfe:.0f} inhabitants per agency** in Golfe vs. a national average of **{ratio_national:.0f}**. Among agencyless prefectures, **Tandjoaré** ({pop_tandjoare} inhab.) and **Est-Mono** ({pop_estmono} inhab.) have the largest populations without a physical operator service point.",
    },

    # --- Coverage ---
    "coverage_intro": {
        "fr": "Cette page utilise les **indicateurs réels de couverture réseau mobile** issus de la campagne PRISE 2021/2022 du Géoportail national — une mesure directe, canton par canton, qui remplace avantageusement le proxy agents mobile money utilisé faute de données dans les versions précédentes.",
        "en": "This page uses **real mobile network coverage indicators** from the PRISE 2021/2022 campaign of the national Geoportal — a direct canton-by-canton measurement that advantageously replaces the mobile money agent proxy used previously due to lack of data.",
    },
    "coverage_kpi_zb":   {"fr": "Cantons zone blanche (couv. < 50%)", "en": "Dead zone cantons (coverage < 50%)"},
    "coverage_kpi_zero": {"fr": "Cantons à couverture 0%", "en": "Cantons at 0% coverage"},
    "coverage_kpi_mm1":  {"fr": "Pop. moy. à < 1 km d'un agent MM", "en": "Avg. pop. within 1 km of MM agent"},
    "coverage_map_title":{"fr": "Couverture réseau mobile par canton (PRISE 2021/2022)", "en": "Mobile network coverage by canton (PRISE 2021/2022)"},
    "coverage_how_what": {"fr": "Carte de points par centroïde de canton, colorés selon le % de couverture réseau mobile (vert=bonne, rouge=faible).", "en": "Point map by canton centroid, colored by mobile network coverage % (green=good, red=low)."},
    "coverage_how_shows":{"fr": "Les zones en rouge/orange correspondent aux cantons les moins couverts — cibles prioritaires pour l'extension réseau.", "en": "Red/orange zones are the least covered cantons — priority targets for network expansion."},
    "coverage_dynamic_insight": {
        "fr": "**Analyse** — Sélection à la granularité **{level}** : couverture mobile moyenne **{couv_moy:.1f}%** · {n_zb} zone(s) blanche(s) (< 50%) · {n_zero} canton(s) à 0%. {region_insight} La préfecture la moins couverte est **{pref_min}** ({couv_min:.0f}%), qui cumule une couverture réseau quasi-nulle ET un accès MM limité à {mm1km_min:.0f}% de sa population à moins d'1 km — situation de double exclusion numérique nécessitant une intervention prioritaire.",
        "en": "**Analysis** — Selection at **{level}** granularity: average mobile coverage **{couv_moy:.1f}%** · {n_zb} dead zone(s) (< 50%) · {n_zero} canton(s) at 0%. {region_insight} The least covered prefecture is **{pref_min}** ({couv_min:.0f}%), which combines near-zero network coverage AND limited MM access (only {mm1km_min:.0f}% of population within 1 km) — a dual digital exclusion situation requiring priority intervention.",
    },
    "coverage_region_insight": {
        "fr": "La région **Centrale** est la plus vulnérable avec seulement **{couv_centrale:.0f}%** de couverture mobile moyenne — soit **{ratio:.1f}x moins** que la Maritime ({couv_maritime:.0f}%). ",
        "en": "The **Centrale** region is the most vulnerable with only **{couv_centrale:.0f}%** average mobile coverage — **{ratio:.1f}x less** than Maritime ({couv_maritime:.0f}%). ",
    },

    # --- Services financiers ---
    "services_intro": {
        "fr": "Cette page analyse la répartition des infrastructures de services financiers formels et semi-formels (banques, microfinances, postes, distributeurs automatiques), issues des données ouvertes du Géoportail national.",
        "en": "This page analyses the distribution of formal and semi-formal financial service infrastructures (banks, microfinance, post offices, ATMs), from national Geoportal open data.",
    },
    "services_dynamic_insight": {
        "fr": "**Analyse** — Sélection : **{n_banques} banque(s)** · **{n_mfi} microfinance(s)** · **{n_poste} bureau(x) de poste** · **{n_distrib} distributeur(s)**. {concentration_txt} Le réseau de microfinance est le plus décentralisé avec **{n_mfi_hors_maritime} établissements hors région Maritime** ({pct_mfi_hors:.0f}% du total national). Les distributeurs automatiques sont quasi-absents en dehors du Grand-Lomé (**{n_distrib_maritime} sur {n_distrib_total}** se trouvent en Maritime), confirmant la fracture d'accès aux espèces électroniques entre Lomé et le reste du pays.",
        "en": "**Analysis** — Selection: **{n_banques} bank(s)** · **{n_mfi} microfinance(s)** · **{n_poste} post office(s)** · **{n_distrib} ATM(s)**. {concentration_txt} The microfinance network is the most decentralised with **{n_mfi_hors_maritime} establishments outside the Maritime region** ({pct_mfi_hors:.0f}% of national total). ATMs are nearly absent outside Greater Lomé (**{n_distrib_maritime} of {n_distrib_total}** are in Maritime), confirming the cash access divide between Lomé and the rest of the country.",
    },
    "services_concentration_txt": {
        "fr": "La Maritime concentre **{pct_banques_maritime:.0f}%** des banques et **{pct_distrib_maritime:.0f}%** des distributeurs nationaux. ",
        "en": "Maritime concentrates **{pct_banques_maritime:.0f}%** of banks and **{pct_distrib_maritime:.0f}%** of national ATMs. ",
    },

    # --- Recommandations ---
    "reco_intro": {
        "fr": "8 recommandations stratégiques fondées sur le diagnostic quantitatif, priorisées par impact sur l'inclusion numérique et faisabilité opérationnelle.",
        "en": "8 strategic recommendations based on quantitative diagnostic, prioritised by digital inclusion impact and operational feasibility.",
    },
    "reco1_title": {"fr": "1. Déployer d'urgence des agences dans les 6 préfectures à zéro présence opérateur", "en": "1. Urgently deploy agencies in the 6 prefectures with zero operator presence"},
    "reco1_body":  {"fr": "Ouvrir au minimum une agence dans chacune des 6 préfectures sans agence Moov/Togocom (Tandjoaré 163k hab., Est-Mono 192k, Kpendjal-Ouest 105k, Binah 77k, Mô 13k, Akébou 74k). Prioriser Tandjoaré et Est-Mono (Savanes/Plateaux) pour leur poids démographique — 355 000 habitants sans point de service physique opérateur.", "en": "Open at least one agency in each of the 6 prefectures without Moov/Togocom agency (Tandjoaré 163k inhab., Est-Mono 192k, Kpendjal-Ouest 105k, Binah 77k, Mô 13k, Akébou 74k). Prioritise Tandjoaré and Est-Mono (Savanes/Plateaux) for their demographic weight — 355,000 inhabitants with no physical operator service point."},
    "reco2_title": {"fr": "2. Cibler les 41 cantons à couverture 0% pour le déploiement réseau 4G", "en": "2. Target the 41 zero-coverage cantons for 4G network deployment"},
    "reco2_body":  {"fr": "Les 41 cantons à couverture mobile nulle (données PRISE géoportail), concentrés en Centrale (Tchamba, Blitta) et Kara (Kéran), doivent être intégrés en priorité dans les plans de déploiement réseau des opérateurs et dans les obligations de couverture définies par l'ARCEP Togo. Viser 100% de couverture 4G nationale à horizon 2030.", "en": "The 41 cantons with zero mobile coverage (PRISE geoportal data), concentrated in Centrale (Tchamba, Blitta) and Kara (Kéran), must be prioritised in operator network deployment plans and ARCEP Togo coverage obligations. Target 100% national 4G coverage by 2030."},
    "reco3_title": {"fr": "3. Intensifier le réseau d'agents MM dans les préfectures sous la moyenne nationale", "en": "3. Intensify MM agent network in prefectures below the national average"},
    "reco3_body":  {"fr": "Lancer une campagne de recrutement d'agents mobile money dans les préfectures dont le taux est inférieur à la moyenne nationale (24,4/10k hab.) : Kpendjal (4,6), Blitta (5,5), Mô (6,0), Moyen-Mono (8,9), Yoto (9,1). Objectif : ramener ces préfectures à 15/10k comme étape intermédiaire, en ciblant prioritairement les marchés hebdomadaires (1 078 répertoriés) comme sites d'implantation.", "en": "Launch a mobile money agent recruitment campaign in prefectures below the national average (24.4/10k inhab.): Kpendjal (4.6), Blitta (5.5), Mô (6.0), Moyen-Mono (8.9), Yoto (9.1). Target: bring these prefectures to 15/10k as an intermediate step, prioritising weekly markets (1,078 identified) as deployment sites."},
    "reco4_title": {"fr": "4. Décentraliser les datacenters : ouvrir un site secondaire au Nord", "en": "4. Decentralise datacenters: open a secondary site in the North"},
    "reco4_body":  {"fr": "Les 3 datacenters nationaux sont tous dans la préfecture du Golfe. Implanter un datacenter régional à Kara ou Sokodé pour réduire la latence des services numériques au Nord, sécuriser la continuité nationale en cas d'incident à Lomé, et soutenir les initiatives d'administration numérique dans les régions Centrale, Kara et Savanes.", "en": "All 3 national datacenters are in Golfe prefecture. Establish a regional datacenter in Kara or Sokodé to reduce digital service latency in the North, secure national continuity in case of a Lomé incident, and support digital government initiatives in Centrale, Kara and Savanes."},
    "reco5_title": {"fr": "5. Étendre la microfinance et les services Poste dans les zones sans banques", "en": "5. Expand microfinance and Post services in bankless areas"},
    "reco5_body":  {"fr": "Les régions Centrale, Kara et Savanes totalisent seulement 72 banques sur 237 nationales (30%) pour 36% de la population. La microfinance (401 établissements, mieux répartis) et le réseau Poste (95 points) constituent des alternatives crédibles : les renforcer et les connecter aux services mobiles (paiement, épargne) pour pallier l'absence des banques commerciales.", "en": "Centrale, Kara and Savanes regions total only 72 banks out of 237 nationally (30%) for 36% of the population. Microfinance (401 institutions, better distributed) and Post network (95 points) are credible alternatives: strengthen them and connect them to mobile services (payments, savings) to compensate for the absence of commercial banks."},
    "reco6_title": {"fr": "6. Mettre à jour les données ouvertes télécom en continu", "en": "6. Continuously update open telecom data"},
    "reco6_body":  {"fr": "Actualiser le géoportail avec les 859 boutiques CANAL+, les franchises Moov/Yas non encore géoréférencées, et les nouvelles agences ouvertes depuis la campagne PRISE 2021/2022. Établir un protocole de mise à jour trimestrielle entre l'ARCEP, le MPIN et les opérateurs pour garantir la fiabilité des données pour les décisions publiques.", "en": "Update the geoportal with the 859 CANAL+ stores, non-yet geo-referenced Moov/Yas franchises, and new agencies opened since the PRISE 2021/2022 campaign. Establish a quarterly update protocol between ARCEP, MPIN and operators to ensure data reliability for public decisions."},
    "reco7_title": {"fr": "7. Publier des données de couverture réseau en open data", "en": "7. Publish network coverage data as open data"},
    "reco7_body":  {"fr": "Les indicateurs PRISE 2021/2022 du géoportail constituent un socle. Les compléter avec des données temps réel de couverture 2G/3G/4G/5G publiées par les opérateurs sous supervision ARCEP, en partenariat avec des initiatives internationales comme GSMA et ITU. Une carte de couverture actualisée est le prérequis pour mesurer précisément les progrès d'inclusion numérique.", "en": "The PRISE 2021/2022 geoportal indicators are a foundation. Complement them with real-time 2G/3G/4G/5G coverage data published by operators under ARCEP supervision, in partnership with international initiatives like GSMA and ITU. An up-to-date coverage map is the prerequisite for accurately measuring digital inclusion progress."},
    "reco8_title": {"fr": "8. Créer un indice composite d'inclusion numérique par préfecture", "en": "8. Create a composite digital inclusion index by prefecture"},
    "reco8_body":  {"fr": "Consolider les indicateurs disponibles (couverture mobile, accès MM, présence banque/MFI, population par agent) en un indice composite d'inclusion numérique publié annuellement par préfecture. Cet indice permettrait de prioriser les investissements publics, de suivre les progrès dans le temps, et d'alimenter les rapports ARCEP et les plans nationaux de développement numérique.", "en": "Consolidate available indicators (mobile coverage, MM access, bank/MFI presence, population per agent) into a composite digital inclusion index published annually by prefecture. This index would prioritise public investments, track progress over time, and feed ARCEP reports and national digital development plans."},

    "footer_note": {"fr": "Dashboard · Challenge Économie Numérique — Défi 1 · République Togolaise · Septembre 2026", "en": "Dashboard · Digital Economy Challenge — Challenge 1 · Republic of Togo · September 2026"},
}

def t(key, lang="fr"):
    entry = TR.get(key)
    if entry is None:
        return key
    return entry.get(lang, entry.get("fr", key))
