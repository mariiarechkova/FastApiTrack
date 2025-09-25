"""add ondelete cascade to users.organisation_id

Revision ID: 8acecbfbc691
Revises: 64f4a68e96a2
Create Date: 2025-09-25 17:41:01.344318

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8acecbfbc691'
down_revision: Union[str, Sequence[str], None] = '64f4a68e96a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "users_organisation_id_fkey",
        "users",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "users_organisation_id_fkey",
        "users", "organisations",
        ["organisation_id"], ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("users_organisation_id_fkey", "users", type_="foreignkey")
    op.create_foreign_key(
        "users_organisation_id_fkey",
        "users", "organisations",
        ["organisation_id"], ["id"],
    )