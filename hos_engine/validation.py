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
        store: dict[str, dict[str, Any]] = {
            (self.schema_dir / name).resolve().as_uri(): content
            for name, content in self.schemas.items()
        }
        # A schema that declares an $id resolves its relative $refs against
        # that $id, not against the local file path — register every schema
        # under each declared $id base too, so sibling references like
        # "common.schema.json" resolve offline.
        id_bases = {
            declared_id.rsplit("/", 1)[0] + "/"
            for content in self.schemas.values()
            if isinstance(declared_id := content.get("$id"), str) and "/" in declared_id
        }
        for base in id_bases:
            for name, content in self.schemas.items():
                store[base + name] = content
        resolver = RefResolver(
            base_uri=self.schema_dir.resolve().as_uri() + "/",
            referrer=schema,
            store=store,
        )
        Draft202012Validator(schema, resolver=resolver).validate(instance)
