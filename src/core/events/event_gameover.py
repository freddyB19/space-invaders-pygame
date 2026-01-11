from typing import Any
from .event import subscribe

import pygame

def handler_game_over(data: bool) -> None:
	event = pygame.event.Event(pygame.QUIT)
	pygame.event.post(event)

def setup_event_game_over() -> None:
	subscribe("game_over", handler_game_over)
