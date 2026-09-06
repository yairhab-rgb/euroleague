import pandas as pd
import streamlit as st
import unicodedata
import re
import html


# ==================================================
# PAGE SETTINGS
# ==================================================

st.set_page_config(
    page_title="Yaya's Rating",
    page_icon="🏀",
    layout="wide"
)


# ==================================================
# DESIGN
# ==================================================

st.markdown("""
<style>

/* ==================================================
   GLOBAL
================================================== */

.stApp {
    background:
        radial-gradient(
            circle at 78% 4%,
            rgba(31, 224, 154, 0.11),
            transparent 25%
        ),
        radial-gradient(
            circle at 95% 40%,
            rgba(31, 224, 154, 0.05),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #05090d 0%,
            #081017 52%,
            #06110f 100%
        );

    color: #f5f8fa;
}


.block-container {
    max-width: 1500px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}


/* ==================================================
   FONT
================================================== */

html,
body,
div,
span,
p,
input,
button,
select,
textarea {
    font-family:
        "Segoe UI",
        Arial,
        Helvetica,
        sans-serif;
}


/* ==================================================
   HERO
================================================== */

.hero {
    position: relative;

    overflow: hidden;

    min-height: 280px;

    padding:
        42px 46px;

    margin-bottom:
        24px;

    border:
        1px solid #233944;

    border-radius:
        18px;

    background:
        radial-gradient(
            circle at 70% 70%,
            rgba(31, 224, 154, 0.13),
            transparent 32%
        ),
        linear-gradient(
            110deg,
            rgba(8, 15, 21, 0.99),
            rgba(7, 28, 24, 0.96)
        );

    box-shadow:
        0 18px 45px rgba(0, 0, 0, 0.30);
}


/* basketball-court style decoration */

.hero::after {
    content: "";

    position: absolute;

    width: 520px;
    height: 300px;

    right: -60px;
    bottom: -130px;

    border:
        2px solid rgba(40, 227, 159, 0.10);

    border-radius:
        50%;

    transform:
        rotate(-8deg);
}


.hero::before {
    content: "";

    position: absolute;

    width: 420px;
    height: 2px;

    right: 30px;
    bottom: 75px;

    background:
        rgba(40, 227, 159, 0.10);

    transform:
        rotate(-8deg);
}


.hero-content {
    position: relative;
    z-index: 2;
}


.hero-title {
    margin-bottom:
        10px;

    font-size:
        64px;

    line-height:
        1;

    font-weight:
        900;

    letter-spacing:
        -2.5px;
}


.hero-yaya {
    color:
        #ffffff;
}


.hero-rating {
    color:
        #27e5a1;

    text-shadow:
        0 0 30px rgba(39, 229, 161, 0.18);
}


.hero-subtitle {
    margin-bottom:
        20px;

    color:
        #f3f7f9;

    font-size:
        22px;

    font-weight:
        750;
}


.hero-text {
    max-width:
        900px;

    color:
        #bac7cf;

    font-size:
        16px;

    line-height:
        1.75;
}


.hero-side-text {
    position:
        absolute;

    right:
        55px;

    top:
        48px;

    z-index:
        2;

    text-align:
        right;

    color:
        #9df8d8;

    font-size:
        13px;

    line-height:
        1.8;

    letter-spacing:
        3px;
}


/* ==================================================
   GLOBAL WARNING
================================================== */

.global-warning {
    position: relative;

    z-index: 2;

    margin-top:
        26px;

    padding:
        13px 16px;

    max-width:
        940px;

    border:
        1px solid rgba(255, 201, 71, 0.52);

    border-radius:
        10px;

    background:
        rgba(255, 193, 7, 0.09);

    color:
        #ffd86b;

    font-size:
        14px;

    line-height:
        1.55;
}


/* ==================================================
   HEADINGS
================================================== */

h1,
h2,
h3 {
    color:
        #f5f8fa !important;
}


.section-description {
    margin-top:
        -7px;

    margin-bottom:
        24px;

    color:
        #9aabb6;

    font-size:
        15px;
}


/* ==================================================
   TABS
================================================== */

div[data-baseweb="tab-list"] {
    gap:
        8px;

    border-bottom:
        1px solid #142029;
}


button[data-baseweb="tab"] {
    min-width:
        170px;

    padding:
        12px 20px;

    border:
        1px solid #22333d;

    border-radius:
        9px 9px 0 0;

    background:
        #0e171e;
}


button[data-baseweb="tab"] p {
    font-size:
        15px;

    font-weight:
        700;
}


button[data-baseweb="tab"][aria-selected="true"] {
    border:
        1px solid #27e5a1;

    border-bottom-color:
        #27e5a1;

    background:
        linear-gradient(
            180deg,
            #12382f,
            #0e221e
        );
}


button[data-baseweb="tab"][aria-selected="true"] p {
    color:
        #2ce6a4 !important;
}


/* ==================================================
   INPUTS
================================================== */

div[data-baseweb="input"] {
    border:
        1px solid #2a3b45 !important;

    border-radius:
        9px !important;

    background:
        #101a22 !important;
}


div[data-baseweb="input"] input {
    color:
        white !important;

    background:
        transparent !important;
}


div[data-baseweb="input"]:focus-within {
    border-color:
        #27e5a1 !important;

    box-shadow:
        0 0 0 1px rgba(39, 229, 161, 0.15);
}


/* ==================================================
   SELECT BOXES
================================================== */

div[data-baseweb="select"] > div {
    border:
        1px solid #2a3b45 !important;

    border-radius:
        9px !important;

    background:
        #101a22 !important;

    color:
        white !important;
}


div[data-baseweb="select"] span {
    color:
        #f4f7f8 !important;
}


/* ==================================================
   DATABASE CARD
================================================== */

.database-card {
    margin-top:
        18px;

    border:
        1px solid #263943;

    border-radius:
        16px;

    overflow:
        hidden;

    background:
        linear-gradient(
            135deg,
            #0d171e,
            #0a1218
        );

    box-shadow:
        0 14px 32px rgba(0, 0, 0, 0.25);
}


.database-scroll {
    max-height:
        660px;

    overflow:
        auto;
}


/* ==================================================
   DATABASE TABLE
================================================== */

.database-table {
    width:
        100%;

    min-width:
        1050px;

    border-collapse:
        collapse;
}


.database-table thead th {
    position:
        sticky;

    top:
        0;

    z-index:
        5;

    padding:
        15px 14px;

    border-bottom:
        1px solid #29404b;

    background:
        #101d25;

    color:
        #a8bac5;

    text-align:
        left;

    font-size:
        12px;

    font-weight:
        800;

    text-transform:
        uppercase;

    letter-spacing:
        0.7px;
}


.database-table tbody td {
    padding:
        14px;

    border-bottom:
        1px solid #192832;

    color:
        #dce6eb;

    font-size:
        14px;
}


.database-table tbody tr {
    transition:
        0.15s ease;
}


.database-table tbody tr:hover {
    background:
        rgba(40, 227, 159, 0.055);
}


.database-table tbody tr:last-child td {
    border-bottom:
        none;
}


.db-player {
    color:
        white !important;

    font-weight:
        750;
}


.db-rating {
    color:
        #2ce6a4 !important;

    font-weight:
        900;

    font-size:
        16px !important;
}


.db-price {
    font-weight:
        700;

    color:
        #e9f1f4 !important;
}


/* ==================================================
   DATABASE INFO BAR
================================================== */

.database-info {
    display:
        flex;

    justify-content:
        space-between;

    align-items:
        center;

    padding:
        13px 16px;

    border-top:
        1px solid #263943;

    background:
        #0d161d;

    color:
        #798b96;

    font-size:
        13px;
}


/* ==================================================
   HEAD TO HEAD
================================================== */

.h2h-wrapper {
    margin-top:
        25px;

    border:
        1px solid #29404b;

    border-radius:
        18px;

    overflow:
        hidden;

    background:
        linear-gradient(
            135deg,
            #0d1820,
            #091217
        );

    box-shadow:
        0 16px 38px rgba(0, 0, 0, 0.28);
}


.h2h-table {
    width:
        100%;

    border-collapse:
        collapse;

    table-layout:
        fixed;
}


.h2h-table th {
    padding:
        28px 18px;

    border-bottom:
        1px solid #2a3f49;

    background:
        linear-gradient(
            180deg,
            #12212a,
            #0d171d
        );

    text-align:
        center;
}


.player-name {
    color:
        #ffffff;

    font-size:
        28px;

    font-weight:
        900;
}


.vs {
    width:
        17%;

    color:
        #28e39f;

    font-size:
        17px;

    font-weight:
        900;

    text-transform:
        uppercase;
}


.h2h-table td {
    padding:
        21px 18px;

    border-bottom:
        1px solid #20313a;

    text-align:
        center;

    font-size:
        19px;
}


.h2h-table tr:last-child td {
    border-bottom:
        none;
}


.stat-name {
    background:
        rgba(255,255,255,0.014);

    color:
        #91a6b1;

    font-size:
        12px !important;

    font-weight:
        800;

    text-transform:
        uppercase;

    letter-spacing:
        0.9px;
}


.stat-value {
    color:
        #e8eff2;

    font-weight:
        700;
}


.winner {
    background:
        linear-gradient(
            90deg,
            rgba(35, 190, 126, 0.08),
            rgba(35, 190, 126, 0.17)
        );

    color:
        #32e7a7 !important;

    font-weight:
        900 !important;
}


.rating-value {
    color:
        #32e7a7 !important;

    font-size:
        27px !important;

    font-weight:
        900 !important;
}


/* ==================================================
   YELLOW WARNINGS
================================================== */

.yellow-warning {
    margin-top:
        16px;

    padding:
        13px 15px;

    border:
        1px solid rgba(255, 201, 71, 0.48);

    border-radius:
        10px;

    background:
        rgba(255, 193, 7, 0.09);

    color:
        #ffd86b;

    font-size:
        14px;

    line-height:
        1.5;
}


/* ==================================================
   FOOTER
================================================== */

.footer {
    margin-top:
        42px;

    padding-top:
        20px;

    padding-bottom:
        10px;

    border-top:
        1px solid #17242c;

    color:
        #667a86;

    text-align:
        center;

    font-size:
        13px;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# LOAD DATA
# ==================================================

old_df = pd.read_csv(
    "fantasy_euroleague_stats.csv"
)

new_df = pd.read_csv(
    "new.csv"
)


# ==================================================
# TEAM NAMES
# ==================================================

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
    "BAY": "Bayern Munich",
    "VIR": "Virtus Bologna",
    "KBA": "Baskonia",
    "MON": "AS Monaco"
}


# ==================================================
# OLD TEAM -> CURRENT TEAM CODE
# ==================================================

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


# ==================================================
# NORMALIZE NAMES
# ==================================================

def normalize_name(value):

    if pd.isna(value):
        return ""

    text = str(value).lower()

    text = unicodedata.normalize(
        "NFKD",
        text
    )

    text = "".join(
        character
        for character in text
        if not unicodedata.combining(character)
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


old_df["Name_Key"] = (
    old_df["Full Name"]
    .apply(normalize_name)
)


new_df["Name_Key"] = (
    new_df["שם שחקן"]
    .apply(normalize_name)
)


# ==================================================
# MANUAL ALIASES
# ==================================================

NAME_ALIASES = {

}


normalized_aliases = {}


for new_name in NAME_ALIASES:

    normalized_aliases[
        normalize_name(new_name)
    ] = normalize_name(
        NAME_ALIASES[new_name]
    )


# ==================================================
# FIND OLD PLAYER
# ==================================================

def find_old_player(new_row):

    name_key = (
        new_row["Name_Key"]
    )


    matches = old_df[
        old_df["Name_Key"]
        ==
        name_key
    ]


    if len(matches) == 1:
        return matches.iloc[0]


    if name_key in normalized_aliases:

        old_key = (
            normalized_aliases[
                name_key
            ]
        )


        matches = old_df[
            old_df["Name_Key"]
            ==
            old_key
        ]


        if len(matches) == 1:
            return matches.iloc[0]


    return None


# ==================================================
# BUILD CURRENT DATABASE
# ==================================================

rows = []


for index in range(
    len(new_df)
):

    new_row = (
        new_df.iloc[index]
    )


    old_player = find_old_player(
        new_row
    )


    team_code = str(
        new_row["שם קבוצה"]
    )


    team_name = TEAM_NAMES.get(
        team_code,
        team_code
    )


    price = pd.to_numeric(
        new_row["מחיר"],
        errors="coerce"
    )


    if old_player is not None:

        old_team = (
            old_player["Team"]
        )


        old_team_code = (
            OLD_TEAM_TO_CODE.get(
                old_team,
                old_team
            )
        )


        team_changed = (
            old_team_code
            !=
            team_code
        )


        row = {

            "Full Name":
                new_row["שם שחקן"],

            "Team":
                team_name,

            "Team Code":
                team_code,

            "Position":
                new_row["עמדה"],

            "Price":
                price,

            "Overall Avg FPT":
                old_player[
                    "Overall Avg FPT"
                ],

            "FPT Std Dev":
                old_player[
                    "FPT Std Dev"
                ],

            "Floor Rate % (FPT<8)":
                old_player[
                    "Floor Rate % (FPT<8)"
                ],

            "Ceiling Rate % (FPT>=20)":
                old_player[
                    "Ceiling Rate % (FPT>=20)"
                ],

            "Total Minutes":
                old_player[
                    "Total Minutes"
                ],

            "FPT per Minute":
                old_player[
                    "FPT per Minute"
                ],

            "Games Played":
                old_player[
                    "Games Played"
                ],

            "Old Team":
                old_team,

            "Team Changed":
                team_changed,

            "Is New Player":
                False
        }


    else:

        row = {

            "Full Name":
                new_row["שם שחקן"],

            "Team":
                team_name,

            "Team Code":
                team_code,

            "Position":
                new_row["עמדה"],

            "Price":
                price,

            "Overall Avg FPT":
                pd.NA,

            "FPT Std Dev":
                pd.NA,

            "Floor Rate % (FPT<8)":
                pd.NA,

            "Ceiling Rate % (FPT>=20)":
                pd.NA,

            "Total Minutes":
                pd.NA,

            "FPT per Minute":
                pd.NA,

            "Games Played":
                pd.NA,

            "Old Team":
                pd.NA,

            "Team Changed":
                False,

            "Is New Player":
                True
        }


    rows.append(row)


df = pd.DataFrame(
    rows
)


# ==================================================
# NUMERIC COLUMNS
# ==================================================

numeric_columns = [

    "Price",

    "Overall Avg FPT",

    "FPT Std Dev",

    "Floor Rate % (FPT<8)",

    "Ceiling Rate % (FPT>=20)",

    "Total Minutes",

    "FPT per Minute",

    "Games Played"
]


for column in numeric_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ==================================================
# MINUTES PER GAME
# ==================================================

df["Minutes"] = (

    df["Total Minutes"]
    /
    df["Games Played"]

)


# ==================================================
# SCORE FUNCTION
# ==================================================

def calculate_score(
    value,
    points
):

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


        if (
            x1
            <=
            value
            <=
            x2
        ):

            score = (

                y1

                +

                (value - x1)

                *

                (y2 - y1)

                /

                (x2 - x1)

            )


            return score


    return pd.NA


# ==================================================
# PRODUCTION
# ==================================================

PRODUCTION_POINTS = [

    (0, 0),

    (5, 2.5),

    (8, 4.5),

    (11, 6.5),

    (14, 8),

    (17, 9),

    (20, 10)
]


df["Production Score"] = (

    df["Overall Avg FPT"]

    .apply(
        lambda x:
        calculate_score(
            x,
            PRODUCTION_POINTS
        )
    )

)


# ==================================================
# VALUE
# ==================================================

df["Value Ratio"] = (

    df["Overall Avg FPT"]
    /
    df["Price"]

)


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


df["Value Score"] = (

    df["Value Ratio"]

    .apply(
        lambda x:
        calculate_score(
            x,
            VALUE_POINTS
        )
    )

)


# ==================================================
# STABILITY
# ==================================================

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


df["Stability Score"] = (

    df["FPT Std Dev"]

    .apply(
        lambda x:
        calculate_score(
            x,
            STABILITY_POINTS
        )
    )

)


# ==================================================
# FLOOR
# ==================================================

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


df["Floor Score"] = (

    df["Floor Rate % (FPT<8)"]

    .apply(
        lambda x:
        calculate_score(
            x,
            FLOOR_POINTS
        )
    )

)


# ==================================================
# MINUTES
# ==================================================

MINUTES_POINTS = [

    (8, 1),

    (12, 3),

    (16, 5),

    (20, 7),

    (24, 9),

    (28, 10)
]


df["Minutes Score"] = (

    df["Minutes"]

    .apply(
        lambda x:
        calculate_score(
            x,
            MINUTES_POINTS
        )
    )

)


# ==================================================
# EFFICIENCY
# ==================================================

EFFICIENCY_POINTS = [

    (0.20, 1),

    (0.30, 3),

    (0.40, 5),

    (0.50, 7),

    (0.65, 9),

    (0.80, 10)
]


df["Efficiency Score"] = (

    df["FPT per Minute"]

    .apply(
        lambda x:
        calculate_score(
            x,
            EFFICIENCY_POINTS
        )
    )

)


# ==================================================
# TEAM ROLE
# ==================================================

df["Team Role Score"] = 0.0


for team_code in (
    df["Team Code"]
    .dropna()
    .unique()
):

    team_players = df[
        df["Team Code"]
        ==
        team_code
    ]


    for position in (
        team_players[
            "Position"
        ]
        .dropna()
        .unique()
    ):

        group = team_players[
            team_players[
                "Position"
            ]
            ==
            position
        ].copy()


        group = group[
            group["Price"]
            .notna()
        ]


        if len(group) == 0:
            continue


        group = (
            group.sort_values(
                "Price",
                ascending=False
            )
        )


        unique_prices = sorted(
            group["Price"].unique(),
            reverse=True
        )


        position_number = 1


        for price in unique_prices:

            same_price = group[
                group["Price"]
                ==
                price
            ]


            amount = len(
                same_price
            )


            last_position = (

                position_number

                +

                amount

                -

                1

            )


            if last_position == 1:

                role_score = 10


            elif last_position == 2:

                role_score = 6


            elif last_position == 3:

                role_score = 3


            else:

                role_score = 0


            if price < 8:

                role_score = 0


            df.loc[
                same_price.index,
                "Team Role Score"
            ] = role_score


            position_number = (
                last_position + 1
            )


# ==================================================
# CAPTAIN
# ==================================================

df["Captain Option"] = (

    (
        df[
            "Floor Rate % (FPT<8)"
        ]
        <=
        10
    )

    &

    (
        df[
            "Ceiling Rate % (FPT>=20)"
        ]
        >
        40
    )

)


# ==================================================
# YAYA RATING
# ==================================================

def calculate_yaya_rating(row):

    required_values = [

        row[
            "Production Score"
        ],

        row[
            "Value Score"
        ],

        row[
            "Stability Score"
        ],

        row[
            "Floor Score"
        ],

        row[
            "Minutes Score"
        ],

        row[
            "Efficiency Score"
        ]

    ]


    for value in required_values:

        if pd.isna(value):
            return pd.NA


    rating = (

        row[
            "Production Score"
        ]
        * 0.25

        +

        row[
            "Value Score"
        ]
        * 0.20

        +

        row[
            "Team Role Score"
        ]
        * 0.25

        +

        row[
            "Stability Score"
        ]
        * 0.06

        +

        row[
            "Floor Score"
        ]
        * 0.04

        +

        row[
            "Minutes Score"
        ]
        * 0.10

        +

        row[
            "Efficiency Score"
        ]
        * 0.10

    )


    # New-team penalty

    if row["Team Changed"]:

        rating = (
            rating
            *
            0.94
        )


    return round(
        rating,
        2
    )


df["Yaya Rating"] = df.apply(
    calculate_yaya_rating,
    axis=1
)


# ==================================================
# DISPLAY NAME
# ==================================================

def display_name(row):

    name = str(
        row["Full Name"]
    )


    if row["Captain Option"]:

        name = (
            name
            +
            "  C"
        )


    return name


df["Display Name"] = df.apply(
    display_name,
    axis=1
)


# ==================================================
# FORMAT FUNCTIONS
# ==================================================

def format_number(
    value,
    decimals=1
):

    if pd.isna(value):
        return "N/A"

    return (
        f"{value:.{decimals}f}"
    )


def format_games(value):

    if pd.isna(value):
        return "N/A"

    return str(
        int(value)
    )


def safe_text(value):

    if pd.isna(value):
        return "N/A"

    return html.escape(
        str(value)
    )


# ==================================================
# HERO
# ==================================================

hero_html = """
<div class="hero">
<div class="hero-content">
<div class="hero-title">
<span class="hero-yaya">Yaya's</span>
<span class="hero-rating">Rating</span>
</div>
<div class="hero-subtitle">EuroLeague Fantasy Player Analytics</div>
<div class="hero-text">
Yaya's Rating is a fantasy-focused player rating built to identify the most valuable EuroLeague players.<br>
The score combines production, efficiency, consistency, playing time, price value and the player's role within his team.<br>
Go beyond the basic Fantasy average and find the players who can give you the edge.
</div>
<div class="global-warning">
⚠️ Past performance is only a reference point. Historical Fantasy numbers do not guarantee how a player will perform in the upcoming season.
</div>
</div>
<div class="hero-side-text">
PLAY<br>
ANALYZE<br>
COMPARE<br>
WIN
</div>
</div>
"""


st.markdown(
    hero_html,
    unsafe_allow_html=True
)


# ==================================================
# TABS
# ==================================================

database_tab, h2h_tab = (
    st.tabs(
        [
            "📊 Player Database",
            "⚔️ Head-to-Head"
        ]
    )
)


# ==================================================
# PLAYER DATABASE
# ==================================================

with database_tab:


    st.header(
        "Player Database"
    )


    st.markdown(
        '<div class="section-description">'
        "Search and explore EuroLeague players "
        "with their key Fantasy statistics and Yaya Rating."
        "</div>",
        unsafe_allow_html=True
    )


    # ==================================================
    # FILTERS
    # ==================================================

    search_col, team_col, position_col = (
        st.columns(
            [
                2.4,
                1,
                1
            ]
        )
    )


    with search_col:

        search = st.text_input(
            "Search",
            placeholder=
                "Search for a player...",
            label_visibility=
                "collapsed"
        )


    team_options = sorted(
        df[
            "Team"
        ]
        .dropna()
        .unique()
    )


    with team_col:

        selected_team = (
            st.selectbox(
                "Team",
                [
                    "All Teams"
                ]
                +
                team_options
            )
        )


    position_options = sorted(
        df[
            "Position"
        ]
        .dropna()
        .unique()
    )


    with position_col:

        selected_position = (
            st.selectbox(
                "Position",
                [
                    "All Positions"
                ]
                +
                position_options
            )
        )


    filtered_df = (
        df.copy()
    )


    if search != "":

        filtered_df = (
            filtered_df[
                filtered_df[
                    "Full Name"
                ]
                .str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]
        )


    if (
        selected_team
        !=
        "All Teams"
    ):

        filtered_df = (
            filtered_df[
                filtered_df[
                    "Team"
                ]
                ==
                selected_team
            ]
        )


    if (
        selected_position
        !=
        "All Positions"
    ):

        filtered_df = (
            filtered_df[
                filtered_df[
                    "Position"
                ]
                ==
                selected_position
            ]
        )


    # Highest rating first

    filtered_df = (
        filtered_df
        .sort_values(
            "Yaya Rating",
            ascending=False,
            na_position="last"
        )
    )


    # ==================================================
    # CUSTOM DARK DATABASE TABLE
    # ==================================================

    database_rows = ""


    ranking_number = 1


    for index in range(
        len(filtered_df)
    ):

        player = (
            filtered_df.iloc[index]
        )


        database_rows += (
            "<tr>"

            f'<td>{ranking_number}</td>'

            f'<td class="db-player">'
            f'{safe_text(player["Display Name"])}'
            f'</td>'

            f'<td>'
            f'{safe_text(player["Team"])}'
            f'</td>'

            f'<td>'
            f'{safe_text(player["Position"])}'
            f'</td>'

            f'<td class="db-price">'
            f'{format_number(player["Price"], 1)}'
            f'</td>'

            f'<td>'
            f'{format_number(player["Overall Avg FPT"], 2)}'
            f'</td>'

            f'<td>'
            f'{format_number(player["Minutes"], 1)}'
            f'</td>'

            f'<td>'
            f'{format_number(player["FPT per Minute"], 2)}'
            f'</td>'

            f'<td>'
            f'{format_games(player["Games Played"])}'
            f'</td>'

            f'<td class="db-rating">'
            f'{format_number(player["Yaya Rating"], 2)}'
            f'</td>'

            "</tr>"
        )


        ranking_number += 1


    database_html = (
        '<div class="database-card">'
        '<div class="database-scroll">'
        '<table class="database-table">'

        '<thead>'
        '<tr>'

        '<th>#</th>'
        '<th>Player</th>'
        '<th>Team</th>'
        '<th>Position</th>'
        '<th>Price</th>'
        '<th>Avg FPT</th>'
        '<th>Minutes</th>'
        '<th>FPT / Min</th>'
        '<th>Games</th>'
        '<th>Yaya Rating</th>'

        '</tr>'
        '</thead>'

        '<tbody>'

        +

        database_rows

        +

        '</tbody>'
        '</table>'
        '</div>'

        '<div class="database-info">'
        f'<span>Showing {len(filtered_df)} players</span>'
        '<span>Sorted by Yaya Rating</span>'
        '</div>'

        '</div>'
    )


    st.markdown(
        database_html,
        unsafe_allow_html=True
    )


# ==================================================
# HEAD TO HEAD
# ==================================================

with h2h_tab:


    st.header(
        "Head-to-Head Comparison"
    )


    st.markdown(
        '<div class="section-description">'
        "Compare two EuroLeague Fantasy players side by side."
        "</div>",
        unsafe_allow_html=True
    )


    player_names = sorted(
        df[
            "Full Name"
        ]
        .dropna()
        .unique()
    )


    # ==================================================
    # DEFAULT PLAYERS
    # ==================================================

    player1_default = 0

    player2_default = 0


    if "Sasha Vezenkov" in player_names:

        player1_default = (
            player_names.index(
                "Sasha Vezenkov"
            )
        )


    if "Elijah Bryant" in player_names:

        player2_default = (
            player_names.index(
                "Elijah Bryant"
            )
        )


    elif len(player_names) > 1:

        player2_default = 1


    # ==================================================
    # PLAYER SELECTORS
    # ==================================================

    player1_col, center_col, player2_col = (
        st.columns(
            [
                1,
                0.12,
                1
            ]
        )
    )


    with player1_col:

        player1_name = (
            st.selectbox(
                "Player 1",
                player_names,
                index=
                    player1_default,
                key=
                    "player1"
            )
        )


    with player2_col:

        player2_name = (
            st.selectbox(
                "Player 2",
                player_names,
                index=
                    player2_default,
                key=
                    "player2"
            )
        )


    player1 = df[
        df["Full Name"]
        ==
        player1_name
    ].iloc[0]


    player2 = df[
        df["Full Name"]
        ==
        player2_name
    ].iloc[0]


    # ==================================================
    # WINNER
    # ==================================================

    def winner_class(
        value1,
        value2,
        side
    ):

        if (
            pd.isna(value1)
            or
            pd.isna(value2)
        ):

            return "stat-value"


        if value1 == value2:

            return "stat-value"


        if (
            side == 1
            and
            value1 > value2
        ):

            return "winner"


        if (
            side == 2
            and
            value2 > value1
        ):

            return "winner"


        return "stat-value"


    # ==================================================
    # COMPARISON ROW
    # ==================================================

    def comparison_row(
        value1,
        label,
        value2,
        decimals=1,
        rating=False
    ):

        left_class = (
            winner_class(
                value1,
                value2,
                1
            )
        )


        right_class = (
            winner_class(
                value1,
                value2,
                2
            )
        )


        if rating:

            left_class += (
                " rating-value"
            )

            right_class += (
                " rating-value"
            )


        left_value = (
            format_number(
                value1,
                decimals
            )
        )


        right_value = (
            format_number(
                value2,
                decimals
            )
        )


        return (
            "<tr>"

            f'<td class="{left_class}">'
            f'{left_value}'
            f'</td>'

            '<td class="stat-name">'
            f'{label}'
            '</td>'

            f'<td class="{right_class}">'
            f'{right_value}'
            f'</td>'

            "</tr>"
        )


    player1_display = (
        safe_text(
            display_name(
                player1
            )
        )
    )


    player2_display = (
        safe_text(
            display_name(
                player2
            )
        )
    )


    # ==================================================
    # HEAD TO HEAD TABLE
    # ==================================================

    table_html = (

        '<div class="h2h-wrapper">'

        '<table class="h2h-table">'

        '<thead>'

        '<tr>'

        '<th>'
        f'<div class="player-name">{player1_display}</div>'
        '</th>'

        '<th class="vs">'
        'VS'
        '</th>'

        '<th>'
        f'<div class="player-name">{player2_display}</div>'
        '</th>'

        '</tr>'

        '</thead>'

        '<tbody>'

        '<tr>'

        f'<td class="stat-value">'
        f'{safe_text(player1["Team"])}'
        '</td>'

        '<td class="stat-name">'
        'Team'
        '</td>'

        f'<td class="stat-value">'
        f'{safe_text(player2["Team"])}'
        '</td>'

        '</tr>'


        '<tr>'

        f'<td class="stat-value">'
        f'{safe_text(player1["Position"])}'
        '</td>'

        '<td class="stat-name">'
        'Position'
        '</td>'

        f'<td class="stat-value">'
        f'{safe_text(player2["Position"])}'
        '</td>'

        '</tr>'

        +

        comparison_row(
            player1["Price"],
            "Price",
            player2["Price"],
            1
        )

        +

        comparison_row(
            player1[
                "Overall Avg FPT"
            ],
            "Overall Avg FPT",
            player2[
                "Overall Avg FPT"
            ],
            2
        )

        +

        comparison_row(
            player1["Minutes"],
            "Minutes",
            player2["Minutes"],
            1
        )

        +

        comparison_row(
            player1[
                "FPT per Minute"
            ],
            "FPT / Minute",
            player2[
                "FPT per Minute"
            ],
            2
        )

        +

        comparison_row(
            player1[
                "Games Played"
            ],
            "Games",
            player2[
                "Games Played"
            ],
            0
        )

        +

        comparison_row(
            player1[
                "Yaya Rating"
            ],
            "Yaya Rating",
            player2[
                "Yaya Rating"
            ],
            2,
            True
        )

        +

        '</tbody>'

        '</table>'

        '</div>'
    )


    st.markdown(
        table_html,
        unsafe_allow_html=True
    )


    # ==================================================
    # WARNINGS
    # ==================================================

    warning_col1, warning_col2 = (
        st.columns(2)
    )


    with warning_col1:


        if player1[
            "Is New Player"
        ]:

            st.markdown(
                '<div class="yellow-warning">'
                '⚠️ '
                +
                safe_text(
                    player1[
                        "Full Name"
                    ]
                )
                +
                ' is a new player. Historical EuroLeague data is not available yet.'
                '</div>',
                unsafe_allow_html=True
            )


        elif player1[
            "Team Changed"
        ]:

            st.markdown(
                '<div class="yellow-warning">'
                '⚠️ '
                +
                safe_text(
                    player1[
                        "Full Name"
                    ]
                )
                +
                ' changed teams: '
                +
                safe_text(
                    player1[
                        "Old Team"
                    ]
                )
                +
                ' → '
                +
                safe_text(
                    player1[
                        "Team"
                    ]
                )
                +
                '. Historical numbers should be interpreted with extra caution.'
                '</div>',
                unsafe_allow_html=True
            )


    with warning_col2:


        if player2[
            "Is New Player"
        ]:

            st.markdown(
                '<div class="yellow-warning">'
                '⚠️ '
                +
                safe_text(
                    player2[
                        "Full Name"
                    ]
                )
                +
                ' is a new player. Historical EuroLeague data is not available yet.'
                '</div>',
                unsafe_allow_html=True
            )


        elif player2[
            "Team Changed"
        ]:

            st.markdown(
                '<div class="yellow-warning">'
                '⚠️ '
                +
                safe_text(
                    player2[
                        "Full Name"
                    ]
                )
                +
                ' changed teams: '
                +
                safe_text(
                    player2[
                        "Old Team"
                    ]
                )
                +
                ' → '
                +
                safe_text(
                    player2[
                        "Team"
                    ]
                )
                +
                '. Historical numbers should be interpreted with extra caution.'
                '</div>',
                unsafe_allow_html=True
            )


# ==================================================
# FOOTER
# ==================================================

st.markdown(
    '<div class="footer">'
    "Yaya's Rating • EuroLeague Fantasy Analytics"
    '</div>',
    unsafe_allow_html=True
)
