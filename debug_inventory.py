import pandas as pd
from sqlalchemy import create_engine

db_engine = create_engine("sqlite:///munder_difflin.db")

# Check what inventory exists
try:
    df = pd.read_sql("SELECT * FROM inventory LIMIT 5", db_engine)
    print("Inventory table (first 5):")
    print(df)
    print(f"\nTotal items in inventory: {len(pd.read_sql('SELECT * FROM inventory', db_engine))}")
    
    # Check A4 paper specifically
    a4_df = pd.read_sql("SELECT * FROM inventory WHERE item_name = 'A4 paper'", db_engine)
    print(f"\nA4 paper in inventory:")
    print(a4_df)
except Exception as e:
    print(f"Error: {e}")
