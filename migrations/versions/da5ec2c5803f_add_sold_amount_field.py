"""add sold amount field

Revision ID: da5ec2c5803f
Revises: 05f936cb1d5e
Create Date: 2023-09-10 12:29:57.292060

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'da5ec2c5803f'
down_revision = '05f936cb1d5e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('products', sa.Column('sold_amount', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('products', 'sold_amount')
