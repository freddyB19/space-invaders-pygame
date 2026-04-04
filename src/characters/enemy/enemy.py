from typing import Iterator
from dataclasses import dataclass

import pygame

from src.core.events.event import post_event

from src.characters.characters import (
	MoveCharacter,
	move_character_x,
	move_character_y
)
from src.characters.interfaces import (
	IEvent,
	IAlien,
	IBullet,
	ICharacter,
	IBullectAction, 
	Rect,
	Size,
	Image,
	Speed,
	Position,
)


@dataclass
class AlienLimits:
	right: int
	left: int




class MoveAlien:
	def __init__(self, position: Position, size_alien: Size, screen_size: Size) -> None:
		
		self._position = pygame.Rect(position, size_alien)
		self._width = size_alien[0]
		self._height = size_alien[1]
		self._speed_x = 0.7
		self._speed_y = 10
		self._direction = 1
		self._screen_size = screen_size
		self._limits = AlienLimits(right = 0, left = (screen_size[0] - self._width))

	def _set_new_postion_x(self, value: int | float) -> None:
		self._position.x = value

	def _set_new_postion_y(self, value: int | float) -> None:
		self._position.y = value

	def get_position(self) -> None:
		return self._position.x, self._position.y

	def get_position_x(self):
		return self._position.x

	def change_direction(self) -> None:
		self._direction *= -1

	def changing_position_x(self) -> None:
		new_position = move_character_x(
			position_x = self._position.x + (self._speed_x * self._direction), 
			width = self._width,
			screen_size = self._screen_size
		)

		self._set_new_postion_x(new_position)

	def changing_position_y(self) -> None:
		new_position = move_character_y(
			position_y = self._position.y + self._speed_y,
			height = self._height,
			screen_size = self._screen_size
		)

		self._set_new_postion_y(new_position)

	def touch_edge(self) -> bool:
		position_x = self.get_position_x() 
		return position_x >= self._limits.left or position_x <= self._limits.right 


class Alien:
	def __init__(self, position: Position, img: Image, screen_size: Size) -> None:
		self.image = img
		self.mask = pygame.mask.from_surface(self.image)
		self.height =  self.image.get_height()
		self.width = self.image.get_width()
		self.size = self.image.get_size()
		self.alive = True
		self.bullets = []

		self.position = MoveAlien(
			position = position, 
			size_alien = self.size,
			screen_size = screen_size
		)

	def is_alive(self) -> None:
		return self.alive

	def dead(self) -> None:
		self.alive = False

	def collision(self, character: ICharacter, event: IEvent) -> bool:
		position = self.position.get_position()
		
		collision = (position[0] - character.position[0], position[1] - character.position[1])

		if character.mask.overlap(self.mask, collision) and self.is_alive():
			post_event(event.event_type, event.data)
			self.dead()
			return True

		return False

	def move_x(self) -> None:
		self.position.changing_position_x()

	def move_y(self) -> None:
		self.position.change_direction()
		self.position.changing_position_y()

	def draw(self, screen: Image):
		screen.blit(self.image, self.position.get_position())

	def __repr__(self):
		return f"Alien(alive = {self.is_alive()}, position = {self.position.get_position()}, bullets = {len(self.bullets)})"

def create_aliens(image: Image, screen_size: Size) -> list[IAlien]:
	aliens:list[Alien] = []
	total_rows = 5
	total_columns = 10

	spacing_between = 50
	horizontal_starting_position = 50
	vertical_starting_position = 50

	for row in range(total_rows):
		for column in range(total_columns):
			aliens.append(
				Alien(
					position = (
						column * horizontal_starting_position + spacing_between, 
						row * vertical_starting_position + spacing_between 
					), 
					img = image,
					screen_size = screen_size
				)
			)

	return aliens


def draw_aliens(aliens: list[IAlien], image: Image, screen: Image) -> None:
	valid_alien = []
	for alien in aliens:
		if alien.is_alive():
			valid_alien.append([image, alien.position.get_position()])

	screen.blits(blit_sequence = valid_alien)
