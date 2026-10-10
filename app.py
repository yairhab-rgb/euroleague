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
    'How much do I want this player on my Fantasy team?'
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
    "Wendell Moore Jr.": 2,
    "Damion Baugh": 2,
    "Furkan Korkmaz": 4,
    "Patrick Baldwin Jr.": 3,
    "Max Shulga": 5,
    "Yvon Pons": 2,
    "Justin Minaya": 3,
    "Davion Mintz": 1,
    "Tyler Ennis": 3,
    "Nikola Djurisic": 1
}


EUROPE_EXPERIENCE = {
    "Guerschon Yabusele": 5,
    "Ante Zizic": 5,
    "Johannes Thiemann": 5,
    "Joffrey Lauvergne": 5,
    "Rokas Jokubaitis": 5,
    "Scottie Wilbekin": 5,
    "Mam Jaiteh": 5,
    "Sertac Sanli": 5,

    "Jonas Valanciunas": 4,
    "Dario Saric": 4,
    "Marek Blazevic": 4,
    "David DeJulius": 4,
    "Mathis Dossou-Yovo": 4,
    "Furkan Korkmaz": 4,
    "Olek Balcerowski": 4,
    "Vitto Brown": 4,
    "Santi Yusta": 4,
    "Yoan Makoundou": 4,
    "Agustin Ubal": 4,
    "Nobel Boungou-Colo": 4,
    "Eli Ndiaye": 4,
    "Eleftherios Mantzoukas": 4,
    "Berk Ugurlu": 4,
    "Tommaso Baldasso": 4,
    "Dimitris Moraitis": 4,
    "Oz Blayzer": 4,

    "Patty Mills": 3,
    "Marcus Bingham": 3,
    "Austin Wiley": 3,
    "Rasheed Bello": 3,
    "Darrun Russell": 3,
    "Trent Frazier": 3,
    "Umoja Gibson": 3,
    "Kyle Allman Jr.": 3,
    "Johnny Juzang": 3,
    "Chris Duarte": 3,
    "Devon Dotson": 3,
    "Anthony Brown": 3,
    "Maozinha Pereira": 3,
    "Jason Burnell": 3,
    "Gonzalo Corbalan": 3,
    "Kevin Kokila": 3,
    "Hugo Besson": 3,
    "Both Gach": 3,
    "Mady Sissoko": 3,
    "Conor Morgan": 3,
    "R.J. Cole": 3,
    "Nikola Tanaskovic": 3,
    "Olivier Nkamhoua": 3,
    "Khadeen Carrington": 3,
    "Yvon Pons": 3,
    "Elias Valtonen": 3,
    "Tobias Jensen": 3,
    "Kaodirichi Akobundu-Ehiogu": 3,
    "Alvaro Cardenas": 3,
    "Vojin Medarevic": 3,

    "Marcus Carr": 1,
    "Eugene German": 1
}


EXPERIENCE_ADJUSTMENT = {
    "Ante Zizic": -2,
    "Joffrey Lauvergne": -2,
    "Rokas Jokubaitis": 2,
    "Johannes Thiemann": 2
}


# =========================================================
# INJURY STATUS
# =========================================================

def load_injured_players():
    if not os.path.exists("injuries.xlsx"):
        return set()
    try:
        injury_df = pd.read_excel("injuries.xlsx")
        required_columns = {"Player", "Status"}
        if not required_columns.issubset(set(injury_df.columns)):
            return set()

        injury_df = injury_df.copy()
        injury_df["Player"] = injury_df["Player"].astype(str).str.strip()
        injury_df["Status"] = injury_df["Status"].astype(str).str.strip().str.upper()

        out_players = injury_df.loc[
            injury_df["Status"] == "OUT",
            "Player"
        ].dropna().tolist()

        return set(out_players)
    except Exception:
        return set()


INJURED_PLAYERS = load_injured_players()

INJURED_KEYS = {
    apply_alias(normalize_name(name))
    for name in INJURED_PLAYERS
}


# =========================================================
# LOAD FILES
# =========================================================

try:
    old_df = pd.read_csv("fantasy_euroleague_stats.csv", encoding="utf-8-sig")
except Exception as e:
    st.error(f"Error loading fantasy_euroleague_stats.csv: {e}")
    st.stop()

try:
    new_df = pd.read_csv("new.csv", encoding="utf-8-sig", header=None)
except Exception as e:
    st.error(f"Error loading new.csv: {e}")
    st.stop()

if len(new_df.columns) == 4:
    first_row = [
        str(value).strip().casefold()
        for value in new_df.iloc[0].tolist()
    ] if not new_df.empty else []

    known_name_headers = {
        "name", "player", "current name", "שם שחקן"
    }

    if first_row and first_row[0] in known_name_headers:
        new_df.columns = new_df.iloc[0].astype(str).str.strip().tolist()
        new_df = new_df.iloc[1:].reset_index(drop=True)
    else:
        new_df.columns = [
            "Current Name", "Team Code", "Position", "Price"
        ]


# =========================================================
# LOAD CURRENT-SEASON ROUND FILES
# =========================================================

def load_current_season_rounds():
    round_files = []

    for file_path in glob.glob("round_*.xlsx"):
        match = re.search(
            r"round_(\d+)\.xlsx$",
            os.path.basename(file_path),
            flags=re.IGNORECASE
        )
        if match:
            round_files.append((int(match.group(1)), file_path))

    round_files.sort(key=lambda item: item[0])
    frames = []

    for round_number, file_path in round_files:
        try:
            round_df = pd.read_excel(file_path)
        except Exception:
            continue

        required_columns = {"Name", "Surname", "Team", "FPT", "Quotation"}
        if not required_columns.issubset(set(round_df.columns)):
            continue

        round_df = round_df.copy()
        round_df["Round"] = round_number

        round_df["Current Full Name"] = (
            round_df["Name"].fillna("").astype(str).str.strip()
            + " "
            + round_df["Surname"].fillna("").astype(str).str.strip()
        ).str.strip()

        round_df["Name Key"] = (
            round_df["Current Full Name"]
            .apply(normalize_name)
            .apply(apply_alias)
        )

        round_df["FPT"] = pd.to_numeric(round_df["FPT"], errors="coerce")
        round_df["Quotation"] = pd.to_numeric(round_df["Quotation"], errors="coerce")
        round_df["Team"] = round_df["Team"].astype(str).str.strip()

        round_df = round_df[round_df["FPT"].notna()].copy()
        frames.append(round_df)

    if not frames:
        return pd.DataFrame(), []

    current_games = pd.concat(frames, ignore_index=True)
    return current_games, round_files


