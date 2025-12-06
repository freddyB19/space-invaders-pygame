from dataclasses import dataclass

import pygame

from src import BACKGROUND_DIR, ASSETS_DIR

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
			
			self.events()

			self.update_screen()

		self.exit()


def main() -> None:
	pygame.init()

	running = True
	alien_opc_move = ["right", "left"]
	moving_alien_x = random.choice(alien_opc_move)
	bullets = []

	time_shoot = ShotFrequencyTime()

	while running:
		SCREEN.blit(BG, (0,0))
		
		time_shoot.set_time(new_time = pygame.time.get_ticks())
		keys = pygame.key.get_pressed()

		for event in pygame.event.get():
			if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
				running = False

		draw_characters([
			[SHIP_IMG, [rect_ship.x, rect_ship.y]],
			[ALIEN_IMG, [rect_alien.x, rect_alien.y]],

		])

		move_x, move_y = valid_move_alien(rect_alien.x, moving_alien_x)
		moving_alien_x = move_x

		new_position_alien = move_alien(
			position_x = rect_alien.x,
			position_y = rect_alien.y,
			move = (move_x, move_y),
			width = WIDTH_ALIEN,
			height = HEIGHT_ALIEN
		)
		rect_alien.x = new_position_alien[0]
		rect_alien.y = new_position_alien[1]

		new_position_ship = move_player(
			position_x = rect_ship.x,
			position_y = rect_ship.y,
			width = rect_ship.width,
			height = rect_ship.height
		)
		rect_ship.x = new_position_ship[0]
		rect_ship.y = new_position_ship[1]

		bullets = shoot(
			position = [new_position_ship[0], new_position_ship[1]], 
			bullets = bullets.copy(),
			time_shoot = time_shoot
		)	

		is_game_over = collision(
			ship = Character(position = new_position_ship, image = SHIP_IMG),
			alien = Character(position = new_position_alien, image = ALIEN_IMG),
			bullets = bullets.copy()
		)
		
		if is_alien_winner(new_position_alien[1]) or is_game_over:
			running = False

		pygame.display.update()

	pygame.time.wait(3500)
	pygame.quit()