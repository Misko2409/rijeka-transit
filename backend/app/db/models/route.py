from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class Route(Base):
    __tablename__ = "routes"

    unique_id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
    )

    route_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    route_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    direction_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    direction: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    variant_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
