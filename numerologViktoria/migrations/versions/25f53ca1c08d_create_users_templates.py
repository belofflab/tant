"""create users templates

Revision ID: 25f53ca1c08d
Revises: a7ad2e355375
Create Date: 2023-10-12 09:55:12.959493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25f53ca1c08d'
down_revision = 'a7ad2e355375'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_templates',
    sa.Column('idx', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('idx')
    )
    op.create_table('user_user_template_association',
    sa.Column('idx', sa.BigInteger(), nullable=False),
    sa.Column('user_template_id', sa.BigInteger(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.idx'], ),
    sa.ForeignKeyConstraint(['user_template_id'], ['user_templates.idx'], ),
    sa.PrimaryKeyConstraint('idx')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_user_template_association')
    op.drop_table('user_templates')
    # ### end Alembic commands ###
