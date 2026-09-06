import pandas as pd
import streamlit as st
import unicodedata
import re


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="EuroLeague Fantasy",
    page_icon="🏀",
    layout="wide"
)


# --------------------------------------------------
# LOAD FILES
# --------------------------------------------------

old_df = pd.read_csv("fantasy_euroleague_stats.csv")
new_df = pd.read_csv("new.csv")


# --------------------------------------------------
# TEAM CODES
# --------------------------------------------------

# This dictionary explains what every team abbreviation
# in new.csv means.

TEAM_NAMES = {
    "OLY": "Olympiacos Piraeus",
    "EFS": "Anadolu Efes Istanbul",
    "CZV": "Crvena Zvezda Meridianbet Belgrade",
    "HTA": "Hapoel IBI Tel Aviv",
    "ZAL": "Zalgiris Kaunas",
    "VBC": "Valencia Basket",
    "MTA": "Maccabi Rapyd Tel Aviv",
    "PBB": "Paris Basketball",
    "PAO": "Panathinaikos AKTOR Athens",
    "RMB": "Real Madrid",
    "DUB": "Dubai Basketball",
    "FBT": "Fenerbahce Beko Istanbul",
    "MIL": "EA7 Emporio Armani Milan",
    "PAR": "Partizan Mozzart Bet Belgrade",
    "BAR": "FC Barcelona",
    "ASV": "LDLC ASVEL Villeurbanne",
    "BJK": "Besiktas",
    "BAY": "FC Bayern Munich",
    "VIR": "Virtus Bologna",
    "KBA": "Baskonia Vitoria-Gasteiz"
}


# Reverse dictionary:
# full old team name -> new abbreviation

OLD_TEAM_TO_CODE = {
    "Baskonia Vitoria-Gasteiz": "KBA",
    "Crvena Zvezda Meridianbet Belgrade": "CZV",
    "FC Barcelona": "BAR",
    "Partizan Mozzart Bet Belgrade": "PAR",
    "Real Madrid": "RMB",
    "Hapoel IBI Tel Aviv": "HTA",
    "Valencia Basket": "VBC",
    "Dubai Basketball": "DUB",
    "FC Bayern Munich": "BAY",
    "Virtus Bologna": "VIR",
    "Olympiacos Piraeus": "OLY",
    "Anadolu Efes Istanbul": "EFS",
    "Panathinaikos AKTOR Athens": "PAO",
    "EA7 Emporio Armani Milan": "MIL",
    "Fenerbahce Beko Istanbul": "FBT",
    "Paris Basketball": "PBB",
    "LDLC ASVEL Villeurbanne": "ASV",
    "Zalgiris Kaunas": "ZAL",
    "AS Monaco": "MON",
    "Maccabi Rapyd Tel Aviv": "MTA"
}


# --------------------------------------------------
# NAME CLEANING
# --------------------------------------------------

def normalize_name(value):

    if pd.isna(value):
        return ""

    text = str(value).lower()

    # Remove accents:
    # example: Corbalán -> corbalan
    text = unicodedata.normalize("NFKD", text)

    text = "".join(
        character
        for character in text
        if not unicodedata.combining(character)
    )

    # Remove punctuation
    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    # Remove extra spaces
    text = " ".join(text.split())

    return text


old_df["Name_Key"] = old_df["Full Name"].apply(normalize_name)
new_df["Name_Key"] = new_df["שם שחקן"].apply(normalize_name)


# --------------------------------------------------
# MANUAL NAME ALIASES
# --------------------------------------------------

# If in the future one player has a slightly different
# name in the two files, we can add him here.
#
# Format:
#
# "name in new.csv": "name in old csv"
#
# Example:
#
# NAME_ALIASES = {
#     "example new name": "example old name"
# }

NAME_ALIASES = {

}


# Normalize aliases
normalized_aliases = {}

for new_name in NAME_ALIASES:

    old_name = NAME_ALIASES[new_name]

    normalized_aliases[
        normalize_name(new_name)
    ] = normalize_name(old_name)


# --------------------------------------------------
# MATCH OLD PLAYER
# --------------------------------------------------

