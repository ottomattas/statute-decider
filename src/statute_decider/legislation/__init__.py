"""Legislation corpus: official Riigi Teataja XML, one reference vocabulary.

* ``riigiteataja`` — parse a consolidated-text XML (``tyviseadus_1_10.02.2010``),
  iterate provisions, the RT-id <-> Akoma Ntoso eId bijection, plain-text rendering.
* ``catalogue`` — ``data/sources/legislation/catalogue.json`` (generated, never hand-edited).
* ``references`` — ``<act_slug>/<eId>`` provision keys and their display form.
* ``corpus`` — ingest / check the corpus directory (``sd corpus``).
* ``units`` — the statute input a model receives: whole act or the smallest
  structural unit enclosing the declared provisions, within a token budget (Ruling H).

Riigi Teataja element ids are never stored anywhere this repo writes;
the resolver recomputes them from the eId at lookup time.
"""

from statute_decider.legislation.catalogue import Catalogue, CatalogueEntry
from statute_decider.legislation.references import (
    ProvisionRef,
    display_eid,
    display_reference,
    is_within,
    parse_reference,
    validate_eid,
)
from statute_decider.legislation.riigiteataja import (
    Act,
    ActMetadata,
    Provision,
    eid_to_rt_id,
    load_act,
    parse_metadata,
    rt_id_to_eid,
)
from statute_decider.legislation.units import (
    DEFAULT_MAX_STATUTE_TOKENS,
    UnitChoice,
    UnitTooLarge,
    estimate_tokens,
    select_statute_unit,
    unit_candidates,
)

__all__ = [
    "Act",
    "ActMetadata",
    "Catalogue",
    "CatalogueEntry",
    "DEFAULT_MAX_STATUTE_TOKENS",
    "Provision",
    "ProvisionRef",
    "UnitChoice",
    "UnitTooLarge",
    "display_eid",
    "display_reference",
    "eid_to_rt_id",
    "estimate_tokens",
    "is_within",
    "load_act",
    "parse_metadata",
    "parse_reference",
    "rt_id_to_eid",
    "select_statute_unit",
    "unit_candidates",
    "validate_eid",
]
