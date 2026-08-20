"""Unit tests for the step-00 user-input extractor (Wave 3 Track C, ART-66)."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

FRAMEWORK_ROOT = Path(__file__).resolve().parents[1]
if str(FRAMEWORK_ROOT) not in sys.path:
    sys.path.insert(0, str(FRAMEWORK_ROOT))

from llm import UserInputExtractionItem, UserInputExtractionResponse  # noqa: E402
from schemas import EvidenceSnippet, LogicLevel  # noqa: E402
from use_case_files import load_use_case_from_dir  # noqa: E402
from user_input import (  # noqa: E402
    ClaimResponse,
    UserInputSession,
    UserUtterance,
    extract_user_input_deterministic,
    extract_user_input_llm,
    session_to_intent_assignments,
)


CASES = [
    "civil_service_eligibility",
    "consumer_withdrawal",
    "land_tax_exemption",
    "personal_data_journalism",
    "building_permit",
]


def _load_utterances(case: str, kind: str) -> list[UserUtterance]:
    path = FRAMEWORK_ROOT / "examples" / case / "user_input" / f"utterances_{kind}.json"
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [UserUtterance.model_validate(item) for item in raw]


class TestDeterministicExtractor(unittest.TestCase):
    def test_allow_sessions_resolve_claims_across_all_domains(self) -> None:
        """Every domain's allow fixture must produce at least one True response."""
        for case in CASES:
            with self.subTest(case=case):
                use_case = load_use_case_from_dir(FRAMEWORK_ROOT / "examples" / case)
                session = extract_user_input_deterministic(
                    use_case, _load_utterances(case, "allow")
                )
                truthy = [r for r in session.responses if r.value is True]
                self.assertTrue(
                    truthy, f"{case} allow session produced no positive responses"
                )
                # At least one claim should not need confirmation in the allow case.
                self.assertTrue(
                    any(not r.needs_user_confirmation for r in truthy),
                    f"{case} allow session has no firmly-positive response",
                )

    def test_needs_user_sessions_flag_u5_and_u8_signals(self) -> None:
        """needs_user fixtures must leave at least one claim unresolved (U5)
        and flag at least one hedged response for confirmation (U8)."""
        for case in CASES:
            with self.subTest(case=case):
                use_case = load_use_case_from_dir(FRAMEWORK_ROOT / "examples" / case)
                session = extract_user_input_deterministic(
                    use_case, _load_utterances(case, "needs_user")
                )
                self.assertTrue(
                    session.unresolved_claim_ids,
                    f"{case} needs_user has no U5 unresolved claim",
                )
                needs_confirm = [r for r in session.responses if r.needs_user_confirmation]
                self.assertTrue(
                    needs_confirm,
                    f"{case} needs_user produced no hedged U8 response",
                )
                # Hedged responses must carry value=None.
                for response in needs_confirm:
                    self.assertIsNone(response.value)

    def test_hedged_utterance_is_routed_to_needs_confirmation(self) -> None:
        use_case = load_use_case_from_dir(
            FRAMEWORK_ROOT / "examples" / "civil_service_eligibility"
        )
        utterances = [
            UserUtterance(
                text="I think I have full legal capacity but I'm not sure.",
                source="user",
            )
        ]
        session = extract_user_input_deterministic(use_case, utterances)
        full_capacity = next(
            r for r in session.responses if r.claim_id == "full_capacity"
        )
        self.assertIsNone(full_capacity.value)
        self.assertTrue(full_capacity.needs_user_confirmation)
        self.assertLess(full_capacity.confidence, 0.5)

    def test_explicit_unknown_is_unresolved_without_confirmation_flag(self) -> None:
        use_case = load_use_case_from_dir(
            FRAMEWORK_ROOT / "examples" / "civil_service_eligibility"
        )
        utterances = [
            UserUtterance(
                text="I don't know whether I have full legal capacity.",
                source="user",
            )
        ]
        session = extract_user_input_deterministic(use_case, utterances)
        full_capacity = next(
            r for r in session.responses if r.claim_id == "full_capacity"
        )
        self.assertIsNone(full_capacity.value)
        self.assertFalse(full_capacity.needs_user_confirmation)

    def test_negation_near_keyword_is_captured_as_false(self) -> None:
        use_case = load_use_case_from_dir(
            FRAMEWORK_ROOT / "examples" / "land_tax_exemption"
        )
        utterances = [
            UserUtterance(
                text="I am not the omanik of the parcel — my neighbour owns it.",
                source="user",
            )
        ]
        session = extract_user_input_deterministic(use_case, utterances)
        owner = next(
            r for r in session.responses if r.claim_id == "applicant_is_owner"
        )
        self.assertEqual(owner.value, False)

    def test_no_conflict_cue_is_not_misread_as_negation(self) -> None:
        """The "no family conflict" cue is itself part of the positive
        claim vocabulary and must not trigger a False value."""
        use_case = load_use_case_from_dir(
            FRAMEWORK_ROOT / "examples" / "civil_service_eligibility"
        )
        utterances = [
            UserUtterance(
                text="I confirm no family conflict with any supervising official.",
                source="user",
            )
        ]
        session = extract_user_input_deterministic(use_case, utterances)
        no_conflict = next(
            r for r in session.responses if r.claim_id == "no_conflict_declared"
        )
        self.assertEqual(no_conflict.value, True)

    def test_unmentioned_claims_become_u5_unresolved(self) -> None:
        use_case = load_use_case_from_dir(
            FRAMEWORK_ROOT / "examples" / "consumer_withdrawal"
        )
        utterances = [UserUtterance(text="I am a tarbija.", source="user")]
        session = extract_user_input_deterministic(use_case, utterances)
        self.assertIn("distance_contract", session.unresolved_claim_ids)
        self.assertIn("excluded_category", session.unresolved_claim_ids)
        self.assertIn("within_14_days", session.unresolved_claim_ids)
        self.assertIn("notice_sent_in_time", session.unresolved_claim_ids)

    def test_session_to_intent_assignments_shape(self) -> None:
        use_case = load_use_case_from_dir(
            FRAMEWORK_ROOT / "examples" / "land_tax_exemption"
        )
        session = extract_user_input_deterministic(
            use_case, _load_utterances("land_tax_exemption", "needs_user")
        )
        assignments, reasons, snippets = session_to_intent_assignments(session)
        # Every claim id is present in all three maps (responses + unresolved).
        for claim_id in use_case.claim_by_id:
            self.assertIn(claim_id, assignments)
            self.assertIn(claim_id, reasons)
            self.assertIn(claim_id, snippets)
        # At least one hedged response carries the needs_user_confirmation marker.
        confirm_markers = [
            claim_id
            for claim_id, reason in reasons.items()
            if "needs_user_confirmation=true" in reason
        ]
        self.assertTrue(
            confirm_markers,
            "Bridge did not surface any U8 needs_user_confirmation marker",
        )
        # Assignment values match response values where provided.
        for response in session.responses:
            self.assertEqual(assignments[response.claim_id], response.value)