def find_old_player(new_row):

    new_name_key = new_row["Name_Key"]

    # First try exact full-name match
    matches = old_df[
        old_df["Name_Key"] == new_name_key
    ]

    if len(matches) == 1:
        return matches.iloc[0]

    # If an alias exists, try it
    if new_name_key in normalized_aliases:

        old_name_key = normalized_aliases[new_name_key]

        alias_matches = old_df[
            old_df["Name_Key"] == old_name_key
        ]

        if len(alias_matches) == 1:
            return alias_matches.iloc[0]

    # No safe match
    return None


# --------------------------------------------------
# BUILD CURRENT PLAYER DATABASE
# --------------------------------------------------

rows = []

for index in range(len(new_df)):

    new_row = new_df.iloc[index]

    old_player = find_old_player(new_row)

    new_team_code = str(
        new_row["שם קבוצה"]
    )

    new_team_name = TEAM_NAMES.get(
        new_team_code,
        new_team_code
    )

    # ----------------------------------------------
    # EXISTING PLAYER
    # ----------------------------------------------

    if old_player is not None:

        old_team_name = old_player["Team"]

        old_team_code = OLD_TEAM_TO_CODE.get(
            old_team_name,
            old_team_name
        )

        team_changed = (
            old_team_code != new_team_code
        )

        row = {
            "Full Name": new_row["שם שחקן"],
            "Team": new_team_name,
            "Team Code": new_team_code,
            "Position": new_row["עמדה"],
            "Price": pd.to_numeric(
                new_row["מחיר"],
                errors="coerce"
            ),

            "Overall Avg FPT":
                old_player["Overall Avg FPT"],

            "Home Avg FPT":
                old_player["Home Avg FPT"],

            "Away Avg FPT":
                old_player["Away Avg FPT"],

            "FPT Std Dev":
                old_player["FPT Std Dev"],

            "Floor Rate % (FPT<8)":
                old_player["Floor Rate % (FPT<8)"],

            "Ceiling Rate % (FPT>=20)":
                old_player["Ceiling Rate % (FPT>=20)"],

            "Total Minutes":
                old_player["Total Minutes"],

            "FPT per Minute":
                old_player["FPT per Minute"],

            "Games Played":
                old_player["Games Played"],

            "Old Team":
                old_team_name,

            "Team Changed":
                team_changed,

            "Is New Player":
                False
        }

    # ----------------------------------------------
    # COMPLETELY NEW PLAYER
    # ----------------------------------------------

    else:

        row = {
            "Full Name": new_row["שם שחקן"],
            "Team": new_team_name,
            "Team Code": new_team_code,
            "Position": new_row["עמדה"],
            "Price": pd.to_numeric(
                new_row["מחיר"],
                errors="coerce"
            ),

            "Overall Avg FPT": pd.NA,
            "Home Avg FPT": pd.NA,
            "Away Avg FPT": pd.NA,
            "FPT Std Dev": pd.NA,
            "Floor Rate % (FPT<8)": pd.NA,
            "Ceiling Rate % (FPT>=20)": pd.NA,
            "Total Minutes": pd.NA,
            "FPT per Minute": pd.NA,
            "Games Played": pd.NA,

            "Old Team": pd.NA,

            "Team Changed": False,

            "Is New Player": True
        }

    rows.append(row)


df = pd.DataFrame(rows)


# --------------------------------------------------
# CONVERT STAT COLUMNS TO NUMBERS
# --------------------------------------------------

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

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# --------------------------------------------------
# MINUTES PER GAME
# --------------------------------------------------

df["Minutes Per Game"] = (
    df["Total Minutes"]
    /
    df["Games Played"]
)


# --------------------------------------------------
# SCORE CALCULATION
# --------------------------------------------------

def calculate_score(value, points):

    if pd.isna(value):
        return pd.NA

    # Below minimum
    if value <= points[0][0]:
        return points[0][1]

    # Above maximum
    if value >= points[-1][0]:
        return points[-1][1]

    # Linear interpolation
    for i in range(len(points) - 1):

        x1 = points[i][0]
        y1 = points[i][1]

        x2 = points[i + 1][0]
        y2 = points[i + 1][1]

        if x1 <= value <= x2:

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


