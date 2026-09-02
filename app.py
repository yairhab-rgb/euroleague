"""
====================================================================
 EuroLeague Fantasy - Smart Dashboard (No Pyarrow DLL Required)
====================================================================
"""

import streamlit as st
import pandas as pd
import os

# --------------------------------------------------------------
# הגדרות עמוד + עיצוב כהה + RTL מקצועי ללא תלות בספריות חיצוניות
# --------------------------------------------------------------
st.set_page_config(
    page_title="EuroLeague Fantasy - דאשבורד חכם",
    page_icon="🏀",
    layout="wide",
)

DARK_RTL_CSS = """
<style>
    /* ערכת נושא כהה ויישור לימין */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
        direction: rtl;
    }
    section[data-testid="stSidebar"] {
        background-color: #161a23;
        direction: rtl;
    }
    .block-container, h1, h2, h3, h4, p, label, .stMarkdown {
        text-align: right;
    }
    div[data-testid="stMetric"] {
        background-color: #1b1f2a;
        border: 1px solid #2b3040;
        border-radius: 10px;
        padding: 12px;
    }
    
    /* עיצוב פרימיום לטבלת הנתונים (מחליף את st.dataframe שקורס) */
    .custom-table-container {
        overflow-x: auto;
        margin-top: 15px;
        border-radius: 8px;
        border: 1px solid #2b3040;
    }
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .custom-table th, .custom-table td {
        border-bottom: 1px solid #2b3040;
        padding: 12px 10px;
        text-align: center !important;
        color: #fafafa;
        font-size: 15px;
    }
    .custom-table thead th {
        background-color: #1b1f2a;
        color: #a3a8b8;
        font-weight: 600;
        white-space: nowrap;
    }
    .custom-table tbody tr:hover {
        background-color: #242936;
        transition: background-color 0.2s ease;
    }
</style>
"""
st.markdown(DARK_RTL_CSS, unsafe_allow_html=True)

# --------------------------------------------------------------
# מיפוי שמות עמודות
# --------------------------------------------------------------
COLUMN_ALIASES = {
    "שחקן": ["שחקן", "Full Name"],
    "משחקים": ["משחקים", "Games Played"],
    "ממוצע_כללי": ["ממוצע_כללי", "Overall Avg FPT", "Overall Avg PIR"],
    "ממוצע_בית": ["ממוצע_בית", "Home Avg FPT", "Home Avg PIR"],
    "ממוצע_חוץ": ["ממוצע_חוץ", "Away Avg FPT", "Away Avg PIR"],
    "אחוז_מתחת_8": ["אחוז_מתחת_8", "Floor Rate % (FPT<8)", "Floor Rate % (PIR<8)"],
    "אחוז_מעל_20": ["אחוז_מעל_20", "Ceiling Rate % (FPT>=20)", "Ceiling Rate % (PIR>=20)"],
    "ציון_יציבות": ["ציון_יציבות"],
    "_std_dev_raw": ["FPT Std Dev", "PIR Std Dev"],
}

REQUIRED_BASE_COLS = [
    "שחקן", "משחקים", "ממוצע_כללי", "ממוצע_בית",
    "ממוצע_חוץ", "אחוז_מתחת_8", "אחוז_מעל_20",
]

def find_column(df: pd.DataFrame, canonical_name: str):
    for candidate in COLUMN_ALIASES.get(canonical_name, [canonical_name]):
        if candidate in df.columns:
            return candidate
    return None

@st.cache_data
def load_data(file_path_or_buffer, is_csv: bool) -> pd.DataFrame:
    if is_csv:
        raw = pd.read_csv(file_path_or_buffer, encoding="utf-8-sig")
    else:
        raw = pd.read_excel(file_path_or_buffer)

    normalized = pd.DataFrame()
    missing = []
    for canonical in REQUIRED_BASE_COLS:
        col = find_column(raw, canonical)
        if col is None:
            missing.append(canonical)
        else:
            normalized[canonical] = raw[col]

    if missing:
        raise ValueError(f"חסרות עמודות בקובץ: {', '.join(missing)}")

    stability_col = find_column(raw, "ציון_יציבות")
    if stability_col is not None:
        normalized["ציון_יציבות"] = raw[stability_col]
    else:
        std_col = find_column(raw, "_std_dev_raw")
        if std_col is not None:
            std_vals = pd.to_numeric(raw[std_col], errors="coerce")
            min_std, max_std = std_vals.min(), std_vals.max()
            if max_std > min_std:
                normalized["ציון_יציבות"] = 100 * (1 - (std_vals - min_std) / (max_std - min_std))
            else:
                normalized["ציון_יציבות"] = 100.0
        else:
            normalized["ציון_יציבות"] = 50.0

    numeric_cols = ["משחקים", "ממוצע_כללי", "ממוצע_בית", "ממוצע_חוץ",
                     "אחוז_מתחת_8", "אחוז_מעל_20", "ציון_יציבות"]
    for c in numeric_cols:
        normalized[c] = pd.to_numeric(normalized[c], errors="coerce")

    normalized = normalized.dropna(subset=["שחקן", "ממוצע_כללי"])
    return normalized

