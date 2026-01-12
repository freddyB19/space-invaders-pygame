from typing import Protocol, Any

from src.characters.bullet.bullet import Bullet

class IBulletPool(Protocol):
	def get(self) -> Bullet:
		pass

	def release(self, resorce: Bullet) -> None:
		pass
