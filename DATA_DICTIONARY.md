# Data Dictionary – Supply Chain Dataset

This document describes each column in the dataset.

---

## weather.csv

date  
Calendar date of the weather record.

region  
Geographical business region.

rainfall_mm  
Daily rainfall in millimeters.

storm_flag  
Indicator of severe weather (1 = storm, 0 = normal).

temperature_c  
Average daily temperature in Celsius.

---

## orders.csv

order_id  
Unique identifier for each customer order.

order_date  
Date when the order was placed.

sku_id  
Unique product identifier.

quantity  
Number of units ordered.

unit_price  
Selling price per unit.

region  
Region where the order was placed.

---

## inventory.csv

snapshot_date  
Date of the inventory snapshot.

sku_id  
Unique product identifier.

warehouse_id  
Warehouse where the SKU is stored.

on_hand_qty  
Available physical inventory quantity.

reserved_qty  
Quantity reserved for open orders (zero in current version).

last_movement_date  
Most recent date when inventory changed.

unit_cost  
Cost per unit of the SKU.

---

## shipments.csv

shipment_id  
Unique identifier for the shipment.

order_id  
Reference to the originating order.

dispatch_date  
Date the shipment left the warehouse.

expected_delivery_date  
Planned delivery date.

actual_delivery_date  
Actual delivery completion date.

delivered_qty  
Quantity delivered to the customer.

freight_cost  
Transportation cost of the shipment.

region  
Delivery region.
