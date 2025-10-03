from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from app.organisations.models import Organisation


@pytest.fixture
def mock_org_repo():
    repo = AsyncMock()
    repo.get_all.return_value = [
        Organisation(id=1, name="Org1"),
        Organisation(id=2, name="Org2"),
    ]
    repo.get_by_id.return_value = Organisation(id=1, name="Org1")
    repo.create.return_value = Organisation(id=3, name="Acme Inc", created_at=datetime(2025, 1, 1, 0, 0))
    return repo


@pytest.fixture
def mock_user_service():
    service = AsyncMock()
    service.create_admin_user.return_value = {
        "id": 10,
        "email": "admin@acme.io",
        "first_name": "Ada",
        "last_name": "Lovelace",
        "is_admin": True,
        "organisation_id": 3,
        "created_at": "2025-01-01T12:00:00Z",
    }
    return service
