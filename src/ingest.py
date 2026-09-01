# src/ingest.py
import pandas as pd
from pathlib import Path

class GoldDataIngester:
    def __init__(self, gold_dir: str = "data/gold"):
        self.gold_dir = Path(gold_dir)

    def load_table(self, table_name: str) -> pd.DataFrame:
        """Loads a specific Gold parquet table."""
        table_path = self.gold_dir / table_name / f"{table_name}.parquet"
        if not table_path.exists():
            raise FileNotFoundError(f"Gold table not found at: {table_path}")
        df = pd.read_parquet(table_path)
        print(f"Loaded {table_name} with columns: {list(df.columns)}")
        return df

    def load_all(self) -> dict:
        """Loads all Gold datasets into a dictionary of DataFrames."""
        tables = [
            "dim_constructors",
            "dim_drivers",
            "dim_races",
            "fact_session_results",
            "ref_nationality_region"
        ]
        return {table: self.load_table(table) for table in tables}

    def get_merged_session_data(self) -> pd.DataFrame:
        """Joins fact and dimension tables into a unified analytical view."""
        data = self.load_all()
        
        fact = data["fact_session_results"]
        drivers = data["dim_drivers"]
        constructors = data["dim_constructors"]
        races = data["dim_races"]

        # Dynamically inspect columns and perform robust merges
        # (Change keys here if your columns use names like 'raceId' instead of 'race_id')
        df = fact.copy()
        
        if 'driver_id' in df.columns and 'driver_id' in drivers.columns:
            df = df.merge(drivers, on="driver_id", how="left", suffixes=('', '_driver'))
        elif 'driverId' in df.columns and 'driverId' in drivers.columns:
            df = df.merge(drivers, on="driverId", how="left", suffixes=('', '_driver'))

        if 'constructor_id' in df.columns and 'constructor_id' in constructors.columns:
            df = df.merge(constructors, on="constructor_id", how="left", suffixes=('', '_constructor'))
        elif 'constructorId' in df.columns and 'constructorId' in constructors.columns:
            df = df.merge(constructors, on="constructorId", how="left", suffixes=('', '_constructor'))

        if 'race_id' in df.columns and 'race_id' in races.columns:
            df = df.merge(races, on="race_id", how="left", suffixes=('', '_race'))
        elif 'raceId' in df.columns and 'raceId' in races.columns:
            df = df.merge(races, on="raceId", how="left", suffixes=('', '_race'))
        
        return df

if __name__ == "__main__":
    ingester = GoldDataIngester()
    df = ingester.get_merged_session_data()
    print(f"Successfully loaded merged Gold data with shape: {df.shape}")