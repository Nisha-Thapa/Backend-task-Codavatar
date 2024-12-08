"""Update Genders enum in User model

Revision ID: 870ef05370f3
Revises: e19e89b7b5b9
Create Date: 2024-12-07 17:52:44.051837

"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa  # noqa: F401
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.
revision: str = "870ef05370f3"
down_revision: str | None = "e19e89b7b5b9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

old_genders_enum = ENUM("male", "female", "other", name="genders", create_type=False)
new_genders_enum = ENUM("MALE", "FEMALE", "OTHER", name="genders", create_type=False)


def upgrade():
    # Update the genders enum type
    op.execute("ALTER TYPE genders RENAME TO genders_old;")
    new_genders_enum.create(op.get_bind())
    op.execute(
        "ALTER TABLE users ALTER COLUMN gender TYPE genders USING gender::text::genders;"
    )
    op.execute("DROP TYPE genders_old;")


def downgrade():
    # Revert to the old enum type
    op.execute("ALTER TYPE genders RENAME TO genders_new;")
    old_genders_enum.create(op.get_bind())
    op.execute(
        "ALTER TABLE users ALTER COLUMN gender TYPE genders USING gender::text::genders;"
    )
    op.execute("DROP TYPE genders_new;")
