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
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==================================================
# DESIGN
# ==================================================

st.markdown("""
<style>

/* ==================================================
   GENERAL
================================================== */

.stApp {
    background:
        radial-gradient(
            circle at 78% 0%,
            rgba(20, 211, 144, 0.12),
            transparent 27%
        ),
        linear-gradient(
            135deg,
            #05090d 0%,
            #081018 55%,
            #07130f 100%
        );

    color: #f7f9fb;
}


.block-container {
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}


html,
body,
[class*="css"] {
    font-family:
        Inter,
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

    padding:
        48px 50px;

    margin-bottom:
        25px;

    border:
        1px solid #223943;

    border-radius:
        20px;

    background:
        radial-gradient(
            circle at 75% 40%,
            rgba(31, 220, 150, 0.18),
            transparent 24%
        ),
        radial-gradient(
            circle at 95% 0%,
            rgba(255, 255, 255, 0.06),
            transparent 19%
        ),
        linear-gradient(
            115deg,
            rgba(8, 16, 23, 0.99) 0%,
            rgba(9, 29, 27, 0.97) 72%,
            rgba(7, 39, 29, 0.96) 100%
        );

    box-shadow:
        0 18px 50px
        rgba(0, 0, 0, 0.35);
}


.hero:after {

    content: "";

    position: absolute;

    right: -70px;
    bottom: -110px;

    width: 520px;
    height: 280px;

    border:
        2px solid
        rgba(53, 229, 164, 0.12);

    border-radius:
        50%;

    transform:
        rotate(-8deg);
}


.hero-title {

    position: relative;

    z-index: 2;

    font-size:
        66px;

    font-weight:
        900;

    line-height:
        0.95;

    letter-spacing:
        -3px;

    margin-bottom:
        13px;
}


.hero-white {
    color: white;
}


.hero-green {

    color:
        #25e3a0;

    text-shadow:
        0 0 35px
        rgba(37, 227, 160, 0.18);
}


.hero-subtitle {

    position: relative;

    z-index: 2;

    color:
        #f2f6f8;

    font-size:
        22px;

    font-weight:
        800;

    margin-bottom:
        18px;
}


.hero-description {

    position: relative;

    z-index: 2;

    color:
        #b5c3cc;

    font-size:
        15px;

    line-height:
        1.75;

    max-width:
        880px;
}


/* ==================================================
   WARNING
================================================== */

.warning-box {

    position: relative;

    z-index: 2;

    margin-top:
        22px;

    padding:
        13px 16px;

    max-width:
        900px;

    border-radius:
        10px;

    border:
        1px solid
        rgba(255, 204, 70, 0.40);

    background:
        rgba(255, 193, 7, 0.09);

    color:
        #ffd86b;

    font-size:
        13px;

    line-height:
        1.5;
}


.player-warning {

    margin-top:
        16px;

    padding:
        13px 16px;

    border-radius:
        11px;

    border:
        1px solid
        rgba(255, 204, 70, 0.42);

    background:
        rgba(255, 193, 7, 0.10);

    color:
        #ffd86b;

    font-size:
        14px;
}


/* ==================================================
   TABS
================================================== */

div[data-baseweb="tab-list"] {

    gap:
        6px;

    border-bottom:
        1px solid #14222b;
}


button[data-baseweb="tab"] {

    background:
        transparent;

    padding:
        13px 18px;

    border-radius:
        0;

    border:
        none;
}


button[data-baseweb="tab"] p {

    font-size:
        15px;

    font-weight:
        700;
}


button[data-baseweb="tab"][aria-selected="true"] {

    border-bottom:
        2px solid #28e39f;
}


button[data-baseweb="tab"][aria-selected="true"] p {

    color:
        #28e39f !important;
}


/* ==================================================
   TITLES
================================================== */

h1,
h2,
h3 {

    color:
        white !important;
}


.section-title {

    font-size:
        30px;

    color:
        white;

    font-weight:
        900;

    margin-top:
        16px;

    margin-bottom:
        3px;
}


.section-description {

    color:
        #9dafba;

    font-size:
        14px;

    margin-bottom:
        20px;
}


/* ==================================================
   INPUTS
================================================== */

div[data-baseweb="input"] {

    background:
        #0e1821 !important;

    border:
        1px solid #2b3e49 !important;

    border-radius:
        9px !important;
}


div[data-baseweb="input"] input {

    color:
        white !important;
}


div[data-baseweb="select"] > div {

    background:
        #0e1821 !important;

    border:
        1px solid #2b3e49 !important;

    color:
        white !important;

    border-radius:
        9px !important;
}


div[data-baseweb="select"] span {

    color:
        #eef4f7 !important;
}


div[data-baseweb="select"] svg {

    fill:
        #a8b9c4 !important;
}


label {

    color:
        #8fa2ae !important;
}


/* ==================================================
   PANEL
================================================== */

.dashboard-panel {

    margin-top:
        16px;

    padding:
        0;

    background:
        linear-gradient(
            145deg,
            rgba(13, 24, 32, 0.98),
            rgba(9, 20, 27, 0.98)
        );

    border:
        1px solid #273b47;

    border-radius:
        16px;

    overflow:
        hidden;

    box-shadow:
        0 15px 35px
        rgba(0, 0, 0, 0.24);
}


/* ==================================================
   DATABASE TABLE
================================================== */

.player-table {

    width:
        100%;

    border-collapse:
        collapse;

    table-layout:
        auto;
}


.player-table thead {

    background:
        #101c25;
}


.player-table th {

    padding:
        14px 13px;

    text-align:
        left;

    color:
        #9fb0bb;

    font-size:
        12px;

    font-weight:
        800;

    text-transform:
        uppercase;

    letter-spacing:
        0.55px;

    border-bottom:
        1px solid #2a3b46;
}


.player-table td {

    padding:
        13px;

    color:
        #dce5ea;

    font-size:
        14px;

    border-bottom:
        1px solid #182933;
}


.player-table tr:hover td {

    background:
        rgba(40, 227, 159, 0.035);
}


.player-table tr:last-child td {

    border-bottom:
        none;
}


.player-cell {

    font-weight:
        800;

    color:
        white !important;
}


.rating-cell {

    color:
        #28e39f !important;

    font-weight:
        900;

    font-size:
        15px !important;
}


.price-cell {

    color:
        #e4edf2 !important;

    font-weight:
        700;
}


.captain-mark {

    display:
        inline-block;

    margin-left:
        6px;

    padding:
        1px 6px;

    border:
        1px solid
        rgba(255, 213, 79, 0.55);

    border-radius:
        5px;

    color:
        #ffd54f;

    background:
        rgba(255, 213, 79, 0.09);

    font-size:
        10px;

    font-weight:
        900;
}


/* ==================================================
   TABLE INFO
================================================== */

.table-footer {

    display:
        flex;

    justify-content:
        space-between;

    padding:
        14px 16px;

    color:
        #768a96;

    font-size:
        12px;

    background:
        #0b151c;

    border-top:
        1px solid #22343f;
}


/* ==================================================
   HEAD TO HEAD
================================================== */

.h2h-card {

    margin-top:
        22px;

    border:
        1px solid #2a3e49;

    border-radius:
        17px;

    overflow:
        hidden;

    background:
        linear-gradient(
            145deg,
            #0d1922,
            #09141b
        );

    box-shadow:
        0 15px 35px
        rgba(0, 0, 0, 0.30);
}


.h2h-header {

    display:
        grid;

    grid-template-columns:
        1fr 140px 1fr;

    align-items:
        center;

    background:
        linear-gradient(
            180deg,
            #111f29,
            #0d1820
        );

    border-bottom:
        1px solid #293d48;
}


.h2h-player {

    text-align:
        center;

    padding:
        29px 15px;
}


.h2h-player-name {

    color:
        white;

    font-size:
        28px;

    font-weight:
        900;
}


.h2h-player-team {

    color:
        #8fa2ae;

    font-size:
        14px;

    margin-top:
        6px;
}


.h2h-vs {

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    height:
        100%;

    color:
        #28e39f;

    font-size:
        18px;

    font-weight:
        900;

    border-left:
        1px solid #1c2d36;

    border-right:
        1px solid #1c2d36;
}


/* ==================================================
   H2H ROW
================================================== */

.compare-row {

    display:
        grid;

    grid-template-columns:
        1fr 140px 1fr;

    min-height:
        59px;

    border-bottom:
        1px solid #1e3039;
}


.compare-row:last-child {

    border-bottom:
        none;
}


.compare-value {

    display:
        flex;

    justify-content:
        center;

    align-items:
        center;

    color:
        #eaf0f3;

    font-size:
        18px;

    font-weight:
        800;
}


.compare-label {

    display:
        flex;

    justify-content:
        center;

    align-items:
        center;

    color:
        #91a4af;

    background:
        rgba(255, 255, 255, 0.015);

    border-left:
        1px solid #1c2d36;

    border-right:
        1px solid #1c2d36;

    font-size:
        11px;

    font-weight:
        900;

    text-transform:
        uppercase;

    letter-spacing:
        0.7px;
}


.compare-winner {

    color:
        #28e39f;

    background:
        linear-gradient(
            90deg,
            rgba(40, 227, 159, 0.03),
            rgba(40, 227, 159, 0.11)
        );
}


.yaya-big {

    color:
        #28e39f;

    font-size:
        26px;

    font-weight:
        900;
}


/* ==================================================
   H2H BOTTOM CARD
================================================== */

.edge-box {

    margin-top:
        18px;

    padding:
        22px 25px;

    border:
        1px solid
        rgba(40, 227, 159, 0.25);

    border-radius:
        13px;

    background:
        linear-gradient(
            100deg,
            rgba(20, 87, 67, 0.20),
            rgba(10, 30, 29, 0.25)
        );

    color:
        #d9e6e3;

    font-size:
        16px;

    font-style:
        italic;

    text-align:
        center;
}


/* ==================================================
   FOOTER
================================================== */

.site-footer {

    margin-top:
        40px;

    padding-top:
        20px;

    border-top:
        1px solid #17262e;

    color:
        #687b86;

    text-align:
        center;

    font-size:
        12px;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# LOAD FILES
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


OLD_TEAM_TO_CODE = {

    "Olympiacos Piraeus":
        "OLY",

    "Anadolu Efes Istanbul":
        "EFS",

    "Crvena Zvezda Meridianbet Belgrade":
        "CZV",

    "Hapoel IBI Tel Aviv":
        "HTA",

    "Zalgiris Kaunas":
        "ZAL",

    "Valencia Basket":
        "VBC",

    "Maccabi Rapyd Tel Aviv":
        "MTA",

    "Paris Basketball":
        "PBB",

    "Panathinaikos AKTOR Athens":
        "PAO",

    "Real Madrid":
        "RMB",

    "Dubai Basketball":
        "DUB",

    "Fenerbahce Beko Istanbul":
        "FBT",

    "EA7 Emporio Armani Milan":
        "MIL",

    "Partizan Mozzart Bet Belgrade":
        "PAR",

    "FC Barcelona":
        "BAR",

    "LDLC ASVEL Villeurbanne":
        "ASV",

    "FC Bayern Munich":
        "BAY",

    "Virtus Bologna":
        "VIR",

    "Baskonia Vitoria-Gasteiz":
        "KBA",

    "AS Monaco":
        "MON"
}


# ==================================================
# NORMALIZE NAME
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
        if not unicodedata.combining(
            character
        )
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
        normalize_name(
            new_name
        )
    ] = normalize_name(
        NAME_ALIASES[
            new_name
        ]
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

    old_player = (
        find_old_player(
            new_row
        )
    )

    team_code = str(
        new_row["שם קבוצה"]
    )

    team_name = (
        TEAM_NAMES.get(
            team_code,
            team_code
        )
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


    rows.append(
        row
    )


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

            return (

                y1

                +

                (
                    value - x1
                )

                *

                (
                    y2 - y1
                )

                /

                (
                    x2 - x1
                )

            )


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
        team_players["Position"]
        .dropna()
        .unique()
    ):

        group = team_players[
            team_players["Position"]
            ==
            position
        ].copy()


        group = group[
            group["Price"]
            .notna()
        ]


        if len(group) == 0:
            continue


        group = group.sort_values(
            "Price",
            ascending=False
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
                last_position
                +
                1
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

        row["Production Score"]
        * 0.25

        +

        row["Value Score"]
        * 0.20

        +

        row["Team Role Score"]
        * 0.25

        +

        row["Stability Score"]
        * 0.06

        +

        row["Floor Score"]
        * 0.04

        +

        row["Minutes Score"]
        * 0.10

        +

        row["Efficiency Score"]
        * 0.10

    )


    # Player moved to a new team
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


def clean_text(value):

    if pd.isna(value):
        return "N/A"

    return html.escape(
        str(value)
    )


def get_player_name_html(row):

    name = clean_text(
        row["Full Name"]
    )

    if row["Captain Option"]:

        return (
            name
            +
            '<span class="captain-mark">'
            'C'
            '</span>'
        )

    return name


# ==================================================
# HERO
# ==================================================

hero_html = """
<div class="hero">
<div class="hero-title">
<span class="hero-white">Yaya's</span>
<span class="hero-green"> Rating</span>
</div>
<div class="hero-subtitle">
EuroLeague Fantasy Player Analytics
</div>
<div class="hero-description">
Yaya's Rating is a fantasy-focused player rating built to identify the most valuable EuroLeague players.<br>
The score combines production, efficiency, consistency, playing time, price value and the player's role within his team.<br>
Go beyond the basic Fantasy average and find the players who can give you the edge.
</div>
<div class="warning-box">
⚠ Historical performance is an analytical reference only. Past results do not guarantee how a player will perform in the current or future season.
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

database_tab, h2h_tab = st.tabs(
    [
        "📊 Player Database",
        "⚔️ Head-to-Head"
    ]
)


# ==================================================
# PLAYER DATABASE
# ==================================================

with database_tab:

    st.markdown(
        '<div class="section-title">'
        'Player Database'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        "Search and explore all EuroLeague players with their key Fantasy statistics and Yaya's Rating."
        '</div>',
        unsafe_allow_html=True
    )


    # ----------------------------------------------
    # FILTERS
    # ----------------------------------------------

    search_col, team_col, pos_col, show_col = (
        st.columns(
            [
                2.4,
                0.95,
                0.95,
                0.65
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
        df["Team"]
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
        df["Position"]
        .dropna()
        .unique()
    )


    with pos_col:

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


    with show_col:

        show_amount = (
            st.selectbox(
                "Show",
                [
                    25,
                    50,
                    100,
                    "All"
                ],
                index=1
            )
        )


    # ----------------------------------------------
    # FILTER PLAYERS
    # ----------------------------------------------

    filtered_df = (
        df.copy()
    )


    if search != "":

        filtered_df = filtered_df[
            filtered_df[
                "Full Name"
            ]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]


    if (
        selected_team
        !=
        "All Teams"
    ):

        filtered_df = filtered_df[
            filtered_df[
                "Team"
            ]
            ==
            selected_team
        ]


    if (
        selected_position
        !=
        "All Positions"
    ):

        filtered_df = filtered_df[
            filtered_df[
                "Position"
            ]
            ==
            selected_position
        ]


    filtered_df = (
        filtered_df.sort_values(
            "Yaya Rating",
            ascending=False,
            na_position="last"
        )
    )


    total_players = len(
        filtered_df
    )


    if show_amount != "All":

        shown_df = (
            filtered_df.head(
                show_amount
            )
        )

    else:

        shown_df = (
            filtered_df
        )


    # ----------------------------------------------
    # BUILD DARK DATABASE TABLE
    # ----------------------------------------------

    database_html = (
        '<div class="dashboard-panel">'
        '<table class="player-table">'
        '<thead>'
        '<tr>'
        '<th>#</th>'
        '<th>Player</th>'
        '<th>Team</th>'
        '<th>Pos</th>'
        '<th>Price</th>'
        '<th>Avg FPT</th>'
        '<th>Minutes</th>'
        '<th>FPT/Min</th>'
        '<th>Games</th>'
        '<th>Yaya Rating</th>'
        '</tr>'
        '</thead>'
        '<tbody>'
    )


    row_number = 1


    for index, row in (
        shown_df.iterrows()
    ):

        database_html += (

            '<tr>'

            f'<td>{row_number}</td>'

            '<td class="player-cell">'
            f'{get_player_name_html(row)}'
            '</td>'

            '<td>'
            f'{clean_text(row["Team"])}'
            '</td>'

            '<td>'
            f'{clean_text(row["Position"])}'
            '</td>'

            '<td class="price-cell">'
            f'{format_number(row["Price"], 1)}'
            '</td>'

            '<td>'
            f'{format_number(row["Overall Avg FPT"], 2)}'
            '</td>'

            '<td>'
            f'{format_number(row["Minutes"], 1)}'
            '</td>'

            '<td>'
            f'{format_number(row["FPT per Minute"], 2)}'
            '</td>'

            '<td>'
            f'{format_games(row["Games Played"])}'
            '</td>'

            '<td class="rating-cell">'
            f'{format_number(row["Yaya Rating"], 2)}'
            '</td>'

            '</tr>'

        )


        row_number += 1


    database_html += (
        '</tbody>'
        '</table>'
        '<div class="table-footer">'
        f'<span>Showing {len(shown_df)} of {total_players} players</span>'
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

    st.markdown(
        '<div class="section-title">'
        'Head-to-Head Comparison'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Compare two EuroLeague Fantasy players side by side.'
        '</div>',
        unsafe_allow_html=True
    )


    # ----------------------------------------------
    # PLAYER LIST
    # ----------------------------------------------

    player_names = sorted(
        df["Full Name"]
        .dropna()
        .unique()
    )


    def find_player_index(
        wanted_name
    ):

        wanted_key = normalize_name(
            wanted_name
        )

        for i in range(
            len(player_names)
        ):

            if (
                normalize_name(
                    player_names[i]
                )
                ==
                wanted_key
            ):

                return i


        return 0


    # Sasha default
    player1_default = (
        find_player_index(
            "Sasha Vezenkov"
        )
    )


    # Elijah Bryant default
    player2_default = (
        find_player_index(
            "Elijah Bryant"
        )
    )


    player1_col, space_col, player2_col = (
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
                "Select Player 1",
                player_names,
                index=
                    player1_default,
                key=
                    "comparison_player_1"
            )
        )


    with player2_col:

        player2_name = (
            st.selectbox(
                "Select Player 2",
                player_names,
                index=
                    player2_default,
                key=
                    "comparison_player_2"
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
    # WINNER FUNCTION
    # ==================================================

    def get_compare_class(
        value1,
        value2,
        side
    ):

        if (
            pd.isna(value1)
            or
            pd.isna(value2)
        ):

            return "compare-value"


        if value1 == value2:

            return "compare-value"


        if (
            side == 1
            and
            value1 > value2
        ):

            return (
                "compare-value "
                "compare-winner"
            )


        if (
            side == 2
            and
            value2 > value1
        ):

            return (
                "compare-value "
                "compare-winner"
            )


        return "compare-value"


    # ==================================================
    # COMPARISON ROW
    # ==================================================

    def build_compare_row(
        value1,
        label,
        value2,
        decimals=1,
        text_mode=False,
        rating=False
    ):

        if text_mode:

            left_class = (
                "compare-value"
            )

            right_class = (
                "compare-value"
            )

            left_value = (
                clean_text(
                    value1
                )
            )

            right_value = (
                clean_text(
                    value2
                )
            )


        else:

            left_class = (
                get_compare_class(
                    value1,
                    value2,
                    1
                )
            )

            right_class = (
                get_compare_class(
                    value1,
                    value2,
                    2
                )
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


        if rating:

            left_class += (
                " yaya-big"
            )

            right_class += (
                " yaya-big"
            )


        return (

            '<div class="compare-row">'

            f'<div class="{left_class}">'
            f'{left_value}'
            '</div>'

            '<div class="compare-label">'
            f'{label}'
            '</div>'

            f'<div class="{right_class}">'
            f'{right_value}'
            '</div>'

            '</div>'

        )


    # ==================================================
    # H2H CARD
    # ==================================================

    h2h_html = (

        '<div class="h2h-card">'

        '<div class="h2h-header">'

        '<div class="h2h-player">'

        '<div class="h2h-player-name">'
        f'{get_player_name_html(player1)}'
        '</div>'

        '<div class="h2h-player-team">'
        f'{clean_text(player1["Team"])}'
        '</div>'

        '</div>'


        '<div class="h2h-vs">'
        'VS'
        '</div>'


        '<div class="h2h-player">'

        '<div class="h2h-player-name">'
        f'{get_player_name_html(player2)}'
        '</div>'

        '<div class="h2h-player-team">'
        f'{clean_text(player2["Team"])}'
        '</div>'

        '</div>'


        '</div>'


        +

        build_compare_row(
            player1["Team"],
            "Team",
            player2["Team"],
            text_mode=True
        )


        +

        build_compare_row(
            player1["Position"],
            "Position",
            player2["Position"],
            text_mode=True
        )


        +

        build_compare_row(
            player1["Price"],
            "Price",
            player2["Price"],
            1
        )


        +

        build_compare_row(
            player1[
                "Overall Avg FPT"
            ],
            "Avg FPT",
            player2[
                "Overall Avg FPT"
            ],
            2
        )


        +

        build_compare_row(
            player1["Minutes"],
            "Minutes",
            player2["Minutes"],
            1
        )


        +

        build_compare_row(
            player1[
                "FPT per Minute"
            ],
            "FPT / Min",
            player2[
                "FPT per Minute"
            ],
            2
        )


        +

        build_compare_row(
            player1["Games Played"],
            "Games",
            player2["Games Played"],
            0
        )


        +

        build_compare_row(
            player1["Yaya Rating"],
            "Yaya Rating",
            player2["Yaya Rating"],
            2,
            rating=True
        )


        +

        '</div>'

    )


    st.markdown(
        h2h_html,
        unsafe_allow_html=True
    )


    # ==================================================
    # PLAYER WARNINGS
    # ==================================================

    warning_col1, warning_col2 = (
        st.columns(2)
    )


    with warning_col1:

        if player1["Is New Player"]:

            warning_html = (
                '<div class="player-warning">'
                '⚠ '
                f'{clean_text(player1["Full Name"])} '
                'is a new player and does not yet have historical EuroLeague data.'
                '</div>'
            )

            st.markdown(
                warning_html,
                unsafe_allow_html=True
            )


        elif player1["Team Changed"]:

            warning_html = (
                '<div class="player-warning">'
                '⚠ '
                f'{clean_text(player1["Full Name"])} '
                'changed teams. Historical statistics were recorded with '
                f'{clean_text(player1["Old Team"])}.'
                '</div>'
            )

            st.markdown(
                warning_html,
                unsafe_allow_html=True
            )


    with warning_col2:

        if player2["Is New Player"]:

            warning_html = (
                '<div class="player-warning">'
                '⚠ '
                f'{clean_text(player2["Full Name"])} '
                'is a new player and does not yet have historical EuroLeague data.'
                '</div>'
            )

            st.markdown(
                warning_html,
                unsafe_allow_html=True
            )


        elif player2["Team Changed"]:

            warning_html = (
                '<div class="player-warning">'
                '⚠ '
                f'{clean_text(player2["Full Name"])} '
                'changed teams. Historical statistics were recorded with '
                f'{clean_text(player2["Old Team"])}.'
                '</div>'
            )

            st.markdown(
                warning_html,
                unsafe_allow_html=True
            )


    st.markdown(
        '<div class="edge-box">'
        '“Different players. Same goal. Find the edge.”'
        '</div>',
        unsafe_allow_html=True
    )


# ==================================================
# FOOTER
# ==================================================

st.markdown(
    '<div class="site-footer">'
    "Yaya's Rating • EuroLeague Fantasy Player Analytics"
    '</div>',
    unsafe_allow_html=True
)
