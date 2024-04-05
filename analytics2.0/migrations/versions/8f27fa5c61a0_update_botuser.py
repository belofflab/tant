"""update botuser

Revision ID: 8f27fa5c61a0
Revises: 1ea72117c880
Create Date: 2024-03-24 13:44:21.631543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f27fa5c61a0'
down_revision = '1ea72117c880'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bot_users', sa.Column('last_activity', sa.DateTime(), nullable=True))
    op.add_column('bot_users', sa.Column('first_touch', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_bot_users_first_touch'), 'bot_users', ['first_touch'], unique=False)
    op.create_index(op.f('ix_bot_users_last_activity'), 'bot_users', ['last_activity'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_bot_users_last_activity'), table_name='bot_users')
    op.drop_index(op.f('ix_bot_users_first_touch'), table_name='bot_users')
    op.drop_column('bot_users', 'first_touch')
    op.drop_column('bot_users', 'last_activity')
    # ### end Alembic commands ###