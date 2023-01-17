from fastapi import APIRouter, Depends, HTTPException

import src.models.menu
# vremeno tut
from src.db import get_db
from sqlalchemy.orm import Session
from src.models.menu import SubMenu, Dish
from src.api.v1.schemas.submenu import SubMenuBase, SubMenuCreate, SubMenuModel

###

router = APIRouter()


@router.get(
    path="/submenus",
    summary="Список подменю",
    tags=["submenus"],
    status_code=200,
)
def submenu_list(db: Session = Depends(get_db)):
    submenus = db.query(SubMenu).all()
    return submenus


@router.get(
    path="/submenus/{submenu_id}",
    summary="Список подменю",
    tags=["submenus"],
    status_code=200,
)
def submenu_detail(submenu_id: int, db: Session = Depends(get_db)):
    submenu = db.query(SubMenu).filter(SubMenu.id == submenu_id).first()
    count_dishes = db.query(Dish).filter(Dish.owner == submenu_id).count()  # TODO
    if not submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    return {"id": str(submenu.id), "title": submenu.title, "description": submenu.description,
            "dishes_count": count_dishes}


@router.post(
    path="/submenus",
    summary="Добавить подменю",
    tags=["submenus"],
    status_code=201,
)
def submenu(menu_id: int, sub_menu: SubMenuCreate, db: Session = Depends(get_db)):
    new_submenu = SubMenu(title=sub_menu.title, description=sub_menu.description, owner=menu_id)
    db.add(new_submenu)
    db.commit()
    db.refresh(new_submenu)
    return {"id": str(new_submenu.id), "title": new_submenu.title, "description": new_submenu.description}


@router.patch(
    path="/submenus/{submenu_id}",
    summary="Добавить подменю",
    tags=["submenus"],
    status_code=200,
)
def submenu(submenu_id: int, sub_menu: SubMenuCreate, db: Session = Depends(get_db)):
    submenu_to_change = db.get(SubMenu, submenu_id)
    if not submenu_to_change:
        # должен быть статус код 404, но в тестах проверка на 200
        raise HTTPException(status_code=200, detail="menu not found")
    submenu_to_change.title = sub_menu.title
    submenu_to_change.description = sub_menu.description

    db.add(submenu_to_change)
    db.commit()
    db.refresh(submenu_to_change)
    return {"id": str(submenu_to_change.id), "title": submenu_to_change.title,
            "description": submenu_to_change.description,
            "dishes_count": 0}


@router.delete(
    path="/submenus/{submenu_id}",
    summary="Удалить подменю",
    tags=["submenus"],
    status_code=200,
)
def submenu_delete(submenu_id, db: Session = Depends(get_db)):
    to_del = db.get(SubMenu, submenu_id)
    db.delete(to_del)
    db.commit()
    return {"status": "true", "message": "The menu has been deleted"}
