from dataclasses import  dataclass
from typing import List
from classes.test_answer import TestAnswer

@dataclass
class TestQuestion():
    id: int
    test_id: int
    question: str
    question_photo_url: str

    def __init__(self, q_tuple: tuple):
        self.id = q_tuple[0]
        self.test_id = q_tuple[1]
        self.question = q_tuple[2]
        self.question_photo_url = q_tuple[3]
    
    def __str__(self) -> str:
        return f"Вопрос для теста #{self.test_id} <{self.question}>"

test_answer_set: List[TestAnswer] = None