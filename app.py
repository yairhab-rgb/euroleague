"""
====================================================================
 Yaya's Fantasy Tool - EuroLeague Fantasy Dashboard (2026-27 only)
====================================================================
Data sources (all loaded automatically from the app's folder):
  - round_1.xlsx ... round_N.xlsx  (per-round fantasy box scores)
  - a .xml/.json file from the official EuroLeague stats API
    (used for average minutes played -> Fantasy Points per Minute)
  - injuries.xlsx (optional - injury status badges)
  - schedule.xlsx (optional, not wired in yet - see "FPT Allowed" tab)

The player pool is taken from the LATEST round file found (highest
round number), as requested - not from a separate player list file.
Yaya Rating has been removed entirely at the user's request.
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
# General setup
# --------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Yaya's Fantasy Tool",
    page_icon="🏀",
    layout="wide",
)

DARK_CSS = """
<style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    div[data-testid="stMetric"] {
        background-color: #1b1f2a;
        border: 1px solid #2b3040;
        border-radius: 10px;
        padding: 12px;
    }
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
    .subtitle-line {
        color: #a3a8b8;
        font-size: 15px;
        margin: 2px 0;
    }
</style>
"""
st.markdown(DARK_CSS, unsafe_allow_html=True)

# --------------------------------------------------------------
# Team code -> full team name. Derived by matching players between
# the round files (fantasy team codes) and the official EuroLeague
# stats feed (official team codes/names), since the two sources use
# different abbreviations for the same clubs.
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

def team_full_name(code: str) -> str:
    code = str(code).strip().upper()
    return TEAM_FULL_NAMES.get(code, code)

# --------------------------------------------------------------
# 2026-27 EuroLeague Regular Season calendar (Round, Home, Away),
# as (team fantasy codes). Extracted from the official PDF calendar
# the user provided. 38 rounds x 10 games = 380 games. This is the
# full-season fixture list, so it stays correct all season long and
# does not need to be re-uploaded with every round file.
# --------------------------------------------------------------
SCHEDULE_2026_27 = [
    (1, 'CZV', 'ZAL'), (1, 'DUB', 'RMB'), (1, 'HTA', 'BAY'), (1, 'BAR', 'EFS'), (1, 'KBA', 'OLY'),
    (1, 'ASV', 'MTA'), (1, 'PAO', 'PBB'), (1, 'BJK', 'VBC'), (1, 'FBT', 'VIR'), (1, 'PAR', 'MIL'),
    (2, 'EFS', 'RMB'), (2, 'CZV', 'HTA'), (2, 'DUB', 'BAR'), (2, 'ZAL', 'OLY'), (2, 'VBC', 'KBA'),
    (2, 'MIL', 'VIR'), (2, 'FBT', 'BAY'), (2, 'PBB', 'PAR'), (2, 'MTA', 'BJK'), (2, 'PAO', 'ASV'),
    (3, 'CZV', 'EFS'), (3, 'HTA', 'RMB'), (3, 'VIR', 'OLY'), (3, 'PBB', 'ZAL'), (3, 'BJK', 'BAR'),
    (3, 'ASV', 'VBC'), (3, 'KBA', 'MIL'), (3, 'BAY', 'PAR'), (3, 'FBT', 'DUB'), (3, 'PAO', 'MTA'),
    (4, 'PBB', 'ASV'), (4, 'MTA', 'MIL'), (4, 'BAY', 'VIR'), (4, 'VBC', 'HTA'), (4, 'RMB', 'PAR'),
    (4, 'PAO', 'FBT'), (4, 'DUB', 'CZV'), (4, 'KBA', 'BJK'), (4, 'BAR', 'ZAL'), (4, 'OLY', 'EFS'),
    (5, 'ASV', 'CZV'), (5, 'KBA', 'DUB'), (5, 'MIL', 'RMB'), (5, 'BAR', 'MTA'), (5, 'VBC', 'OLY'),
    (5, 'FBT', 'ZAL'), (5, 'PAR', 'PAO'), (5, 'HTA', 'BJK'), (5, 'EFS', 'BAY'), (5, 'PBB', 'VIR'),
    (6, 'MIL', 'DUB'), (6, 'VBC', 'MTA'), (6, 'RMB', 'ASV'), (6, 'FBT', 'PAR'), (6, 'BJK', 'BAY'),
    (6, 'CZV', 'PBB'), (6, 'ZAL', 'EFS'), (6, 'BAR', 'OLY'), (6, 'VIR', 'KBA'), (6, 'PAO', 'HTA'),
    (7, 'HTA', 'VIR'), (7, 'MTA', 'RMB'), (7, 'MIL', 'BAR'), (7, 'EFS', 'BJK'), (7, 'BAY', 'DUB'),
    (7, 'PAR', 'CZV'), (7, 'PAO', 'KBA'), (7, 'ZAL', 'ASV'), (7, 'PBB', 'VBC'), (7, 'OLY', 'FBT'),
    (8, 'CZV', 'MTA'), (8, 'DUB', 'PBB'), (8, 'KBA', 'RMB'), (8, 'BAY', 'BAR'), (8, 'VBC', 'FBT'),
    (8, 'PAO', 'MIL'), (8, 'HTA', 'EFS'), (8, 'ASV', 'PAR'), (8, 'BJK', 'OLY'), (8, 'VIR', 'ZAL'),
    (9, 'CZV', 'BAY'), (9, 'MTA', 'PBB'), (9, 'RMB', 'FBT'), (9, 'DUB', 'HTA'), (9, 'ASV', 'KBA'),
    (9, 'ZAL', 'PAR'), (9, 'BAR', 'VBC'), (9, 'EFS', 'PAO'), (9, 'VIR', 'BJK'), (9, 'OLY', 'MIL'),
    (10, 'RMB', 'PAO'), (10, 'FBT', 'KBA'), (10, 'HTA', 'BAR'), (10, 'ASV', 'BAY'), (10, 'EFS', 'PBB'),
    (10, 'MIL', 'VBC'), (10, 'BJK', 'ZAL'), (10, 'VIR', 'DUB'), (10, 'PAR', 'MTA'), (10, 'OLY', 'CZV'),
    (11, 'PBB', 'FBT'), (11, 'PAR', 'KBA'), (11, 'MTA', 'HTA'), (11, 'MIL', 'ZAL'), (11, 'VBC', 'BAY'),
    (11, 'RMB', 'CZV'), (11, 'OLY', 'DUB'), (11, 'ASV', 'BJK'), (11, 'EFS', 'VIR'), (11, 'PAO', 'BAR'),
    (12, 'DUB', 'EFS'), (12, 'ZAL', 'BAY'), (12, 'MTA', 'OLY'), (12, 'KBA', 'HTA'), (12, 'MIL', 'CZV'),
    (12, 'BAR', 'PBB'), (12, 'FBT', 'ASV'), (12, 'PAR', 'VBC'), (12, 'VIR', 'PAO'), (12, 'BJK', 'RMB'),
    (13, 'ZAL', 'PAO'), (13, 'MTA', 'DUB'), (13, 'MIL', 'FBT'), (13, 'BAY', 'KBA'), (13, 'VBC', 'VIR'),
    (13, 'PBB', 'HTA'), (13, 'EFS', 'ASV'), (13, 'BAR', 'CZV'), (13, 'PAR', 'BJK'), (13, 'OLY', 'RMB'),
    (14, 'CZV', 'VIR'), (14, 'BJK', 'PBB'), (14, 'BAR', 'FBT'), (14, 'BAY', 'MTA'), (14, 'VBC', 'PAO'),
    (14, 'ASV', 'MIL'), (14, 'DUB', 'PAR'), (14, 'KBA', 'EFS'), (14, 'RMB', 'ZAL'), (14, 'OLY', 'HTA'),
    (15, 'HTA', 'MIL'), (15, 'EFS', 'VBC'), (15, 'BAY', 'PBB'), (15, 'FBT', 'CZV'), (15, 'RMB', 'BAR'),
    (15, 'BJK', 'PAO'), (15, 'ZAL', 'DUB'), (15, 'KBA', 'MTA'), (15, 'VIR', 'PAR'), (15, 'OLY', 'ASV'),
    (16, 'HTA', 'ASV'), (16, 'ZAL', 'KBA'), (16, 'MIL', 'BAY'), (16, 'PBB', 'RMB'), (16, 'FBT', 'EFS'),
    (16, 'DUB', 'BJK'), (16, 'VBC', 'CZV'), (16, 'VIR', 'MTA'), (16, 'PAR', 'BAR'), (16, 'PAO', 'OLY'),
    (17, 'MTA', 'ZAL'), (17, 'VBC', 'DUB'), (17, 'VIR', 'ASV'), (17, 'FBT', 'HTA'), (17, 'PBB', 'OLY'),
    (17, 'RMB', 'BAY'), (17, 'BJK', 'MIL'), (17, 'KBA', 'BAR'), (17, 'PAR', 'EFS'), (17, 'PAO', 'CZV'),
    (18, 'HTA', 'ZAL'), (18, 'ASV', 'DUB'), (18, 'FBT', 'MTA'), (18, 'RMB', 'VBC'), (18, 'CZV', 'BJK'),
    (18, 'EFS', 'MIL'), (18, 'KBA', 'PBB'), (18, 'BAR', 'VIR'), (18, 'BAY', 'PAO'), (18, 'OLY', 'PAR'),
    (19, 'BJK', 'FBT'), (19, 'HTA', 'PAR'), (19, 'ASV', 'BAR'), (19, 'BAY', 'OLY'), (19, 'VIR', 'RMB'),
    (19, 'CZV', 'KBA'), (19, 'DUB', 'PAO'), (19, 'ZAL', 'VBC'), (19, 'MTA', 'EFS'), (19, 'MIL', 'PBB'),
    (20, 'HTA', 'MTA'), (20, 'KBA', 'VBC'), (20, 'FBT', 'PAO'), (20, 'PAR', 'ZAL'), (20, 'RMB', 'DUB'),
    (20, 'ASV', 'OLY'), (20, 'EFS', 'BAR'), (20, 'BAY', 'BJK'), (20, 'VIR', 'MIL'), (20, 'PBB', 'CZV'),
    (21, 'BAR', 'BJK'), (21, 'ZAL', 'PBB'), (21, 'MTA', 'PAO'), (21, 'EFS', 'FBT'), (21, 'MIL', 'HTA'),
    (21, 'VBC', 'PAR'), (21, 'CZV', 'ASV'), (21, 'DUB', 'BAY'), (21, 'KBA', 'VIR'), (21, 'RMB', 'OLY'),
    (22, 'CZV', 'RMB'), (22, 'HTA', 'PBB'), (22, 'ASV', 'ZAL'), (22, 'MTA', 'BAY'), (22, 'BAR', 'MIL'),
    (22, 'VIR', 'EFS'), (22, 'DUB', 'FBT'), (22, 'PAO', 'VBC'), (22, 'BJK', 'PAR'), (22, 'OLY', 'KBA'),
    (23, 'HTA', 'VBC'), (23, 'ZAL', 'CZV'), (23, 'MIL', 'ASV'), (23, 'RMB', 'EFS'), (23, 'PAO', 'BAY'),
    (23, 'BJK', 'KBA'), (23, 'DUB', 'MTA'), (23, 'VIR', 'BAR'), (23, 'PAR', 'FBT'), (23, 'OLY', 'PBB'),
    (24, 'HTA', 'PAO'), (24, 'BAY', 'MIL'), (24, 'FBT', 'BJK'), (24, 'PBB', 'KBA'), (24, 'PAR', 'OLY'),
    (24, 'RMB', 'MTA'), (24, 'CZV', 'BAR'), (24, 'ZAL', 'VIR'), (24, 'EFS', 'DUB'), (24, 'VBC', 'ASV'),
    (25, 'BJK', 'CZV'), (25, 'KBA', 'ZAL'), (25, 'BAY', 'VBC'), (25, 'VIR', 'PBB'), (25, 'OLY', 'MTA'),
    (25, 'ASV', 'HTA'), (25, 'MIL', 'PAR'), (25, 'BAR', 'DUB'), (25, 'FBT', 'RMB'), (25, 'PAO', 'EFS'),
    (26, 'MTA', 'VIR'), (26, 'EFS', 'ZAL'), (26, 'KBA', 'FBT'), (26, 'PBB', 'BJK'), (26, 'PAR', 'RMB'),
    (26, 'PAO', 'DUB'), (26, 'HTA', 'OLY'), (26, 'BAR', 'ASV'), (26, 'BAY', 'CZV'), (26, 'VBC', 'MIL'),
    (27, 'DUB', 'VIR'), (27, 'ZAL', 'BJK'), (27, 'EFS', 'MTA'), (27, 'RMB', 'PBB'), (27, 'ASV', 'FBT'),
    (27, 'KBA', 'CZV'), (27, 'MIL', 'PAO'), (27, 'VBC', 'BAR'), (27, 'PAR', 'HTA'), (27, 'OLY', 'BAY'),
    (28, 'HTA', 'KBA'), (28, 'ASV', 'EFS'), (28, 'BJK', 'DUB'), (28, 'CZV', 'PAR'), (28, 'MTA', 'BAR'),
    (28, 'VBC', 'PBB'), (28, 'VIR', 'BAY'), (28, 'ZAL', 'RMB'), (28, 'FBT', 'MIL'), (28, 'OLY', 'PAO'),
    (29, 'KBA', 'PAR'), (29, 'VBC', 'ZAL'), (29, 'VIR', 'HTA'), (29, 'PBB', 'MTA'), (29, 'PAO', 'BJK'),
    (29, 'CZV', 'FBT'), (29, 'DUB', 'OLY'), (29, 'MIL', 'EFS'), (29, 'BAR', 'RMB'), (29, 'BAY', 'ASV'),
    (30, 'BJK', 'ASV'), (30, 'ZAL', 'BAR'), (30, 'MTA', 'CZV'), (30, 'KBA', 'PAO'), (30, 'BAY', 'EFS'),
    (30, 'VIR', 'FBT'), (30, 'PAR', 'PBB'), (30, 'RMB', 'HTA'), (30, 'DUB', 'VBC'), (30, 'MIL', 'OLY'),
    (31, 'MTA', 'ASV'), (31, 'EFS', 'PAR'), (31, 'BAY', 'HTA'), (31, 'PBB', 'PAO'), (31, 'RMB', 'VIR'),
    (31, 'CZV', 'DUB'), (31, 'ZAL', 'MIL'), (31, 'BAR', 'KBA'), (31, 'FBT', 'VBC'), (31, 'OLY', 'BJK'),
    (32, 'MTA', 'VBC'), (32, 'PAR', 'BAY'), (32, 'FBT', 'PBB'), (32, 'RMB', 'KBA'), (32, 'PAO', 'ZAL'),
    (32, 'BJK', 'EFS'), (32, 'CZV', 'OLY'), (32, 'DUB', 'MIL'), (32, 'ASV', 'VIR'), (32, 'BAR', 'HTA'),
    (33, 'DUB', 'KBA'), (33, 'HTA', 'FBT'), (33, 'ASV', 'PAO'), (33, 'EFS', 'CZV'), (33, 'PBB', 'MIL'),
    (33, 'PAR', 'VIR'), (33, 'ZAL', 'MTA'), (33, 'BAY', 'RMB'), (33, 'VBC', 'BJK'), (33, 'OLY', 'BAR'),
    (34, 'HTA', 'DUB'), (34, 'ASV', 'PBB'), (34, 'EFS', 'KBA'), (34, 'PAO', 'PAR'), (34, 'CZV', 'VBC'),
    (34, 'MIL', 'MTA'), (34, 'BAY', 'ZAL'), (34, 'FBT', 'BAR'), (34, 'RMB', 'BJK'), (34, 'OLY', 'VIR'),
    (35, 'ZAL', 'HTA'), (35, 'VIR', 'CZV'), (35, 'EFS', 'OLY'), (35, 'MTA', 'FBT'), (35, 'MIL', 'BJK'),
    (35, 'VBC', 'RMB'), (35, 'PBB', 'DUB'), (35, 'KBA', 'BAY'), (35, 'BAR', 'PAO'), (35, 'PAR', 'ASV'),
    (36, 'BJK', 'HTA'), (36, 'CZV', 'PAO'), (36, 'KBA', 'ASV'), (36, 'BAR', 'BAY'), (36, 'VIR', 'VBC'),
    (36, 'FBT', 'OLY'), (36, 'PBB', 'EFS'), (36, 'RMB', 'MIL'), (36, 'DUB', 'ZAL'), (36, 'MTA', 'PAR'),
    (37, 'HTA', 'CZV'), (37, 'ASV', 'RMB'), (37, 'MIL', 'KBA'), (37, 'BAY', 'FBT'), (37, 'VBC', 'EFS'),
    (37, 'PBB', 'BAR'), (37, 'PAO', 'VIR'), (37, 'BJK', 'MTA'), (37, 'PAR', 'DUB'), (37, 'OLY', 'ZAL'),
    (38, 'ZAL', 'FBT'), (38, 'CZV', 'MIL'), (38, 'MTA', 'KBA'), (38, 'EFS', 'HTA'), (38, 'PBB', 'BAY'),
    (38, 'PAO', 'RMB'), (38, 'BJK', 'VIR'), (38, 'DUB', 'ASV'), (38, 'BAR', 'PAR'), (38, 'OLY', 'VBC'),
]

def build_schedule_lookup():
    """Maps (round_number, team_code) -> opponent_team_code for every
    game in the 2026-27 regular season."""
    lookup = {}
    for round_num, home, away in SCHEDULE_2026_27:
        lookup[(round_num, home)] = away
        lookup[(round_num, away)] = home
    return lookup

SCHEDULE_LOOKUP = build_schedule_lookup()

# --------------------------------------------------------------
# Name normalization, used to match players across files (round
# files, the official stats feed, and injuries.xlsx). Handles case,
# accents, punctuation, extra spaces and suffixes like Jr./III.
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
# Discover round_*.xlsx files
# --------------------------------------------------------------
_ROUND_FILE_RE = re.compile(r"round[_\-\s]*?(\d+)", re.IGNORECASE)

def discover_round_files(base_dir: str):
    """Returns a sorted list of (round_number, path)."""
    found = {}
    for path in glob.glob(os.path.join(base_dir, "*round*.xlsx")):
        match = _ROUND_FILE_RE.search(os.path.basename(path))
        if match:
            found[int(match.group(1))] = path
    return sorted(found.items(), key=lambda item: item[0])

def round_files_signature(base_dir: str):
    """Cache key: (round_number, path, mtime) per file found. Any change
    to a file (edited / added / removed) changes the signature and
    forces a reload, so the app never keeps showing stale data."""
    sig = []
    for round_num, path in discover_round_files(base_dir):
        try:
            mtime = os.path.getmtime(path)
        except OSError:
            mtime = None
        sig.append((round_num, path, mtime))
    return tuple(sig)

REQUIRED_ROUND_COLS = ["ID", "Name", "Surname", "Position", "Team", "FPT", "Quotation"]
BOX_SCORE_COLS = [
    "Pts", "Reb", "Ast", "Stl", "Tov", "Blk", "Blka",
    "Fd", "Pf", "Fg missed", "Ft missed",
]

def _to_numeric_dash(series: pd.Series) -> pd.Series:
    """Converts a column where '-' represents 0 into numbers."""
    cleaned = series.astype(str).str.strip().str.replace("-", "0", regex=False)
    return pd.to_numeric(cleaned, errors="coerce").fillna(0)

def _read_single_round_file(path: str) -> pd.DataFrame:
    raw = pd.read_excel(path, sheet_name=0)
    raw.columns = [str(c).strip() for c in raw.columns]

    missing = [c for c in REQUIRED_ROUND_COLS if c not in raw.columns]
    if missing:
        raise ValueError(f"Missing columns in {os.path.basename(path)}: {', '.join(missing)}")

    df = raw.dropna(subset=["Name", "Surname"]).copy()
    # Head coaches are not part of the player pool
    df = df[df["Position"].astype(str).str.strip() != "Head Coach"].copy()

    for col in ["Name", "Surname", "Position", "Team"]:
        df[col] = df[col].astype(str).str.strip()

    df["FPT"] = pd.to_numeric(df["FPT"], errors="coerce").fillna(0.0)
    df["Quotation"] = pd.to_numeric(df["Quotation"], errors="coerce")

    for col in BOX_SCORE_COLS:
        if col in df.columns:
            df[col] = _to_numeric_dash(df[col])
        else:
            df[col] = 0.0

    # A player is considered to have "played" a round if any box-score
    # stat is non-zero. The round files have no explicit played/DNP
    # flag, so this is the best inference available from the data
    # (an all-zero row means the player did not take the court).
    df["__played__"] = df[BOX_SCORE_COLS].abs().sum(axis=1) > 0

    df["__pid__"] = df["ID"].astype(str).str.strip()
    if "Active" in df.columns:
        df["__active__"] = pd.to_numeric(df["Active"], errors="coerce").fillna(0) == 1
    else:
        df["__active__"] = True

    return df

@st.cache_data(show_spinner="Loading round files...")
def load_all_round_data(signature):
    """Loads every discovered round file. Returns:
    (combined_df, last_round_num, errors, loaded_round_numbers)"""
    frames = []
    errors = []
    loaded_rounds = []
    for round_num, path, _mtime in signature:
        try:
            df = _read_single_round_file(path)
        except Exception as exc:  # noqa: BLE001 - one bad file must not crash the app
            errors.append(f"Could not read {os.path.basename(path)}: {exc}")
            continue
        df["__round__"] = round_num
        frames.append(df)
        loaded_rounds.append(round_num)

    if not frames:
        return pd.DataFrame(), None, errors, []

    combined = pd.concat(frames, ignore_index=True)
    # Prevent double-counting: one row per player per round
    combined = combined.drop_duplicates(subset=["__pid__", "__round__"])
    last_round_num = max(loaded_rounds)
    return combined, last_round_num, errors, sorted(loaded_rounds)

# --------------------------------------------------------------
# Official minutes-played feed (XML/JSON)
# --------------------------------------------------------------
def _find_minutes_file(base_dir: str):
    candidates = glob.glob(os.path.join(base_dir, "*.xml")) + glob.glob(os.path.join(base_dir, "*.json"))
    return candidates[0] if candidates else None

def _parse_minutes_payload(payload: dict):
    """Expects {"players": [{"player": {"name": "SURNAME, FIRST", ...}, "minutesPlayed": ...}, ...]}"""
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
            for alt_key in ("MinutesPlayed", "minutes_played", "Minutes"):
                if alt_key in entry:
                    minutes = entry[alt_key]
                    break
        if key and minutes is not None:
            rows.append((key, minutes))
    return rows

@st.cache_data(show_spinner="Loading minutes-played data...")
def load_minutes_lookup(path, _mtime):
    if path is None:
        return {}, "No .xml/.json minutes file was found in the app folder."
    try:
        with open(path, "r", encoding="utf-8") as handle:
            text = handle.read()
    except Exception as exc:  # noqa: BLE001
        return {}, f"Could not read the minutes file: {exc}"

    rows = []
    # The supplied file is actually JSON (despite a possible .xml extension) - try that first.
    try:
        payload = json.loads(text)
        rows = _parse_minutes_payload(payload)
    except json.JSONDecodeError:
        # Fall back to real XML parsing in case the format changes later.
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
            return {}, f"Could not parse the minutes file (neither valid JSON nor XML): {exc}"

    lookup = {}
    for key, minutes in rows:
        try:
            lookup[key] = float(minutes)
        except (TypeError, ValueError):
            continue

    if not lookup:
        return {}, "The minutes file was loaded but no valid player minutes were found in it."
    return lookup, None

# --------------------------------------------------------------
# Injuries (optional)
# --------------------------------------------------------------
_INJURY_NAME_ALIASES = ["Player", "Name", "Full Name", "Player Name"]
_INJURY_STATUS_ALIASES = ["Status", "Injury Status", "Injury"]

@st.cache_data(show_spinner="Checking injury data...")
def load_injuries(path, _mtime):
    try:
        raw = pd.read_excel(path)
    except Exception as exc:  # noqa: BLE001
        return {}, f"Could not read injuries.xlsx: {exc}"

    raw.columns = [str(c).strip() for c in raw.columns]
    name_col = next((c for c in _INJURY_NAME_ALIASES if c in raw.columns), None)
    status_col = next((c for c in _INJURY_STATUS_ALIASES if c in raw.columns), None)

    if name_col is None or status_col is None:
        return {}, (
            "Could not find player-name / status columns in injuries.xlsx "
            f"(columns found: {', '.join(raw.columns)}). Injury display is disabled until this is fixed."
        )

    injuries = {}
    for _, row in raw.iterrows():
        name_val = row.get(name_col)
        if not isinstance(name_val, str) or not name_val.strip():
            continue
        status_raw = str(row.get(status_col, "")).strip().upper()
        if "OUT" in status_raw:
            status = "OUT"
        elif "GTD" in status_raw or "QUESTION" in status_raw:
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
        return "<span class='injury-out'>OUT</span>"
    if status == "GTD":
        return "<span class='injury-gtd'>GTD</span>"
    return ""

# --------------------------------------------------------------
# Metric computation (current-season data only)
# --------------------------------------------------------------
@st.cache_data(show_spinner="Computing metrics...")
def build_player_table(round_signature, minutes_path, minutes_mtime):
    combined, last_round_num, round_errors, loaded_rounds = load_all_round_data(round_signature)
    if combined.empty:
        return pd.DataFrame(), round_errors, [], last_round_num, loaded_rounds

    # --- Player pool: the latest round file found ---
    roster = combined[combined["__round__"] == last_round_num].copy()
    roster = roster[roster["__active__"]]
    roster = roster.drop_duplicates(subset=["__pid__"])
    roster = roster[["__pid__", "Name", "Surname", "Team", "Position", "Quotation"]].reset_index(drop=True)
    roster["Player"] = roster["Name"] + " " + roster["Surname"]
    roster["__namekey__"] = roster["Player"].map(normalize_name)
    roster = roster.rename(columns={"Quotation": "Price"})

    # --- Aggregate metrics across every loaded round ---
    played = combined[combined["__played__"]]
    grouped = played.groupby("__pid__")["FPT"]

    games_played = grouped.size()
    avg_fpt = grouped.mean()
    below8_count = played[played["FPT"] < 8].groupby("__pid__").size()
    above20_count = played[played["FPT"] > 20].groupby("__pid__").size()

    stats = pd.DataFrame({
        "Games": games_played,
        "AvgFPT": avg_fpt,
        "Below8Count": below8_count,
        "Above20Count": above20_count,
    })
    stats["Below8Count"] = stats["Below8Count"].fillna(0)
    stats["Above20Count"] = stats["Above20Count"].fillna(0)
    stats["Below8Pct"] = stats["Below8Count"] / stats["Games"] * 100
    stats["Above20Pct"] = stats["Above20Count"] / stats["Games"] * 100

    df = roster.merge(stats, left_on="__pid__", right_index=True, how="left")
    df["Games"] = df["Games"].fillna(0)

    # --- Minutes played (official feed) + Fantasy Points per Minute ---
    minutes_lookup, minutes_warning = load_minutes_lookup(minutes_path, minutes_mtime)
    df["AvgMinutes"] = df["__namekey__"].map(minutes_lookup)
    df["FPM"] = np.where(
        df["AvgMinutes"].notna() & (df["AvgMinutes"] > 0) & (df["Games"] > 0),
        df["AvgFPT"] / df["AvgMinutes"],
        np.nan,
    )

    unmatched_minutes = df[(df["Games"] > 0) & df["AvgMinutes"].isna()]["Player"].tolist()

    # --- Display fields ---
    df["TeamFull"] = df["Team"].map(team_full_name)

    # --- Injuries ---
    injuries, injury_warning = get_injuries_dict()
    df["InjuryStatus"] = df["__namekey__"].map(injuries)

    warnings_list = list(round_errors)
    if minutes_warning:
        warnings_list.append(minutes_warning)
    if injury_warning:
        warnings_list.append(injury_warning)

    return df, warnings_list, unmatched_minutes, last_round_num, loaded_rounds

# --------------------------------------------------------------
# FPT Allowed by Position (defense vs. position)
#
# For every played game, we look up the player's OPPONENT that round
# from the official season schedule (SCHEDULE_LOOKUP), then group by
# (opponent team, player position) to see how many fantasy points that
# opponent's defense allowed, on average, to each position.
# --------------------------------------------------------------
POSITIONS_ORDER = ["Guard", "Forward", "Center"]

@st.cache_data(show_spinner="Computing FPT Allowed by Position...")
def build_fpt_allowed_table(round_signature):
    combined, _last_round_num, _errors, _loaded_rounds = load_all_round_data(round_signature)
    if combined.empty:
        return pd.DataFrame(), 0

    played = combined[combined["__played__"]].copy()
    played["Opponent"] = played.apply(
        lambda r: SCHEDULE_LOOKUP.get((int(r["__round__"]), r["Team"])), axis=1
    )

    unmatched = played["Opponent"].isna().sum()
    played = played.dropna(subset=["Opponent"])

    grouped = played.groupby(["Opponent", "Position"])["FPT"].agg(["mean", "count"]).reset_index()
    avg_pivot = grouped.pivot(index="Opponent", columns="Position", values="mean")
    count_pivot = grouped.pivot(index="Opponent", columns="Position", values="count")

    for pos in POSITIONS_ORDER:
        if pos not in avg_pivot.columns:
            avg_pivot[pos] = np.nan
        if pos not in count_pivot.columns:
            count_pivot[pos] = 0

    result = pd.DataFrame(index=avg_pivot.index)
    for pos in POSITIONS_ORDER:
        result[f"{pos}_avg"] = avg_pivot[pos]
        result[f"{pos}_games"] = count_pivot[pos].fillna(0)
    result = result.reset_index().rename(columns={"Opponent": "TeamCode"})
    result["TeamFull"] = result["TeamCode"].map(team_full_name)
    return result, int(unmatched)

# --------------------------------------------------------------
# Display helpers
# --------------------------------------------------------------
def fmt_num(value, decimals=1, suffix=""):
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return "N/A"
    return f"{value:.{decimals}f}{suffix}"

SORTABLE_COLUMNS = [
    ("Price", "Price"),
    ("AvgFPT", "Avg FPT"),
    ("Below8Pct", "Below 8 pts %"),
    ("Above20Pct", "Above 20 pts %"),
    ("FPM", "FPT / Minute"),
]

def build_table_html(headers, rows_cells):
    """Builds the players table as one flat HTML string with no leading
    whitespace on any line, so Streamlit's markdown renderer treats it
    as raw HTML rather than an indented (and therefore escaped) code
    block."""
    parts = ["<div class='custom-table-container'><table class='custom-table'><thead><tr>"]
    for h in headers:
        parts.append(f"<th>{h}</th>")
    parts.append("</tr></thead><tbody>")
    for cells in rows_cells:
        parts.append("<tr>")
        for cell_html in cells:
            parts.append(f"<td>{cell_html}</td>")
        parts.append("</tr>")
    parts.append("</tbody></table></div>")
    return "".join(parts)

# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------
round_signature = round_files_signature(BASE_DIR)
minutes_path = _find_minutes_file(BASE_DIR)
minutes_mtime = os.path.getmtime(minutes_path) if minutes_path else 0.0

if not round_signature:
    st.error(
        "No round files (round_1.xlsx, round_2.xlsx, ...) were found in the app folder. "
        "Upload at least one round file so the app can show data."
    )
    st.stop()

player_df, data_warnings, unmatched_minutes_players, last_round_num, loaded_rounds = build_player_table(
    round_signature, minutes_path, minutes_mtime
)

if player_df.empty:
    st.error("Could not build the player table from the round files that were found.")
    st.stop()

# --------------------------------------------------------------
# Header
# --------------------------------------------------------------
st.title("Yaya's Fantasy Tool")
st.markdown(
    "<p class='subtitle-line'>EuroLeague Fantasy stats for the 2026-27 season, built from the official round-by-round data.</p>"
    "<p class='subtitle-line'>Browse Average Fantasy Points, consistency (Below 8 / Above 20), Fantasy Points per Minute and price for every active player.</p>"
    "<p class='subtitle-line'>Compare two players head-to-head, or check how much fantasy production each team allows per position.</p>",
    unsafe_allow_html=True,
)

top_col1, top_col2 = st.columns([4, 1])
with top_col1:
    st.caption(
        f"Season 2026-27 - player pool based on Round {last_round_num} - "
        f"rounds loaded: {', '.join(str(r) for r in loaded_rounds)}"
    )
with top_col2:
    if st.button("Refresh data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

if data_warnings:
    with st.expander("Data warnings"):
        for w in data_warnings:
            st.write(f"- {w}")

if unmatched_minutes_players:
    with st.expander(f"{len(unmatched_minutes_players)} players without a minutes match (FPM = N/A)"):
        st.write(", ".join(unmatched_minutes_players))

tab_overall, tab_h2h, tab_fpt_allowed = st.tabs(["Overall", "Head to Head", "FPT Allowed"])

# --------------------------------------------------------------
# Tab 1: Overall
# --------------------------------------------------------------
with tab_overall:
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

    with filter_col1:
        max_games = int(player_df["Games"].max()) if not player_df.empty else 0
        min_games = st.slider("Minimum games played", min_value=0, max_value=max_games, value=0)

    with filter_col2:
        price_series = player_df["Price"].dropna()
        if not price_series.empty:
            price_min, price_max = float(price_series.min()), float(price_series.max())
        else:
            price_min, price_max = 0.0, 0.0
        price_range = st.slider(
            "Fantasy price range",
            min_value=price_min,
            max_value=price_max,
            value=(price_min, price_max),
            step=0.1,
        )

    with filter_col3:
        position_options = sorted(player_df["Position"].dropna().unique().tolist())
        selected_positions = st.multiselect("Position", position_options, default=position_options)

    with filter_col4:
        team_options = sorted(player_df["TeamFull"].dropna().unique().tolist())
        selected_teams = st.multiselect("Team", team_options, default=team_options)

    filtered = player_df[
        (player_df["Games"] >= min_games)
        & (player_df["Price"].isna() | player_df["Price"].between(price_range[0], price_range[1]))
        & (player_df["Position"].isin(selected_positions))
        & (player_df["TeamFull"].isin(selected_teams))
    ].copy()

    if "sort_col" not in st.session_state:
        st.session_state.sort_col = "AvgFPT"
    if "sort_asc" not in st.session_state:
        st.session_state.sort_asc = False

    header_cols = st.columns([2, 1.6, 1] + [1] * len(SORTABLE_COLUMNS))
    header_cols[0].markdown("**Player**")
    header_cols[1].markdown("**Team**")
    header_cols[2].markdown("**Position**")
    for i, (col_key, label) in enumerate(SORTABLE_COLUMNS):
        with header_cols[3 + i]:
            arrow = ""
            if st.session_state.sort_col == col_key:
                arrow = " v" if not st.session_state.sort_asc else " ^"
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

    headers = ["Player", "Team", "Position", "Price", "Avg FPT", "Below 8 pts %", "Above 20 pts %", "FPT / Minute"]
    rows_cells = []
    for _, row in filtered.iterrows():
        player_cell = f"<b>{row['Player']}</b>"
        injury_status = row.get("InjuryStatus")
        if isinstance(injury_status, str):
            player_cell += " " + injury_badge_html(injury_status)

        rows_cells.append([
            player_cell,
            row["TeamFull"],
            row["Position"],
            fmt_num(row["Price"], 1),
            fmt_num(row["AvgFPT"]),
            fmt_num(row["Below8Pct"], 0, "%"),
            fmt_num(row["Above20Pct"], 0, "%"),
            fmt_num(row["FPM"], 2),
        ])

    st.markdown(build_table_html(headers, rows_cells), unsafe_allow_html=True)
    st.caption(f"Showing {len(filtered)} of {len(player_df)} players")

# --------------------------------------------------------------
# Tab 2: Head to Head
# --------------------------------------------------------------
with tab_h2h:
    players_list = sorted(player_df["Player"].unique().tolist())

    default_a = "Sasha Vezenkov" if "Sasha Vezenkov" in players_list else players_list[0]
    default_b = "TJ Shorts" if "TJ Shorts" in players_list else (players_list[1] if len(players_list) > 1 else players_list[0])

    col_select_a, col_select_b = st.columns(2)
    with col_select_a:
        player_a_name = st.selectbox("Player A", players_list, index=players_list.index(default_a))
    with col_select_b:
        player_b_name = st.selectbox("Player B", players_list, index=players_list.index(default_b))

    player_a = player_df[player_df["Player"] == player_a_name].iloc[0]
    player_b = player_df[player_df["Player"] == player_b_name].iloc[0]

    LOW_GAMES_THRESHOLD = 5
    for p, label in ((player_a, player_a_name), (player_b, player_b_name)):
        if p["Games"] < LOW_GAMES_THRESHOLD:
            st.warning(
                f"{label} has only played {int(p['Games'])} game(s) this season - "
                "these metrics may not be stable yet."
            )

    st.markdown("---")

    top_col_a, top_col_mid, top_col_b = st.columns([1, 1.2, 1])
    with top_col_a:
        st.metric(player_a_name, f"{player_a['TeamFull']} - {player_a['Position']}")
        if isinstance(player_a.get("InjuryStatus"), str):
            st.markdown(injury_badge_html(player_a["InjuryStatus"]), unsafe_allow_html=True)
    with top_col_mid:
        st.markdown("<h4 style='text-align:center;margin-top:20px'>Head to Head</h4>", unsafe_allow_html=True)
    with top_col_b:
        st.metric(player_b_name, f"{player_b['TeamFull']} - {player_b['Position']}")
        if isinstance(player_b.get("InjuryStatus"), str):
            st.markdown(injury_badge_html(player_b["InjuryStatus"]), unsafe_allow_html=True)

    st.markdown("---")

    H2H_METRICS = [
        ("Price", "Price", True, 1, ""),
        ("Games", "Games Played", False, 0, ""),
        ("AvgFPT", "Avg Fantasy Points", False, 1, ""),
        ("Below8Pct", "Below 8 pts %", True, 0, "%"),
        ("Above20Pct", "Above 20 pts %", False, 0, "%"),
        ("FPM", "FPT / Minute", False, 2, ""),
    ]

    GREEN = "#1db954"
    NEUTRAL = "#fafafa"

    row_parts = []
    for col, label, lower_is_better, decimals, suffix in H2H_METRICS:
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

        row_parts.append(
            "<tr style='border-bottom: 1px solid #2b3040;'>"
            f"<td style='color:{color_a}; font-weight:{weight_a}; text-align:center; padding:12px; font-size:16px;'>{display_a}</td>"
            f"<td style='text-align:center; padding:12px; color:#a3a8b8; font-size:15px;'>{label}</td>"
            f"<td style='color:{color_b}; font-weight:{weight_b}; text-align:center; padding:12px; font-size:16px;'>{display_b}</td>"
            "</tr>"
        )

    table_html = (
        "<div style='border: 1px solid #2b3040; border-radius: 8px; overflow: hidden;'>"
        "<table style='width:100%; border-collapse:collapse; font-family: \"Segoe UI\", Tahoma, Geneva, Verdana, sans-serif;'>"
        "<tr style='background-color:#1b1f2a; border-bottom:1px solid #2b3040;'>"
        f"<th style='padding:15px; text-align:center; font-size:18px; width:33%;'>{player_a_name}</th>"
        "<th style='padding:15px; text-align:center; font-size:16px; color:#9aa0aa; width:33%;'>Metric</th>"
        f"<th style='padding:15px; text-align:center; font-size:18px; width:33%;'>{player_b_name}</th>"
        "</tr>"
        + "".join(row_parts)
        + "</table></div>"
    )
    st.markdown(table_html, unsafe_allow_html=True)

# --------------------------------------------------------------
# Tab 3: FPT Allowed (defense vs. position)
# --------------------------------------------------------------
with tab_fpt_allowed:
    st.subheader("FPT Allowed by Position")
    st.markdown(
        "For every team, how many fantasy points its defense gives up on average "
        "to each position (Guard / Forward / Center), based on every opponent that "
        "has actually played against that team so far this season. Higher numbers "
        "(green) mean a softer matchup for that position; lower numbers (red) mean "
        "a tougher one. Use this to help decide who to start."
    )
    st.caption(
        "How it's calculated: for every player's performance in a round, the "
        "opponent that round is looked up from the official 2026-27 schedule "
        "(embedded in the app). Each performance is then grouped by (opponent team, "
        "player's position) and averaged - e.g. Guard rows under 'Real Madrid' are "
        "the average fantasy points scored by every Guard who has played against "
        "Real Madrid this season."
    )

    fpt_allowed_df, unmatched_games = build_fpt_allowed_table(round_signature)

    if fpt_allowed_df.empty:
        st.warning("Not enough data yet to compute FPT Allowed by Position.")
    else:
        if unmatched_games:
            st.caption(
                f"Note: {unmatched_games} played game-rows could not be matched to a "
                "schedule entry (round/team combination not found) and were excluded."
            )

        total_games_loaded = len(loaded_rounds)
        if total_games_loaded < 5:
            st.warning(
                f"Only {total_games_loaded} round(s) of data are loaded so far - these "
                "numbers are based on a small sample and will stabilize as more rounds "
                "are added."
            )

        if "fpt_allowed_sort" not in st.session_state:
            st.session_state.fpt_allowed_sort = "Guard_avg"
        if "fpt_allowed_sort_asc" not in st.session_state:
            st.session_state.fpt_allowed_sort_asc = False

        sort_header_cols = st.columns([2] + [1] * len(POSITIONS_ORDER))
        sort_header_cols[0].markdown("**Team**")
        for i, pos in enumerate(POSITIONS_ORDER):
            col_key = f"{pos}_avg"
            with sort_header_cols[1 + i]:
                arrow = ""
                if st.session_state.fpt_allowed_sort == col_key:
                    arrow = " v" if not st.session_state.fpt_allowed_sort_asc else " ^"
                is_active = st.session_state.fpt_allowed_sort == col_key
                if st.button(f"{pos}{arrow}", key=f"fpt_sortbtn_{col_key}", use_container_width=True,
                             type="primary" if is_active else "secondary"):
                    if is_active:
                        st.session_state.fpt_allowed_sort_asc = not st.session_state.fpt_allowed_sort_asc
                    else:
                        st.session_state.fpt_allowed_sort = col_key
                        st.session_state.fpt_allowed_sort_asc = False
                    st.rerun()

        sorted_fpt_allowed = fpt_allowed_df.sort_values(
            st.session_state.fpt_allowed_sort,
            ascending=st.session_state.fpt_allowed_sort_asc,
            na_position="last",
        )

        all_avgs = pd.concat([fpt_allowed_df[f"{p}_avg"] for p in POSITIONS_ORDER]).dropna()
        avg_min = all_avgs.min() if not all_avgs.empty else 0
        avg_max = all_avgs.max() if not all_avgs.empty else 1

        def _allowed_color(value):
            if pd.isna(value) or avg_max <= avg_min:
                return "#fafafa"
            ratio = (value - avg_min) / (avg_max - avg_min)
            if ratio >= 0.66:
                return "#1db954"   # soft matchup
            if ratio <= 0.33:
                return "#e74c3c"   # tough matchup
            return "#f39c12"

        headers = ["Team"] + POSITIONS_ORDER
        rows_cells = []
        for _, row in sorted_fpt_allowed.iterrows():
            cells = [row["TeamFull"]]
            for pos in POSITIONS_ORDER:
                avg_val = row[f"{pos}_avg"]
                games_val = int(row[f"{pos}_games"])
                if pd.isna(avg_val):
                    cells.append("N/A")
                else:
                    color = _allowed_color(avg_val)
                    cells.append(
                        f"<span style='color:{color}; font-weight:bold;'>{avg_val:.1f}</span>"
                        f"<br/><span style='color:#a3a8b8; font-size:11px;'>n={games_val}</span>"
                    )
            rows_cells.append(cells)

        st.markdown(build_table_html(headers, rows_cells), unsafe_allow_html=True)
        st.caption("n = number of individual player performances included in that cell's average.")
