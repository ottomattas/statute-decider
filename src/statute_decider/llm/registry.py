"""Model registry: friendly model ids -> provider + API model + prices."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class ModelSpec:
    model_id: str
    provider: str  # google | openai | anthropic | deepseek
    api_model: str
    tier: str = ""
    input_usd_per_million: float = 0.0
    output_usd_per_million: float = 0.0
    # Prompt-cache rates. When absent (0.0) the ledger prices cache hits and
    # writes at the plain input rate — the pre-3 Sep behaviour, an overestimate.
    cached_input_usd_per_million: float = 0.0
    cache_write_usd_per_million: float = 0.0

    def eur(
        self,
        input_tokens: int,
        output_tokens: int,
        usd_to_eur: float,
        cached_input_tokens: int = 0,
        cache_write_input_tokens: int = 0,
    ) -> float:
        """Cost of one call. ``input_tokens`` is the vendor's full prompt count;
        cached and cache-write tokens are priced at their own rates and the
        remainder at the plain input rate."""
        cached_rate = self.cached_input_usd_per_million or self.input_usd_per_million
        write_rate = self.cache_write_usd_per_million or self.input_usd_per_million
        cached = min(cached_input_tokens, input_tokens)
        written = min(cache_write_input_tokens, input_tokens - cached)
        plain = input_tokens - cached - written
        usd = (
            plain / 1_000_000 * self.input_usd_per_million
            + cached / 1_000_000 * cached_rate
            + written / 1_000_000 * write_rate
            + output_tokens / 1_000_000 * self.output_usd_per_million
        )
        return usd * usd_to_eur


class ModelRegistry:
    def __init__(self, models_path: Path | str, prices_path: Path | str | None = None) -> None:
        models_raw = yaml.safe_load(Path(models_path).read_text(encoding="utf-8"))
        prices_raw: dict = {}
        if prices_path is not None and Path(prices_path).exists():
            prices_raw = yaml.safe_load(Path(prices_path).read_text(encoding="utf-8")) or {}
        self.usd_to_eur: float = float(prices_raw.get("usd_to_eur", 0.92))
        price_models: dict = prices_raw.get("models", {})
        self._specs: dict[str, ModelSpec] = {}
        for model_id, spec in (models_raw.get("models") or {}).items():
            prices = price_models.get(model_id, {})
            self._specs[model_id] = ModelSpec(
                model_id=model_id,
                provider=spec["provider"],
                api_model=spec.get("api_model", model_id),
                tier=spec.get("tier", ""),
                input_usd_per_million=float(prices.get("input_usd_per_million", 0.0)),
                output_usd_per_million=float(prices.get("output_usd_per_million", 0.0)),
                cached_input_usd_per_million=float(prices.get("cached_input_usd_per_million", 0.0)),
                cache_write_usd_per_million=float(prices.get("cache_write_usd_per_million", 0.0)),
            )

    def model_ids(self, tier: str | None = None) -> list[str]:
        if tier is None:
            return sorted(self._specs)
        return sorted(mid for mid, s in self._specs.items() if s.tier == tier)

    def spec(self, model_id: str) -> ModelSpec:
        try:
            return self._specs[model_id]
        except KeyError as exc:
            raise ValueError(
                f"Unknown model {model_id!r}. Known: {sorted(self._specs)}"
            ) from exc

    def resolve(self, requested: list[str]) -> list[ModelSpec]:
        """Resolve CLI/experiment model selections; 'all' means every registered model."""
        if any(item == "all" for item in requested):
            return [self._specs[mid] for mid in self.model_ids()]
        return [self.spec(mid) for mid in requested]
