from datetime import datetime

from pydantic import BaseModel

__all__ = (
    "SubMenuBase",
    "SubMenuCreate",
    "SubMenuModel"
)


class SubMenuBase(BaseModel):
    title: str
    description: str


class SubMenuCreate(SubMenuBase):
    ...


class SubMenuModel(SubMenuBase):
    id: str

# class PostModel(PostBase):
#     id: int
#     created_at: datetime
#
#
# class PostListResponse(BaseModel):
#     posts: list[PostModel] = []
