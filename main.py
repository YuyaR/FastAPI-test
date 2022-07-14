from enum import Enum
from typing import Union, List

from fastapi import FastAPI, Path, Body, HTTPException
from pydantic import BaseModel


class ItemIn(BaseModel):
	name: str
	description: Union[str, None] = None
	price: float
	tax: float = None

class ItemWithoutTax(BaseModel):
	item_id: int
	name: str
	description: Union[str, None] = None
	price: float

class ItemOut(BaseModel):
	message: str
	item_info: Union[List[ItemWithoutTax], ItemWithoutTax]

class ItemDel(BaseModel):
	item_id: int
	# message: str = None

items_list = [
	{"item_id": 1, "name": "Foo", "description": 'generic item', "price": 5, "tax": 1},
	{"item_id": 2, "name": "Bar", "description": 'generic item', "price": 7},
	{"item_id": 3, "name": "Baz", "description": 'generic item', "price": 3, "tax": 0.3},
]

app = FastAPI()


@app.get("/")
async def root():
	return {"message": "Welcome to Yuya's warehouse"}

@app.get("/items/")
async def read_item_list(skip: int = 0, limit: int = 100):
	return items_list[skip : skip + limit]

@app.get("/items/{item_q}")
async def read_item(item_q):
	try:
		int(item_q)
	except ValueError:
		return read_item_by_name(item_q)
	return read_item_by_id(int(item_q))

def read_item_by_id(item_id: int):
	if item_id not in [itm["item_id"] for itm in items_list]:
		raise HTTPException(status_code=404, detail="Item not in the warehouse")
	item_filter = {"item_id": item_id}
	right_item = [dic for dic in items_list if all(dic[key] == val for key, val in item_filter.items())]
	return right_item

def read_item_by_name(name: str):
	if name not in [itm["name"] for itm in items_list]:
		raise HTTPException(status_code=404, detail="Item with this name not found")
	item_filter = {"name": name}
	right_item = [dic for dic in items_list if all(dic[key] == val for key, val in item_filter.items())]
	return right_item

@app.post("/items/", response_model=ItemOut, status_code=201)
async def create_item(
	item: ItemIn = Body(
		example = {
			"name": "yuya",
			"description": "a junior data analyst",
			"price":10,
			"tax":1.2,
		}
	)
):
	if item.tax:
		item.price += item.tax
	id_list = [itm["item_id"] for itm in items_list]
	item_dict = item.dict()
	item_dict.update(item_id = max(id_list)+1)
	items_list.append(item_dict)
	return {
		"message": "new item added successfully",
		"item_info": item_dict
	}

@app.delete("/items/", status_code=202)
async def delete_item(item: ItemDel):
	item_dict = dict(item)
	[items_list.remove(dic) for dic in items_list if (dic['item_id'] == item_dict['item_id'])]
