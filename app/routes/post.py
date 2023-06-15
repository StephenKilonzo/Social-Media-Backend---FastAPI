from typing import List, Annotated
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=['Post']
)


@router.get("/", response_model=List[schemas.Post])
async def get_post(db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM post")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post: schemas.PostCreate,   db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("INSERT INTO post(title, content, published) VALUES (%s, %s, %s) RETURNING *",(post.title, post.content, post.published))
    # new_post = cursor.fetchall()
    # conn.commit()

    new_post =models.Post(owner_id = current_user.id, **post.dict())
    # new_post = models.Post(title = post.title, content= post.content, published= post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
 
  
@router.get("/{id}", response_model=schemas.Post)
async def get_post(id: int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * from post WHERE id = %s", (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorised to delete the post.")
    
    return post


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("DELETE FROM post WHERE id = %s returning *",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_quary = db.query(models.Post).filter(models.Post.id == id)

    post = post_quary.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorised to delete the post.")
    
    post_quary.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.Post)
async def update_post(id: int, updated_post: schemas.PostCreate, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()

    update_post = db.query(models.Post).filter(models.Post.id == id)
    post = update_post.first()

    if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist.")
 
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorised to delete the post.")
    
    update_post.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return update_post.first()