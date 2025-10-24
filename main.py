from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.responses import RedirectResponse
import uvicorn
from pydantic import BaseModel
import validators
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db, Link
import random, string

import traceback

app = FastAPI()

@app.get("/")
def read_root():
    return True


#? Добавление данных
class LinkCreate(BaseModel):
    link: str

def generate_code(lenght=9):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=lenght))

# @app.post("/link_post", status_code=status.HTTP_201_CREATED)
# async def link_create(link: LinkCreate, db: Session = Depends(get_db)):
#     try:
#         if not validators.url(link.link):
#             return {"message": False}

#         db_link = Link(url=link.link)
#         db.add(db_link)
#         db.commit()
#         db.refresh(db_link)

#         return {"message": True, "link": db_link.url}
#     except Exception as e:
#         traceback.print_exc()  # покажет ошибку в консоли
#         return {"error": str(e)}

def generate_code(lenght=9):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=lenght))

#! Добавление ссылки и получение короткого кода с ссылкой
base_url = "http://localhost:8000/"
@app.post("/link/{post_link}", status_code=status.HTTP_201_CREATED)
async def link_create(link: LinkCreate, db: Session = Depends(get_db)):
    code = generate_code()
    short_url = f"{base_url}{code}"
    db_link = Link(url=link.link, short_code=code, short_url=short_url)
    if validators.url(link.link) == True:   
        db.add(db_link)
        db.commit()
        db.refresh(db_link)
        return {"message": True, "link": link, "short_code": code, "short_url": short_url}
    else:
        return {"message": False}

#! Переадресация по короткой ссылке
@app.get("/redirect/{short_code}")
async def redirect_short_link(short_code: str, db: Session = Depends(get_db)):
    db_link = db.query(Link).filter(Link.short_code == short_code).first()
    if not db_link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Link not found")
    else:
        return RedirectResponse(url=db_link.url)

@app.delete("/clear_links", status_code=status.HTTP_200_OK)
async def clear_links(db: Session = Depends(get_db)):
    try:
        db.execute(text("DELETE FROM lincore"))
        db.commit()
        return {"message": True}
    except Exception as e:
        db.rollback()
        return {"message": False, "error": str(e)}



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)