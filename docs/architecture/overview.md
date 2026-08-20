# Architecture Overview

## Purpose

The framework provides a graph-native neurosymbolic runtime for transforming structured knowledge into deterministic decision support while keeping the implementation use-case agnostic.

## Core objects

The public API is built around four top-level objects:

- `World`
- `Case`
- `Agent`
- `Decision`

Each object exposes the same outer shape:

- `model`
- `state`
- `governance`
- `history`
- `meta`

This keeps the mental model stable while allowing each object to specialize internally.

## Shared model/state split

`model` carries reusable knowledge:

- `ontology` for declarations and axioms
- `rules` for executable statements
- `conformance` for closed-world checks and local-closure expectations
- `sources` for provenance-grounding artefacts

`state` carries the active decision-time slice:

- `graph` for assertions
- `context` for temporal and jurisdictional scope
- `provenance` for how the state was assembled
- `conflicts` for explicit contradictions
- `hypotheses` for abductive or explanatory placeholders
- `proposals` for pending or historical updates

`Decision.state` extends the shared state shape with:

- `valuation`
- `stage`
- `actions`
- `outcomes`
- `records`

## Decision pipeline

The staged reasoner proceeds as follows:

1. Compose `Decision.state.graph` from world, case, agent, and pre-existing decision assertions.
2. Evaluate conformance clauses against that composed graph.
3. Detect explicit conflicts without collapsing reasoning into explosion.
4. Compute four-valued rule-atom valuation.
5. Evaluate rules through a symbolic solver over the conclusive boolean slice.
6. Apply rule effects into decision state.

This keeps graph assembly, conformance, valuation, and effect application visible as separate reasoning phases.

## Governed evolution

Runtime decisioning does not silently extend the active world. World evolution is handled separately through proposal and approval workflow:

1. an authorized agent proposes an assertion update
2. an approver reviews it
3. approved changes are applied to `World.state.graph`
4. approvals and world-history events preserve traceability

This separation keeps decision execution and knowledge-governance distinct.
