from datetime import date

# =========================================================
# 1. GLOBAL TIME CONFIGURATION
# =========================================================

START_DATE = date(2023, 1, 1)
END_DATE   = date(2023, 12, 31)

# =========================================================
# 2. CORE DIMENSIONS
# =========================================================

# Regions where business operates
REGIONS = [
    "North",
    "South",
    "East",
    "West"
]

# Warehouses mapped to regions (1 primary per region for simplicity)
WAREHOUSES = {
    "North": "WH_NORTH",
    "South": "WH_SOUTH",
    "East":  "WH_EAST",
    "West":  "WH_WEST"
}

# Number of unique SKUs
NUM_SKUS = 20

# SKU master (generated once, reused everywhere)
SKU_IDS = [f"SKU_{str(i).zfill(3)}" for i in range(1, NUM_SKUS + 1)]

# =========================================================
# 3. WEATHER PARAMETERS (EXTERNAL SHOCKS)
# =========================================================

# Probability that a storm starts on any given day in a region
STORM_PROBABILITY = 0.03          # ~3% of days

# Once a storm starts, how long it lasts (max)
STORM_CLUSTER_DAYS = 3            # storms persist 1–3 days

# Base average temperatures by region (°C)
BASE_TEMPERATURE_BY_REGION = {
    "North": 18,
    "South": 28,
    "East":  24,
    "West":  22
}

# =========================================================
# 4. DEMAND PARAMETERS
# =========================================================

# Average daily base demand per SKU (before modifiers)
BASE_DEMAND_RANGE = (5, 40)

# Weekend demand multiplier
WEEKEND_DEMAND_MULTIPLIER = 1.2

# Seasonal demand multipliers (month-based)
SEASONAL_DEMAND_MULTIPLIER = {
    1: 0.9,   # Jan
    2: 0.95,
    3: 1.0,
    4: 1.05,
    5: 1.1,
    6: 1.15,
    7: 1.2,
    8: 1.15,
    9: 1.1,
    10: 1.05,
    11: 1.2,
    12: 1.3    # Dec peak
}

# =========================================================
# 5. INVENTORY & REPLENISHMENT LOGIC
# =========================================================

# Lead time in days by SKU category
LEAD_TIME_RANGE = (3, 10)

# Safety stock factor (multiplier on average daily demand)
SAFETY_STOCK_DAYS = 7

# Reorder point formula:
# ROP = (avg_daily_demand * lead_time) + safety_stock
REORDER_BUFFER_MULTIPLIER = 1.0

# Initial inventory coverage (days of demand)
INITIAL_STOCK_DAYS = 25

# =========================================================
# 6. SHIPMENT & LOGISTICS PARAMETERS
# =========================================================

# Probability of delay on normal days
BASE_DELAY_PROBABILITY = 0.1       # ~10%

# Additional delay probability during storm days
STORM_DELAY_INCREMENT = 0.25       # storms significantly hurt OTIF

# Delivery delay range (days)
DELAY_DAYS_RANGE = (1, 3)

# Freight cost parameters
BASE_FREIGHT_COST = 50
COST_PER_UNIT = 2.0
EXPEDITE_COST_MULTIPLIER = 1.5

# =========================================================
# 7. RANDOMNESS CONTROL
# =========================================================

# Global seed to make results reproducible
RANDOM_SEED = 42

# =========================================================
# 8. SKU COST & MARGIN MODEL (FINANCIAL LOGIC)
# =========================================================

# Base cost per SKU (manufacturing / procurement)
SKU_BASE_COST_RANGE = (25, 100)

# Gross margin range per SKU (15% – 45%)
SKU_MARGIN_RANGE = (0.15, 0.45)

