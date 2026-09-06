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

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(circle at 15% 10%, rgba(0, 255, 135, 0.08), transparent 28%),
            radial-gradient(circle at 85% 20%, rgba(0, 180, 100, 0.06), transparent 25%),
            linear-gradient(180deg, #07100d 0%, #050806 45%, #020403 100%);
        color: white;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1.3rem;
        padding-bottom: 3rem;
    }

    /* HERO */

    .hero {
        position: relative;
        min-height: 245px;
        border-radius: 28px;
        overflow: hidden;
        padding: 42px 46px;
        margin-bottom: 20px;

        background:
            radial-gradient(circle at 18% 100%, rgba(0,255,140,.22), transparent 38%),
            radial-gradient(circle at 78% 20%, rgba(0,255,120,.13), transparent 28%),
            linear-gradient(120deg, rgba(5,25,17,.98), rgba(3,8,6,.98));

        border: 1px solid rgba(54,255,154,.22);

        box-shadow:
            0 30px 80px rgba(0,0,0,.48),
            inset 0 0 60px rgba(0,255,130,.035);
    }

    .hero:before {
        content: "";
        position: absolute;
        width: 390px;
        height: 390px;
        border: 2px solid rgba(80,255,165,.10);
        border-radius: 50%;
        right: 110px;
        top: -165px;
    }

    .hero:after {
        content: "";
        position: absolute;
        width: 2px;
        height: 100%;
        background: rgba(70,255,160,.08);
        right: 305px;
        top: 0;
    }

    .court-line {
        position: absolute;
        width: 230px;
        height: 115px;
        border: 2px solid rgba(80,255,165,.08);
        border-bottom: none;
        border-radius: 230px 230px 0 0;
        right: 170px;
        bottom: -2px;
    }

    .hero-title {
        position: relative;
        z-index: 2;
        font-size: 58px;
        line-height: 1;
        font-weight: 950;
        letter-spacing: -2.5px;
        color: #f7fff9;
        margin-top: 16px;
    }

    .hero-title span {
        color: #42f58d;
        text-shadow: 0 0 25px rgba(50,255,145,.20);
    }

    .hero-subtitle {
        position: relative;
        z-index: 2;
        color: #a8b8af;
        font-size: 19px;
        margin-top: 14px;
        letter-spacing: .5px;
    }

    .hero-tag {
        position: relative;
        z-index: 2;
        display: inline-block;
        background: rgba(52,245,137,.10);
        color: #55f49a;
        border: 1px solid rgba(75,255,155,.20);
        padding: 7px 13px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 850;
        letter-spacing: 1.2px;
    }

    .hero-words {
        position: absolute;
        z-index: 3;
        right: 34px;
        top: 32px;
        text-align: right;
        font-size: 13px;
        line-height: 2.15;
        font-weight: 900;
        letter-spacing: 3px;
        color: rgba(111,255,177,.56);
    }

    /* WARNING */

    .global-warning,
    .yellow-warning {
        background: rgba(255,193,7,.09);
        border: 1px solid rgba(255,203,46,.34);
        border-left: 4px solid #ffd447;
        border-radius: 13px;
        color: #ffe69a;
        padding: 12px 15px;
        margin: 10px 0 16px 0;
        font-size: 14px;
    }

    /* TABS */

    [data-baseweb="tab-list"] {
        gap: 14px;
        background: rgba(7,18,13,.80);
        padding: 8px;
        border-radius: 17px;
        border: 1px solid rgba(70,255,155,.10);
    }

    [data-baseweb="tab-list"] button {
        flex: 1;
    }

    [data-baseweb="tab"] {
        height: 62px;
        padding: 0 32px;
        border-radius: 13px;
        background: rgba(13,31,22,.80);
        border: 1px solid rgba(70,255,155,.10);
        font-size: 17px;
        font-weight: 850;
        color: #b9c9c0;
    }

    [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(
            135deg,
            rgba(22,137,75,.95),
            rgba(25,203,105,.85)
        );
        color: white;
        border: 1px solid rgba(90,255,165,.45);
        box-shadow: 0 8px 25px rgba(0,255,130,.12);
    }

    [data-baseweb="tab-highlight"] {
        display: none;
    }

    /* FILTERS */

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background: #0c1712 !important;
        border-color: rgba(80,255,160,.15) !important;
    }

    /* TABLE */

    .table-wrap {
        width: 100%;
        overflow-x: auto;
        max-height: 720px;
        overflow-y: auto;
        border-radius: 18px;
        border: 1px solid rgba(72,255,155,.12);
        background: rgba(5,12,9,.90);
        box-shadow: 0 20px 50px rgba(0,0,0,.25);
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
        background: #10231a;
        color: #5cf49e;
        padding: 15px 13px;
        text-align: left;
        border-bottom: 1px solid rgba(75,255,155,.20);
        font-size: 12px;
        letter-spacing: .4px;
        text-transform: uppercase;
    }

    .yaya-table td {
        padding: 13px;
        border-bottom: 1px solid rgba(255,255,255,.045);
        color: #dce7e1;
    }

    .yaya-table tr:hover td {
        background: rgba(45,245,130,.045);
    }

    .player-cell {
        color: white !important;
        font-weight: 800;
    }

    .rating-cell {
        color: #50f294 !important;
        font-weight: 950;
        font-size: 15px;
    }

    /* H2H */

    .compare-card {
        background:
            radial-gradient(circle at 10% 0%, rgba(38,245,128,.07), transparent 35%),
            linear-gradient(145deg, rgba(12,28,20,.96), rgba(5,11,8,.96));
        border: 1px solid rgba(70,255,155,.13);
        border-radius: 20px;
        padding: 22px;
        min-height: 150px;
        box-shadow: 0 18px 45px rgba(0,0,0,.22);
    }

    .compare-name {
        font-size: 26px;
        font-weight: 950;
        color: white;
        margin-bottom: 6px;
    }

    .compare-meta {
        color: #91a69a;
        font-size: 14px;
    }

    .compare-rating {
        font-size: 37px;
        font-weight: 950;
        color: #4bf393;
        margin-top: 12px;
    }

    .badge {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        margin-right: 6px;
        margin-top: 10px;
        font-size: 11px;
        font-weight: 900;
        letter-spacing: .3px;
        border: 1px solid rgba(255,255,255,.12);
    }

    .badge-high {
        background: rgba(48,239,134,.12);
        color: #59f59b;
        border-color: rgba(60,255,150,.24);
    }

    .badge-low {
        background: rgba(64,161,255,.11);
        color: #8bc6ff;
        border-color: rgba(100,180,255,.23);
    }

    .badge-zero {
        background: rgba(255,193,7,.11);
        color: #ffd96b;
        border-color: rgba(255,205,70,.28);
    }

    .section-title {
        font-size: 25px;
        font-weight: 950;
        margin: 20px 0 12px 0;
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-tag">EUROLEAGUE FANTASY ANALYTICS</div>

        <div class="hero-title">
            Yaya's <span>Rating</span>
        </div>

        <div class="hero-subtitle">
            Data-driven EuroLeague Fantasy player analysis
        </div>

        <div class="court-line"></div>

        <div class="hero-words">
            PLAY<br>
            ANALYZE<br>
            COMPARE<br>
            WIN
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="global-warning">
    ⚠️ Past performance is only a reference point.
    Historical Fantasy numbers do not guarantee how a player will perform
    in the upcoming season.
    </div>
    """,
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

    text = re.sub(
        r"[^a-z0-9\\s]",
        " ",
        text
    )

    text = " ".join(text.split())

    return text


# Manual spelling corrections only.
# We do NOT use dangerous initial/surname guessing.

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
# EXPERIENCE SCORES
# =========================================================
#
# These scores are ONLY for players who do not have
# sufficient historical Fantasy data.
#
# NBA:
# 5 = >500 NBA games
# 4 = >40 NBA and NBA >= 2 x G League
# 3 = >40 NBA but NBA < 2 x G League
# 2 = at least 1 NBA game
# 1 = G League only
# 0 = neither
#
# EUROPE:
# 5 = >100 EuroLeague games
# 4 = at least 1 EuroLeague game
# 3 = selected European experience
# 0 = none
#
# The values below also include the user's manual decisions.
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

    # Manual decision by Yaya:
    "Max Shulga": 5,

    "Yvon Pons": 2,

    "Justin Minaya": 3,

    "Davion Mintz": 1,

    "Tyler Ennis": 3,

    "Nikola Djurisic": 1
}


EUROPE_EXPERIENCE = {

    # 5 - High EuroLeague experience
    "Guerschon Yabusele": 5,
    "Ante Zizic": 5,
    "Johannes Thiemann": 5,
    "Joffrey Lauvergne": 5,

    "Rokas Jokubaitis": 5,
    "Scottie Wilbekin": 5,
    "Mam Jaiteh": 5,
    "Sertaç Şanlı": 5,

    # 4 - EuroLeague experience
    "Jonas Valanciunas": 4,
    "Dario Saric": 4,

    # Blazevic correction
    "Marek Blazevic": 4,

    "David DeJulius": 4,
    "Mathis Dossou-Yovo": 4,
    "Furkan Korkmaz": 4,
    "Olek Balcerowski": 4,

    "Vitto Brown": 4,
    "Yoan Makoundou": 4,

    "Agustin Ubal": 4,
    "Nobel Boungou-Colo": 4,
    "Eli Ndiaye": 4,

    "Eleftherios Mantzoukas": 4,
    "Berk Ugurlu": 4,
    "Tommaso Baldasso": 4,
    "Dimitris Moraitis": 4,
    "Oz Blayzer": 4,

    # 3 - Manual European experience list
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
# CLEAN DATA
# =========================================================

old["Name Key"] = old["Full Name"].apply(
    normalize_name
)

new["Name Key"] = new["Current Name"].apply(
    normalize_name
)


new["Match Key"] = new["Name Key"].apply(
    lambda x: NAME_ALIASES.get(x, x)
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


merged["Display Name"] = merged["Current Name"]


merged["Current Team"] = (
    merged["Team Code"]
    .map(TEAM_NAMES)
    .fillna(merged["Team Code"])
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
# NUMERIC DATA
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
    (merged["Floor Rate % (FPT<8)"] <= 10)
    &
    (merged["Ceiling Rate % (FPT>=20)"] > 40)
)


merged["Player"] = merged["Display Name"]


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

    for i in range(len(points) - 1):

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
                + ratio * (y2 - y1)
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
        ["Team Code", "Position"]
    )["Price"]
    .rank(
        method="max",
        ascending=False
    )
)


def team_role_score(row):

    price = row["Price"]
    rank = row["Role Rank"]

    if pd.isna(price) or pd.isna(rank):
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


merged["Team Role Score"] = merged.apply(
    team_role_score,
    axis=1
)


# =========================================================
# HISTORICAL YAYA RATING
# =========================================================

merged["Production Score"] = (
    merged["Overall Avg FPT"]
    .apply(
        lambda x:
        linear_score(
            x,
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
        lambda x:
        linear_score(
            x,
            VALUE_POINTS
        )
    )
)


merged["Stability Score"] = (
    merged["FPT Std Dev"]
    .apply(
        lambda x:
        linear_score(
            x,
            STABILITY_POINTS
        )
    )
)


merged["Floor Score"] = (
    merged["Floor Rate % (FPT<8)"]
    .apply(
        lambda x:
        linear_score(
            x,
            FLOOR_POINTS
        )
    )
)


merged["Minutes Score"] = (
    merged["Minutes"]
    .apply(
        lambda x:
        linear_score(
            x,
            MINUTES_POINTS
        )
    )
)


merged["Efficiency Score"] = (
    merged["FPT per Minute"]
    .apply(
        lambda x:
        linear_score(
            x,
            EFFICIENCY_POINTS
        )
    )
)


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

    return round(rating, 2)


merged["Historical Rating"] = merged.apply(
    historical_rating,
    axis=1
)


# =========================================================
# EXPERIENCE DATA
# =========================================================

def experience_name(name):

    key = normalize_name(name)

    if key == normalize_name("Antony Brown"):
        return "Anthony Brown"

    if key == normalize_name("D.J. Stewart"):
        return "D.J. Steward"

    if key == normalize_name("Bobi Gach"):
        return "Both Gach"

    if key == normalize_name("Olivier Nkamboua"):
        return "Olivier Nkamhoua"

    return name


merged["Experience Name"] = (
    merged["Display Name"]
    .apply(experience_name)
)


merged["NBA Experience"] = (
    merged["Experience Name"]
    .map(NBA_EXPERIENCE)
    .fillna(0)
)


merged["Europe Experience"] = (
    merged["Experience Name"]
    .map(EUROPE_EXPERIENCE)
    .fillna(0)
)


merged["Experience Score"] = (
    merged["NBA Experience"]
    + merged["Europe Experience"]
)


# =========================================================
# EXPERIENCE LABELS
# =========================================================

def get_labels(row):

    nba = row["NBA Experience"]
    europe = row["Europe Experience"]

    labels = []

    if nba == 0 and europe == 0:
        return ["Not Expected to Play"]

    if nba > 3:
        labels.append(
            "High NBA Experience"
        )

    elif nba > 0:
        labels.append(
            "Low NBA Experience"
        )

    if europe > 3:
        labels.append(
            "High European Experience"
        )

    elif europe > 0:
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
# NEW PLAYER PRICE SCORE
# =========================================================
#
# Lower price = better score for a player whose historical
# Fantasy production is unavailable.
# =========================================================

def budget_score(price):

    if pd.isna(price):
        return 0

    if price <= 4:
        return 10

    if price >= 17:
        return 0

    return (
        10
        - (
            (price - 4)
            / (17 - 4)
        ) * 10
    )


merged["Budget Score"] = (
    merged["Price"]
    .apply(budget_score)
)


# =========================================================
# EXPERIENCE-BASED RATING
# =========================================================

def experience_rating(row):

    experience = row["Experience Score"]

    if experience == 0:
        return 0.0

    rating = (
        experience * 0.50
        + row["Team Role Score"] * 0.30
        + row["Budget Score"] * 0.20
    )

    return round(rating, 2)


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
        return row["Historical Rating"]

    return row["Experience Rating"]


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

    return str(int(value))


def rating_display(value):

    if pd.isna(value):
        return "N/A"

    return f"{value:.2f}"


def labels_html(labels):

    output = ""

    for label in labels:

        if label == "Not Expected to Play":

            css = "badge-zero"

        elif label.startswith("High"):

            css = "badge-high"

        else:

            css = "badge-low"

        output += (
            '<span class="badge '
            + css
            + '">'
            + html.escape(label)
            + "</span>"
        )

    return output


# =========================================================
# TABS
# =========================================================

tab_database, tab_compare = st.tabs(
    [
        "🏀  Player Database",
        "⚔️  Head-to-Head Comparison"
    ]
)


# =========================================================
# PLAYER DATABASE
# =========================================================

with tab_database:

    st.markdown(
        '<div class="section-title">'
        'Player Database'
        '</div>',
        unsafe_allow_html=True
    )

    filter1, filter2, filter3 = st.columns(
        [1.4, 1, 1]
    )


    with filter1:

        search = st.text_input(
            "Search Player",
            placeholder="Type a player name..."
        )


    teams = sorted(
        merged["Current Team"]
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
        merged["Position"]
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
        merged["Price"].min()
    )

    maximum_price = float(
        merged["Price"].max()
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
            filtered["Display Name"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]


    if len(team_filter) > 0:

        filtered = filtered[
            filtered["Current Team"]
            .isin(team_filter)
        ]


    if len(position_filter) > 0:

        filtered = filtered[
            filtered["Position"]
            .isin(position_filter)
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


    filtered = filtered.sort_values(
        "Yaya Rating",
        ascending=False,
        na_position="last"
    )


    table = """
    <div class="table-wrap">
    <table class="yaya-table">
    <thead>
    <tr>
        <th>Name</th>
        <th>Team</th>
        <th>Position</th>
        <th>Price</th>
        <th>Overall Avg FPT</th>
        <th>Minutes</th>
        <th>FPT/Min</th>
        <th>Games</th>
        <th>Yaya Rating</th>
    </tr>
    </thead>
    <tbody>
    """


    for _, row in filtered.iterrows():

        table += "<tr>"

        table += (
            '<td class="player-cell">'
            + html.escape(
                str(row["Player"])
            )
            + "</td>"
        )

        table += (
            "<td>"
            + html.escape(
                str(row["Current Team"])
            )
            + "</td>"
        )

        table += (
            "<td>"
            + html.escape(
                str(row["Position"])
            )
            + "</td>"
        )

        table += (
            "<td>"
            + display_number(
                row["Price"],
                1
            )
            + "</td>"
        )

        table += (
            "<td>"
            + display_number(
                row["Overall Avg FPT"],
                2
            )
            + "</td>"
        )

        table += (
            "<td>"
            + display_number(
                row["Minutes"],
                1
            )
            + "</td>"
        )

        table += (
            "<td>"
            + display_number(
                row["FPT per Minute"],
                2
            )
            + "</td>"
        )

        table += (
            "<td>"
            + display_integer(
                row["Games Played"]
            )
            + "</td>"
        )

        table += (
            '<td class="rating-cell">'
            + rating_display(
                row["Yaya Rating"]
            )
            + "</td>"
        )

        table += "</tr>"


    table += """
    </tbody>
    </table>
    </div>
    """


    st.markdown(
        table,
        unsafe_allow_html=True
    )


# =========================================================
# HEAD TO HEAD
# =========================================================

with tab_compare:

    st.markdown(
        '<div class="section-title">'
        'Head-to-Head Comparison'
        '</div>',
        unsafe_allow_html=True
    )


    player_names = sorted(
        merged["Display Name"]
        .dropna()
        .tolist()
    )


    if "Sasha Vezenkov" in player_names:

        player1_default = (
            player_names.index(
                "Sasha Vezenkov"
            )
        )

    else:

        player1_default = 0


    if "Elijah Bryant" in player_names:

        player2_default = (
            player_names.index(
                "Elijah Bryant"
            )
        )

    elif len(player_names) > 1:

        player2_default = 1

    else:

        player2_default = 0


    select1, select2 = st.columns(2)


    with select1:

        player1_name = st.selectbox(
            "Player 1",
            player_names,
            index=player1_default
        )


    with select2:

        player2_name = st.selectbox(
            "Player 2",
            player_names,
            index=player2_default
        )


    p1 = merged[
        merged["Display Name"]
        == player1_name
    ].iloc[0]


    p2 = merged[
        merged["Display Name"]
        == player2_name
    ].iloc[0]


    card1, card2 = st.columns(2)


    with card1:

        st.markdown(
            f"""
            <div class="compare-card">

                <div class="compare-name">
                    {html.escape(str(p1["Player"]))}
                </div>

                <div class="compare-meta">
                    {html.escape(str(p1["Current Team"]))}
                    &nbsp; • &nbsp;
                    {html.escape(str(p1["Position"]))}
                    &nbsp; • &nbsp;
                    Price {display_number(p1["Price"], 1)}
                </div>

                <div class="compare-rating">
                    {rating_display(p1["Yaya Rating"])}
                </div>

                {labels_html(p1["Experience Labels"])}

            </div>
            """,
            unsafe_allow_html=True
        )


    with card2:

        st.markdown(
            f"""
            <div class="compare-card">

                <div class="compare-name">
                    {html.escape(str(p2["Player"]))}
                </div>

                <div class="compare-meta">
                    {html.escape(str(p2["Current Team"]))}
                    &nbsp; • &nbsp;
                    {html.escape(str(p2["Position"]))}
                    &nbsp; • &nbsp;
                    Price {display_number(p2["Price"], 1)}
                </div>

                <div class="compare-rating">
                    {rating_display(p2["Yaya Rating"])}
                </div>

                {labels_html(p2["Experience Labels"])}

            </div>
            """,
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
                player["Current Team"]
            )

            st.markdown(
                f"""
                <div class="yellow-warning">
                ⚠️ <b>{html.escape(str(player["Display Name"]))}</b>
                changed teams:
                {html.escape(old_team)}
                → {html.escape(new_team)}.
                Historical performance may not fully represent
                the player's new role.
                </div>
                """,
                unsafe_allow_html=True
            )


        if not player["Has Historical Data"]:

            st.markdown(
                f"""
                <div class="yellow-warning">
                ⚠️ <b>{html.escape(str(player["Display Name"]))}</b>
                does not have sufficient historical Fantasy data.
                The Yaya Rating shown here is based on
                experience, current price and projected team role.
                </div>
                """,
                unsafe_allow_html=True
            )


    # =====================================================
    # H2H TABLE
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
                p1["Overall Avg FPT"],
                2
            ),
            display_number(
                p2["Overall Avg FPT"],
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
                p1["FPT per Minute"],
                2
            ),
            display_number(
                p2["FPT per Minute"],
                2
            )
        ),

        (
            "Games",
            display_integer(
                p1["Games Played"]
            ),
            display_integer(
                p2["Games Played"]
            )
        ),

        (
            "Yaya Rating",
            rating_display(
                p1["Yaya Rating"]
            ),
            rating_display(
                p2["Yaya Rating"]
            )
        )
    ]


    comparison_table = """
    <div class="table-wrap"
         style="margin-top:18px; max-height:none;">
    <table class="yaya-table">
    <thead>
    <tr>
        <th>Category</th>
        <th>Player 1</th>
        <th>Player 2</th>
    </tr>
    </thead>
    <tbody>
    """


    for category, value1, value2 in comparison_rows:

        class1 = ""
        class2 = ""

        if category == "Yaya Rating":

            class1 = "rating-cell"
            class2 = "rating-cell"


        comparison_table += (
            "<tr>"
            "<td><b>"
            + html.escape(
                str(category)
            )
            + "</b></td>"
            + '<td class="'
            + class1
            + '">'
            + html.escape(
                str(value1)
            )
            + "</td>"
            + '<td class="'
            + class2
            + '">'
            + html.escape(
                str(value2)
            )
            + "</td>"
            + "</tr>"
        )


    comparison_table += """
    </tbody>
    </table>
    </div>
    """


    st.markdown(
        comparison_table,
        unsafe_allow_html=True
    )
