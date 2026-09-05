"""Prompt templates: versioned config-plane data, swept like models.

``prompts/<node>/<strategy>/<variant>.md`` (nodes with one code path drop the
strategy segment). YAML frontmatter + template body. A new wording is a new
variant file; provenance records prompt id *and* content hash, so old results
stay interpretable.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class PromptTemplate:
    prompt_id: str  # e.g. "utterance_term/ground/ground"
    path: Path
    description: str
    system: str
    body: str
    sha256: str

    def render(self, **placeholders: str) -> str:
        try:
            return self.body.format(**placeholders)
        except KeyError as exc:
            raise ValueError(
                f"Prompt {self.prompt_id} expects placeholder {exc} not supplied."
            ) from exc

    def render_with_prefix(self, static: str, **placeholders: str) -> tuple[str, int]:
        """Render, and report how many leading characters are the static prefix.

        The prefix is everything up to and including the ``{static}``
        placeholder (e.g. the statute text). Callers pass that length to the
        LLM client so vendors that need an explicit cache marker get one; the
        rendered text is identical to ``render``.
        """
        marker = "{" + static + "}"
        idx = self.body.find(marker)
        if idx < 0:
            return self.render(**placeholders), 0
        head = self.body[: idx + len(marker)]
        try:
            prefix = head.format(**placeholders)
        except KeyError as exc:
            raise ValueError(
                f"Prompt {self.prompt_id} expects placeholder {exc} not supplied."
            ) from exc
        return prefix + self.body[idx + len(marker) :].format(**placeholders), len(prefix)


class _SafeDict(dict):
    def __missing__(self, key: str) -> str:  # pragma: no cover
        raise KeyError(key)


def load_prompt(
    prompts_dir: Path | str,
    node: str,
    variant: str,
    strategy: str | None = None,
) -> PromptTemplate:
    prompts_dir = Path(prompts_dir)
    candidates = []
    if strategy:
        candidates.append(prompts_dir / node / strategy / f"{variant}.md")
    candidates.append(prompts_dir / node / f"{variant}.md")
    path = next((p for p in candidates if p.exists()), None)
    if path is None:
        tried = ", ".join(str(p) for p in candidates)
        raise FileNotFoundError(f"No prompt file for {node}/{variant} (tried: {tried})")
    raw = path.read_text(encoding="utf-8")
    meta: dict = {}
    body = raw
    if raw.startswith("---"):
        _, front, body = raw.split("---", 2)
        meta = yaml.safe_load(front) or {}
        body = body.lstrip("\n")
    prompt_id = str(path.relative_to(prompts_dir).with_suffix(""))
    return PromptTemplate(
        prompt_id=prompt_id,
        path=path,
        description=str(meta.get("description", "")),
        system=str(meta.get("system", "")),
        body=body,
        sha256=hashlib.sha256(raw.encode("utf-8")).hexdigest(),
    )


def list_variants(prompts_dir: Path | str, node: str) -> list[str]:
    """All prompt ids available for a node (any strategy)."""
    node_dir = Path(prompts_dir) / node
    if not node_dir.exists():
        return []
    return sorted(
        str(p.relative_to(prompts_dir).with_suffix("")) for p in node_dir.rglob("*.md")
    )
