from enum import IntEnum
from collections import defaultdict

class EnemyType(IntEnum):
	NORMAL = 1
	BOSS = 2

class ScoreEnemyType(IntEnum):
	NORMAL = 10
	BOSS = 100

class ManagerScore:
	def __init__(self):
		self._score: int = 0
		self._ScoreType: dict[str, int] = defaultdict(
			lambda: False,
			{
				EnemyType.NORMAL: ScoreEnemyType.NORMAL,
				EnemyType.BOSS: ScoreEnemyType.BOSS
			}
		)

	def get_total_score(self) -> int:
		return self._score

	def add_point(self, enemy_type: int) -> int:

		score = self._ScoreType[enemy_type]
		
		if score:
			self._score += score