class TestLlmBridge(unittest.TestCase):
    """The LLM path is exercised only via an in-memory fake generator.

    This avoids any dependency on `google.genai` and keeps the test suite
    deterministic and offline, as Wave 3 requires.
    """

    def test_llm_extractor_maps_fake_response_to_session(self) -> None:
        use_case = load_use_case_from_dir(
            FRAMEWORK_ROOT / "examples" / "land_tax_exemption"
        )
        utterances = [
            UserUtterance(
                text="I am the omanik and the land is elamumaa.",
                source="user",
            )
        ]
        canned = UserInputExtractionResponse(
            claims=[
                UserInputExtractionItem(
                    claim_id="applicant_is_owner",
                    value=True,
                    confidence=0.95,
                    needs_user_confirmation=False,
                    evidence=[EvidenceSnippet(snippet="I am the omanik")],
                ),
                UserInputExtractionItem(
                    claim_id="residential_land",
                    value=None,
                    confidence=0.4,
                    needs_user_confirmation=True,
                    evidence=[EvidenceSnippet(snippet="the land is elamumaa")],
                ),
            ]
        )

        def fake_generator(**_kwargs: object) -> UserInputExtractionResponse:
            return canned

        session = extract_user_input_llm(
            use_case,
            utterances,
            use_case_dir=str(FRAMEWORK_ROOT / "examples" / "land_tax_exemption"),
            logic_level=LogicLevel.PROPOSITIONAL,
            generator=fake_generator,
        )
        self.assertEqual(len(session.responses), 2)
        by_id = {r.claim_id: r for r in session.responses}
        self.assertTrue(by_id["applicant_is_owner"].value)
        self.assertTrue(by_id["residential_land"].needs_user_confirmation)
        # Unresolved claims cover the rest of the use-case vocabulary.
        remaining = set(use_case.claim_by_id) - {"applicant_is_owner", "residential_land"}
        self.assertEqual(set(session.unresolved_claim_ids), remaining)
        # Bridge maps to the build_intent_artifact shape.
        assignments, reasons, snippets = session_to_intent_assignments(session)
        self.assertEqual(assignments["applicant_is_owner"], True)
        self.assertIsNone(assignments["residential_land"])
        self.assertIn("needs_user_confirmation=true", reasons["residential_land"])
        self.assertEqual(snippets["applicant_is_owner"], ["I am the omanik"])


if __name__ == "__main__":
    unittest.main()