current_games, loaded_round_files = load_current_season_rounds()


# =========================================================
# 2026-27 EUROLEAGUE SCHEDULE
# =========================================================

EUROLEAGUE_SCHEDULE = {
    1: [("CZV", "ZAL"), ("DUB", "RMB"), ("HTA", "BAY"), ("BAR", "EFS"), ("KBA", "OLY"), ("ASV", "MTA"), ("PAO", "PBB"), ("BJK", "VBC"), ("FBT", "VIR"), ("PAR", "MIL")],
    2: [("EFS", "RMB"), ("CZV", "HTA"), ("DUB", "BAR"), ("ZAL", "OLY"), ("VBC", "KBA"), ("MIL", "VIR"), ("FBT", "BAY"), ("PBB", "PAR"), ("MTA", "BJK"), ("PAO", "ASV")],
    3: [("CZV", "EFS"), ("HTA", "RMB"), ("VIR", "OLY"), ("PBB", "ZAL"), ("BJK", "BAR"), ("ASV", "VBC"), ("KBA", "MIL"), ("BAY", "PAR"), ("FBT", "DUB"), ("PAO", "MTA")],
    4: [("PBB", "ASV"), ("MTA", "MIL"), ("BAY", "VIR"), ("VBC", "HTA"), ("RMB", "PAR"), ("PAO", "FBT"), ("DUB", "CZV"), ("KBA", "BJK"), ("BAR", "ZAL"), ("OLY", "EFS")],
    5: [("ASV", "CZV"), ("KBA", "DUB"), ("MIL", "RMB"), ("BAR", "MTA"), ("VBC", "OLY"), ("FBT", "ZAL"), ("PAR", "PAO"), ("HTA", "BJK"), ("EFS", "BAY"), ("PBB", "VIR")],
    6: [("MIL", "DUB"), ("VBC", "MTA"), ("RMB", "ASV"), ("FBT", "PAR"), ("BJK", "BAY"), ("CZV", "PBB"), ("ZAL", "EFS"), ("BAR", "OLY"), ("VIR", "KBA"), ("PAO", "HTA")],
    7: [("HTA", "VIR"), ("MTA", "RMB"), ("MIL", "BAR"), ("EFS", "BJK"), ("BAY", "DUB"), ("PAR", "CZV"), ("PAO", "KBA"), ("ZAL", "ASV"), ("PBB", "VBC"), ("OLY", "FBT")],
    8: [("CZV", "MTA"), ("DUB", "PBB"), ("KBA", "RMB"), ("BAY", "BAR"), ("VBC", "FBT"), ("PAO", "MIL"), ("HTA", "EFS"), ("ASV", "PAR"), ("BJK", "OLY"), ("VIR", "ZAL")],
    9: [("CZV", "BAY"), ("MTA", "PBB"), ("RMB", "FBT"), ("DUB", "HTA"), ("ASV", "KBA"), ("ZAL", "PAR"), ("BAR", "VBC"), ("EFS", "PAO"), ("VIR", "BJK"), ("OLY", "MIL")],
    10: [("RMB", "PAO"), ("FBT", "KBA"), ("HTA", "BAR"), ("ASV", "BAY"), ("EFS", "PBB"), ("MIL", "VBC"), ("BJK", "ZAL"), ("VIR", "DUB"), ("PAR", "MTA"), ("OLY", "CZV")],
    11: [("PBB", "FBT"), ("PAR", "KBA"), ("MTA", "HTA"), ("MIL", "ZAL"), ("VBC", "BAY"), ("RMB", "CZV"), ("OLY", "DUB"), ("ASV", "BJK"), ("EFS", "VIR"), ("PAO", "BAR")],
    12: [("DUB", "EFS"), ("ZAL", "BAY"), ("MTA", "OLY"), ("KBA", "HTA"), ("MIL", "CZV"), ("BAR", "PBB"), ("FBT", "ASV"), ("PAR", "VBC"), ("VIR", "PAO"), ("BJK", "RMB")],
    13: [("ZAL", "PAO"), ("MTA", "DUB"), ("MIL", "FBT"), ("BAY", "KBA"), ("VBC", "VIR"), ("PBB", "HTA"), ("EFS", "ASV"), ("BAR", "CZV"), ("PAR", "BJK"), ("OLY", "RMB")],
    14: [("CZV", "VIR"), ("BJK", "PBB"), ("BAR", "FBT"), ("BAY", "MTA"), ("VBC", "PAO"), ("ASV", "MIL"), ("DUB", "PAR"), ("KBA", "EFS"), ("RMB", "ZAL"), ("OLY", "HTA")],
    15: [("HTA", "MIL"), ("EFS", "VBC"), ("BAY", "PBB"), ("FBT", "CZV"), ("RMB", "BAR"), ("BJK", "PAO"), ("ZAL", "DUB"), ("KBA", "MTA"), ("VIR", "PAR"), ("OLY", "ASV")],
    16: [("HTA", "ASV"), ("ZAL", "KBA"), ("MIL", "BAY"), ("PBB", "RMB"), ("FBT", "EFS"), ("DUB", "BJK"), ("VBC", "CZV"), ("VIR", "MTA"), ("PAR", "BAR"), ("PAO", "OLY")],
    17: [("MTA", "ZAL"), ("VBC", "DUB"), ("VIR", "ASV"), ("FBT", "HTA"), ("PBB", "OLY"), ("RMB", "BAY"), ("BJK", "MIL"), ("KBA", "BAR"), ("PAR", "EFS"), ("PAO", "CZV")],
    18: [("HTA", "ZAL"), ("ASV", "DUB"), ("FBT", "MTA"), ("RMB", "VBC"), ("CZV", "BJK"), ("EFS", "MIL"), ("KBA", "PBB"), ("BAR", "VIR"), ("BAY", "PAO"), ("OLY", "PAR")],
    19: [("BJK", "FBT"), ("HTA", "PAR"), ("ASV", "BAR"), ("BAY", "OLY"), ("VIR", "RMB"), ("CZV", "KBA"), ("DUB", "PAO"), ("ZAL", "VBC"), ("MTA", "EFS"), ("MIL", "PBB")],
    20: [("HTA", "MTA"), ("KBA", "VBC"), ("FBT", "PAO"), ("PAR", "ZAL"), ("RMB", "DUB"), ("ASV", "OLY"), ("EFS", "BAR"), ("BAY", "BJK"), ("VIR", "MIL"), ("PBB", "CZV")],
    21: [("BAR", "BJK"), ("ZAL", "PBB"), ("MTA", "PAO"), ("EFS", "FBT"), ("MIL", "HTA"), ("VBC", "PAR"), ("CZV", "ASV"), ("DUB", "BAY"), ("KBA", "VIR"), ("RMB", "OLY")],
    22: [("CZV", "RMB"), ("HTA", "PBB"), ("ASV", "ZAL"), ("MTA", "BAY"), ("BAR", "MIL"), ("VIR", "EFS"), ("DUB", "FBT"), ("PAO", "VBC"), ("BJK", "PAR"), ("OLY", "KBA")],
    23: [("HTA", "VBC"), ("ZAL", "CZV"), ("MIL", "ASV"), ("RMB", "EFS"), ("PAO", "BAY"), ("BJK", "KBA"), ("DUB", "MTA"), ("VIR", "BAR"), ("PAR", "FBT"), ("OLY", "PBB")],
    24: [("HTA", "PAO"), ("BAY", "MIL"), ("FBT", "BJK"), ("PBB", "KBA"), ("PAR", "OLY"), ("RMB", "MTA"), ("CZV", "BAR"), ("ZAL", "VIR"), ("EFS", "DUB"), ("VBC", "ASV")],
    25: [("BJK", "CZV"), ("KBA", "ZAL"), ("BAY", "VBC"), ("VIR", "PBB"), ("OLY", "MTA"), ("ASV", "HTA"), ("MIL", "PAR"), ("BAR", "DUB"), ("FBT", "RMB"), ("PAO", "EFS")],
    26: [("MTA", "VIR"), ("EFS", "ZAL"), ("KBA", "FBT"), ("PBB", "BJK"), ("PAR", "RMB"), ("PAO", "DUB"), ("HTA", "OLY"), ("BAR", "ASV"), ("BAY", "CZV"), ("VBC", "MIL")],
    27: [("DUB", "VIR"), ("ZAL", "BJK"), ("EFS", "MTA"), ("RMB", "PBB"), ("ASV", "FBT"), ("KBA", "CZV"), ("MIL", "PAO"), ("VBC", "BAR"), ("PAR", "HTA"), ("OLY", "BAY")],
    28: [("HTA", "KBA"), ("ASV", "EFS"), ("BJK", "DUB"), ("CZV", "PAR"), ("MTA", "BAR"), ("VBC", "PBB"), ("VIR", "BAY"), ("ZAL", "RMB"), ("FBT", "MIL"), ("OLY", "PAO")],
    29: [("KBA", "PAR"), ("VBC", "ZAL"), ("VIR", "HTA"), ("PBB", "MTA"), ("PAO", "BJK"), ("CZV", "FBT"), ("DUB", "OLY"), ("MIL", "EFS"), ("BAR", "RMB"), ("BAY", "ASV")],
    30: [("BJK", "ASV"), ("ZAL", "BAR"), ("MTA", "CZV"), ("KBA", "PAO"), ("BAY", "EFS"), ("VIR", "FBT"), ("PAR", "PBB"), ("RMB", "HTA"), ("DUB", "VBC"), ("MIL", "OLY")],
    31: [("MTA", "ASV"), ("EFS", "PAR"), ("BAY", "HTA"), ("PBB", "PAO"), ("RMB", "VIR"), ("CZV", "DUB"), ("ZAL", "MIL"), ("BAR", "KBA"), ("FBT", "VBC"), ("OLY", "BJK")],
    32: [("MTA", "VBC"), ("PAR", "BAY"), ("FBT", "PBB"), ("RMB", "KBA"), ("PAO", "ZAL"), ("BJK", "EFS"), ("CZV", "OLY"), ("DUB", "MIL"), ("ASV", "VIR"), ("BAR", "HTA")],
    33: [("DUB", "KBA"), ("HTA", "FBT"), ("ASV", "PAO"), ("EFS", "CZV"), ("PBB", "MIL"), ("PAR", "VIR"), ("ZAL", "MTA"), ("BAY", "RMB"), ("VBC", "BJK"), ("OLY", "BAR")],
    34: [("HTA", "DUB"), ("ASV", "PBB"), ("EFS", "KBA"), ("PAO", "PAR"), ("CZV", "VBC"), ("MIL", "MTA"), ("BAY", "ZAL"), ("FBT", "BAR"), ("RMB", "BJK"), ("OLY", "VIR")],
    35: [("ZAL", "HTA"), ("VIR", "CZV"), ("EFS", "OLY"), ("MTA", "FBT"), ("MIL", "BJK"), ("VBC", "RMB"), ("PBB", "DUB"), ("KBA", "BAY"), ("BAR", "PAO"), ("PAR", "ASV")],
    36: [("BJK", "HTA"), ("CZV", "PAO"), ("KBA", "ASV"), ("BAR", "BAY"), ("VIR", "VBC"), ("FBT", "OLY"), ("PBB", "EFS"), ("RMB", "MIL"), ("DUB", "ZAL"), ("MTA", "PAR")],
    37: [("HTA", "CZV"), ("ASV", "RMB"), ("MIL", "KBA"), ("BAY", "FBT"), ("VBC", "EFS"), ("PBB", "BAR"), ("PAO", "VIR"), ("BJK", "MTA"), ("PAR", "DUB"), ("OLY", "ZAL")],
    38: [("ZAL", "FBT"), ("CZV", "MIL"), ("MTA", "KBA"), ("EFS", "HTA"), ("PBB", "BAY"), ("PAO", "RMB"), ("BJK", "VIR"), ("DUB", "ASV"), ("BAR", "PAR"), ("OLY", "VBC")],
}


