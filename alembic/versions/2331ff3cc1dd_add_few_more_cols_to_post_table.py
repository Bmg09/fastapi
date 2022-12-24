"""add few more cols to post table

Revision ID: 2331ff3cc1dd
Revises: bc8011c2a42f
Create Date: 2022-12-02 02:09:25.262044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2331ff3cc1dd'
down_revision = 'bc8011c2a42f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'))
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
