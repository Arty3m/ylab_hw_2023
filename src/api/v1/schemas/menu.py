from datetime import datetime

from pydantic import BaseModel

__all__ = (
    "MenuBase",
    "MenuCreate",
    "MenuModel"
)


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    ...


class MenuModel(MenuBase):
    id: str

# class PostModel(PostBase):
#     id: int
#     created_at: datetime
#
#
# class PostListResponse(BaseModel):
#     posts: list[PostModel] = []
