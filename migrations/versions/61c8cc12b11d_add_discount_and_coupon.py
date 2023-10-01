"""add discount and coupon

Revision ID: 61c8cc12b11d
Revises: 7b34125e19e4
Create Date: 2023-09-16 16:41:43.661663

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '61c8cc12b11d'
down_revision = '7b34125e19e4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'discounts',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('discount_percent', sa.Integer(), nullable=True),
        sa.Column('expired', sa.Boolean(), nullable=False),
        sa.Column('expiration_hours', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id')),
        sa.PrimaryKeyConstraint('id')
    )
    op.add_column('products', sa.Column('on_discount', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('products', sa.Column('discounted_price', sa.Integer(), nullable=True))

    op.create_table(
        'coupons',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('code', sa.String(length=20), nullable=False),
        sa.Column('discount_percent', sa.Integer(), nullable=True),
        sa.Column('expired', sa.Boolean(), nullable=False),
        sa.Column('expiration_hours', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('coupons')
    op.drop_table('discounts')
    op.drop_column('products', 'on_discount')
    op.drop_column('products', 'discounted_price')