def add_opponents_to_current_games(games_df):
    if games_df.empty:
        return games_df.copy()

    output = games_df.copy()

    opponent_lookup = {}
    for round_number, games in EUROLEAGUE_SCHEDULE.items():
        for team_a, team_b in games:
            opponent_lookup[(round_number, team_a)] = team_b
            opponent_lookup[(round_number, team_b)] = team_a

    output["Opponent Team Code"] = output.apply(
        lambda row: opponent_lookup.get(
            (int(row["Round"]), str(row["Team"]).strip())
        ),
        axis=1
    )

    if "Position" in output.columns:
        position_text = output["Position"].fillna("").astype(str).str.strip().str.upper()
        output["Position Bucket"] = position_text.map(
            lambda value: (
                "G" if value.startswith("G") else
                "F" if value.startswith("F") else
                "C" if value.startswith("C") else
                None
            )
        )
    else:
        output["Position Bucket"] = None

    return output


current_games = add_opponents_to_current_games(current_games)


# =========================================================
# PREPARE CURRENT ROSTER
# =========================================================

new_df = new_df.rename(
    columns={
        "שם שחקן": "Current Name",
        "שם קבוצה": "Team Code",
        "עמדה": "Position",
        "מחיר": "Price",
        "Name": "Current Name",
        "Player": "Current Name",
        "Current Name": "Current Name",
        "Team": "Team Code",
        "Team Code": "Team Code",
        "Position": "Position",
        "Price": "Price"
    }
)

