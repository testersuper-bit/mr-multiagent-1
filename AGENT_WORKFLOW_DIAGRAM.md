# Multi-Agent Workflow Diagram

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                     QUOTE REQUEST PROCESSING SYSTEM                 │
└─────────────────────────────────────────────────────────────────────┘

                           ┌──────────────────┐
                           │  Quote Requests  │
                           │     Dataset      │
                           │  (401 requests)  │
                           └────────┬─────────┘
                                    │
                                    ▼
                    ┌────────────────────────────────┐
                    │   ORCHESTRATOR AGENT           │
                    │  (Request Router & Coordinator)│
                    ├────────────────────────────────┤
                    │ • Parse customer request       │
                    │ • Extract: job, need_size,     │
                    │   event, request_date          │
                    │ • Route to worker agents       │
                    │ • Aggregate results            │
                    │ • Track cash flow              │
                    └────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ INVENTORY MGR    │ │ QUOTE GENERATOR  │ │   SALES AGENT    │
│     AGENT        │ │      AGENT       │ │      AGENT       │
├──────────────────┤ ├──────────────────┤ ├──────────────────┤
│ Responsibilities:│ │ Responsibilities:│ │ Responsibilities:│
│ • Check stock    │ │ • Calculate      │ │ • Confirm order  │
│ • Assess avail.  │ │   pricing        │ │ • Record trans.  │
│ • Verify delivery│ │ • Apply discounts│ │ • Update balance │
│   feasibility    │ │ • Generate quote │ │ • Send response  │
├──────────────────┤ ├──────────────────┤ ├──────────────────┤
│ Tools:           │ │ Tools:           │ │ Tools:           │
│ • get_inventory()│ │ • get_inventory()│ │ •record_trans.() │
│ • get_item_stock│ │ • estimate_deliv.│ │ •get_cash_balance│
│   ()            │ │   ()             │ │   ()             │
│                 │ │                  │ │                  │
└────────┬────────┘ └────────┬─────────┘ └────────┬─────────┘
         │ (Availability)    │ (Quote)            │ (Fulfillment)
         │ (Delivery Date)   │ (Pricing)          │ (Transaction)
         │                   │                    │
         └───────────────────┼────────────────────┘
                             │
                             ▼
                    ┌────────────────────┐
                    │  Response Output   │
                    │  • Approved quote  │
                    │  • Delivery date   │
                    │  • Price & rationale
                    │  • Or denial with  │
                    │    reason          │
                    └────────────────────┘


DATA FLOW DETAILS
═══════════════════════════════════════════════════════════════════════

REQUEST: {job, need_size, event, request_date, mood}
    │
    ▼
ORCHESTRATOR: Parse & validate request
    │
    ▼
    ├─► INVENTORY MANAGER:
    │   • Call: get_inventory(request_date)
    │   • Call: get_item_stock(item_id, request_date)
    │   • Return: {available: bool, stock_level: int}
    │
    ├─► QUOTE GENERATOR:
    │   • Receives: stock_level from Inventory Agent
    │   • Call: estimate_delivery_time(units_requested)
    │   • Calculates: base_price * quantity * (1 - bulk_discount)
    │   • Return: {price: float, explanation: str, delivery_days: int}
    │
    └─► SALES AGENT:
        • If approved by customer:
        • Call: record_transaction(transaction_type='sale')
        • Call: get_cash_balance()
        • Update: database with order details
        • Return: {transaction_id, cash_balance, confirmation}


AGENT INTERACTION SEQUENCE
═══════════════════════════════════════════════════════════════════════

1. ORCHESTRATOR receives quote request
   │
2. ORCHESTRATOR → INVENTORY MANAGER
   │  "Check if 500 units of Standard Paper available by Apr 15"
   │
3. INVENTORY MANAGER → Database
   │  queries inventory table for date & item
   │
4. INVENTORY MANAGER ← Result
   │  "500 units available; delivery: 4 days"
   │
5. ORCHESTRATOR → QUOTE GENERATOR
   │  "Generate quote for 500 units, 4-day delivery"
   │
6. QUOTE GENERATOR → Tools
   │  estimates delivery time, calculates bulk discount
   │
7. QUOTE GENERATOR ← Result
   │  "Quote: $5,000 (bulk discount applied)"
   │
8. ORCHESTRATOR → SALES AGENT
   │  "Approve and fulfill order for $5,000"
   │
9. SALES AGENT → Database
   │  records transaction, updates cash balance
   │
10. SALES AGENT ← Result
    │  "Order recorded; new balance: $55,000"
    │
11. ORCHESTRATOR ← All results
    │  aggregates and returns customer response


TOOLS UTILIZED BY AGENTS
═══════════════════════════════════════════════════════════════════════

