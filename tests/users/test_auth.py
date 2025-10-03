from unittest.mock import AsyncMock, Mock

import pytest

from app.users import schemas
from app.users.dependencies import get_auth_service
from app.users.services.auth_service import AuthService

VERIFY_PATH = "app.users.services.auth_service.verify_password"
CREATE_TOKEN_PATH = "app.users.services.auth_service.create_access_token"


@pytest.mark.asyncio
async def test_login_success(monkeypatch, mock_user_repo, stub_user):
    auth = AuthService(repo=mock_user_repo)
    mock_user_repo.get_user_by_email.return_value = stub_user

    fake_verify = Mock(return_value=True)
    fake_create_token = Mock(return_value="jwt-123")

    monkeypatch.setattr(VERIFY_PATH, fake_verify)
    monkeypatch.setattr(CREATE_TOKEN_PATH, fake_create_token)

    result = await auth.login(stub_user.email, "secret")

    mock_user_repo.get_user_by_email.assert_awaited_once_with(stub_user.email)
    fake_verify.assert_called_once_with("secret", stub_user.hashed_password)
    fake_create_token.assert_called_once()
    assert result.access_token == "jwt-123"


@pytest.mark.asyncio
async def test_login_user_not_found(monkeypatch, mock_user_repo, stub_user):
    auth = AuthService(repo=mock_user_repo)
    mock_user_repo.get_user_by_email.return_value = stub_user

    fake_verify = Mock(return_value=False)
    fake_create_token = Mock(return_value="ignored")
    monkeypatch.setattr(VERIFY_PATH, fake_verify)
    monkeypatch.setattr(CREATE_TOKEN_PATH, fake_create_token)

    with pytest.raises(ValueError, match="Invalid email or password"):
        await auth.login(stub_user.email, "bad-pass")

    mock_user_repo.get_user_by_email.assert_awaited_once_with(stub_user.email)
    fake_verify.assert_called_once_with("bad-pass", stub_user.hashed_password)
    fake_create_token.assert_not_called()


@pytest.mark.asyncio
async def test_login_smoke_success(app, client):
    mock_service = AsyncMock()
    mock_service.login = AsyncMock(return_value=schemas.Token(access_token="jwt-123"))
    app.dependency_overrides[get_auth_service] = lambda: mock_service

    resp = await client.post(
        "/api/auth/login",
        data={"username": "user@acme.io", "password": "secret"},
    )

    assert resp.status_code == 200
    assert resp.json()["access_token"] == "jwt-123"
    mock_service.login.assert_awaited_once_with("user@acme.io", "secret")


@pytest.mark.asyncio
async def test_login_unauthorized(app, client):
    mock_service = AsyncMock()
    mock_service.login = AsyncMock(side_effect=ValueError("Invalid email or password"))
    app.dependency_overrides[get_auth_service] = lambda: mock_service

    resp = await client.post(
        "/api/auth/login",
        data={"username": "user@acme.io", "password": "bad"},
    )

    assert resp.status_code == 401
