import os, random, math
from typing import Literal, Any
from dataclasses import dataclass

import pygame

BASEDIR = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(BASEDIR, "assets")

WINDOW = (800, 600)
SCREEN = pygame.display.set_mode(WINDOW)
BACKGROUND = (50, 12, 122)

pygame.display.set_caption("Space invaders")

background_dir = os.path.join(assets_dir, "background")
bg_name = "background.jpg"
BG = pygame.image.load(os.path.join(background_dir, bg_name))

icon_name = "icon.png"
icon = pygame.image.load(os.path.join(assets_dir, icon_name))
pygame.display.set_icon(icon)


ship_img_name = "player.png"
SHIP_IMG = pygame.image.load(os.path.join(assets_dir, ship_img_name))
POSITION_INIT_SHIP = [
	400,
	400,
]
rect_ship = SHIP_IMG.get_rect()
rect_ship.x = POSITION_INIT_SHIP[0]
rect_ship.y = POSITION_INIT_SHIP[1]
SIZE_SHIP = SHIP_IMG.get_size()
SIZE_SHIP = (SIZE_SHIP[0] * 1, SIZE_SHIP[0] * 1)
SHIP_IMG = pygame.transform.scale(SHIP_IMG, SIZE_SHIP)
HEIGHT_SHIP = SHIP_IMG.get_height()
WIDTH_SHIP = SHIP_IMG.get_width()


bullet_img_name = "fireball.png"
BULLET_IMG = pygame.image.load(os.path.join(assets_dir, bullet_img_name))
rect_bullet = BULLET_IMG.get_rect()
SIZE_BULLET = BULLET_IMG.get_size()
HEIGHT_BULLET = BULLET_IMG.get_height()
WIDTH_BULLET = BULLET_IMG.get_width()


alien_img_name = "enemy.png"
ALIEN_IMG = pygame.image.load(os.path.join(assets_dir, alien_img_name))
POSITION_INIT_ALIEN = [
	400,
	30,
]
rect_alien = ALIEN_IMG.get_rect()
rect_alien.x = POSITION_INIT_ALIEN[0]
rect_alien.y = POSITION_INIT_ALIEN[1]
WIDTH_ALIEN = ALIEN_IMG.get_width()
HEIGHT_ALIEN = ALIEN_IMG.get_height()
SIZE_ALIEN = ALIEN_IMG.get_size()
SIZE_ALIEN = [SIZE_ALIEN[0] * 1, SIZE_ALIEN[1] * 1]
ALIEN_IMG = pygame.transform.scale(ALIEN_IMG, SIZE_ALIEN)


explosion_img_name = "explosion.png"
EXPLOSION_IMG = pygame.image.load(os.path.join(assets_dir, explosion_img_name))

# Draw
Image = pygame.surface.Surface
SEQUENCE = [Image, list[int | float]]

def draw_character(character: Image, position: list[int | float]) -> None:
	SCREEN.blit(character, position)

def draw_characters(characters: list[SEQUENCE]) -> None:
	SCREEN.blits(blit_sequence = characters)

def draw_shots(fires: list[SEQUENCE]) -> None:
	SCREEN.blits(blit_sequence = fires)

# Move
def move_character_x(position_x: int, width: int) -> int:
	LEFT = 0
	RIGHT = WINDOW[0] - width
	
	if position_x <= 0:
		position_x = 0
	elif position_x >= RIGHT:
		position_x = RIGHT

	return position_x

def move_character_y(position_y: int, height: int) -> int:
	TOP = 0
	BOTTOM = WINDOW[1] - height
	
	if position_y <= TOP:
		position_y = TOP
	elif position_y >= BOTTOM:
		position_y = BOTTOM

	return position_y


# Ship
Bullets = list[pygame.Rect]

@dataclass
class ShotFrequencyTime:
	time: int | float = 0
	last_shoot_time: int | float = 0
	shoot_freq: int = 115

	def can_shoot(self) -> bool:
		if self.time > self.last_shoot_time + self.shoot_freq:
			self.set_last_shoot_time(time = self.time)
			return True
		return False

	def set_time(self, new_time) -> None:
		self.time = new_time

	def set_last_shoot_time(self, time: int | float) -> None:
		self.last_shoot_time = time

