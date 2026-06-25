from sqlalchemy import select
from kribton.db.base_query_manager import BaseQueryManager

class AsyncQueryManager(BaseQueryManager):
    async def all(self):
        async with self.db.session() as session:
            result = await session.execute(select(self.model))
            rows = result.scalars().all()
            return [self.serialize(row) for row in rows]

    def serialize(self, obj):
        return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
