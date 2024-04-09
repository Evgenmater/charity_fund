from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonateBase(BaseModel):

    full_amount: int = Field(..., gt=0)
    comment: Optional[str]


class DonationCreate(DonateBase):

    pass


class DonationDB(DonateBase):

    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationAdminDB(DonationDB):

    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
