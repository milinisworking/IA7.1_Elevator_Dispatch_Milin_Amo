# My agent plan

Fill in the brackets before delegation. This is a template, not a completed plan.

- Dispatcher builder owns dispatcher.py: Implement choose_elevator exactly as POLICY.md says: call rules.eligible_ids, return WAIT if the list is empty, then apply Rule 1 (moving car with the caller's floor in stops), Rule 2 (moving car with load_kg <= 130) and Rule 3 (all eligible), in that order. Apply the tie-breaker. The reason must name the rule that fired, with distance and estimated riders. Do not mutate inputs.
- Display builder owns app.py: Implement run_scenarios per SPEC.md R4/R5. For each scenario, print its name, both elevators' floor, direction, load and stops, and the request. Call choose_elevator exactly once, print Selected: A/B/WAIT and the reason, and return the list of decisions ([] for empty input). No selection logic.
- Reviewer is read-only after both outputs are integrated: Check SPEC rules R1–R5, check that the code follows my rule order, threshold and tie-breaker, and check S1/S3/S6 against my predictions. Examine one tradeoff.
- Handoff steps: Commit the starter, POLICY.md, PLAN.md and S6 first. Open elevator_lab in VS Code and give each builder AGENTS.md, SPEC.md, POLICY.md, PLAN.md and all the Python files, plus the Python command py -3.13. Builders edit only their own file in this folder. I inspect the Source Control diff, run the tests and app, then start the reviewer in a fresh session.
- Final check: Run py -3.13 -m unittest -v and py -3.13 app.py. Copy the actual selection and reason for S1, S2/S3 and S6 into EVIDENCE.md next to my predictions. Investigate any mismatch before changing anything.
