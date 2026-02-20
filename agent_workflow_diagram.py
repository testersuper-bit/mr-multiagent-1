#!/usr/bin/env python3
"""
Munder Difflin Multi-Agent System Workflow Diagram
Visualizes the distinct worker agents and their interactions using NetworkX and Matplotlib
Based on the architecture pattern demonstrated in demo_image.py
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

def create_agent_workflow_diagram():
    """
    Create a visual representation of the multi-agent system workflow.
    Shows distinct agents (nodes) and their tool interactions (edges).
    """
    
    # Create figure and axis
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    fig.suptitle('Munder Difflin Multi-Agent Quote Processing System', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    # Create directed graph
    G = nx.DiGraph()
    
    # Define node positions using a hierarchical layout
    pos = {
        # Top level: User/Request input
        'user': (8, 10),

        # Second level: Orchestrator
        'orchestrator': (8, 8),

        # Third level: Worker agents
        'inventory_agent': (2, 5),
        'quote_agent': (8, 5),
        'sales_agent': (14, 5),

        # Fourth level: Tools (use exact tool_* names from project_starter.py)
        'tool_check_item_availability': (0.5, 2.5),
        'tool_get_all_available_items': (3, 2.5),
        'tool_get_delivery_estimate': (6, 2.5),
        'tool_calculate_quote': (9, 2.5),
        'tool_record_sale': (12, 2.5),
        'tool_record_stock_order': (14.5, 2.5),
        'tool_get_current_cash_balance': (16, 2.5),

        # Fifth level: Database
        'database': (8, 0.5),
    }
    
    # Add nodes with different types
    user_nodes = ['user']
    orchestrator_nodes = ['orchestrator']
    agent_nodes = ['inventory_agent', 'quote_agent', 'sales_agent']
    tool_nodes = [
        'tool_check_item_availability',
        'tool_get_all_available_items',
        'tool_get_delivery_estimate',
        'tool_calculate_quote',
        'tool_record_sale',
        'tool_record_stock_order',
        'tool_get_current_cash_balance',
    ]
    database_nodes = ['database']
    
    # Add nodes to graph
    for node in user_nodes + orchestrator_nodes + agent_nodes + tool_nodes + database_nodes:
        G.add_node(node)
    
    # Add edges showing workflow
    # User to Orchestrator
    G.add_edge('user', 'orchestrator')
    
    # Orchestrator to Worker Agents
    G.add_edge('orchestrator', 'inventory_agent')
    G.add_edge('orchestrator', 'quote_agent')
    G.add_edge('orchestrator', 'sales_agent')
    
    # Worker Agents to Tools
    G.add_edge('inventory_agent', 'tool_check_item_availability')
    G.add_edge('inventory_agent', 'tool_get_all_available_items')

    G.add_edge('quote_agent', 'tool_get_delivery_estimate')
    G.add_edge('quote_agent', 'tool_calculate_quote')

    G.add_edge('sales_agent', 'tool_record_sale')
    G.add_edge('sales_agent', 'tool_record_stock_order')
    G.add_edge('sales_agent', 'tool_get_current_cash_balance')
    
    # Tools to Database
    G.add_edge('tool_check_item_availability', 'database')
    G.add_edge('tool_get_all_available_items', 'database')
    G.add_edge('tool_get_delivery_estimate', 'database')
    G.add_edge('tool_calculate_quote', 'database')
    G.add_edge('tool_record_sale', 'database')
    G.add_edge('tool_record_stock_order', 'database')
    G.add_edge('tool_get_current_cash_balance', 'database')
    
    # Database back to Sales Agent (confirmation)
    G.add_edge('database', 'sales_agent')
    
    # Define colors for different node types
    node_colors = {}
    for node in user_nodes:
        node_colors[node] = '#FF6B6B'  # Red for user input
    for node in orchestrator_nodes:
        node_colors[node] = '#4ECDC4'  # Teal for orchestrator
    for node in agent_nodes:
        node_colors[node] = '#45B7D1'  # Blue for worker agents
    for node in tool_nodes:
        node_colors[node] = '#FFA07A'  # Light salmon for tools
    for node in database_nodes:
        node_colors[node] = '#95E1D3'  # Mint for database
    
    # Define node shapes and sizes
    node_size_map = {
        'user': 3000,
        'orchestrator': 4000,
        'inventory_agent': 3500,
        'quote_agent': 3500,
        'sales_agent': 3500,
        'tool_check_item_availability': 2200,
        'tool_get_all_available_items': 2200,
        'tool_get_delivery_estimate': 2200,
        'tool_calculate_quote': 2200,
        'tool_record_sale': 2200,
        'tool_record_stock_order': 2200,
        'tool_get_current_cash_balance': 2200,
        'database': 3000,
    }
    
    # Get colors in order for visualization
    colors = [node_colors[node] for node in G.nodes()]
    sizes = [node_size_map[node] for node in G.nodes()]
    
    # Draw nodes with different shapes
    nx.draw_networkx_nodes(G, pos, 
                          nodelist=user_nodes,
                          node_color=[node_colors[n] for n in user_nodes],
                          node_size=[node_size_map[n] for n in user_nodes],
                          node_shape='s',
                          ax=ax, label='Customer Request')
    
    nx.draw_networkx_nodes(G, pos,
                          nodelist=orchestrator_nodes,
                          node_color=[node_colors[n] for n in orchestrator_nodes],
                          node_size=[node_size_map[n] for n in orchestrator_nodes],
                          node_shape='o',
                          ax=ax, label='Orchestrator')
    
    nx.draw_networkx_nodes(G, pos,
                          nodelist=agent_nodes,
                          node_color=[node_colors[n] for n in agent_nodes],
                          node_size=[node_size_map[n] for n in agent_nodes],
                          node_shape='o',
                          ax=ax, label='Worker Agents')
    
    nx.draw_networkx_nodes(G, pos,
                          nodelist=tool_nodes,
                          node_color=[node_colors[n] for n in tool_nodes],
                          node_size=[node_size_map[n] for n in tool_nodes],
                          node_shape='^',
                          ax=ax, label='Tools')
    
    nx.draw_networkx_nodes(G, pos,
                          nodelist=database_nodes,
                          node_color=[node_colors[n] for n in database_nodes],
                          node_size=[node_size_map[n] for n in database_nodes],
                          node_shape='D',
                          ax=ax, label='Database')
    
    # Draw edges with arrows
    nx.draw_networkx_edges(G, pos, 
                          edge_color='#666666',
                          arrows=True,
                          arrowsize=20,
                          arrowstyle='->',
                          width=2,
                          connectionstyle='arc3,rad=0.1',
                          ax=ax)
    
    # Draw labels with better positioning
    labels = {
        'user': 'Customer\nRequest',
        'orchestrator': 'Orchestrator\nAgent',
        'inventory_agent': 'Inventory\nManager\nAgent',
        'quote_agent': 'Quote\nGenerator\nAgent',
        'sales_agent': 'Sales\nFinalization\nAgent',
        'tool_check_item_availability': 'tool_check_item_availability\n(Check Availability)',
        'tool_get_all_available_items': 'tool_get_all_available_items\n(Get All Items)',
        'tool_get_delivery_estimate': 'tool_get_delivery_estimate\n(Get Delivery Estimate)',
        'tool_calculate_quote': 'tool_calculate_quote\n(Calculate Quote)',
        'tool_record_sale': 'tool_record_sale\n(Record Sale)',
        'tool_record_stock_order': 'tool_record_stock_order\n(Record Stock Order)',
        'tool_get_current_cash_balance': 'tool_get_current_cash_balance\n(Get Cash Balance)',
        'database': 'SQLite\nDatabase',
    }
    
    nx.draw_networkx_labels(G, pos, labels, 
                           font_size=9,
                           font_weight='bold',
                           ax=ax)
    
    # Add legend with descriptions
    legend_elements = [
        mpatches.Patch(color='#FF6B6B', label='Customer Request'),
        mpatches.Patch(color='#4ECDC4', label='Orchestrator (Coordinator)'),
        mpatches.Patch(color='#45B7D1', label='Worker Agents'),
        mpatches.Patch(color='#FFA07A', label='Tools/Functions'),
        mpatches.Patch(color='#95E1D3', label='Database'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=11, title='Component Types', title_fontsize=12)
    
    # Add workflow description
    workflow_text = """