required_roster_columns = {
    "Current Name", "Team Code", "Position", "Price"
}
if not required_roster_columns.issubset(set(new_df.columns)):
    st.error(
        "new.csv must contain four columns: player name, team code, position, and price. "
        f"Detected columns: {list(new_df.columns)}"
    )
    st.stop()

new_df["Current Name"] = new_df["Current Name"].astype(str).str.strip()
new_df["Team Code"] = new_df["Team Code"].astype(str).str.strip()
new_df["Position"] = new_df["Position"].astype(str).str.strip()

new_df["Price"] = pd.to_numeric(
    new_df["Price"],
    errors="coerce"
)

new_df["Name Key"] = (
    new_df["Current Name"]
    .apply(normalize_name)
    .apply(apply_alias)
)


# =========================================================
# PREPARE HISTORICAL DATA
# =========================================================

old_df["Old Name"] = old_df["Full Name"]

old_df["Name Key"] = (
    old_df["Full Name"]
    .apply(normalize_name)
    .apply(apply_alias)
)

old_df["Old Team Code"] = old_df["Team"].map(
    OLD_TEAM_TO_CODE
)


# =========================================================
# MERGE
# =========================================================

merged = new_df.merge(
    old_df,
    on="Name Key",
    how="left",
    suffixes=("", "_old")
)

merged["Name"] = merged["Current Name"]
merged["Preseason Price"] = merged["Price"]

merged["Team"] = merged["Team Code"].map(
    TEAM_NAMES
).fillna(merged["Team Code"])


# =========================================================
# CURRENT-SEASON AGGREGATES
# =========================================================

merged["Injured"] = merged["Name Key"].isin(
    INJURED_KEYS
)

if not current_games.empty:

    current_summary = (
        current_games
        .groupby("Name Key", as_index=False)
        .agg(
            **{
                "Current Season Avg FPT": ("FPT", "mean"),
                "Current Season Games": ("FPT", "count"),
                "Current Season FPT Std Dev": ("FPT", "std"),
                "Current Season Floor Rate": (
                    "FPT",
                    lambda values: (values < 8).mean() * 100
                ),
                "Current Season Ceiling Rate": (
                    "FPT",
                    lambda values: (values >= 20).mean() * 100
                ),
                "Latest Round Played": ("Round", "max"),
            }
        )
    )

    latest_rows = (
        current_games
        .sort_values(
            ["Name Key", "Round"]
        )
        .groupby(
            "Name Key",
            as_index=False
        )
        .tail(1)[
            [
                "Name Key",
                "Quotation",
                "Team"
            ]
        ]
        .rename(
            columns={
                "Quotation": "Latest Price",
                "Team": "Latest Team Code"
            }
        )
    )

    current_summary = current_summary.merge(
        latest_rows,
        on="Name Key",
        how="left"
    )

    merged = merged.merge(
        current_summary,
        on="Name Key",
        how="left"
    )

    has_latest_price = (
        merged["Latest Price"].notna()
    )

    merged.loc[
        has_latest_price,
        "Price"
    ] = merged.loc[
        has_latest_price,
        "Latest Price"
    ]

else:

    merged["Current Season Avg FPT"] = pd.NA
    merged["Current Season Games"] = 0
    merged["Current Season FPT Std Dev"] = pd.NA
    merged["Current Season Floor Rate"] = pd.NA
    merged["Current Season Ceiling Rate"] = pd.NA
    merged["Latest Round Played"] = pd.NA
    merged["Latest Price"] = pd.NA
    merged["Latest Team Code"] = pd.NA


merged["Current Season Games"] = (
    pd.to_numeric(
        merged["Current Season Games"],
        errors="coerce"
    )
    .fillna(0)
)


# =========================================================
# NUMERIC COLUMNS
# =========================================================

numeric_columns = [
    "Overall Avg FPT",
    "Home Avg FPT",
    "Away Avg FPT",
    "FPT Std Dev",
    "Floor Rate % (FPT<8)",
    "Ceiling Rate % (FPT>=20)",
    "Total Minutes",
    "FPT per Minute",
    "Games Played"
]

for column in numeric_columns:
    if column in merged.columns:
        merged[column] = pd.to_numeric(
            merged[column],
            errors="coerce"
        )


# =========================================================
# HISTORICAL DATA FLAGS
# =========================================================

merged["Has Historical Data"] = (
    merged["Overall Avg FPT"].notna()
)

merged["Team Changed"] = (
    merged["Has Historical Data"]
    & merged["Old Team Code"].notna()
    & (merged["Old Team Code"] != merged["Team Code"])
)


# =========================================================
# MINUTES PER GAME
# =========================================================

merged["Minutes Per Game"] = 0.0

valid_games = (
    merged["Games Played"].notna()
    & (merged["Games Played"] > 0)
)

merged.loc[
    valid_games,
    "Minutes Per Game"
] = (
    merged.loc[
        valid_games,
        "Total Minutes"
    ]
    /
    merged.loc[
        valid_games,
        "Games Played"
    ]
)


# =========================================================
# CAPTAIN BADGE
# =========================================================

merged["Captain"] = (
    merged["Has Historical Data"]
    & (
        merged["Floor Rate % (FPT<8)"] <= 10
    )
    & (
        merged["Ceiling Rate % (FPT>=20)"] > 40
    )
)


# =========================================================
# INTERPOLATION FUNCTION
# =========================================================

def interpolate_score(value, points):
    if pd.isna(value):
        return 0.0

    value = float(value)

    if value <= points[0][0]:
        return float(points[0][1])

    if value >= points[-1][0]:
        return float(points[-1][1])

    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]

        if x1 <= value <= x2:
            if x2 == x1:
                return float(y1)

            ratio = (value - x1) / (x2 - x1)
            return y1 + ratio * (y2 - y1)

    return 0.0


