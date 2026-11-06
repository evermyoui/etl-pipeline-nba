
import pandas as pd

COLUMN_ORDER = ["game_id", "game_date", "season_id", "team_id", "team_abbreviation",
                "team_name", "matchup", "is_home", "wl", "win", "pts"]

def transform(new: pd.DataFrame) -> pd.DataFrame:
    if new.empty:
        return new
    df = new.copy()
    df.columns = [c.lower() for c in df.columns]
    df["game_date"] = pd.to_datetime(df["game_date"], errors="coerce").dt.normalize()
    df["is_home"] = df["matchup"].str.contains("vs.", regex=False)
    df["win"] = df["wl"] == "W"
    return df

def finalize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates(subset=["game_id", "team_id"], keep="last")
    present = [c for c in COLUMN_ORDER if c in df.columns]
    rest = [c for c in df.columns if c not in present]
    return (df[present + rest]
            .sort_values(["game_date", "game_id", "team_id"])
            .reset_index(drop=True))