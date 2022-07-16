from sqlalchemy.orm import Session

from . import models, schema


def read_item_list(db: Session, skip: int = 0, limit: int = 100):
	return db.query(models.Item).offset(skip).limit(limit).all()

def read_item_by_id(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def read_item_by_name(db: Session, name: str):
	return db.query(models.Item).filter(models.Item.name == name).all()

def create_item(db: Session, item: schema.Item):
    new_item = models.Item(
        name=item.name,
        price=item.price,
        tax=item.tax,
        description=item.description,
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

def remove_item(db: Session, item: schema.ItemDel):
    item_del = db.query(models.Item).filter(models.Item.id == item.item_id)
    db.delete(item_del)
    db.commit()
    db.flush()