WORKFLOW PROCESS:
1. Customer submits quote request
2. Orchestrator Agent receives and routes request
3. Inventory Manager Agent checks stock availability
4. Quote Generator Agent calculates pricing with bulk discounts
5. Sales Finalization Agent processes order and records transaction
6. All agents access shared SQLite database for persistent storage
"""
    
    ax.text(0.5, -0.15, workflow_text, 
           transform=ax.transAxes,
           fontsize=10,
           verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
           family='monospace')

    # Add a tool -> helper mapping legend box for clarity
    tool_mapping = (
        "Tool -> Helper mapping:\n"
        "- tool_check_item_availability -> get_stock_level(...)\n"
        "- tool_get_all_available_items -> get_all_inventory(...)\n"
        "- tool_get_delivery_estimate -> get_supplier_delivery_date(...)\n"
        "- tool_calculate_quote -> inventory unit_price + discount logic\n"
        "- tool_record_sale -> create_transaction(..., transaction_type='sales')\n"
        "- tool_record_stock_order -> create_transaction(..., transaction_type='stock_orders')\n"
        "- tool_get_current_cash_balance -> get_cash_balance(...)\n"
    )
    ax.text(0.02, 0.02, tool_mapping, transform=ax.transAxes, fontsize=8, family='monospace', bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.7))
    
    # Remove axes
    ax.axis('off')
    ax.set_xlim(-1, 17)
    ax.set_ylim(-2, 11)
    
    # Save figure
    output_path = os.path.join(os.path.dirname(__file__), 'munder_difflin_multiagent_workflow.png')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Diagram saved to: {output_path}")
    
    return fig, ax


def create_agent_responsibilities_diagram():
    """
    Create a detailed diagram showing agent responsibilities and data flow.
    """
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    fig.suptitle('Agent Responsibilities and Data Flow', fontsize=16, fontweight='bold')
    
    # Define agent boxes with responsibilities
    agents_info = {
        'Inventory Manager Agent': {
            'pos': (2, 7),
            'color': '#45B7D1',
            'responsibilities': [
                '• Check stock levels',
                '• Assess availability',
                '• Evaluate reorder needs'
            ]
        },
        'Quote Generator Agent': {
            'pos': (8, 7),
            'color': '#45B7D1',
            'responsibilities': [
                '• Calculate pricing',
                '• Apply bulk discounts',
                '• Estimate delivery dates'
            ]
        },
        'Sales Finalization Agent': {
            'pos': (14, 7),
            'color': '#45B7D1',
            'responsibilities': [
                '• Process orders',
                '• Record transactions',
                '• Update financial state'
            ]
        },
        'Orchestrator Agent': {
            'pos': (8, 3.5),
            'color': '#4ECDC4',
            'responsibilities': [
                '• Route requests to agents',
                '• Aggregate responses',
                '• Manage workflow'
            ]
        }
    }
    
    # Draw agent boxes
    for agent_name, info in agents_info.items():
        x, y = info['pos']
        
        # Draw box
        box = FancyBboxPatch((x-1.8, y-0.8), 3.6, 1.6,
                            boxstyle="round,pad=0.1",
                            edgecolor='black',
                            facecolor=info['color'],
                            linewidth=2,
                            alpha=0.7)
        ax.add_patch(box)
        
        # Add agent name
        ax.text(x, y+0.5, agent_name, 
               ha='center', va='center',
               fontsize=11, fontweight='bold')
        
        # Add responsibilities
        resp_text = '\n'.join(info['responsibilities'])
        ax.text(x, y-0.1, resp_text,
               ha='center', va='center',
               fontsize=8, family='monospace')
    
    # Draw arrows showing coordination
    arrow_props = dict(arrowstyle='->', lw=2, color='#333333')
    
    # Orchestrator to each agent
    ax.annotate('', xy=(2, 6.1), xytext=(7, 4.3),
                arrowprops=arrow_props)
    ax.annotate('', xy=(8, 6.1), xytext=(8, 4.3),
                arrowprops=arrow_props)
    ax.annotate('', xy=(14, 6.1), xytext=(9, 4.3),
                arrowprops=arrow_props)
    
    # Add data sharing layer
    ax.text(8, 2.5, 'Shared SQLite Database', 
           ha='center', va='center',
           fontsize=12, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='#95E1D3', alpha=0.7))
    
    # Database connections
    db_arrow_props = dict(arrowstyle='<->', lw=1.5, color='#666666', linestyle='dashed')
    
    ax.annotate('', xy=(2, 1.5), xytext=(2, 6.1),
                arrowprops=db_arrow_props)
    ax.annotate('', xy=(8, 1.5), xytext=(8, 6.1),
                arrowprops=db_arrow_props)
    ax.annotate('', xy=(14, 1.5), xytext=(14, 6.1),
                arrowprops=db_arrow_props)
    
    # Key features text
    features = """
