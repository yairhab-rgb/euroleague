import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="EuroLeague Fantasy Dashboard",
    page_icon="🏀",
    layout="wide"
)

# --- Clean High-Readability Light Theme & Hiding Sidebar ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Clean Light Background */
    .stApp {
        background-color: #f8f9fa;
        color: #212529;
        font-family: 'Inter', sans-serif;
    }
    
    /* Completely Hide Sidebar */
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Main Title Styling */
    .main-title {
        font-weight: 700;
        color: #00b4d8;
        font-size: 2.2rem;
        margin-bottom: 20px;
        letter-spacing: -0.5px;
    }
    
    /* Clean Modern Metric Cards for Light Mode */
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
    
    /* Custom Styling for Tabs */
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
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    if os.path.exists("fantasy_euroleague_stats.csv"):
        return pd.read_csv("fantasy_euroleague_stats.csv")
    elif os.path.exists("euroleague_fantasy.xlsx"):
        return pd.read_excel("euroleague_fantasy.xlsx")
    else:
        return None

st.markdown("<h1 class='main-title'>🏀 EuroLeague Fantasy Analytics</h1>", unsafe_allow_html=True)

# Automatically load local data
df = load_data()

if df is None:
    st.error("⚠️ Default data file ('fantasy_euroleague_stats.csv' or 'euroleague_fantasy.xlsx') not found in directory.")
    st.stop()
    
df.columns = df.columns.str.strip().str.replace('\ufeff', '')

def find_col(keywords):
    for col in df.columns:
        if all(kw.lower() in col.lower() for kw in keywords):
            return col
    return None

def get_num_series(col_name):
    if col_name and col_name in df.columns:
        return pd.to_numeric(df[col_name].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)
    return pd.Series([0.0] * len(df))

player_col = df.columns[0]
col_team = find_col(["team"]) or df.columns[1]
col_pos = find_col(["position", "pos"]) or df.columns[2]
col_overall = find_col(["overall", "avg"]) or df.columns[3]
col_mins = find_col(["min"]) or df.columns[4]
col_per_min = find_col(["per minute"]) or col_overall
col_games = find_col(["games", "played", "gp"]) or df.columns[-1]

val_overall = get_num_series(col_overall)
val_per_min = get_num_series(col_per_min)
val_ceiling = get_num_series(find_col(["ceiling"]) or col_overall)

raw_ratings = (val_overall * 1.5) + (val_per_min * 25) + (val_ceiling * 0.1)
max_raw = raw_ratings.max()
if max_raw > 0 and pd.notna(max_raw):
    df["Yaya Rating"] = (raw_ratings / max_raw) * 9.8
else:
    df["Yaya Rating"] = 5.0

# --- Clean Top-Level Tabs Navigation (Replacing Sidebar) ---
tab_h2h, tab_db = st.tabs(["⚔️ Head-to-Head Comparison", "📋 Player Database"])

with tab_h2h:
    st.subheader("Head-to-Head Player Comparison")
    
    if len(df.columns) > 0:
        players = sorted(df[player_col].dropna().unique().tolist())
        col_select_a, col_select_b = st.columns(2)
        
        with col_select_a:
            player_a_name = st.selectbox("Player A", players, index=0, key="player_a_select")
        with col_select_b:
            default_b_index = 1 if len(players) > 1 else 0
            player_b_name = st.selectbox("Player B", players, index=default_b_index, key="player_b_select")
            
        player_a = df[df[player_col] == player_a_name].iloc[0]
        player_b = df[df[player_col] == player_b_name].iloc[0]
        
        st.markdown("---")
        
        METRICS = [
            ("Team", col_team),
            ("Position", col_pos),
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
        
        def fmt(val):
            try:
                if isinstance(val, (float, int)) or pd.notna(float(str(val).replace(',', '.'))):
                    return f"{float(str(val).replace(',', '.')):.2f}"
            except:
                pass
            return str(val)
            
        comparison_data = []
        for label, col in METRICS:
            if col and (col in df.columns or col == "Yaya Rating"):
                comparison_data.append({
                    player_a_name: fmt(player_a[col]),
                    "Metric": label,
                    player_b_name: fmt(player_b[col])
                })
        
        comp_df = pd.DataFrame(comparison_data)
        st.dataframe(comp_df, use_container_width=True, hide_index=True)

    else:
        st.error("Dataset is empty or invalid.")

with tab_db:
    st.subheader("Player Database Overview")
    
    db_cols_mapping = {
        player_col: "Player",
        col_team: "Team",
        col_pos: "Position",
        col_overall: "Total Avg Points",
        col_mins: "Minutes",
        col_per_min: "Points per Minute",
        col_games: "Total Games",
        "Yaya Rating": "Yaya Rating"
    }
    
    valid_db_cols = {k: v for k, v in db_cols_mapping.items() if k and (k in df.columns or k == "Yaya Rating")}
    display_db = df[list(valid_db_cols.keys())].rename(columns=valid_db_cols)
    
    st.dataframe(display_db, use_container_width=True, hide_index=True)
