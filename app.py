import streamlit as st
import pandas as pd
import unicodedata
import re
import html


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="Yaya's Rating",
    page_icon="🏀",
    layout="wide"
)


# =========================================================
# DESIGN
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 5%, rgba(0, 255, 135, 0.08), transparent 30%),
        radial-gradient(circle at 90% 15%, rgba(0, 180, 100, 0.06), transparent 27%),
        linear-gradient(180deg, #06100c 0%, #030806 48%, #010302 100%);
    color: white;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.25rem;
    padding-bottom: 3rem;
}


/* ======================================================
   HERO
====================================================== */

.hero {
    position: relative;
    min-height: 260px;
    border-radius: 28px;
    overflow: hidden;
    padding: 45px 48px;
    margin-bottom: 22px;

    background:
        radial-gradient(circle at 15% 105%, rgba(0,255,130,.30), transparent 40%),
        radial-gradient(circle at 76% 10%, rgba(0,255,140,.17), transparent 30%),
        radial-gradient(circle at 52% 120%, rgba(0,140,75,.12), transparent 40%),
        linear-gradient(120deg, #062015 0%, #04110c 43%, #020705 100%);

    border: 1px solid rgba(60,255,150,.27);

    box-shadow:
        0 30px 80px rgba(0,0,0,.48),
        inset 0 0 70px rgba(0,255,130,.045);
}

.hero-circle {
    position: absolute;
    width: 400px;
    height: 400px;
    border: 2px solid rgba(70,255,155,.11);
    border-radius: 50%;
    right: 115px;
    top: -185px;
}

.hero-line {
    position: absolute;
    right: 307px;
    top: 0;
    width: 2px;
    height: 100%;
    background: rgba(70,255,150,.08);
}

.hero-court {
    position: absolute;
    width: 250px;
    height: 125px;
    border: 2px solid rgba(70,255,155,.10);
    border-bottom: none;
    border-radius: 250px 250px 0 0;
    right: 175px;
    bottom: -2px;
}

.hero-tag {
    position: relative;
    z-index: 3;
    display: inline-block;
    background: rgba(43,245,130,.10);
    color: #59f79c;
    border: 1px solid rgba(70,255,150,.23);
    padding: 8px 15px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 900;
    letter-spacing: 1.25px;
}

.hero-title {
    position: relative;
    z-index: 3;
    font-size: 62px;
    line-height: 1;
    font-weight: 950;
    letter-spacing: -3px;
    color: #f6fff9;
    margin-top: 25px;
}

.hero-title span {
    color: #43f58d;
    text-shadow: 0 0 30px rgba(50,255,145,.25);
}

.hero-subtitle {
    position: relative;
    z-index: 3;
    color: #a6bbb0;
    font-size: 19px;
    margin-top: 15px;
    letter-spacing: .4px;
}

.hero-words {
    position: absolute;
    z-index: 4;
    right: 38px;
    top: 36px;
    text-align: right;
    font-size: 14px;
    line-height: 2.15;
    font-weight: 950;
    letter-spacing: 3.5px;
    color: rgba(102,255,171,.63);
}


/* ======================================================
   WARNINGS
====================================================== */

.global-warning,
.yellow-warning {
    background: rgba(255,193,7,.09);
    border: 1px solid rgba(255,204,55,.35);
    border-left: 5px solid #ffd447;
    border-radius: 13px;
    color: #ffe89b;
    padding: 14px 16px;
    margin: 12px 0 20px 0;
    font-size: 14px;
}


/* ======================================================
   BIG CENTERED TABS
====================================================== */

div[data-testid="stTabs"] {
    margin-top: 18px;
}

div[data-testid="stTabs"] div[data-baseweb="tab-list"] {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 24px !important;

    background: transparent !important;
    border-bottom: none !important;

    padding: 10px 0 20px 0 !important;
    margin: 0 auto !important;
}

div[data-testid="stTabs"] button[data-baseweb="tab"] {
    flex: none !important;

    min-width: 390px !important;
    width: 390px !important;
    height: 78px !important;

    justify-content: center !important;

    padding: 0 30px !important;

    border-radius: 18px !important;

    background:
        linear-gradient(
            145deg,
            rgba(12,30,21,.98),
            rgba(6,17,12,.98)
        ) !important;

    border: 1px solid rgba(68,255,150,.22) !important;

    color: #c8d8cf !important;

    font-size: 21px !important;
    font-weight: 900 !important;

    box-shadow:
        0 12px 30px rgba(0,0,0,.24) !important;

    transition: all .2s ease !important;
}

div[data-testid="stTabs"] button[data-baseweb="tab"]:hover {
    border-color: rgba(70,255,150,.48) !important;
    background:
        linear-gradient(
            145deg,
            rgba(15,48,31,.98),
            rgba(7,24,16,.98)
        ) !important;
    transform: translateY(-1px);
}

div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] {
    color: white !important;

    background:
        linear-gradient(
            135deg,
            #137b45 0%,
            #1ab75f 50%,
            #16904f 100%
        ) !important;

    border: 1px solid rgba(97,255,170,.65) !important;

    box-shadow:
        0 12px 35px rgba(0,255,125,.17),
        inset 0 0 30px rgba(255,255,255,.04) !important;
}

