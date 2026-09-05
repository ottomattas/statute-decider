"""Legislation corpus: official Riigi Teataja XML, one reference vocabulary.

* ``riigiteataja`` — parse a consolidated-text XML (``tyviseadus_1_10.02.2010``),
  iterate provisions, the RT-id <-> Akoma Ntoso eId bijection, plain-text rendering.
* ``catalogue`` — ``data/sources/legislation/catalogue.json`` (generated, never hand-edited).
* ``references`` — ``<act_slug>/<eId>`` provision keys and their display form.
* ``corpus`` — ingest / check the corpus directory (``sd corpus``).

RT element ids (``para11lg5p1``) are never stored anywhere this repo writes;
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

__all__ = [
    "Act",
    "ActMetadata",
    "Catalogue",
    "CatalogueEntry",
    "Provision",
    "ProvisionRef",
    "display_eid",
    "display_reference",
    "eid_to_rt_id",
    "is_within",
    "load_act",
    "parse_metadata",
    "parse_reference",
    "rt_id_to_eid",
    "validate_eid",
]
