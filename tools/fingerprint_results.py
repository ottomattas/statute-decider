"""Fingerprint every committed result set so an id rename can be proven lossless.

For each ``experiments/*/results/rows.jsonl`` the script records, per
``(experiment, condition, model, prompts)`` group, the outcome aggregate the
reports use (``OutcomeAggregate.summary()``: n, accuracy, per-class P/R/F1,
macro F1, missing-set means), the row count, and a canonical hash of every
row with the renameable id fields (``experiment``, ``condition``, ``case_id``,
``scenario_id``) removed. The ids themselves are kept beside the hash so a
verifier can map them (old -> new or back) and compare multisets.

Usage::

    .venv/bin/python tools/fingerprint_results.py /tmp/rename-before.json
    # ... rename ...
    .venv/bin/python tools/fingerprint_results.py /tmp/rename-after.json
    .venv/bin/python tools/fingerprint_results.py --compare \
        /tmp/rename-before.json /tmp/rename-after.json --map tools/rename_map.yaml

``--compare`` applies the map's inverse to the *after* file and asserts
identical group keys, row counts, aggregate numbers, and row multisets.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from statute_decider.runner.scoring import OutcomeAggregate  # noqa: E402

ID_FIELDS = ("experiment", "condition", "case_id", "scenario_id")


def _rows(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def _canonical_hash(row: dict) -> str:
    stripped = {k: v for k, v in row.items() if k not in ID_FIELDS}
    blob = json.dumps(stripped, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def fingerprint(root: Path) -> dict:
    out: dict = {"experiments": {}}
    for rows_path in sorted(root.glob("experiments/*/results/rows.jsonl")):
        exp_dir = rows_path.parents[1].name
        rows = _rows(rows_path)
        groups: dict[str, OutcomeAggregate] = defaultdict(OutcomeAggregate)
        counts: Counter = Counter()
        row_records = []
        for row in rows:
            key = json.dumps(
                [
                    row.get("experiment"),
                    row.get("condition"),
                    row.get("model"),
                    json.dumps(row.get("prompts") or {}, sort_keys=True),
                ]
            )
            counts[key] += 1
            if not row.get("error") and row.get("score"):
                groups[key].add(row["score"])
            row_records.append([*(row.get(f) for f in ID_FIELDS), _canonical_hash(row)])
        out["experiments"][exp_dir] = {
            "row_count": len(rows),
            "groups": {
                key: {"row_count": counts[key], "aggregate": groups[key].summary() if key in groups else None}
                for key in sorted(counts)
            },
            "rows": row_records,
        }
    return out


def _inverse_map(map_path: Path) -> dict:
    import yaml

    m = yaml.safe_load(map_path.read_text(encoding="utf-8"))
    inv_exp = {v: k for k, v in (m.get("experiments") or {}).items()}
    inv_cond = {v: k for k, v in (m.get("conditions") or {}).items()}
    inv_scen = {v: k for k, v in (m.get("scenarios") or {}).items()}
    inv_case = {v: k for k, v in (m.get("cases") or {}).items()}
    return {"experiments": inv_exp, "conditions": inv_cond, "scenarios": inv_scen, "cases": inv_case}


def _unmap_row(rec: list, inv: dict) -> tuple:
    experiment, condition, case_id, scenario_id, digest = rec
    experiment = inv["experiments"].get(experiment, experiment)
    condition = inv["conditions"].get(condition, condition)
    pair = inv["scenarios"].get(f"{case_id}/{scenario_id}")
    if pair:
        case_id, scenario_id = pair.split("/", 1)
    else:
        case_id = inv["cases"].get(case_id, case_id)
    return (experiment, condition, case_id, scenario_id, digest)


def _unmap_group_key(key: str, inv: dict) -> str:
    experiment, condition, model, prompts = json.loads(key)
    return json.dumps(
        [inv["experiments"].get(experiment, experiment), inv["conditions"].get(condition, condition), model, prompts]
    )


def compare(before_path: Path, after_path: Path, map_path: Path | None) -> int:
    before = json.loads(before_path.read_text(encoding="utf-8"))["experiments"]
    after = json.loads(after_path.read_text(encoding="utf-8"))["experiments"]
    inv = _inverse_map(map_path) if map_path else {"experiments": {}, "conditions": {}, "scenarios": {}, "cases": {}}
    problems: list[str] = []
    after_by_old = {inv["experiments"].get(name, name): data for name, data in after.items()}
    if set(before) != set(after_by_old):
        problems.append(f"experiment set differs: {sorted(set(before) ^ set(after_by_old))}")
    for name in sorted(set(before) & set(after_by_old)):
        b, a = before[name], after_by_old[name]
        if b["row_count"] != a["row_count"]:
            problems.append(f"{name}: row count {b['row_count']} != {a['row_count']}")
        a_groups = {_unmap_group_key(k, inv): v for k, v in a["groups"].items()}
        if set(b["groups"]) != set(a_groups):
            problems.append(f"{name}: group keys differ: {sorted(set(b['groups']) ^ set(a_groups))}")
        for key in sorted(set(b["groups"]) & set(a_groups)):
            if b["groups"][key] != a_groups[key]:
                problems.append(f"{name}: group {key} aggregate/count differs")
        b_rows = Counter(tuple(r) for r in b["rows"])
        a_rows = Counter(_unmap_row(r, inv) for r in a["rows"])
        if b_rows != a_rows:
            diff = (b_rows - a_rows) + (a_rows - b_rows)
            problems.append(f"{name}: row multiset differs in {sum(diff.values())} rows, e.g. {next(iter(diff))}")
    if problems:
        for p in problems:
            print(f"MISMATCH {p}")
        return 1
    total = sum(d["row_count"] for d in before.values())
    print(f"OK: {len(before)} experiments, {total} rows; counts, aggregates and row multisets identical.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--compare", action="store_true")
    parser.add_argument("--map", default=None, help="tools/rename_map.yaml (for --compare)")
    parser.add_argument("--root", default=str(ROOT))
    args = parser.parse_args(argv)
    if args.compare:
        if len(args.paths) != 2:
            parser.error("--compare needs BEFORE AFTER")
        return compare(Path(args.paths[0]), Path(args.paths[1]), Path(args.map) if args.map else None)
    out = Path(args.paths[0])
    data = fingerprint(Path(args.root))
    out.write_text(json.dumps(data, indent=1, sort_keys=True), encoding="utf-8")
    total = sum(d["row_count"] for d in data["experiments"].values())
    print(f"Fingerprinted {len(data['experiments'])} experiments, {total} rows -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