# =========================================================
# HISTORICAL RATING SCALES
# =========================================================

PRODUCTION_POINTS = [
    (0, 0),
    (5, 2.5),
    (8, 4.5),
    (11, 6.5),
    (14, 8),
    (17, 9),
    (20, 10)
]

CURRENT_PRODUCTION_POINTS = [
    (0, 0),
    (30, 10)
]

VALUE_POINTS = [
    (0.50, 0),
    (0.60, 1),
    (0.70, 2),
    (0.80, 3),
    (0.90, 4),
    (1.00, 5),
    (1.10, 6.5),
    (1.20, 8),
    (1.30, 9),
    (1.40, 10)
]

STABILITY_POINTS = [
    (3, 10),
    (4, 9),
    (5, 8),
    (6, 6.5),
    (7, 5),
    (8, 3.5),
    (9, 2),
    (10, 0)
]

FLOOR_POINTS = [
    (0, 10),
    (10, 10),
    (20, 8.5),
    (30, 7),
    (40, 5.5),
    (50, 4),
    (60, 2.5),
    (75, 0)
]

MINUTES_POINTS = [
    (8, 1),
    (12, 3),
    (16, 5),
    (20, 7),
    (24, 9),
    (28, 10)
]

EFFICIENCY_POINTS = [
    (0.20, 1),
    (0.30, 3),
    (0.40, 5),
    (0.50, 7),
    (0.65, 9),
    (0.80, 10)
]

CEILING_POINTS = [
    (0, 0),
    (10, 2),
    (20, 4),
    (30, 6),
    (40, 8),
    (50, 9),
    (60, 10)
]

GAMES_POINTS = [
    (5, 2),
    (10, 4),
    (15, 6),
    (20, 8),
    (25, 9),
    (30, 10)
]


# =========================================================
# SCORE COMPONENTS
# =========================================================

merged["Production Score"] = merged["Overall Avg FPT"].apply(
    lambda x: interpolate_score(x, PRODUCTION_POINTS)
)

merged["Value Ratio"] = merged["Overall Avg FPT"] / merged["Preseason Price"]

merged["Value Score"] = merged["Value Ratio"].apply(
    lambda x: interpolate_score(x, VALUE_POINTS)
)

merged["Stability Score"] = merged["FPT Std Dev"].apply(
    lambda x: interpolate_score(x, STABILITY_POINTS)
)

merged["Floor Score"] = merged["Floor Rate % (FPT<8)"].apply(
    lambda x: interpolate_score(x, FLOOR_POINTS)
)

merged["Minutes Score"] = merged["Minutes Per Game"].apply(
    lambda x: interpolate_score(x, MINUTES_POINTS)
)

merged["Efficiency Score"] = merged["FPT per Minute"].apply(
    lambda x: interpolate_score(x, EFFICIENCY_POINTS)
)

merged["Ceiling Score"] = merged["Ceiling Rate % (FPT>=20)"].apply(
    lambda x: interpolate_score(x, CEILING_POINTS)
)

merged["Games Score"] = merged["Games Played"].apply(
    lambda x: interpolate_score(x, GAMES_POINTS)
)


# =========================================================
# TEAM ROLE
# =========================================================

merged["Baseline Role Rank"] = (
    merged
    .groupby(["Team Code", "Position"])["Preseason Price"]
    .rank(method="max", ascending=False)
)


def role_score_from_price_and_rank(price, rank):
    if pd.isna(price) or pd.isna(rank):
        return 0.0

    if float(price) < 8:
        return 0.0

    if rank == 1:
        return 10.0
    if rank == 2:
        return 6.0
    if rank == 3:
        return 3.0

    return 0.0


merged["Baseline Team Role Score"] = merged.apply(
    lambda row: role_score_from_price_and_rank(
        row["Preseason Price"],
        row["Baseline Role Rank"]
    ),
    axis=1
)

merged["Role Rank"] = pd.NA

active_for_role = (
    (~merged["Injured"])
    & merged["Price"].notna()
)

merged.loc[active_for_role, "Role Rank"] = (
    merged.loc[active_for_role]
    .groupby(["Team Code", "Position"])["Price"]
    .rank(method="max", ascending=False)
)


def team_role_score(row):
    if row["Injured"]:
        return 0.0

    return role_score_from_price_and_rank(
        row["Price"],
        row["Role Rank"]
    )


merged["Team Role Score"] = merged.apply(
    team_role_score,
    axis=1
)


# =========================================================
# HISTORICAL YAYA RATING
# =========================================================

def historical_yaya_rating(row):
    if not row["Has Historical Data"]:
        return pd.NA

    rating = (
        row["Production Score"] * 0.16
        + row["Value Score"] * 0.27
        + row["Baseline Team Role Score"] * 0.23
        + row["Stability Score"] * 0.05
        + row["Floor Score"] * 0.04
        + row["Minutes Score"] * 0.09
        + row["Efficiency Score"] * 0.08
        + row["Ceiling Score"] * 0.05
        + row["Games Score"] * 0.03
    )

    if row["Team Changed"]:
        rating = rating * 0.94

    return round(rating, 2)


merged["Historical Rating"] = merged.apply(
    historical_yaya_rating,
    axis=1
)


# =========================================================
# EXPERIENCE NAME MATCHING
# =========================================================

experience_names = set(
    list(NBA_EXPERIENCE.keys())
    + list(EUROPE_EXPERIENCE.keys())
    + list(EXPERIENCE_ADJUSTMENT.keys())
)

experience_lookup = {}
for experience_name in experience_names:
    experience_lookup[normalize_name(experience_name)] = experience_name


def get_experience_name(player_name):
    normalized = normalize_name(player_name)
    normalized = apply_alias(normalized)

    if normalized in experience_lookup:
        return experience_lookup[normalized]

    return player_name


merged["Experience Name"] = merged["Name"].apply(get_experience_name)


# =========================================================
# EXPERIENCE SCORE
# =========================================================

def get_nba_experience(name):
    return NBA_EXPERIENCE.get(name, 0)

def get_europe_experience(name):
    return EUROPE_EXPERIENCE.get(name, 0)

def get_experience_adjustment(name):
    return EXPERIENCE_ADJUSTMENT.get(name, 0)


merged["NBA Experience"] = merged["Experience Name"].apply(get_nba_experience)
merged["European Experience"] = merged["Experience Name"].apply(get_europe_experience)
merged["Experience Adjustment"] = merged["Experience Name"].apply(get_experience_adjustment)

