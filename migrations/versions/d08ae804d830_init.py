"""init

Revision ID: d08ae804d830
Revises: 
Create Date: 2023-07-10 09:14:23.637349

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from src.models.enums import UserRoleEnum

# revision identifiers, used by Alembic.
revision = 'd08ae804d830'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True,  nullable=False),
    sa.Column('uuid', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('firstname', sa.String(length=38), nullable=True),
    sa.Column('lastname', sa.String(length=38), nullable=True),
    sa.Column('email', sa.String(length=60), nullable=True, unique=True),
    sa.Column('phone', sa.String(length=11), nullable=True, unique=True),
    sa.Column('password', sa.String(length=8), nullable=True),
    sa.Column('role', postgresql.ENUM('admin', 'supplier', 'customer', name='userroleenum'),
              default=UserRoleEnum.customer.value, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid'),
    sa.Index('idx_users_email', 'email'),
    sa.Index('idx_users_phone', 'phone'),
    sa.Index('idx_users_id', 'id'),
    sa.Index('idx_users_uuid', 'uuid')
    )

    def downgrade():
        op.drop_table('users')
