from fastapi import FastAPI, HTTPException, Depends
from typing import List, Annotated
import models
import schemas 
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/questions/",response_model=List[schemas.Question])
def read_questions(db:db_dependency):
  
  questions = db.query(models.Questions).all()
  return questions


@app.get("/questions/{question_id}", response_model=schemas.Question)
def read_question(question_id:int,db: db_dependency):
  
  question=db.query(models.Questions).filter(question_id==models.Questions.id).first()
  if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
  return question

@app.get("/{question_id:int}/choices",response_model=List[schemas.Choice])
def read_choices(question_id:int,db:db_dependency):
  
  choices = db.query(models.Choices).filter(question_id==models.Choices.question_id).all()
 
  return choices


@app.post('/questions/', response_model=schemas.Question)
def create_question(question: schemas.QuestionCreate, db: db_dependency):
       
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question) 

    for choice_data in question.choices:
        db_choice = models.Choices(
            choice_text=choice_data.choice_text,
            is_correct=choice_data.is_correct,
            question_id=db_question.id  
        )
        db.add(db_choice)

    db.commit()
    db.refresh(db_question)
    
    return db_question
