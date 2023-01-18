import uvicorn
from fastapi import FastAPI

from src.core import config
from src.api.v1.resources import menu, submenu, dish

app = FastAPI(
    title=config.PROJECT_NAME,
)


@app.get("/")
def read_root():
    return {"Hello": "YLab"}


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
