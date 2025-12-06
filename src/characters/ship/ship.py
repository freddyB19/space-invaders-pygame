from typing import Iterator
from dataclasses import dataclass

import pygame

from src.characters.characters import (
	MoveCharacter,
	move_character_x,
	move_character_y
)

Position = Iterator[int | float]
SIZE = Iterator[int | float]
Image = pygame.surface.Surface


class MoveShip:

	def __init__(self, position: Position, size_ship: SIZE, screen_size: SIZE) -> None:
		self.speed = 0.9
		self.rect_position = pygame.Rect(position, size_ship)
		self.screen_size = screen_size

	def get_position(self):
		return self.rect_position.x, self.rect_position.y

	def set_new_position_x(self, value: int | float) -> None:
		self.rect_position.x = value

	def set_new_position_y(self, value: int | float) -> None:
		self.rect_position.y = value

	def move_left(self, width_ship: int | float) -> None:
		self.set_new_position_x(
			value = move_character_x(
				position_x = self.rect_position.x - self.speed, 
				width = width_ship,
				screen_size = self.screen_size
			)
		)

	def move_right(self, width_ship: int | float) -> None:
		self.set_new_position_x(
			value = move_character_x(
				position_x = self.rect_position.x + self.speed, 
				width = width_ship,
				screen_size = self.screen_size
			)
		)

	def move_top(self, height_ship: int | float) -> None:

		self.set_new_position_y(
			value = move_character_y(
				position_y = self.rect_position.y - self.speed, 
				height = height_ship,
				screen_size = self.screen_size
			)
		)
			
	def move_bottom(self, height_ship: int | float) -> None:
		self.set_new_position_y(
			value = move_character_y(
				position_y = self.rect_position.y + self.speed, 
				height = height_ship,
				screen_size = self.screen_size
			)
		)

class Ship:
	def __init__(self, position: Position, img: Image, screen_size: SIZE) -> None:

		self.image = img
		self.height =  self.image.get_height()
		self.width = self.image.get_width()
		self.size = self.image.get_size()
		self.move_ship = MoveShip(position = position, size_ship = self.size, screen_size = screen_size)

	def move(self, direction: str) -> None:
		if MoveCharacter.TOP == direction:
			self.move_ship.move_top(height_ship = self.height)
		elif MoveCharacter.BOTTOM == direction:
			self.move_ship.move_bottom(height_ship = self.height)
		elif MoveCharacter.LEFT == direction:
			self.move_ship.move_left(width_ship = self.width)
		elif MoveCharacter.RIGHT == direction:
			self.move_ship.move_right(width_ship = self.width)

	def shoot(self) -> None:
		pass

	def draw(self, screen: Image) -> None:
		screen.blit(self.image, self.move_ship.get_position())
