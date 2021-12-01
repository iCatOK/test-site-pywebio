from dataclasses import dataclass
from datetime import datetime

@dataclass
class TestResult():
    id: int
    user_id: int
    test_id: int
    score: int
    date: datetime

    def __init__(self, res_tuple: tuple):
        self.id = res_tuple[0]
        self.user_id = res_tuple[1]
        self.test_id = res_tuple[2]
        self.score = res_tuple[3]
        self.date = res_tuple[4]
    
    def __str__(self) -> str:
        return f"Результат пользователя #{self.user_id} id-{self.id}, счёт-{self.score}"