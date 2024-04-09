from sqlalchemy import Column, Text, ForeignKey, Integer

from app.core.db import Base
from .base import ProjectAndDonationBase


class Donation(ProjectAndDonationBase, Base):
    user_id = Column(Integer, ForeignKey(
        'user.id', name='fk_donation_user_id_user'
    ))
    comment = Column(Text)