Tool #1: create_inventory()
   Used by: INVENTORY MANAGER (on system initialization)
   Purpose: Seed inventory with 45 paper products, random stock 200-800

Tool #2: setup_db()
   Used by: ORCHESTRATOR (on system initialization)
   Purpose: Create SQLite database with tables: transactions, quotes, inventory

Tool #3: record_transaction(transaction_type, item_id, quantity, cost, date)
   Used by: SALES AGENT
   Purpose: Log stock orders (purchases from suppliers) or sales to customers

Tool #4: get_inventory(date)
   Used by: INVENTORY MANAGER, QUOTE GENERATOR
   Purpose: Return dict of all items with positive stock as of date

Tool #5: get_item_stock(item_id, date)
   Used by: INVENTORY MANAGER
   Purpose: Return detailed stock history for specific item

Tool #6: estimate_delivery_time(units)
   Used by: QUOTE GENERATOR
   Purpose: Calculate delivery days based on order quantity
      ≤10 units → same day (0 days)
      11-100 units → 1 day
      101-1000 units → 4 days
      >1000 units → 7 days

Tool #7: get_cash_balance()
   Used by: SALES AGENT, ORCHESTRATOR
   Purpose: Return net balance (sales revenue - inventory purchase costs)

Tool #8 (Bonus): get_financial_summary()
   Used by: ORCHESTRATOR (for reporting)
   Purpose: Full snapshot with cash, inventory value, top sellers


AGENT RESPONSIBILITY BOUNDARIES
═══════════════════════════════════════════════════════════════════════

ORCHESTRATOR AGENT (Controller):
   Input: Quote requests (CSV rows)
   Output: Customer-facing responses
   Domain: Request routing, result aggregation, customer communication
   No direct database writes

INVENTORY MANAGER AGENT (Domain Expert - Supply):
   Input: Item name, request date, requested quantity
   Output: Availability boolean, delivery feasibility, stock levels
   Domain: Inventory queries only
   Tools: get_inventory(), get_item_stock(), estimate_delivery_time()

QUOTE GENERATOR AGENT (Domain Expert - Pricing):
   Input: Item, quantity, availability status, delivery days
   Output: Price quote, discount rationale, delivery estimate
   Domain: Pricing logic and discount calculations
   Tools: Calculation based on received data

SALES AGENT (Domain Expert - Fulfillment):
   Input: Approved quote details
   Output: Transaction confirmation, updated cash balance
   Domain: Order recording, financial transactions
   Tools: record_transaction(), get_cash_balance()


CUSTOMER-FACING OUTPUT (Sensitive Data Handling)
═══════════════════════════════════════════════════════════════════════

✓ INCLUDED:
   • Quote price (business value)
   • Delivery estimate (relevant for planning)
   • Discount explanation (transparency)
   • Confirmation details (order tracking)
   • Request fulfillment status

✗ EXCLUDED (Internal Only):
   • Unit cost / inventory purchase prices
   • Margin/profit calculations
   • Total cash balance (shows company finances)
   • Individual employee IDs (PII)
   • Raw inventory levels (competitive info)
   • Internal agent communication logs

ERROR HANDLING & EDGE CASES
═══════════════════════════════════════════════════════════════════════

OUT OF STOCK:
   INVENTORY MANAGER → "Not available" → ORCHESTRATOR
   → Customer: "Sorry, insufficient inventory. Alternative suggestions: [X, Y, Z]"

IMPOSSIBLE DELIVERY DATE:
   INVENTORY MANAGER: "Requested date before possible delivery"
   → ORCHESTRATOR → Customer: "Delivery not feasible by requested date"

INVALID REQUEST DATA:
   ORCHESTRATOR validates → If missing required fields
   → Customer: "Unable to process - please provide [field]"

DATABASE ERROR:
   Any agent → Error in tool execution
   → ORCHESTRATOR catches → Customer: "System error, please retry"
```

## Implementation Sequence

1. **Initialize System** (Orchestrator)
   - Call `setup_db()` → Create SQLite database
   - Call `create_inventory()` → Seed 45 products
   - Set starting cash balance: $50,000

2. **For Each Request** in quote_requests.csv:
   - Orchestrator routes to Inventory Manager
   - Inventory Manager checks availability & delivery
   - Orchestrator routes to Quote Generator
   - Quote Generator calculates price
   - Orchestrator routes to Sales Agent (if approved)
   - Sales Agent records transaction
   - Orchestrator returns response to customer

3. **Tracking Metrics**:
   - Cash balance changes (starting $50,000 → final balance)
   - Successful quotes generated (count ≥ 3)
   - Unfulfilled requests (reasons: out of stock, impossible date)
   - Processing time per request

4. **Output Results**:
   - `test_results.csv` with request ID, status, price, delivery date
   - Summary statistics
   - Architecture reflection & improvement suggestions
