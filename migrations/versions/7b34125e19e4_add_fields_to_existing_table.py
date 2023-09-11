"""add_fields_to_existing_table

Revision ID: 7b34125e19e4
Revises: 959ed0c93f13
Create Date: 2023-09-11 17:27:57.524018

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7b34125e19e4'
down_revision = '959ed0c93f13'
branch_labels = None
depends_on = None


def upgrade():
    # Add the new columns to the existing table
    op.add_column('products', sa.Column('sold_amount', sa.Integer(), nullable=True))
    op.add_column('products', sa.Column('rate', sa.Float(), nullable=True))
    op.add_column('products', sa.Column('total_rating', sa.Float(), server_default='0'))
    op.add_column('products', sa.Column('num_ratings', sa.Integer(), server_default='0'))


def downgrade():
    # Remove the new columns if necessary (make sure to handle data migration)
    op.drop_column('products', 'sold_amount')
    op.drop_column('products', 'rate')
    op.drop_column('products', 'total_rating')
    op.drop_column('products', 'num_ratings')
