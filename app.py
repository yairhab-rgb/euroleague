```python
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="EuroLeague Fantasy Dashboard",
    page_icon="🏀",
    layout="wide"
)


# ---------------------------------------------------------
# עיצוב
# ---------------------------------------------------------

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    .stApp {
        background-color: #f8f9fa;
        color: #212529;
        font-family: 'Inter', sans-serif;
    }

    section[data-testid="stSidebar"] {
        display: none !important;
    }

    .main-title {
        font-weight: 700;
        color: #00b4d8;
        font-size: 2.2rem;
        margin-bottom: 20px;
        letter-spacing: -0.5px;
    }

    div[data-testid="stMetric"] {
        background: #ffffff;
        padding: 16px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }

    div[data-testid="stMetric"] label {
        color: #64748b !important;
        font-weight: 500;
        font-size: 0.9rem;
    }

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #0f172a !important;
        font-weight: 700;
        font-size: 1.7rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #edf2f7;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
        font-weight: 600;
        color: #4a5568;
    }

    .stTabs [aria-selected="true"] {
        background-color: #00b4d8 !important;
        color: white !important;
    }

    .warning-badge {
        background-color: #fff3cd;
        color: #856404;
        padding: 8px 12px;
        border-radius: 6px;
        border: 1px solid #ffeeba;
        font-weight: 600;
        margin-bottom: 15px;
    }

    .new-player-badge {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 8px 12px;
        border-radius: 6px;
        border: 1px solid #bee5eb;
        font-weight: 600;
        margin-bottom: 15px;
    }
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# טעינת הקבצים
# ---------------------------------------------------------

@st.cache_data
def load_data():

    old_df = pd.read_csv("fantasy_euroleague_stats.csv")
    new_df = pd.read_csv("new.csv")

    return old_df, new_df


df_old, df_new = load_data()


# ---------------------------------------------------------
# ניקוי שמות עמודות
# ---------------------------------------------------------

df_old.columns = (
    df_old.columns
    .str.strip()
    .str.replace("\ufeff", "")
)

df_new.columns = (
    df_new.columns
    .str.strip()
    .str.replace("\ufeff", "")
)


# ---------------------------------------------------------
# בדיקת עמודות
# ---------------------------------------------------------

required_old_columns = [
    "Full Name",
    "Team",
    "Position"
]

required_new_columns = [
    "שם שחקן",
    "שם קבוצה",
    "עמדה",
    "מחיר"
]


for column in required_old_columns:

    if column not in df_old.columns:

        st.error(
            "לא נמצאה העמודה "
            + column
            + " בקובץ הישן."
        )

        st.stop()


for column in required_new_columns:

    if column not in df_new.columns:

        st.error(
            "לא נמצאה העמודה "
            + column
            + " בקובץ new.csv."
        )

        st.stop()


# ---------------------------------------------------------
# ניקוי טקסט
# ---------------------------------------------------------

def clean_text(value):

    if pd.isna(value):

        return ""

    value = str(value)

    value = value.strip().lower()

    value = value.replace(".", "")
    value = value.replace(",", "")
    value = value.replace("'", "")
    value = value.replace("-", " ")

    return value


# ---------------------------------------------------------
# יצירת שם מלא נקי
# ---------------------------------------------------------

def clean_full_name(name):

    name = clean_text(name)

    return " ".join(name.split())


# ---------------------------------------------------------
# יצירת Initial + שם משפחה
# ---------------------------------------------------------

def get_name_key(name):

    name = clean_full_name(name)

    if name == "":

        return ""

    parts = name.split()

    initial = parts[0][0]

    last_name = parts[-1]

    return initial + "_" + last_name


# ---------------------------------------------------------
# יצירת המפתחות בקובץ הישן
# ---------------------------------------------------------

df_old["Full_Name_Key"] = (
    df_old["Full Name"]
    .apply(clean_full_name)
)

df_old["Name_Key"] = (
    df_old["Full Name"]
    .apply(get_name_key)
)


# ---------------------------------------------------------
# יצירת המפתחות בקובץ החדש
# ---------------------------------------------------------

df_new["Full_Name_Key"] = (
    df_new["שם שחקן"]
    .apply(clean_full_name)
)

df_new["Name_Key"] = (
    df_new["שם שחקן"]
    .apply(get_name_key)
)


# ---------------------------------------------------------
# הסרת שורות שאינן שחקנים
# ---------------------------------------------------------

df_new = df_new[
    df_new["שם שחקן"].notna()
].copy()

df_new = df_new[
    df_new["שם שחקן"]
    .astype(str)
    .str.lower()
    != "head coach"
].copy()


# ---------------------------------------------------------
# פונקציה למציאת שחקן בקובץ הישן
#
# שלב 1:
# שם מלא
#
# שלב 2:
# Initial + שם משפחה
#
# שלב 3:
# אם יש יותר משחקן אחד:
# משתמשים בקבוצה
#
# אם עדיין אין התאמה:
# לא מנחשים
# ---------------------------------------------------------

def find_old_player(new_row):

    new_full_name = new_row["Full_Name_Key"]
    new_name_key = new_row["Name_Key"]
    new_team = clean_text(
        new_row["שם קבוצה"]
    )


    # -----------------------------------------------------
    # שלב 1 - התאמה לפי שם מלא
    # -----------------------------------------------------

    full_name_candidates = df_old[
        df_old["Full_Name_Key"]
        == new_full_name
    ]


    if len(full_name_candidates) == 1:

        return "MATCH", full_name_candidates.index[0]


    if len(full_name_candidates) > 1:

        team_candidates = full_name_candidates[
            full_name_candidates["Team"]
            .apply(clean_text)
            == new_team
        ]

        if len(team_candidates) == 1:

            return (
                "MATCH",
                team_candidates.index[0]
            )

        return (
            "AMBIGUOUS",
            full_name_candidates.index.tolist()
        )


    # -----------------------------------------------------
    # שלב 2 - Initial + שם משפחה
    # -----------------------------------------------------

    name_candidates = df_old[
        df_old["Name_Key"]
        == new_name_key
    ]


    if len(name_candidates) == 0:

        return "NEW_PLAYER", None


    # יש התאמה אחת בלבד
    if len(name_candidates) == 1:

        return (
            "MATCH",
            name_candidates.index[0]
        )


    # -----------------------------------------------------
    # שלב 3 - יש כמה שחקנים עם אותו Initial
    # ושם משפחה
    # -----------------------------------------------------

    team_candidates = name_candidates[
        name_candidates["Team"]
        .apply(clean_text)
        == new_team
    ]


    if len(team_candidates) == 1:

        return (
            "MATCH",
            team_candidates.index[0]
        )


    # -----------------------------------------------------
    # לא ניתן לזהות בוודאות
    # -----------------------------------------------------

    return (
        "AMBIGUOUS",
        name_candidates.index.tolist()
    )


# ---------------------------------------------------------
# התאמת כל השחקנים
# ---------------------------------------------------------

ambiguous_players = []

matched_indexes = []


for _, new_row in df_new.iterrows():

    result, old_index = find_old_player(
        new_row
    )

    if result == "MATCH":

        matched_indexes.append(old_index)

    elif result == "AMBIGUOUS":

        ambiguous_players.append(
            {
                "name": new_row["שם שחקן"],
                "team": new_row["שם קבוצה"],
                "indexes": old_index
            }
        )


# ---------------------------------------------------------
# טיפול בהתאמות לא חד משמעיות
# ---------------------------------------------------------

if len(ambiguous_players) > 0:

    st.error(
        "⚠️ נמצאו שחקנים שלא ניתן לזהות בוודאות."
    )

    st.write(
        "הקוד לא מנחש במקרים כאלה."
    )

    for item in ambiguous_players:

        st.write(
            "שחקן: "
            + str(item["name"])
            + " | קבוצה: "
            + str(item["team"])
        )

        for index in item["indexes"]:

            st.write(
                "→ "
                + str(df_old.loc[index, "Full Name"])
                + " | "
                + str(df_old.loc[index, "Team"])
            )

    st.stop()


# ---------------------------------------------------------
# בניית בסיס הנתונים החדש
#
# חשוב:
# אנחנו עוברים על new.csv
# ולכן רק שחקנים שקיימים בו ייכנסו לאתר.
# ---------------------------------------------------------

new_data = []


for _, new_row in df_new.iterrows():

    result, old_index = find_old_player(
        new_row
    )


    # -----------------------------------------------------
    # שחקן שקיים גם בקובץ הישן
    # -----------------------------------------------------

    if result == "MATCH":

        old_row = df_old.loc[
            old_index
        ].copy()


        old_team = str(
            old_row["Team"]
        ).strip()


        new_team = str(
            new_row["שם קבוצה"]
        ).strip()


        # האם הקבוצה השתנתה?
        team_changed = (
            clean_text(old_team)
            != clean_text(new_team)
        )


        # -------------------------------------------------
        # new.csv קובע:
        #
        # שם
        # קבוצה
        # עמדה
        # מחיר
        # -------------------------------------------------

        old_row["Full Name"] = (
            new_row["שם שחקן"]
        )

        old_row["Team"] = new_team

        old_row["Position"] = (
            new_row["עמדה"]
        )


        old_row["Price_Clean"] = (
            pd.to_numeric(
                new_row["מחיר"],
                errors="coerce"
            )
        )


        old_row["Team_Changed"] = (
            team_changed
        )


        old_row["Is_New_Player"] = False


        new_data.append(
            old_row
        )


    # -----------------------------------------------------
    # שחקן חדש
    # -----------------------------------------------------

    elif result == "NEW_PLAYER":

        new_player = {}


        # מידע נוכחי
        new_player["Full Name"] = (
            new_row["שם שחקן"]
        )

        new_player["Team"] = (
            new_row["שם קבוצה"]
        )

        new_player["Position"] = (
            new_row["עמדה"]
        )

        new_player["Price_Clean"] = (
            pd.to_numeric(
                new_row["מחיר"],
                errors="coerce"
            )
        )


        # -------------------------------------------------
        # אין עדיין נתוני עבר
        # -------------------------------------------------

        new_player["Overall Avg FPT"] = pd.NA
        new_player["Home Avg FPT"] = pd.NA
        new_player["Away Avg FPT"] = pd.NA
        new_player["FPT Std Dev"] = pd.NA
        new_player["Floor Rate % (FPT<8)"] = pd.NA
        new_player["Ceiling Rate % (FPT>=20)"] = pd.NA
        new_player["Total Minutes"] = pd.NA
        new_player["FPT per Minute"] = pd.NA
        new_player["Games Played"] = pd.NA


        # שחקן חדש
        new_player["Team_Changed"] = False
        new_player["Is_New_Player"] = True


        new_data.append(
            pd.Series(new_player)
        )


# ---------------------------------------------------------
# יצירת DataFrame סופי
# ---------------------------------------------------------

df = pd.DataFrame(
    new_data
)


# ---------------------------------------------------------
# פונקציה לזיהוי עמודה
# ---------------------------------------------------------

def find_col(dataset, keywords):

    for col in dataset.columns:

        match = True

        for keyword in keywords:

            if keyword.lower() not in col.lower():

                match = False

        if match:

            return col

    return None


# ---------------------------------------------------------
# פונקציה לנתונים מספריים
# ---------------------------------------------------------

def get_num_series(dataset, col_name):

    if (
        col_name
        and col_name in dataset.columns
    ):

        return pd.to_numeric(
            dataset[col_name],
            errors="coerce"
        )

    return pd.Series(
        [pd.NA] * len(dataset),
        index=dataset.index
    )


# ---------------------------------------------------------
# עמודות סטטיסטיקה
# ---------------------------------------------------------

player_col = "Full Name"

col_team = "Team"

col_pos = "Position"

col_overall = find_col(
    df,
    ["overall", "avg", "pts"]
)

col_mins = find_col(
    df,
    ["min"]
)

col_per_min = find_col(
    df,
    ["per minute"]
)

col_games = find_col(
    df,
    ["games", "played", "gp"]
)


# ---------------------------------------------------------
# נתונים מספריים
# ---------------------------------------------------------

val_overall = get_num_series(
    df,
    col_overall
)

val_per_min = get_num_series(
    df,
    col_per_min
)

val_games = get_num_series(
    df,
    col_games
)

val_mins = get_num_series(
    df,
    col_mins
)


# ---------------------------------------------------------
# Yaya Rating
#
# כרגע נשארת הנוסחה המקורית.
# שחקנים חדשים מקבלים N/A.
# ---------------------------------------------------------

df["Yaya Rating"] = pd.NA


historical_players = (
    df["Is_New_Player"] == False
)


if historical_players.any():

    historical_overall = (
        val_overall[
            historical_players
        ].fillna(0)
    )

    historical_per_min = (
        val_per_min[
            historical_players
        ].fillna(0)
    )

    historical_price = (
        df.loc[
            historical_players,
            "Price_Clean"
        ]
        .fillna(10)
    )


    safe_price = (
        historical_price
        .replace(0, 1.0)
    )


    efficiency = (
        historical_overall
        / safe_price
    )


    max_eff = efficiency.max()


    if (
        pd.isna(max_eff)
        or max_eff <= 0
    ):

        max_eff = 1.0


    raw_ratings = (
        (historical_overall * 1.2)
        +
        (historical_per_min * 15)
        +
        (
            (efficiency / max_eff)
            * 25
        )
    )


    max_raw = raw_ratings.max()


    if (
        pd.notna(max_raw)
        and max_raw > 0
    ):

        df.loc[
            historical_players,
            "Yaya Rating"
        ] = (
            raw_ratings
            / max_raw
        ) * 9.8


# ---------------------------------------------------------
# מיון לפי שם
# ---------------------------------------------------------

df = df.sort_values(
    "Full Name"
).reset_index(
    drop=True
)


# ---------------------------------------------------------
# כותרת
# ---------------------------------------------------------

st.markdown(
    "<h1 class='main-title'>"
    "🏀 EuroLeague Fantasy Analytics"
    "</h1>",
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# טאבים
# ---------------------------------------------------------

tab_h2h, tab_db = st.tabs(
    [
        "⚔️ Head-to-Head Comparison",
        "📋 Player Database"
    ]
)


# =========================================================
# HEAD TO HEAD
# =========================================================

with tab_h2h:

    st.subheader(
        "Head-to-Head Player Comparison"
    )


    players = sorted(
        df[player_col]
        .dropna()
        .unique()
        .tolist()
    )


    if len(players) == 0:

        st.error(
            "לא נמצאו שחקנים."
        )

    else:

        col_select_a, col_select_b = (
            st.columns(2)
        )


        with col_select_a:

            player_a_name = st.selectbox(
                "Player A",
                players,
                index=0,
                key="player_a_select"
            )


        with col_select_b:

            if len(players) > 1:

                default_b_index = 1

            else:

                default_b_index = 0


            player_b_name = st.selectbox(
                "Player B",
                players,
                index=default_b_index,
                key="player_b_select"
            )


        player_a = df[
            df[player_col]
            == player_a_name
        ].iloc[0]


        player_b = df[
            df[player_col]
            == player_b_name
        ].iloc[0]


        st.markdown("---")


        # -------------------------------------------------
        # אזהרת שינוי קבוצה
        # -------------------------------------------------

        if player_a["Team_Changed"]:

            st.markdown(
                f"""
                <div class='warning-badge'>
                ⚠️ Warning: {player_a_name} changed
                teams compared to last year!
                </div>
                """,
                unsafe_allow_html=True
            )


        if player_b["Team_Changed"]:

            st.markdown(
                f"""
                <div class='warning-badge'>
                ⚠️ Warning: {player_b_name} changed
                teams compared to last year!
                </div>
                """,
                unsafe_allow_html=True
            )


        # -------------------------------------------------
        # סימון שחקן חדש
        # -------------------------------------------------

        if player_a["Is_New_Player"]:

            st.markdown(
                f"""
                <div class='new-player-badge'>
                ℹ️ {player_a_name} is a new player
                with no historical data yet.
                </div>
                """,
                unsafe_allow_html=True
            )


        if player_b["Is_New_Player"]:

            st.markdown(
                f"""
                <div class='new-player-badge'>
                ℹ️ {player_b_name} is a new player
                with no historical data yet.
                </div>
                """,
                unsafe_allow_html=True
            )


        # -------------------------------------------------
        # מדדים
        # -------------------------------------------------

        METRICS = [

            ("Team", col_team),

            ("Position", col_pos),

            ("Price", "Price_Clean"),

            ("Total Avg Points", col_overall),

            ("Minutes", col_mins),

            ("Points per Minute", col_per_min),

            ("Total Games", col_games),

            ("Yaya Rating", "Yaya Rating")

        ]


        rating_a = player_a[
            "Yaya Rating"
        ]

        rating_b = player_b[
            "Yaya Rating"
        ]


        # -------------------------------------------------
        # Rating cards
        # -------------------------------------------------

        col_m1, col_m2 = (
            st.columns(2)
        )


        with col_m1:

            if pd.isna(rating_a):

                st.metric(
                    f"Yaya Rating - {player_a_name}",
                    "N/A"
                )

            else:

                st.metric(
                    f"Yaya Rating - {player_a_name}",
                    f"{float(rating_a):.2f} / 9.8"
                )


        with col_m2:

            if pd.isna(rating_b):

                st.metric(
                    f"Yaya Rating - {player_b_name}",
                    "N/A"
                )

            else:

                st.metric(
                    f"Yaya Rating - {player_b_name}",
                    f"{float(rating_b):.2f} / 9.8"
                )


        st.markdown("---")


        # -------------------------------------------------
        # פורמט ערכים
        # -------------------------------------------------

        def fmt(value, is_price=False):

            if pd.isna(value):

                return "N/A"


            numeric_value = pd.to_numeric(
                value,
                errors="coerce"
            )


            if pd.notna(numeric_value):

                if is_price:

                    return (
                        f"{numeric_value:.1f} ₳"
                    )

                return (
                    f"{numeric_value:.2f}"
                )


            return str(value)


        comparison_data = []


        for label, col in METRICS:

            if (
                col
                and col in df.columns
            ):

                is_price = (
                    label == "Price"
                )


                comparison_data.append(
                    {
                        player_a_name:
                            fmt(
                                player_a[col],
                                is_price
                            ),

                        "Metric":
                            label,

                        player_b_name:
                            fmt(
                                player_b[col],
                                is_price
                            )
                    }
                )


        comp_df = pd.DataFrame(
            comparison_data
        )


        st.dataframe(
            comp_df,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# PLAYER DATABASE
# =========================================================

with tab_db:

    st.subheader(
        "Player Database Overview (Prices & Value)"
    )


    db_cols_mapping = {

        player_col:
            "Player",

        col_team:
            "Team",

        col_pos:
            "Position",

        "Price_Clean":
            "Price",

        col_overall:
            "Total Avg Points",

        col_mins:
            "Minutes",

        col_per_min:
            "Points per Minute",

        col_games:
            "Total Games",

        "Yaya Rating":
            "Yaya Rating"

    }


    valid_db_cols = {}


    for original_col, display_name in (
        db_cols_mapping.items()
    ):

        if (
            original_col
            and original_col in df.columns
        ):

            valid_db_cols[
                original_col
            ] = display_name


    display_db = df[
        list(
            valid_db_cols.keys()
        )
    ].rename(
        columns=valid_db_cols
    )


    st.dataframe(
        display_db,
        use_container_width=True,
        hide_index=True
    )
```
