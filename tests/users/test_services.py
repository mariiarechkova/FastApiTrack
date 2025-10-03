from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import HTTPException

from app.users.dependencies import require_admin_user
from app.users.schemas import UserCreate
from app.users.services.user_service import UserService


@pytest.mark.asyncio
async def test_create_user_success(monkeypatch, mock_org_query, mock_user_repo):
    service = UserService(repo=mock_user_repo, org_query=mock_org_query)
    fake_hash = Mock(return_value="HASHED")

    monkeypatch.setattr("app.users.services.user_service.hash_password", fake_hash)
    dto = UserCreate(
        email="user@acme.io",
        first_name="Ada",
        last_name="Lovelace",
        password="secret123",
    )

    result = await service.create_user(org_id=1, dto=dto)

    fake_hash.assert_called_once_with("secret123")
    mock_org_query.exists_by_id.assert_awaited_once_with(1)
    mock_user_repo.create_user.assert_awaited_once_with(
        email="user@acme.io",
        first_name="Ada",
        last_name="Lovelace",
        organisation_id=1,
        hashed_password="HASHED",
        is_admin=False,
    )

    assert result.email == "user@acme.io"
    assert result.organisation_id == 1
    assert result.is_admin is False


REPO_PATH = "app.users.dependencies.UserRepository"


async def test_require_admin_user_success(monkeypatch, mock_user_repo, stub_user):
    mock_user_repo.is_admin.return_value = True

    monkeypatch.setattr(REPO_PATH, lambda session: mock_user_repo)
    out = await require_admin_user(current_user=stub_user, session=AsyncMock())
    assert out is stub_user
    mock_user_repo.is_admin.assert_called_once_with(stub_user.id)


async def test_require_admin_user_forbidden(monkeypatch, mock_user_repo, stub_user):
    mock_user_repo.is_admin.return_value = False

    monkeypatch.setattr(REPO_PATH, lambda session: mock_user_repo)
    with pytest.raises(HTTPException) as exc:
        await require_admin_user(current_user=stub_user, session=AsyncMock())

    assert exc.value.status_code == 403
    mock_user_repo.is_admin.assert_called_once_with(stub_user.id)
