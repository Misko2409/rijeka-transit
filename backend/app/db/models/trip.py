from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    route_unique_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("routes.unique_id"),
        nullable=False,
    )

    vehicle_trip_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
