import requests
import pandas as pd
import os

def fetch_and_save_nav(scheme_name, amfi_code):
    url = f"https://api.mfapi.in/mf/{amfi_code}"
    print(f"Fetching data for {scheme_name} ({amfi_code})...")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        json_data = response.json()
        if "data" in json_data and len(json_data["data"]) > 0:
            df = pd.DataFrame(json_data["data"])
            df["amfi_code"] = amfi_code
            output_path = f"data/raw/nav_{scheme_name.lower()}.csv"
            df.to_csv(output_path, index=False)
            print(f"Saved {len(df)} records to {output_path}")
        else:
            print(f"No NAV data found for {scheme_name}.")
    else:
        print(f"Failed to fetch {scheme_name}. Status code: {response.status_code}")

if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)
    
    schemes = {
        "HDFC_Top_100": "125497",
        "SBI_Bluechip": "119551",
        "ICICI_Bluechip": "120503",
        "Nippon_Large_Cap": "118632",
        "Axis_Bluechip": "119092",
        "Kotak_Bluechip": "120841"
    }
    
    for name, code in schemes.items():
        fetch_and_save_nav(name, code)