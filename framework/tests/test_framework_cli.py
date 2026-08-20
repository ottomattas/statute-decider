"""Focused checks for the `framework` four-step workflow."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

FRAMEWORK_ROOT = Path(__file__).resolve().parents[1]
if str(FRAMEWORK_ROOT) not in sys.path:
    sys.path.insert(0, str(FRAMEWORK_ROOT))

from llm import (  # noqa: E402
    DomainExtractionResponse,
    IntentExtractionItem,
    IntentExtractionResponse,
    extract_domain_artifact,
    extract_intent_artifact,
)
from logic_levels import build_domain_artifact, build_intent_artifact, render_solution_trace  # noqa: E402
from mock_db import load_mock_db  # noqa: E402
from reasoner import solve_case_bundle  # noqa: E402
from schemas import (  # noqa: E402
    BlockReasonCode,
    CaseBundle,
    ClaimSource,
    DomainArtifact,
    DomainClaim,
    DomainRule,
    EvidenceSnippet,
    ExtractionRunMetadata,
    IntentArtifact,
    IntentClaim,
    LogicLevel,
    LookupSource,
    MockDbArtifact,
    OutcomeDefinition,
    PromptMetadata,
    RuleKind,
    SolverOutcome,
    SolveRunMetadata,
)
from use_case_files import load_use_case_from_dir  # noqa: E402


class TestFrameworkCli(unittest.TestCase):
    def setUp(self) -> None:
        self.use_case_dir = FRAMEWORK_ROOT / "examples/section_120_demo"
        self.use_case = load_use_case_from_dir(self.use_case_dir)
        self.law_text = (FRAMEWORK_ROOT / "examples/section_120_demo/law.txt").read_text(encoding="utf-8")
        self.allow_text = (FRAMEWORK_ROOT / "examples/section_120_demo/request_allow.txt").read_text(encoding="utf-8")
        self.deny_text = (FRAMEWORK_ROOT / "examples/section_120_demo/request_deny.txt").read_text(encoding="utf-8")
        self.need_db_text = (FRAMEWORK_ROOT / "examples/section_120_demo/request_need_db.txt").read_text(encoding="utf-8")
        self.need_user_text = (FRAMEWORK_ROOT / "examples/section_120_demo/request_need_user.txt").read_text(encoding="utf-8")
        self.db_then_user_text = (
            FRAMEWORK_ROOT / "examples/section_120_demo/request_db_then_user.txt"
        ).read_text(encoding="utf-8")
        self.unrelated_law_text = (
            FRAMEWORK_ROOT / "examples/laws/121112025003.txt"
        ).read_text(encoding="utf-8")
        self.mock_db = load_mock_db(FRAMEWORK_ROOT / "examples/section_120_demo/mock_db.json")

    def _solve(
        self,
        request_text: str,
        assignments: dict[str, bool | None],
        *,
        logic_level: LogicLevel = LogicLevel.PROPOSITIONAL,
        mock_db: MockDbArtifact | None = None,
    ):
        domain = build_domain_artifact(self.use_case, logic_level, self.law_text)
        intent = build_intent_artifact(self.use_case, request_text, logic_level, assignments)
        bundle = CaseBundle(
            logic_level=logic_level,
            domain=domain,
            intent=intent,
            mock_db=mock_db or self.mock_db,
        )
        return solve_case_bundle(bundle)

    def test_allow_case(self) -> None:
        solution = self._solve(
            self.allow_text,
            {
                "applicant_is_parent": True,
                "applicant_is_not_parent": False,
                "emergency": True,
                "one_parent_unreachable": True,
            },
        )
        self.assertEqual(solution.final_outcome, SolverOutcome.ALLOW)

    def test_deny_case(self) -> None:
        solution = self._solve(
            self.deny_text,
            {
                "applicant_is_parent": False,
                "applicant_is_not_parent": True,
                "delegated_decision_right": False,
                "both_parents_consent": False,
            },
        )
        self.assertEqual(solution.final_outcome, SolverOutcome.DENY)

    def test_need_db_info_case(self) -> None:
        empty_db = MockDbArtifact(
            sources=[
                LookupSource(
                    source_id="empty",
                    label="Empty DB",
                    description="Returns no useful values.",
                    values={},
                )
            ]
        )
        solution = self._solve(
            self.need_db_text,
            {},
            mock_db=empty_db,
        )
        self.assertEqual(solution.final_outcome, SolverOutcome.NEED_DB_INFO)
        self.assertEqual(solution.snapshots[0].outcome, SolverOutcome.NEED_DB_INFO)

    def test_need_user_info_case(self) -> None:
        solution = self._solve(
            self.need_user_text,
            {
                "applicant_is_parent": True,
                "applicant_is_not_parent": False,
                "sole_custody": False,
                "delegated_decision_right": False,
                "both_parents_consent": False,
                "one_parent_unreachable": False,
                "emergency": None,
            },
        )
        self.assertEqual(solution.final_outcome, SolverOutcome.NEED_USER_INFO)

    def test_db_then_user_flow(self) -> None:
        solution = self._solve(
            self.db_then_user_text,
            {
                "emergency": None,
            },
        )
        self.assertEqual(solution.snapshots[0].outcome, SolverOutcome.NEED_DB_INFO)
        self.assertEqual(solution.final_outcome, SolverOutcome.NEED_USER_INFO)
        self.assertTrue(solution.lookup_events)

    def test_intent_post_validation_preserves_explicit_uncertainty(self) -> None:
        def fake_generator(*, response_model, **kwargs):
            self.assertEqual(response_model, IntentExtractionResponse)
            return IntentExtractionResponse(
                claims=[
                    IntentExtractionItem(
                        claim_id="emergency",
                        value=False,
                        reason="The request was interpreted as non-emergency.",
                        provenance=[
                            EvidenceSnippet(
                                snippet="I do not yet know whether this is an emergency.",
                                note="request text",
                            )
                        ],
                    )
                ]
            )

        artifact = extract_intent_artifact(
            self.use_case_dir,
            self.db_then_user_text,
            LogicLevel.PROPOSITIONAL,
            generator=fake_generator,
        )
        emergency = next(claim for claim in artifact.claims if claim.claim_id == "emergency")
        self.assertIsNone(emergency.value)
        self.assertIn("expresses uncertainty", emergency.reason)

    def test_intent_prompt_files_can_be_overridden(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            system_prompt = tmpdir_path / "intent.system.txt"
            user_prompt = tmpdir_path / "intent.user.txt"
            system_prompt.write_text("CUSTOM INTENT SYSTEM", encoding="utf-8")
            user_prompt.write_text(
                "CUSTOM INTENT USER\n{request_text}\n{claim_catalog}\n{outcome_catalog}",
                encoding="utf-8",
            )

            def fake_generator(*, system_instruction, user_content, response_model, **kwargs):
                self.assertEqual(response_model, IntentExtractionResponse)
                self.assertIn("CUSTOM INTENT SYSTEM", system_instruction)
                self.assertIn("CUSTOM INTENT USER", user_content)
                self.assertIn(self.allow_text.strip(), user_content)
                return IntentExtractionResponse(
                    claims=[
                        IntentExtractionItem(
                            claim_id="applicant_is_parent",
                            value=True,
                            reason="Grounded by custom prompt path test.",
                            provenance=[EvidenceSnippet(snippet="mother", note="text")],
                        )
                    ]
                )

            artifact = extract_intent_artifact(
                self.use_case_dir,
                self.allow_text,
                LogicLevel.PROPOSITIONAL,
                system_prompt_path=system_prompt,
                user_prompt_path=user_prompt,
                generator=fake_generator,
            )

        self.assertEqual(artifact.logic_level, LogicLevel.PROPOSITIONAL)
        self.assertEqual(artifact.claims[0].claim_id, "applicant_is_parent")

    def test_domain_prompt_files_can_be_overridden(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            system_prompt = tmpdir_path / "domain.system.txt"
            user_prompt = tmpdir_path / "domain.user.txt"
            system_prompt.write_text("CUSTOM DOMAIN SYSTEM", encoding="utf-8")
            user_prompt.write_text(
                "CUSTOM DOMAIN USER\n{law_text}\n{rule_catalog}\n{claim_catalog}",
                encoding="utf-8",
            )

            def fake_generator(*, system_instruction, user_content, response_model, **kwargs):
                self.assertEqual(response_model, DomainExtractionResponse)
                self.assertIn("CUSTOM DOMAIN SYSTEM", system_instruction)
                self.assertIn("CUSTOM DOMAIN USER", user_content)
                self.assertIn("Perekonnaseadus", user_content)
                return DomainExtractionResponse(
                    title="Custom prompt domain",
                    claim_ids=["applicant_is_parent", "emergency", "one_parent_unreachable"],
                    rule_ids=["allow_emergency"],
                    summary="Custom prompt path test.",
                )

            artifact = extract_domain_artifact(
                self.use_case_dir,
                self.law_text,
                LogicLevel.PROPOSITIONAL,
                system_prompt_path=system_prompt,
                user_prompt_path=user_prompt,
                generator=fake_generator,
            )

        self.assertEqual(artifact.title, "Custom prompt domain")
        self.assertEqual(len(artifact.rules), 1)

    def test_domain_validation_prunes_unrelated_law_ids(self) -> None:
        def fake_generator(*, response_model, **kwargs):
            self.assertEqual(response_model, DomainExtractionResponse)
            return DomainExtractionResponse(
                title="Over-broad unrelated extraction",
                claim_ids=["applicant_is_parent", "both_parents_consent", "emergency"],
                rule_ids=["allow_joint_consent", "allow_emergency"],
                summary="The extractor guessed a family-law vocabulary anyway.",
            )

        artifact = extract_domain_artifact(
            self.use_case_dir,
            self.unrelated_law_text,
            LogicLevel.PROPOSITIONAL,
            generator=fake_generator,
        )

        self.assertEqual(artifact.claims, [])
        self.assertEqual(artifact.rules, [])

    def test_non_propositional_logic_levels_fail_early(self) -> None:
        with self.assertRaises(ValueError):
            extract_intent_artifact(
                self.use_case_dir,
                self.allow_text,
                LogicLevel.PREDICATE,
                generator=lambda **kwargs: None,
            )

    def test_solver_reports_neutral_domain_blockage(self) -> None:
        base_domain = build_domain_artifact(self.use_case, LogicLevel.PROPOSITIONAL, "Reference law text")
        irrelevant_domain = DomainArtifact(
            logic_level=LogicLevel.PROPOSITIONAL,
            title="Irrelevant law demo",
            law_text="An unrelated law text that does not map to the supported vocabulary.",
            lowered_view_note=base_domain.lowered_view_note,
            allow_outcome_id=base_domain.allow_outcome_id,
            deny_outcome_id=base_domain.deny_outcome_id,
            claims=[],
            outcomes=base_domain.outcomes,
            rules=[],
        )
        intent = build_intent_artifact(
            self.use_case,
            self.allow_text,
            LogicLevel.PROPOSITIONAL,
            {
                "applicant_is_parent": True,
                "applicant_is_not_parent": False,
                "emergency": True,
                "one_parent_unreachable": True,
            },
        )
        bundle = CaseBundle(
            logic_level=LogicLevel.PROPOSITIONAL,
            domain=irrelevant_domain,
            intent=intent,
            mock_db=self.mock_db,
        )

        solution = solve_case_bundle(bundle)
        trace = render_solution_trace(solution)

        self.assertEqual(solution.final_outcome, SolverOutcome.DENY)
        self.assertEqual(solution.blocked_at_step, "domain_extraction")
        self.assertEqual(solution.block_reason_code, BlockReasonCode.DOMAIN_EXTRACTION_EMPTY)
        self.assertEqual(solution.extracted_claim_count, 0)
        self.assertEqual(solution.extracted_rule_count, 0)
        self.assertIn("BLOCKED AT STEP: domain_extraction", trace)
        self.assertIn("BLOCK REASON CODE: domain_extraction_empty", trace)

    def test_trace_includes_metadata_provenance_and_law_grounding(self) -> None:
        intent = build_intent_artifact(
            self.use_case,
            self.allow_text,
            LogicLevel.PROPOSITIONAL,
            {
                "applicant_is_parent": True,
                "applicant_is_not_parent": False,
                "emergency": True,
                "one_parent_unreachable": True,
            },
            reasons={"emergency": "The hospital request makes the case urgent."},
            snippets={"emergency": ["The child is in hospital and the doctor needs a quick decision."]},
            run_metadata=ExtractionRunMetadata(
                generated_at_utc="2026-04-10T10:00:00+00:00",
                model_name="fixture-intent-model",
                source_path=str(FRAMEWORK_ROOT / "examples/section_120_demo/request_allow.txt"),
                prompt=PromptMetadata(
                    system_prompt_path=str(
                        FRAMEWORK_ROOT / "examples/section_120_demo/prompts/intent/system.propositional.txt"
                    ),
                    user_prompt_path=str(FRAMEWORK_ROOT / "examples/section_120_demo/prompts/intent/user.txt"),
                    system_prompt_sha256="intent-system-hash",
                    user_prompt_sha256="intent-user-hash",
                ),
            ),
        )
        domain = build_domain_artifact(
            self.use_case,
            LogicLevel.PROPOSITIONAL,
            self.law_text,
            run_metadata=ExtractionRunMetadata(
                generated_at_utc="2026-04-10T10:01:00+00:00",
                model_name="fixture-domain-model",
                source_path=str(FRAMEWORK_ROOT / "examples/section_120_demo/law.txt"),
                prompt=PromptMetadata(
                    system_prompt_path=str(
                        FRAMEWORK_ROOT / "examples/section_120_demo/prompts/domain/system.propositional.txt"
                    ),
                    user_prompt_path=str(FRAMEWORK_ROOT / "examples/section_120_demo/prompts/domain/user.txt"),
                    system_prompt_sha256="domain-system-hash",
                    user_prompt_sha256="domain-user-hash",
                ),
            ),
        )
        solution = solve_case_bundle(
            CaseBundle(
                logic_level=LogicLevel.PROPOSITIONAL,
                domain=domain,
                intent=intent,
                mock_db=self.mock_db,
            )
        )
        solution.solve_metadata = SolveRunMetadata(
            generated_at_utc="2026-04-10T10:02:00+00:00",
            domain_artifact_path=str(FRAMEWORK_ROOT / "tmp/domain.json"),
            intent_artifact_path=str(FRAMEWORK_ROOT / "tmp/intent.json"),
            mock_db_path=str(FRAMEWORK_ROOT / "examples/section_120_demo/mock_db.json"),
        )
        trace = render_solution_trace(solution)

        self.assertIn("RUN METADATA", trace)
        self.assertIn("fixture-intent-model", trace)
        self.assertIn("INTENT CLAIMS", trace)
        self.assertIn("provenance:", trace)
        self.assertIn("DOMAIN RULES", trace)
        self.assertIn("§ 120(3) Lapse esindamine", trace)
        self.assertIn("law.txt", trace)

    def test_solve_and_trace_cli_infer_logic_level_from_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            domain = build_domain_artifact(self.use_case, LogicLevel.PROPOSITIONAL, self.law_text)
            intent = build_intent_artifact(
                self.use_case,
                self.allow_text,
                LogicLevel.PROPOSITIONAL,
                {
                    "applicant_is_parent": True,
                    "applicant_is_not_parent": False,
                    "emergency": True,
                    "one_parent_unreachable": True,
                },
            )
            domain_path = tmpdir_path / "domain.json"
            intent_path = tmpdir_path / "intent.json"
            solution_path = tmpdir_path / "solution.json"
            domain_path.write_text(domain.model_dump_json(indent=2), encoding="utf-8")
            intent_path.write_text(intent.model_dump_json(indent=2), encoding="utf-8")

            solve_result = subprocess.run(
                [
                    sys.executable,
                    str(FRAMEWORK_ROOT / "03_solve_case.py"),
                    "--domain",
                    str(domain_path),
                    "--intent",
                    str(intent_path),
                    "--db",
                    str(FRAMEWORK_ROOT / "examples/section_120_demo/mock_db.json"),
                    "--out",
                    str(solution_path),
                ],
                cwd=FRAMEWORK_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(solve_result.returncode, 0, solve_result.stderr)

            trace_result = subprocess.run(
                [
                    sys.executable,
                    str(FRAMEWORK_ROOT / "04_print_trace.py"),
                    "--solution",
                    str(solution_path),
                ],
                cwd=FRAMEWORK_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(trace_result.returncode, 0, trace_result.stderr)
            self.assertIn("FINAL OUTCOME: ALLOW", trace_result.stdout)

    def test_scenario_runner_generates_deterministic_review_log(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            out_dir = tmpdir_path / "scenario_suite"
            transcript_path = tmpdir_path / "scenario_suite.txt"
            result = subprocess.run(
                [
                    sys.executable,
                    str(FRAMEWORK_ROOT / "run_scenarios.py"),
                    "--scenario",
                    "allow",
                    "--mode",
                    "deterministic",
                    "--out-dir",
                    str(out_dir),
                    "--transcript-file",
                    str(transcript_path),
                ],
                cwd=FRAMEWORK_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(transcript_path.exists())
            self.assertTrue((out_dir / "allow" / "trace.txt").exists())
            transcript = transcript_path.read_text(encoding="utf-8")
            self.assertIn("SCENARIO: allow", transcript)
            self.assertIn("FINAL OUTCOME: ALLOW", transcript)


def _single_rule_bundle(
    *,
    claim_source: ClaimSource = ClaimSource.DB,
    intent_value: bool | None = None,
    intent_kwargs: dict | None = None,
    rule_kwargs: dict | None = None,
    lookup_sources: list[LookupSource] | None = None,
) -> CaseBundle:
    """Build the minimal domain+intent+DB bundle used by the U1..U12 tests.

    One allow rule fires when the single claim ``fact`` is true. Callers
    can mark the claim source (for U1/U10), add intent-level flags (for
    U6/U11/U12), toggle rule-level flags (for U2/U4/U9), and inject
    uncertainty-aware lookup sources (for U3/U7).
    """
    intent_kwargs = intent_kwargs or {}
    rule_kwargs = rule_kwargs or {}
    domain = DomainArtifact(
        logic_level=LogicLevel.PROPOSITIONAL,
        title="Uncertainty fixture",
        law_text="Fixture law text.",
        allow_outcome_id="ALLOW",
        deny_outcome_id="DENY",
        claims=[
            DomainClaim(
                claim_id="fact",
                lowered_atom="fact",
                label="fact",
                description="",
                source_type=claim_source,
                formal_text="fact",
            )
        ],
        outcomes=[
            OutcomeDefinition(outcome_id="ALLOW", lowered_atom="ALLOW", label="ALLOW", formal_text="ALLOW"),
            OutcomeDefinition(outcome_id="DENY", lowered_atom="DENY", label="DENY", formal_text="DENY"),
        ],
        rules=[
            DomainRule(
                rule_id="allow_rule",
                kind=RuleKind.ALLOW_IF_ALL,
                label="allow_rule",
                when_claim_ids=["fact"],
                formal_text="fact -> ALLOW",
                lowered_formula="fact -> ALLOW",
                target_outcome_id="ALLOW",
                **rule_kwargs,
            )
        ],
    )
    intent = IntentArtifact(
        logic_level=LogicLevel.PROPOSITIONAL,
        request_text="fixture request",
        claims=[
            IntentClaim(
                claim_id="fact",
                lowered_atom="fact",
                label="fact",
                description="",
                source_type=claim_source,
                formal_text="fact",
                value=intent_value,
                **intent_kwargs,
            )
        ],
    )
    mock_db = MockDbArtifact(sources=lookup_sources or [])
    return CaseBundle(
        logic_level=LogicLevel.PROPOSITIONAL,
        domain=domain,
        intent=intent,
        mock_db=mock_db,
    )


class TestUncertaintyTaxonomyEndToEnd(unittest.TestCase):
    """One test per U-code, asserting the solver emits the expected pair."""

    def _solve(self, bundle: CaseBundle):
        return solve_case_bundle(bundle)

    def test_u1_statute_underspecified(self) -> None:
        bundle = _single_rule_bundle(claim_source=ClaimSource.STATUTE_OPEN)
        solution = self._solve(bundle)
        self.assertEqual(solution.final_outcome, SolverOutcome.UNDETERMINED_INTERPRETATION)
        self.assertEqual(solution.block_reason_code, BlockReasonCode.STATUTE_UNDERSPECIFIED)

    def test_u2_interpretation_ambiguous(self) -> None:
        bundle = _single_rule_bundle(
            claim_source=ClaimSource.USER,
            rule_kwargs={"interpretation_ambiguous": True},
        )
        solution = self._solve(bundle)
        self.assertEqual(solution.final_outcome, SolverOutcome.UNDETERMINED_INTERPRETATION)
        self.assertEqual(solution.block_reason_code, BlockReasonCode.INTERPRETATION_AMBIGUOUS)

    def test_u3_no_register(self) -> None:
        unavailable = LookupSource(
            source_id="offline_registry",
            label="Offline registry",
            description="Covers `fact` but is currently unavailable.",
            values={"fact": True},
            availability="unavailable",
        )
        bundle = _single_rule_bundle(lookup_sources=[unavailable])
        solution = self._solve(bundle)
        self.assertEqual(solution.final_outcome, SolverOutcome.UNVERIFIABLE_CLAIM)
        self.assertEqual(solution.block_reason_code, BlockReasonCode.NO_REGISTER)

    def test_u4_process_indeterminate(self) -> None:
        bundle = _single_rule_bundle(
            claim_source=ClaimSource.USER,
            rule_kwargs={"process_indeterminate": True},
        )
        solution = self._solve(bundle)
        self.assertEqual(solution.final_outcome, SolverOutcome.UNDETERMINED_INTERPRETATION)
        self.assertEqual(solution.block_reason_code, BlockReasonCode.PROCESS_INDETERMINATE)

    def test_u5_needs_db_info(self) -> None:
        bundle = _single_rule_bundle(claim_source=ClaimSource.DB)
        solution = self._solve(bundle)
        self.assertEqual(solution.final_outcome, SolverOutcome.NEED_DB_INFO)
        self.assertEqual(solution.block_reason_code, BlockReasonCode.NEEDS_DB_INFO)

    def test_u6_subjective_party(self) -> None:
        bundle = _single_rule_bundle(
            claim_source=ClaimSource.USER,
            intent_kwargs={"subjective_party": True},
        )
        solution = self._solve(bundle)
        self.assertEqual(solution.final_outcome, SolverOutcome.UNVERIFIABLE_CLAIM)
        self.assertEqual(solution.block_reason_code, BlockReasonCode.SUBJECTIVE_PARTY)

    def test_u7_trust_only(self) -> None:
        trust_only_source = LookupSource(
            source_id="applicant_statement",
            label="Applicant statement",
            description="Accepts the applicant's word as authoritative.",
            values={"fact": True},
            trust_only=True,
        )
        bundle = _single_rule_bundle(lookup_sources=[trust_only_source])
        solution = self._solve(bundle)
        self.assertEqual(solution.final_outcome, SolverOutcome.UNVERIFIABLE_CLAIM)
        self.assertEqual(solution.block_reason_code, BlockReasonCode.TRUST_ONLY)

    def test_u8_needs_user_info(self) -> None:
        bundle = _single_rule_bundle(claim_source=ClaimSource.USER)
        solution = self._solve(bundle)
        self.assertEqual(solution.final_outcome, SolverOutcome.NEED_USER_INFO)
        self.assertEqual(solution.block_reason_code, BlockReasonCode.NEEDS_USER_INFO)

    def test_u9_context_dependent(self) -> None:
        bundle = _single_rule_bundle(
            claim_source=ClaimSource.USER,
            rule_kwargs={"context_dependent": True},
        )
        solution = self._solve(bundle)
        self.assertEqual(solution.final_outcome, SolverOutcome.NEED_USER_INFO)
        self.assertEqual(solution.block_reason_code, BlockReasonCode.CONTEXT_DEPENDENT)

    def test_u10_expert_judgment(self) -> None:
        bundle = _single_rule_bundle(claim_source=ClaimSource.EXPERT)
        solution = self._solve(bundle)
        self.assertEqual(solution.final_outcome, SolverOutcome.NEED_EXPERT_JUDGMENT)
        self.assertEqual(solution.block_reason_code, BlockReasonCode.EXPERT_JUDGMENT_REQUIRED)

    def test_u11_glossary_low_confidence(self) -> None:
        bundle = _single_rule_bundle(
            claim_source=ClaimSource.USER,
            intent_kwargs={"glossary_low_confidence": True},
        )
        solution = self._solve(bundle)
        self.assertEqual(solution.final_outcome, SolverOutcome.UNDETERMINED_INTERPRETATION)
        self.assertEqual(solution.block_reason_code, BlockReasonCode.GLOSSARY_LOW_CONFIDENCE)

    def test_u12_model_drift(self) -> None:
        bundle = _single_rule_bundle(
            claim_source=ClaimSource.USER,
            intent_kwargs={"model_drift": True},
        )
        solution = self._solve(bundle)
        self.assertEqual(solution.final_outcome, SolverOutcome.UNDETERMINED_INTERPRETATION)
        self.assertEqual(solution.block_reason_code, BlockReasonCode.MODEL_DRIFT)

    def test_trace_renders_uncertainty_code_inline(self) -> None:
        bundle = _single_rule_bundle(claim_source=ClaimSource.STATUTE_OPEN)
        solution = self._solve(bundle)
        trace = render_solution_trace(solution)
        self.assertIn("[U1:statute_underspecified]", trace)


if __name__ == "__main__":
    unittest.main()
