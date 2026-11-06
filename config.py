from dataclasses import dataclass, field
from typing import List
from pathlib import Path

@dataclass
class NBAConfig:
        season_types : List[str] = field(default_factory= lambda: ['Regular Season', 'Playoffs'])
        earliest_date: str = "2025-10-01"
        timeout_seconds: int = 60
        sleep_seconds: float = 1.0   # stats.nba.com rate-limits hard
        output_dir: Path = Path("output")
        output_filename: str = "nba_team_games.csv"

NBA_CONFIG = NBAConfig()