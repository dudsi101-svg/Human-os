from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# jsonschema publishes no type stubs -- the ignore below is scoped to that.
from jsonschema import (  # type: ignore[import-untyped]
    Draft202012Validator,
    RefResolver,
)


class SchemaRegistry:
    def __init__(self, schema_dir: str | Path) -> None:
        self.schema_dir = Path(schema_dir)
        self.schemas: dict[str, dict[str, Any]] = {}
        for path in self.schema_dir.glob("*.json"):
            schema = json.loads(path.read_text(encoding="utf-8"))
            self.schemas[path.name] = schema

    def validate(self, schema_name: str, instance: dict[str, Any]) -> None:
        schema = self.schemas[schema_name]
        resolver = RefResolver(
            base_uri=self.schema_dir.resolve().as_uri() + "/",
            referrer=schema,
            store={
                path.resolve().as_uri(): value
                for path, value in [
                    (self.schema_dir / name, content)
                    for name, content in self.schemas.items()
                ]
            },
        )
        Draft202012Validator(schema, resolver=resolver).validate(instance)
