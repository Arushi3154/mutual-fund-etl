import pandas as pd
import glob
import os

def inspect_csvs(raw_data_path="data/raw"):
    csv_files = glob.glob(f"{raw_data_path}/*.csv")
    print(f"\nFound {len(csv_files)} CSV files.\n")
    
    for file in csv_files:
        filename = os.path.basename(file)
        print(f"--- Inspecting: {filename} ---")
        try:
            df = pd.read_csv(file)
            print(f"Shape: {df.shape}")
            print(f"Data Types:\n{df.dtypes.to_dict()}")
            print(f"Head:\n{df.head(2)}\n")
        except Exception as e:
            print(f"Error reading {filename}: {e}\n")

def explore_and_validate():
    fund_master_path = "data/raw/fund_master.csv"
    nav_history_path = "data/raw/nav_history.csv"
    
    if os.path.exists(fund_master_path) and os.path.exists(nav_history_path):
        fund_master = pd.read_csv(fund_master_path)
        nav_history = pd.read_csv(nav_history_path)
        
        print("\n--- Fund Master Exploration ---")
        if 'fund_house' in fund_master.columns:
            print("Unique Fund Houses:", fund_master['fund_house'].nunique())
        if 'category' in fund_master.columns:
            print("Categories:", fund_master['category'].unique())
        
        print("\n--- AMFI Code Validation ---")
        master_codes = set(fund_master['amfi_code'].unique())
        history_codes = set(nav_history['amfi_code'].unique())
        
        missing_in_history = master_codes - history_codes
        
        print("Data Quality Summary:")
        print(f"Total codes in master: {len(master_codes)}")
        print(f"Total codes in history: {len(history_codes)}")
        
        if len(missing_in_history) == 0:
            print("Validation Passed: Every AMFI code in fund_master exists in nav_history.")
        else:
            print(f"Validation Warning: {len(missing_in_history)} codes in fund_master have no history data.")
    else:
        print("\nSkipping validation: Ensure fund_master.csv and nav_history.csv are in data/raw/")

if __name__ == "__main__":
    inspect_csvs()
    explore_and_validate()