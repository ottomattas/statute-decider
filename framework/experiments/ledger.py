"""Append-only JSONL cost ledger and USD price lookup."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterator

import yaml

from providers import Usage

from .budget import usd_to_eur

_MILLION = 1_000_000
_DEFAULT_WORST_INPUT = 32_000
_DEFAULT_WORST_OUTPUT = 8_192


def repo_root() -> Path:
    """Return the statute-decider repository root."""
    return Path(__file__).resolve().parents[2]


def prices_path() -> Path:
    return repo_root() / "experiments" / "prices.yaml"


def ledger_path() -> Path:
    return repo_root() / "experiments" / "ledger.jsonl"


@lru_cache(maxsize=1)
def _load_prices_file(path_str: str) -> dict[str, Any]:
    raw = yaml.safe_load(Path(path_str).read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError(f"prices file {path_str} must be a mapping")
    return raw


def load_price_table(path: Path | None = None) -> dict[str, dict[str, Any]]:
    data = _load_prices_file(str(path or prices_path()))
    models = data.get("models")
    if not isinstance(models, dict):
        raise ValueError("prices.yaml must contain a 'models' mapping")
    aliases = data.get("aliases") or {}
    table = {str(name): dict(row) for name, row in models.items()}
    for alias, target in aliases.items():
        if target not in table:
            raise ValueError(f"Alias {alias!r} points at unknown model {target!r}")
        table[str(alias)] = table[str(target)]
    return table


def lookup_price(model: str, path: Path | None = None) -> dict[str, Any]:
    table = load_price_table(path)
    try:
        return table[model]
    except KeyError as exc:
        known = ", ".join(sorted(table))
        raise ValueError(f"No price for model {model!r}. Known: {known}") from exc


def estimate_usd(model: str, usage: Usage, path: Path | None = None) -> float:
    """USD cost for ``usage`` at the model's listed per-1M rates.

    Cached input tokens are billed at the full input rate (conservative).
    """
    row = lookup_price(model, path)
    inp = float(row["input_usd_per_million"])
    out = float(row["output_usd_per_million"])
    usd = (usage.input_tokens / _MILLION) * inp + (usage.output_tokens / _MILLION) * out
    return round(usd, 8)


def estimate_worst_case_usd(
    model: str,
    *,
    max_input_tokens: int = _DEFAULT_WORST_INPUT,
    max_output_tokens: int = _DEFAULT_WORST_OUTPUT,
    path: Path | None = None,
) -> float:
    return estimate_usd(
        model,
        Usage(input_tokens=max_input_tokens, output_tokens=max_output_tokens),
        path,
    )


def append_ledger(
    *,
    provider: str,
    model: str,
    experiment: str,
    scenario: str,
    input_tokens: int,
    output_tokens: int,
    usd: float,
    eur: float | None = None,
    path: Path | None = None,
) -> dict[str, Any]:
    """Append one JSONL row. ``eur`` defaults to ``usd`` converted at USD_TO_EUR."""
    row = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "provider": provider,
        "model": model,
        "experiment": experiment,
        "scenario": scenario,
        "input_tokens": int(input_tokens),
        "output_tokens": int(output_tokens),
        "usd": round(float(usd), 8),
        "eur": round(float(eur) if eur is not None else usd_to_eur(usd), 6),
    }
    out = path or ledger_path()
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=True) + "\n")
    return row


def iter_ledger(path: Path | None = None) -> Iterator[dict[str, Any]]:
    target = path or ledger_path()
    if not target.is_file():
        return
    for line in target.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        yield json.loads(stripped)
