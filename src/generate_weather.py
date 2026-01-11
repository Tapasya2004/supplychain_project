import pandas as pd
import numpy as np
from datetime import timedelta

from config import (
    START_DATE,
    END_DATE,
    REGIONS,
    STORM_PROBABILITY,
    STORM_CLUSTER_DAYS,
    BASE_TEMPERATURE_BY_REGION,
    RANDOM_SEED
)


def generate_weather():
    """
    Generates realistic regional daily weather data.

    Design principles:
    - Weather is external (no dependency on business data)
    - Storms are rare, clustered, and regional
    - Weather affects logistics delays, not demand
    - Deterministic + controlled randomness
    """

    rng = np.random.default_rng(RANDOM_SEED)

    dates = pd.date_range(start=START_DATE, end=END_DATE, freq="D")
    weather_records = []

    for region in REGIONS:
        storm_days_left = 0

        for current_date in dates:

            # --------------------------------------------------
            # STORM GENERATION (RARE + CLUSTERED)
            # --------------------------------------------------
            if storm_days_left > 0:
                storm_flag = 1
                storm_days_left -= 1
            else:
                if rng.random() < STORM_PROBABILITY:
                    storm_flag = 1
                    storm_days_left = rng.integers(1, STORM_CLUSTER_DAYS + 1)
                else:
                    storm_flag = 0

            # --------------------------------------------------
            # RAINFALL LOGIC
            # --------------------------------------------------
            if storm_flag == 1:
                rainfall_mm = rng.uniform(30, 120)   # heavy rainfall
            else:
                rainfall_mm = rng.uniform(0, 8)      # dry / light rain

            # --------------------------------------------------
            # TEMPERATURE LOGIC (SEASONAL + REGIONAL)
            # --------------------------------------------------
            day_of_year = current_date.timetuple().tm_yday
            seasonal_effect = 10 * np.sin(2 * np.pi * day_of_year / 365)

            base_temp = BASE_TEMPERATURE_BY_REGION[region]
            temperature_c = base_temp + seasonal_effect + rng.normal(0, 1.5)

            weather_records.append({
                "date": current_date.date(),
                "region": region,
                "rainfall_mm": round(rainfall_mm, 2),
                "storm_flag": storm_flag,
                "temperature_c": round(temperature_c, 1)
            })

    weather_df = pd.DataFrame(weather_records)

    # --------------------------------------------------
    # HARD CONSTRAINT VALIDATION
    # --------------------------------------------------
    assert weather_df["rainfall_mm"].min() >= 0, "Negative rainfall detected"
    assert weather_df["storm_flag"].isin([0, 1]).all(), "Invalid storm flag"
    assert weather_df.isnull().sum().sum() == 0, "Null values detected"

    # --------------------------------------------------
    # BUSINESS SANITY CHECKS (NON-BREAKING)
    # --------------------------------------------------
    storm_rate = weather_df["storm_flag"].mean()
    if storm_rate > 0.08:
        print("⚠️ Warning: Storm frequency unusually high")

    return weather_df
