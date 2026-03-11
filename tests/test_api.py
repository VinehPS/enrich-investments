import pytest


@pytest.mark.asyncio
async def test_read_main(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Enrich Investments API"}


@pytest.mark.asyncio
async def test_default_questions(async_client):
    response = await async_client.get("/api/v1/analyze/default-questions")
    assert response.status_code == 200
    data = response.json()
    assert "stocks" in data
    assert "real_estate_funds" in data
    assert len(data["stocks"]) > 0
    assert len(data["real_estate_funds"]) > 0


@pytest.mark.asyncio
async def test_protected_route_unauthorized(async_client):
    # Should block access without token
    response = await async_client.get("/api/v1/auth/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.asyncio
async def test_analyze_unauthorized(async_client):
    response = await async_client.post("/api/v1/analyze/", json={"ticker": "BBAS3", "type": "stocks"})
    # Cannot analyze without token
    assert response.status_code == 401
