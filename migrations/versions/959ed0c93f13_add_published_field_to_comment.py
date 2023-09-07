"""add published field to comment

Revision ID: 959ed0c93f13
Revises: 23a48996dfba
Create Date: 2023-09-07 12:29:02.223515

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '959ed0c93f13'
down_revision = '23a48996dfba'
branch_labels = None
depends_on = None


def upgrade():
    # Add the new column to the comments table
    op.add_column('comments', sa.Column('is_published', sa.Boolean(), nullable=True))


def downgrade():
    # Remove the column if needed
    op.drop_column('comments', 'is_published')
