from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_user_donations(
        self,
        user: User,
        session: AsyncSession,
    ) -> list[Donation]:
        """
        Возвращать список объектов Donation.
        Связанный с пользователем, выполняющим запрос.
        """
        user_donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        user_donations = user_donations.scalars().all()

        return user_donations


donation_crud = CRUDDonation(Donation)