from config import NBA_CONFIG
from etl.load import load_csv, determine_update_range
from etl.transform import transform, finalize
from etl.extract import fetch_all_data

import pandas as pd

def run_etl_pipeline() -> pd.DataFrame:
    NBA_CONFIG.output_dir.mkdir(parents=True, exist_ok=True)
    out_path = NBA_CONFIG.output_dir / NBA_CONFIG.output_filename

    existing = load_csv(out_path)
    if not existing.empty:
        existing["game_date"] = pd.to_datetime(existing["game_date"], errors="coerce")

    should_update, start = determine_update_range(existing)
    if not should_update:
        print("Already up to date.")
        return existing

    fetched = transform(fetch_all_data(start))
    merged = pd.concat([existing, fetched], ignore_index=True)
    final = finalize(merged)
    final.to_csv(out_path, index=False)
    return final

if __name__ == "__main__":
    run_etl_pipeline()