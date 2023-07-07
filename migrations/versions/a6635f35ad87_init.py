"""init

Revision ID: a6635f35ad87
Revises: 
Create Date: 2023-07-06 11:20:41.439886

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a6635f35ad87'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), primary_key=True, nullable=False),
        sa.Column("uuid", sa.String(length=36), nullable=False),
        sa.Column("firstname", sa.String(length=38), nullable=True),
        sa.Column("lastname", sa.String(length=38), nullable=True),
        sa.Column("email", sa.String(length=60), nullable=True, unique=True),
        sa.Column("phone", sa.String(length=11), nullable=True, unique=True),
        sa.Column("password", sa.String(length=8)),
        sa.Column(
            "role",
            sa.Enum("admin", "supplier", "customer", name="userroleenum"),
            nullable=False,
            default="customer"
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )


def downgrade():
    op.drop_table("users")
