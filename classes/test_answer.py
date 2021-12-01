from dataclasses import  dataclass

@dataclass
class TestAnswer():
    id: int
    question_id: int
    answer_text: str
    is_right: bool

    def __init__(self, q_tuple: tuple):
        self.id = q_tuple[0]
        self.question_id = q_tuple[1]
        self.answer_text = q_tuple[2]
        self.is_right = bool(q_tuple[3])
    
    def __str__(self) -> str:
        return f"Ответ для вопроса #{self.question_id} <{self.answer_text}>, правильно={self.is_right}"