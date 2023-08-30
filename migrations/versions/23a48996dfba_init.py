"""init

Revision ID: 23a48996dfba
Revises: 
Create Date: 2023-08-29 17:17:19.063627

"""
from alembic import op
import sqlalchemy as sa

from src.models.enums import UserRoleEnum

# revision identifiers, used by Alembic.
revision = '23a48996dfba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'categories',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('parent_id', sa.Integer(), sa.ForeignKey('categories.id', ondelete="CASCADE"), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['parent_id'], ['categories.id']),
        sa.Index('idx_categories_id', 'id'),
    )
    op.create_table(
        'products',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('attributes', sa.JSON(), nullable=True),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('categories.id', ondelete='CASCADE'), nullable=True),
        sa.Column('images', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_products_id', 'id'),
    )
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('firstname', sa.String(length=38), nullable=True),
        sa.Column('lastname', sa.String(length=38), nullable=True),
        sa.Column('email', sa.String(length=60), nullable=True, unique=True),
        sa.Column('phone', sa.String(length=11), nullable=True, unique=True),
        sa.Column('password', sa.String(), nullable=True),
        sa.Column('role', sa.Enum(UserRoleEnum), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_users_email', 'email'),
        sa.Index('idx_users_phone', 'phone'),
        sa.Index('idx_users_id', 'id'),
    )
    op.create_table(
        'comments',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('content', sa.String(), nullable=True),
        sa.Column('reviewer_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False),
        sa.Column('like', sa.Integer(), nullable=True),
        sa.Column('dislike', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['product_id'], ['products.id']),
        sa.ForeignKeyConstraint(['reviewer_id'], ['users.id']),
        sa.Index('idx_comments_id', 'id'),
    )


def downgrade() -> None:
    op.drop_table('categories')
    op.drop_table('comments')
    op.drop_table('users')
