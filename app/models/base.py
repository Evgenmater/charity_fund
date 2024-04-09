from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime

from app.core.config import DEFAULT_AMOUNT
from app.core.db import Base


class ProjectAndDonationBase(Base):
    __abstract__ = True
    full_amount = Column(Integer, nullable=False)
    fully_invested = Column(Boolean, default=False)
    invested_amount = Column(Integer, default=DEFAULT_AMOUNT)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
