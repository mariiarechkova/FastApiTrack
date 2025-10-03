import pytest

from app.organisations.schemas import OrganisationAndUserCreate
from app.organisations.services.organisation_services import OrganisationService
from app.users.schemas import UserCreate


@pytest.mark.asyncio
async def test_get_all_returns_list_from_repo(mock_org_repo):
    service = OrganisationService(repo=mock_org_repo, user_service=None)
    orgs = await service.get_all()

    assert isinstance(orgs, list)
    assert len(orgs) == 2
    assert orgs[0].name == "Org1"

    mock_org_repo.get_all.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_get_by_id_success(mock_org_repo):
    service = OrganisationService(repo=mock_org_repo, user_service=None)

    org = await service.get_by_id(1)
    assert org.id == 1
    assert org.name == "Org1"

    mock_org_repo.get_by_id.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_create_org_and_admin(mock_org_repo, mock_user_service):
    service = OrganisationService(repo=mock_org_repo, user_service=mock_user_service)

    dto = OrganisationAndUserCreate(
        name="Acme",
        user=UserCreate(
            email="admin@acme.io",
            first_name="Ada",
            last_name="Lovelace",
            password="secret123",
        ),
    )

    result = await service.create(dto)

    assert result.id == 3
    assert result.name == "Acme Inc"
    assert result.admin.email == "admin@acme.io"
    assert result.admin.is_admin is True

    mock_org_repo.create.assert_awaited_once_with(name="Acme")
    mock_user_service.create_admin_user.assert_awaited_once_with(
        org_id=3,
        dto=dto.user,
    )
