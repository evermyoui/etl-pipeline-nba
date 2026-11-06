from datetime import date, timedelta
from typing import Tuple, Optional
from config import NBA_CONFIG

import pandas as pd
import os

def load_csv(path) -> pd.DataFrame:
    if os.path.exists(path):
        return pd.read_csv(path, low_memory=False)
    return pd.DataFrame()

def determine_update_range(existing: pd.DataFrame) -> Tuple[bool, Optional[date]]:
    if existing.empty:
        return True, date.fromisoformat(NBA_CONFIG.earliest_date)
    last_day = pd.to_datetime(existing["game_date"], errors="coerce").max().date()
    if last_day >= date.today() - timedelta(days=1):
        return False, None
    return True, last_day + timedelta(days=1)