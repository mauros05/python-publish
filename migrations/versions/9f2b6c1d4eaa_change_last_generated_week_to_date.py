"""change last_generated_week to date

Revision ID: 9f2b6c1d4eaa
Revises: 40a014a73fd4
Create Date: 2026-02-14 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9f2b6c1d4eaa"
down_revision = "40a014a73fd4"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("rotation_state", schema=None) as batch_op:
        batch_op.alter_column(
            "last_generated_week",
            existing_type=sa.Integer(),
            type_=sa.Date(),
            existing_nullable=True,
        )


def downgrade():
    with op.batch_alter_table("rotation_state", schema=None) as batch_op:
        batch_op.alter_column(
            "last_generated_week",
            existing_type=sa.Date(),
            type_=sa.Integer(),
            existing_nullable=True,
        )
