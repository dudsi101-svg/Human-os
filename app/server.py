from __future__ import annotations

import json
from pathlib import Path

from flask import Flask, render_template, request

from hos_engine import HumanOSEngine

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples"
DEFAULT_ACTOR_ID = "HOS-HUM-000001"

EXAMPLES = {
    "approved": EXAMPLES_DIR / "action.approved.example.json",
    "blocked": EXAMPLES_DIR / "action.blocked.example.json",
}


def _load_example(name: str) -> str:
    path = EXAMPLES.get(name, EXAMPLES["approved"])
    return path.read_text(encoding="utf-8")


def create_app() -> Flask:
    app = Flask(__name__)
    engine = HumanOSEngine(event_store_path=str(REPO_ROOT / "data" / "events.jsonl"))

    @app.get("/")
    def index():
        example = request.args.get("example", "approved")
        action_json = _load_example(example)
        return render_template(
            "index.html",
            action_json=action_json,
            actor_id=DEFAULT_ACTOR_ID,
            result=None,
            error=None,
        )

    @app.post("/evaluate")
    def evaluate():
        action_json = request.form.get("action_json", "")
        actor_id = request.form.get("actor_id", "").strip() or DEFAULT_ACTOR_ID
        error = None
        result = None

        try:
            action = json.loads(action_json)
        except json.JSONDecodeError as exc:
            error = f"Invalid JSON: {exc.msg} (line {exc.lineno}, column {exc.colno})"
        else:
            if not isinstance(action, dict):
                error = "The action must be a JSON object, not a list or scalar value."
            else:
                result = engine.evaluate_action(action, actor_id)

        return render_template(
            "index.html",
            action_json=action_json,
            actor_id=actor_id,
            result=result,
            result_json=json.dumps(result, ensure_ascii=False, indent=2) if result else None,
            error=error,
        )

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
