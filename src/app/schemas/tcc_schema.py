from pydantic import BaseModel
from app.models.tcc_model import User_Type


class TCC_DTO(BaseModel):
    authorId: str
    authorEmail: str
    title: str
    body: str
    type: User_Type


class TCC_list_DTO(BaseModel):
    __root__: list[TCC_DTO]
