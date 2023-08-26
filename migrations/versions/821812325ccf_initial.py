"""initial

Revision ID: 821812325ccf
Revises: 
Create Date: 2023-08-10 12:35:12.183203

"""
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy import func

from src.models.enums import UserRoleEnum

# revision identifiers, used by Alembic.
revision = '821812325ccf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('uuid', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('firstname', sa.String(length=38), nullable=True),
        sa.Column('lastname', sa.String(length=38), nullable=True),
        sa.Column('email', sa.String(length=60), nullable=True, unique=True),
        sa.Column('phone', sa.String(length=11), nullable=True, unique=True),
        sa.Column('password', sa.String(), nullable=True),
        sa.Column('role', sa.Enum(UserRoleEnum), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('uuid'),
        sa.Index('idx_users_email', 'email'),
        sa.Index('idx_users_phone', 'phone'),
        sa.Index('idx_users_id', 'id'),
        sa.Index('idx_users_uuid', 'uuid')
    )
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False, autoincrement=True, index=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('parent_id', sa.Integer(), sa.ForeignKey('categories.id'), nullable=True),
        sa.ForeignKeyConstraint(['parent_id'], ['categories.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_categories_id', 'id'),

    )
    op.create_table(
        'products',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('uuid', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('attributes', sa.JSON(), nullable=True),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id']),
        sa.Column('images', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('uuid'),
        sa.Index('idx_products_id', 'id'),
        sa.Index('idx_products_uuid', 'uuid')
    )


def downgrade():
    op.drop_table('users')
    op.drop_table('products')
    op.drop_table('categories')
