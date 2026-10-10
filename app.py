import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import unicodedata
import re
import html
import glob
import os


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Yaya's Rating",
    page_icon="🏀",
    layout="wide"
)

# =========================================================
# GOOGLE ANALYTICS
# =========================================================

components.html("""
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-94WZ8E7BME"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-94WZ8E7BME', {
            page_title: document.title,
            page_location: window.location.href
        });
    </script>
""", height=0)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
<style>

/* ==============================
   GLOBAL
============================== */

.stApp {
    background:
        radial-gradient(circle at 20% 10%, rgba(0, 255, 140, 0.12), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(0, 255, 120, 0.07), transparent 25%),
        linear-gradient(180deg, #07110d 0%, #050806 45%, #020403 100%);
    color: #ffffff;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.3rem;
    padding-bottom: 4rem;
}

h1, h2, h3, h4, p, div, span {
    font-family: Arial, Helvetica, sans-serif;
}

hr {
    border-color: rgba(255,255,255,0.08);
}


/* ==============================
   HERO
============================== */

.yaya-hero {
    position: relative;
    overflow: hidden;
    min-height: 360px;
    border-radius: 30px;
    border: 1px solid rgba(45,255,151,0.24);
    padding: 60px 60px 50px 60px;
    margin-bottom: 25px;

    background:
        radial-gradient(circle at 22% 35%, rgba(0,255,140,0.18), transparent 25%),
        radial-gradient(circle at 77% 35%, rgba(0,255,140,0.10), transparent 26%),
        linear-gradient(115deg, rgba(5,19,13,0.98) 0%, rgba(3,10,7,0.98) 55%, rgba(0,0,0,0.98) 100%);

    box-shadow:
        0 30px 80px rgba(0,0,0,0.45),
        inset 0 0 80px rgba(0,255,120,0.03);
}

.yaya-hero::before {
    content: "";
    position: absolute;
    width: 520px;
    height: 520px;
    border: 2px solid rgba(45,255,151,0.10);
    border-radius: 50%;
    right: 120px;
    bottom: -360px;
}

.yaya-hero::after {
    content: "";
    position: absolute;
    width: 300px;
    height: 300px;
    border: 2px solid rgba(45,255,151,0.08);
    border-radius: 50%;
    right: 230px;
    bottom: -210px;
}

.hero-content {
    position: relative;
    z-index: 3;
    max-width: 900px;
}

.hero-kicker {
    color: #35ff98;
    font-weight: 800;
    font-size: 15px;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 14px;
}

.hero-title {
    color: #ffffff;
    font-size: 74px;
    line-height: 0.95;
    font-weight: 950;
    letter-spacing: -4px;
    margin-bottom: 22px;
}

.hero-title span {
    color: #35ff98;
    text-shadow: 0 0 30px rgba(53,255,152,0.22);
}

.hero-subtitle {
    color: #f1f6f3;
    font-weight: 700;
    font-size: 21px;
    line-height: 1.45;
    max-width: 830px;
    margin-bottom: 15px;
}

.hero-description {
    color: #aab8b0;
    font-size: 15px;
    line-height: 1.65;
    max-width: 850px;
}

.hero-side-text {
    position: absolute;
    right: 28px;
    top: 42px;
    writing-mode: vertical-rl;
    transform: rotate(180deg);
    font-weight: 900;
    letter-spacing: 5px;
    color: rgba(255,255,255,0.11);
    font-size: 18px;
    z-index: 2;
}


/* ==============================
   INFO / WARNING
============================== */

.info-box {
    background: linear-gradient(90deg, rgba(255,196,0,0.09), rgba(255,196,0,0.025));
    border: 1px solid rgba(255,204,0,0.26);
    border-left: 4px solid #ffc928;
    border-radius: 13px;
    padding: 14px 18px;
    color: #ffe99a;
    margin: 10px 0 25px 0;
    font-size: 14px;
}

.rookie-warning {
    background: linear-gradient(90deg, rgba(255,196,0,0.11), rgba(255,196,0,0.035));
    border: 1px solid rgba(255,204,0,0.30);
    border-left: 4px solid #ffc928;
    border-radius: 12px;
    padding: 11px 14px;
    color: #ffe48a;
    margin-top: -10px;
    margin-bottom: 20px;
    font-size: 13px;
    font-weight: 750;
}


/* ==============================
   TABS - BIG + CENTERED
============================== */

div[data-baseweb="tab-list"] {
    justify-content: center !important;
    gap: 28px !important;
    background: transparent !important;
    margin-top: 20px;
    margin-bottom: 30px;
}

button[data-baseweb="tab"] {
    height: 105px !important;
    width: 46% !important;
    max-width: 620px !important;
    min-width: 360px !important;

    border-radius: 22px !important;
    border: 1px solid rgba(53,255,152,0.20) !important;

    background:
        linear-gradient(135deg, rgba(18,42,30,0.98), rgba(5,14,10,0.98)) !important;

    box-shadow:
        0 15px 35px rgba(0,0,0,0.26),
        inset 0 0 24px rgba(53,255,152,0.025);

    transition: all 0.2s ease;
}

button[data-baseweb="tab"]:hover {
    border-color: rgba(53,255,152,0.65) !important;
    transform: translateY(-2px);
}

button[data-baseweb="tab"][aria-selected="true"] {
    background:
        linear-gradient(135deg, rgba(24,89,55,0.98), rgba(8,35,22,0.98)) !important;

    border: 1px solid #35ff98 !important;

    box-shadow:
        0 0 30px rgba(53,255,152,0.12),
        inset 0 0 30px rgba(53,255,152,0.05);
}

button[data-baseweb="tab"],
button[data-baseweb="tab"] *,
button[data-baseweb="tab"] p,
button[data-baseweb="tab"] span,
button[data-baseweb="tab"] div {
    color: #ffffff !important;
    fill: #ffffff !important;
    font-size: 25px !important;
    font-weight: 900 !important;
}


/* ==============================
   WIDGET LABELS
============================== */

.stWidgetLabel,
.stWidgetLabel *,
div[data-testid="stWidgetLabel"],
div[data-testid="stWidgetLabel"] *,
label,
label * {
    color: #e9f3ed !important;
    font-size: 15px !important;
    font-weight: 800 !important;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
.stTextInput input {
    background: #f6f7f6 !important;
    color: #09120d !important;
    border-radius: 10px !important;
}

div[data-baseweb="select"] *,
div[data-baseweb="input"] * {
    color: #09120d;
}

.stMultiSelect [data-baseweb="tag"] {
    background-color: #d7ffe8 !important;
    color: #082c19 !important;
}


/* ==============================
   SECTION TITLES
============================== */

.section-title {
    font-size: 34px;
    font-weight: 950;
    color: #ffffff;
    margin-top: 8px;
    margin-bottom: 6px;
}

.section-title span {
    color: #35ff98;
}

.section-description {
    color: #9eaaa3;
    font-size: 14px;
    margin-bottom: 20px;
}


/* ==============================
   DATAFRAME STYLING
============================== */

div[data-testid="stDataFrame"] {
    border: 1px solid rgba(53,255,152,0.16) !important;
    border-radius: 18px !important;
    overflow: hidden !important;
    background: rgba(2,8,5,0.86) !important;
    box-shadow: 0 20px 50px rgba(0,0,0,0.20) !important;
}

div[data-testid="stDataFrame"] [role="columnheader"] {
    background: #0b2016 !important;
    color: #35ff98 !important;
    font-weight: 900 !important;
}

div[data-testid="stDataFrame"] [role="gridcell"] {
    background: #06100b !important;
    color: #eef6f1 !important;
    border-color: rgba(255,255,255,0.055) !important;
}

div[data-testid="stDataFrame"] [role="row"]:hover [role="gridcell"] {
    background: #0a1b12 !important;
}


/* ==============================
   DATABASE TABLE
============================== */

.database-wrap {
    width: 100%;
    overflow-x: auto;
    overflow-y: visible;
    border-radius: 18px;
    border: 1px solid rgba(53,255,152,0.16);
    background: rgba(2,8,5,0.86);
    box-shadow: 0 20px 50px rgba(0,0,0,0.20);
}

.yaya-table {
    border-collapse: separate;
    border-spacing: 0;
    width: 100%;
    min-width: 1050px;
    font-size: 14px;
}

.yaya-table th {
    padding: 15px 14px;
    text-align: center;
    background: #0b2016;
    color: #35ff98;
    font-weight: 900;
    border-bottom: 1px solid rgba(53,255,152,0.23);
    white-space: nowrap;
}

.yaya-table td {
    padding: 13px 14px;
    text-align: center;
    color: #eef6f1;
    background: #06100b;
    border-bottom: 1px solid rgba(255,255,255,0.055);
    white-space: nowrap;
}

.yaya-table tr:hover td {
    background: #0a1b12;
}

.yaya-table th:first-child {
    position: sticky;
    left: 0;
    z-index: 8;
    background: #0b2016;
}

.yaya-table td:first-child {
    position: sticky;
    left: 0;
    z-index: 5;
    background: #07130d;
    min-width: 190px;
    text-align: left;
    font-weight: 800;
}

.yaya-table tr:hover td:first-child {
    background: #0a1b12;
}

.rating-value {
    color: #35ff98;
    font-weight: 950;
    font-size: 16px;
}

.captain-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 23px;
    height: 23px;
    margin-left: 7px;
    border-radius: 50%;
    background: linear-gradient(135deg, #ffd84d, #ffad00);
    color: #161000 !important;
    font-size: 12px;
    font-weight: 950;
    box-shadow: 0 0 12px rgba(255,195,0,0.35);
}


/* ==============================
   INJURY BADGE
============================== */

.inj-badge {
    display: inline-block;
    margin-left: 7px;
    padding: 4px 8px;
    border-radius: 999px;
    background: rgba(255,72,72,0.14);
    border: 1px solid rgba(255,72,72,0.48);
    color: #ff7373 !important;
    font-size: 10px;
    font-weight: 950;
    letter-spacing: 0.6px;
    vertical-align: middle;
}


/* ==============================
   PLAYER CARDS
============================== */

.player-card {
    min-height: 230px;
    border-radius: 24px;
    padding: 28px;
    margin: 5px 0 20px 0;

    background:
        radial-gradient(circle at 100% 0%, rgba(53,255,152,0.13), transparent 35%),
        linear-gradient(145deg, rgba(12,37,24,0.98), rgba(3,11,7,0.98));

    border: 1px solid rgba(53,255,152,0.20);
    box-shadow: 0 20px 50px rgba(0,0,0,0.25);
}

.player-label {
    color: #35ff98;
    font-weight: 900;
    font-size: 12px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin-bottom: 13px;
}

.player-name {
    color: #ffffff;
    font-size: 31px;
    line-height: 1.05;
    font-weight: 950;
    margin-bottom: 9px;
}

.player-meta {
    color: #aebbb4;
    font-size: 14px;
    margin-bottom: 18px;
}

.player-rating-title {
    color: #8fa098;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.player-rating {
    color: #35ff98;
    font-weight: 950;
    font-size: 51px;
    line-height: 1;
    margin-top: 3px;
}

.player-rating span {
    color: #6c7b73;
    font-size: 20px;
}


/* ==============================
   EXPERIENCE BADGES
============================== */

.exp-badges {
    margin-top: 13px;
}

.exp-badge {
    display: inline-block;
    border-radius: 999px;
    padding: 7px 11px;
    margin-right: 6px;
    margin-top: 5px;
    font-size: 11px;
    font-weight: 850;
}

.exp-high {
    background: rgba(53,255,152,0.14);
    border: 1px solid rgba(53,255,152,0.42);
    color: #54ffaa;
}

.exp-low {
    background: rgba(59,147,255,0.13);
    border: 1px solid rgba(59,147,255,0.35);
    color: #89bdff;
}

.exp-none {
    background: rgba(255,196,0,0.13);
    border: 1px solid rgba(255,196,0,0.36);
    color: #ffd75a;
}


/* ==============================
   H2H TABLE
============================== */

.h2h-wrap {
    width: 100%;
    overflow-x: hidden;
    border-radius: 20px;
    border: 1px solid rgba(53,255,152,0.17);
    background: rgba(3,10,7,0.95);
}

.h2h-table {
    width: 100%;
    table-layout: fixed;
    border-collapse: collapse;
}

.h2h-table td {
    padding: 17px 16px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    font-size: 16px;
    vertical-align: middle;
}

.h2h-table tr:last-child td {
    border-bottom: none;
}

.h2h-left {
    width: 35%;
    text-align: right;
    color: #eef6f1;
    font-weight: 750;
}

.h2h-category {
    width: 30%;
    text-align: center;
    color: #35ff98;
    font-weight: 950;
    font-size: 15px !important;
    letter-spacing: 0.2px;
}

.h2h-right {
    width: 35%;
    text-align: left;
    color: #eef6f1;
    font-weight: 750;
}

.h2h-win {
    color: #35ff98 !important;
    font-weight: 950 !important;
}


/* ==============================
   MOBILE
============================== */

@media (max-width: 700px) {

    .block-container {
        padding-left: 0.65rem;
        padding-right: 0.65rem;
    }

    .yaya-hero {
        min-height: 290px;
        padding: 35px 23px 30px 23px;
        border-radius: 20px;
    }

    .hero-title {
        font-size: 45px;
        letter-spacing: -2px;
    }

    .hero-subtitle {
        font-size: 16px;
    }

    .hero-description {
        font-size: 12px;
    }

    .hero-side-text {
        display: none;
    }

    div[data-baseweb="tab-list"] {
        gap: 8px !important;
    }

    button[data-baseweb="tab"] {
        min-width: 0 !important;
        width: 48% !important;
        height: 72px !important;
        border-radius: 15px !important;
        padding: 5px !important;
    }

    button[data-baseweb="tab"],
    button[data-baseweb="tab"] *,
    button[data-baseweb="tab"] p,
    button[data-baseweb="tab"] span,
    button[data-baseweb="tab"] div {
        font-size: 15px !important;
    }

    .player-card {
        min-height: 185px;
        padding: 20px;
    }

    .player-name {
        font-size: 23px;
    }

    .player-rating {
        font-size: 40px;
    }

    .h2h-table td {
        padding: 10px 4px;
        font-size: 11px;
        word-wrap: break-word;
        white-space: normal;
    }

    .h2h-left {
        width: 35%;
        padding-right: 5px !important;
    }

    .h2h-category {
        width: 30%;
        font-size: 10px !important;
        padding-left: 2px !important;
        padding-right: 2px !important;
    }

    .h2h-right {
        width: 35%;
        padding-left: 5px !important;
    }

    .section-title {
        font-size: 27px;
    }
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# HERO
# =========================================================

hero_html = (
    '<div class="yaya-hero">'
    '<div class="hero-side-text">PLAY&nbsp;&nbsp; ANALYZE&nbsp;&nbsp; COMPARE&nbsp;&nbsp; WIN</div>'
    '<div class="hero-content">'
    '<div class="hero-kicker">EuroLeague Fantasy Analysis</div>'
    '<div class="hero-title">Yaya’s <span>Rating</span></div>'
    '<div class="hero-subtitle">'
    'A Fantasy rating built to answer one question: '
    'How much do I want this player on My Fantasy team?'
    '</div>'
    '<div class="hero-description">'
    'The rating combines Fantasy production, value, team role, consistency, '
    'playing time, efficiency, ceiling and sample size. Players without enough '
    'previous EuroLeague Fantasy data are evaluated using their NBA and European '
    'experience, current price and projected team role.'
    '</div>'
    '</div>'
    '</div>'
)

st.markdown(hero_html, unsafe_allow_html=True)

st.markdown(
    '<div class="info-box">'
    '⚡ Ratings now combine previous-season information with current-season Fantasy '
    'performance. Current-season influence increases automatically as more games are played.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# TEAM MAPPING
# =========================================================

TEAM_NAMES = {
    "OLY": "Olympiacos",
    "EFS": "Anadolu Efes",
    "CZV": "Crvena Zvezda",
    "HTA": "Hapoel Tel Aviv",
    "ZAL": "Zalgiris Kaunas",
    "VBC": "Valencia",
    "MTA": "Maccabi Tel Aviv",
    "PBB": "Paris Basketball",
    "PAO": "Panathinaikos",
    "RMB": "Real Madrid",
    "DUB": "Dubai Basketball",
    "FBT": "Fenerbahce",
    "MIL": "Milano",
    "PAR": "Partizan",
    "BAR": "Barcelona",
    "ASV": "ASVEL",
    "BJK": "Besiktas",
    "BAY": "Bayern Munich",
    "VIR": "Virtus Bologna",
    "KBA": "Baskonia",
    "MON": "AS Monaco"
}


OLD_TEAM_TO_CODE = {
    "Olympiacos Piraeus": "OLY",
    "Anadolu Efes Istanbul": "EFS",
    "Crvena Zvezda Meridianbet Belgrade": "CZV",
    "Hapoel IBI Tel Aviv": "HTA",
    "Zalgiris Kaunas": "ZAL",
    "Valencia Basket": "VBC",
    "Maccabi Rapyd Tel Aviv": "MTA",
    "Paris Basketball": "PBB",
    "Panathinaikos AKTOR Athens": "PAO",
    "Real Madrid": "RMB",
    "Dubai Basketball": "DUB",
    "Fenerbahce Beko Istanbul": "FBT",
    "EA7 Emporio Armani Milan": "MIL",
    "Partizan Mozzart Bet Belgrade": "PAR",
    "FC Barcelona": "BAR",
    "LDLC ASVEL Villeurbanne": "ASV",
    "FC Bayern Munich": "BAY",
    "Virtus Bologna": "VIR",
    "Baskonia Vitoria-Gasteiz": "KBA",
    "AS Monaco": "MON"
}


# =========================================================
# NAME NORMALIZATION
# =========================================================

def normalize_name(value):
    if pd.isna(value):
        return ""

    text = str(value).lower()

    text = unicodedata.normalize("NFKD", text)
    text = "".join(
        c for c in text
        if not unicodedata.combining(c)
    )

    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = " ".join(text.split())

    return text


NAME_ALIASES = {
    normalize_name("Antony Brown"): normalize_name("Anthony Brown"),
    normalize_name("D.J. Stewart"): normalize_name("D.J. Steward"),
    normalize_name("Bobi Gach"): normalize_name("Both Gach"),
    normalize_name("Olivier Nkamboua"): normalize_name("Olivier Nkamhoua")
}


def apply_alias(name_key):
    if name_key in NAME_ALIASES:
        return NAME_ALIASES[name_key]

    return name_key


# =========================================================
# EXPERIENCE DATA
# =========================================================

NBA_EXPERIENCE = {
    "Jonas Valanciunas": 5,
    "Dario Saric": 4,
    "Guerschon Yabusele": 4,
    "Amir Coffey": 4,
    "Patty Mills": 5,
    "Ante Zizic": 4,
    "T.J. Warren": 3,
    "MarJon Beauchamp": 3,
    "Tyson Etienne": 2,
    "Keaton Wallace": 3,
    "Ethan Thompson": 3,
    "Johnny Juzang": 3,
    "Chris Duarte": 4,
    "Devon Dotson": 3,
    "Tremont Waters": 2,
    "Bobi Klintman": 2,
    "Jacob Toppin": 2,
    "Alize Johnson": 3,
    "Anthony Brown": 3,
    "Jaylen Nowell": 4,
    "Jae Crowder": 5,
    "Tosan Evbuomwan": 3,
    "TyTy Washington Jr.": 3,
    "Maozinha Pereira": 2,
    "Joffrey Lauvergne": 4,
    "Stanley Umude": 2,
    "Olivier Sarr": 2,
    "Damian Jones": 4,
    "Garrison Mathews": 4,
    "D.J. Steward": 1,
    "Tyrese Martin": 3,
    "A.J. Lawson": 3,
    "Mouhamadou Gueye": 2,
    "Wendell Moore Jr.
