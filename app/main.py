from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routes import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password='Stivkilosj@01', port= '5432', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connected successfully.")
#         break
#     except Exception as error:
#         print("Connection to the database failed: ", error)
#         time.sleep(3)





# @app.get("/sqlalchemy")
# def test_post(db:Session = Depends(get_db)):
#     post = db.query(models.Post).all()
#     return {"data": post}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {'message': "welcome"}

