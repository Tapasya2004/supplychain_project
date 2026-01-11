import pandas as pd
import numpy as np

from config import (
    START_DATE,
    END_DATE,
    REGIONS,
    SKU_IDS,
    BASE_DEMAND_RANGE,
    WEEKEND_DEMAND_MULTIPLIER,
    SEASONAL_DEMAND_MULTIPLIER,
    RANDOM_SEED
)
from config import SKU_BASE_COST_RANGE, SKU_MARGIN_RANGE




def generate_orders():
    """
    Generates realistic order (demand) data.

    Core principles:
    - Demand varies by SKU
    - Demand varies by date (seasonality, weekends)
    - Demand varies by region
    - No inventory awareness here (pure demand signal)
    """

    rng = np.random.default_rng(RANDOM_SEED)

    dates = pd.date_range(start=START_DATE, end=END_DATE, freq="D")

    # --------------------------------------------------
    # SKU BASE DEMAND PROFILE (FIXED ACROSS TIME)
    # --------------------------------------------------
    sku_base_demand = {
        sku: rng.integers(BASE_DEMAND_RANGE[0], BASE_DEMAND_RANGE[1] + 1)
        for sku in SKU_IDS
    }

    # Unit price per SKU (stable, realistic)
    sku_base_cost = {
    sku: rng.uniform(*SKU_BASE_COST_RANGE)
    for sku in SKU_IDS
    }

    sku_margin = {
    sku: rng.uniform(*SKU_MARGIN_RANGE)
    for sku in SKU_IDS
    }

    sku_unit_price = {
    sku: round(sku_base_cost[sku] * (1 + sku_margin[sku]), 2)
    for sku in SKU_IDS
    }

    order_records = []
    order_id_counter = 1

    for current_date in dates:
        month = current_date.month
        is_weekend = current_date.weekday() >= 5

        seasonal_multiplier = SEASONAL_DEMAND_MULTIPLIER[month]
        weekend_multiplier = WEEKEND_DEMAND_MULTIPLIER if is_weekend else 1.0

        for region in REGIONS:
            region_multiplier = rng.uniform(0.85, 1.15)  # region demand bias

            for sku in SKU_IDS:
                base_demand = sku_base_demand[sku]

                expected_demand = (
                    base_demand
                    * seasonal_multiplier
                    * weekend_multiplier
                    * region_multiplier
                )

                # --------------------------------------------------
                # STOCHASTIC REALIZATION (CONTROLLED)
                # --------------------------------------------------
                daily_quantity = rng.poisson(lam=max(expected_demand, 0.1))

                if daily_quantity <= 0:
                    continue  # no order that day

                order_records.append({
                    "order_id": f"ORD_{str(order_id_counter).zfill(7)}",
                    "order_date": current_date.date(),
                    "sku_id": sku,
                    "quantity": int(daily_quantity),
                    "unit_price": sku_unit_price[sku],
                    "region": region
                })

                order_id_counter += 1

    orders_df = pd.DataFrame(order_records)

    # --------------------------------------------------
    # HARD CONSTRAINT VALIDATIONS
    # --------------------------------------------------
    assert orders_df["quantity"].min() >= 1, "Invalid order quantity"
    assert orders_df["sku_id"].isin(SKU_IDS).all(), "Unknown SKU detected"
    assert orders_df["region"].isin(REGIONS).all(), "Unknown region detected"
    assert orders_df.isnull().sum().sum() == 0, "Null values detected"

    return orders_df
