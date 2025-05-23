"""add user model

Revision ID: 35e60095fe61
Revises: 86a0c2f6a891
Create Date: 2025-04-17 23:57:45.487377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35e60095fe61'
down_revision = '86a0c2f6a891'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
