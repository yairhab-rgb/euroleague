import pandas as pd
import streamlit as st

# הגדרת עמוד Streamlit
st.set_page_config(
    page_title="Fanzonebasket - EuroLeague Fantasy Dashboard",
    page_icon="🏀",
    layout="wide",
)

# עיצוב וכותרת ראשית
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        color: #ff4b4b;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #888;
        margin-bottom: 2rem;
    }
    </style>
    <div class="main-header">Fanzonebasket EuroLeague Fantasy Hub</div>
    <div class="sub-header">Advanced Player Analysis, Current Season Rosters & Yaya Rating System</div>
""",
    unsafe_allow_html=True,
)


# אתחול נתוני בסיס הכוללים את השחקנים העכשוויים והמחירים
@st.cache_data
def load_data():
  data = {
      "Player": [
          "TJ Leaf",
          "Wade Baldwin",
          "Kendrick Nunn",
          "Mathias Lessort",
          "Tornike Shengelia",
          "Mario Hezonja",
          "Nigel Hayes-Davis",
      ],
      "Team": [
          "Dubai / Real",
          "Fenerbahce",
          "Panathinaikos",
          "Panathinaikos",
          "Virtus Bologna",
          "Real Madrid",
          "Fenerbahce",
      ],
      "Position": [
          "Forward",
          "Guard",
          "Guard",
          "Center",
          "Forward",
          "Forward",
          "Forward",
      ],
      "Price": [10.5, 14.2, 15.0, 14.8, 13.5, 13.0, 14.5],
      "PIR": [16.5, 18.0, 19.5, 18.8, 17.2, 16.8, 18.2],
      "Yaya_Rating": [9.4, 9.6, 9.8, 9.7, 9.2, 9.1, 9.5],
      "Status": [
          "Active",
          "Active",
          "Active",
          "Active",
          "Active",
          "Active",
          "Active",
      ],
  }
  return pd.DataFrame(data)


df = load_data()

# ניווט צדדי (Sidebar)
st.sidebar.title("Navigation")
menu = st.sidebar.selectbox(
    "Choose View",
    [
        "Player Database & Current Additions",
        "Head-to-Head Comparison",
        "Yaya Rating Rankings",
    ],
)

if menu == "Player Database & Current Additions":
  st.subheader("📋 Current Season Roster & Player Database")

  # טופס להוספת/עדכון שחקנים עכשוויים
  with st.expander("➕ Add / Update Current Player"):
    with st.form("add_player_form"):
      col1, col2, col3 = st.columns(3)
      with col1:
        new_player = st.text_input("Player Name")
        new_team = st.text_input("Team")
      with col2:
        new_pos = st.selectbox("Position", ["Guard", "Forward", "Center"])
        new_price = st.number_input(
            "Price (Credits)", min_value=4.0, max_value=20.0, value=10.0, step=0.1
        )
      with col3:
        new_pir = st.number_input(
            "Avg PIR", min_value=0.0, max_value=40.0, value=12.0, step=0.1
        )
        new_yaya = st.number_input(
            "Yaya Rating", min_value=1.0, max_value=10.0, value=8.5, step=0.1
        )

      submit_btn = st.form_submit_button("Add/Update Player")
      if submit_btn and new_player:
        st.success(
            f"Successfully added/updated {new_player} to the roster database!"
        )

  # חיפוש וסינון
  search_query = st.text_input("🔍 Search Player or Team", "")
  filtered_df = df[
      df["Player"].str.contains(search_query, case=False, na=False)
      | df["Team"].str.contains(search_query, case=False, na=False)
  ]

  st.dataframe(filtered_df, use_container_width=True)

elif menu == "Head-to-Head Comparison":
  st.subheader("⚔️ Head-to-Head Player Comparison")
  col1, col2 = st.columns(2)

  player_list = df["Player"].tolist()
  with col1:
    p1 = st.selectbox("Select Player 1", player_list, index=0)
  with col2:
    p2 = st.selectbox(
        "Select Player 2", player_list, index=1 if len(player_list) > 1 else 0
    )

  p1_data = df[df["Player"] == p1].iloc[0]
  p2_data = df[df["Player"] == p2].iloc[0]

  col_a, col_b = st.columns(2)
  with col_a:
    st.markdown(f"### {p1_data['Player']}")
    st.metric("Team", p1_data["Team"])
    st.metric("Price", f"{p1_data['Price']} Cr")
    st.metric("Avg PIR", p1_data["PIR"])
    st.metric("Yaya Rating", p1_data["Yaya_Rating"])

  with col_b:
    st.markdown(f"### {p2_data['Player']}")
    st.metric("Team", p2_data["Team"])
    st.metric("Price", f"{p2_data['Price']} Cr")
    st.metric("Avg PIR", p2_data["PIR"])
    st.metric("Yaya Rating", p2_data["Yaya_Rating"])

elif menu == "Yaya Rating Rankings":
  st.subheader("⭐ Top Players by Yaya Rating")
  sorted_df = df.sort_values(by="Yaya_Rating", ascending=False)
  st.bar_chart(sorted_df.set_index("Player")["Yaya_Rating"])
  st.dataframe(sorted_df, use_container_width=True)
    
