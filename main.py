from fastapi import Depends, FastAPI, HTTPException, Response, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import crud, models, schemas
from db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# Créer une instance de Jinja2Templates
templates = Jinja2Templates(directory="templates")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/", response_model=list[schemas.User])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/{user_id}/posts/", response_model=list[schemas.Post])
async def get_user_posts(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    posts = crud.get_user_posts(db, user_id, skip, limit)
    return posts

@app.post("/users/new", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/users/{user_id}/posts/new", response_model=schemas.Post)
async def create_post_for_user(user_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_user_post(db=db, post=post, user_id=user_id)

@app.delete("/users/{user_id}/delete_post/{post_id}")
async def delete_post_for_user(user_id: int, post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.author == user_id, models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="User or Post not found")
    crud.delete_user_post(db=db, post=db_post)
    return {"msg": "Successfully Deleted"}

# Route pour afficher la page index.html
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/posts", response_class=HTMLResponse)
async def show_posts(request: Request, db: Session = Depends(get_db)):

    
    posts = crud.get_posts(db)

    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts})



