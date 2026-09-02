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

current_df, past_df = load_data()

if past_df is None or len(past_df.columns) == 0:
  st.error("⚠️ לא נמצא קובץ new.csv בתיקייה (הקובץ הקטן חובה).")
  st.stop()

if current_df is not None:
  current_df.columns = current_df.columns.str.strip().str.replace("\ufeff", "")
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


# מיפוי עמודות מהקובץ הראשי (אם קיים)
if current_df is not None and len(current_df.columns) > 0:
  curr_player_col = current_df.columns[0]
  col_team = get_safe_col(current_df, ["team"], 1)
  col_pos = get_safe_col(current_df, ["position", "pos"], 2)
  col_overall = get_safe_col(current_df, ["overall", "avg", "pts"], 3)
  col_mins = get_safe_col(current_df, ["min"], 4)
  col_per_min = find_col(current_df, ["per minute"]) or col_overall
  col_games = (
      find_col(current_df, ["games", "played", "gp"])
      or current_df.columns[-1]
  )
  col_price = find_col(current_df, ["price", "cost", "credit"])

  current_df["Last_Name"] = (
      current_df[curr_player_col]
      .fillna("")
      .astype(str)
      .str.strip()
      .str.split()
      .str[-1]
      .str.lower()
  )
  stats_dict = {}
  for _, row in current_df.iterrows():
    l_name = row["Last_Name"]
    if l_name:
      stats_dict[l_name] = row
else:
  stats_dict = {}

# בניית רשימת השחקנים הסופית מתוך הקובץ הקטן (new.csv) שהוא המאסטר המחייב
past_player_col = past_df.columns[0]
past_team_col = find_col(past_df, ["team"])
past_price_col = find_col(past_df, ["price", "cost", "credit"])
past_pos_col = find_col(past_df, ["position", "pos"])

rows = []
for _, p_row in past_df.iterrows():
  p_name = str(p_row[past_player_col]).strip()
  if not p_name or pd.isna(p_name):
    continue
  l_name = p_name.split()[-1].lower()

  # קבוצה מהקובץ הקטן קובעת בלעדית
  team = (
      str(p_row[past_team_col]).strip()
      if past_team_col and pd.notna(p_row[past_team_col])
      else "Unknown"
  )

  stat_row = stats_dict.get(l_name, None)

  if stat_row is not None:
    orig_team = (
        str(stat_row[col_team]).strip()
        if current_df is not None
        and col_team in current_df.columns
        and pd.notna(stat_row[col_team])
        else ""
    )
    team_changed = orig_team.lower() != team.lower() if orig_team else False

    pos = (
        stat_row[col_pos]
        if current_df is not None
        and col_pos in current_df.columns
        and pd.notna(stat_row[col_pos])
        else "Unknown"
    )
    price = (
        pd.to_numeric(str(stat_row[col_price]).replace(",", "."), errors="coerce")
        if current_df is not None
        and col_price
        and col_price in current_df.columns
        and pd.notna(stat_row[col_price])
        else 10.0
    )
    overall = (
        pd.to_numeric(
            str(stat_row[col_overall]).replace(",", "."), errors="coerce"
        )
        if current_df is not None
        and col_overall in current_df.columns
        and pd.notna(stat_row[col_overall])
        else 0.0
    )
    mins = (
        pd.to_numeric(str(stat_row[col_mins]).replace(",", "."), errors="coerce")
        if current_df is not None
        and col_mins in current_df.columns
        and pd.notna(stat_row[col_mins])
        else 0.0
    )
    per_min = (
        pd.to_numeric(
            str(stat_row[col_per_min]).replace(",", "."), errors="coerce"
        )
        if current_df is not None
        and col_per_min in current_df.columns
        and pd.notna(stat_row[col_per_min])
        else overall
    )
    games = (
        pd.to_numeric(
            str(stat_row[col_games]).replace(",", "."), errors="coerce"
        )
        if current_df is not None
        and col_games in current_df.columns
        and pd.notna(stat_row[col_games])
        else 0.0
    )
  else:
    # שחקן חדש לגמרי שמופיע רק בקובץ הקטן
    team_changed = False
    pos = (
        p_row[past_pos_col]
        if past_pos_col
        and past_pos_col in past_df.columns
        and pd.notna(p_row[past_pos_col])
        else "Unknown"
    )
    price = (
        pd.to_numeric(str(p_row[past_price_col]).replace(",", "."), errors="coerce")
        if past_price_col
        and past_price_col in past_df.columns
        and pd.notna(p_row[past_price_col])
        else 10.0
    )
    overall = 0.0
    mins = 0.0
    per_min = 0.0
    games = 0.0

  rows.append({
      "Player": p_name,
      "Team": team,
      "Position": pos,
      "Price": price if pd.notna(price) else 10.0,
      "Total Avg Points": overall if pd.notna(overall) else 0.0,
      "Minutes": mins if pd.notna(mins) else 0.0,
      "Points per Minute": per_min if pd.notna(per_min) else 0.0,
      "Total Games": games if pd.notna(games) else 0.0,
      "Team_Changed": team_changed,
  })

