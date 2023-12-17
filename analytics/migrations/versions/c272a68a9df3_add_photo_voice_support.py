"""add photo, voice support

Revision ID: c272a68a9df3
Revises: 91b29d407031
Create Date: 2023-12-17 10:43:21.881796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c272a68a9df3'
down_revision = '91b29d407031'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('photo', sa.String(length=2048), nullable=True))
    op.add_column('messages', sa.Column('voice', sa.String(length=2048), nullable=True))
    op.alter_column('messages', 'text',
               existing_type=sa.VARCHAR(length=2048),
               nullable=True)
    op.alter_column('worker_requests', 'amount',
               existing_type=sa.NUMERIC(precision=12, scale=2),
               type_=sa.DECIMAL(precision=20, scale=2),
               existing_nullable=True)
    op.alter_column('worker_requests', 'marginal_amount',
               existing_type=sa.NUMERIC(precision=12, scale=2),
               type_=sa.DECIMAL(precision=20, scale=2),
               existing_nullable=True)
    op.alter_column('worker_requests', 'worker_amount',
               existing_type=sa.NUMERIC(precision=12, scale=2),
               type_=sa.DECIMAL(precision=20, scale=2),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('worker_requests', 'worker_amount',
               existing_type=sa.DECIMAL(precision=20, scale=2),
               type_=sa.NUMERIC(precision=12, scale=2),
               existing_nullable=True)
    op.alter_column('worker_requests', 'marginal_amount',
               existing_type=sa.DECIMAL(precision=20, scale=2),
               type_=sa.NUMERIC(precision=12, scale=2),
               existing_nullable=True)
    op.alter_column('worker_requests', 'amount',
               existing_type=sa.DECIMAL(precision=20, scale=2),
               type_=sa.NUMERIC(precision=12, scale=2),
               existing_nullable=True)
    op.alter_column('messages', 'text',
               existing_type=sa.VARCHAR(length=2048),
               nullable=False)
    op.drop_column('messages', 'voice')
    op.drop_column('messages', 'photo')
    # ### end Alembic commands ###