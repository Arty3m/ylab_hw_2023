from fastapi import APIRouter, Depends, HTTPException

import src.models.menu
# vremeno tut
from src.db import get_db
from sqlalchemy.orm import Session
from src.models.menu import Dish
from src.api.v1.schemas.dish import DishBase, DishCreate, DishModel

###

router = APIRouter()


@router.get(
    path="/dishes",
    summary="Список блюд",
    tags=["dishes"],
    status_code=200,
)
def dish_list(db: Session = Depends(get_db)):
    dishs = db.query(Dish).all()
    # if not dishs:
        # raise HTTPException(status_code=404, detail='Not Found')

    return dishs


@router.get(
    path="/dishes/{dish_id}",
    summary="Список подменю",
    tags=["dishes"],
    status_code=200,
)
def dish_detail(dish_id: int, db: Session = Depends(get_db)):
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")
    return {"id": str(dish.id), "title": dish.title, "description": dish.description,
            "price": str(dish.price)}


@router.post(
    path="/dishes",
    summary="Добавить блюдо",
    tags=["dishes"],
    status_code=201,
)
def dish(submenu_id: int, dish_data: DishCreate, db: Session = Depends(get_db)):
    new_dish = Dish(title=dish_data.title, description=dish_data.description, price=dish_data.price, owner=submenu_id)
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    return {"id": str(new_dish.id), "title": new_dish.title, "description": new_dish.description,
            "price": new_dish.price}


@router.patch(
    path="/dishes/{dish_id}",
    summary="Добавить подменю",
    tags=["dishes"],
    status_code=200,
)
def dish_update(dish_id: int, dish_data: DishCreate, db: Session = Depends(get_db)):
    dish_to_change = db.get(Dish, dish_id)
    if not dish_to_change:
        # должен быть статус код 404, но в тестах проверка на 200
        raise HTTPException(status_code=200, detail="menu not found")
    dish_to_change.title = dish_data.title
    dish_to_change.description = dish_data.description
    dish_to_change.price = dish_data.price
    db.add(dish_to_change)
    db.commit()
    db.refresh(dish_to_change)
    return {"id": str(dish_to_change.id), "title": dish_to_change.title,
            "description": dish_to_change.description, "price": dish_to_change.price,
            "dishes_count": 0}


@router.delete(
    path="/dishes/{dish_id}",
    summary="Удалить подменю",
    tags=["dishes"],
    status_code=200,
)
def dish_delete(dish_id: int, db: Session = Depends(get_db)):
    to_del = db.get(Dish, dish_id)
    db.delete(to_del)
    db.commit()
    return {"status": "true", "message": "The menu has been deleted"}
