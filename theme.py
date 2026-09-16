# -*- coding: utf-8 -*-
THEMES = {
    "clair": {
        "bg": "#F7F8F5", "bg_secondary": "#FFFFFF",
        "sidebar_bg": "#0B3D2E", "sidebar_text": "#FFFFFF",
        "text": "#1A1A1A", "text_muted": "#5A5A5A",
        "card_bg": "#FFFFFF", "card_border": "#E0E0E0",
        "shadow": "rgba(0,0,0,0.08)",
        "green": "#006A4E", "green_dark": "#0B3D2E",
        "yellow": "#FFCE00", "red": "#D21034", "accent": "#006A4E",
        "map_style": "carto-positron", "plot_template": "plotly_white",
        "grid": "#E5E5E5",
    },
    "sombre": {
        "bg": "#0E1512", "bg_secondary": "#16201C",
        "sidebar_bg": "#081911", "sidebar_text": "#F0F0F0",
        "text": "#F0F0F0", "text_muted": "#A8B3AE",
        "card_bg": "#1B2621", "card_border": "#2B3A33",
        "shadow": "rgba(0,0,0,0.4)",
        "green": "#2FA57A", "green_dark": "#1B2621",
        "yellow": "#FFCE00", "red": "#FF5A6E", "accent": "#2FA57A",
        "map_style": "carto-darkmatter", "plot_template": "plotly_dark",
        "grid": "#2B3A33",
    },
}

def inject_css(theme):
    t = THEMES[theme]
    return f"""
    <style>
    .stApp {{ background-color: {t['bg']}; color: {t['text']}; }}
    section[data-testid="stSidebar"] {{ background-color: {t['sidebar_bg']}; }}
    section[data-testid="stSidebar"] * {{ color: {t['sidebar_text']} !important; }}
    section[data-testid="stSidebar"] div[data-baseweb="select"] *,
    section[data-testid="stSidebar"] div[data-baseweb="popover"] *,
    section[data-testid="stSidebar"] ul[role="listbox"] *,
    section[data-testid="stSidebar"] input {{ color: #1A1A1A !important; }}
    section[data-testid="stSidebar"] span[data-baseweb="tag"],
    section[data-testid="stSidebar"] span[data-baseweb="tag"] * {{ color: #FFFFFF !important; }}
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{ color: {t['sidebar_text']} !important; }}
    .kpi-card {{
        background-color: {t['card_bg']}; border: 1px solid {t['card_border']};
        border-radius: 12px; padding: 18px 16px;
        box-shadow: 0 3px 10px {t['shadow']}; text-align: center; height: 100%;
    }}
    .kpi-value {{ font-size: 1.9rem; font-weight: 800; color: {t['accent']}; margin: 4px 0; }}
    .kpi-value-alert {{ font-size: 1.9rem; font-weight: 800; color: {t['red']}; margin: 4px 0; }}
    .kpi-label {{ font-size: 0.82rem; color: {t['text_muted']}; text-transform: uppercase; letter-spacing: 0.03em; }}
    .insight-card {{
        background-color: {t['card_bg']}; border-left: 5px solid {t['green']};
        border-radius: 8px; padding: 14px 18px; margin: 10px 0;
        box-shadow: 0 2px 6px {t['shadow']};
    }}
    .insight-card-warn {{
        background-color: {t['card_bg']}; border-left: 5px solid {t['yellow']};
        border-radius: 8px; padding: 14px 18px; margin: 10px 0;
        box-shadow: 0 2px 6px {t['shadow']};
    }}
    .insight-card-alert {{
        background-color: {t['card_bg']}; border-left: 5px solid {t['red']};
        border-radius: 8px; padding: 14px 18px; margin: 10px 0;
        box-shadow: 0 2px 6px {t['shadow']};
    }}
    .reco-card {{
        background-color: {t['card_bg']}; border-top: 5px solid {t['yellow']};
        border-radius: 10px; padding: 16px 18px; margin: 8px 0;
        box-shadow: 0 3px 10px {t['shadow']}; height: 100%;
    }}
    .header-band {{
        background: linear-gradient(90deg, {t['green_dark']} 0%, {t['green']} 100%);
        padding: 18px 26px; border-radius: 12px; color: white !important;
        margin-bottom: 18px; display: flex; align-items: center;
    }}
    .header-band * {{ color: white !important; }}
    hr {{ border-color: {t['card_border']}; }}
    .stTabs [data-baseweb="tab"] {{ color: {t['text']}; }}
    </style>
    """
