import os
from typing import Union, List

from .database import engine, SessionLocal
from . import crud, models, schema

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Body, HTTPException
from sqlalchemy.orm import Session

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
	return {"message": "Welcome to Yuya's warehouse"}

@app.get("/items/", response_model=schema.ItemRecall)
async def read_item_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	items = crud.read_item_list(db=db, skip=skip, limit=limit)
	if items is None or len(items) == 0:
		raise HTTPException(
			status_code=404,
			detail="Not that many items in the warehouse",
		)
	return {
		"message": "Here are your search results",
		"item_info": items,
	}

@app.get("/items/{item_q}", response_model=Union[schema.Item, List[schema.Item]])
async def read_item(item_q: Union[int, str], db: Session = Depends(get_db)):
	try:
		int(item_q)
		items = crud.read_item_by_id(db=db, item_id=int(item_q))
	except ValueError:
		items = crud.read_item_by_name(db=db, name=item_q)
	if items is None or len(items) == 0:
		raise HTTPException(status_code=404, detail="Item not in the warehouse") 
	return items

@app.post("/items/", response_model=schema.ItemRecall, status_code=201)
async def create_item(
	item: schema.ItemBase = Body(
		example = {
			"name": "yuya",
			"description": "a junior data analyst",
			"price":10,
			"tax":1.2,
		}
	),
	db: Session = Depends(get_db)
):
	return {
		"message": "new item added successfully",
		"item_info": crud.create_item(db=db, item=item)
	}

@app.delete("/items/", status_code=202)
async def delete_item(item: schema.ItemDel, db: Session = Depends(get_db)):
	crud.remove_item(db=db, item=item)
