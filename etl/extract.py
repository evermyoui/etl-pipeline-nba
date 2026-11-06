from datetime import date
from config import NBA_CONFIG
from nba_api.stats.endpoints import leaguegamelog

import time
import pandas as pd

def season_for(d: date) -> str:
    y = d.year if d.month >= 10 else d.year - 1
    return f"{y}-{str(y + 1)[-2:]}"

def fetch_season(season: str, season_type: str, start: date) -> pd.DataFrame:
    try:
        log = leaguegamelog.LeagueGameLog(
            season=season,
            season_type_all_star=season_type,
            player_or_team_abbreviation="T",
            date_from_nullable=start.strftime("%m/%d/%Y"),
            timeout=NBA_CONFIG.timeout_seconds,
        )
        return log.get_data_frames()[0]
    except Exception as e:
        print(f"Error fetching {season} {season_type}: {e}")
        return pd.DataFrame()

def fetch_all_data(start: date) -> pd.DataFrame:
    first_year = int(season_for(start)[:4])
    last_year = int(season_for(date.today())[:4])
    frames = []
    for y in range(first_year, last_year + 1):
        season = f"{y}-{str(y + 1)[-2:]}"
        for st in NBA_CONFIG.season_types:
            print(f"Fetching {season} {st}...")
            df = fetch_season(season, st, start)
            if not df.empty:
                print(f"  Got {len(df)} rows")
                frames.append(df)
            time.sleep(NBA_CONFIG.sleep_seconds)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
