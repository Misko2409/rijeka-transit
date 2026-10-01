from datetime import datetime

from geoalchemy2 import Geography
from sqlalchemy import BigInteger, DateTime, Index, Integer
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class VehiclePosition(Base):
    __tablename__ = "vehicle_positions"

    __table_args__ = (
        Index(
            "ix_vehicle_positions_vehicle_recorded_at",
            "vehicle_number",
            "recorded_at",
        ),
        Index(
            "ix_vehicle_positions_recorded_at",
            "recorded_at",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    vehicle_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    trip_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    vehicle_trip_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    location: Mapped[object] = mapped_column(
        Geography(
            geometry_type="POINT",
            srid=4326,
            spatial_index=False,
        ),
        nullable=False,
    )

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
