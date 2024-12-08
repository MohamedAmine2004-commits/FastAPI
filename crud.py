from sqlalchemy.orm import Session
import models, schemas
from typing import List


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_posts(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Post).filter(models.Post.author == user_id).offset(skip).limit(limit).all()

def create_user_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(title=post.title, content=post.content, author=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_user_post(db: Session, post: models.Post):
    db.delete(post)
    db.commit()



def get_posts(db: Session, skip: int = 0, limit: int = 100) -> List[models.Post]:
    
    return db.query(models.Post).offset(skip).limit(limit).all()