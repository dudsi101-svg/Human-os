
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

print("\nSELF MODEL EXAMPLE (conversational 'About Me')")
from hos_engine import InteractionMode, MessageAuthor, SelfModelService

svc = SelfModelService()
chat = svc.interactions.start(subject_id="HOS-HUM-000001", mode=InteractionMode.NATURAL)
m1 = svc.interactions.append(chat.interaction_id, author=MessageAuthor.USER,
                             text="Cenię wolność i nie lubię, kiedy ktoś organizuje mi życie.")
m2 = svc.interactions.append(chat.interaction_id, author=MessageAuthor.USER,
                             text="Sam ustalam sobie rytm pracy.")
hyp = svc.hypothesize(subject_id="HOS-HUM-000001", domain="values", key="dominant_value",
                      value="autonomia", confidence=0.72,
                      supported_by=[m1.message_id, m2.message_id])
print("Hypothesis (before confirmation):",
      json.dumps({k: v for k, v in svc.why(hyp.record_id).items()
                  if k in ("statement", "evidence_type", "confidence_band", "created_by")},
                 ensure_ascii=False, indent=2))
m3 = svc.interactions.append(chat.interaction_id, author=MessageAuthor.USER, text="Tak, zgadza sie.")
confirmed = svc.confirm(hyp.record_id, subject_id="HOS-HUM-000001", message_id=m3.message_id)
view = svc.living_view("HOS-HUM-000001")
print("Living view counts:", {k: len(v) for k, v in view.items()})

from hos_engine import SQLiteSelfModelStore

store = SQLiteSelfModelStore("data/self_model.db")
store.save_snapshot(svc)
reloaded = store.load_service()
print("Survives restart:",
      reloaded.why(confirmed.record_id)["sources"][0]["quote"] is not None,
      "| counts:", store.counts())
store.close()

print("\nRECOVERY EXAMPLE (SAFE MODE + refusal audit)")
from datetime import UTC, datetime, timedelta

from hos_engine import AuthorityRole, EmergencyMode, RecoveryRefused, SovereignRecoveryKernel

kernel = SovereignRecoveryKernel()
expiry = (datetime.now(UTC) + timedelta(hours=1)).isoformat()
kernel.activate(mode=EmergencyMode.SAFE_MODE, initiator_id="HOS-HUM-000001",
                initiator_role=AuthorityRole.OWNER, scope="system",
                reason="demo: suspected compromise", expires_at=expiry,
                verification_method="recovery-key")
print("SAFE MODE active (scope=system):",
      kernel.is_active(EmergencyMode.SAFE_MODE, scope="system"))
try:
    kernel.activate(mode=EmergencyMode.SAFE_MODE, initiator_id="HOS-AGT-000001",
                    initiator_role=AuthorityRole.AGENT, scope="system",
                    reason="agent tries to toggle protection", expires_at=expiry,
                    verification_method="none")
except RecoveryRefused as refused:
    print("Agent activation refused (and logged):", refused)
print("Audit results:", [e.result for e in kernel.events()])
