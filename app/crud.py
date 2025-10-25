from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


class ItemCRUD:
    async def get(self, session: AsyncSession, item_id: int) -> models.Item | None:
        result = await session.execute(select(models.Item).where(models.Item.id == item_id))
        return result.scalar_one_or_none()

    async def get_multi(self, session: AsyncSession, skip: int = 0, limit: int = 100) -> Sequence[models.Item]:
        result = await session.execute(
            select(models.Item).offset(skip).limit(limit).order_by(models.Item.id)
        )
        return result.scalars().all()

    async def create(self, session: AsyncSession, item_in: schemas.ItemCreate) -> models.Item:
        item = models.Item(**item_in.dict())
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item

    async def update(
        self,
        session: AsyncSession,
        item: models.Item,
        item_in: schemas.ItemUpdate,
    ) -> models.Item:
        for field, value in item_in.dict(exclude_unset=True).items():
            setattr(item, field, value)
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item

    async def remove(self, session: AsyncSession, item: models.Item) -> None:
        await session.delete(item)
        await session.commit()


item_crud = ItemCRUD()
