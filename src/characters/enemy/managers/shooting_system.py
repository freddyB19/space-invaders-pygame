import math, random
from typing import Iterator
from dataclasses import dataclass

import pygame

from src.core.pools.bullet_pool import BulletPool

from src.characters.enemy.enemy import create_aliens
from src.characters.interfaces import (
	Size, 
	Image, 
	Rect,
	Speed,
	Position, 
	IAlien, 
	IBullet,
	
	IBullectAction
)


Time = float | int

"""
	Esta solución para elegir las naves enemigas que disparán, 
	representa una solución momentanea, ya que aun así suelo encontrar
	ciertos fallos al elegir que nave debe hacer el disparo.
	Más adelante será cambiado por una solución de la cual me encuentro
	trabajando.
"""
def distance_between(position_1: Iterator[Position], position_2: Iterator[Position]) -> Position:
	return math.sqrt( 
		((position_1[0] - position_2[0]) ** 2) + 
		((position_1[1] - position_2[1]) ** 2)
	)


def enemy_shoot(aliens: list[IAlien], position_ship: Iterator[Position]) -> Iterator[Position]:

	p1 = 0
	p2 = len(aliens) - 1

	min_distance = 1_000_000_000
	positions_shoot = []


	for _ in aliens:
		alien_1 = aliens[p1]
		alien_2 = aliens[p2]

		distance_alien_1 = distance_between(alien_1.position.get_position(), position_ship)
		distance_alien_2 = distance_between(alien_2.position.get_position(), position_ship)

		distance = min(distance_alien_1, distance_alien_2)

		if distance <= min_distance:
			positions_shoot.append(
				alien_1.position.get_position()
				if  distance_alien_1 == distance
				else alien_2.position.get_position()
			)
			min_distance = distance

		p1 += 1
		p2 -= 1

	return random.choice(positions_shoot[-3:]) if positions_shoot else ()


class EnemySimpleBullet(IBullectAction):
	def __init__(self, limit_x: int = None, limit_y: int = None) -> None:
		self.limit_x = limit_x
		self.limit_y = limit_y

	def valid_position_limit(self, position: Rect) -> bool:
		return position.y < self.limit_y

	def set_position(self, position: Rect, speed: Speed) -> Rect:
		new_position = position.copy()
		new_position.y += speed
		return new_position


class ShootFrequencyTime:
	def __init__(self, last_shoot_time: Time = 0, shoot_freq: Time = 200) -> None:
		self._last_shoot_time = last_shoot_time
		self._shoot_freq = shoot_freq

	def _set_last_shoot_time(self, time: Time) -> None:
		self._last_shoot_time = time

	def can_shoot(self, time: Time) -> bool:
		if time > self._last_shoot_time + self._shoot_freq:
			self._set_last_shoot_time(time = time)
			return True
		return False


WITHOUT_BULLETS = 0

class AlienShootingSystem:
	def __init__(self, level: int, bullet_img: Image) -> None:
		self.bullet_pool = BulletPool(size  = 200, bullet_img = bullet_img)
		self.simple_alien = ShootFrequencyTime(shoot_freq = 3000)
		self.alien_bullets = []

	def _can_alien_shoot(self, time: Time) -> bool:
		return self.simple_alien.can_shoot(time)

	def _load_bullet(self, position: Position) -> None:
		bullet = self.bullet_pool.get()
		bullet.set_position(position = position)
		self.alien_bullets.append(bullet)

	def _set_bullets(self, bullets: list[IBullet]) -> None:
		self.alien_bullets = bullets

	def has_bullets(self) -> bool:
		return len(self.alien_bullets) > WITHOUT_BULLETS

	def get_bullets(self) -> list[IBullet]:
		return self.alien_bullets.copy()

	def clean_weapon(self, index_bullets: list[IBullet]) -> None:
		if not index_bullets:
			return

		new_bullets = [bullet for index, bullet in enumerate(self.alien_bullets) if index not in index_bullets]

		self._set_bullets(new_bullets.copy())

	def alien_shoot(self, aliens: list[IAlien], ship_position: Position) -> Position:
		time = pygame.time.get_ticks()

		if self._can_alien_shoot(time = time) and aliens:
			alien_position = enemy_shoot(aliens, ship_position)
			self._load_bullet(position = alien_position)


__all__ = [
	"AlienShootingSystem",
	"EnemySimpleBullet"
]