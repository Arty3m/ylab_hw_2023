import uvicorn
from typing import Union

from fastapi import FastAPI

from src.models import menu as mn
from src.core import config
from src.api.v1.resources import menu, submenu, dish
from src.db import SessionLocal, engine

# make migrations all of tables to db
# mn.Base.metadata.create_all(engine)

app = FastAPI(
    title=config.PROJECT_NAME,
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


app.include_router(router=menu.router, prefix='/api/v1')
app.include_router(router=submenu.router, prefix='/api/v1/menus/{menu_id}')
app.include_router(router=dish.router, prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}')

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
