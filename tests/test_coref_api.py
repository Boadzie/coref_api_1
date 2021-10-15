import coref_api.main as main
import pytest
from httpx import AsyncClient


@pytest.fixture
async def async_app_client():
    async with AsyncClient(app=main.app, base_url="http://test") as client:
        yield client
        

@pytest.mark.asyncio
async def test_app(async_app_client):
    payload = {"text": "My sister has a dog. She loves him."}

    response = await async_app_client.post("/coref", json=payload)


    assert response.status_code == 200, response.text
    # assert response.json() == payload
