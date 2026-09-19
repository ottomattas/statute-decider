# ADR 0008: Results transcripts are gzip on disk and in git

## Status

Accepted — 2026-09-19

## Context

`results/transcript.jsonl` is the audit trail for every provider call
(rendered system and user messages, raw response). Statute-carrying cells
repeat the whole act in every call, so a finished grid can exceed GitHub's
100 MB file limit. At paper pin `20a3a60` the two largest r2 transcripts
were gzipped by hand and committed as `transcript.jsonl.gz`; the other 29
runs stayed plain. There was no writer path, no reader, and no guard —
`--resume` on a finished grid rewrote `config.snapshot.yaml`,
`invocations.jsonl`, `run.log`, and `summary.md` even when zero cells ran
(the leftover LaunchAgent re-fires of 14–18 Sep).

## Decision

1. **Gzip is the only on-disk and in-git format.** The writer streams
   `transcript.jsonl.gz` (`gzip.open(..., "at")`). One gzip member per
   invocation; a resume appends a second member; the stdlib reader
   concatenates members. A leftover plain `transcript.jsonl` is read-only
   compatibility during migration.
2. **Inspect through the CLI**, not `gunzip -k` in the repo:
   `sd transcript cat|extract|compress|check`.
3. **A no-op `--resume` writes nothing.** Pending cells are computed
   before any result sidecar is opened; `resume` with zero pending units
   logs and returns.
4. **CI fails** a tracked file under `experiments/` over 90 MB, a leftover
   plain `transcript.jsonl`, or a corrupt `.gz`.
5. **No history rewrite.** Pin `20a3a60` still holds plain files for the
   early runs and the hand-made `.gz` for the r2 runs. Reproduction stays
   `git checkout 20a3a60`.

## Consequences

- Git LFS is not used. `rows.jsonl` and `nodes/*.jsonl` stay plain (largest
  is ~6 MB).
- `tools/rename_ids.py` reads and writes `.gz` through the same I/O layer.
- Multi-member files are normal after a resumed LLM run; `gzip -t` and
  `sd transcript cat` both accept them.
