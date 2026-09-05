"""The experimentation matrix: capability registry + generated full expansion.

The hand-readable table lives in docs/refactor-v2-plan.md; the full expansion
is generated, never hand-written: ``sd matrix export`` joins the code
registries (nodes, methods, strategies) with ``configs/llm/models.yaml`` and
``prompts/`` — one row per chain x level x node x method x strategy x provider
x model x consumed artifact. Always in sync with what the code can run.
"""

from __future__ import annotations

import csv
import subprocess
from dataclasses import dataclass
from pathlib import Path

from statute_decider.llm.registry import ModelRegistry
from statute_decider.strategies import list_variants


@dataclass(frozen=True)
class Capability:
    chain: str
    level: str
    family: str
    node: str
    method: str
    strategies: tuple[str, ...] = ()
    future: bool = False  # declared expansion slot, no executor yet
    implemented: bool = True  # executor exists in this repo today
    note: str = ""


CAPABILITIES: list[Capability] = [
    # statute chain
    Capability("statute", "source", "*_text", "statute_text", "file", ("full-act",), note="the whole act rendered from the official Riigi Teataja XML in data/sources/legislation (provenance: global_id + sha256 + declared eIds)"),
    Capability("statute", "source", "*_text", "statute_text", "slice", ("declared-provisions",), note="only the eIds statute.yaml declares; ablation against full-act"),
    Capability("statute", "source", "*_text", "statute_text", "live", ("statute-api",), future=True, implemented=False),
    Capability("statute", "source", "*_text", "statute_text", "generate", ("synthetic",), future=True, implemented=False),
    Capability("statute", "source", "*_text", "regulation_text", "file", ("fixture",), future=True, implemented=False, note="new family member; feeds the same text_term"),
    Capability("statute", "source", "*_markup", "statute_markup", "file", ("riigiteataja-xml",), note="machine-readable legislation: Riigi Teataja tyviseadus XML (legislation.riigiteataja); Akoma Ntoso eIds"),
    Capability("statute", "term", "*_term", "text_term", "oracle", ("hand-defined catalog",)),
    Capability("statute", "term", "*_term", "text_term", "llm", ("select", "synthesize"), implemented=False, note="capability declared; executor lands with the experiment that needs it"),
    Capability("statute", "term", "*_term", "markup_term", "parse", ("provision-resolver",), note="eId -> provision element and display form (legislation.riigiteataja / references)"),
    Capability("statute", "premise", "term_*", "term_rule", "oracle", ("hand-authored rules",)),
    Capability("statute", "premise", "term_*", "term_rule", "llm", ("select", "synthesize"), implemented=False, note="loop re-entry (remap/regenerate) is a grid coordinate"),
    Capability("statute", "premise", "term_*", "term_presumption", "oracle", (), future=True, implemented=False, note="new epistemic type: statutory presumptions"),
    # user chain
    Capability("user", "source", "*_utterance", "user_utterance", "file", ("fixture",)),
    Capability("user", "source", "*_utterance", "user_utterance", "live", ("intake",), future=True, implemented=False),
    Capability("user", "source", "*_utterance", "user_utterance", "generate", ("synthetic",), future=True, implemented=False),
    Capability("user", "source", "*_document", "user_document", "file", ("fixture",), future=True, implemented=False, note="asserted — shape does not upgrade warrant"),
    Capability("user", "term", "*_term", "utterance_term", "oracle", ("hand-tagged recognition",)),
    Capability("user", "term", "*_term", "utterance_term", "llm", ("ground", "open")),
    Capability("user", "term", "*_term", "document_term", "llm", (), future=True, implemented=False),
    Capability("user", "premise", "term_*", "term_claim", "oracle", ("hand-assigned values",)),
    Capability("user", "premise", "term_*", "term_claim", "llm", ("value",), note="fusable with utterance_term (ground)"),
    # register chain
    Capability("register", "source", "*_record", "registry_record", "file", ("fixture",)),
    Capability("register", "source", "*_record", "registry_record", "live", ("register-api",), future=True, implemented=False),
    Capability("register", "source", "*_record", "registry_record", "generate", ("synthetic",), future=True, implemented=False),
    Capability("register", "term", "*_term", "record_term", "oracle", ("hand-validated mapping",)),
    Capability("register", "term", "*_term", "record_term", "match", ("name/alias matching",)),
    Capability("register", "term", "*_term", "record_term", "llm", ("schema-mapping",), implemented=False),
    Capability("register", "term", "*_term", "record_term", "vendor", ("register documentation",), future=True, implemented=False),
    Capability("register", "premise", "term_*", "term_fact", "oracle", ("hand-assigned values",)),
    Capability("register", "premise", "term_*", "term_fact", "lookup", ("via the mapping",)),
    Capability("register", "premise", "term_*", "term_fact", "llm", ("record-reading",), implemented=False, note="fusable with record_term"),
    # join
    Capability("join", "outcome", "*_outcome", "premise_outcome", "oracle", ("bind expected outcome",), note="isolation testing"),
    Capability("join", "outcome", "*_outcome", "premise_outcome", "solver", ("z3",)),
    Capability("join", "outcome", "*_outcome", "premise_outcome", "solver", ("pysat", "clingo", "horn", "hol"), future=True, implemented=False),
    Capability("join", "outcome", "*_outcome", "premise_outcome", "llm", ("decide",)),
    Capability("join", "trace", "*_trace", "outcome_trace", "oracle", ("hand-written reference trace",)),
    Capability("join", "trace", "*_trace", "outcome_trace", "render", ("default",)),
    Capability("join", "trace", "*_trace", "outcome_trace", "llm", ("justify",)),
]