merged["Experience Score"] = (
    merged["NBA Experience"] * 0.75
    + merged["European Experience"] * 1.40
    + merged["Experience Adjustment"]
)

merged["Experience Score"] = merged["Experience Score"].clip(lower=0, upper=10)
merged["Use Experience Rating"] = ~merged["Has Historical Data"]


# =========================================================
# EXPERIENCE LABELS
# =========================================================

def experience_labels(row):
    if not row["Use Experience Rating"]:
        return []

    nba = row["NBA Experience"]
    europe = row["European Experience"]
    labels = []

    if nba == 0 and europe == 0:
        labels.append(("Not Expected to Play", "none"))
        return labels

    if europe > 0:
        if europe > 3:
            labels.append(("High European Experience", "high"))
        else:
            labels.append(("Low European Experience", "low"))

    if nba > 0:
        if nba > 3:
            labels.append(("High NBA Experience", "high"))
        else:
            labels.append(("Low NBA Experience", "low"))

    return labels


merged["Experience Labels"] = merged.apply(experience_labels, axis=1)


# =========================================================
# PRICE / BUDGET SCORE FOR NEW PLAYERS
# =========================================================

def budget_score(price):
    if pd.isna(price):
        return 0.0

    price = float(price)
    minimum_price = 4.0
    maximum_price = 17.0

    if price <= minimum_price:
        return 10.0
    if price >= maximum_price:
        return 0.0

    score = 10 * (maximum_price - price) / (maximum_price - minimum_price)
    return score


merged["Budget Score"] = merged["Price"].apply(budget_score)


# =========================================================
# EXPERIENCE RATING
# =========================================================

def experience_yaya_rating(row):
    if not row["Use Experience Rating"]:
        return pd.NA

    experience = row["Experience Score"]
    if experience <= 0:
        return 0.0

    rating = (
        experience * 0.60
        + row["Team Role Score"] * 0.25
        + row["Budget Score"] * 0.15
    )

    rating = rating * 0.75
    return round(rating, 2)


merged["Experience Rating"] = merged.apply(experience_yaya_rating, axis=1)


# =========================================================
# CURRENT-SEASON PERFORMANCE RATING
# =========================================================

merged["Current Production Score"] = merged["Current Season Avg FPT"].apply(
    lambda x: interpolate_score(x, CURRENT_PRODUCTION_POINTS)
)

merged["Current Value Ratio"] = merged["Current Season Avg FPT"] / merged["Price"]

merged["Current Value Score"] = merged["Current Value Ratio"].apply(
    lambda x: interpolate_score(x, VALUE_POINTS)
)

merged["Current Stability Score"] = merged["Current Season FPT Std Dev"].apply(
    lambda x: 5.0 if pd.isna(x) else interpolate_score(x, STABILITY_POINTS)
)

merged["Current Floor Score"] = merged["Current Season Floor Rate"].apply(
    lambda x: interpolate_score(x, FLOOR_POINTS)
)

merged["Current Ceiling Score"] = merged["Current Season Ceiling Rate"].apply(
    lambda x: interpolate_score(x, CEILING_POINTS)
)

merged["Current Games Score"] = merged["Current Season Games"].apply(
    lambda x: interpolate_score(x, GAMES_POINTS)
)


def current_season_rating(row):
    current_avg_fpt = row["Current Season Avg FPT"]
    if pd.isna(current_avg_fpt) or row["Current Season Games"] <= 0:
        return pd.NA

    rating = interpolate_score(current_avg_fpt, CURRENT_PRODUCTION_POINTS)
    return round(rating, 2)


merged["Current Season Rating"] = merged.apply(current_season_rating, axis=1)


def current_season_weight(games):
    if pd.isna(games):
        return 0.0

    games = int(games)
    weights = {
        0: 0.00,
        1: 0.15,
        2: 0.25,
        3: 0.35,
        4: 0.45,
        5: 0.55,
        6: 0.65,
        7: 0.75,
        8: 0.85,
    }

    if games >= 9:
        return 0.90

    return weights.get(games, 0.0)


def choose_baseline_rating(row):
    if row["Has Historical Data"]:
        return row["Historical Rating"]
    return row["Experience Rating"]


merged["Baseline Rating"] = merged.apply(choose_baseline_rating, axis=1)


def choose_final_rating(row):
    baseline = row["Baseline Rating"]
    current = row["Current Season Rating"]
    games = row["Current Season Games"]

    if pd.isna(current) or games <= 0:
        return baseline

    weight = current_season_weight(games)

    if pd.isna(baseline):
        return current

    if not row["Has Historical Data"]:
        return current

    rating = float(baseline) * (1 - weight) + float(current) * weight
    return round(rating, 2)


merged["Yaya Rating"] = merged.apply(choose_final_rating, axis=1)


# =========================================================
# DISPLAY HELPERS
# =========================================================

def safe_text(value):
    if pd.isna(value):
        return "N/A"
    return html.escape(str(value))

def display_number(value, decimals=1):
    if pd.isna(value):
        return "N/A"
    return f"{float(value):.{decimals}f}"

def display_integer(value):
    if pd.isna(value):
        return "N/A"
    return str(int(round(float(value))))

def display_price(value):
    if pd.isna(value):
        return "N/A"
    return f"{float(value):.1f}"

def display_rating(value):
    if pd.isna(value):
        return "N/A"
    return f"{float(value):.2f}"

def player_name_html(row):
    name = html.escape(str(row["Name"]))
    badges = ""
    if row["Captain"]:
        badges += '<span class="captain-badge">C</span>'
    if row["Injured"]:
        badges += '<span class="inj-badge">INJ</span>'
    return name + badges

def experience_badges_html(row):
    labels = row["Experience Labels"]
    if not labels:
        return ""

    output = '<div class="exp-badges">'
    for label, badge_type in labels:
        if badge_type == "high":
            css_class = "exp-high"
        elif badge_type == "low":
            css_class = "exp-low"
        else:
            css_class = "exp-none"

        output += f'<span class="exp-badge {css_class}">{html.escape(label)}</span>'
    output += "</div>"
    return output


# =========================================================
# SORT
# =========================================================

merged = merged.sort_values(
    by=["Yaya Rating", "Price"],
    ascending=[False, False]
).reset_index(drop=True)


# =========================================================
# TABS
# =========================================================

database_tab, h2h_tab, fpt_allowed_tab = st.tabs(
    [
        "🏀 Player Database",
        "⚔️ Head-to-Head",
        "🛡️ FPT Allowed"
    ]
)


