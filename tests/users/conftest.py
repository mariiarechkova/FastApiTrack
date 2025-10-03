from dataclasses import dataclass
from unittest.mock import AsyncMock

import pytest

from app.users.models import User


@dataclass
class StubUser:
    id: int = 123
    email: str = "user@acme.io"
    hashed_password: str = "HASHED_DB"


@pytest.fixture
def stub_user() -> "StubUser":
    return StubUser()


@pytest.fixture
def mock_org_query():
    query = AsyncMock()
    query.exists_by_id.return_value = True
    return query


@pytest.fixture
def mock_user_repo():
    repo = AsyncMock()
    repo.create_user.return_value = User(
        id=10,
        email="user@acme.io",
        first_name="Ada",
        last_name="Lovelace",
        is_admin=False,
        organisation_id=1,
        hashed_password="HASHED",
    )
    return repo
