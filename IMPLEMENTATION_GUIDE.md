# Implementation Guide: Multi-Agent Quote Processing System

## Quick Start

### Prerequisites
- Python 3.10+
- OpenAI API key (from Udacity)
- Required packages (auto-installed): pandas, openai, SQLAlchemy, python-dotenv, smolagents, pydantic

### Setup

1. **Configure API Key**
   ```bash
   # Edit .env file and add your Udacity OpenAI API key
   UDACITY_OPENAI_API_KEY=your_api_key_here
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install smolagents pydantic
   ```

3. **Run System**
   ```bash
   python project_starter.py
   ```

### Expected Output

```
==============================================================
INITIAL STATE
==============================================================
Starting Cash: $50,000.00
Starting Inventory Value: [calculated value]
Total Initial Assets: [sum]
Processing 401 requests...
==============================================================

Progress: Processed 50/401 requests...
Progress: Processed 100/401 requests...
...
Progress: Processed 400/401 requests...

==============================================================
FINAL STATE SUMMARY
==============================================================
Requests Processed: 401
Successful Quotes: [count]
Unfulfilled Requests: [count]
Success Rate: [percentage]%

Cash Changes Recorded: [count]
  First change: [details]
  Last change: [details]

Final Cash Balance: $[amount]
Initial Cash Balance: $50,000.00
Final Inventory Value: $[amount]
Total Final Assets: $[sum]
==============================================================

Results saved to test_results.csv
```

---

## Architecture Overview

### System Components

```
1. ORCHESTRATOR AGENT (LLM-based)
   ├─ Receives: Customer quote requests
   ├─ Process: Routes to appropriate tools
   └─ Returns: Customer-friendly quote responses

2. TOOLS (6 Callable Functions)
   ├─ tool_check_item_availability() → Inventory checking
   ├─ tool_get_delivery_estimate() → Delivery calculation
   ├─ tool_calculate_quote() → Pricing with discounts
   ├─ tool_record_sale() → Transaction logging
   ├─ tool_get_current_cash_balance() → Financial tracking
   └─ tool_get_all_available_items() → Inventory discovery

3. DATABASE (SQLite)
   ├─ transactions table → All sales and stock orders
   ├─ quote_requests table → Customer requests
   ├─ quotes table → Historical quotes
   ├─ inventory table → Available items and pricing
   └─ (Implicitly) → Stock calculations via transactions

4. HELPER FUNCTIONS (From project_starter.py)
   ├─ create_inventory() → Seed inventory with 18 items
   ├─ setup_db() → Initialize database schema
   ├─ record_transaction() → Log transactions
   ├─ get_all_inventory() → Snapshot of available stock
   ├─ get_stock_level() → Individual item stock level
   ├─ get_supplier_delivery_date() → Lead time calculation
   ├─ get_cash_balance() → Calculate balance as of date
   └─ generate_financial_report() → Full financial snapshot
```

### Data Flow

```
Customer Request (CSV)
    ↓
ORCHESTRATOR (LLM reads request)
    ↓
    ├─→ tool_get_all_available_items() [Check inventory]
    ├─→ tool_check_item_availability() [Verify specific items]
    ├─→ tool_calculate_quote() [Generate price]
    ├─→ tool_get_delivery_estimate() [Estimate delivery]
    │
    ├─→ LLM Generates Response (with all details)
    │
    └─→ tool_record_sale() [If approved, log transaction]

Response sent to customer (captured in test_results.csv)
```

---

## Key Implementation Details

### 1. Tool Definitions

All tools are Python functions decorated with `@tool`:

```python
@tool
def tool_check_item_availability(item_name: str, requested_quantity: int, as_of_date: str) -> dict:
    """Check if item is available in sufficient quantity."""
    # Wraps get_stock_level() and handles availability logic
    # Returns: {available: bool, current_stock: int, message: str}
```

### 2. Orchestrator Agent

```python
class MultiAgentOrchestrator:
    def process_quote_request(self, request: dict) -> dict:
        """
        Process single quote request through the system.
        
        Args:
            request: {
                job: str (customer title),
                need_size: str (small/medium/large),
                event: str (event type),
                request_text: str (detailed request),
                request_date: str (YYYY-MM-DD),
                mood: str (customer sentiment)
            }
        
        Returns:
            {
                status: str (processed/error),
                response: str (customer-facing response),
                customer_response: str (approval status)
            }
        """
```

### 3. Bulk Discount Strategy

Applied in `tool_calculate_quote()`:

```
Quantity Range    Discount    Example
≤100 units       0%          1000 sheets @ $0.10 = $100
100-499 units    10%         200 sheets @ $0.10 = $18
500-999 units    15%         600 sheets @ $0.10 = $51
≥1000 units      20%         1500 sheets @ $0.10 = $120
```