# =========================================================
# PLAYER DATABASE
# =========================================================

with database_tab:
    st.markdown(
        '<div class="section-title">Player <span>Database</span></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-description">Search, filter and compare every current EuroLeague Fantasy player.</div>',
        unsafe_allow_html=True
    )

    all_player_names = sorted(merged["Name"].dropna().astype(str).unique().tolist())
    team_options = sorted(merged["Team"].dropna().astype(str).unique().tolist())
    position_options = sorted(merged["Position"].dropna().astype(str).unique().tolist())

    filter_col1, filter_col2, filter_col3 = st.columns([1.4, 1, 1])

    with filter_col1:
        selected_player = st.selectbox("Search Player", options=[""] + all_player_names, index=0)

    with filter_col2:
        selected_teams = st.multiselect("Team", options=team_options)

    with filter_col3:
        selected_positions = st.multiselect("Position", options=position_options)

    minimum_price = float(merged["Price"].min())
    maximum_price = float(merged["Price"].max())

    selected_price_range = st.slider(
        "Price Range",
        min_value=minimum_price,
        max_value=maximum_price,
        value=(minimum_price, maximum_price),
        step=0.1
    )

    filtered = merged.copy()

    if selected_player != "":
        filtered = filtered[filtered["Name"] == selected_player]

    if selected_teams:
        filtered = filtered[filtered["Team"].isin(selected_teams)]

    if selected_positions:
        filtered = filtered[filtered["Position"].isin(selected_positions)]

    filtered = filtered[
        (filtered["Price"] >= selected_price_range[0])
        & (filtered["Price"] <= selected_price_range[1])
    ]

    filtered = filtered.sort_values("Yaya Rating", ascending=False)

    table_html = (
        '<div class="database-wrap">'
        '<table class="yaya-table">'
        '<thead>'
        '<tr>'
        '<th>Name</th>'
        '<th>Team</th>'
        '<th>Position</th>'
        '<th>Last Season Avg FPT</th>'
        '<th>Last Season FPT/Min</th>'
        '<th>Last Season Games</th>'
        '<th>Current Season Avg FPT</th>'
        '<th>Current Games</th>'
        '<th>Yaya Rating</th>'
        '</tr>'
        '</thead>'
        '<tbody>'
    )

    for _, row in filtered.iterrows():
        table_html += (
            '<tr>'
            f'<td>{player_name_html(row)}</td>'
            f'<td>{safe_text(row["Team"])}</td>'
            f'<td>{safe_text(row["Position"])}</td>'
            f'<td>{display_number(row["Overall Avg FPT"], 1)}</td>'
            f'<td>{display_number(row["FPT per Minute"], 2)}</td>'
            f'<td>{display_integer(row["Games Played"])}</td>'
            f'<td>{display_number(row["Current Season Avg FPT"], 1)}</td>'
            f'<td>{display_integer(row["Current Season Games"])}</td>'
            f'<td class="rating-value">{display_rating(row["Yaya Rating"])}</td>'
            '</tr>'
        )

    table_html += '</tbody></table></div>'
    st.markdown(table_html, unsafe_allow_html=True)


# =========================================================
# FPT ALLOWED BY POSITION
# =========================================================

with fpt_allowed_tab:
    st.markdown(
        '<div class="section-title">FPT <span>Allowed</span></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-description">Average Fantasy points allowed by each team to Guards, Forwards and Centers. Click any column header to sort the table.</div>',
        unsafe_allow_html=True
    )

    if current_games.empty:
        st.warning("No current-season round files are loaded yet.")
    elif current_games["Opponent Team Code"].notna().sum() == 0:
        st.warning("The loaded round files could not be matched to the EuroLeague schedule.")
    else:
        available_rounds = sorted(current_games["Round"].dropna().astype(int).unique().tolist())

        if len(available_rounds) == 1:
            start_round = end_round = available_rounds[0]
            st.caption(f"Round {start_round}")
        else:
            start_round, end_round = st.slider(
                "Rounds included",
                min_value=min(available_rounds),
                max_value=max(available_rounds),
                value=(min(available_rounds), max(available_rounds)),
                step=1,
                key="fpt_allowed_round_range"
            )

        allowed_games = current_games[
            current_games["Round"].between(start_round, end_round)
            & current_games["Opponent Team Code"].notna()
            & current_games["Position Bucket"].isin(["G", "F", "C"])
        ].copy()

        if allowed_games.empty:
            st.warning("No usable Fantasy data was found for the selected round range.")
        else:
            by_position = (
                allowed_games
                .groupby(["Opponent Team Code", "Position Bucket"])["FPT"]
                .mean()
                .unstack("Position Bucket")
                .reindex(columns=["G", "F", "C"])
            )

            overall_allowed = (
                allowed_games
                .groupby("Opponent Team Code")["FPT"]
                .mean()
                .rename("ALL")
            )

            allowed_table = by_position.join(overall_allowed).reset_index()

            allowed_table["Team"] = (
                allowed_table["Opponent Team Code"]
                .map(TEAM_NAMES)
                .fillna(allowed_table["Opponent Team Code"])
            )

            for column in ["G", "F", "C", "ALL"]:
                allowed_table[column] = allowed_table[column].round(1)

            allowed_table = (
                allowed_table[["Team", "G", "F", "C", "ALL"]]
                .sort_values("C", ascending=False, na_position="last")
                .reset_index(drop=True)
            )

            st.caption(
                f"Showing Rounds {start_round}-{end_round}. "
                "Higher FPT Allowed = a more favorable Fantasy matchup for that position."
            )

            st.dataframe(
                allowed_table,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Team": st.column_config.TextColumn("Team"),
                    "G": st.column_config.NumberColumn("Guards (G)", format="%.1f"),
                    "F": st.column_config.NumberColumn("Forwards (F)", format="%.1f"),
                    "C": st.column_config.NumberColumn("Centers (C)", format="%.1f"),
                    "ALL": st.column_config.NumberColumn("All Players", format="%.1f"),
                }
            )


# =========================================================
# HEAD TO HEAD
# =========================================================

