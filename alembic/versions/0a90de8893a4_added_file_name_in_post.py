"""added file name in post

Revision ID: 0a90de8893a4
Revises: 0a1f6d184e62
Create Date: 2023-09-23 22:26:01.918042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a90de8893a4'
down_revision = '0a1f6d184e62'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",sa.Column('filePath',sa.String))
    pass


def downgrade() -> None:
    op.drop_column("posts","filePath")
    pass
