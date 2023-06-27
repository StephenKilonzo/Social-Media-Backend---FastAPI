"""Create Post Table

Revision ID: 71b3d0bb922c
Revises: 
Create Date: 2023-06-25 21:26:16.966409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71b3d0bb922c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), primary_key = True, nullable = False), sa.Column('name', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
