# Responsible AI and privacy

The risk classifier, anomaly model and versioned policy decide. The optional LLM only rephrases grounded explanations or answers coaching questions; it cannot mutate scores, severity, payment state or policy.

Fixed English/Bangla templates work without an LLM. Numeric integrity rejects changed or invented values and links. A conservative extra guard rejects explicit English/Bangla safety reversals in PAUSE explanations. This heuristic is not full semantic verification; malicious or incorrect paraphrases can evade it. Original rule reasons and advice remain visible. Sensitive production warnings should use approved templates until stronger semantic validation exists.

Human control: PAUSE requires explicit acknowledgement before simulated authorization; customers can cancel or continue. Reports are unverified signals, not proof that a recipient is malicious. Newness alone is not evidence of fraud. No-report and low-risk states do not mean guaranteed safety. Customers must not be shamed.

All customer histories, model labels, report seeds and payments are synthetic. Public Bangladesh evidence has separate provenance and does not validate the trained model. Oversampled injected scams distort apparent precision, and simulator-rule recovery can be optimistic. Known-recipient impersonation can be missed. Persona comparisons are descriptive synthetic checks, not proof of demographic fairness.

External LLMs are disabled by default (`LLM_DATA_RESIDENCY=internal_only`). `allow_external` is for synthetic demonstrations only. Private-address/host checks identify routing configuration, not the actual geographic location or compliance of hosting. Production should minimize collection and use encrypted storage, access controls and vetted private/internal model hosting. Bangladesh residency is a design requirement to review with the provider and applicable law, not a verified legal-compliance claim.

The current prototype is not connected to a wallet. It cannot intercept credential theft or payments made outside its own simulated flow. Real deployment needs wallet-provider authorization, representative data, prospective testing, oversight, incident response, model drift review and privacy/legal assessment.
