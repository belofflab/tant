"""update worker

Revision ID: 7945e051049d
Revises: a313b4720927
Create Date: 2023-11-04 08:25:14.883210

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7945e051049d'
down_revision = 'a313b4720927'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('workers', sa.Column('subdomain', sa.String(length=255), nullable=True))
    op.add_column('workers', sa.Column('hostname', sa.String(length=255), nullable=True))
    op.drop_column('workers', 'api_port')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('workers', sa.Column('api_port', sa.BIGINT(), autoincrement=False, nullable=True))
    op.drop_column('workers', 'hostname')
    op.drop_column('workers', 'subdomain')
    # ### end Alembic commands ###
