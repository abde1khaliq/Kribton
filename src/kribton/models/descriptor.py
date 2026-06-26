class QueryManagerDescriptor:
    """Resolves the query manager at access time, not at import time."""

    def __get__(self, obj, cls):
        if cls is None:
            return self
        if BaseModel._db is None:
            raise RuntimeError(
                f"Database not initialized. Create AsyncDatabase before accessing "
                f"{cls.__name__}.objects"
            )
        manager = BaseModel._db._make_manager(cls)
        setattr(cls, "_objects_cache", manager)
        return manager