div[data-testid="stTabs"] div[data-baseweb="tab-highlight"] {
    display: none !important;
}

div[data-testid="stTabs"] div[data-baseweb="tab-border"] {
    display: none !important;
}


/* ======================================================
   INPUTS
====================================================== */

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    border-radius: 12px !important;
}

div[data-testid="stTextInput"] input {
    border-radius: 12px !important;
}


/* ======================================================
   SECTION TITLES
====================================================== */

.section-title {
    font-size: 30px;
    font-weight: 950;
    margin: 25px 0 18px 0;
    color: #ffffff;
}


/* ======================================================
   DATABASE TABLE
====================================================== */

.table-wrap {
    width: 100%;
    overflow-x: auto;
    max-height: 720px;
    overflow-y: auto;

    border-radius: 18px;

    border: 1px solid rgba(72,255,155,.13);

    background: rgba(4,11,8,.94);

    box-shadow: 0 20px 50px rgba(0,0,0,.27);
}

.yaya-table {
    width: 100%;
    border-collapse: collapse;
    min-width: 1000px;
    font-size: 14px;
}

.yaya-table th {
    position: sticky;
    top: 0;
    z-index: 2;

    background: #10251a;
    color: #57f599;

    padding: 15px 13px;

    text-align: left;

    border-bottom:
        1px solid rgba(75,255,155,.20);

    font-size: 12px;
    letter-spacing: .45px;
    text-transform: uppercase;
}

.yaya-table td {
    padding: 13px;
    border-bottom:
        1px solid rgba(255,255,255,.045);
    color: #dce8e1;
}

.yaya-table tr:hover td {
    background: rgba(45,245,130,.05);
}

.player-cell {
    color: white !important;
    font-weight: 850;
}

.rating-cell {
    color: #50f294 !important;
    font-weight: 950;
    font-size: 15px;
}


/* ======================================================
   HEAD TO HEAD
====================================================== */

.compare-card {
    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(38,245,128,.08),
            transparent 36%
        ),
        linear-gradient(
            145deg,
            rgba(12,29,20,.98),
            rgba(4,11,8,.98)
        );

    border:
        1px solid rgba(70,255,155,.15);

    border-radius: 21px;

    padding: 25px;

    min-height: 185px;

    box-shadow:
        0 18px 45px rgba(0,0,0,.24);
}

.compare-name {
    font-size: 28px;
    font-weight: 950;
    color: white;
    margin-bottom: 8px;
}

.compare-meta {
    color: #96aa9e;
    font-size: 15px;
}

.compare-rating {
    font-size: 40px;
    line-height: 1;
    font-weight: 950;
    color: #4bf393;
    margin-top: 18px;
}

.rating-caption {
    color: #788b80;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-top: 5px;
}


/* ======================================================
   EXPERIENCE BADGES
====================================================== */

.badges-area {
    margin-top: 15px;
}

.badge {
    display: inline-block;
    padding: 7px 11px;

    border-radius: 999px;

    margin-right: 7px;
    margin-top: 5px;

    font-size: 11px;
    font-weight: 900;
    letter-spacing: .35px;

    border:
        1px solid rgba(255,255,255,.12);
}

.badge-high {
    background: rgba(48,239,134,.12);
    color: #59f59b;
    border-color:
        rgba(60,255,150,.25);
}

.badge-low {
    background: rgba(64,161,255,.11);
    color: #8bc6ff;
    border-color:
        rgba(100,180,255,.23);
}

.badge-zero {
    background: rgba(255,193,7,.11);
    color: #ffd96b;
    border-color:
        rgba(255,205,70,.28);
}


/* ======================================================
   RESPONSIVE
====================================================== */

