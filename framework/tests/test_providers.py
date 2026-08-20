"""Unit tests for multi-provider adapters, prices, and the EUR budget guard."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

FRAMEWORK_ROOT = Path(__file__).resolve().parents[1]
if str(FRAMEWORK_ROOT) not in sys.path:
    sys.path.insert(0, str(FRAMEWORK_ROOT))

from experiments.budget import BudgetExceeded, BudgetGuard, USD_TO_EUR, usd_to_eur  # noqa: E402
from experiments.ledger import (  # noqa: E402
    append_ledger,
    estimate_usd,
    estimate_worst_case_usd,
    lookup_price,
)
from providers import (  # noqa: E402
    Usage,
    get_provider,
    list_available_providers,
)
from pydantic import BaseModel  # noqa: E402

_CLEARED_KEYS = {
    "GEMINI_API_KEY": "",
    "GOOGLE_API_KEY": "",
    "OPENAI_API_KEY": "",
    "ANTHROPIC_API_KEY": "",
    "DEEPSEEK_API_KEY": "",
}


class _Probe(BaseModel):
    ok: bool
    label: str = "x"


def _complete(name: str) -> object:
    return get_provider(name).complete(
        system="sys",
        user="user",
        response_model=_Probe,
    )


class TestProvidersSkipped(unittest.TestCase):
    def test_missing_keys_are_unavailable_and_skip_complete(self) -> None:
        with patch.dict(os.environ, _CLEARED_KEYS, clear=False):
            for name in ("gemini", "openai", "anthropic", "deepseek"):
                provider = get_provider(name)
                self.assertFalse(provider.available(), name)
                with patch(f"providers._{name}_client") as factory:
                    result = provider.complete(
                        system="s",
                        user="u",
                        response_model=_Probe,
                    )
                factory.assert_not_called()
                self.assertTrue(result.skipped, name)
                self.assertIn("missing", result.skip_reason)

    def test_list_available_empty_without_keys(self) -> None:
        with patch.dict(os.environ, _CLEARED_KEYS, clear=False):
            self.assertEqual(list_available_providers(), [])

    def test_unknown_provider_raises(self) -> None:
        with self.assertRaises(ValueError):
            get_provider("not-a-vendor")

    def test_ollama_is_stubbed(self) -> None:
        provider = get_provider("ollama")
        self.assertFalse(provider.available())
        result = provider.complete(system="s", user="u", response_model=_Probe)
        self.assertTrue(result.skipped)
        self.assertEqual(result.skip_reason, "ollama stub")


class TestProviderMocks(unittest.TestCase):
    def test_gemini_parses_json_and_usage_metadata(self) -> None:
        client = MagicMock()
        client.models.generate_content.return_value = SimpleNamespace(
            text='{"ok": true, "label": "g"}',
            usage_metadata=SimpleNamespace(
                prompt_token_count=11,
                candidates_token_count=7,
                cached_content_token_count=2,
            ),
        )
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            with patch("providers._gemini_client", return_value=client):
                result = _complete("gemini")
        self.assertFalse(result.skipped)
        self.assertTrue(result.parsed.ok)
        self.assertEqual(result.parsed.label, "g")
        self.assertEqual(result.usage.input_tokens, 11)
        self.assertEqual(result.usage.output_tokens, 7)
        self.assertEqual(result.provider, "gemini")
        client.models.generate_content.assert_called_once()

    def test_openai_responses_json_schema_path(self) -> None:
        client = MagicMock()
        client.responses.create.return_value = SimpleNamespace(
            output_text='{"ok": true, "label": "o"}',
            usage=SimpleNamespace(
                input_tokens=3,
                output_tokens=4,
                input_tokens_details=SimpleNamespace(cached_tokens=1),
            ),
        )
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            with patch("providers._openai_client", return_value=client):
                result = _complete("openai")
        self.assertEqual(result.parsed.label, "o")
        self.assertEqual(result.usage.input_tokens, 3)
        self.assertEqual(result.usage.cached_input_tokens, 1)
        kwargs = client.responses.create.call_args.kwargs
        self.assertEqual(kwargs["text"]["format"]["type"], "json_schema")
        self.assertTrue(kwargs["text"]["format"]["strict"])
        self.assertNotIn("temperature", kwargs)

    def test_anthropic_output_config_path(self) -> None:
        client = MagicMock()
        client.messages.create.return_value = SimpleNamespace(
            content=[SimpleNamespace(type="text", text='{"ok": true, "label": "a"}')],
            usage=SimpleNamespace(input_tokens=9, output_tokens=6, cache_read_input_tokens=0),
        )
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            with patch("providers._anthropic_client", return_value=client):
                result = _complete("anthropic")
        self.assertEqual(result.parsed.label, "a")
        self.assertEqual(result.usage.output_tokens, 6)
        kwargs = client.messages.create.call_args.kwargs
        self.assertEqual(kwargs["output_config"]["format"]["type"], "json_schema")

    def test_anthropic_falls_back_when_output_config_rejected(self) -> None:
        client = MagicMock()

        def _create(**kwargs):
            if "output_config" in kwargs:
                raise TypeError("messages.create() got an unexpected keyword argument 'output_config'")
            return SimpleNamespace(
                content=[
                    SimpleNamespace(
                        type="tool_use",
                        input={"ok": True, "label": "tool"},
                    )
                ],
                usage=SimpleNamespace(input_tokens=1, output_tokens=2, cache_read_input_tokens=0),
            )

        client.messages.create.side_effect = lambda **kwargs: _create(**kwargs)
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            with patch("providers._anthropic_client", return_value=client):
                result = _complete("anthropic")
        self.assertEqual(result.parsed.label, "tool")
        self.assertEqual(client.messages.create.call_count, 2)
        fallback_kwargs = client.messages.create.call_args.kwargs
        self.assertEqual(fallback_kwargs["tool_choice"]["name"], "emit_structured_json")

    def test_deepseek_json_mode_and_disabled_thinking(self) -> None:
        client = MagicMock()
        client.chat.completions.create.return_value = SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content='{"ok": true, "label": "d"}'))],
            usage=SimpleNamespace(prompt_tokens=8, completion_tokens=5),
        )
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test-key"}):
            with patch("providers._deepseek_client", return_value=client):
                result = _complete("deepseek")
        self.assertEqual(result.parsed.label, "d")
        self.assertEqual(result.usage.input_tokens, 8)
        self.assertEqual(result.usage.output_tokens, 5)
        kwargs = client.chat.completions.create.call_args.kwargs
        self.assertEqual(kwargs["response_format"], {"type": "json_object"})
        self.assertEqual(kwargs["extra_body"], {"thinking": {"type": "disabled"}})
        combined = kwargs["messages"][0]["content"].lower()
        self.assertIn("json", combined)


class TestPricesAndLedger(unittest.TestCase):
    def test_repo_price_lookup(self) -> None:
        flash = lookup_price("gemini-2.5-flash")
        self.assertEqual(flash["input_usd_per_million"], 0.30)
        self.assertEqual(flash["output_usd_per_million"], 2.50)
        usd = estimate_usd("gemini-2.5-flash", Usage(input_tokens=1_000_000, output_tokens=1_000_000))
        self.assertAlmostEqual(usd, 2.80, places=6)
        alias = lookup_price("gpt-5-mini-2025-08-07")
        self.assertEqual(alias["input_usd_per_million"], 0.25)
        self.assertIn("api-docs.deepseek.com", lookup_price("deepseek-v4-flash")["source"])

    def test_unknown_model_price_raises(self) -> None:
        with self.assertRaises(ValueError):
            lookup_price("not-a-model")

    def test_worst_case_estimate_positive(self) -> None:
        usd = estimate_worst_case_usd("gpt-5-mini")
        self.assertGreater(usd, 0.0)

    def test_append_ledger_writes_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.jsonl"
            row = append_ledger(
                provider="gemini",
                model="gemini-2.5-flash",
                experiment="smoke",
                scenario="allow",
                input_tokens=100,
                output_tokens=20,
                usd=0.01,
                path=path,
            )
            lines = path.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(lines), 1)
            loaded = json.loads(lines[0])
            self.assertEqual(loaded["provider"], "gemini")
            self.assertEqual(loaded["eur"], usd_to_eur(0.01))
            self.assertEqual(row["scenario"], "allow")


class TestBudgetGuard(unittest.TestCase):
    def test_usd_to_eur_constant(self) -> None:
        self.assertEqual(USD_TO_EUR, 0.92)
        self.assertAlmostEqual(usd_to_eur(1.0), 0.92, places=6)

    def test_check_or_raise_blocks_when_estimate_exceeds_remaining(self) -> None:
        guard = BudgetGuard(cap_eur=1.0)
        guard.check_or_raise(0.5)
        with self.assertRaises(BudgetExceeded):
            guard.check_or_raise(1.5)

    def test_record_usd_halts_after_cap(self) -> None:
        guard = BudgetGuard(cap_eur=1.0)
        guard.record_usd(0.5)  # 0.46 EUR
        self.assertGreater(guard.remaining(), 0)
        with self.assertRaises(BudgetExceeded):
            guard.record_usd(1.0)  # +0.92 EUR → 1.38 > 1.0
        self.assertLess(guard.remaining(), 0)

    def test_zero_remaining_refuses_next_call(self) -> None:
        guard = BudgetGuard(cap_eur=0.92)
        guard.record_usd(1.0)
        self.assertEqual(guard.remaining(), 0.0)
        with self.assertRaises(BudgetExceeded):
            guard.check_or_raise(0.0)

    def test_ingest_ledger_counts_prior_spend(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.jsonl"
            append_ledger(
                provider="openai",
                model="gpt-5-mini",
                experiment="smoke",
                scenario="deny",
                input_tokens=1,
                output_tokens=1,
                usd=1.0,
                path=path,
            )
            guard = BudgetGuard(cap_eur=2.0)
            guard.ingest_ledger(path)
            self.assertAlmostEqual(guard.spent_eur, 0.92, places=6)

    def test_default_cap_from_env(self) -> None:
        with patch.dict(os.environ, {"FRAMEWORK_BUDGET_EUR": "7.5"}):
            guard = BudgetGuard()
            self.assertEqual(guard.cap_eur, 7.5)


if __name__ == "__main__":
    unittest.main()