# --------------------------------------------------
# PRODUCTION SCORE
# --------------------------------------------------

PRODUCTION_POINTS = [
    (0, 0),
    (5, 2.5),
    (8, 4.5),
    (11, 6.5),
    (14, 8),
    (17, 9),
    (20, 10)
]


df["Production Score"] = df[
    "Overall Avg FPT"
].apply(
    lambda x: calculate_score(
        x,
        PRODUCTION_POINTS
    )
)


# --------------------------------------------------
# VALUE FOR PRICE
# --------------------------------------------------

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


df["Value Score"] = df[
    "Value Ratio"
].apply(
    lambda x: calculate_score(
        x,
        VALUE_POINTS
    )
)


# --------------------------------------------------
# STABILITY SCORE
# Lower standard deviation = better
# --------------------------------------------------

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


df["Stability Score"] = df[
    "FPT Std Dev"
].apply(
    lambda x: calculate_score(
        x,
        STABILITY_POINTS
    )
)


# --------------------------------------------------
# FLOOR SCORE
# Lower Floor Rate = better
# --------------------------------------------------

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


df["Floor Score"] = df[
    "Floor Rate % (FPT<8)"
].apply(
    lambda x: calculate_score(
        x,
        FLOOR_POINTS
    )
)


# --------------------------------------------------
# PLAYING TIME SCORE
# --------------------------------------------------

MINUTES_POINTS = [
    (8, 1),
    (12, 3),
    (16, 5),
    (20, 7),
    (24, 9),
    (28, 10)
]


df["Minutes Score"] = df[
    "Minutes Per Game"
].apply(
    lambda x: calculate_score(
        x,
        MINUTES_POINTS
    )
)


# --------------------------------------------------
# EFFICIENCY SCORE
# --------------------------------------------------

EFFICIENCY_POINTS = [
    (0.20, 1),
    (0.30, 3),
    (0.40, 5),
    (0.50, 7),
    (0.65, 9),
    (0.80, 10)
]


df["Efficiency Score"] = df[
    "FPT per Minute"
].apply(
    lambda x: calculate_score(
        x,
        EFFICIENCY_POINTS
    )
)


# --------------------------------------------------
# TEAM ROLE SCORE
# --------------------------------------------------

df["Team Role Score"] = 0.0


for team_code in df["Team Code"].dropna().unique():

    team_players = df[
        df["Team Code"] == team_code
    ]

    for position in team_players["Position"].dropna().unique():

        group = team_players[
            team_players["Position"] == position
        ].copy()

        group = group[
            group["Price"].notna()
        ]

        if len(group) == 0:
            continue

        # Sort highest price first
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

            same_price_players = group[
                group["Price"] == price
            ]

            amount_same_price = len(
                same_price_players
            )

            # Example:
            #
            # 14.0 -> position 1
            # 12.0 -> positions 2 and 3
            #
            # Both 12.0 players receive the score
            # of position 3.

            last_position = (
                position_number
                +
                amount_same_price
                -
                1
            )

            if last_position == 1:
                role_score = 10

            elif last_position == 2:
                role_score = 7

            elif last_position == 3:
                role_score = 4

            else:
                role_score = 0

            # Player must cost at least 8
            # to receive Team Role points.

            if price < 8:
                role_score = 0

            player_indexes = (
                same_price_players.index
            )

            df.loc[
                player_indexes,
                "Team Role Score"
            ] = role_score

            position_number = (
                last_position + 1
            )


# --------------------------------------------------
# CAPTAIN OPTION
# --------------------------------------------------

df["Captain Option"] = (
    (
        df["Floor Rate % (FPT<8)"] <= 10
    )
    &
    (
        df["Ceiling Rate % (FPT>=20)"] > 40
    )
)


# --------------------------------------------------
# FINAL YAYA RATING
# --------------------------------------------------

