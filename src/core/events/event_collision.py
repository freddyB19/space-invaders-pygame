from typing import Any
from .event import subscribe

def handler_explosion_collision(data_event: dict[str, Any]) -> None:
	screen = data_event["screen"]

	screen.blit(data_event["character"]["image"], data_event["character"]["position"])

def setup_event_explosion_collision() -> None:
	subscribe("explosion", handler_explosion_collision)