with h2h_tab:
    st.markdown(
        '<div class="section-title">Head-to-<span>Head</span></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-description">Compare two players side by side and see which one fits your Fantasy team better.</div>',
        unsafe_allow_html=True
    )

    all_names = sorted(merged["Name"].dropna().astype(str).unique().tolist())

    default_player_1 = "Sasha Vezenkov"
    default_player_2 = "Elijah Bryant"

    player_1_index = all_names.index(default_player_1) if default_player_1 in all_names else 0
    player_2_index = all_names.index(default_player_2) if default_player_2 in all_names else min(1, len(all_names) - 1)

    selector_col1, selector_col2 = st.columns(2)

    with selector_col1:
        player_1_name = st.selectbox("Player 1", options=all_names, index=player_1_index, key="h2h_player_1")

    with selector_col2:
        player_2_name = st.selectbox("Player 2", options=all_names, index=player_2_index, key="h2h_player_2")

    player_1 = merged[merged["Name"] == player_1_name].iloc[0]
    player_2 = merged[merged["Name"] == player_2_name].iloc[0]

    card_col1, card_col2 = st.columns(2)

    with card_col1:
        player_1_card = (
            '<div class="player-card">'
            '<div class="player-label">Player 1</div>'
            f'<div class="player-name">{player_name_html(player_1)}</div>'
            f'<div class="player-meta">{safe_text(player_1["Team"])} • {safe_text(player_1["Position"])} • Price {display_price(player_1["Price"])}</div>'
            '<div class="player-rating-title">Yaya Rating</div>'
            f'<div class="player-rating">{display_rating(player_1["Yaya Rating"])}<span>/10</span></div>'
            f'{experience_badges_html(player_1)}'
            '</div>'
        )
        st.markdown(player_1_card, unsafe_allow_html=True)

        if not player_1["Has Historical Data"]:
            rookie_warning_1 = (
                '<div class="rookie-warning">'
                '⚠️ <b>Rookie:</b> '
                + html.escape(str(player_1["Name"]))
                + ' has no previous EuroLeague Fantasy data, so the rating is based on experience, current price and projected team role.'
                '</div>'
            )
            st.markdown(rookie_warning_1, unsafe_allow_html=True)

    with card_col2:
        player_2_card = (
            '<div class="player-card">'
            '<div class="player-label">Player 2</div>'
            f'<div class="player-name">{player_name_html(player_2)}</div>'
            f'<div class="player-meta">{safe_text(player_2["Team"])} • {safe_text(player_2["Position"])} • Price {display_price(player_2["Price"])}</div>'
            '<div class="player-rating-title">Yaya Rating</div>'
            f'<div class="player-rating">{display_rating(player_2["Yaya Rating"])}<span>/10</span></div>'
            f'{experience_badges_html(player_2)}'
            '</div>'
        )
        st.markdown(player_2_card, unsafe_allow_html=True)

        if not player_2["Has Historical Data"]:
            rookie_warning_2 = (
                '<div class="rookie-warning">'
                '⚠️ <b>Rookie:</b> '
                + html.escape(str(player_2["Name"]))
                + ' has no previous EuroLeague Fantasy data, so the rating is based on experience, current price and projected team role.'
                '</div>'
            )
            st.markdown(rookie_warning_2, unsafe_allow_html=True)

    warning_messages = []
    if player_1["Team Changed"]:
        warning_messages.append(player_1["Name"] + " is playing for a new team this season. His rating uses last season's performance from his previous team.")
    if player_2["Team Changed"]:
        warning_messages.append(player_2["Name"] + " is playing for a new team this season. His rating uses last season's performance from his previous team.")

    if warning_messages:
        warning_html = '<div class="info-box">⚠️ ' + "<br><br>⚠️ ".join(html.escape(m) for m in warning_messages) + '</div>'
        st.markdown(warning_html, unsafe_allow_html=True)

    comparison_rows = [
        (safe_text(player_1["Name"]), "Name", safe_text(player_2["Name"]), None),
        (safe_text(player_1["Team"]), "Team", safe_text(player_2["Team"]), None),
        (safe_text(player_1["Position"]), "Position", safe_text(player_2["Position"]), None),
        (display_price(player_1["Price"]), "Price", display_price(player_2["Price"]), "lower"),
        (display_number(player_1["Overall Avg FPT"], 1), "Last Season Avg FPT", display_number(player_2["Overall Avg FPT"], 1), "higher"),
        (display_number(player_1["Current Season Avg FPT"], 1), "Current Season Avg FPT", display_number(player_2["Current Season Avg FPT"], 1), "higher"),
        (display_integer(player_1["Current Season Games"]), "Current Season Games", display_integer(player_2["Current Season Games"]), "higher"),
        (display_number(player_1["Minutes Per Game"], 1), "Minutes", display_number(player_2["Minutes Per Game"], 1), "higher"),
        (display_number(player_1["FPT per Minute"], 2), "FPT / Min", display_number(player_2["FPT per Minute"], 2), "higher"),
        (display_integer(player_1["Games Played"]), "Games", display_integer(player_2["Games Played"]), "higher"),
        (display_rating(player_1["Yaya Rating"]), "Yaya Rating", display_rating(player_2["Yaya Rating"]), "higher")
    ]

    def numeric_value(row, category):
        if category == "Price":
            return row["Price"]
        if category == "Last Season Avg FPT":
            return row["Overall Avg FPT"]
        if category == "Current Season Avg FPT":
            return row["Current Season Avg FPT"]
        if category == "Current Season Games":
            return row["Current Season Games"]
        if category == "Minutes":
            return row["Minutes Per Game"]
        if category == "FPT / Min":
            return row["FPT per Minute"]
        if category == "Games":
            return row["Games Played"]
        if category == "Yaya Rating":
            return row["Yaya Rating"]
        return pd.NA

    h2h_html = '<div class="h2h-wrap"><table class="h2h-table"><tbody>'

    for value_1, category, value_2, comparison_type in comparison_rows:
        class_1 = "h2h-left"
        class_2 = "h2h-right"

        if comparison_type is not None:
            number_1 = numeric_value(player_1, category)
            number_2 = numeric_value(player_2, category)

            if not pd.isna(number_1) and not pd.isna(number_2):
                if comparison_type == "higher":
                    if number_1 > number_2:
                        class_1 += " h2h-win"
                    elif number_2 > number_1:
                        class_2 += " h2h-win"
                elif comparison_type == "lower":
                    if number_1 < number_2:
                        class_1 += " h2h-win"
                    elif number_2 < number_1:
                        class_2 += " h2h-win"

        h2h_html += (
            '<tr>'
            f'<td class="{class_1}">{value_1}</td>'
            f'<td class="h2h-category">{html.escape(category)}</td>'
            f'<td class="{class_2}">{value_2}</td>'
            '</tr>'
        )

    h2h_html += '</tbody></table></div>'
    st.markdown(h2h_html, unsafe_allow_html=True)
