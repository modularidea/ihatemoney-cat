"""project categories, payment modes, repeating bills

Revision ID: b2d1e4f5a6c7
Revises: a1c0bd2e3f77
Create Date: 2026-09-11 00:00:00.000000

"""

# revision identifiers, used by Alembic.
revision = "b2d1e4f5a6c7"
down_revision = "a1c0bd2e3f77"

from alembic import op
import sqlalchemy as sa


def upgrade():
    for table in ("category", "payment_mode"):
        op.create_table(
            table,
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("project_id", sa.String(length=64), nullable=True),
            sa.Column("name", sa.UnicodeText(), nullable=False),
            sa.Column("icon", sa.UnicodeText(), nullable=True),
            sa.Column("color", sa.String(length=7), nullable=True),
            sa.Column("order", sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(["project_id"], ["project.id"]),
            sa.PrimaryKeyConstraint("id"),
            sqlite_autoincrement=True,
        )
    for table, autoinc in (("bill", None), ("bill_version", False)):
        extra = {} if autoinc is None else {"autoincrement": autoinc}
        op.add_column(table, sa.Column("payment_mode_id", sa.Integer(), nullable=True, **extra))
        op.add_column(table, sa.Column("repeat", sa.String(length=1), nullable=True, server_default="n", **extra))
        op.add_column(table, sa.Column("repeat_freq", sa.Integer(), nullable=True, server_default="1", **extra))
        op.add_column(table, sa.Column("repeat_until", sa.Date(), nullable=True, **extra))
        op.add_column(table, sa.Column("repeat_all_active", sa.Boolean(), nullable=True, server_default="0", **extra))


def downgrade():
    for table in ("bill_version", "bill"):
        for column in ("repeat_all_active", "repeat_until", "repeat_freq", "repeat", "payment_mode_id"):
            op.drop_column(table, column)
    op.drop_table("payment_mode")
    op.drop_table("category")
