import json
from pathlib import Path

# File paths
scrip_master_path = Path(r"C:\Users\Nitish\Desktop\volume_scanner\OpenAPIScripMaster.json")
verified_path = Path(r"C:\Users\Nitish\Desktop\volume_scanner\verified_nse_eq.json")

# Load OpenAPIScripMaster.json
with scrip_master_path.open("r", encoding="utf-8") as f:
    scrip_master = json.load(f)

# Load verified_nse_eq.json
with verified_path.open("r", encoding="utf-8") as f:
    verified = json.load(f)

# Create a dict of existing symbols for quick lookup
existing = {entry["symbol"]: entry["token"] for entry in verified}

# Find new EQ symbols
new_entries = []
for entry in scrip_master:
    symbol = entry.get("symbol", "")
    token = entry.get("token", "")
    if symbol.endswith("-EQ") and symbol not in existing and token:
        new_entries.append({"symbol": symbol, "token": token})
        existing[symbol] = token  # update tracker

# Append new entries
final_list = verified + new_entries

# Save updated JSON file
with verified_path.open("w", encoding="utf-8") as f:
    json.dump(final_list, f, indent=4)

print(f"✅ Added {len(new_entries)} new -EQ stocks to verified_nse_eq.json")
