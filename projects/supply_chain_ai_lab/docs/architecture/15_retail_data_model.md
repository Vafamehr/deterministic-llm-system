# Retail Data Model

## Purpose

Defines the **core data structure** used across the system.

All modules operate on a shared key:

SKU × Location × Time

This allows consistent representation of:

- demand  
- inventory  
- shipments  
- decisions  
- disruptions  

---

## One-Line Summary

All supply chain data is structured as **SKU × Location × Time**.

---

## Core Dimensions

### SKU (Product)

Represents a unique product.

Examples:

- Coke 12oz  
- Nike Air Max  
- iPhone 14  

Attributes may include:

- category  
- brand  
- price  
- cost  
- shelf life  
- supplier  

**Mental Hook:** what product

---

### Location

Represents a node in the supply chain.

#### Store

- demand point  
- customer-facing  
- limited capacity  

#### Warehouse / DC

- inventory storage  
- supplies stores  
- redistribution hub  

**Mental Hook:** where inventory exists

---

### Time

Discrete planning periods:

- daily  
- weekly  

Example:

| week | start_date |
|------|------------|
| 2024-W01 | 2024-01-01 |

**Mental Hook:** when events happen

---

## Core Tables

### Sales Table

Primary demand signal.

| sku | store | week | units_sold |
|-----|-------|------|------------|

Used by forecasting.

---

### Inventory Table

Tracks available stock.

| sku | location | week | inventory_on_hand |
|-----|----------|------|-------------------|

Used by:

- inventory module  
- replenishment  
- simulation  

---

### Shipment Table

Tracks inventory movement.

| sku | from | to | week | units |

Represents flow across network.

---

### Lead Time Table

Defines replenishment delay.

| supplier | sku | lead_time_days |

Used for:

- reorder logic  
- safety stock  
- simulation  

---

### Promotion Table

Captures demand drivers.

| sku | store | week | promotion_type |

Used in forecasting.

---

## Relationship to Forecasting

Sales data → demand signals → forecasts  

Pipeline:

Sales  
→ demand records  
→ time series  
→ features  
→ model  

---

## Relationship to Other Modules

Shared structure enables all modules:

- forecasting → sales  
- inventory → inventory table  
- replenishment → demand + inventory + lead time  
- simulation → modifies inputs  
- allocation → distributes inventory  
- monitoring → aggregates signals  

---

## Design Principle

Single unified structure:

SKU × Location × Time  

This ensures:

- consistency  
- modular integration  
- easy extension  

---

## Mental Model

SKU = what  
Location = where  
Time = when  

---

## Final View

The data model is the **foundation of the system**, enabling all modules to operate on a consistent and unified representation of supply chain data.