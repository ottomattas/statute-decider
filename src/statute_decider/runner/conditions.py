"""Conditions: named bindings of methods onto nodes (plus fuse declarations).

Oracle, baseline, and candidate are conditions, not extra machinery. A
condition never precludes an experiment — what a condition binds is config.
"""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field

from statute_decider.nodes import NODE_ORDER

VALID_METHODS = {
    "oracle",
    "llm",
    "solver",
    "lookup",
    "match",
    "render",
    "parse",
    "file",
    "slice",
    "live",
    "generate",
    "skip",
}


class NodeBinding(BaseModel):
    method: str
    strategy: str | None = None
    prompt: str | None = None  # prompt variant (llm) — swept by experiments
    solver: str | None = None  # backend (solver method)
    template: str | None = None  # render template

    def model_post_init(self, context, /) -> None:
        if self.method not in VALID_METHODS:
            raise ValueError(f"Unknown method {self.method!r}. Known: {sorted(VALID_METHODS)}")


class Condition(BaseModel):
    condition: str
    bindings: dict[str, NodeBinding] = Field(default_factory=dict)
    fuse: list[list[str]] = Field(default_factory=list)
    logic: str = "propositional"
    loop: str = "off"
    notes: str = ""

    def binding(self, node: str) -> NodeBinding:
        try:
            return self.bindings[node]
        except KeyError as exc:
            raise ValueError(
                f"Condition {self.condition!r} does not bind node {node!r}."
            ) from exc

    def fused_with(self, node: str) -> str | None:
        """Return the second node of a fuse pair whose first node is ``node``."""
        for pair in self.fuse:
            if pair and pair[0] == node:
                return pair[1]
        return None

    def is_fused_secondary(self, node: str) -> bool:
        return any(len(pair) > 1 and pair[1] == node for pair in self.fuse)

    def uses_llm(self) -> bool:
        return any(binding.method == "llm" for binding in self.bindings.values())


def load_condition(path: Path | str) -> Condition:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    name = raw.pop("condition", Path(path).stem)
    fuse = raw.pop("fuse", []) or []
    logic = raw.pop("logic", "propositional")
    loop = raw.pop("loop", "off")
    notes = raw.pop("notes", "")
    bindings = {node: NodeBinding.model_validate(spec) for node, spec in raw.items()}
    unknown = set(bindings) - set(NODE_ORDER)
    if unknown:
        raise ValueError(f"Condition {name!r} binds unknown nodes: {sorted(unknown)}")
    missing = set(NODE_ORDER) - set(bindings)
    if missing:
        raise ValueError(f"Condition {name!r} leaves nodes unbound: {sorted(missing)}")
    for pair in fuse:
        if len(pair) != 2 or any(node not in NODE_ORDER for node in pair):
            raise ValueError(f"Condition {name!r} has an invalid fuse pair: {pair}")
    return Condition(
        condition=name, bindings=bindings, fuse=fuse, logic=logic, loop=loop, notes=notes
    )
