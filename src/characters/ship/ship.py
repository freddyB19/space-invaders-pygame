from typing import Iterator
from dataclasses import dataclass

import pygame

from src.core.events.event import post_event
from src.characters.characters import (
	MoveCharacter,
	move_character_x,
	move_character_y
)
from src.characters.bullet.bullet import Bullet

Position = Iterator[int | float]
SIZE = Iterator[int | float]
Image = pygame.surface.Surface


@dataclass
class ShotFrequencyTime:
	last_shoot_time: int | float = 0
	shoot_freq: int = 200

	def can_shoot(self, time: float) -> bool:
		if time > self.last_shoot_time + self.shoot_freq:
			self.set_last_shoot_time(time = time)
			return True
		return False

	def set_last_shoot_time(self, time: int | float) -> None:
		self.last_shoot_time = time


class MoveShip:

	def __init__(self, position: Position, size_ship: SIZE, screen_size: SIZE) -> None:
		self.speed = 0.9
		self.rect_position = pygame.Rect(position, size_ship)
		self.start_position = position
		self.screen_size = screen_size

	def reset_position(self):
		self.set_new_position_x(self.start_position[0])
		self.set_new_position_y(self.start_position[1])

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


class LiveShip:
    REST_LIVE = 1
    TOTAL_MIN_LIVE = 1

    def __init__(self) -> None:
        self._total_lives = 3
        self._alive = True
    
    def is_alive(self) -> bool:
        return self._alive

    def removing_life(self) -> None:
        if self.is_alive():
            self._total_lives -= self.REST_LIVE

    def check_lives(self) -> bool:
        return self._total_lives >= self.TOTAL_MIN_LIVE

    def dead(self) -> None:
        self._alive = False

    def take_life(self) -> None:
        self.removing_life()

        if not self.check_lives():
            self.dead()
            post_event("game_over", True)


class Ship:
	def __init__(self, position: Position, img: Image, screen_size: SIZE) -> None:

		self.image = img
		self.mask = pygame.mask.from_surface(self.image)
		self.height =  self.image.get_height()
		self.width = self.image.get_width()
		self.size = self.image.get_size()
		self.move_ship = MoveShip(position = position, size_ship = self.size, screen_size = screen_size)
		self.shoot_freq = ShotFrequencyTime()
		self.bullets = []
		self.live = LiveShip()

	def move(self, direction: str) -> None:
		if MoveCharacter.TOP == direction:
			self.move_ship.move_top(height_ship = self.height)
		elif MoveCharacter.BOTTOM == direction:
			self.move_ship.move_bottom(height_ship = self.height)
		elif MoveCharacter.LEFT == direction:
			self.move_ship.move_left(width_ship = self.width)
		elif MoveCharacter.RIGHT == direction:
			self.move_ship.move_right(width_ship = self.width)

	def collision(self, character, event) -> bool:
		position = self.move_ship.get_position()

		collision = (position[0] - character.position[0], position[1] - character.position[1])

		if character.mask.overlap(self.mask, collision):
			post_event(event.event_type, event.data)

			self.live.take_life()

			return True

		return False


	def shoot(self, time_shoot: float, bullet: Bullet) -> None:
		
		if self.shoot_freq.can_shoot(time = time_shoot):
			bullet.set_position(position = self.move_ship.get_position())
			self.bullets.append(bullet)

	def draw(self, screen: Image) -> None:
		if self.live.is_alive():
			screen.blit(self.image, self.move_ship.get_position())
