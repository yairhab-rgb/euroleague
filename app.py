"""
====================================================================
 Yaya's Rating - EuroLeague Fantasy Dashboard (2026-27 בלבד)
====================================================================
גרסה מחודשת שמבוססת אך ורק על נתוני העונה הנוכחית:
- קובצי מחזורים round_1.xlsx ... round_N.xlsx (נטענים אוטומטית מהתיקייה)
- קובץ XML/JSON רשמי של היורוליג עם דקות משחק ממוצעות (minutesPlayed)
- injuries.xlsx (פציעות, אופציונלי)

מאגר השחקנים נקבע לפי המחזור האחרון שנמצא (המספר הגבוה ביותר מבין
קובצי round_*.xlsx), כפי שהתבקש - ולא לפי new.csv.
"""

import glob
import json
import os
import re
import unicodedata

import numpy as np
import pandas as pd
import streamlit as st

# --------------------------------------------------------------
# הגדרות כלליות
# --------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Yaya's Rating - EuroLeague Fantasy",
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
        white-space: nowrap;
    }
    .custom-table thead th {
        background-color: #1b1f2a;
        color: #a3a8b8;
        font-weight: 600;
    }
    .custom-table tbody tr:hover {
        background-color: #242936;
        transition: background-color 0.2s ease;
    }

    /* כפתורי המיון שמתפקדים ככותרות טבלה לחיצות */
    div[data-testid="stButton"] button {
        background-color: #1b1f2a;
        border: 1px solid #2b3040;
        color: #a3a8b8;
        font-weight: 600;
        font-size: 13px;
    }
    div[data-testid="stButton"] button:hover {
        background-color: #242936;
        color: #fafafa;
        border-color: #3a4154;
    }
    div[data-testid="stButton"] button[kind="primary"] {
        background-color: #1db954;
        color: #0e1117;
        border-color: #1db954;
    }

    .injury-out {
        color: #e74c3c;
        font-weight: bold;
        font-size: 12px;
    }
    .injury-gtd {
        color: #f39c12;
        font-weight: bold;
        font-size: 12px;
    }
