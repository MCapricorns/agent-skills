# Tests That Catch Breaks

Name the production break and exercise the smallest real boundary that owns it. Derive expectations independently of production helpers. Source-text and private-structure assertions are change detectors unless that representation is the contract; exact bytes or messages are valid when promised.

A new or changed test must fail for the intended break, not setup. Never weaken a meaningful assertion to pass.

Mock at the external or slow boundary and model its failures. Combine generated properties with known examples or an independent oracle; matching encoder/decoder bugs survive a naive round trip. Control time, randomness, and resources; wait for an observable condition instead of sleeping a flake away.