### 4. Delivery Estimation

Implemented in `tool_get_delivery_estimate()`:

```
Order Size          Calculation             Example
≤10 units          0 days                  May 1 → May 1
11-100 units       +1 day                  May 1 → May 2
101-1000 units     +4 days                 May 1 → May 5
>1000 units        +7 days                 May 1 → May 8
```

### 5. Financial Tracking

Cash balance calculated from `get_cash_balance()`:

```
Cash Balance = Total Sales Revenue - Total Inventory Costs

Example:
    Starting Cash: $50,000
    First sale: +$500 (20 units @ $25)
    Second sale: +$1,200 (40 units @ $30)
    New Balance: $51,700
```

---

## Processing a Single Request

### Step 1: Request Loaded from CSV

```python
{
    "job": "Office Manager",
    "need_size": "large",
    "event": "quarterly_meeting",
    "request": "Need 500 sheets of premium paper for conference",
    "request_date": "2025-04-15",
    "mood": "stressed"
}
```

### Step 2: Orchestrator Receives Request

LLM receives system prompt explaining its role and access to tools.

### Step 3: Tool Invocations

1. **Get Available Items**
   ```
   tool_get_all_available_items(as_of_date="2025-04-15")
   Returns: {"A4 paper": 450, "Poster paper": 200, ...}
   ```

2. **Check Specific Item**
   ```
   tool_check_item_availability(
       item_name="A4 paper",
       requested_quantity=500,
       as_of_date="2025-04-15"
   )
   Returns: {"available": true, "current_stock": 450, "message": "..."}
   ```

3. **Calculate Quote**
   ```
   tool_calculate_quote(
       item_name="A4 paper",
       quantity=500,
       unit_price=0.05
   )
   Returns: {
       "final_price": 212.50,
       "discount_rate": 0.15,
       "discount_explanation": "15% bulk discount (500-999 units)",
       "savings": 37.50
   }
   ```

4. **Estimate Delivery**
   ```
   tool_get_delivery_estimate(
       requested_date="2025-04-15",
       quantity=500
   )
   Returns: {
       "estimated_delivery": "2025-04-19",
       "lead_time_days": 4,
       "feasible": true
   }
   ```

### Step 4: LLM Generates Response

LLM combines tool results into customer-friendly response:

```
"We can fulfill your order! Here are the details:

Item: A4 paper
Quantity: 500 sheets
Unit Price: $0.05/sheet
Base Price: $250.00

Bulk Discount: 15% (orders 500-999 units)
Discount Amount: -$37.50
Final Price: $212.50

Estimated Delivery: April 19, 2025 (4 days)

This is a great deal for your quarterly meeting!
We'll have this ready for you by your event."
```

### Step 5: Record Transaction (if Approved)

```python
tool_record_sale(
    item_name="A4 paper",
    quantity=500,
    total_price=212.50,
    transaction_date="2025-04-15"
)
Returns: {
    "success": true,
    "transaction_id": 42,
    "message": "Sale recorded: 500 units of A4 paper for $212.50"
}
```

### Step 6: Store Results

```python
result = {
    "request_id": 1,
    "job": "Office Manager",
    "event": "quarterly_meeting",
    "request_date": "2025-04-15",
    "status": "processed",
    "response": "[LLM response text]",
    "cash_balance": 50212.50,  # Updated after sale
    "inventory_value": [calculated]
}
```

---

## Output Files

### 1. test_results.csv

```csv
request_id,job,event,request_date,status,response,cash_balance,inventory_value
1,Office Manager,quarterly_meeting,2025-04-15,processed,"We can fulfill...",50212.50,47234.56
2,School Teacher,graduation_ceremony,2025-04-16,processed,"Great news...",50512.50,46934.56
3,Hotel Manager,conference,2025-04-17,error,"Sorry, we cannot...",50512.50,46934.56
...
```

### 2. AGENT_WORKFLOW_DIAGRAM.md

Comprehensive architecture documentation showing:
- All agents and responsibilities
- Tool associations
- Data flow diagrams
- Error handling paths
- Sensitive data handling

### 3. EVALUATION_REFLECTION_REPORT.md

Detailed report including:
- System architecture overview
- Implementation details
- Test results summary
- 5 improvement suggestions with implementation guidance
- Compliance with industry best practices
- Rubric requirements checklist

---

## Customization Guide

### Adjust Bulk Discount Tiers

Edit in `tool_calculate_quote()`:

```python
if quantity >= 1000:
    discount_rate = 0.25  # Change from 0.20 to 0.25
elif quantity >= 500:
    discount_rate = 0.18  # Change from 0.15 to 0.18
```

### Modify Delivery Estimates

Edit in `tool_get_delivery_estimate()` (via `get_supplier_delivery_date()`):

