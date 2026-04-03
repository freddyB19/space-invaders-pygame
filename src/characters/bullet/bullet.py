from typing import Iterator

import pygame

from src.characters.interfaces import (
	Image,
	Position,
	IBullectAction
)


class Bullet:
	def __init__(self, position: Position, img: Image) -> None:
		self.image = img
		self.mask = pygame.mask.from_surface(self.image)
		self.size = self.image.get_size()
		self.speed = 2.8
		self.status = True

		self.rect_position = pygame.Rect(position, self.size)

	def change_status(self) -> None:
		self.status = not self.status

	def set_position(self, position: Position) -> None:
		self.rect_position.x = position[0]
		self.rect_position.y = position[1]

	def get_position(self) -> Position:
		return (self.rect_position.x, self.rect_position.y)

	def move(self, bullect_action: IBullectAction) -> bool:
		if not bullect_action.valid_position_limit(position = self.rect_position):
			return False

		self.rect_position = bullect_action.set_position(
			position = self.rect_position, 
			speed = self.speed
		)
		return True

	def draw(self, screen: Image) -> None:
		if self.status:
			screen.blit(self.image, self.get_position())