def calculate_yaya_rating(row):

    needed_values = [
        row["Production Score"],
        row["Value Score"],
        row["Stability Score"],
        row["Floor Score"],
        row["Minutes Score"],
        row["Efficiency Score"]
    ]

    for value in needed_values:

        if pd.isna(value):
            return pd.NA

    rating = (
        row["Production Score"] * 0.30
        +
        row["Value Score"] * 0.25
        +
        row["Stability Score"] * 0.09
        +
        row["Floor Score"] * 0.06
        +
        row["Minutes Score"] * 0.10
        +
        row["Efficiency Score"] * 0.10
        +
        row["Team Role Score"] * 0.10
    )

    return round(rating, 2)


df["Yaya Rating"] = df.apply(
    calculate_yaya_rating,
    axis=1
)


# --------------------------------------------------
# PLAYER DISPLAY NAME
# --------------------------------------------------

def player_display_name(row):

    name = row["Full Name"]

    if row["Captain Option"]:
        name = name + "  C"

    return name


df["Player Display"] = df.apply(
    player_display_name,
    axis=1
)


# --------------------------------------------------
# FORMAT FUNCTION
# --------------------------------------------------

def format_value(value, decimals=2):

    if pd.isna(value):
        return "N/A"

    number = pd.to_numeric(
        value,
        errors="coerce"
    )

    if pd.isna(number):
        return str(value)

    return f"{number:.{decimals}f}"


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🏀 EuroLeague Fantasy Player Analytics")

st.caption(
    "Player comparison, fantasy value and Yaya Rating"
)


# --------------------------------------------------
# TABS
# --------------------------------------------------

tab1, tab2 = st.tabs(
    [
        "⚔️ Head-to-Head",
        "📊 Player Database"
    ]
)


# ==================================================
# HEAD TO HEAD
# ==================================================

with tab1:

    st.header("Player Head-to-Head")

    player_names = sorted(
        df["Full Name"].dropna().unique()
    )

    col1, col2 = st.columns(2)

    with col1:

        player1_name = st.selectbox(
            "Player 1",
            player_names,
            index=0
        )

    with col2:

        default_index = 1

        if len(player_names) < 2:
            default_index = 0

        player2_name = st.selectbox(
            "Player 2",
            player_names,
            index=default_index
        )


    player1 = df[
        df["Full Name"] == player1_name
    ].iloc[0]

    player2 = df[
        df["Full Name"] == player2_name
    ].iloc[0]


    left, right = st.columns(2)


    # ----------------------------------------------
    # PLAYER 1
    # ----------------------------------------------

    with left:

        title1 = player1["Full Name"]

        if player1["Captain Option"]:
            title1 = title1 + "  🅲"

        st.subheader(title1)

        st.write(
            f"**Team:** {player1['Team']}"
        )

        st.write(
            f"**Position:** {player1['Position']}"
        )

        st.write(
            f"**Price:** {format_value(player1['Price'], 1)}"
        )


        if player1["Is New Player"]:

            st.info(
                "New player – no historical EuroLeague data available."
            )


        elif player1["Team Changed"]:

            st.warning(
                "⚠️ Team changed: "
                +
                str(player1["Old Team"])
                +
                " → "
                +
                str(player1["Team"])
            )


        st.metric(
            "Yaya Rating",
            format_value(
                player1["Yaya Rating"],
                2
            )
        )

        st.metric(
            "Overall Avg FPT",
            format_value(
                player1["Overall Avg FPT"],
                2
            )
        )

        st.metric(
            "Games Played",
            format_value(
                player1["Games Played"],
                0
            )
        )

        st.metric(
            "Home Avg FPT",
            format_value(
                player1["Home Avg FPT"],
                2
            )
        )

        st.metric(
            "Away Avg FPT",
            format_value(
                player1["Away Avg FPT"],
                2
            )
        )

        st.metric(
            "FPT per Minute",
            format_value(
                player1["FPT per Minute"],
                2
            )
        )

        st.metric(
            "Minutes per Game",
            format_value(
                player1["Minutes Per Game"],
                1
            )
        )

        st.metric(
            "Floor Rate",
            format_value(
                player1[
                    "Floor Rate % (FPT<8)"
                ],
                1
            )
            + "%"
            if not pd.isna(
                player1[
                    "Floor Rate % (FPT<8)"
                ]
            )
            else "N/A"
        )

        st.metric(
            "Ceiling Rate",
            format_value(
                player1[
                    "Ceiling Rate % (FPT>=20)"
                ],
                1
            )
            + "%"
            if not pd.isna(
                player1[
                    "Ceiling Rate % (FPT>=20)"
                ]
            )
            else "N/A"
        )


    # ----------------------------------------------
    # PLAYER 2
    # ----------------------------------------------

    with right:

        title2 = player2["Full Name"]

        if player2["Captain Option"]:
            title2 = title2 + "  🅲"

        st.subheader(title2)

        st.write(
            f"**Team:** {player2['Team']}"
        )

        st.write(
            f"**Position:** {player2['Position']}"
        )

        st.write(
            f"**Price:** {format_value(player2['Price'], 1)}"
        )


        if player2["Is New Player"]:

            st.info(
                "New player – no historical EuroLeague data available."
            )


        elif player2["Team Changed"]:

            st.warning(
                "⚠️ Team changed: "
                +
                str(player2["Old Team"])
                +
                " → "
                +
                str(player2["Team"])
            )


        st.metric(
            "Yaya Rating",
            format_value(
                player2["Yaya Rating"],
                2
            )
        )

        st.metric(
            "Overall Avg FPT",
            format_value(
                player2["Overall Avg FPT"],
                2
            )
        )

        st.metric(
            "Games Played",
            format_value(
                player2["Games Played"],
                0
            )
        )

        st.metric(
            "Home Avg FPT",
            format_value(
                player2["Home Avg FPT"],
                2
            )
        )

        st.metric(
            "Away Avg FPT",
            format_value(
                player2["Away Avg FPT"],
                2
            )
        )

        st.metric(
            "FPT per Minute",
            format_value(
                player2["FPT per Minute"],
                2
            )
        )

        st.metric(
            "Minutes per Game",
            format_value(
                player2["Minutes Per Game"],
                1
            )
        )

        st.metric(
            "Floor Rate",
            format_value(
                player2[
                    "Floor Rate % (FPT<8)"
                ],
                1
            )
            + "%"
            if not pd.isna(
                player2[
                    "Floor Rate % (FPT<8)"
                ]
            )
            else "N/A"
        )

        st.metric(
            "Ceiling Rate",
            format_value(
                player2[
                    "Ceiling Rate % (FPT>=20)"
                ],
                1
            )
            + "%"
            if not pd.isna(
                player2[
                    "Ceiling Rate % (FPT>=20)"
                ]
            )
            else "N/A"
        )