</style>
"""
st.markdown(DARK_RTL_CSS, unsafe_allow_html=True)

# --------------------------------------------------------------
# מיפוי שמות קבוצות (קוד -> שם מלא), נגזר מהתאמה בין קובצי
# המחזורים (קודי הקבוצה של הפנטזי) לבין קובץ הסטטיסטיקה הרשמי
# של היורוליג. אם קוד קבוצה לא מוכר - הקוד עצמו יוצג כברירת מחדל.
# --------------------------------------------------------------
TEAM_FULL_NAMES = {
    "ASV": "LDLC ASVEL Villeurbanne",
    "BAR": "FC Barcelona",
    "BAY": "FC Bayern Munich",
    "BJK": "Besiktas Istanbul",
    "CZV": "Crvena Zvezda Meridianbet Belgrade",
    "DUB": "Dubai Basketball",
    "EFS": "Anadolu Efes Istanbul",
    "FBT": "Fenerbahce Istanbul",
    "HTA": "Hapoel Tel Aviv",
    "KBA": "Baskonia Vitoria-Gasteiz",
    "MIL": "Armani Olimpia Milan",
    "MTA": "Maccabi Rapyd Tel Aviv",
    "OLY": "Olympiacos Piraeus",
    "PAO": "Panathinaikos AKTOR Athens",
    "PAR": "Partizan Mozzart Bet Belgrade",
    "PBB": "Paris Basketball",
    "RMB": "Real Madrid",
    "VBC": "Valencia Basket",
    "VIR": "Virtus Bologna",
    "ZAL": "Zalgiris Kaunas",
}

POSITION_HE = {
    "Guard": "גארד",
    "Forward": "פורוורד",
    "Center": "פיבוט",
}

def team_full_name(code: str) -> str:
    code = str(code).strip().upper()
    return TEAM_FULL_NAMES.get(code, code)

def position_he(pos: str) -> str:
    pos = str(pos).strip()
    return POSITION_HE.get(pos, pos)

# --------------------------------------------------------------
# נרמול שמות - לשם התאמה בין קבצים שונים (מחזורים, XML, פציעות)
# מטפל בהבדלי רישיות, רווחים, סימני פיסוק, גרשיים והטיות (Jr./III)
# --------------------------------------------------------------
_NAME_SUFFIXES = {"JR", "SR", "II", "III", "IV", "V"}

def normalize_name(value) -> str:
    if value is None:
        return ""
    text = unicodedata.normalize("NFKD", str(value))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.upper()
    text = re.sub(r"[^A-Z\s]", " ", text)
    tokens = [t for t in text.split() if t and t not in _NAME_SUFFIXES]
    return " ".join(tokens)

# --------------------------------------------------------------
# איתור קובצי המחזורים (round_1.xlsx, round_2.xlsx, ...)
# --------------------------------------------------------------
_ROUND_FILE_RE = re.compile(r"round[_\-\s]*?(\d+)", re.IGNORECASE)

def discover_round_files(base_dir: str):
    """מחזיר רשימת (מספר_מחזור, נתיב) ממוינת לפי מספר המחזור."""
    found = {}
    for path in glob.glob(os.path.join(base_dir, "*round*.xlsx")):
        match = _ROUND_FILE_RE.search(os.path.basename(path))
        if match:
            round_num = int(match.group(1))
            found[round_num] = path
    return sorted(found.items(), key=lambda item: item[0])

def round_files_signature(base_dir: str):
    """חתימה לקאש: (מספר_מחזור, נתיב, זמן_שינוי) לכל קובץ שנמצא.
    כל שינוי בקובץ (עדכון/הוספה/הסרה) ישנה את החתימה ויאלץ טעינה מחדש."""
    files = discover_round_files(base_dir)
    sig = []
    for round_num, path in files:
        try:
            mtime = os.path.getmtime(path)
        except OSError:
            mtime = None
        sig.append((round_num, path, mtime))
    return tuple(sig)

REQUIRED_ROUND_COLS = ["ID", "Name", "Surname", "Position", "Team", "FPT"]
BOX_SCORE_COLS = [
    "Pts", "Reb", "Ast", "Stl", "Tov", "Blk", "Blka",
    "Fd", "Pf", "Fg missed", "Ft missed",
]

def _to_numeric_dash(series: pd.Series) -> pd.Series:
    """ממיר עמודה שבה '-' מייצג 0, למספרים."""
    cleaned = series.astype(str).str.strip().str.replace("-", "0", regex=False)
    return pd.to_numeric(cleaned, errors="coerce").fillna(0)

def _read_single_round_file(path: str) -> pd.DataFrame:
    raw = pd.read_excel(path, sheet_name=0)
    raw.columns = [str(c).strip() for c in raw.columns]

    missing = [c for c in REQUIRED_ROUND_COLS if c not in raw.columns]
    if missing:
        raise ValueError(f"חסרות עמודות בקובץ {os.path.basename(path)}: {', '.join(missing)}")

    df = raw.dropna(subset=["Name", "Surname"]).copy()
    # הסרת מאמנים - אינם חלק מדירוג השחקנים
    df = df[df["Position"].astype(str).str.strip() != "Head Coach"].copy()

    for col in ["Name", "Surname", "Position", "Team"]:
        df[col] = df[col].astype(str).str.strip()

    df["FPT"] = pd.to_numeric(df["FPT"], errors="coerce").fillna(0.0)

    for col in BOX_SCORE_COLS:
        if col in df.columns:
            df[col] = _to_numeric_dash(df[col])
        else:
            df[col] = 0.0

    # שחקן נחשב כ"שיחק" במחזור אם יש לו סטטיסטיקת משחק כלשהי שאינה אפס.
    # אין בקובץ דגל מפורש של "שיחק/לא שיחק", ולכן זו ההיסק הטוב ביותר
    # הזמין מהנתונים (שורה עם 0 בכל השדות = לא שיחק באותו מחזור).
    df["__played__"] = df[BOX_SCORE_COLS].abs().sum(axis=1) > 0

    df["__pid__"] = df["ID"].astype(str).str.strip()
    if "Active" in df.columns:
        df["__active__"] = pd.to_numeric(df["Active"], errors="coerce").fillna(0) == 1
    else:
        df["__active__"] = True

    return df

@st.cache_data(show_spinner="טוען את קובצי המחזורים...")
def load_all_round_data(signature):
    """טוען את כל קובצי המחזורים שנמצאו, לפי החתימה (round_num, path, mtime).
    מחזיר: (combined_df, last_round_num, errors, loaded_round_numbers)"""
    frames = []
    errors = []
    loaded_rounds = []
    for round_num, path, _mtime in signature:
        try:
            df = _read_single_round_file(path)
        except Exception as exc:  # noqa: BLE001 - לא מפילים את האתר בגלל קובץ בודד
            errors.append(f"⚠️ שגיאה בקריאת {os.path.basename(path)}: {exc}")
            continue
        df["__round__"] = round_num
        frames.append(df)
        loaded_rounds.append(round_num)

    if not frames:
        return pd.DataFrame(), None, errors, []

    combined = pd.concat(frames, ignore_index=True)
    # מניעת ספירה כפולה: שחקן אחד פעם אחת בלבד לכל מחזור
    combined = combined.drop_duplicates(subset=["__pid__", "__round__"])
    last_round_num = max(loaded_rounds)
    return combined, last_round_num, errors, sorted(loaded_rounds)

# --------------------------------------------------------------
# טעינת קובץ הדקות הרשמי (XML/JSON) מה-API של היורוליג
# --------------------------------------------------------------
def _find_minutes_file(base_dir: str):
    candidates = glob.glob(os.path.join(base_dir, "*.xml")) + glob.glob(os.path.join(base_dir, "*.json"))
    return candidates[0] if candidates else None

def _parse_minutes_payload(payload: dict):
    """מצפה למבנה {"players": [{"player": {"name": "SURNAME, FIRST", "team": {...}}, "minutesPlayed": ...}, ...]}"""
    rows = []
    players = payload.get("players", []) if isinstance(payload, dict) else []
    for entry in players:
        player_info = entry.get("player", {}) if isinstance(entry, dict) else {}
        full_name = player_info.get("name", "")
        if not full_name:
            continue
        if "," in full_name:
            surname, first = [p.strip() for p in full_name.split(",", 1)]
        else:
            parts = full_name.split()
            if not parts:
                continue
            surname, first = parts[-1], " ".join(parts[:-1])
        key = normalize_name(f"{first} {surname}")
        minutes = entry.get("minutesPlayed")
        if minutes is None:
            # ניסיון למצוא שדה דומה בשם אחר, למקרה שמבנה הקובץ ישתנה
            for alt_key in ("MinutesPlayed", "minutes_played", "Minutes"):
                if alt_key in entry:
                    minutes = entry[alt_key]
                    break
        if key and minutes is not None:
            rows.append((key, minutes))
    return rows

@st.cache_data(show_spinner="טוען נתוני דקות משחק...")
def load_minutes_lookup(path: str, _mtime: float):
    if path is None:
        return {}, "לא נמצא קובץ XML/JSON עם נתוני דקות משחק בתיקיית האתר."
    try:
        with open(path, "r", encoding="utf-8") as handle:
            text = handle.read()
    except Exception as exc:  # noqa: BLE001
        return {}, f"שגיאה בקריאת קובץ הדקות: {exc}"

    rows = []
    # הקובץ שסופק הוא בפועל JSON (למרות סיומת .xml אפשרית) - ננסה את זה קודם.
    try:
        payload = json.loads(text)
        rows = _parse_minutes_payload(payload)
    except json.JSONDecodeError:
        # נפילה חזרה ל-XML אמיתי, אם פורמט הקובץ ישתנה בעתיד
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(text)
            for el in root.iter():
                attrs = {k.lower(): v for k, v in el.attrib.items()}
                minutes_val = None
                for key in attrs:
                    if "minutesplayed" in key.replace("_", "").replace(" ", ""):
                        minutes_val = attrs[key]
                        break
                name_val = attrs.get("name") or attrs.get("playername")
                if name_val and minutes_val is not None:
                    rows.append((normalize_name(name_val), minutes_val))
        except Exception as exc:  # noqa: BLE001
            return {}, f"לא ניתן לפענח את קובץ הדקות (לא JSON ולא XML תקין): {exc}"

    lookup = {}
    for key, minutes in rows:
        try:
            lookup[key] = float(minutes)
        except (TypeError, ValueError):
            continue

    if not lookup:
        return {}, "קובץ הדקות נטען אך לא נמצאו בו רשומות שחקנים עם דקות משחק תקינות."
    return lookup, None

# --------------------------------------------------------------
# טעינת קובץ פציעות (אופציונלי)
# --------------------------------------------------------------
_INJURY_NAME_ALIASES = ["שחקן", "שם שחקן", "שם", "Player", "Name", "Full Name"]
_INJURY_STATUS_ALIASES = ["סטטוס", "מצב", "Status", "Injury Status", "Injury"]

@st.cache_data(show_spinner="בודק נתוני פציעות...")
def load_injuries(path: str, _mtime: float):
    try:
        raw = pd.read_excel(path)
    except Exception as exc:  # noqa: BLE001
        return {}, f"⚠️ שגיאה בקריאת קובץ הפציעות: {exc}"

    raw.columns = [str(c).strip() for c in raw.columns]
    name_col = next((c for c in _INJURY_NAME_ALIASES if c in raw.columns), None)
    status_col = next((c for c in _INJURY_STATUS_ALIASES if c in raw.columns), None)

    if name_col is None or status_col is None:
        return {}, (
            "⚠️ לא זוהו עמודות שם/סטטוס בקובץ injuries.xlsx "
            f"(העמודות שנמצאו: {', '.join(raw.columns)}). תצוגת הפציעות מושבתת עד לתיקון."
        )

    injuries = {}
    for _, row in raw.iterrows():
        name_val = row.get(name_col)
        if not isinstance(name_val, str) or not name_val.strip():
            continue
        status_raw = str(row.get(status_col, "")).strip().upper()
        if "OUT" in status_raw:
            status = "OUT"
        elif "GTD" in status_raw or "QUESTION" in status_raw or "ספק" in status_raw:
            status = "GTD"
        else:
            continue
        injuries[normalize_name(name_val)] = status
    return injuries, None

def get_injuries_dict():
    path = os.path.join(BASE_DIR, "injuries.xlsx")
    if not os.path.exists(path):
        return {}, None
    return load_injuries(path, os.path.getmtime(path))

def injury_badge_html(status: str) -> str:
    if status == "OUT":
        return "<span class='injury-out'>⛔ OUT</span>"
    if status == "GTD":
        return "<span class='injury-gtd'>❓ GTD</span>"
    return ""

# --------------------------------------------------------------
# חישוב המדדים (כולם מבוססים אך ורק על נתוני העונה הנוכחית)
# --------------------------------------------------------------
@st.cache_data(show_spinner="מחשב מדדים...")
def build_player_table(round_signature, minutes_path, minutes_mtime):
    combined, last_round_num, round_errors, loaded_rounds = load_all_round_data(round_signature)
    if combined.empty:
        return pd.DataFrame(), round_errors, [], last_round_num, loaded_rounds

    # --- מאגר השחקנים: לפי המחזור האחרון שנמצא (round_13 כרגע) ---
    roster = combined[combined["__round__"] == last_round_num].copy()
    roster = roster[roster["__active__"]]
    roster = roster.drop_duplicates(subset=["__pid__"])
    roster = roster[["__pid__", "Name", "Surname", "Team", "Position"]].reset_index(drop=True)
    roster["שחקן"] = roster["Name"] + " " + roster["Surname"]
    roster["__namekey__"] = roster["שחקן"].map(normalize_name)

    # --- צבירת מדדים על פני כל המחזורים שנטענו ---
    played = combined[combined["__played__"]]
    grouped = played.groupby("__pid__")["FPT"]

    games_played = grouped.size()
    avg_fpt = grouped.mean()
    std_fpt = grouped.std()
    below8_count = played[played["FPT"] < 8].groupby("__pid__").size()
    above20_count = played[played["FPT"] > 20].groupby("__pid__").size()

    stats = pd.DataFrame({
        "games_played": games_played,
        "avg_fpt": avg_fpt,
        "std_fpt": std_fpt,
        "below8_count": below8_count,
        "above20_count": above20_count,
    })
    stats["below8_count"] = stats["below8_count"].fillna(0)
    stats["above20_count"] = stats["above20_count"].fillna(0)
    stats["below8_pct"] = stats["below8_count"] / stats["games_played"] * 100
    stats["above20_pct"] = stats["above20_count"] / stats["games_played"] * 100

    df = roster.merge(stats, left_on="__pid__", right_index=True, how="left")
    df["games_played"] = df["games_played"].fillna(0)

    # --- ציון יציבות פנימי (לא מוצג, משמש רק לחישוב Yaya Rating) ---
    std_series = df["std_fpt"]
    min_std, max_std = std_series.min(skipna=True), std_series.max(skipna=True)
    if pd.notna(min_std) and pd.notna(max_std) and max_std > min_std:
        stability = 100 * (1 - (std_series - min_std) / (max_std - min_std))
    else:
        stability = pd.Series(100.0, index=df.index)
    df["_stability"] = stability.fillna(100.0).clip(0, 100)

    # --- דקות משחק מהקובץ הרשמי + נק' פנטזי לדקה ---
    minutes_lookup, minutes_warning = load_minutes_lookup(minutes_path, minutes_mtime)
    df["avg_minutes"] = df["__namekey__"].map(minutes_lookup)
    df["fpm"] = np.where(
        df["avg_minutes"].notna() & (df["avg_minutes"] > 0) & (df["games_played"] > 0),
        df["avg_fpt"] / df["avg_minutes"],
        np.nan,
    )

    unmatched_minutes = df[(df["games_played"] > 0) & df["avg_minutes"].isna()]["שחקן"].tolist()

    # --- Yaya Rating: נוסחת הדירוג הקיימת, מבוססת עונה נוכחית בלבד ---
    def _compute_rating(row):
        if row["games_played"] <= 0 or pd.isna(row["avg_fpt"]):
            return np.nan
        base_score = (row["avg_fpt"] / 25) * 8
        upside_bonus = (row["above20_pct"] / 100) * 2
        risk_penalty = (row["below8_pct"] / 100) * 2
        raw_score = base_score + upside_bonus - risk_penalty
        stability_multiplier = 0.8 + (row["_stability"] / 100) * 0.3
        final_score = raw_score * stability_multiplier
        final_score = max(0.0, min(10.0, final_score))
        return round(final_score, 1)

    df["yaya_rating"] = df.apply(_compute_rating, axis=1)

    # --- תצוגה: קבוצה מלאה + תפקיד בעברית ---
    df["קבוצה"] = df["Team"].map(team_full_name)
    df["תפקיד"] = df["Position"].map(position_he)

    # --- פציעות ---
    injuries, injury_warning = get_injuries_dict()
    df["__injury__"] = df["__namekey__"].map(injuries)

    warnings_list = list(round_errors)
    if minutes_warning:
        warnings_list.append(f"⚠️ {minutes_warning}")
    if injury_warning:
        warnings_list.append(injury_warning)

    return df, warnings_list, unmatched_minutes, last_round_num, loaded_rounds

# --------------------------------------------------------------
# עיצוב ערכים לתצוגה
# --------------------------------------------------------------
def fmt_num(value, decimals=1, suffix=""):
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return "N/A"
    return f"{value:.{decimals}f}{suffix}"

METRIC_COLUMNS = [
    ("avg_fpt", "ממוצע נק' פנטזי"),
    ("below8_pct", "% מתחת ל-8"),
    ("above20_pct", "% מעל 20"),
    ("fpm", "נק' פנטזי לדקה"),
    ("yaya_rating", "Yaya Rating"),
]

# --------------------------------------------------------------
# טעינת הנתונים
# --------------------------------------------------------------
round_signature = round_files_signature(BASE_DIR)
minutes_path = _find_minutes_file(BASE_DIR)
minutes_mtime = os.path.getmtime(minutes_path) if minutes_path else 0.0

if not round_signature:
    st.error(
        "⚠️ לא נמצאו קובצי מחזורים (round_1.xlsx, round_2.xlsx ...) בתיקיית האתר. "
        "יש להעלות לפחות קובץ מחזור אחד כדי שהאתר יוכל להציג נתונים."
    )
    st.stop()

player_df, data_warnings, unmatched_minutes_players, last_round_num, loaded_rounds = build_player_table(
    round_signature, minutes_path, minutes_mtime
)

if player_df.empty:
    st.error("⚠️ לא ניתן היה לבנות את טבלת השחקנים מקובצי המחזורים שנמצאו.")
    st.stop()

# --------------------------------------------------------------
# סרגל צד
# --------------------------------------------------------------
st.sidebar.title("🏀 Yaya's Rating")
page = st.sidebar.radio("ניווט", ["📊 דירוג שחקנים כולל", "⚔️ השוואת שחקנים ראש בראש"])
st.sidebar.markdown("---")
st.sidebar.caption(f"עונת 2026-27 · מאגר השחקנים לפי מחזור {last_round_num}")
st.sidebar.caption(f"מחזורים שנטענו: {', '.join(str(r) for r in loaded_rounds)}")
if st.sidebar.button("🔄 רענן נתונים"):
    st.cache_data.clear()
    st.rerun()

if data_warnings:
    with st.sidebar.expander("⚠️ אזהרות טעינת נתונים", expanded=False):
        for w in data_warnings:
            st.write(w)

if unmatched_minutes_players:
    with st.sidebar.expander(
        f"⚠️ {len(unmatched_minutes_players)} שחקנים ללא התאמת דקות משחק (FPM = N/A)",
        expanded=False,
    ):
        st.write(", ".join(unmatched_minutes_players))

# --------------------------------------------------------------
# מסך 1: דירוג שחקנים כולל
# --------------------------------------------------------------
if page == "📊 דירוג שחקנים כולל":
    st.title("📊 דירוג שחקנים כולל")
    st.caption("כל השחקנים הפעילים ממחזור האחרון, לפי נתוני עונת 2026-27 בלבד")

    max_games = int(player_df["games_played"].max()) if not player_df.empty else 0
    min_games = st.slider("סינון: מינימום משחקים", min_value=0, max_value=max_games, value=0)

    filtered = player_df[player_df["games_played"] >= min_games].copy()

    if "sort_col" not in st.session_state:
        st.session_state.sort_col = "yaya_rating"
    if "sort_asc" not in st.session_state:
        st.session_state.sort_asc = False

    header_cols = st.columns([2, 1.3, 1] + [1] * len(METRIC_COLUMNS))
    header_cols[0].markdown("**שחקן**")
    header_cols[1].markdown("**קבוצה**")
    header_cols[2].markdown("**תפקיד**")
    for i, (col_key, label) in enumerate(METRIC_COLUMNS):
        with header_cols[3 + i]:
            arrow = ""
            if st.session_state.sort_col == col_key:
                arrow = " ▼" if not st.session_state.sort_asc else " ▲"
            is_active = st.session_state.sort_col == col_key
            if st.button(label + arrow, key=f"sortbtn_{col_key}", use_container_width=True,
                         type="primary" if is_active else "secondary"):
                if is_active:
                    st.session_state.sort_asc = not st.session_state.sort_asc
                else:
                    st.session_state.sort_col = col_key
                    st.session_state.sort_asc = False
                st.rerun()

    sort_col = st.session_state.sort_col
    sort_asc = st.session_state.sort_asc
    filtered = filtered.sort_values(sort_col, ascending=sort_asc, na_position="last")

    table_html = "<div class='custom-table-container'><table class='custom-table'><thead><tr>"
    table_html += "<th>שחקן</th><th>קבוצה</th><th>תפקיד</th>"
    for _, label in METRIC_COLUMNS:
        table_html += f"<th>{label}</th>"
    table_html += "</tr></thead><tbody>"

    for _, row in filtered.iterrows():
        player_cell = f"<b>{row['שחקן']}</b>"
        injury_status = row.get("__injury__")
        if isinstance(injury_status, str):
            player_cell += " " + injury_badge_html(injury_status)

        table_html += "<tr>"
        table_html += f"<td style='text-align:right !important;'>{player_cell}</td>"
        table_html += f"<td>{row['קבוצה']}</td>"
        table_html += f"<td>{row['תפקיד']}</td>"
        table_html += f"<td>{fmt_num(row['avg_fpt'])}</td>"
        table_html += f"<td>{fmt_num(row['below8_pct'], 0, '%')}</td>"
        table_html += f"<td>{fmt_num(row['above20_pct'], 0, '%')}</td>"
        table_html += f"<td>{fmt_num(row['fpm'], 2)}</td>"

        rating_val = row["yaya_rating"]
        if pd.isna(rating_val):
            table_html += "<td>N/A</td>"
        else:
            if rating_val >= 8.0:
                color = "#1db954"
            elif rating_val >= 5.0:
                color = "#f39c12"
            else:
                color = "#e74c3c"
            table_html += f"<td style='color:{color}; font-weight:bold; font-size:16px;'>{rating_val:.1f}</td>"
        table_html += "</tr>"

    table_html += "</tbody></table></div>"
    st.markdown(table_html, unsafe_allow_html=True)
    st.caption(f"מציג {len(filtered)} שחקנים מתוך {len(player_df)}")

# --------------------------------------------------------------
# מסך 2: השוואת שחקנים ראש בראש
# --------------------------------------------------------------
else:
    st.title("⚔️ השוואת שחקנים ראש בראש")

    players_list = sorted(player_df["שחקן"].unique().tolist())
    col_select_a, col_select_b = st.columns(2)
    with col_select_a:
        player_a_name = st.selectbox("שחקן A", players_list, index=0)
    with col_select_b:
        default_b_index = 1 if len(players_list) > 1 else 0
        player_b_name = st.selectbox("שחקן B", players_list, index=default_b_index)

    player_a = player_df[player_df["שחקן"] == player_a_name].iloc[0]
    player_b = player_df[player_df["שחקן"] == player_b_name].iloc[0]

    LOW_GAMES_THRESHOLD = 5
    for p, label in ((player_a, player_a_name), (player_b, player_b_name)):
        if p["games_played"] < LOW_GAMES_THRESHOLD:
            st.warning(
                f"⚠️ {label} שיחק רק {int(p['games_played'])} משחקים בעונה הנוכחית - "
                "המדדים עשויים להיות לא יציבים."
            )

    st.markdown("---")

    rating_a = player_a["yaya_rating"]
    rating_b = player_b["yaya_rating"]
    if pd.isna(rating_a) or pd.isna(rating_b):
        verdict = "⚠️ לא ניתן לקבוע עדיפות - לפחות לאחד השחקנים אין מספיק נתונים (N/A)"
    elif rating_a > rating_b:
        verdict = f"🏆 **{player_a_name}** עדיף (Yaya Rating {rating_a} לעומת {rating_b})"
    elif rating_b > rating_a:
        verdict = f"🏆 **{player_b_name}** עדיף (Yaya Rating {rating_b} לעומת {rating_a})"
    else:
        verdict = "🤝 תיקו - שני השחקנים באותה רמה"

    top_col_a, top_col_mid, top_col_b = st.columns([1, 1.2, 1])
    with top_col_a:
        st.metric(f"Yaya Rating - {player_a_name}", fmt_num(rating_a))
        if isinstance(player_a.get("__injury__"), str):
            st.markdown(injury_badge_html(player_a["__injury__"]), unsafe_allow_html=True)
    with top_col_mid:
        st.markdown(f"<h4 style='text-align:center;margin-top:20px'>{verdict}</h4>", unsafe_allow_html=True)
    with top_col_b:
        st.metric(f"Yaya Rating - {player_b_name}", fmt_num(rating_b))
        if isinstance(player_b.get("__injury__"), str):
            st.markdown(injury_badge_html(player_b["__injury__"]), unsafe_allow_html=True)

    st.markdown("---")

    H2H_METRICS = [
        ("ממוצע נק' פנטזי", "avg_fpt", False, 1, ""),
        ("% מתחת ל-8", "below8_pct", True, 0, "%"),
        ("% מעל 20", "above20_pct", False, 0, "%"),
        ("נק' פנטזי לדקה", "fpm", False, 2, ""),
        ("Yaya Rating", "yaya_rating", False, 1, ""),
    ]

    GREEN = "#1db954"
    NEUTRAL = "#fafafa"

    rows_html = ""
    for label, col, lower_is_better, decimals, suffix in H2H_METRICS:
        val_a = player_a[col]
        val_b = player_b[col]

        a_na = pd.isna(val_a)
        b_na = pd.isna(val_b)

        if a_na or b_na:
            a_better = b_better = False
        elif lower_is_better:
            a_better = val_a < val_b
            b_better = val_b < val_a
        else:
            a_better = val_a > val_b
            b_better = val_b > val_a

        color_a = GREEN if a_better else NEUTRAL
        color_b = GREEN if b_better else NEUTRAL
        weight_a = "bold" if a_better else "normal"
        weight_b = "bold" if b_better else "normal"

        display_a = fmt_num(val_a, decimals, suffix)
        display_b = fmt_num(val_b, decimals, suffix)

        rows_html += f"""
        <tr style="border-bottom: 1px solid #2b3040;">
            <td style="color:{color_a}; font-weight:{weight_a}; text-align:center; padding:12px; font-size:16px;">{display_a}</td>
            <td style="text-align:center; padding:12px; color:#a3a8b8; font-size:15px;">{label}</td>
            <td style="color:{color_b}; font-weight:{weight_b}; text-align:center; padding:12px; font-size:16px;">{display_b}</td>
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
