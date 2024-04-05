"""update wbot

Revision ID: 1ea72117c880
Revises: f2e9fb3cbf6c
Create Date: 2024-03-23 19:25:43.448215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ea72117c880'
down_revision = 'f2e9fb3cbf6c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bots', sa.Column('service_photo', sa.String(length=1024), nullable=True))
    op.add_column('bots', sa.Column('free_consulting_photo', sa.String(length=1024), nullable=True))
    op.add_column('bots', sa.Column('free_consulting_description', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bots', 'free_consulting_description')
    op.drop_column('bots', 'free_consulting_photo')
    op.drop_column('bots', 'service_photo')
    # ### end Alembic commands ###