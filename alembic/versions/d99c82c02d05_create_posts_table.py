"""create posts table

Revision ID: d99c82c02d05
Revises: 
Create Date: 2022-06-14 20:40:22.409988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd99c82c02d05'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts",
                    sa.Column('id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('userId', sa.Integer, nullable=False),
                    sa.Column('title', sa.String, nullable=False),
                    sa.Column('body', sa.String, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text('now()'))
                    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
