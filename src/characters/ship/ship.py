from typing import Iterator
from dataclasses import dataclass

import pygame

Position = Iterator[int | float]
SIZE = Iterator[int | float]
Image = pygame.surface.Surface

class Ship:
	def __init__(self, position: Position, img: Image) -> None:

		self.image = img
		self.height =  self.image.get_height()
		self.width = self.image.get_width()
		self.size = self.image.get_size()
		self.rect_position = pygame.Rect(position, self.size)
		self.speed = 0.9

	def move(self) -> None:
		pass

	def shoot(self) -> None:
		pass

	def draw(self, screen: Image) -> None:
		screen.blit(self.image, (self.rect_position.x, self.rect_position.y))
