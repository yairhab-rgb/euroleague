import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="EuroLeague Fantasy Dashboard",
    page_icon="🏀",
    layout="wide"
)

# --- Custom UI / UX Styling (Fonts, Colors, Clean Cards) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Heebo', sans-serif;
    }
    
    .main-title {
        font-weight: 700;
        color: #FF4B4B;
        margin-bottom: 20px;
    }
    
    .stMetric {
        background-color: #1E1E2F;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border: 1px solid #2d2d44;
    }
    
    .stMetric label {
        color: #A0A0AB !important;
        font-weight: 500;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(file_path_or_buffer, is_csv=True):
    if is_csv:
        return pd.read_csv(file_path_or_buffer)
    else:
        return pd.read_excel(file_path_or_buffer)

st.markdown("<h1 class='main-title'>🏀 EuroLeague Fantasy Dashboard</h1>", unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader("Upload Fantasy CSV/Excel file", type=["csv", "xlsx"])
df = None

try:
    if uploaded_file is not None:
        is_csv = uploaded_file.name.lower().endswith(".csv")
        df = load_data(uploaded_file, is_csv)
    elif os.path.exists("fantasy_euroleague_stats.csv"):
        df = load_data("fantasy_euroleague_stats.csv", is_csv=True)
    elif os.path.exists("euroleague_fantasy.xlsx"):
        df = load_data("euroleague_fantasy.xlsx", is_csv=False)
    else:
        st.error("⚠️ No data file found. Please upload a CSV file.")
        st.stop()
        
    df.columns = df.columns.str.strip().str.replace('\ufeff', '')
    
    # Helper function to find columns dynamically
    def find_col(keywords):
        for col in df.columns:
            if all(kw.lower() in col.lower() for kw in keywords):
                return col
        return None

    def get_num_series(col_name):
        if col_name and col_name in df.columns:
            return pd.to_numeric(df[col_name].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)
        return pd.Series([0.0] * len(df))

    # Column mappings
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
    
    # Calculating Yaya Rating dynamically
    raw_ratings = (val_overall * 1.5) + (val_per_min * 25) + (val_ceiling * 0.1)
    max_raw = raw_ratings.max()
    if max_raw > 0 and pd.notna(max_raw):
        df["Yaya Rating"] = (raw_ratings / max_raw) * 9.8
    else:
        df["Yaya Rating"] = 5.0

except Exception as e:
    st.error(f"⚠️ Error loading data: {e}")
    st.stop()

nav_option = st.sidebar.radio("ניווט במערכת", ["השוואת ראש בראש (Head-to-Head)", "מסד נתונים שחקנים (Database)"])

if nav_option == "השוואת ראש בראש (Head-to-Head)":
    st.markdown("---")
    st.subheader("⚔️ השוואת שחקנים")
    
    if len(df.columns) > 0:
        players = sorted(df[player_col].dropna().unique().tolist())
        col_select_a, col_select_b = st.columns(2)
        
        with col_select_a:
            player_a_name = st.selectbox("שחקן א'", players, index=0)
        with col_select_b:
            default_b_index = 1 if len(players) > 1 else 0
            player_b_name = st.selectbox("שחקן ב'", players, index=default_b_index)
            
        player_a = df[df[player_col] == player_a_name].iloc[0]
        player_b = df[df[player_col] == player_b_name].iloc[0]
        
        st.markdown("---")
        
        # Curated exact metrics requested by Yaya
        METRICS = [
            ("קבוצה", col_team),
            ("עמדה", col_pos),
            ("סה\"כ ממוצע נקודות", col_overall),
            ("דקות", col_mins),
            ("נקודות לדקה", col_per_min),
            ("סה\"כ משחקים", col_games),
            ("דירוג יאיא", "Yaya Rating"),
        ]
        
        rating_a = player_a["Yaya Rating"]
        rating_b = player_b["Yaya Rating"]
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric(f"דירוג יאיא - {player_a_name}", f"{rating_a:.2f} / 9.8")
        with col_m2:
            st.metric(f"דירוג יאיא - {player_b_name}", f"{rating_b:.2f} / 9.8")
            
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
                    "מדד": label,
                    player_b_name: fmt(player_b[col])
                })
        
        comp_df = pd.DataFrame(comparison_data)
        st.dataframe(comp_df, use_container_width=True, hide_index=True)

    else:
        st.error("הנתונים ריקים או שגויים.")
else:
    st.subheader("📋 מסד נתונים שחקנים (סינון מדדים)")
    
    # Selecting only the requested columns for the database view
    db_cols_mapping = {
        player_col: "שחקן",
        col_team: "קבוצה",
        col_pos: "עמדה",
        col_overall: "סה\"כ ממוצע נקודות",
        col_mins: "דקות",
        col_per_min: "נקודות לדקה",
        col_games: "סה\"כ משחקים",
        "Yaya Rating": "דירוג יאיא"
    }
    
    valid_db_cols = {k: v for k, v in db_cols_mapping.items() if k and (k in df.columns or k == "Yaya Rating")}
    display_db = df[list(valid_db_cols.keys())].rename(columns=valid_db_cols)
    
    st.dataframe(display_db, use_container_width=True, hide_index=True)
