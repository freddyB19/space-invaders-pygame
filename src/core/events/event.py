from typing import Any, Callable

Function = Callable[[Any], None]

subscribers:dict[str, Function] = {}

def subscribe(event_type: str, func: Function) -> None:
	if event_type not in subscribers:
		subscribers[event_type] = []

	subscribers[event_type].append(func)


def post_event(event_type: str, data: Any) -> None:
	if event_type not in subscribers:
		return

	for subscriber in subscribers[event_type]:
		subscriber(data)
