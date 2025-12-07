from dataclasses import dataclass

import pygame

from src import BACKGROUND_DIR, ASSETS_DIR

from src.characters.ship.ship import Ship
from src.characters.enemy.enemy import Alien
from src.characters.characters import MoveCharacter

Image = pygame.surface.Surface

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

		self.aliens = [
			Alien(position = (400, 30), img = self.alien_surface)
		]

	def ship_events(self) -> None:
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
					self.ship.bullets.pop(index)


	def alien_events(self) -> None:
		for alien in self.aliens:
			alien.draw(screen = self.screen)


	def keys_player(self, time: float) -> None:
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

		if keys[pygame.K_SPACE]:
			self.ship.shoot(time_shoot = time, bullet_image = self.bullet_surface)


	def events(self) -> None:
		keys = pygame.key.get_pressed()

		for event in pygame.event.get():
			if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
				self.running = False

	def draw_background(self) -> None:
		self.screen.blit(self.BACKGROUND, (0,0))

	def update_screen(self) -> None:
		pygame.display.update()

	def exit(self):
		pygame.time.wait(3500)
		pygame.quit()

	def run(self) -> None:
		pygame.init()
		
		while self.running:
			self.draw_background()

			time = pygame.time.get_ticks()
			
			self.events()

			self.keys_player(time = time)
			self.ship_events()

			self.bullets_events()
			
			self.alien_events()

			self.update_screen()

		self.exit()
