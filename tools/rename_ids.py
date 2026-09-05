"""Rename statute / case / scenario / register / condition / experiment / prompt ids
in place, driven only by ``tools/rename_map.yaml``. Idempotent; no LLM call.

What it touches (see docs/reference/id-aliases.md for the full table):

* data plane — ``git mv`` of statute, register, case directories and of
  scenario YAML / oracle JSON files; structured id fields rewritten
  (``statute_id``, ``case_id``, ``scenario_id``, ``register_id``,
  ``statute_ids[]``, ``register_ids[]``, ``unavailable_registers[]``,
  ``register_overrides`` keys); tags/label/mechanism from the map.
* configs — condition files renamed, ``condition:`` / ``prompt:`` rewritten;
  prompt files renamed (content untouched, so recorded ``prompt_hash`` stays valid).
* results plane, per experiment — folder renamed; ``experiment.yaml``,
  ``config.snapshot.yaml``, ``invocations.jsonl``, ``rows.jsonl``,
  ``nodes/*.jsonl``, ``ledger.jsonl`` rewritten in their *structured* id
  fields; ``transcript.jsonl`` ``meta.*`` only. Free text (``system``,
  ``user``, ``raw_response``, ``justification``, ``message``, ``note``,
  ``run.log``) is never rewritten. ``summary.md`` is regenerated through
  ``render_summary``; ``docs/matrix.csv`` through ``sd matrix export``.

Numbers never change: every rewrite is a key/value substitution on ids.
Prove it with ``tools/fingerprint_results.py --compare``.

Usage::

    .venv/bin/python tools/rename_ids.py            # apply
    .venv/bin/python tools/rename_ids.py --dry-run  # list the moves only
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

MAP_PATH = ROOT / "tools" / "rename_map.yaml"
RENAME_NOTE = (
    "ids renamed 2026-09-05, see docs/reference/id-aliases.md; "
    "free-text prompt/response strings keep the pre-rename ids"
)
PROVENANCE_MARK = "renamed 2026-09-05 from "
SCENARIO_KEY_ORDER = [
    "scenario_id", "case_id", "label", "mechanism", "description", "utterance_file",
    "register_overrides", "tags", "gold_confidence", "notes", "provenance",
]


class RenameMap:
    def __init__(self, path: Path) -> None:
        m = yaml.safe_load(path.read_text(encoding="utf-8"))
        self.statutes: dict[str, str] = m.get("statutes") or {}
        self.cases: dict[str, str] = m.get("cases") or {}
        self.registers: dict[str, str] = m.get("registers") or {}
        self.scenarios: dict[str, str] = m.get("scenarios") or {}
        self.conditions: dict[str, str] = m.get("conditions") or {}
        self.experiments: dict[str, str] = m.get("experiments") or {}
        self.prompts: dict[str, str] = m.get("prompts") or {}
        self.tags_add: dict[str, list[str]] = m.get("tags_add") or {}
        self.scenario_fields: dict[str, dict] = m.get("scenario_fields") or {}
        # variant-name view of the prompt map: "solver-inputs-v1" -> "solver-inputs-partial-specification"
        self.prompt_variants = {k.rsplit("/", 1)[-1]: v.rsplit("/", 1)[-1] for k, v in self.prompts.items()}
        # per old case: old scenario -> new scenario
        self.scen_by_case: dict[str, dict[str, str]] = {}
        for old, new in self.scenarios.items():
            oc, os_ = old.split("/", 1)
            nc, ns = new.split("/", 1)
            if self.cases.get(oc, oc) != nc:
                raise ValueError(f"scenario map {old} -> {new} disagrees with cases map")
            self.scen_by_case.setdefault(oc, {})[os_] = ns

    def pair(self, case_id: str, scenario_id: str) -> tuple[str, str]:
        new_scen = self.scen_by_case.get(case_id, {}).get(scenario_id, scenario_id)
        return self.cases.get(case_id, case_id), new_scen

    def composite(self, composite: str) -> str:
        case_id, scenario_id = composite.split("/", 1)
        return "/".join(self.pair(case_id, scenario_id))


M = RenameMap(MAP_PATH)
DRY = False
MOVES: list[tuple[Path, Path]] = []


# --- helpers -----------------------------------------------------------------


def git_mv(old: Path, new: Path) -> None:
    if not old.exists() or old == new:
        return
    MOVES.append((old, new))
    if DRY:
        print(f"git mv {old.relative_to(ROOT)} -> {new.relative_to(ROOT)}")
        return
    new.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "mv", str(old), str(new)], check=True, cwd=ROOT)


def read_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def write_json(p: Path, data) -> None:
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_yaml(p: Path) -> dict:
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


class _BlockDumper(yaml.SafeDumper):
    """Multi-line strings as literal blocks (experiment.yaml question/notes stay readable)."""


def _str_representer(dumper: yaml.SafeDumper, value: str):
    style = "|" if "\n" in value else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


_BlockDumper.add_representer(str, _str_representer)


def write_yaml(p: Path, data, *, block: bool = False) -> None:
    """Default dump matches what the runner/authoring tools write (round-trip stable);
    ``block=True`` is used for hand-edited experiment.yaml so long strings stay readable."""
    if block:
        text = yaml.dump(data, Dumper=_BlockDumper, sort_keys=False, allow_unicode=True)
    else:
        text = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    p.write_text(text, encoding="utf-8")


def jsonl_line(row) -> str:
    return json.dumps(row, ensure_ascii=False, default=str)


def rewrite_jsonl(p: Path, fix) -> None:
    """Rewrite each line through ``fix``; abort if a line does not round-trip byte-for-byte."""
    if not p.exists():
        return
    out_lines = []
    for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        if jsonl_line(row) != line:
            raise RuntimeError(f"{p}:{n} does not round-trip through json.dumps; refusing to rewrite")
        out_lines.append(jsonl_line(fix(row)))
    if not DRY:
        p.write_text("".join(l + "\n" for l in out_lines), encoding="utf-8")


def map_register_fields(obj, scenario_map: dict[str, str] | None = None):
    """Recursively rewrite structured id fields: register_id, unavailable_registers,
    register_ids, register_overrides keys, statute_id(s), prompt_id, and —
    when ``scenario_map`` is given — scenario_id. Never touches other strings."""
    if isinstance(obj, list):
        for item in obj:
            map_register_fields(item, scenario_map)
        return obj
    if not isinstance(obj, dict):
        return obj
    for key, value in list(obj.items()):
        if key == "register_id" and isinstance(value, str):
            obj[key] = M.registers.get(value, value)
        elif key in ("unavailable_registers", "register_ids") and isinstance(value, list):
            obj[key] = [M.registers.get(v, v) for v in value]
        elif key == "register_overrides" and isinstance(value, dict):
            obj[key] = {M.registers.get(k, k): v for k, v in value.items()}
        elif key == "statute_id" and isinstance(value, str):
            obj[key] = M.statutes.get(value, value)
        elif key == "statute_ids" and isinstance(value, list):
            obj[key] = [M.statutes.get(v, v) for v in value]
        elif key == "prompt_id" and isinstance(value, str):
            obj[key] = M.prompts.get(value, value)
        elif key == "scenario_id" and scenario_map is not None and isinstance(value, str):
            obj[key] = scenario_map.get(value, value)
        elif isinstance(value, (dict, list)):
            map_register_fields(value, scenario_map)
    return obj


# --- data plane --------------------------------------------------------------


def rename_statutes() -> None:
    for old, new in M.statutes.items():
        git_mv(ROOT / "data" / "statutes" / old, ROOT / "data" / "statutes" / new)
        d = ROOT / "data" / "statutes" / new
        if DRY or not d.exists():
            continue
        side = d / "statute.yaml"
        data = read_yaml(side)
        data["statute_id"] = new
        write_yaml(side, data)
        for name in ("text_term.json", "term_rule.json"):
            p = d / "oracle" / name
            if p.exists():
                write_json(p, map_register_fields(read_json(p)))


def rename_registers() -> None:
    for old, new in M.registers.items():
        git_mv(ROOT / "data" / "registers" / old, ROOT / "data" / "registers" / new)
        d = ROOT / "data" / "registers" / new
        if DRY or not d.exists():
            continue
        schema = d / "schema.yaml"
        data = read_yaml(schema)
        data["register_id"] = new
        write_yaml(schema, data)
        p = d / "oracle" / "record_term.json"
        if p.exists():
            write_json(p, map_register_fields(read_json(p)))


def rename_cases() -> None:
    for old_case, new_case in M.cases.items():
        git_mv(ROOT / "data" / "cases" / old_case, ROOT / "data" / "cases" / new_case)
        d = ROOT / "data" / "cases" / new_case
        scen_map = M.scen_by_case.get(old_case, {})
        # file moves
        for old_scen, new_scen in scen_map.items():
            git_mv(d / "scenarios" / f"{old_scen}.yaml", d / "scenarios" / f"{new_scen}.yaml")
            for node_dir in (d / "oracle").glob("*"):
                git_mv(node_dir / f"{old_scen}.json", node_dir / f"{new_scen}.json")
        if DRY or not d.exists():
            continue
        # case.yaml
        case_yaml = d / "case.yaml"
        data = read_yaml(case_yaml)
        data["case_id"] = new_case
        write_yaml(case_yaml, map_register_fields(data))
        # base registry
        reg = d / "sources" / "registry.json"
        if reg.exists():
            write_json(reg, map_register_fields(read_json(reg)))
        # scenarios
        for old_scen, new_scen in scen_map.items():
            composite = f"{old_case}/{old_scen}"
            p = d / "scenarios" / f"{new_scen}.yaml"
            data = read_yaml(p)
            data["scenario_id"] = new_scen
            data["case_id"] = new_case
            map_register_fields(data)
            tags = list(data.get("tags") or [])
            for tag in M.tags_add.get(composite, []):
                if tag not in tags:
                    tags.append(tag)
            data["tags"] = tags
            data.update(M.scenario_fields.get(composite, {}))
            prov = str(data.get("provenance") or "")
            if PROVENANCE_MARK not in prov:
                data["provenance"] = (prov + " | " if prov else "") + f"{PROVENANCE_MARK}{composite}"
            ordered = {k: data[k] for k in SCENARIO_KEY_ORDER if k in data}
            ordered.update({k: v for k, v in data.items() if k not in ordered})
            write_yaml(p, ordered)
            # oracle node values
            for node_dir in (d / "oracle").glob("*"):
                q = node_dir / f"{new_scen}.json"
                if q.exists():
                    write_json(q, map_register_fields(read_json(q), {old_scen: new_scen}))


# --- configs -----------------------------------------------------------------


def rename_conditions() -> None:
    cond_dir = ROOT / "configs" / "conditions"
    for old, new in M.conditions.items():
        git_mv(cond_dir / f"{old}.yaml", cond_dir / f"{new}.yaml")
        p = cond_dir / f"{new}.yaml"
        if DRY or not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        text = re.sub(rf"^condition:\s*{re.escape(old)}\s*$", f"condition: {new}", text, flags=re.M)
        for ov, nv in M.prompt_variants.items():
            text = re.sub(rf"(prompt:\s*){re.escape(ov)}(?=[\s,}}\]]|$)", rf"\g<1>{nv}", text)
        p.write_text(text, encoding="utf-8")


def rename_prompts() -> None:
    for old, new in M.prompts.items():
        git_mv(ROOT / "prompts" / f"{old}.md", ROOT / "prompts" / f"{new}.md")


def rename_template() -> None:
    p = ROOT / "experiments" / "_template" / "experiment.yaml"
    if DRY or not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    for old, new in M.conditions.items():
        text = re.sub(rf"^(condition:\s*){re.escape(old)}\b", rf"\g<1>{new}", text, flags=re.M)
    p.write_text(text, encoding="utf-8")


# --- results plane -----------------------------------------------------------


def fix_experiment_dict(exp: dict) -> dict:
    """experiment.yaml / snapshot.experiment: name, condition, cases[], prompts sweep."""
    exp["name"] = M.experiments.get(exp.get("name"), exp.get("name"))
    exp["condition"] = M.conditions.get(exp.get("condition"), exp.get("condition"))
    if isinstance(exp.get("cases"), list):
        exp["cases"] = [M.cases.get(c, c) for c in exp["cases"]]
    if isinstance(exp.get("prompts"), dict):
        exp["prompts"] = {
            node: [M.prompt_variants.get(v, v) for v in variants] for node, variants in exp["prompts"].items()
        }
    return exp


def fix_condition_dict(cond: dict) -> dict:
    cond["condition"] = M.conditions.get(cond.get("condition"), cond.get("condition"))
    for binding in (cond.get("bindings") or {}).values():
        if isinstance(binding, dict) and isinstance(binding.get("prompt"), str):
            binding["prompt"] = M.prompt_variants.get(binding["prompt"], binding["prompt"])
    return cond


def fix_snapshot(snap: dict) -> dict:
    if isinstance(snap.get("experiment"), dict):
        fix_experiment_dict(snap["experiment"])
    if isinstance(snap.get("condition"), dict):
        fix_condition_dict(snap["condition"])
    if isinstance(snap.get("scenarios"), list):
        snap["scenarios"] = [M.composite(s) for s in snap["scenarios"]]
    if isinstance(snap.get("prompt_combos"), list):
        snap["prompt_combos"] = [
            {node: M.prompt_variants.get(v, v) for node, v in combo.items()} for combo in snap["prompt_combos"]
        ]
    return snap


def fix_row(row: dict) -> dict:
    """rows / ledger / nodes / transcript.meta: structured ids only."""
    if "experiment" in row and isinstance(row["experiment"], str):
        row["experiment"] = M.experiments.get(row["experiment"], row["experiment"])
    if "condition" in row and isinstance(row["condition"], str):
        row["condition"] = M.conditions.get(row["condition"], row["condition"])
    if "prompt_id" in row and isinstance(row["prompt_id"], str):
        row["prompt_id"] = M.prompts.get(row["prompt_id"], row["prompt_id"])
    if isinstance(row.get("prompts"), dict):
        row["prompts"] = {node: M.prompt_variants.get(v, v) for node, v in row["prompts"].items()}
    scenario_map = None
    if isinstance(row.get("case_id"), str):
        old_case, old_scen = row["case_id"], row.get("scenario_id")
        scenario_map = M.scen_by_case.get(old_case, {})
        if isinstance(old_scen, str):
            row["case_id"], row["scenario_id"] = M.pair(old_case, old_scen)
        else:
            row["case_id"] = M.cases.get(old_case, old_case)
    if "value" in row:
        map_register_fields(row["value"], scenario_map)
    return row


def fix_transcript(row: dict) -> dict:
    if isinstance(row.get("meta"), dict):
        fix_row(row["meta"])
    return row


def regenerate_summary(exp_dir: Path) -> None:
    from statute_decider.runner.conditions import load_condition
    from statute_decider.runner.experiment import _load_rows, load_experiment
    from statute_decider.runner.report import render_summary

    results = exp_dir / "results"
    if not (results / "rows.jsonl").exists():
        return
    config = load_experiment(exp_dir / "experiment.yaml")
    condition = load_condition(ROOT / "configs" / "conditions" / f"{config.condition}.yaml")
    execution = "parallel"
    snap = results / "config.snapshot.yaml"
    if snap.exists():
        execution = str(read_yaml(snap).get("execution") or execution)
    summary = render_summary(
        experiment=config.model_dump(),
        condition=condition,
        rows=_load_rows(results / "rows.jsonl"),
        results_dir=results,
        execution=execution,
    )
    (results / "summary.md").write_text(summary, encoding="utf-8")


def rename_experiments() -> None:
    for old, new in M.experiments.items():
        git_mv(ROOT / "experiments" / old, ROOT / "experiments" / new)
        exp_dir = ROOT / "experiments" / new
        if DRY or not exp_dir.exists():
            continue
        # experiment.yaml (re-dumped; add the rename note once)
        ey = exp_dir / "experiment.yaml"
        exp = fix_experiment_dict(read_yaml(ey))
        notes = str(exp.get("notes") or "").rstrip()
        if RENAME_NOTE not in notes:
            exp["notes"] = (notes + "\n" if notes else "") + RENAME_NOTE + "\n"
        write_yaml(ey, exp, block=True)
        results = exp_dir / "results"
        if not results.exists():
            continue
        snap = results / "config.snapshot.yaml"
        if snap.exists():
            write_yaml(snap, fix_snapshot(read_yaml(snap)))
        rewrite_jsonl(results / "invocations.jsonl", fix_snapshot)
        rewrite_jsonl(results / "rows.jsonl", fix_row)
        rewrite_jsonl(results / "ledger.jsonl", fix_row)
        rewrite_jsonl(results / "transcript.jsonl", fix_transcript)
        for p in sorted((results / "nodes").glob("*.jsonl")) if (results / "nodes").exists() else []:
            rewrite_jsonl(p, fix_row)
        regenerate_summary(exp_dir)
        print(f"rewrote {new}")


def export_matrix() -> None:
    if DRY:
        return
    sd = ROOT / ".venv" / "bin" / "sd"
    if sd.exists():
        subprocess.run([str(sd), "matrix", "export"], check=True, cwd=ROOT)


def main(argv: list[str] | None = None) -> int:
    global DRY
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    DRY = args.dry_run
    rename_statutes()
    rename_registers()
    rename_cases()
    rename_conditions()
    rename_prompts()
    rename_template()
    rename_experiments()
    export_matrix()
    print(f"{'would move' if DRY else 'moved'} {len(MOVES)} paths")
    return 0


if __name__ == "__main__":
    sys.exit(main())
