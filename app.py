import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="EuroLeague Fantasy Dashboard", page_icon="🏀", layout="wide"
)

# --- Clean High-Readability Light Theme & Hiding Sidebar ---
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
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    current_df = None
    past_df = None

    # זיהוי אוטומטי של הקובץ הראשי בתיקייה
    csv_files = [
        f for f in os.listdir(".") if f.endswith(".csv") and f != "new.csv"
    ]
    main_file = None
    euroleague_candidates = [
        f
        for f in csv_files
        if any(
            kw in f.lower() for kw in ["euroleague", "current", "season", "stats"]
        )
    ]
    if euroleague_candidates:
        main_file = max(euroleague_candidates, key=os.path.getmtime)
    elif csv_files:
        main_file = max(csv_files, key=os.path.getmtime)

    if main_file and os.path.exists(main_file):
        current_df = pd.read_csv(main_file)

    if os.path.exists("new.csv"):
        past_df = pd.read_csv("new.csv")

    return current_df, past_df


st.markdown(
    "<h1 class='main-title'>🏀 EuroLeague Fantasy Analytics</h1>",
    unsafe_allow_html=True,
)

df, past_df = load_data()

if df is None or len(df.columns) == 0:
    st.error("⚠️ לא נמצא קובץ ראשי מתאים בתיקייה.")
    st.stop()

if past_df is None or len(past_df.columns) == 0:
    st.error("⚠️ לא נמצא קובץ new.csv בתיקייה.")
    st.stop()

df.columns = df.columns.str.strip().str.replace("\ufeff", "")
past_df.columns = past_df.columns.str.strip().str.replace("\ufeff", "")


def find_col(dataset, keywords):
    if dataset is None:
        return None
    for col in dataset.columns:
        if all(kw.lower() in col.lower() for kw in keywords):
            return col
    return None


def get_safe_col(dataset, keywords, fallback_idx):
    found = find_col(dataset, keywords)
    if found:
        return found
    if len(dataset.columns) > fallback_idx:
        return dataset.columns[fallback_idx]
    return dataset.columns[0]


def get_num_series(dataset, col_name):
    if dataset is not None and col_name and col_name in dataset.columns:
        return (
            pd.to_numeric(
                dataset[col_name].astype(str).str.replace(",", "."),
                errors="coerce",
            )
            .fillna(0)
        )
    return pd.Series([0.0] * len(df))


player_col = df.columns[0]
col_team = get_safe_col(df, ["team"], 1 if len(df.columns) > 1 else 0)
col_pos = get_safe_col(df, ["position", "pos"], 2 if len(df.columns) > 2 else 0)
col_overall = get_safe_col(
    df, ["overall", "avg", "pts"], 3 if len(df.columns) > 3 else 0
)
col_mins = get_safe_col(df, ["min"], 4 if len(df.columns) > 4 else 0)
col_per_min = find_col(df, ["per minute"]) or col_overall
col_games = (
    find_col(df, ["games", "played", "gp"])
    or df.columns[-1]
    if len(df.columns) > 0
    else player_col
)
col_price = find_col(df, ["price", "cost", "credit"])

# מיפוי שמות משפחה וקבוצות מתוך new.csv
past_player_col = past_df.columns[0]
past_team_col = find_col(past_df, ["team"])

past_last_names = set()
past_team_map = {}

for _, row in past_df.iterrows():
    p_name = str(row[past_player_col]).strip().lower()
    if p_name:
        l_name = p_name.split()[-1]
        past_last_names.add(l_name)
        if past_team_col:
            past_team_map[l_name] = str(row[past_team_col]).strip()

# חילוץ שם משפחה מהקובץ הראשי
df["Last_Name"] = (
    df[player_col]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.split()
    .str[-1]
    .str.lower()
    .fillna("")
)

# שיטת הדרה (Elimination): השארת אך ורק שחקנים ששם המשפחה שלהם קיים בקובץ new.csv
df = df[df["Last_Name"].isin(past_last_names)].copy()

if df.empty:
    st.error(
        "⚠️ לא נמצאו שחקנים חופפים בין הקובץ הראשי לקובץ new.csv לאחר הסינון."
    )
    st.stop()

# בדיקת שינוי מועדון עבור השחקנים שנשארו
team_changed = []
for _, row in df.iterrows():
    l_name = row["Last_Name"]
    if col_team in df.columns and l_name in past_team_map:
        current_team = str(row[col_team]).strip().lower()
        old_team = past_team_map[l_name].lower()
        team_changed.append(current_team != old_team)
    else:
        team_changed.append(False)

