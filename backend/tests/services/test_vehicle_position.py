from unittest.mock import AsyncMock, MagicMock

import pytest

from backend.app.models.external.autotrolej.vehicle import (
    AutotrolejVehicle,
    AutotrolejVehiclesResponse,
)
from backend.app.services.vehicle_position import VehiclePositionService


def create_session_factory() -> tuple[MagicMock, MagicMock]:
    session = MagicMock()
    session_context = MagicMock()
    session_context.__enter__.return_value = session

    session_factory = MagicMock(return_value=session_context)

    return session_factory, session


@pytest.mark.anyio
async def test_collect_snapshot_commits_vehicle_positions() -> None:
    client = MagicMock()
    client.get_buses = AsyncMock(
        return_value=AutotrolejVehiclesResponse(
            msg="ok",
            res=[
                AutotrolejVehicle(
                    gbr=773,
                    lon=14.446925,
                    lat=45.323968,
                    voznjaId=None,
                    voznjaBusId=2214313,
                ),
                AutotrolejVehicle(
                    gbr=811,
                    lon=14.451234,
                    lat=45.329876,
                    voznjaId=1433806,
                    voznjaBusId=2214314,
                ),
            ],
            err=False,
        )
    )

    session_factory, session = create_session_factory()

    service = VehiclePositionService(
        autotrolej_client=client,
        session_factory=session_factory,
    )

    inserted_count = await service.collect_snapshot()

    assert inserted_count == 2

    client.get_buses.assert_awaited_once()
    session_factory.assert_called_once()
    session.execute.assert_called_once()
    session.commit.assert_called_once()
    session.rollback.assert_not_called()


@pytest.mark.anyio
async def test_collect_snapshot_rolls_back_on_database_error() -> None:
    client = MagicMock()
    client.get_buses = AsyncMock(
        return_value=AutotrolejVehiclesResponse(
            msg="ok",
            res=[
                AutotrolejVehicle(
                    gbr=773,
                    lon=14.446925,
                    lat=45.323968,
                    voznjaId=None,
                    voznjaBusId=2214313,
                ),
            ],
            err=False,
        )
    )

    session_factory, session = create_session_factory()
    session.execute.side_effect = RuntimeError("Database error")

    service = VehiclePositionService(
        autotrolej_client=client,
        session_factory=session_factory,
    )

    with pytest.raises(RuntimeError, match="Database error"):
        await service.collect_snapshot()

    session_factory.assert_called_once()
    session.commit.assert_not_called()
    session.rollback.assert_called_once()


@pytest.mark.anyio
async def test_collect_empty_snapshot_commits_without_insert() -> None:
    client = MagicMock()
    client.get_buses = AsyncMock(
        return_value=AutotrolejVehiclesResponse(
            msg="ok",
            res=[],
            err=False,
        )
    )

    session_factory, session = create_session_factory()

    service = VehiclePositionService(
        autotrolej_client=client,
        session_factory=session_factory,
    )

    inserted_count = await service.collect_snapshot()

    assert inserted_count == 0

    client.get_buses.assert_awaited_once()
    session_factory.assert_called_once()
    session.execute.assert_not_called()
    session.commit.assert_called_once()
    session.rollback.assert_not_called()


@pytest.mark.anyio
async def test_each_snapshot_uses_a_new_session() -> None:
    client = MagicMock()
    client.get_buses = AsyncMock(
        return_value=AutotrolejVehiclesResponse(
            msg="ok",
            res=[],
            err=False,
        )
    )

    first_session = MagicMock()
    first_context = MagicMock()
    first_context.__enter__.return_value = first_session

    second_session = MagicMock()
    second_context = MagicMock()
    second_context.__enter__.return_value = second_session

    session_factory = MagicMock(
        side_effect=[
            first_context,
            second_context,
        ]
    )

    service = VehiclePositionService(
        autotrolej_client=client,
        session_factory=session_factory,
    )

    await service.collect_snapshot()
    await service.collect_snapshot()

    assert session_factory.call_count == 2

    first_session.commit.assert_called_once()
    second_session.commit.assert_called_once()

    first_context.__exit__.assert_called_once()
    second_context.__exit__.assert_called_once()
