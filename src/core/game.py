from typing import Iterator, Literal, Any
from dataclasses import dataclass

import pygame

from src import BACKGROUND_DIR, ASSETS_DIR

from src.characters.ship.ship import Ship
from src.characters.enemy.enemy import Alien, draw_aliens, create_aliens
from src.characters.characters import MoveCharacter

from .managers.score import EnemyType, ManagerScore

from .events.event_gameover import setup_event_game_over
from .events.event_collision import setup_event_explosion_collision

from .pools.bullet_pool import BulletPool


Image = pygame.surface.Surface
Mask = pygame.mask.Mask
Position = Iterator[int | float]

@dataclass
class Character:
	mask: Mask
	position: Position

@dataclass
class Event:
	event_type: str
	data: dict[str, Any]

@dataclass
class SettingsGame:
	SCREEN = (800, 600)
	TITLE = "Space invaders"

@dataclass
class SettingsMediaGame:
	BACKGROUND_IMG = BACKGROUND_DIR / "background.jpg"
	ICON_IMG = ASSETS_DIR / "icon.png"
	SHIP_IMG = ASSETS_DIR / "player.png"
	ENEMY_IMG = ASSETS_DIR / "enemy.png"
	BULLET_IMG = ASSETS_DIR / "fireball.png"
	EXPLOSION_IMG = ASSETS_DIR / "explosion.png"

	@classmethod
	def exists(cls) -> None:
		assert cls.BACKGROUND_IMG.exists()
		assert cls.SHIP_IMG.exists()
		assert cls.ENEMY_IMG.exists()
		assert cls.BULLET_IMG.exists()
		assert cls.EXPLOSION_IMG.exists()


