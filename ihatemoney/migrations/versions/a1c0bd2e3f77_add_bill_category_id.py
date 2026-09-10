"""add bill category_id (obsidian-ihm-plugin server-patch)

Revision ID: a1c0bd2e3f77
Revises: c941aaca38c2
Create Date: 2026-09-08 00:00:00.000000

"""

# revision identifiers, used by Alembic.
revision = "a1c0bd2e3f77"
down_revision = "c941aaca38c2"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column("bill", sa.Column("category_id", sa.Integer(), nullable=True))
    op.add_column(
        "bill_version",
        sa.Column("category_id", sa.Integer(), autoincrement=False, nullable=True),
    )


def downgrade():
    op.drop_column("bill_version", "category_id")
    op.drop_column("bill", "category_id")
