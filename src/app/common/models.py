from datetime import datetime, timedelta, timezone

from sqlalchemy import Column, DateTime, event


class TimeStampMixin:
    """Timestamping mixin"""

    kathmandu_time = timedelta(hours=5, minutes=45)
    kathmandu_tz = timezone(kathmandu_time)
    created_at = Column(DateTime, default=datetime.now(kathmandu_tz))
    created_at._creation_order = 9998
    updated_at = Column(DateTime, default=datetime.now(kathmandu_tz))
    updated_at._creation_order = 9998

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = default = datetime.now(  # noqa: 841
            TimeStampMixin.kathmandu_tz
        )

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "before_update", cls._updated_at)
