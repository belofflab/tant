"""add trainings 

Revision ID: 08c39ea65c99
Revises: 25f53ca1c08d
Create Date: 2023-12-03 09:25:27.467984

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08c39ea65c99'
down_revision = '25f53ca1c08d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trainings',
    sa.Column('idx', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.Numeric(precision=12, scale=2), nullable=True),
    sa.Column('is_visible', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('idx')
    )
    op.create_table('taro_trainings',
    sa.Column('idx', sa.BigInteger(), nullable=False),
    sa.Column('training', sa.BigInteger(), nullable=True),
    sa.Column('user', sa.BigInteger(), nullable=True),
    sa.Column('is_banned', sa.Boolean(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['training'], ['trainings.idx'], ),
    sa.ForeignKeyConstraint(['user'], ['users.idx'], ),
    sa.PrimaryKeyConstraint('idx')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('taro_trainings')
    op.drop_table('trainings')
    # ### end Alembic commands ###
