# u7 disclosure probe — trust-only facts disclosed to the LLM-only baseline

Generated 2026-08-28T07:08:00+00:00 by `experiments/u7_disclosure_probe.py`. Five
`*_u7_trust_only` scenarios × 4 cheap models × 1 repeat, disclosure variant
of `llm_baseline` (trust-only facts moved to an UNVERIFIED ASSERTIONS prompt
section; one system-prompt paragraph added; missing-fact filter widened to
accept disclosed ids). Baseline comparison: 0/200 correct on these scenarios
in the 25 Aug run.

| model | correct outcome | mean MF precision | mean MF recall |
|---|---|---|---|
| claude-haiku-4-5-20251001 | 2/5 | 1.000 | 0.120 |
| deepseek-v4-flash | 2/5 | 1.000 | 0.080 |
| gemini-2.5-flash | 1/3 | 1.000 | 0.133 |
| gpt-5-mini | 4/5 | 1.000 | 0.420 |

## Per-row outcomes

| model | scenario | outcome | missing facts |
|---|---|---|---|
| gemini-2.5-flash | building_permit_u7_trust_only | ERROR | ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}} |
| gemini-2.5-flash | civil_service_u7_trust_only | NEED_MORE_INFO | ee_citizen, full_capacity |
| gemini-2.5-flash | consumer_withdrawal_u7_trust_only | ERROR | ServerError: 504 DEADLINE_EXCEEDED. {'error': {'code': 504, 'message': 'Stream cancelled; RPC from prefill servable to decode servable failed; Failed to close the streaming context; status = CANCELLED: Stream cancelled; RPC from prefill servable to decode servable failed [type.googleapis.com/util.ErrorSpacePayload=\'RPC::CANCELLED\']\n=== Source Location Trace: ===\nnet/rpc/rpc-errorspace-util.cc:19\nlearning/serving/servables/wiz/remote_wiz_servable.cc:231\nlearning/serving/servables/wiz/prefill_remote_wiz_servable.cc:223\nlearning/serving/servables/wiz/wiz_servable.cc:3484\n;  Failed to run inference for model: go/debugonly  \nname: "prod-common-global__/aistudio/gemini-v3p1s-rev19-calmriver-sc__main__/aistudio/gemini-v3p1s-rev19-calmriver-sc__2025112500__prefill__variantvlp__556b6a7d-5a2c-4482-9b88-c274ee28dc34"\nversion {\n  value: 1\n}\nsignature_name: "serving_stream"\n', 'status': 'DEADLINE_EXCEEDED'}} |
| gemini-2.5-flash | land_tax_u7_trust_only | DENY | — |
| gemini-2.5-flash | journalism_u7_trust_only | ALLOW | — |
| gpt-5-mini | building_permit_u7_trust_only | NEED_MORE_INFO | competent_designer |
| gpt-5-mini | civil_service_u7_trust_only | NEED_MORE_INFO | ee_citizen, full_capacity |
| gpt-5-mini | consumer_withdrawal_u7_trust_only | NEED_MORE_INFO | is_consumer, distance_contract |
| gpt-5-mini | land_tax_u7_trust_only | DENY | — |
| gpt-5-mini | journalism_u7_trust_only | NEED_MORE_INFO | journalistic_purpose |
| claude-haiku-4-5-20251001 | building_permit_u7_trust_only | NEED_MORE_INFO | competent_designer |
| claude-haiku-4-5-20251001 | civil_service_u7_trust_only | NEED_MORE_INFO | ee_citizen, full_capacity |
| claude-haiku-4-5-20251001 | consumer_withdrawal_u7_trust_only | ALLOW | — |
| claude-haiku-4-5-20251001 | land_tax_u7_trust_only | DENY | — |
| claude-haiku-4-5-20251001 | journalism_u7_trust_only | ALLOW | — |
| deepseek-v4-flash | building_permit_u7_trust_only | ALLOW | — |
| deepseek-v4-flash | civil_service_u7_trust_only | NEED_MORE_INFO | ee_citizen, full_capacity |
| deepseek-v4-flash | consumer_withdrawal_u7_trust_only | ALLOW | — |
| deepseek-v4-flash | land_tax_u7_trust_only | NEED_MORE_INFO | — |
| deepseek-v4-flash | journalism_u7_trust_only | ALLOW | — |
