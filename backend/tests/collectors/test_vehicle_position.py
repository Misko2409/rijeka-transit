import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.app.collectors.vehicle_position import VehiclePositionCollector


@pytest.mark.anyio
async def test_collector_collects_repeated_snapshots() -> None:
    service = MagicMock()
    service.collect_snapshot = AsyncMock(
        side_effect=[
            100,
            95,
            asyncio.CancelledError(),
        ]
    )

    collector = VehiclePositionCollector(
        service=service,
        interval_seconds=15.0,
    )

    with (
        patch(
            "backend.app.collectors.vehicle_position.asyncio.sleep",
            new=AsyncMock(),
        ),
        pytest.raises(asyncio.CancelledError),
    ):
        await collector.run()

    assert service.collect_snapshot.await_count == 3


@pytest.mark.anyio
async def test_collector_continues_after_snapshot_failure() -> None:
    service = MagicMock()
    service.collect_snapshot = AsyncMock(
        side_effect=[
            RuntimeError("Temporary failure"),
            87,
            asyncio.CancelledError(),
        ]
    )

    collector = VehiclePositionCollector(
        service=service,
        interval_seconds=15.0,
    )

    with (
        patch(
            "backend.app.collectors.vehicle_position.asyncio.sleep",
            new=AsyncMock(),
        ),
        pytest.raises(asyncio.CancelledError),
    ):
        await collector.run()

    assert service.collect_snapshot.await_count == 3


@pytest.mark.anyio
async def test_collector_propagates_cancellation() -> None:
    service = MagicMock()
    service.collect_snapshot = AsyncMock(side_effect=asyncio.CancelledError())

    collector = VehiclePositionCollector(
        service=service,
        interval_seconds=15.0,
    )

    with pytest.raises(asyncio.CancelledError):
        await collector.run()

    service.collect_snapshot.assert_awaited_once()