@media (max-width: 900px) {

    div[data-testid="stTabs"]
    div[data-baseweb="tab-list"] {
        gap: 10px !important;
    }

    div[data-testid="stTabs"]
    button[data-baseweb="tab"] {
        min-width: 0 !important;
        width: 46% !important;
        height: 68px !important;
        font-size: 16px !important;
    }

    .hero-title {
        font-size: 45px;
    }

    .hero-words {
        display: none;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HERO
# IMPORTANT:
# Built as one continuous HTML string so Streamlit
# cannot interpret the HTML as a Markdown code block.
# =========================================================

hero_html = (
    '<div class="hero">'
    '<div class="hero-circle"></div>'
    '<div class="hero-line"></div>'
    '<div class="hero-court"></div>'
    '<div class="hero-tag">EUROLEAGUE FANTASY ANALYTICS</div>'
    '<div class="hero-title">Yaya&apos;s <span>Rating</span></div>'
    '<div class="hero-subtitle">Data-driven EuroLeague Fantasy player analysis</div>'
    '<div class="hero-words">PLAY<br>ANALYZE<br>COMPARE<br>WIN</div>'
    '</div>'
)

st.markdown(
    hero_html,
    unsafe_allow_html=True
)


warning_html = (
    '<div class="global-warning">'
    '⚠️ Past performance is only a reference point. '
    'Historical Fantasy numbers do not guarantee how a player will perform '
    'in the upcoming season.'
    '</div>'
)

st.markdown(
    warning_html,
    unsafe_allow_html=True
)


# =========================================================
# TEAM NAMES
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
# NORMALIZE NAME
# =========================================================

def normalize_name(value):

    if pd.isna(value):
        return ""

    text = str(value).lower()

    text = unicodedata.normalize(
        "NFKD",
        text
    )

    text = "".join(
        c for c in text
        if not unicodedata.combining(c)
    )

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = " ".join(
        text.split()
    )

    return text


# =========================================================
# NAME ALIASES
# =========================================================

NAME_ALIASES = {
    normalize_name("Antony Brown"):
        normalize_name("Anthony Brown"),

    normalize_name("D.J. Stewart"):
        normalize_name("D.J. Steward"),

    normalize_name("Bobi Gach"):
        normalize_name("Both Gach"),

    normalize_name("Olivier Nkamboua"):
        normalize_name("Olivier Nkamhoua")
}


# =========================================================
# NBA EXPERIENCE
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

    "Jae Crowder": 5,

    "Tosan Evbuomwan": 3,
    "TyTy Washington Jr.": 3,

    "Mãozinha Pereira": 2,

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

    # Manual decision
    "Max Shulga": 5,

    "Yvon Pons": 2,

    "Justin Minaya": 3,

    "Davion Mintz": 1,

    "Tyler Ennis": 3,

    "Nikola Djurisic": 1
}


# =========================================================
# EUROPE EXPERIENCE
# =========================================================

EUROPE_EXPERIENCE = {

    # ---------------------------------------------
    # 5 POINTS - HIGH EUROLEAGUE EXPERIENCE
    # ---------------------------------------------

    "Guerschon Yabusele": 5,
    "Ante Zizic": 5,
    "Johannes Thiemann": 5,
    "Joffrey Lauvergne": 5,

    "Rokas Jokubaitis": 5,
    "Scottie Wilbekin": 5,
    "Mam Jaiteh": 5,
    "Sertaç Şanlı": 5,

    # ---------------------------------------------
    # 4 POINTS - HAS EUROLEAGUE EXPERIENCE
    # ---------------------------------------------

    "Jonas Valanciunas": 4,
    "Dario Saric": 4,

    # Correction
    "Marek Blazevic": 4,

    "David DeJulius": 4,
    "Mathis Dossou-Yovo": 4,
    "Furkan Korkmaz": 4,
    "Olek Balcerowski": 4,

    "Vitto Brown": 4,

    "Agustin Ubal": 4,
    "Nobel Boungou-Colo": 4,
    "Eli Ndiaye": 4,

    "Eleftherios Mantzoukas": 4,
    "Berk Ugurlu": 4,
    "Tommaso Baldasso": 4,
    "Dimitris Moraitis": 4,
    "Oz Blayzer": 4,

    # ---------------------------------------------
    # 3 POINTS - MANUAL EUROPE EXPERIENCE
    # ---------------------------------------------

    "Patty Mills": 3,
    "Marcus Bingham": 3,
    "Austin Wiley": 3,
    "Rasheed Bello": 3,
    "Trent Frazier": 3,
    "Umoja Gibson": 3,
    "Kyle Allman Jr.": 3,

    "Johnny Juzang": 3,
    "Chris Duarte": 3,
    "Devon Dotson": 3,

    "Anthony Brown": 3,
    "Mãozinha Pereira": 3,

    "Jason Burnell": 3,
    "Gonzalo Corbalán": 3,
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

    "Álvaro Cárdenas": 3,
    "Vojin Medarevic": 3
}


# =========================================================
# THE PLAYERS TO WHICH EXPERIENCE LABELS APPLY
# =========================================================

SPECIAL_EXPERIENCE_PLAYERS = set(
    NBA_EXPERIENCE.keys()
)

SPECIAL_EXPERIENCE_PLAYERS.update(
    EUROPE_EXPERIENCE.keys()
)


# =========================================================
# LOAD DATA
# =========================================================

old = pd.read_csv(
    "fantasy_euroleague_stats.csv",
    encoding="utf-8-sig"
)

new = pd.read_csv(
    "new.csv",
    encoding="utf-8-sig"
)


new = new.rename(
    columns={
        "שם שחקן": "Current Name",
        "שם קבוצה": "Team Code",
        "עמדה": "Position",
        "מחיר": "Price"
    }
)


# =========================================================
# MATCH DATA
# =========================================================

old["Name Key"] = old["Full Name"].apply(
    normalize_name
)

new["Name Key"] = new["Current Name"].apply(
    normalize_name
)


new["Match Key"] = new["Name Key"].apply(
    lambda value:
    NAME_ALIASES.get(
        value,
        value
    )
)


old_columns = [
    "Name Key",
    "Full Name",
    "Team",
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


merged = new.merge(
    old[old_columns],
    left_on="Match Key",
    right_on="Name Key",
    how="left",
    suffixes=("", "_old")
)


merged["Display Name"] = (
    merged["Current Name"]
)


merged["Current Team"] = (
    merged["Team Code"]
    .map(TEAM_NAMES)
    .fillna(
        merged["Team Code"]
    )
)


merged["Old Team Code"] = (
    merged["Team"]
    .map(OLD_TEAM_TO_CODE)
)


merged["Has Historical Data"] = (
    merged["Full Name"].notna()
)


merged["Team Changed"] = (
    merged["Has Historical Data"]
    & merged["Old Team Code"].notna()
    & (
        merged["Old Team Code"]
        != merged["Team Code"]
    )
)


# =========================================================
# NUMERIC
# =========================================================

numeric_columns = [
    "Price",
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

    merged[column] = pd.to_numeric(
        merged[column],
        errors="coerce"
    )


merged["Minutes"] = (
    merged["Total Minutes"]
    / merged["Games Played"]
)


merged.loc[
    merged["Games Played"] <= 0,
    "Minutes"
] = pd.NA


# =========================================================
# CAPTAIN
# =========================================================

merged["Captain"] = (
    (
        merged[
            "Floor Rate % (FPT<8)"
        ]
        <= 10
    )
    &
    (
        merged[
            "Ceiling Rate % (FPT>=20)"
        ]
        > 40
    )
)


merged["Player"] = (
    merged["Display Name"]
)


merged.loc[
    merged["Captain"] == True,
    "Player"
] = (
    merged.loc[
        merged["Captain"] == True,
        "Display Name"
    ]
    + " C"
)


# =========================================================
# LINEAR SCORE
# =========================================================

def linear_score(value, points):

    if pd.isna(value):
        return pd.NA

    if value <= points[0][0]:
        return points[0][1]

    if value >= points[-1][0]:
        return points[-1][1]

    for i in range(
        len(points) - 1
    ):

        x1 = points[i][0]
        y1 = points[i][1]

        x2 = points[i + 1][0]
        y2 = points[i + 1][1]

        if x1 <= value <= x2:

            if x2 == x1:
                return y2

            ratio = (
                (value - x1)
                / (x2 - x1)
            )

            return (
                y1
                + ratio
                * (y2 - y1)
            )

    return pd.NA


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


# =========================================================
# TEAM ROLE
# =========================================================

merged["Role Rank"] = (
    merged
    .groupby(
        [
            "Team Code",
            "Position"
        ]
    )["Price"]
    .rank(
        method="max",
        ascending=False
    )
)


def team_role_score(row):

    price = row["Price"]
    rank = row["Role Rank"]

    if pd.isna(price):
        return 0

    if pd.isna(rank):
        return 0

    if price < 8:
        return 0

    if rank == 1:
        return 10

    if rank == 2:
        return 6

    if rank == 3:
        return 3

    return 0


merged["Team Role Score"] = (
    merged.apply(
        team_role_score,
        axis=1
    )
)


# =========================================================
# HISTORICAL COMPONENTS
# =========================================================

merged["Production Score"] = (
    merged["Overall Avg FPT"]
    .apply(
        lambda value:
        linear_score(
            value,
            PRODUCTION_POINTS
        )
    )
)


merged["Value"] = (
    merged["Overall Avg FPT"]
    / merged["Price"]
)


merged["Value Score"] = (
    merged["Value"]
    .apply(
        lambda value:
        linear_score(
            value,
            VALUE_POINTS
        )
    )
)


merged["Stability Score"] = (
    merged["FPT Std Dev"]
    .apply(
        lambda value:
        linear_score(
            value,
            STABILITY_POINTS
        )
    )
)


merged["Floor Score"] = (
    merged[
        "Floor Rate % (FPT<8)"
    ]
    .apply(
        lambda value:
        linear_score(
            value,
            FLOOR_POINTS
        )
    )
)


merged["Minutes Score"] = (
    merged["Minutes"]
    .apply(
        lambda value:
        linear_score(
            value,
            MINUTES_POINTS
        )
    )
)


merged["Efficiency Score"] = (
    merged["FPT per Minute"]
    .apply(
        lambda value:
        linear_score(
            value,
            EFFICIENCY_POINTS
        )
    )
)


# =========================================================
# HISTORICAL RATING
# =========================================================

def historical_rating(row):

    required = [
        row["Production Score"],
        row["Value Score"],
        row["Stability Score"],
        row["Floor Score"],
        row["Minutes Score"],
        row["Efficiency Score"]
    ]

    for value in required:

        if pd.isna(value):
            return pd.NA

    rating = (
        row["Production Score"] * 0.25
        + row["Value Score"] * 0.20
        + row["Team Role Score"] * 0.25
        + row["Stability Score"] * 0.06
        + row["Floor Score"] * 0.04
        + row["Minutes Score"] * 0.10
        + row["Efficiency Score"] * 0.10
    )

    if row["Team Changed"]:
        rating = rating * 0.94

    return round(
        rating,
        2
    )


merged["Historical Rating"] = (
    merged.apply(
        historical_rating,
        axis=1
    )
)


# =========================================================
# EXPERIENCE NAME
# =========================================================

def experience_name(name):

    key = normalize_name(name)

    if key == normalize_name(
        "Antony Brown"
    ):
        return "Anthony Brown"

    if key == normalize_name(
        "D.J. Stewart"
    ):
        return "D.J. Steward"

    if key == normalize_name(
        "Bobi Gach"
    ):
        return "Both Gach"

    if key == normalize_name(
        "Olivier Nkamboua"
    ):
        return "Olivier Nkamhoua"

    return name


merged["Experience Name"] = (
    merged["Display Name"]
    .apply(
        experience_name
    )
)


# =========================================================
# EXPERIENCE SCORES
# =========================================================

merged["NBA Experience"] = (
    merged["Experience Name"]
    .map(
        NBA_EXPERIENCE
    )
    .fillna(0)
)


merged["Europe Experience"] = (
    merged["Experience Name"]
    .map(
        EUROPE_EXPERIENCE
    )
    .fillna(0)
)


merged["Experience Score"] = (
    merged["NBA Experience"]
    + merged["Europe Experience"]
)


merged["Is Experience Player"] = (
    merged["Experience Name"]
    .isin(
        SPECIAL_EXPERIENCE_PLAYERS
    )
)


# =========================================================
# LABELS
# IMPORTANT:
# Normal historical players such as Sasha / Elijah
# receive NO experience label.
# =========================================================

def get_labels(row):

    if not row["Is Experience Player"]:
        return []

    nba = row["NBA Experience"]
    europe = row["Europe Experience"]

    labels = []

    if nba == 0 and europe == 0:

        labels.append(
            "Not Expected to Play"
        )

        return labels

    if nba >= 4:

        labels.append(
            "High NBA Experience"
        )

    elif nba >= 1:

        labels.append(
            "Low NBA Experience"
        )

    if europe >= 4:

        labels.append(
            "High European Experience"
        )

    elif europe >= 1:

        labels.append(
            "Low European Experience"
        )

    return labels


merged["Experience Labels"] = (
    merged.apply(
        get_labels,
        axis=1
    )
)


# =========================================================
# BUDGET SCORE
# =========================================================

def budget_score(price):

    if pd.isna(price):
        return 0

    if price <= 4:
        return 10

    if price >= 17:
        return 0

    score = (
        10
        - (
            (price - 4)
            / 13
        )
        * 10
    )

    return score


merged["Budget Score"] = (
    merged["Price"]
    .apply(
        budget_score
    )
)


# =========================================================
# EXPERIENCE-BASED RATING
# =========================================================

def experience_rating(row):

    if not row["Is Experience Player"]:
        return pd.NA

    experience = (
        row["Experience Score"]
    )

    if experience == 0:
        return 0.0

    rating = (
        experience * 0.50
        + row["Team Role Score"] * 0.30
        + row["Budget Score"] * 0.20
    )

    return round(
        rating,
        2
    )


merged["Experience Rating"] = (
    merged.apply(
        experience_rating,
        axis=1
    )
)


# =========================================================
# FINAL YAYA RATING
# =========================================================

def final_rating(row):

    if not pd.isna(
        row["Historical Rating"]
    ):
        return row[
            "Historical Rating"
        ]

    if row["Is Experience Player"]:
        return row[
            "Experience Rating"
        ]

    return pd.NA


merged["Yaya Rating"] = (
    merged.apply(
        final_rating,
        axis=1
    )
)


# =========================================================
# DISPLAY HELPERS
# =========================================================

def display_number(
    value,
    decimals=1
):

    if pd.isna(value):
        return "N/A"

    return f"{value:.{decimals}f}"


def display_integer(value):

    if pd.isna(value):
        return "N/A"

    return str(
        int(value)
    )


def rating_display(value):

    if pd.isna(value):
        return "N/A"

    return f"{value:.2f}"


def labels_html(labels):

    if len(labels) == 0:
        return ""

    result = (
        '<div class="badges-area">'
    )

    for label in labels:

        if label == "Not Expected to Play":

            css_class = "badge-zero"

        elif label.startswith("High"):

            css_class = "badge-high"

        else:

            css_class = "badge-low"

        result += (
            '<span class="badge '
            + css_class
            + '">'
            + html.escape(label)
            + '</span>'
        )

    result += '</div>'

    return result


# =========================================================
# TABS
# =========================================================

tab_database, tab_compare = st.tabs(
    [
        "🏀  PLAYER DATABASE",
        "⚔️  HEAD-TO-HEAD"
    ]
)


# =========================================================
# PLAYER DATABASE
# =========================================================

with tab_database:

    st.markdown(
        '<div class="section-title">Player Database</div>',
        unsafe_allow_html=True
    )


    filter1, filter2, filter3 = (
        st.columns(
            [1.4, 1, 1]
        )
    )


    with filter1:

        search = st.text_input(
            "Search Player",
            placeholder="Type a player name..."
        )


    teams = sorted(
        merged[
            "Current Team"
        ]
        .dropna()
        .unique()
        .tolist()
    )


    with filter2:

        team_filter = st.multiselect(
            "Team",
            teams
        )


    positions = sorted(
        merged[
            "Position"
        ]
        .dropna()
        .unique()
        .tolist()
    )


    with filter3:

        position_filter = st.multiselect(
            "Position",
            positions
        )


    minimum_price = float(
        merged[
            "Price"
        ].min()
    )

    maximum_price = float(
        merged[
            "Price"
        ].max()
    )


    price_range = st.slider(
        "Price Range",
        min_value=minimum_price,
        max_value=maximum_price,
        value=(
            minimum_price,
            maximum_price
        ),
        step=0.1
    )


    filtered = merged.copy()


    if search:

        filtered = filtered[
            filtered[
                "Display Name"
            ]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]


    if len(team_filter) > 0:

        filtered = filtered[
            filtered[
                "Current Team"
            ]
            .isin(
                team_filter
            )
        ]


    if len(position_filter) > 0:

        filtered = filtered[
            filtered[
                "Position"
            ]
            .isin(
                position_filter
            )
        ]


    filtered = filtered[
        (
            filtered["Price"]
            >= price_range[0]
        )
        &
        (
            filtered["Price"]
            <= price_range[1]
        )
    ]


    filtered = (
        filtered
        .sort_values(
            "Yaya Rating",
            ascending=False,
            na_position="last"
        )
    )


    table_html = (
        '<div class="table-wrap">'
        '<table class="yaya-table">'
        '<thead>'
        '<tr>'
        '<th>Name</th>'
        '<th>Team</th>'
        '<th>Position</th>'
        '<th>Price</th>'
        '<th>Overall Avg FPT</th>'
        '<th>Minutes</th>'
        '<th>FPT/Min</th>'
        '<th>Games</th>'
        '<th>Yaya Rating</th>'
        '</tr>'
        '</thead>'
        '<tbody>'
    )


    for _, row in filtered.iterrows():

        table_html += (
            '<tr>'

            '<td class="player-cell">'
            + html.escape(
                str(
                    row["Player"]
                )
            )
            + '</td>'

            '<td>'
            + html.escape(
                str(
                    row["Current Team"]
                )
            )
            + '</td>'

            '<td>'
            + html.escape(
                str(
                    row["Position"]
                )
            )
            + '</td>'

            '<td>'
            + display_number(
                row["Price"],
                1
            )
            + '</td>'

            '<td>'
            + display_number(
                row[
                    "Overall Avg FPT"
                ],
                2
            )
            + '</td>'

            '<td>'
            + display_number(
                row["Minutes"],
                1
            )
            + '</td>'

            '<td>'
            + display_number(
                row[
                    "FPT per Minute"
                ],
                2
            )
            + '</td>'

            '<td>'
            + display_integer(
                row[
                    "Games Played"
                ]
            )
            + '</td>'

            '<td class="rating-cell">'
            + rating_display(
                row[
                    "Yaya Rating"
                ]
            )
            + '</td>'

            '</tr>'
        )


    table_html += (
        '</tbody>'
        '</table>'
        '</div>'
    )


    st.markdown(
        table_html,
        unsafe_allow_html=True
    )


# =========================================================
# HEAD TO HEAD
# =========================================================

with tab_compare:

    st.markdown(
        '<div class="section-title">Head-to-Head Comparison</div>',
        unsafe_allow_html=True
    )


    player_names = sorted(
        merged[
            "Display Name"
        ]
        .dropna()
        .tolist()
    )


    if (
        "Sasha Vezenkov"
        in player_names
    ):

        player1_default = (
            player_names.index(
                "Sasha Vezenkov"
            )
        )

    else:

        player1_default = 0


    if (
        "Elijah Bryant"
        in player_names
    ):

        player2_default = (
            player_names.index(
                "Elijah Bryant"
            )
        )

    elif len(player_names) > 1:

        player2_default = 1

    else:

        player2_default = 0


    select1, select2 = (
        st.columns(2)
    )


    with select1:

        player1_name = (
            st.selectbox(
                "Player 1",
                player_names,
                index=player1_default
            )
        )


    with select2:

        player2_name = (
            st.selectbox(
                "Player 2",
                player_names,
                index=player2_default
            )
        )


    p1 = merged[
        merged[
            "Display Name"
        ]
        == player1_name
    ].iloc[0]


    p2 = merged[
        merged[
            "Display Name"
        ]
        == player2_name
    ].iloc[0]


    card1, card2 = (
        st.columns(2)
    )


    # =====================================================
    # PLAYER 1 CARD
    # =====================================================

    player1_card = (
        '<div class="compare-card">'

        '<div class="compare-name">'
        + html.escape(
            str(
                p1["Player"]
            )
        )
        + '</div>'

        '<div class="compare-meta">'
        + html.escape(
            str(
                p1["Current Team"]
            )
        )
        + ' &nbsp;•&nbsp; '
        + html.escape(
            str(
                p1["Position"]
            )
        )
        + ' &nbsp;•&nbsp; Price '
        + display_number(
            p1["Price"],
            1
        )
        + '</div>'

        '<div class="compare-rating">'
        + rating_display(
            p1[
                "Yaya Rating"
            ]
        )
        + '</div>'

        '<div class="rating-caption">'
        'YAYA RATING'
        '</div>'

        + labels_html(
            p1[
                "Experience Labels"
            ]
        )

        + '</div>'
    )


    with card1:

        st.markdown(
            player1_card,
            unsafe_allow_html=True
        )


    # =====================================================
    # PLAYER 2 CARD
    # =====================================================

    player2_card = (
        '<div class="compare-card">'

        '<div class="compare-name">'
        + html.escape(
            str(
                p2["Player"]
            )
        )
        + '</div>'

        '<div class="compare-meta">'
        + html.escape(
            str(
                p2["Current Team"]
            )
        )
        + ' &nbsp;•&nbsp; '
        + html.escape(
            str(
                p2["Position"]
            )
        )
        + ' &nbsp;•&nbsp; Price '
        + display_number(
            p2["Price"],
            1
        )
        + '</div>'

        '<div class="compare-rating">'
        + rating_display(
            p2[
                "Yaya Rating"
            ]
        )
        + '</div>'

        '<div class="rating-caption">'
        'YAYA RATING'
        '</div>'

        + labels_html(
            p2[
                "Experience Labels"
            ]
        )

        + '</div>'
    )


    with card2:

        st.markdown(
            player2_card,
            unsafe_allow_html=True
        )


    # =====================================================
    # WARNINGS
    # =====================================================

    for player in [p1, p2]:

        if player["Team Changed"]:

            old_team = str(
                player["Team"]
            )

            new_team = str(
                player[
                    "Current Team"
                ]
            )

            warning = (
                '<div class="yellow-warning">'
                '⚠️ <b>'
                + html.escape(
                    str(
                        player[
                            "Display Name"
                        ]
                    )
                )
                + '</b> changed teams: '
                + html.escape(
                    old_team
                )
                + ' → '
                + html.escape(
                    new_team
                )
                + '. Historical performance may not fully represent '
                + 'the player&apos;s role with the new team.'
                + '</div>'
            )

            st.markdown(
                warning,
                unsafe_allow_html=True
            )


        if (
            not player[
                "Has Historical Data"
            ]
            and player[
                "Is Experience Player"
            ]
        ):

            warning = (
                '<div class="yellow-warning">'
                '⚠️ <b>'
                + html.escape(
                    str(
                        player[
                            "Display Name"
                        ]
                    )
                )
                + '</b> does not have sufficient historical Fantasy data. '
                + 'The Yaya Rating is currently based on experience, '
                + 'price and projected team role.'
                + '</div>'
            )

            st.markdown(
                warning,
                unsafe_allow_html=True
            )


    # =====================================================
    # COMPARISON TABLE
    # =====================================================

    comparison_rows = [

        (
            "Name",
            p1["Player"],
            p2["Player"]
        ),

        (
            "Team",
            p1["Current Team"],
            p2["Current Team"]
        ),

        (
            "Position",
            p1["Position"],
            p2["Position"]
        ),

        (
            "Price",
            display_number(
                p1["Price"],
                1
            ),
            display_number(
                p2["Price"],
                1
            )
        ),

        (
            "Overall Avg FPT",
            display_number(
                p1[
                    "Overall Avg FPT"
                ],
                2
            ),
            display_number(
                p2[
                    "Overall Avg FPT"
                ],
                2
            )
        ),

        (
            "Minutes",
            display_number(
                p1["Minutes"],
                1
            ),
            display_number(
                p2["Minutes"],
                1
            )
        ),

        (
            "FPT/Min",
            display_number(
                p1[
                    "FPT per Minute"
                ],
                2
            ),
            display_number(
                p2[
                    "FPT per Minute"
                ],
                2
            )
        ),

        (
            "Games",
            display_integer(
                p1[
                    "Games Played"
                ]
            ),
            display_integer(
                p2[
                    "Games Played"
                ]
            )
        ),

        (
            "Yaya Rating",
            rating_display(
                p1[
                    "Yaya Rating"
                ]
            ),
            rating_display(
                p2[
                    "Yaya Rating"
                ]
            )
        )
    ]


    comparison_html = (
        '<div class="table-wrap" '
        'style="margin-top:20px; max-height:none;">'

        '<table class="yaya-table">'

        '<thead>'
        '<tr>'
        '<th>Category</th>'
        '<th>'
        + html.escape(
            str(
                p1["Display Name"]
            )
        )
        + '</th>'
        '<th>'
        + html.escape(
            str(
                p2["Display Name"]
            )
        )
        + '</th>'
        '</tr>'
        '</thead>'

        '<tbody>'
    )


    for category, value1, value2 in comparison_rows:

        class1 = ""
        class2 = ""

        if category == "Yaya Rating":

            class1 = (
                "rating-cell"
            )

            class2 = (
                "rating-cell"
            )


        comparison_html += (
            '<tr>'

            '<td><b>'
            + html.escape(
                str(
                    category
                )
            )
            + '</b></td>'

            '<td class="'
            + class1
            + '">'
            + html.escape(
                str(
                    value1
                )
            )
            + '</td>'

            '<td class="'
            + class2
            + '">'
            + html.escape(
                str(
                    value2
                )
            )
            + '</td>'

            '</tr>'
        )


    comparison_html += (
        '</tbody>'
        '</table>'
        '</div>'
    )


    st.markdown(
        comparison_html,
        unsafe_allow_html=True
    )
