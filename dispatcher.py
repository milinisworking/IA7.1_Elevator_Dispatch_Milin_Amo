"""Builder 1 implements the student's policy here."""
from models import Elevator, Request, Decision
from rules import eligible_ids, ASSUMED_PASSENGER_KG

LIGHT_LOAD_KG = 130  # POLICY.md Rule 2 threshold (student's judgement call)


def _distance(elevator: Elevator, request: Request) -> int:
    return abs(elevator.floor - request.floor)


def _tie_key(elevator: Elevator, request: Request) -> tuple[int, int, str]:
    # POLICY.md tie-breaker: smallest floor distance, then lower load_kg, then alphabetical ID.
    return (_distance(elevator, request), elevator.load_kg, elevator.id)


def _riders(elevator: Elevator) -> str:
    estimate = elevator.load_kg / ASSUMED_PASSENGER_KG
    return f"about {estimate:.1f} riders estimated ({elevator.load_kg} kg / {ASSUMED_PASSENGER_KG} kg)"


def choose_elevator(elevators: tuple[Elevator, Elevator], request: Request) -> Decision:
    """Choose one eligible elevator according to POLICY.md; never mutate inputs."""
    allowed = eligible_ids(elevators, request)
    eligible = [e for e in elevators if e.id in allowed]

    if not eligible:
        return Decision(
            None,
            f"No elevator is eligible for the {request.direction} call at floor {request.floor} "
            "(each car is full, or moving the wrong way / not passing this floor); defer the assignment.",
        )

    moving = [e for e in eligible if e.direction != "idle"]
    rule1 = [e for e in moving if request.floor in e.stops]
    rule2 = [e for e in moving if e.load_kg <= LIGHT_LOAD_KG]

    if rule1:
        group, rule = rule1, 1
    elif rule2:
        group, rule = rule2, 2
    else:
        group, rule = eligible, 3

    chosen = min(group, key=lambda e: _tie_key(e, request))
    dist = _distance(chosen, request)
    floors = "floor" if dist == 1 else "floors"
    pickup = f"{chosen.id} is {dist} {floors} from the caller at floor {request.floor}"
    riders = _riders(chosen)
    tie_note = " Tie-breaker among them: smallest pickup distance, then lower load, then ID." if len(group) > 1 else ""

    if rule == 1:
        text = (
            f"Rule 1 (stop already scheduled): {chosen.id} is moving {chosen.direction} and already "
            f"stops at floor {request.floor}, so no stop is added.{tie_note} "
            f"{pickup}; {riders}."
        )
    elif rule == 2:
        text = (
            f"Rule 2 (light passing car): no eligible car already stops at floor {request.floor}; "
            f"{chosen.id} is moving {chosen.direction} past it with {chosen.load_kg} kg "
            f"<= {LIGHT_LOAD_KG} kg, so one added stop delays only a few riders.{tie_note} "
            f"{pickup}; {riders}."
        )
    else:
        others = [e for e in eligible if e is not chosen]
        if not others:
            basis = f"{chosen.id} is the only eligible car."
        elif _distance(others[0], request) > dist:
            basis = f"{chosen.id} is the nearest eligible car."
        else:
            basis = f"Eligible cars are equally near; tie-breaker (lower load, then ID) picks {chosen.id}."
        text = (
            f"Rule 3 (nearest car): no eligible moving car already stops at floor {request.floor} "
            f"or is light (<= {LIGHT_LOAD_KG} kg). {basis} {pickup}; {riders}."
        )
    return Decision(chosen.id, text)