# --------------------------------------------------------------
# אלגוריתם הציון החכם
# --------------------------------------------------------------
def calculate_smart_rating(row) -> float:
    base_score = (row["ממוצע_כללי"] / 25) * 8
    upside_bonus = (row["אחוז_מעל_20"] / 100) * 2
    risk_penalty = (row["אחוז_מתחת_8"] / 100) * 2
    raw_score = base_score + upside_bonus - risk_penalty
    stability_multiplier = 0.8 + (row["ציון_יציבות"] / 100) * 0.3
    final_score = raw_score * stability_multiplier
    final_score = max(0.0, min(10.0, final_score))
    return round(final_score, 1)

# --------------------------------------------------------------
# טעינת הנתונים למערכת
# --------------------------------------------------------------
st.sidebar.title("🏀 EuroLeague Fantasy")
page = st.sidebar.radio("ניווט", ["📊 דירוג שחקנים כולל", "⚔️ השוואת שחקנים ראש בראש"])
st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("העלה קובץ נתונים", type=["xlsx", "csv"])

df = None
try:
    if uploaded_file is not None:
        is_csv = uploaded_file.name.lower().endswith(".csv")
        df = load_data(uploaded_file, is_csv)
    elif os.path.exists("euroleague_fantasy.xlsx"):
        df = load_data("euroleague_fantasy.xlsx", is_csv=False)
    elif os.path.exists("fantasy_euroleague_stats.csv"):
        df = load_data("fantasy_euroleague_stats.csv", is_csv=True)
    else:
        st.error("⚠️ לא נמצא קובץ נתונים באותה תיקייה. אנא העלה קובץ מהתפריט בצד.")
        st.stop()
except Exception as e:
    st.error(f"⚠️ שגיאה בטעינת הנתונים: {e}")
    st.stop()

df["דירוג חכם"] = df.apply(calculate_smart_rating, axis=1)

# --------------------------------------------------------------
# מסך 1: דירוג שחקנים כולל (ללא pyarrow וללא st.dataframe!)
# --------------------------------------------------------------
if page == "📊 דירוג שחקנים כולל":
    st.title("📊 דירוג שחקנים כולל")
    st.caption("כל השחקנים ממוינים לפי הציון החכם המשוקלל")

    min_games = st.slider(
        "סינון: מינימום משחקים",
        min_value=0,
        max_value=int(df["משחקים"].max()) if not df.empty else 0,
        value=0,
    )

    filtered = df[df["משחקים"] >= min_games].sort_values("דירוג חכם", ascending=False)
    
    display_cols = [
        "שחקן", "משחקים", "ממוצע_כללי", "ממוצע_בית", "ממוצע_חוץ",
        "אחוז_מתחת_8", "אחוז_מעל_20", "ציון_יציבות", "דירוג חכם",
    ]

    # יצירת טבלה ידנית ב-HTML כדי לעקוף את מנגנון האבטחה שחוסם DLL
    table_html = "<div class='custom-table-container'><table class='custom-table'><thead><tr>"
    for col in display_cols:
        col_display = col.replace("_", " ")
        table_html += f"<th>{col_display}</th>"
    table_html += "</tr></thead><tbody>"

    for _, row in filtered.iterrows():
        table_html += "<tr>"
        for col in display_cols:
            val = row[col]
            # צביעת הדירוג החכם לפי ביצועים (ירוק/צהוב/אדום) מותאם לרקע כהה
            if col == "דירוג חכם":
                if val >= 8.0: color = "#1db954"
                elif val >= 5.0: color = "#f39c12"
                else: color = "#e74c3c"
                table_html += f"<td style='color:{color}; font-weight:bold; font-size:16px;'>{val:.1f}</td>"
            elif col == "שחקן":
                table_html += f"<td style='font-weight:bold;'>{val}</td>"
            elif isinstance(val, (float, int)):
                table_html += f"<td>{val:.1f}</td>"
            else:
                table_html += f"<td>{val}</td>"
        table_html += "</tr>"
    table_html += "</tbody></table></div>"

    st.markdown(table_html, unsafe_allow_html=True)
    st.caption(f"מציג {len(filtered)} שחקנים מתוך {len(df)}")