df = pd.DataFrame(rows)

if df.empty:
  st.error("⚠️ לא נמצאו שחקנים תקינים בקובץ new.csv.")
  st.stop()

# חישוב Yaya Rating מובטח לכל השחקנים ללא יוצא מן הכלל
val_overall = df["Total Avg Points"].fillna(0)
val_per_min = df["Points per Minute"].fillna(0)
val_price = df["Price"].fillna(10.0).replace(0, 1.0)

efficiency = val_overall / val_price
max_eff = efficiency.max() if efficiency.max() > 0 else 1.0

raw_ratings = (
    (val_overall * 1.2) + (val_per_min * 15) + ((efficiency / max_eff) * 25)
)
max_raw = raw_ratings.max()
if max_raw > 0 and pd.notna(max_raw):
  df["Yaya Rating"] = (raw_ratings / max_raw) * 9.8
else:
  df["Yaya Rating"] = 5.0
df["Yaya Rating"] = df["Yaya Rating"].fillna(5.0)

# --- ניווט טאבים (שני טאבים בלבד) ---
tab_h2h, tab_db = st.tabs(["⚔️ Head-to-Head Comparison", "📋 Player Database"])

with tab_h2h:
  st.subheader("Head-to-Head Player Comparison")

  players = sorted(df["Player"].dropna().unique().tolist())
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

  player_a = df[df["Player"] == player_a_name].iloc[0]
  player_b = df[df["Player"] == player_b_name].iloc[0]

  st.markdown("---")

  if player_a["Team_Changed"]:
    st.markdown(
        f"<div class='warning-badge'>⚠️ Warning: {player_a_name} changed teams"
        " compared to last year!</div>",
        unsafe_allow_html=True,
    )

  if player_b["Team_Changed"]:
    st.markdown(
        f"<div class='warning-badge'>⚠️ Warning: {player_b_name} changed teams"
        " compared to last year!</div>",
        unsafe_allow_html=True,
    )

  METRICS = [
      ("Team", "Team"),
      ("Position", "Position"),
      ("Price", "Price"),
      ("Total Avg Points", "Total Avg Points"),
      ("Minutes", "Minutes"),
      ("Points per Minute", "Points per Minute"),
      ("Total Games", "Total Games"),
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
        return f"{numeric_val:.1f} ₳" if is_price else f"{numeric_val:.2f}"
    except:
      pass
    return str(val)


  comparison_data = []
  for label, col in METRICS:
    is_p = label == "Price"
    comparison_data.append({
        player_a_name: fmt(player_a[col], is_p),
        "Metric": label,
        player_b_name: fmt(player_b[col], is_p),
    })

  comp_df = pd.DataFrame(comparison_data)
  st.dataframe(comp_df, use_container_width=True, hide_index=True)

with tab_db:
  st.subheader("Player Database Overview (Prices & Value)")

  display_db = df[[
      "Player",
      "Team",
      "Position",
      "Price",
      "Total Avg Points",
      "Minutes",
      "Points per Minute",
      "Total Games",
      "Yaya Rating",
  ]].rename(columns={
      "Player": "Player",
      "Team": "Team",
      "Position": "Position",
      "Price": "Price",
      "Total Avg Points": "Total Avg Points",
      "Minutes": "Minutes",
      "Points per Minute": "Points per Minute",
      "Total Games": "Total Games",
      "Yaya Rating": "Yaya Rating",
  })

  st.dataframe(display_db, use_container_width=True, hide_index=True)
