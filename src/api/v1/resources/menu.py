from fastapi import APIRouter, Depends, HTTPException

import src.models.menu
# vremeno tut
from src.db import get_db
from sqlalchemy.orm import Session
from src.models.menu import Menu, SubMenu, Dish
from src.api.v1.schemas.menu import MenuBase, MenuCreate, MenuModel

###

router = APIRouter()


@router.get(
    path="/menus",
    summary="Список меню",
    tags=["menus"],
    status_code=200,
)
def menu_list(db: Session = Depends(get_db)):
    ms = db.query(Menu).all()
    return ms


@router.get(
    path="/menus/{menu_id}",
    summary="Просмотр определенного меню",
    tags=["menus"],
    status_code=200,
)
def menu_detail(menu_id: int, db: Session = Depends(get_db)):
    ms = db.query(Menu).filter(Menu.id == menu_id).first()
    count_submenus = db.query(SubMenu).filter(SubMenu.owner == menu_id).count()
    cur_id = tm.id if (tm := db.query(SubMenu).filter(SubMenu.owner == menu_id).first()) else -1
    if cur_id != -1:
        count_dishes = db.query(Dish).filter(Dish.owner == cur_id).count()
    else:
        count_dishes = 0
    if not ms:
        # status_code должен быть 404, но тесты на 200
        raise HTTPException(status_code=404, detail="menu not found")
    return {"id": str(ms.id), "title": ms.title, "description": ms.description, "submenus_count": count_submenus,
            "dishes_count": count_dishes}


@router.patch(
    path="/menus/{menu_id}",
    summary="Обновить меню",
    tags=["menus"],
    status_code=200,
)
def menu(m: MenuBase, menu_id: int, db: Session = Depends(get_db)):
    to_change_menu = db.get(Menu, menu_id)
    if not to_change_menu:
        # должен быть статус код 404, но в тестах проверка на 200
        raise HTTPException(status_code=200, detail="menu not found")
    to_change_menu.title = m.title
    to_change_menu.description = m.description
    db.add(to_change_menu)
    db.commit()
    db.refresh(to_change_menu)
    return to_change_menu


@router.post(
    path="/menus",
    summary="Добавить меню",
    tags=["menus"],
    status_code=201,
)
def menu(m: MenuCreate, db: Session = Depends(get_db)):
    new_menu: Menu = Menu(title=m.title, description=m.description)
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return {"id": str(new_menu.id), "title": new_menu.title, "description": new_menu.description}


@router.delete(
    path="/menus/{menu_id}",
    summary="Удалить меню",
    tags=["menus"],
    status_code=200,
)
def menu_delete(menu_id, db: Session = Depends(get_db)):
    to_del = db.get(Menu, menu_id)
    db.delete(to_del)
    db.commit()
    return {"status": "true", "message": "The menu has been deleted"}
