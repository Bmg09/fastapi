"""create column content

Revision ID: 269b8baffa03
Revises: 1a0ecfb08a56
Create Date: 2022-12-01 23:39:05.564613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '269b8baffa03'
down_revision = '1a0ecfb08a56'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass