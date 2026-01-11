import pandas as pd
import numpy as np

from config import (
    START_DATE,
    END_DATE,
    SKU_IDS,
    WAREHOUSES,
    LEAD_TIME_RANGE,
    SAFETY_STOCK_DAYS,
    INITIAL_STOCK_DAYS,
    RANDOM_SEED
)
from config import SKU_BASE_COST_RANGE



def generate_inventory(orders_df):
    """
    Generates daily inventory snapshots with strict causal logic.

    Inventory rules:
    - No negative inventory
    - Stock only changes due to sales or replenishment
    - Reorder Point (ROP) logic enforced
    """

    rng = np.random.default_rng(RANDOM_SEED)
    dates = pd.date_range(start=START_DATE, end=END_DATE, freq="D")

    sku_unit_cost = {
    sku: rng.uniform(*SKU_BASE_COST_RANGE)
    for sku in SKU_IDS
    }


    # --------------------------------------------------
    # SKU PARAMETERS (FIXED)
    # --------------------------------------------------
    avg_daily_demand = {
        sku: orders_df[orders_df["sku_id"] == sku]["quantity"].mean()
        for sku in SKU_IDS
    }

    lead_time = {
        sku: rng.integers(LEAD_TIME_RANGE[0], LEAD_TIME_RANGE[1] + 1)
        for sku in SKU_IDS
    }

    reorder_point = {
        sku: int(avg_daily_demand[sku] * (lead_time[sku] + SAFETY_STOCK_DAYS))
        for sku in SKU_IDS
    }

    # --------------------------------------------------
    # INITIAL INVENTORY
    # --------------------------------------------------
    inventory_state = {}

    for sku in SKU_IDS:
        initial_qty = int(avg_daily_demand[sku] * INITIAL_STOCK_DAYS)
        inventory_state[sku] = {
            "on_hand": initial_qty,
            "reserved": 0,
            "last_movement_date": START_DATE
        }

    records = []

    for current_date in dates:

        daily_orders = orders_df[orders_df["order_date"] == current_date.date()]

        for region, warehouse_id in WAREHOUSES.items():

            region_orders = daily_orders[daily_orders["region"] == region]

            for sku in SKU_IDS:

                sku_orders = region_orders[region_orders["sku_id"] == sku]
                sales_qty = sku_orders["quantity"].sum()

                on_hand = inventory_state[sku]["on_hand"]

                # --------------------------------------------------
                # SALES REDUCE INVENTORY
                # --------------------------------------------------
                actual_sales = min(on_hand, sales_qty)
                on_hand -= actual_sales

                # --------------------------------------------------
                # REPLENISHMENT LOGIC
                # --------------------------------------------------
                replenishment_qty = 0
                if on_hand <= reorder_point[sku]:
                    replenishment_qty = reorder_point[sku] * 2
                    on_hand += replenishment_qty

                # --------------------------------------------------
                # UPDATE STATE
                # --------------------------------------------------
                inventory_state[sku]["on_hand"] = on_hand

                if actual_sales > 0 or replenishment_qty > 0:
                    inventory_state[sku]["last_movement_date"] = current_date.date()

                records.append({
                    "snapshot_date": current_date.date(),
                    "sku_id": sku,
                    "warehouse_id": warehouse_id,
                    "on_hand_qty": int(on_hand),
                    "reserved_qty": 0,
                    "last_movement_date": inventory_state[sku]["last_movement_date"],
                    "unit_cost": round(sku_unit_cost[sku], 2)

                })

    inventory_df = pd.DataFrame(records)

    # --------------------------------------------------
    # HARD CONSTRAINT CHECKS
    # --------------------------------------------------
    assert inventory_df["on_hand_qty"].min() >= 0
    assert inventory_df["reserved_qty"].max() <= inventory_df["on_hand_qty"].max()
    assert inventory_df.isnull().sum().sum() == 0

    return inventory_df

# #today_on_hand
# = yesterday_on_hand
# – today_sales
# + today_replenishment
