from typing import Iterator, Literal
from dataclasses import dataclass

import pygame

from src.core.events.event import post_event

from src.characters.characters import (
	MoveCharacter,
	move_character_x,
	move_character_y
)

Position = Iterator[int | float]
SIZE = Iterator[int | float]
Image = pygame.surface.Surface


@dataclass
class MovementsAlien(MoveCharacter):
	CONTINUE = "continue"

@dataclass
class MoveSatus:
	vertical: Literal["bottom", "continue"]
	horizontal: Literal["left", "right"]

class MoveAlien:
	def __init__(self, position: Position, size_alien: SIZE, screen_size: SIZE) -> None:
		self.speed_x = 0.7
		self.speed_y = 10 

		self.rect_position = pygame.Rect(position, size_alien)
		self.screen_size = screen_size
		self.move_status = MoveSatus(
			horizontal = MovementsAlien.LEFT,
			vertical = MovementsAlien.CONTINUE
		)

	def get_position(self):
		return self.rect_position.x, self.rect_position.y

	def set_new_postion_x(self, value: int | float) -> None:
		self.rect_position.x = value

	def set_new_postion_y(self, value: int | float) -> None:
		self.rect_position.y = value

	def right_position_limit_alien(self, position_x: int | float, width_alien: int | float) -> bool:
		RIGHT = self.screen_size[0] - width_alien
		return position_x == RIGHT

	def left_position_limit_alien(self, position_x: int | float) -> bool:
		LEFT = 0
		return position_x == LEFT

	def move_right(self, width_alien: int | float) -> None:
		new_postion = move_character_x(
			position_x = self.rect_position.x + self.speed_x, 
			width = width_alien,
			screen_size = self.screen_size
		)

		self.set_new_postion_x(value = new_postion)
		if self.right_position_limit_alien(position_x = self.rect_position.x, width_alien = width_alien):
			self.move_status.vertical = MovementsAlien.LEFT
			self.move_status.horizontal = MovementsAlien.BOTTOM


	def move_left(self, width_alien: int | float) -> None:
		new_postion = move_character_x(
			position_x = self.rect_position.x - self.speed_x, 
			width = width_alien,
			screen_size = self.screen_size
		)
		
		self.set_new_postion_x(value = new_postion)
		if self.left_position_limit_alien(position_x = self.rect_position.x):
			self.move_status.horizontal = MovementsAlien.BOTTOM
			self.move_status.vertical = MovementsAlien.RIGHT

	def move_bottom(self, height_alien: int | float) -> None:
		new_postion = move_character_y(
			position_y = self.rect_position.y + self.speed_y,
			height = height_alien,
			screen_size = self.screen_size
		)

		self.set_new_postion_y(value = new_postion)
		self.move_status.horizontal = MovementsAlien.CONTINUE


class Alien:
	def __init__(self, position: Position, img: Image, screen_size: SIZE) -> None:
		self.image = img
		self.mask = pygame.mask.from_surface(self.image)
		self.height =  self.image.get_height()
		self.width = self.image.get_width()
		self.size = self.image.get_size()

		self.move_alien = MoveAlien(
			position = position, 
			size_alien = self.size,
			screen_size = screen_size
		)

		self.moving = {
			MovementsAlien.LEFT: lambda: self.move_alien.move_left(width_alien = self.width),
			MovementsAlien.RIGHT: lambda: self.move_alien.move_right(width_alien = self.width),
			MovementsAlien.BOTTOM: lambda: self.move_alien.move_bottom(height_alien = self.height),
			MovementsAlien.CONTINUE: lambda: None
		}

	def collision(self, character, event) -> None:
		position = self.move_alien.get_position()
		
		collision = (position[0] - character.position[0], position[1] - character.position[1])

		if character.mask.overlap(self.mask, collision):
			post_event(event.event_type, event.data)
			post_event("game_over", True)

	def move(self):
		
		action_move_x = self.moving.get(self.move_alien.move_status.horizontal)
		action_move_y = self.moving.get(self.move_alien.move_status.vertical)

		if not action_move_x or not action_move_y:
			raise ValueError(f"Movimiento del Alien incorrecto: {self.move_alien.move_status}")

		action_move_x()
		action_move_y()

	def draw(self, screen):
		screen.blit(self.image, self.move_alien.get_position())
