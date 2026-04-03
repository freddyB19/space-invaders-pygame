from typing import Protocol, Iterator, Any

import pygame

Rect = pygame.Rect
Speed = int | float
Image = pygame.surface.Surface
Mask = pygame.mask.Mask
Position = Iterator[int | float]
Size = Iterator[int | float]

class ICharacter(Protocol):
	mask: Mask
	position: Position

class IEvent(Protocol):
	event_type: str
	data: dict[str, Any]

error_message = 'Debe implementar el método:'


class IBullectAction(Protocol):
	ERROR = f'[IBullectAction], {error_message}'

	def valid_position_limit(position: Rect) -> bool:
		raise NotImplementedError(f'{ERROR} "valid_position_limit"')

	def set_position(position: Rect, speed: Speed) -> Rect:
		raise NotImplementedError(f'{ERROR} "set_position"')


class IBullet:
	ERROR = f'[Bullet], {error_message}'

	def change_status(self):
		raise NotImplementedError(f'{ERROR} "valid_position_limit"')

	def set_position_y(self, value: Position) -> None:
		raise NotImplementedError(f'{ERROR} "valid_position_limit"')

	def set_position(self, position: Iterator[Position]) -> None:
		raise NotImplementedError(f'{ERROR} "set_position"')

	def get_position(self) -> Iterator[Position]:
		raise NotImplementedError(f'{ERROR} "get_position"')

	def move(self, bullect_action: IBullectAction) -> bool:
		raise NotImplementedError(f'{ERROR} "move"')

	def draw(self, screen: Image) -> None:
		raise NotImplementedError(f'{ERROR} "draw"')


class IAlien:
	ERROR = f'[Alien], {error_message}'

	def is_alive(self) -> bool:
		raise NotImplementedError(f'{ERROR} "is_alive"')

	def dead(self) -> None:
		raise NotImplementedError(f'{ERROR} "dead"')

	def collision(self, character: ICharacter, event: IEvent) -> bool:
		raise NotImplementedError(f'{ERROR} "collision"')

	def move_x(self) -> None:
		raise NotImplementedError(f'{ERROR} "move_x"')

	def move_y(self) -> None:
		raise NotImplementedError(f'{ERROR} "move_y"')

	def shoot(self, bullet: IBullet) -> None:
		raise NotImplementedError(f'{ERROR} "shoot"')

	def draw(self, screen: Image) -> None:
		raise NotImplementedError(f'{ERROR} "draw"')


class IShip:
	ERROR = f'[Ship], {error_message}'

	def total_lives(self) -> int:
		raise NotImplementedError(f'{ERROR} "draw"')


	def move(self, direction: str) -> None:
		raise NotImplementedError(f'{ERROR} "move"')


	def collision(self, character: ICharacter, event: IEvent) -> bool:
		raise NotImplementedError(f'{ERROR} "move"')


	def shoot(self, time_shoot: float, bullet: IBullet) -> None:
		raise NotImplementedError(f'{ERROR} "shoot"')

	def draw(self, screen: Image) -> None:
		raise NotImplementedError(f'{ERROR} "shoot"')


__all__ = [
	"IBullet",
	"IShip",
	"IAlien",
	"IEvent",
	"ICharacter",
	"IBullectAction",
	"Rect",
	"Speed",
	"Image",
	"Mask",
	"Position",
	"Size"
]