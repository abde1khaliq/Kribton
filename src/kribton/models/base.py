from typing import ClassVar
from sqlalchemy.orm import DeclarativeBase
from kribton.models.descriptor import QueryManagerDescriptor 


class BaseModel(DeclarativeBase):
    _registry: ClassVar[list[type]] = []
    _db: ClassVar = None
    objects = QueryManagerDescriptor()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "__tablename__"):
            BaseModel._registry.append(cls)