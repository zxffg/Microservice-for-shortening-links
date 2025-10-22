from fastapi import FastAPI, Depends, status
import uvicorn
from pydantic import BaseModel
import validators
from sqlalchemy.orm import Session
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

@app.post("/link_post", status_code=status.HTTP_201_CREATED)
async def link_create(link: LinkCreate, db: Session = Depends(get_db)):
    code = generate_code()
    db_link = Link(url=link.link, short_code=code)
    if validators.url(link.link):   
        db.add(db_link)
        db.commit()
        db.refresh(db_link)
        return {"message": True, "link": link}
    else:
        return {"message": False}
    



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)