CSV_HEADER = [
    "chain",
    "level",
    "node_family",
    "node",
    "method",
    "strategy",
    "provider",
    "model",
    "consumed_artifact",
    "future",
    "implemented",
    "note",
]


def _repo_commit(root: Path) -> str:
    try:
        return (
            subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                cwd=root,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            or "unknown"
        )
    except Exception:  # noqa: BLE001 - git absence must not break the export
        return "unknown"


def expand_rows(root: Path, registry: ModelRegistry) -> list[dict[str, str]]:
    """One row per fully-specified capability cell (executor + consumed artifact)."""
    prompts_dir = root / "prompts"
    commit = _repo_commit(root)
    rows: list[dict[str, str]] = []

    def add(cap: Capability, strategy: str, provider: str, model: str, consumed: str) -> None:
        rows.append(
            {
                "chain": cap.chain,
                "level": cap.level,
                "node_family": cap.family,
                "node": cap.node,
                "method": cap.method,
                "strategy": strategy,
                "provider": provider,
                "model": model,
                "consumed_artifact": consumed,
                "future": str(cap.future).lower(),
                "implemented": str(cap.implemented).lower(),
                "note": cap.note,
            }
        )

    for cap in CAPABILITIES:
        strategies = cap.strategies or ("",)
        if cap.method == "llm":
            variants = list_variants(prompts_dir, cap.node) or ["(prompt variant)"]
            for strategy in strategies:
                selected = [v for v in variants if f"{cap.node}/{strategy}/" in v] or variants
                for spec_id in registry.model_ids():
                    spec = registry.spec(spec_id)
                    for variant in selected:
                        add(cap, strategy, spec.provider, spec.model_id, variant)
        elif cap.method == "solver":
            for backend in strategies:
                add(cap, backend, backend, f"{backend} backend", "encoding options")
        elif cap.method == "oracle":
            for strategy in strategies:
                add(cap, strategy, "human", "operator", "authoring procedure / notes")
        else:  # file, match, lookup, render, parse, live, generate, vendor
            for strategy in strategies:
                consumed = {
                    "file": "fixture path",
                    "slice": "statute.yaml provisions",
                    "match": "term catalog (alias table)",
                    "lookup": "record_term mapping",
                    "render": "render template",
                    "parse": "markup grammar",
                    "live": "endpoint config",
                    "generate": "generation recipe",
                    "vendor": "register documentation",
                }.get(cap.method, "")
                add(cap, strategy, "code", commit, consumed)
    return rows


def export_matrix(root: Path, registry: ModelRegistry, out_path: Path | None = None) -> Path:
    out_path = out_path or root / "docs" / "matrix.csv"
    rows = expand_rows(root, registry)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_HEADER)
        writer.writeheader()
        writer.writerows(rows)
    return out_path


def bound_rows(condition_bindings: dict, fuse: list[list[str]]) -> list[dict[str, str]]:
    """The matrix rows a condition binds — rendered at the top of every summary."""
    rows = []
    for node, binding in condition_bindings.items():
        rows.append(
            {
                "node": node,
                "method": binding.method,
                "strategy": binding.strategy or "",
                "prompt": binding.prompt or "",
                "solver": binding.solver or "",
                "fused": "yes" if any(node in pair for pair in fuse) else "",
            }
        )
    return rows
