"""Add sold_amount and rating fields

Revision ID: 05f936cb1d5e
Revises: 959ed0c93f13
Create Date: 2023-09-10 11:46:14.530487

"""
from enum import Enum

from alembic import op

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '05f936cb1d5e'
down_revision = '959ed0c93f13'
branch_labels = None
depends_on = None


class ProductRatingEnum(Enum):
    very_bad = "1"
    bad = "2"
    average = "3"
    good = "4"
    very_good = "5"


def upgrade():
    # Add the custom enum type
    op.execute(
        "CREATE TYPE productratingenum AS ENUM ('1', '2', '3', '4', '5')"
    )

    # Add the column using the enum type
    op.add_column('products', sa.Column('rating', sa.Enum(ProductRatingEnum), nullable=True))


def downgrade():
    # Drop the column and the custom enum type
    op.drop_column('products', 'rating')
    op.execute("DROP TYPE IF EXISTS productratingenum")
