from typing import Union, List

from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    price: float
    description: Union[str, None] = None
    tax: Union[float, None] = None

    class Config:
        orm_mode=True

class Item(ItemBase):
    item_id: int

    class Config:
        orm_mode=True

class ItemRecall(ItemBase):
	message: str
	item_info: Union[List[Item], Item]

class ItemDel(BaseModel):
	item_id: int