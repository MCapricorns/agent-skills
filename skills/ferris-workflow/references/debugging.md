# Debugging

Capture the failing command, input, relevant error, and expected result. Find the smallest reliable repro. An obvious local defect needs no investigation tour; an unreliable repro needs evidence, not a guessed patch.

Trace to the first violated contract. Prove the symptom on unfixed code and the fix with a regression. A retry or timeout that only hides the symptom is mitigation, not a root-cause fix.

Do not dump credentials, tokens, connection strings, or environment values.

Sleeps and stress runs cannot prove race freedom. Never weaken a meaningful check to go green.
