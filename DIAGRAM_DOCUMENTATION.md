# Munder Difflin Multi-Agent Workflow Diagram

## Visual Representation

The agent workflow has been recreated as a professional network diagram visualization in **matplotlib/networkx** format.

**File**: `munder_difflin_multiagent_workflow.png` (593 KB, high-resolution 300 DPI)

---

## Diagram Components

### Color Coding

| Color | Node Type | Count | Purpose |
|-------|-----------|-------|---------|
| **Blue (Circle)** | Orchestrator Agent | 1 | Central coordinator that routes requests |
| **Gold (Square)** | Tools/Resources | 6 | Specialized functions for business logic |
| **Green (Diamond)** | Database | 1 | SQLite data persistence layer |
| **Red (Diamond)** | Customer Interface | 2 | Input/Output endpoints |

### Node Types

#### 1. **Customer Request** (Red Diamond - Input)
- Entry point for all quote requests
- Contains: job title, event type, need size, request details, date
- Flows to: Orchestrator Agent

#### 2. **Orchestrator Agent** (Blue Circle - Central)
- Main coordinator and decision maker
- Routes requests to appropriate tools
- Aggregates tool responses
- Generates customer-facing responses
- Flows to/from: All tools

#### 3. **Six Specialized Tools** (Gold Squares)

1. **Inventory Checker Tool**
   - Verifies item availability
   - Checks stock levels as of request date
   - Returns: availability status and current stock

2. **Quote Calculator Tool**
   - Applies bulk discount logic
   - Calculates final price
   - Returns: quote with discount explanation

3. **Delivery Estimator Tool**
   - Estimates lead time based on quantity
   - Calculates delivery date
   - Returns: feasibility and estimated delivery date

4. **Sales Recorder Tool**
   - Records confirmed sales transactions
   - Updates inventory and financial records
   - Returns: transaction ID and confirmation

5. **Finance Monitor Tool**
   - Tracks cash balance
   - Calculates financial metrics
   - Returns: current balance and financial status

6. **Inventory Discovery Tool**
   - Retrieves all available items
   - Provides inventory options to customer
   - Returns: list of in-stock items

#### 4. **SQLite Database** (Green Diamond - Storage)
- Persistence layer for all data
- Tables: transactions, quotes, quote_requests, inventory
- Bidirectional communication with all tools
- Maintains financial history and state

#### 5. **Customer Response** (Red Diamond - Output)
- Final response sent to customer
- Contains: quote details, delivery date, price breakdown
- Success response includes: transaction ID and confirmation
- Failure response includes: reason and alternatives

---

## Data Flow

### Request Processing Flow

```
┌─────────────────┐
│Customer Request │
└────────┬────────┘
         │
         ▼
┌──────────────────────────┐
│ Orchestrator Agent       │ ◄─── Receives request
│ (Coordinator)            │     (job, event, date, etc.)
└──────────────────────────┘
         │
         │ Routes to tools
         │
    ┌────┴─────────────────────────────────────┐
    │          ┌──────────┐                     │
    │          │ Inventory│                     │
    ▼          │Checker   │                     ▼
┌─────────────┐└─────┬────┘              ┌───────────────┐
│ Inventory   │◄─────┘                   │ Quote         │
│ Discovery   │◄──────────────────┬──────│ Calculator    │
│ Tool        │                   │      └───────────────┘
└──────┬──────┘                   │            │
       │                          │            │
       ▼ (queries)                ▼            ▼
   ┌─────────────────────────────────────────────────┐
   │        SQLite Database                          │
   │ ┌─────────────┬─────────────┬─────────────┐    │
   │ │transactions │ quotes      │ inventory   │    │
   │ └─────────────┴─────────────┴─────────────┘    │
   └─────────────────────────────────────────────────┘
       ▲                   ▲                   ▲
       │                   │                   │
       └───┬───────────────┼──────────┬────────┘
           │               │          │
         (reads)        (updates)  (records)
           │               │          │
    ┌──────┴──┐      ┌─────┴──────┐ ┌┴──────────┐
    │Delivery │      │ Sales      │ │ Finance   │
    │Estimator│      │ Recorder   │ │ Monitor   │
    └──────┬──┘      └─────┬──────┘ └┴──────────┘
           │               │          │
           └───────────────┼──────────┘
                           │
                    ┌──────┴────────┐
                    │ Orchestrator  │
                    │ Aggregates    │
                    │ Results       │
                    └──────┬────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │Customer Response │
                  │ (Quote + Details)│
                  └──────────────────┘
```

---

## Key Relationships

### Orchestrator Agent Responsibilities