df["Team_Changed"] = team_changed

val_overall = get_num_series(df, col_overall)
val_per_min = get_num_series(df, col_per_min)
val_games = get_num_series(df, col_games)
val_mins = get_num_series(df, col_mins)
val_price = (
    get_num_series(df, col_price) if col_price else pd.Series([10.0] * len(df))
)

# חישוב Yaya Rating
safe_price = val_price.replace(0, 1.0)
efficiency = val_overall / safe_price
max_eff = efficiency.max() if efficiency.max() > 0 else 1.0

raw_ratings = (
    (val_overall * 1.2) + (val_per_min * 15) + ((efficiency / max_eff) * 25)
)
max_raw = raw_ratings.max()
if max_raw > 0 and pd.notna(max_raw):
    df["Yaya Rating"] = (raw_ratings / max_raw) * 9.8
else:
    df["Yaya Rating"] = 5.0

# --- ניווט טאבים (שני טאבים בלבד) ---
tab_h2h, tab_db = st.tabs(["⚔️ Head-to-Head Comparison", "📋 Player Database"])

with tab_h2h:
    st.subheader("Head-to-Head Player Comparison")

    if len(df.columns) > 0:
        players = sorted(df[player_col].dropna().unique().tolist())
        col_select_a, col_select_b = st.columns(2)

        with col_select_a:
            player_a_name = st.selectbox(
                "Player A", players, index=0, key="player_a_select"
            )
        with col_select_b:
            default_b_index = 1 if len(players) > 1 else 0
            player_b_name = st.selectbox(
                "Player B", players, index=default_b_index, key="player_b_select"
            )

        player_a = df[df[player_col] == player_a_name].iloc[0]
        player_b = df[df[player_col] == player_b_name].iloc[0]

        st.markdown("---")

        # אזהרת שינוי מועדון בלבד
        if player_a["Team_Changed"]:
            st.markdown(
                f"<div class='warning-badge'>⚠️ Warning: {player_a_name} changed teams compared to last year!</div>",
                unsafe_allow_html=True,
            )

        if player_b["Team_Changed"]:
            st.markdown(
                f"<div class='warning-badge'>⚠️ Warning: {player_b_name} changed teams compared to last year!</div>",
                unsafe_allow_html=True,
            )

        METRICS = [
            ("Team", col_team),
            ("Position", col_pos),
            ("Price", col_price if col_price else None),
            ("Total Avg Points", col_overall),
            ("Minutes", col_mins),
            ("Points per Minute", col_per_min),
            ("Total Games", col_games),
            ("Yaya Rating", "Yaya Rating"),
        ]

        rating_a = player_a["Yaya Rating"]
        rating_b = player_b["Yaya Rating"]

        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric(f"Yaya Rating - {player_a_name}", f"{rating_a:.2f} / 9.8")
        with col_m2:
            st.metric(f"Yaya Rating - {player_b_name}", f"{rating_b:.2f} / 9.8")

        st.markdown("---")


        def fmt(val, is_price=False):
            try:
                numeric_val = float(str(val).replace(",", "."))
                if pd.notna(numeric_val):
                    return (
                        f"{numeric_val:.1f} ₳"
                        if is_price
                        else f"{numeric_val:.2f}"
                    )
            except:
                pass
            return str(val)


        comparison_data = []
        for label, col in METRICS:
            if col and (col in df.columns or col == "Yaya Rating"):
                is_p = label == "Price"
                comparison_data.append(
                    {
                        player_a_name: fmt(player_a[col], is_p),
                        "Metric": label,
                        player_b_name: fmt(player_b[col], is_p),
                    }
                )

        comp_df = pd.DataFrame(comparison_data)
        st.dataframe(comp_df, use_container_width=True, hide_index=True)

    else:
        st.error("Dataset is empty or invalid.")

with tab_db:
    st.subheader("Player Database Overview (Prices & Value)")

    db_cols_mapping = {
        player_col: "Player",
        col_team: "Team",
        col_pos: "Position",
        col_price if col_price else None: "Price",
        col_overall: "Total Avg Points",
        col_mins: "Minutes",
        col_per_min: "Points per Minute",
        col_games: "Total Games",
        "Yaya Rating": "Yaya Rating",
    }

    valid_db_cols = {
        k: v
        for k, v in db_cols_mapping.items()
        if k and (k in df.columns or k == "Yaya Rating")
    }
    display_db = df[list(valid_db_cols.keys())].rename(columns=valid_db_cols)

    st.dataframe(display_db, use_container_width=True, hide_index=True)
