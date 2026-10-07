# Synthetic data card

Generator: `data/generate.py`; assumptions/personas: `data/personas.py` and `docs/data_assumptions.md`. Default seed 42. April–September 2026 transactions include incoming/outgoing flows, categories, balance context, repeated contacts, bills, spending changes and injected scam patterns. Four separate demo customer histories continue into a simulated October date.

Default generated evaluation run: 200 synthetic customers and 113445 transactions; 57564 outgoing records include 332 scam-labeled records. These are generated counts, not national statistics. Exact split counts and transaction-file SHA-256 are recorded in `evidence/evaluation/benchmarks.json`.

Fraud labels come from injected scenarios (refund, prize, fake agent, account takeover, impersonation), not real investigation. Purpose fields are synthetic known intents, not automatically observable truths. Report seeds are distinct from public incident evidence and from the historical ML dataset. No fabricated timestamped scam-report labels were added for ablation.

Historical features are calculated in timestamp order before updating customer state. Development: April–July fit, August validation, September final temporal test. Thresholds never use September outcomes. Historical scam transactions affect later history in the offline replay; the replay does not simulate changing future behavior after cancellation.

Oversampled scams, scripted amounts, plausible but assumed income/spending distributions, simplified personas, truthful purpose and simulator-specific categories can overstate performance. There is no claim of representative Bangladesh demographics, realistic scam prevalence, real user behavior or causal prevention. No national extrapolation should be made.

The ZIP includes small synthetic demo histories and trained demo artifacts, not the large regenerable transaction/features tables. Reproduce using `python -m data.generate`, `python -m ml.train`, `python -m ml.evaluate`, and `python -m ml.benchmark`. Do not deserialize model pickle files from untrusted sources.
