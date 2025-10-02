from pydantic import BaseModel
from typing import List

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class ChoiceCreate(ChoiceBase):
    pass 

class Choice(ChoiceBase):
    id: int
    question_id: int

    class Config:
        from_attributes = True


class QuestionBase(BaseModel):
    question_text: str

class QuestionCreate(QuestionBase):
    choices: List[ChoiceCreate] 

class Question(QuestionBase):
    id: int
    choices: List[Choice] = [] 

    class Config:
        from_attributes = True