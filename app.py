import pandas as pd
import streamlit as st
import unicodedata
import re


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

/* --------------------------------------------------
   MAIN PAGE
-------------------------------------------------- */

.stApp {
    background:
        radial-gradient(
            circle at 80% 5%,
            rgba(40, 227, 159, 0.10),
            transparent 28%
        ),
        linear-gradient(
            135deg,
            #070b10 0%,
            #0b1118 55%,
            #07100f 100%
        );

    color: #F5F7FA;
}


.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* --------------------------------------------------
   FONT
-------------------------------------------------- */

html,
body,
[class*="css"] {
    font-family:
        Arial,
        Helvetica,
        sans-serif;
}


/* --------------------------------------------------
   HERO
-------------------------------------------------- */

.hero {

    padding: 38px 42px;

    margin-bottom: 28px;

    background:
        radial-gradient(
            circle at 85% 30%,
            rgba(40, 227, 159, 0.10),
            transparent 30%
        ),
        linear-gradient(
            110deg,
            rgba(15, 23, 32, 0.98),
            rgba(8, 28, 24, 0.94)
        );

    border:
        1px solid #263842;

    border-radius:
        18px;

    box-shadow:
        0 15px 40px
        rgba(0, 0, 0, 0.30);
}


.hero-title {

    font-size: 58px;

    font-weight: 900;

    line-height: 1;

    margin-bottom: 12px;

    letter-spacing: -2px;
}


.hero-yaya {
    color: #FFFFFF;
}


.hero-rating {

    color: #28e39f;

    text-shadow:
        0 0 25px
        rgba(40, 227, 159, 0.20);
}


.hero-subtitle {

    font-size: 22px;

    font-weight: 700;

    color: #dce5eb;

    margin-bottom: 22px;
}


.hero-text {

    color: #aebbc5;

    font-size: 16px;

    line-height: 1.8;

    max-width: 950px;
}


/* --------------------------------------------------
   HEADINGS
-------------------------------------------------- */

h1,
h2,
h3 {

    color: #F5F7FA !important;
}


.section-description {

    color: #9baab5;

    margin-top: -8px;

    margin-bottom: 22px;

    font-size: 15px;
}


/* --------------------------------------------------
   TABS
-------------------------------------------------- */

button[data-baseweb="tab"] {

    background-color:
        #111922;

    border-radius:
        10px;

    padding:
        12px 25px;

    margin-right:
        8px;

    border:
        1px solid #273540;
}


button[data-baseweb="tab"] p {

    font-size:
        16px;

    font-weight:
        700;
}


button[data-baseweb="tab"][aria-selected="true"] {

    background-color:
        #12392f;

    border:
        1px solid #28e39f;
}


/* --------------------------------------------------
   TEXT INPUT
-------------------------------------------------- */

div[data-baseweb="input"] {

    background-color:
        #101821 !important;

    border:
        1px solid #2a3945 !important;

    border-radius:
        10px !important;
}


div[data-baseweb="input"] input {

    color:
        white !important;
}


/* --------------------------------------------------
   SELECT BOX
-------------------------------------------------- */

div[data-baseweb="select"] > div {

    background-color:
        #101821 !important;

    color:
        white !important;

    border:
        1px solid #2a3945 !important;

    border-radius:
        10px !important;
}


div[data-baseweb="select"] span {

    color:
        #F5F7FA !important;
}


/* --------------------------------------------------
   DATABASE
-------------------------------------------------- */

[data-testid="stDataFrame"] {

    border:
        1px solid #263540;

    border-radius:
        14px;

    overflow:
        hidden;

    box-shadow:
        0 10px 25px
        rgba(0, 0, 0, 0.18);
}


/* --------------------------------------------------
   HEAD TO HEAD TABLE
-------------------------------------------------- */

.h2h-wrapper {

    border:
        1px solid #293943;

    border-radius:
        18px;

    overflow:
        hidden;

    margin-top:
        24px;

    background:
        linear-gradient(
            135deg,
            rgba(16, 24, 33, 0.99),
            rgba(9, 20, 25, 0.99)
        );

    box-shadow:
        0 15px 35px
        rgba(0, 0, 0, 0.28);
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

    background:
        linear-gradient(
            180deg,
            #121d26,
            #0e171e
        );

    border-bottom:
        1px solid #2a3943;

    text-align:
        center;
}


.player-name {

    font-size:
        27px;

    font-weight:
        900;

    color:
        white;
}


.vs {

    width:
        18%;

    font-size:
        17px;

    color:
        #28e39f;

    font-weight:
        900;
}


.h2h-table td {

    padding:
        20px 18px;

    border-bottom:
        1px solid #22303a;

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

    color:
        #93a5b1;

    font-size:
        13px !important;

    font-weight:
        800;

    text-transform:
        uppercase;

    letter-spacing:
        0.8px;

    background:
        rgba(255, 255, 255, 0.015);
}


.stat-value {

    color:
        #eef3f6;

    font-weight:
        700;
}


.winner {

    color:
        #28e39f !important;

    font-weight:
        900 !important;

    background-color:
        rgba(40, 227, 159, 0.07);
}


