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

# File loading logic
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
        
    # Clean column names
    df.columns = df.columns.str.strip().str.replace('\ufeff', '')
    
    # Normalize Smart Rating to a 9.8 maximum scale
    if "דירוג חכם" in df.columns:
        raw_ratings = df["דירוג חכם"]
        max_raw = raw_ratings.max()
        if max_raw > 0:
            df["Smart Rating (Normalized)"] = (raw_ratings / max_raw) * 9.8
        else:
            df["Smart Rating (Normalized)"] = raw_ratings
    else:
        df["Smart Rating (Normalized)"] = 5.0

except Exception as e:
    st.error(f"⚠️ Error loading data: {e}")
    st.stop()

# Navigation menu
nav_option = st.sidebar.radio("Navigation", ["Head-to-Head Comparison", "Player Database"])

if nav_option == "Head-to-Head Comparison":
    st.markdown("---")
    st.subheader("⚔️ Head-to-Head Player Comparison")
    
    if "שחקן" in df.columns:
        players = sorted(df["שחקן"].dropna().unique().tolist())
        col_select_a, col_select_b = st.columns(2)
        
        with col_select_a:
            player_a_name = st.selectbox("Player A", players, index=0)
        with col_select_b:
            default_b_index = 1 if len(players) > 1 else 0
            player_b_name = st.selectbox("Player B", players, index=default_b_index)
            
        player_a = df[df["שחקן"] == player_a_name].iloc[0]
        player_b = df[df["שחקן"] == player_b_name].iloc[0]
        
        st.markdown("---")
        
        # Metrics Mapping: (UI English Label, CSV Column Name, Lower is Better Flag)
        METRICS = [
            ("Games Played", "משחקים", False),
            ("Overall Avg", "ממוצע_כללי", False),
            ("Home Avg", "ממוצע_בית", False),
            ("Away Avg", "ממוצע_חוץ", False),
            ("Risk (<8)", "אחוז_מתחת_8", True),
            ("Upside (>20)", "אחוז_מעל_20", False),
            ("Consistency Score", "ציון_יציבות", False),
            ("Smart Rating", "Smart Rating (Normalized)", False),
        ]
        
        rating_a = player_a["Smart Rating (Normalized)"]
        rating_b = player_b["Smart Rating (Normalized)"]
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric(f"Smart Rating - {player_a_name}", f"{rating_a:.2f} / 9.8")
        with col_m2:
            st.metric(f"Smart Rating - {player_b_name}", f"{rating_b:.2f} / 9.8")
            
        st.markdown("---")
        
        GREEN = "#1db954"
        NEUTRAL = "#fafafa"
        
        def fmt(val):
            if isinstance(val, (float, int)):
                return f"{val:.2f}"
            return str(val)
            
        rows_html = ""
        for label, col, lower_is_better in METRICS:
            val_a = player_a[col]
            val_b = player_b[col]
            
            if lower_is_better:
                a_better = val_a < val_b
                b_better = val_b < val_a
            else:
                a_better = val_a > val_b
                b_better = val_b > val_b
                
            color_a = GREEN if a_better else NEUTRAL
            color_b = GREEN if b_better else NEUTRAL
            weight_a = "bold" if a_better else "normal"
            weight_b = "bold" if b_better else "normal"
            
            rows_html += f"""
            <tr style="border-bottom: 1px solid #2b3040;">
                <td style="color:{color_a}; font-weight:{weight_a}; text-align:center; padding:12px; font-size:16px;">{fmt(val_a)}</td>
                <td style="text-align:center; padding:12px; color:#a3a8b8; font-size:15px;">{label}</td>
                <td style="color:{color_b}; font-weight:{weight_b}; text-align:center; padding:12px; font-size:16px;">{fmt(val_b)}</td>
            </tr>
            """
            
        table_html = f"""
        <table style="width:100%; border-collapse: collapse; background-color: #1e1e1e; font-family: sans-serif;">
            <thead>
                <tr style="border-bottom: 2px solid #333;">
                    <th style="color: white; text-align: center; padding: 12px; font-size: 16px;">{player_a_name}</th>
                    <th style="color: #a3a8b8; text-align: center; padding: 12px; font-size: 15px;">Metric</th>
                    <th style="color: white; text-align: center; padding: 12px; font-size: 16px;">{player_b_name}</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
        """
        st.markdown(table_html, unsafe_allow_html=True)

else:
    st.subheader("Player Database Overview")
    st.dataframe(df)
