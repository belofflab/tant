"""add model user_payment_details

Revision ID: ded49b213f55
Revises: 46a84ad115d2
Create Date: 2023-10-22 08:22:21.399795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ded49b213f55'
down_revision = '46a84ad115d2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_payment_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.BigInteger(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('text', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['user'], ['users.id'], name='fk_user_payment_details_users_id_user'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_payment_details')
    # ### end Alembic commands ###
