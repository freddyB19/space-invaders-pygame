from typing import Iterator

import pygame

Position = Iterator[int | float]
Image = pygame.surface.Surface


class Bullet:
	def __init__(self, position: Position, img: Image) -> None:
		self.image = img
		self.mask = pygame.mask.from_surface(self.image)
		self.size = self.image.get_size()
		self.speed = 2.8

		self.rect_position = pygame.Rect(position, self.size)

	def set_position_y(self, value: int | float) -> None:
		self.rect_position.y = value

	def get_position(self) -> tuple[int]:
		return (self.rect_position.x, self.rect_position.y)

	def valid_position_limit(self):
		TOP_SCREEN = 0
		return self.rect_position.y > TOP_SCREEN

	def move(self) -> bool:
		if not self.valid_position_limit():
			return False

		self.set_position_y(value = self.rect_position.y - self.speed)
		return True


	def draw(self, screen: Image):
		screen.blit(self.image, self.get_position())