KEY FEATURES OF MULTI-AGENT SYSTEM:

✓ Separation of Concerns: Each agent handles specific domain tasks
✓ Modularity: Agents can be updated/tested independently
✓ Scalability: Easy to add new agents or tools
✓ Parallel Processing: Agents can work concurrently
✓ Coordination: Orchestrator ensures proper workflow
✓ Data Persistence: Shared database maintains state
"""
    
    ax.text(8, -1.5, features,
           ha='center', va='top',
           fontsize=9, family='monospace',
           bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
    
    ax.set_xlim(0, 16)
    ax.set_ylim(-3.5, 9)
    ax.axis('off')
    
    # Save figure
    output_path = os.path.join(os.path.dirname(__file__), 'agent_responsibilities_diagram.png')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Agent responsibilities diagram saved to: {output_path}")
    
    return fig, ax


if __name__ == "__main__":
    print("Generating multi-agent system diagrams...")
    print("=" * 60)
    
    # Create workflow diagram
    create_agent_workflow_diagram()
    
    # Create responsibilities diagram  
    create_agent_responsibilities_diagram()
    
    print("=" * 60)
    print("✓ All diagrams generated successfully!")
    print("\nGenerated files:")
    print("  - munder_difflin_multiagent_workflow.png")
    print("  - agent_responsibilities_diagram.png")
