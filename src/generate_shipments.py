import pandas as pd
import numpy as np
from datetime import timedelta

from config import (
    BASE_DELAY_PROBABILITY,
    STORM_DELAY_INCREMENT,
    DELAY_DAYS_RANGE,
    BASE_FREIGHT_COST,
    COST_PER_UNIT,
    EXPEDITE_COST_MULTIPLIER,
    RANDOM_SEED
)


def generate_shipments(orders_df, weather_df):
    """
    Generates shipment data strictly derived from orders.

    Shipment rules:
    - One shipment per order
    - Delivery delay depends on weather + randomness
    - Delivered quantity <= ordered quantity
    - Time flows forward (no leakage)
    """

    rng = np.random.default_rng(RANDOM_SEED)

    shipments = []

    for _, order in orders_df.iterrows():

        order_id = order["order_id"]
        order_date = pd.to_datetime(order["order_date"])
        region = order["region"]
        quantity = order["quantity"]

        # --------------------------------------------------
        # DISPATCH DATE (1–2 days after order)
        # --------------------------------------------------
        dispatch_delay = rng.integers(1, 3)
        dispatch_date = order_date + timedelta(days=int(dispatch_delay))

        # --------------------------------------------------
        # BASE EXPECTED DELIVERY (2–5 days after dispatch)
        # --------------------------------------------------
        base_lead_time = rng.integers(2, 6)
        expected_delivery_date = dispatch_date + timedelta(days=int(base_lead_time))

        # --------------------------------------------------
        # WEATHER EFFECT (REGION + DATE)
        # --------------------------------------------------
        weather_match = weather_df[
            (weather_df["date"] == expected_delivery_date.date()) &
            (weather_df["region"] == region)
        ]

        storm_flag = int(weather_match["storm_flag"].iloc[0]) if not weather_match.empty else 0

        delay_probability = BASE_DELAY_PROBABILITY
        if storm_flag == 1:
            delay_probability += STORM_DELAY_INCREMENT

        # --------------------------------------------------
        # ACTUAL DELIVERY DATE
        # --------------------------------------------------
        if rng.random() < delay_probability:
            delay_days = rng.integers(
                DELAY_DAYS_RANGE[0],
                DELAY_DAYS_RANGE[1] + 1
            )
            actual_delivery_date = expected_delivery_date + timedelta(days=int(delay_days))
            delayed = True
        else:
            actual_delivery_date = expected_delivery_date
            delayed = False

        # --------------------------------------------------
        # DELIVERED QUANTITY (PARTIAL RARE)
        # --------------------------------------------------
        if delayed and rng.random() < 0.1:
            delivered_qty = int(quantity * rng.uniform(0.6, 0.9))
        else:
            delivered_qty = quantity

        # --------------------------------------------------
        # FREIGHT COST
        # --------------------------------------------------
        freight_cost = BASE_FREIGHT_COST + (delivered_qty * COST_PER_UNIT)
        if delayed:
            freight_cost *= EXPEDITE_COST_MULTIPLIER

        shipments.append({
            "shipment_id": f"SHP_{order_id}",
            "order_id": order_id,
            "dispatch_date": dispatch_date.date(),
            "expected_delivery_date": expected_delivery_date.date(),
            "actual_delivery_date": actual_delivery_date.date(),
            "delivered_qty": delivered_qty,
            "freight_cost": round(freight_cost, 2),
            "region": region
        })

    shipments_df = pd.DataFrame(shipments)

    # --------------------------------------------------
    # HARD CONSTRAINT VALIDATION
        # --------------------------------------------------
    # HARD CONSTRAINT VALIDATION (ROW-LEVEL)
    # --------------------------------------------------
    validation_df = shipments_df.merge(
        orders_df[["order_id", "quantity"]],
        on="order_id",
        how="left"
    )

    assert (validation_df["delivered_qty"] <= validation_df["quantity"]).all(), \
        "Delivered quantity exceeds ordered quantity"

    assert (shipments_df["actual_delivery_date"] >= shipments_df["dispatch_date"]).all(), \
        "Delivery before dispatch detected"

    assert shipments_df.isnull().sum().sum() == 0, \
        "Null values detected"

    return shipments_df
