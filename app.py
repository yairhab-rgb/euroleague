import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="EuroLeague Fantasy Dashboard",
    page_icon="🏀",
    layout="wide"
)

@st.cache_data
def load_data(file_path_or_buffer, is_csv=True):
    if is_csv:
        return pd.read_csv(file_path_or_buffer)
    else:
        return pd.read_excel(file_path_or_buffer)

st.title("🏀 EuroLeague Fantasy Analytics Dashboard")

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
    
    # Helper function to find a column dynamically by keywords
    def find_col(keywords):
        for col in df.columns:
            if all(kw.lower() in col.lower() for kw in keywords):
                return col
        return None

    def get_num_series(col_name):
        if col_name and col_name in df.columns:
            return pd.to_numeric(df[col_name].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)
        return pd.Series([0.0] * len(df))

    # Identify core columns for Yaya Rating calculation
    col_overall = find_col(["overall", "avg"]) or (df.columns[2] if len(df.columns) > 2 else df.columns[1])
    col_per_min = find_col(["per minute"]) or col_overall
    col_ceiling = find_col(["ceiling"]) or col_overall
    
    val_overall = get_num_series(col_overall)
    val_per_min = get_num_series(col_per_min)
    val_ceiling = get_num_series(col_ceiling)
    
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

nav_option = st.sidebar.radio("Navigation", ["Head-to-Head Comparison", "Player Database"])

if nav_option == "Head-to-Head Comparison":
    st.markdown("---")
    st.subheader("⚔️ Head-to-Head Player Comparison")
    
    if len(df.columns) > 0:
        player_col = df.columns[0]
        players = sorted(df[player_col].dropna().unique().tolist())
        col_select_a, col_select_b = st.columns(2)
        
        with col_select_a:
            player_a_name = st.selectbox("Player A", players, index=0)
        with col_select_b:
            default_b_index = 1 if len(players) > 1 else 0
            player_b_name = st.selectbox("Player B", players, index=default_b_index)
            
        player_a = df[df[player_col] == player_a_name].iloc[0]
        player_b = df[df[player_col] == player_b_name].iloc[0]
        
        st.markdown("---")
        
        # Curated list of metrics requested by Yaya
        col_team = find_col(["team"]) or df.columns[1]
        col_pos = find_col(["position", "pos"]) or df.columns[2]
        col_games = find_col(["games", "played"]) or df.columns[-1]
        
        METRICS = [
            ("Team", col_team),
            ("Position", col_pos),
            ("Overall Avg FPT", col_overall),
            ("FPT per Minute", col_per_min),
            ("Games Played", col_games),
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
            if col and col in df.columns:
                comparison_data.append({
                    player_a_name: fmt(player_a[col]),
                    "Metric": label,
                    player_b_name: fmt(player_b[col])
                })
        
        comp_df = pd.DataFrame(comparison_data)
        st.dataframe(comp_df, use_container_width=True, hide_index=True)
        
        # --- Visualization Section ---
        st.markdown("### 📊 Visual Comparison")
        chart_data = pd.DataFrame({
            'Metric': ['Overall Avg', 'FPT x10 (Min Scale)', 'Yaya Rating'],
            player_a_name: [
                float(str(player_a[col_overall]).replace(',', '.')) if col_overall in player_a else 0,
                float(str(player_a[col_per_min]).replace(',', '.')) * 10 if col_per_min in player_a else 0,
                float(player_a["Yaya Rating"])
            ],
            player_b_name: [
                float(str(player_b[col_overall]).replace(',', '.')) if col_overall in player_b else 0,
                float(str(player_b[col_per_min]).replace(',', '.')) * 10 if col_per_min in player_b else 0,
                float(player_b["Yaya Rating"])
            ]
        }).set_index('Metric')
        
        st.bar_chart(chart_data)

    else:
        st.error("Dataset is empty or invalid.")
else:
    st.subheader("Player Database Overview")
    st.dataframe(df)
