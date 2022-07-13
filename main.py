from enum import Enum
from typing import Union

from fastapi import FastAPI, Path, Body, HTTPException
from pydantic import BaseModel


class ModelName(str, Enum):
	alexnet = "alexnet"
	resnet = "resnet"
	lenet = "lenet"

class ItemIn(BaseModel):
	name: str
	description: Union[str, None] = None
	price: float
	tax: float = None

class ItemOut(BaseModel):
	name: str
	description: Union[str, None] = None
	price: float

items_list = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

app = FastAPI()


@app.get("/")
async def root():
	return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
	return {"item_id:": item_id}

@app.get("/model/{model_name}")
async def get_model(model_name: ModelName):
	if model_name == ModelName.alexnet:
		return{"model_name": model_name}
	elif model_name.value == "lenet":
		return{"model_name": model_name}
	else:
		return{"message": "no such model available"}

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
	return {"file_path": file_path}

@app.get("/items/")
async def read_item_list(skip: int = 0, limit: int = 0):
	return items_list[skip : skip + limit]

@app.get("/items/name/")
async def read_item_name(loc: int = 0, size: int = None):
	if loc >= len(items_list):
		raise HTTPException(status_code=404, detail="Item not found")
	if size:
		return {"item_name": items_list[loc]["item_name"], "size": size}
	return {"item_name": items_list[loc]["item_name"], "size": "Free"}

@app.post("/users/{user_id}/items/", response_model=ItemOut, status_code=201)
async def create_item(
	*,
	user_id: int = Path(title="Student ID of User", default=1),
	item: ItemIn = Body(
		example = {
				"name": "yuya",
				"description": "a junior data analyst",
				"price":11.2,
				"tax":1.2,
		}
	)
):
	if item.tax:
		item.price += item.tax
	return item

@app.get("/users/{user_id}/items/{item_id}")
async def read_owned_items(user_id: int, item_id: int, short: bool = True):
	item = {"user_id": user_id, "item_id": item_id}
	if short is False:
		item.update({"description": "This is just extra words"})
	return item
