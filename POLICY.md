# My dispatch policy

Fill in this template yourself before asking the builders to implement it. Short bullets and a small table are enough. You may discuss ideas or ask AI to challenge them, but make and explain your own choices.

## Priorities

- What I prioritise:

1. Avoid adding stops for people already aboard.
2. Use a car that is already travelling past the caller instead of activating a second car.
3. If neither applies, shorten the pickup distance for the caller. People already aboard come first: they have already started their journey, and every added stop delays all of them.

- My exact selection rule: (applied only to the IDs returned by rules.eligible_ids):

1. No eligible car → Decision(None, reason) (WAIT).
2. Rule 1 – Stop already scheduled: if any eligible moving car already has the caller's floor in its stops, choose from those cars. No stop is added.
3. Rule 2 – Light passing car: otherwise, if any eligible moving car has load_kg <= 130, choose from those cars. One added stop delays only a few riders, and the idle car stays parked.
4. Rule 3 – Nearest car: otherwise, choose from all eligible cars.
   The first rule whose group is non-empty decides. Later rules are not checked.

- My deterministic tie-breaker: smallest floor distance abs, then lower load_kg, then alphabetical ID.
- A tradeoff I accept: the caller may wait for a car that is farther away so that a second car stays parked. Above 130 kg I do the opposite: I activate the idle car so that about five riders are not delayed by an extra stop.
- Proxies: floor distance isn’t waiting time, keeping B parked isn’t proven energy saving, load/65 is only an occupancy estimate, and 130 kg is my judgement call.

## Predictions before implementation

Use S1, one of S2/S3, and one valid scenario you create in scenarios.py. For your own case, change something meaningful: location, direction, load or scheduled stops. Name it S6.

| Scenario        | My expected selection | Why it follows my policy                                                                                                                                                              | Benefit and cost / who is affected                                                                                                                                                             |
| --------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| S1              | A                     | Both are eligible. A has no stop at 5. A is moving with 130 kg ≤ 130, so Rule 2 selects A                                                                                             | Benefit: B stays idle, and A's existing trip is reused. Cost: about 2 riders in A get one extra stop, and the caller waits for A to travel 3 floors instead of B's 1.                          |
| S2              | B                     | A is eligible, but at 325 kg it fails Rule 2. Rule 3 picks the nearest car: B is at distance 1, A at distance 3.                                                                      | Benefit: about 5 riders are not delayed, and the caller gets the nearer car. Cost: a second car is activated.                                                                                  |
| S3              | A                     | A already stops at floor 5, so Rule 1 selects A.                                                                                                                                      | Benefit: no added stop and no second car activated. Cost: the caller waits for A from 3 floors away instead of 1. Boarding still takes some time.                                              |
| S6: my scenario | A                     | A at floor 8 is moving down with 65 kg and a stop at 1. B is idle at floor 5, right where the caller is. A is eligible and light, so Rule 2 selects A even though B is 0 floors away. | Benefit: B stays parked, and only about 1 rider gets an extra stop. Cost: the caller waits for a car 3 floors away when one is already at their floor. This is the sharpest cost of my policy. |

## Another defensible policy

- An alternative priority: "Nearest car first." Choose the eligible car with the smallest floor distance. This prioritises the caller's pickup distance over reusing existing journeys.
- A scenario where it could choose differently, and why: In S1 and S6 it picks B, so the caller gets a closer car and A's riders get no extra stop. The cost is that the second car is activated every time. In S3 it would also pick B, adding a car trip even though A was stopping at floor 5 anyway.

If your predicted choices contradict your general rule, resolve that before implementation. If review later changes your mind, note the revision in EVIDENCE.md and update the policy and code together.