# ==================================================
# PLAYER DATABASE
# ==================================================

with tab2:

    st.header("Player Database")


    search = st.text_input(
        "Search player"
    )


    filtered_df = df.copy()


    if search != "":

        filtered_df = filtered_df[
            filtered_df["Full Name"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]


    team_options = sorted(
        df["Team"].dropna().unique()
    )


    selected_team = st.selectbox(
        "Team",
        ["All"] + team_options
    )


    if selected_team != "All":

        filtered_df = filtered_df[
            filtered_df["Team"]
            ==
            selected_team
        ]


    position_options = sorted(
        df["Position"].dropna().unique()
    )


    selected_position = st.selectbox(
        "Position",
        ["All"] + position_options
    )


    if selected_position != "All":

        filtered_df = filtered_df[
            filtered_df["Position"]
            ==
            selected_position
        ]


    database_columns = [
        "Player Display",
        "Team",
        "Position",
        "Price",
        "Yaya Rating",
        "Overall Avg FPT",
        "Games Played",
        "Minutes Per Game",
        "FPT per Minute",
        "FPT Std Dev",
        "Floor Rate % (FPT<8)",
        "Ceiling Rate % (FPT>=20)"
    ]


    database = filtered_df[
        database_columns
    ].copy()


    database = database.rename(
        columns={
            "Player Display": "Player",
            "Floor Rate % (FPT<8)": "Floor %",
            "Ceiling Rate % (FPT>=20)": "Ceiling %"
        }
    )


    database = database.sort_values(
        "Yaya Rating",
        ascending=False,
        na_position="last"
    )


    st.dataframe(
        database,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Yaya Rating – EuroLeague Fantasy Analysis"
)