# --------------------------------------------------------------
# מסך 2: השוואת שחקנים ראש בראש
# --------------------------------------------------------------
else:
    st.title("⚔️ השוואת שחקנים ראש בראש")

    players = sorted(df["שחקן"].unique().tolist())
    col_select_a, col_select_b = st.columns(2)
    with col_select_a:
        player_a_name = st.selectbox("שחקן A", players, index=0)
    with col_select_b:
        default_b_index = 1 if len(players) > 1 else 0
        player_b_name = st.selectbox("שחקן B", players, index=default_b_index)

    player_a = df[df["שחקן"] == player_a_name].iloc[0]
    player_b = df[df["שחקן"] == player_b_name].iloc[0]

    st.markdown("---")

    rating_a, rating_b = player_a["דירוג חכם"], player_b["דירוג חכם"]
    if rating_a > rating_b:
        verdict = f"🏆 **{player_a_name}** עדיף (דירוג חכם {rating_a} לעומת {rating_b})"
    elif rating_b > rating_a:
        verdict = f"🏆 **{player_b_name}** עדיף (דירוג חכם {rating_b} לעומת {rating_a})"
    else:
        verdict = "🤝 תיקו - שני השחקנים באותה רמה"

    top_col_a, top_col_mid, top_col_b = st.columns([1, 1.2, 1])
    with top_col_a:
        st.metric(f"דירוג חכם - {player_a_name}", rating_a)
    with top_col_mid:
        st.markdown(f"<h4 style='text-align:center;margin-top:20px'>{verdict}</h4>", unsafe_allow_html=True)
    with top_col_b:
        st.metric(f"דירוג חכם - {player_b_name}", rating_b)

    st.markdown("---")

    METRICS = [
        ("משחקים", "משחקים", False),
        ("ממוצע כללי", "ממוצע_כללי", False),
        ("ממוצע בית", "ממוצע_בית", False),
        ("ממוצע חוץ", "ממוצע_חוץ", False),
        ("אחוז מתחת ל-8 (Risk)", "אחוז_מתחת_8", True),
        ("אחוז מעל 20 (Upside)", "אחוז_מעל_20", False),
        ("ציון יציבות", "ציון_יציבות", False),
    ]

    GREEN = "#1db954"
    NEUTRAL = "#fafafa"

    rows_html = ""
    for label, col, lower_is_better in METRICS:
        val_a = player_a[col]
        val_b = player_b[col]

        if lower_is_better:
            a_better = val_a < val_b
            b_better = val_b < val_a
        else:
            a_better = val_a > val_b
            b_better = val_b > val_a

        color_a = GREEN if a_better else NEUTRAL
        color_b = GREEN if b_better else NEUTRAL
        weight_a = "bold" if a_better else "normal"
        weight_b = "bold" if b_better else "normal"

        rows_html += f"""
        <tr style="border-bottom: 1px solid #2b3040;">
            <td style="color:{color_a}; font-weight:{weight_a}; text-align:center; padding:12px; font-size:16px;">{val_a:.1f}</td>
            <td style="text-align:center; padding:12px; color:#a3a8b8; font-size:15px;">{label}</td>
            <td style="color:{color_b}; font-weight:{weight_b}; text-align:center; padding:12px; font-size:16px;">{val_b:.1f}</td>
        </tr>
        """

    table_html = f"""
    <div style="border: 1px solid #2b3040; border-radius: 8px; overflow: hidden;">
        <table style="width:100%; border-collapse:collapse; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
            <tr style="background-color:#1b1f2a; border-bottom:1px solid #2b3040;">
                <th style="padding:15px; text-align:center; font-size:18px; width:33%;">{player_a_name}</th>
                <th style="padding:15px; text-align:center; font-size:16px; color:#9aa0aa; width:33%;">מדד השוואה</th>
                <th style="padding:15px; text-align:center; font-size:18px; width:33%;">{player_b_name}</th>
            </tr>
            {rows_html}
        </table>
    </div>
    """
    st.markdown(table_html, unsafe_allow_html=True)