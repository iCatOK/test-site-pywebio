from dataclasses import dataclass
from typing import List
from classes.test_question import TestQuestion

@dataclass
class Test():
    id: int
    name: str
    description: str
    photo_url: str
    avg_score: float
    question_count: int
    play_count: int

    def __init__(self, test_tuple: tuple):
        self.id = test_tuple[0]
        self.name = test_tuple[1]
        self.description = test_tuple[2]
        self.photo_url = test_tuple[3]
        self.avg_score = test_tuple[4]
        self.question_count = test_tuple[5]
        self.play_count = test_tuple[6]
        
    
    def __str__(self) -> str:
        return f"Тест {self.name}: id-{self.id}, кол-во вопросов-{self.question_count}"

current_test: Test = None
test_question_set: List[TestQuestion] = None