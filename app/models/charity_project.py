from sqlalchemy import Column, String, Text

from app.core.config import MAX_LENGTH
from app.core.db import Base
from .base import ProjectAndDonationBase


class CharityProject(ProjectAndDonationBase, Base):
    name = Column(String(MAX_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)
