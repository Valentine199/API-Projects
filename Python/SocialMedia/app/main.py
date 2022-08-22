from fastapi import FastAPI, Response, status, HTTPException, Depends

from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy.orm import Session

from . import Models
from .database import engine, get_db

Models.Base.metadata.create_all(bind=engine)
#  create the instance
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        # cursor seems to write into the database
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Asdfgh.1', cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("Database connected")
        break
    except Exception as error:
        print("Connection failed")
        print("Error was:", error)
        time.sleep(2)

# path operator or route
# If we are at this url we do this methode
@app.get("/")
# async we warn the methode that we do an asynchronous call
async def root():
    # return a JSON
    return {"message": "Hello World"}


@app.get("/test")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(Models.Post).all()
    return {"data": posts}



@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # the SQL first runs then we need to collect the results
    #cursor.execute("""SELECT * FROM POSTS""")
    #posts = cursor.fetchall()
    posts = db.query(Models.Post).all()
    return {"data": posts}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Models.Post).filter(Models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    return {"post": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # same methode but for our changes to take place we also have to commit our changes
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    # conn.commit()

    new_post = Models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}
# title str, content str, category


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(Models.Post).filter(Models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} doesn't exist")

    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    post_query = db.query(Models.Post).filter(Models.Post.id == id)
    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} doesn't exist")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return {'data': post_query.first()}

