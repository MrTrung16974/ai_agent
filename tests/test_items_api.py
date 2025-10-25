import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db import get_db
from app.main import app
from app.models import Base


@pytest.fixture()
async def async_client():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
    TestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.mark.anyio
async def test_crud_flow(async_client: AsyncClient):
    payload = {"name": "Test Item", "description": "A test item", "price": 12.5}
    response = await async_client.post("/items/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    created_item = response.json()
    assert created_item["id"] > 0
    assert created_item["name"] == payload["name"]

    item_id = created_item["id"]

    response = await async_client.get(f"/items/{item_id}")
    assert response.status_code == status.HTTP_200_OK
    fetched_item = response.json()
    assert fetched_item["description"] == payload["description"]

    update_payload = {"price": 25.0}
    response = await async_client.put(f"/items/{item_id}", json=update_payload)
    assert response.status_code == status.HTTP_200_OK
    updated_item = response.json()
    assert float(updated_item["price"]) == update_payload["price"]

    response = await async_client.delete(f"/items/{item_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = await async_client.get(f"/items/{item_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
