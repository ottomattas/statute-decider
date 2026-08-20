# ADR 0001: Graph-native knowledge objects

## Status

Accepted

## Context

The framework needed one coherent public shape across world knowledge, case knowledge, agent knowledge, and decision-time reasoning state. The earlier implementation mixed schema-like structures and decision-time values under incompatible object shapes.

## Decision

Use four top-level objects:

- `World`
- `Case`
- `Agent`
- `Decision`

Each object exposes:

- `model`
- `state`
- `governance`
- `history`
- `meta`

`model` carries ontology, rules, conformance, and sources. `state` carries graph assertions, context, provenance, conflicts, hypotheses, and proposals. `Decision.state` extends the shared state with valuation, stage, actions, outcomes, and records.

## Consequences

- The public API is easier to explain and serialize.
- Shared vocabulary can be reused across world, case, agent, and decision layers.
- Governed world evolution is represented as proposal and approval flow instead of implicit runtime extension.