.rating-value {

    font-size:
        27px !important;

    color:
        #28e39f !important;

    font-weight:
        900 !important;
}


/* --------------------------------------------------
   STATUS MESSAGES
-------------------------------------------------- */

div[data-testid="stAlert"] {

    border-radius:
        12px;
}


/* --------------------------------------------------
   FOOTER
-------------------------------------------------- */

.footer {

    text-align:
        center;

    color:
        #697883;

    margin-top:
        40px;

    padding-top:
        22px;

    padding-bottom:
        15px;

    border-top:
        1px solid #1d2931;
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


# ==================================================
# OLD TEAM NAME -> CURRENT TEAM CODE
# ==================================================

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
# NORMALIZE PLAYER NAMES
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
# MANUAL NAME ALIASES
# ==================================================

# If we find a player whose name is written
# differently in the two files, add him here.
#
# Example:
#
# NAME_ALIASES = {
#     "new name": "old name"
# }

NAME_ALIASES = {

}


normalized_aliases = {}


for new_name in NAME_ALIASES:

    old_name = (
        NAME_ALIASES[new_name]
    )

    normalized_aliases[
        normalize_name(new_name)
    ] = normalize_name(
        old_name
    )


# ==================================================
# FIND PLAYER IN OLD DATA
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
# BUILD CURRENT PLAYER DATABASE
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


    # ----------------------------------------------
    # PLAYER EXISTS IN OLD DATABASE
    # ----------------------------------------------

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


    # ----------------------------------------------
    # NEW PLAYER
    # ----------------------------------------------

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
# CONVERT NUMERIC COLUMNS
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
# GENERAL SCORE FUNCTION
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


            return score


    return pd.NA


# ==================================================
# PRODUCTION SCORE
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
# VALUE FOR PRICE
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
# STABILITY SCORE
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
# FLOOR SCORE
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
# PLAYING TIME SCORE
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
# EFFICIENCY SCORE
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
# TEAM ROLE SCORE
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
            group[
                "Price"
            ].unique(),
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


            # Example:
            #
            # Price 15 -> rank 1
            #
            # Price 12 -> ranks 2 and 3
            # Price 12 -> ranks 2 and 3
            #
            # Both players receive
            # the score of rank 3.


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


            # Very cheap players should not
            # receive major Team Role points
            # just because their position group
            # is small.

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
# CAPTAIN OPTION
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


    # ----------------------------------------------
    # YAYA RATING FORMULA
    #
    # Production      25%
    # Value           20%
    # Team Role       25%
    # Stability        6%
    # Floor            4%
    # Playing Time    10%
    # Efficiency      10%
    #
    # TOTAL          100%
    # ----------------------------------------------


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


    # ----------------------------------------------
    # TEAM CHANGE PENALTY
    #
    # Player who moved to a new team
    # loses 6% of his final rating.
    # ----------------------------------------------

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
# PLAYER DISPLAY NAME
# ==================================================

def display_name(row):

    name = str(
        row["Full Name"]
    )


    # C = Captain Option
    #
    # This does NOT count as another
    # displayed statistic.

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
# FORMAT NUMBERS
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


# ==================================================
# HERO
# ==================================================

# IMPORTANT:
# HTML is deliberately kept without indentation
# so Streamlit does not display it as a code block.

hero_html = """
<div class="hero">
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
        'Search and explore EuroLeague players '
        'and their Yaya Rating.'
        '</div>',
        unsafe_allow_html=True
    )


    # ----------------------------------------------
    # SEARCH + FILTERS
    # ----------------------------------------------

    search_col, team_col, position_col = (
        st.columns(
            [
                2.5,
                1,
                1
            ]
        )
    )


    with search_col:

        search = st.text_input(
            "Search",
            placeholder=
                "Search player...",
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


    # ----------------------------------------------
    # FILTER DATABASE
    # ----------------------------------------------

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


    # ----------------------------------------------
    # EXACTLY 8 DISPLAYED FIELDS
    # ----------------------------------------------

    database = filtered_df[
        [

            "Display Name",

            "Team",

            "Position",

            "Overall Avg FPT",

            "Minutes",

            "FPT per Minute",

            "Games Played",

            "Yaya Rating"

        ]
    ].copy()


    database = database.rename(
        columns={

            "Display Name":
                "Player",

            "Position":
                "Pos",

            "Overall Avg FPT":
                "Avg FPT",

            "FPT per Minute":
                "FPT/Min",

            "Games Played":
                "Games"

        }
    )


    database = (
        database.sort_values(
            "Yaya Rating",
            ascending=False,
            na_position="last"
        )
    )


    # ----------------------------------------------
    # DATABASE TABLE
    # ----------------------------------------------

    st.dataframe(

        database,

        use_container_width=True,

        hide_index=True,

        height=650,

        column_config={


            "Player":

                st.column_config.TextColumn(
                    "Player",
                    width="large"
                ),


            "Team":

                st.column_config.TextColumn(
                    "Team",
                    width="medium"
                ),


            "Pos":

                st.column_config.TextColumn(
                    "Pos",
                    width="small"
                ),


            "Avg FPT":

                st.column_config.NumberColumn(
                    "Avg FPT",
                    format="%.2f"
                ),


            "Minutes":

                st.column_config.NumberColumn(
                    "Minutes",
                    format="%.1f"
                ),


            "FPT/Min":

                st.column_config.NumberColumn(
                    "FPT/Min",
                    format="%.2f"
                ),


            "Games":

                st.column_config.NumberColumn(
                    "Games",
                    format="%d"
                ),


            "Yaya Rating":

                st.column_config.NumberColumn(
                    "Yaya Rating",
                    format="%.2f"
                )

        }

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
        'Select two players and compare them side by side.'
        '</div>',
        unsafe_allow_html=True
    )


    # ----------------------------------------------
    # PLAYER LIST
    # ----------------------------------------------

    player_names = sorted(
        df[
            "Full Name"
        ]
        .dropna()
        .unique()
    )


    player1_col, middle_col, player2_col = (
        st.columns(
            [
                1,
                0.12,
                1
            ]
        )
    )


    # ----------------------------------------------
    # PLAYER 1
    # ----------------------------------------------

    with player1_col:

        player1_name = (
            st.selectbox(
                "Player 1",
                player_names,
                key="player1"
            )
        )


    # ----------------------------------------------
    # PLAYER 2
    # ----------------------------------------------

    second_index = 0


    if len(player_names) > 1:

        second_index = 1


    with player2_col:

        player2_name = (
            st.selectbox(
                "Player 2",
                player_names,
                index=second_index,
                key="player2"
            )
        )


    # ----------------------------------------------
    # GET PLAYER DATA
    # ----------------------------------------------

    player1 = df[
        df[
            "Full Name"
        ]
        ==
        player1_name
    ].iloc[0]


    player2 = df[
        df[
            "Full Name"
        ]
        ==
        player2_name
    ].iloc[0]


    # ==================================================
    # COMPARISON FUNCTIONS
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


    # ----------------------------------------------
    # CREATE ONE COMPARISON ROW
    # ----------------------------------------------

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

            left_class = (
                left_class
                +
                " rating-value"
            )


            right_class = (
                right_class
                +
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
            f'<tr>'
            f'<td class="{left_class}">{left_value}</td>'
            f'<td class="stat-name">{label}</td>'
            f'<td class="{right_class}">{right_value}</td>'
            f'</tr>'
        )


    # ----------------------------------------------
    # PLAYER DISPLAY NAMES
    # ----------------------------------------------

    player1_display = (
        display_name(
            player1
        )
    )


    player2_display = (
        display_name(
            player2
        )
    )


    # ==================================================
    # HEAD TO HEAD TABLE
    # ==================================================

    # No indentation is used in the HTML.
    # This prevents Streamlit from showing
    # the HTML as a code block.

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
        f'<td class="stat-value">{player1["Team"]}</td>'
        '<td class="stat-name">Team</td>'
        f'<td class="stat-value">{player2["Team"]}</td>'
        '</tr>'

        '<tr>'
        f'<td class="stat-value">{player1["Position"]}</td>'
        '<td class="stat-name">Position</td>'
        f'<td class="stat-value">{player2["Position"]}</td>'
        '</tr>'

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
            player1[
                "Minutes"
            ],
            "Minutes",
            player2[
                "Minutes"
            ],
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
    # PLAYER STATUS
    # ==================================================

    status1, status2 = (
        st.columns(2)
    )


    # ----------------------------------------------
    # PLAYER 1 STATUS
    # ----------------------------------------------

    with status1:


        if player1[
            "Is New Player"
        ]:

            st.info(

                player1[
                    "Full Name"
                ]

                +

                " is a new player. "
                "Historical data is not available yet."

            )


        elif player1[
            "Team Changed"
        ]:

            st.warning(

                "⚠️ "

                +

                player1[
                    "Full Name"
                ]

                +

                " changed teams: "

                +

                str(
                    player1[
                        "Old Team"
                    ]
                )

                +

                " → "

                +

                str(
                    player1[
                        "Team"
                    ]
                )

            )


    # ----------------------------------------------
    # PLAYER 2 STATUS
    # ----------------------------------------------

    with status2:


        if player2[
            "Is New Player"
        ]:

            st.info(

                player2[
                    "Full Name"
                ]

                +

                " is a new player. "
                "Historical data is not available yet."

            )


        elif player2[
            "Team Changed"
        ]:

            st.warning(

                "⚠️ "

                +

                player2[
                    "Full Name"
                ]

                +

                " changed teams: "

                +

                str(
                    player2[
                        "Old Team"
                    ]
                )

                +

                " → "

                +

                str(
                    player2[
                        "Team"
                    ]
                )

            )


# ==================================================
# FOOTER
# ==================================================

footer_html = (
    '<div class="footer">'
    "Yaya's Rating • EuroLeague Fantasy Analytics"
    '</div>'
)


st.markdown(
    footer_html,
    unsafe_allow_html=True
)
