from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field


class CharityProjectBase(BaseModel):

    name: str = Field(..., max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)


class CharityProjectCreate(CharityProjectBase):

    pass


class CharityProjectUpdate(CharityProjectBase):

    name: Optional[str]
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[int]

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):

    id: int
    description: str
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
