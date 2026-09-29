from geoalchemy2 import Geography
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class Stop(Base):
    __tablename__ = "stops"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    short_name: Mapped[str | None] = mapped_column(
        String(255),
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

    direction: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    direction_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    opposite_stop_id: Mapped[int | None] = mapped_column(
        ForeignKey("stops.id"),
        nullable=True,
    )
