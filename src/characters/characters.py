from typing import Iterator
from dataclasses import dataclass

@dataclass
class MoveCharacter:
	TOP:str = "top"
	BOTTOM:str = "bottom"
	LEFT:str = "left"
	RIGHT:str = "right"

def move_character_x(position_x: int, width: int, screen_size: Iterator[int | float]) -> int | float:
	LEFT = 0
	RIGHT = screen_size[0] - width
	
	if position_x <= 0:
		position_x = 0
	elif position_x >= RIGHT:
		position_x = RIGHT

	return position_x

def move_character_y(position_y: int, height: int, screen_size: Iterator[int | float]) -> int | float:
	TOP = 0
	BOTTOM = screen_size[1] - height
	
	if position_y <= TOP:
		position_y = TOP
	elif position_y >= BOTTOM:
		position_y = BOTTOM

	return position_y