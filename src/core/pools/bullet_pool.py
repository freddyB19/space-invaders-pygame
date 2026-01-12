import queue

import pygame

from src.characters.bullet.bullet import Bullet

from .interfaces import IBulletPool

Image = pygame.surface.Surface

class BulletPool(IBulletPool):
	def __init__(self, bullet_img: Image, size: int = 1) -> None:
		self._pool = queue.Queue()
		self._bullet_img = bullet_img
		self._default_position = (0,0)

		self._add_bullet_to_pool(size = size)

	def _add_bullet_to_pool(self, size: int) -> None:
		for bullet in range(size):
			self._pool.put(
				Bullet(position = self._default_position, img = self._bullet_img)
			)
 
	def get(self) -> Bullet:
		if not self._pool.empty():
			return self._pool.get(block=False)

		return Bullet(position = self._default_position, img = self._bullet_img)

	def release(self, resorce: Bullet) -> None:
		if not resorce:
			raise ValueError(f"[{self.__class__}]: debe pasar un elemento")
		if not isinstance(resorce, Bullet):
			raise ValueError("Debe ser una instancia de 'Bullet'")

		resorce.set_position(position = self._default_position)
		self._pool.put(resorce, block=False)
