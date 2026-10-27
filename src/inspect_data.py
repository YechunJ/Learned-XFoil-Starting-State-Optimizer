import json
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
data_path = (
    project_root
    / "data"
    / "raw"
    / "aero_audit"
    / "cold_warm_results.json"
)

with data_path.open() as file:
    runs = json.load(file)

print(type(runs))
print(len(runs))
print(runs[0].keys())