def move_player(position_x: int, position_y: int, height: int, width: int) -> list[int]:
	frame = 0.9
	keys = pygame.key.get_pressed()

	new_position = [position_x, position_y]

	if keys[pygame.K_w] or keys[pygame.K_UP]:
		new_position = [position_x, move_character_y(position_y - frame, height)]
	if keys[pygame.K_s] or keys[pygame.K_DOWN]:
		new_position = [position_x, move_character_y(position_y + frame, height)]
	if keys[pygame.K_a] or keys[pygame.K_LEFT]:
		new_position = [move_character_x(position_x - frame, width), position_y]
	if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
		new_position = [move_character_x(position_x + frame, width), position_y]

	return new_position

def move_bullet(bullets: Bullets, frame: float | int) -> Bullets:
	firing_position = []

	if bullets:
		TOP_WINDOW = 0

		for fire in bullets:
			if fire.y > TOP_WINDOW:
				firing_position.append(
					pygame.Rect((fire.x, fire.y - frame), SIZE_BULLET)
				)

	return firing_position

def shoot(position: list[int], bullets: Bullets, time_shoot: ShotFrequencyTime) -> Bullets:
	frame = 2.8
	keys = pygame.key.get_pressed()
	firing_position = move_bullet(bullets = bullets, frame = frame)

	if time_shoot.can_shoot():
		if keys[pygame.K_SPACE]:
			bullet_x_position = position[0] + 12
			bullet_y_position = position[1] - (HEIGHT_SHIP / 2)
			firing_position.append(
				pygame.Rect((bullet_x_position, bullet_y_position), SIZE_BULLET)
			)

	else:
		firing_position = move_bullet(bullets = bullets, frame = frame)

	if firing_position:
		shots = [[BULLET_IMG, [shot.x, shot.y]] for shot in firing_position]
		draw_shots(shots)
		
	return firing_position.copy()


# Alien
def right_position_limit_alien(position_x) -> bool:
	RIGHT = WINDOW[0] - WIDTH_ALIEN
	return position_x == RIGHT

def left_position_limit_alien(position_x) -> bool:
	LEFT = 0
	return position_x == LEFT

def valid_move_alien(position_x: int, actual_move: str) -> tuple[str]:
	if right_position_limit_alien(position_x):
		return "left", "bottom"
	elif left_position_limit_alien(position_x):
		return "right", "bottom"

	return actual_move, "continue"

def move_alien(position_x: int, position_y: int, move: tuple[str], height: int, width: int) -> int:
	frame_x = 0.7
	frame_y = 10

	moving_alien_x = {
		"right": lambda: move_character_x(
			position_x = position_x + frame_x, 
			width = width
		),
		"left": lambda: move_character_x(
			position_x = position_x - frame_x, 
			width = width
		)
	}
	moving_alien_y = {
		"bottom": lambda: move_character_y(
			position_y = position_y + frame_y,
			height = height
		),
		"continue": lambda: position_y
	}

	move_x = move[0]
	move_y = move[1]

	new_position_x = moving_alien_x[move_x]()
	new_position_y = moving_alien_y[move_y]()

	return [new_position_x, new_position_y]

def is_alien_winner(position_y_alien:int) -> bool:
	return position_y_alien == (WINDOW[1] - 45)


# Collisions

@dataclass
class Character:
	position: list[int | float]
	image: Image = None

def collision_alien_ship(ship: Character, alien: Character) -> bool:
	game_over = False

	mask_ship = pygame.mask.from_surface(ship.image)
	mask_alien = pygame.mask.from_surface(alien.image)

	mask_collision = (ship.position[0] - alien.position[0], ship.position[1] - alien.position[1])

	if mask_alien.overlap(mask_ship, mask_collision):
		draw_character(
			character = EXPLOSION_IMG,
			position = ship.position
		)
		game_over = True

	return game_over

def collision_bullet_alien(alien: Character, bullets: Bullets) -> bool:
	game_over = False

	if not bullets:
		return game_over

	mask_alien = pygame.mask.from_surface(alien.image)
	mask_bullet = pygame.mask.from_surface(BULLET_IMG)

	for bullet in bullets:
		mask_collision = (bullet.x - alien.position[0], bullet.y - alien.position[1])
		if mask_alien.overlap(mask_bullet, mask_collision):
			draw_character(
				character = EXPLOSION_IMG,
				position = alien.position
			)
			game_over = True
	
	return game_over

def collision(ship: Character, alien: Character, bullets: Bullets) -> bool:
	has_true = True
	game_over = []
	
	game_over.append(collision_bullet_alien(alien = alien, bullets = bullets))
	game_over.append(collision_alien_ship(ship = ship, alien = alien))

	return has_true in game_over


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


if __name__ == '__main__':
	main()