```python
if quantity <= 10:
    days = 0   # Same day
elif quantity <= 100:
    days = 2   # Changed from 1 to 2
elif quantity <= 1000:
    days = 3   # Changed from 4 to 3
else:
    days = 5   # Changed from 7 to 5
```

### Change Starting Cash

Edit in `init_database()`:

```python
# Initial sales transaction (starting cash)
initial_transactions.append({
    "item_name": None,
    "transaction_type": "sales",
    "units": None,
    "price": 75000.0,  # Change from 50000.0
    "transaction_date": initial_date,
})
```

### Adjust LLM Temperature

Edit in `MultiAgentOrchestrator.__init__()`:

```python
# Lower value (0.1-0.3) = More consistent, deterministic
# Higher value (0.7-1.0) = More creative, varied
response = client.chat.completions.create(
    ...
    temperature=0.3,  # Change from 0.7 for more consistency
)
```

---

## Troubleshooting

### "UDACITY_OPENAI_API_KEY not set"

**Solution**: Update `.env` file with your API key
```
UDACITY_OPENAI_API_KEY=voc-xxxx...
```

### "ModuleNotFoundError: No module named 'smolagents'"

**Solution**: Install package
```bash
pip install smolagents
```

### "Database locked" error

**Solution**: Delete `munder_difflin.db` and rerun (it will be recreated)
```bash
rm munder_difflin.db
python project_starter.py
```

### Slow processing

**Solution**: This is normal for 401 requests. Each request requires:
- API call to OpenAI (~1-2 seconds)
- Database queries (~0.1 seconds)
- Tool invocations (~0.5 seconds)
- Total: ~3-5 seconds per request = 20-33 minutes for all 401

---

## Next Steps After Implementation

1. **Review Test Results**
   - Check `test_results.csv` for successful quotes
   - Verify cash balance changes
   - Identify unfulfilled request patterns

2. **Implement Improvements**
   - See [EVALUATION_REFLECTION_REPORT.md] for detailed suggestions
   - Start with "Dynamic Pricing Strategy"
   - Then "Inventory Forecasting"

3. **Add More Tools**
   - Implement auto-reordering based on stock levels
   - Add competitor pricing lookup
   - Create customer preference learning

4. **Scale the System**
   - Move to production database (PostgreSQL)
   - Add multi-threading for parallel request processing
   - Implement caching for repeated inventory queries

---

## Code Structure

```
project_starter.py
├─ Helper Functions (from project base)
│  ├─ generate_sample_inventory()
│  ├─ init_database()
│  ├─ create_transaction()
│  ├─ get_all_inventory()
│  ├─ get_stock_level()
│  ├─ get_supplier_delivery_date()
│  ├─ get_cash_balance()
│  └─ generate_financial_report()
│
├─ Multi-Agent System (NEW)
│  ├─ Tool Definitions
│  │  ├─ tool_check_item_availability()
│  │  ├─ tool_get_delivery_estimate()
│  │  ├─ tool_calculate_quote()
│  │  ├─ tool_record_sale()
│  │  ├─ tool_get_current_cash_balance()
│  │  └─ tool_get_all_available_items()
│  │
│  ├─ Orchestrator Agent
│  │  └─ MultiAgentOrchestrator class
│  │     └─ process_quote_request()
│  │
│  ├─ System Initialization
│  │  └─ initialize_multi_agent_system()
│  │
│  └─ Test Runner
│     └─ run_test_scenarios()
│
├─ Main Entry Point
│  └─ if __name__ == "__main__"
│
├─ CSV Input Files
│  ├─ quote_requests_sample.csv
│  ├─ quote_requests.csv (401 requests)
│  └─ quotes.csv
│
├─ Configuration Files
│  ├─ .env (API key)
│  ├─ requirements.txt
│  └─ README.md
│
└─ Output Files (Generated)
   ├─ munder_difflin.db (SQLite database)
   ├─ test_results.csv (results from 401 requests)
   ├─ AGENT_WORKFLOW_DIAGRAM.md (architecture)
   └─ EVALUATION_REFLECTION_REPORT.md (evaluation)
```

---

## Learning Outcomes

By implementing this system, you'll have learned:

1. **Multi-Agent Architecture**
   - Orchestrator pattern
   - Tool-based agent design
   - LLM-driven decision making

2. **Python Best Practices**
   - Modular tool design
   - Error handling
   - Database operations
   - API integration

3. **Business Logic**
   - Bulk discount strategies
   - Inventory management
   - Financial tracking
   - Customer communication

4. **Software Engineering**
   - System design
   - Testing and validation
   - Documentation
   - Performance optimization

---

For questions or issues, refer to the included documentation files:
- [AGENT_WORKFLOW_DIAGRAM.md] - Architecture details
- [EVALUATION_REFLECTION_REPORT.md] - Evaluation and improvements
- [README.md] - Original project requirements
