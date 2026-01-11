import os

from generate_weather import generate_weather
from generate_orders import generate_orders
from generate_inventory import generate_inventory
from generate_shipments import generate_shipments


def main():
    """
    End-to-end data generation pipeline.

    Execution order is CRITICAL:
    1. Weather (external)
    2. Orders (demand)
    3. Inventory (stateful, depends on orders)
    4. Shipments (depends on orders + weather)
    """

    # --------------------------------------------------
    # Ensure data directory exists
    # --------------------------------------------------
    os.makedirs("data", exist_ok=True)

    print("⏳ Generating weather data...")
    weather_df = generate_weather()
    weather_df.to_csv("data/weather.csv", index=False)
    print("✅ weather.csv saved")

    print("⏳ Generating orders data...")
    orders_df = generate_orders()
    orders_df.to_csv("data/orders.csv", index=False)
    print("✅ orders.csv saved")

    print("⏳ Generating inventory data...")
    inventory_df = generate_inventory(orders_df)
    inventory_df.to_csv("data/inventory.csv", index=False)
    print("✅ inventory.csv saved")

    print("⏳ Generating shipment data...")
    shipments_df = generate_shipments(orders_df, weather_df)
    shipments_df.to_csv("data/shipments.csv", index=False)
    print("✅ shipments.csv saved")

    print("\n🎉 DATA PIPELINE COMPLETED SUCCESSFULLY")
    print("📁 Files created in /data directory")


if __name__ == "__main__":
    main()