1. **Request Reception**: Receives customer quote request with all details
2. **Tool Orchestration**: Calls tools in optimal sequence
3. **Result Aggregation**: Combines tool outputs into coherent response
4. **Decision Making**: Determines if request can be fulfilled
5. **Response Generation**: Creates customer-friendly output

### Tool Relationships

**Sequential Flow** (typical request):
```
1. Inventory Discovery Tool
   ↓ (Get all available items)
2. Inventory Checker Tool
   ↓ (Verify specific items available)
3. Quote Calculator Tool
   ↓ (Calculate pricing with discounts)
4. Delivery Estimator Tool
   ↓ (Estimate delivery feasibility)
5. Sales Recorder Tool (optional)
   ↓ (Record if approved)
6. Finance Monitor Tool
   ↓ (Confirm financial update)
```

### Database Interactions

Each tool performs three operations:
1. **Read**: Query current state from database
2. **Process**: Apply business logic
3. **Write**: Update database with results

Example for Sales Recorder:
- **Read**: Current inventory and cash balance
- **Process**: Create transaction record
- **Write**: Update transactions table and financial state

---

## Edge Connections

### Bidirectional Edges (Data Exchange)

| Connection | Purpose |
|-----------|---------|
| Orchestrator ↔ Tools | Request routing and result aggregation |
| Tools ↔ Database | Data query and update operations |
| Orchestrator ↔ Database | Occasional direct queries for state |

### Request Flow Edges

| Source → Destination | Data Passed |
|-------------------|------------|
| Customer Request → Orchestrator | Full request details |
| Orchestrator → Tools | Specific query/action parameters |
| Tools → Database | Read/write operations |
| Database → Tools | Data results or confirmation |
| Tools → Orchestrator | Tool results and computed values |
| Orchestrator → Customer Response | Formatted response with quote |

---

## Diagram Legend

### Node Shapes
- **Circle (●)**: Agent - Autonomous decision-making component
- **Square (■)**: Tool - Specific function or resource
- **Diamond (◊)**: Data/Interface - Storage or I/O endpoint

### Node Colors
- **Blue**: Agent (orchestrator)
- **Gold**: Tools (business logic)
- **Green**: Database (persistence)
- **Red**: Interface (customer touchpoint)

### Edge Meanings
- **Solid lines**: Direct data flow
- **Arrow direction**: Information flow direction
- **Line thickness**: Relative importance/frequency

---

## System Characteristics Shown

### Separation of Concerns
Each tool handles a single responsibility:
- Inventory management
- Quote calculation
- Delivery estimation
- Transaction recording
- Financial tracking
- Item discovery

### Modularity
- Tools can be updated independently
- Database acts as central state
- Orchestrator manages coordination

### Scalability
- New tools can be added without modifying existing ones
- Database stores all historical data
- Requests flow through standardized pipeline

### Data Consistency
- All tools read from same database
- Updates are transactional
- Financial state accurately tracked

---

## Generated Files

**Primary Diagram**:
- `munder_difflin_multiagent_workflow.png` (300 DPI, high-resolution)

**Diagram Code**:
- `agent_workflow_diagram.py` (Python script using matplotlib/networkx)

**Can Regenerate**:
```bash
python agent_workflow_diagram.py
```

---

## Visual Reading Guide

**For Beginners**:
1. Start at top with "Customer Request" (red)
2. Follow down to "Orchestrator Agent" (blue)
3. See all tools (gold squares) it can call
4. See database (green) at bottom storing everything
5. Follow back up to "Customer Response" (red)

**For Technical Review**:
1. Examine each tool's database connections (bidirectional)
2. Note orchestrator's central role
3. Understand parallel vs. sequential tool calls
4. See how all data flows through database

**For Business Review**:
1. Customer request enters system (top)
2. System processes through multiple checks
3. Database maintains consistent state
4. Customer receives response (bottom)
5. All financial records persisted

---

## Integration with Documentation

This visual diagram complements:
- **AGENT_WORKFLOW_DIAGRAM.md** - Text-based detailed explanation
- **IMPLEMENTATION_GUIDE.md** - How to customize and extend
- **EVALUATION_REFLECTION_REPORT.md** - Architecture evaluation
- **project_starter.py** - Actual code implementation

Together, they provide complete documentation of the system from visual, textual, and code perspectives.

---

## Summary

The Munder Difflin Multi-Agent Quote Processing System is visualized as:
- **1 Orchestrator** coordinating all operations
- **6 Specialized Tools** handling specific business functions
- **1 Shared Database** maintaining all state
- **Bidirectional Communication** ensuring consistency
- **Clear Data Flow** from customer request to response

This architecture ensures modularity, scalability, and maintainability while accurately modeling real-world business processes.