class SpaceInvaders:

	def __init__(self) -> None:
		SettingsMediaGame.exists()

		pygame.display.set_caption(SettingsGame.TITLE)
		pygame.display.set_icon(pygame.image.load(SettingsMediaGame.ICON_IMG))

		self.screen = pygame.display.set_mode(SettingsGame.SCREEN)
		self.screen_size:tuple[int] = SettingsGame.SCREEN

		self.BACKGROUND:Image = pygame.image.load(SettingsMediaGame.BACKGROUND_IMG)
		self.ship_surface:Image = pygame.image.load(SettingsMediaGame.SHIP_IMG)
		self.alien_surface:Image = pygame.image.load(SettingsMediaGame.ENEMY_IMG)
		self.bullet_surface:Image = pygame.image.load(SettingsMediaGame.BULLET_IMG)
		self.explosion_surface:Image = pygame.image.load(SettingsMediaGame.EXPLOSION_IMG)

		self.running = True
		self.ship = Ship(
			position = (400, 400), 
			img = self.ship_surface,
			screen_size = self.screen_size
		)

		self.aliens = create_aliens(image = self.alien_surface, screen_size = self.screen_size)

		self.bullet_pool = BulletPool(size = 10, bullet_img = self.bullet_surface)
		self.score = ManagerScore()
		setup_event_explosion_collision()
		setup_event_game_over()

	def ship_events(self, aliens: list[Alien]) -> None:
		for alien in aliens:
			if alien.is_alive():
				impact = self.ship.collision(
					character = Character(
						position = alien.position.get_position(),
						mask = alien.mask
					),
					event = Event(
						event_type = "explosion",
						data = {
						    "character": {
						    "image": self.explosion_surface, 
						    "position": self.ship.move_ship.get_position(),
						},
						    "screen": self.screen
						}
					),
				)

				if impact:

					alien.collision(
						character = Character(
							position = self.ship.move_ship.get_position(),
							mask = self.ship.mask
						),
						event = Event(
							event_type = "explosion",
							data = {
							    "character": {
							    "image": self.explosion_surface, 
							    "position": alien.position.get_position(),
							},
							    "screen": self.screen
							}
						),
					)

					for i in range(10):
						draw_aliens(aliens = aliens, screen = self.screen, image = self.alien_surface)
						self.update_screen()
						pygame.time.wait(210)

					self.ship.move_ship.reset_position()

		self.ship.draw(screen = self.screen)

	def bullets_events(self) -> None:
		if self.ship.bullets:
			bullets = []

			# Puede mejorar
			for index, bullet in enumerate(self.ship.bullets):
				moved = bullet.move()

				if moved:
					bullet.draw(screen = self.screen)
				else:
					bullet = self.ship.bullets.pop(index)
					self.bullet_pool.release(resorce = bullet)

	def alien_events(self, aliens: list[Alien]) -> None:
		edge_touched = False

		for alien in aliens:
			
			for bullet in self.ship.bullets:
				impact = alien.collision(
					character = Character(
						position = bullet.get_position(),
						mask = bullet.mask
					),
					event = Event(
						event_type = "explosion",
						data = {
							"character": {
							"image": self.explosion_surface, 
							"position": alien.position.get_position(),
						},
							"screen": self.screen
						}
					),
				)

				if impact:
					bullet.change_status()
					self.score.add_point(enemy_type = EnemyType.NORMAL)

			bullets = list(filter(lambda bullet: bullet.status, self.ship.bullets))
			self.ship.bullets = bullets

			if alien.is_alive():
				alien.move_x()

				if alien.position.touch_edge():
					edge_touched = True

		if edge_touched:
			for alien in aliens:
				alien.move_y()
		
		self.aliens = list(filter(lambda alien: alien.is_alive(), aliens))
		draw_aliens(aliens = self.aliens, screen = self.screen, image = self.alien_surface)

	def draw_game_over(self):
		title_size = 60
		label = pygame.font.Font(None, title_size)

		message = "GAME OVER"
		screen_width = self.screen_size[0]
		screen_height = self.screen_size[1]
		XPOSITION = int(screen_width / 2) 
		YPOSITION = int(screen_height / 2)
		color = (220, 220, 220)

		message_surface = label.render(message, True, color)

		message_rect = message_surface.get_rect(centerx = XPOSITION, centery=YPOSITION)

		for _ in range(13):
			self.screen.blit(message_surface, message_rect)
			self.update_screen()
			pygame.time.wait(300)



	def keys_player(self) -> None:
		keys = pygame.key.get_pressed()

		# Move
		if keys[pygame.K_w] or keys[pygame.K_UP]:
			self.ship.move(direction = MoveCharacter.TOP)
		if keys[pygame.K_s] or keys[pygame.K_DOWN]:
			self.ship.move(direction = MoveCharacter.BOTTOM)
		if keys[pygame.K_a] or keys[pygame.K_LEFT]:
			self.ship.move(direction = MoveCharacter.LEFT)
		if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
			self.ship.move(direction = MoveCharacter.RIGHT)

	def player_shoot_key(self) -> None:
		keys = pygame.key.get_pressed()
		time = pygame.time.get_ticks()

		if keys[pygame.K_SPACE]:
			bullet = self.bullet_pool.get()
			self.ship.shoot(time_shoot = time, bullet = bullet)


	def events(self) -> None:
		keys = pygame.key.get_pressed()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
				print("Cerrando el juego")
				self.draw_game_over()
				self.running = False
			if event.type == pygame.KEYDOWN:
				self.player_shoot_key()
		
		self.keys_player()

	def draw_score(self) -> None:
		label = pygame.font.Font(None, 30)

		text = f"Score:"
		text_score = str(self.score.get_total_score())
		color = (220, 220, 220)
		background_color = (60, 60, 60)

		label_score = label.render(text, False, color)
		label_text_score = label.render(text_score, False, color)

		pos_score = label_score.get_rect(x= self.screen_size[0] - 70, y=10)
		pos_text_score = label_text_score.get_rect(x= self.screen_size[0] - 45, y=35)

		self.screen.blit(label_score, pos_score)
		self.screen.blit(label_text_score, pos_text_score)

	def draw_player_life(self, total_life: int) -> None:
		label = pygame.font.Font(None, 30)

		space_between = 2.5
		horizontal_position = 20
		size = 10
		position_y = 100

		color = (220, 220, 220)
		text = "Lives:"
		position_x_label = self.screen_size[0] - 70
		position_y_label = 70

		label_lives = label.render(text, True, color)

		position_label_lives = label_lives.get_rect(
			x = position_x_label,
			y = position_y_label
		)

		self.screen.blit(label_lives, position_label_lives)


		for i in range(1, total_life + 1):
			pygame.draw.rect(
				self.screen, 
				"red", 
				(
					self.screen_size[0] - (i * horizontal_position + space_between),
					position_y,
					size, 
					size
				)
			)

	def draw_background(self) -> None:
		self.screen.blit(self.BACKGROUND, (0,0))

	def update_screen(self) -> None:
		pygame.display.update()

	def exit(self):
		pygame.time.wait(3500)
		pygame.quit()
		pygame.font.quit()

	def run(self) -> None:
		pygame.init()
		pygame.font.init()


		while self.running:
			self.draw_background()
			
			self.draw_score()
			self.draw_player_life(self.ship.total_lives())

			self.events()

			self.ship_events(aliens = self.aliens)

			self.bullets_events()
			
			self.alien_events(aliens = self.aliens)

			self.update_screen()

		self.exit()
