"""Process helper: arrive -> request -> service -> leave (car example)."""

from typing import Dict, List, Sequence

from core.engine import SimulationEngine
from core.resource import Resource


def run_car_example(arrivals: Sequence[float] = (0.0, 2.0, 3.0),
                    service_time: float = 5.0) -> Dict[str, List[str]]:
    """Reproduce the car-service example (lecture pages 157-159).

    Args:
        arrivals: Arrival time of each car.
        service_time: Constant service time.

    Returns:
        Dict with ``chronological`` (events in simulated time order) and
        ``lecture`` (the layout printed in the lecture: all arrivals first,
        then each car's start and leave lines).
    """
    engine = SimulationEngine()
    chrono: List[str] = []
    arrive_lines: List[str] = []
    service_lines: Dict[int, List[str]] = {}

    def on_start(car: int) -> None:
        line = f"Car {car} started service at {engine.now:.2f}"
        chrono.append(line)
        service_lines.setdefault(car, []).append(line)
        engine.schedule(service_time, lambda c=car: leave(c))

    server = Resource(capacity=1, on_start=on_start)

    def leave(car: int) -> None:
        line = f"Car {car} left at {engine.now:.2f}"
        chrono.append(line)
        service_lines[car].append(line)
        server.release()

    def arrive(car: int) -> None:
        line = f"Car {car} arrived at {engine.now:.2f}"
        chrono.append(line)
        arrive_lines.append(line)
        server.request(car)

    for i, t in enumerate(arrivals, start=1):
        engine.schedule(t, lambda c=i: arrive(c))
    engine.run()

    lecture = list(arrive_lines)
    for car in sorted(service_lines):
        lecture.extend(service_lines[car])
    return {"chronological": chrono, "lecture": lecture}
