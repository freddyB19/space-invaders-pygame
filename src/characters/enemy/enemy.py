from typing import Iterator

import pygame

Position = Iterator[int | float]
SIZE = Iterator[int | float]
Image = pygame.surface.Surface

class Alien:
	def __init__(self, position: Position, img: Image) -> None:
		self.image = img
		self.height =  self.image.get_height()
		self.width = self.image.get_width()
		self.size = self.image.get_size()

		self.rect_position = pygame.Rect(position, self.size)

	def move(self):
		pass

	def draw(self, screen):
		screen.blit(self.image, (self.rect_position.x, self.rect_position.y))
