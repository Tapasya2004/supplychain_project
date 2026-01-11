# Supply Chain Dataset (Synthetic, Realistic)

This repository contains a synthetic but realistic supply chain dataset designed
for analytics, ETL practice, and dashboard development.

The data models demand, inventory, shipments, and weather impacts using
business-driven constraints and logical relationships.

The dataset is suitable for:
- SQL practice
- Power BI / Tableau dashboards
- ETL pipeline development
- Supply chain analytics case studies

---

## Included Tables

The dataset consists of four CSV files:

- weather.csv – daily regional weather conditions  
- orders.csv – customer demand data  
- inventory.csv – daily inventory snapshots  
- shipments.csv – order fulfillment and delivery data  

Each table is described in detail below.

---

## Table Descriptions

### weather.csv
Daily weather conditions by region and date.
Weather is used to model logistics disruption risk.

Key characteristics:
- Storms are rare and regional
- Rainfall increases during storms
- Weather impacts delivery delays, not demand

---

### orders.csv
Customer demand data at SKU, region, and date level.

Key characteristics:
- Demand varies by SKU, region, weekday, and season
- Quantities are always positive
- Selling price is stable at SKU level

---

### inventory.csv
Daily inventory snapshots by SKU and warehouse.

Key characteristics:
- Inventory never goes negative
- Stock levels change only due to sales or replenishment
- Unit cost is stable at SKU level
- Reserved quantity is zero (no backlog modeled)

---

### shipments.csv
Order fulfillment and delivery execution data.

Key characteristics:
- Each shipment corresponds to one order
- Dispatch happens after order date
- Delivery delays are probabilistic and weather-driven
- Delivered quantity never exceeds ordered quantity

---

## Relationships Between Tables

- orders.order_id → shipments.order_id
- orders.sku_id → inventory.sku_id
- orders.region → weather.region
- orders.order_date → weather.date
- shipments.expected_delivery_date → weather.date

All relationships are logically consistent and time-aware.

---

## Sample Data Preview
|![Sample Orders Data](img/sample_orders.png)

![Sample inventory Data](img/sample_inventory.png)

![Sample shipments Data](img/sample_shipment.png)

![Sample weather Data](img/sample_weather.png)

---

## Assumptions & Limitations

- Orders are fulfilled without backlog (no reservation logic)
- One warehouse per region
- One shipment per order
- Weather data is limited to the planning horizon

These assumptions are intentional to keep the dataset
clean, explainable, and suitable for analytics use.

---

## Usage Notes

This dataset is synthetic and intended for learning,
portfolio projects, and demonstrations.
It should not be used for operational decision-making.

---

## License
This dataset is licensed under Creative Commons Attribution–NoDerivatives 4.0
International (CC BY-ND 4.0). Modified versions may not be redistributed.

## Author

Tapasya Mendole 
Aspiring Data Analyst / Business Analyst
