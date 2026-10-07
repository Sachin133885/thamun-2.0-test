# Alert frequency and policy ablation

Simulation result — not real customer data.

Offline friction proxy. No behavior assumptions, user research, coaching nudges or historical report effects included. Not a full deployed-policy replay.

| Policy | Pause rate | Synthetic fraud coverage | Legitimate false-pause rate |
|---|---|---|---|
| Generic: pause every new-recipient payment | 0.1103 | 0.6667 | 0.1070 |
| Model only | 0.0048 | 0.5556 | 0.0015 |
| Purpose rules only (idealized) | 0.0033 | 0.5556 | 0.0000 |
| Model + purpose rules, materiality policy | 0.0061 | 0.7778 | 0.0015 |

Denominators: all test attempts for pause rate, scam-labeled attempts for coverage, legitimate-labeled attempts for false pauses. No user continuation, cancellation or monetary loss avoided is estimated. Lower warning frequency does not establish reduced human alert fatigue.
