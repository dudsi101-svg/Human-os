
import json

from hos_engine import HumanOSEngine

engine = HumanOSEngine(event_store_path="data/events.jsonl")

with open("examples/action.approved.example.json", encoding="utf-8") as f:
    approved = json.load(f)

with open("examples/action.blocked.example.json", encoding="utf-8") as f:
    blocked = json.load(f)

print("APPROVED EXAMPLE")
print(json.dumps(engine.evaluate_action(approved, "HOS-HUM-000001"), ensure_ascii=False, indent=2))

print("\nBLOCKED EXAMPLE")
print(json.dumps(engine.evaluate_action(blocked, "HOS-HUM-000001"), ensure_ascii=False, indent=2))
