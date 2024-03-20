"""anal 2.0 create

Revision ID: 1479b6c905a2
Revises: 
Create Date: 2024-03-20 14:41:49.862124

"""
import ormar
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1479b6c905a2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin_payment_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('text', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('admin_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('type', sa.String(length=10), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admin_requests_date'), 'admin_requests', ['date'], unique=False)
    op.create_table('bots',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('uid', ormar.fields.sqlalchemy_uuid.CHAR(32), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uid')
    )
    op.create_table('proxies',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('host', sa.String(length=255), nullable=False),
    sa.Column('port', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('scheme', sa.String(length=15), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transitions',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('worker_name', sa.String(length=255), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('full_name', sa.String(length=255), nullable=False),
    sa.Column('is_free_consulting', sa.Boolean(), nullable=True),
    sa.Column('is_processing', sa.Boolean(), nullable=True),
    sa.Column('last_activity', sa.DateTime(), nullable=True),
    sa.Column('first_touch', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_first_touch'), 'users', ['first_touch'], unique=False)
    op.create_index(op.f('ix_users_last_activity'), 'users', ['last_activity'], unique=False)
    op.create_table('bot_users',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('bot', sa.BigInteger(), nullable=True),
    sa.Column('user', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['bot'], ['bots.id'], name='fk_bot_users_bots_id_bot'),
    sa.ForeignKeyConstraint(['user'], ['users.id'], name='fk_bot_users_users_id_user'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('bot', 'user', name='uc_bot_users_bot_user')
    )
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender', sa.BigInteger(), nullable=True),
    sa.Column('receiver', sa.BigInteger(), nullable=True),
    sa.Column('text', sa.String(length=2048), nullable=True),
    sa.Column('photo', sa.String(length=2048), nullable=True),
    sa.Column('voice', sa.String(length=2048), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['receiver'], ['users.id'], name='fk_messages_users_id_receiver'),
    sa.ForeignKeyConstraint(['sender'], ['users.id'], name='fk_messages_users_id_sender'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_date'), 'messages', ['date'], unique=False)
    op.create_table('user_payment_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.BigInteger(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('text', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['user'], ['users.id'], name='fk_user_payment_details_users_id_user'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('workers',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user', sa.BigInteger(), nullable=True),
    sa.Column('proxy', sa.BigInteger(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('amount', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('freezed_amount', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('comission', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['proxy'], ['proxies.id'], name='fk_workers_proxies_id_proxy'),
    sa.ForeignKeyConstraint(['user'], ['users.id'], name='fk_workers_users_id_user'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('proxy'),
    sa.UniqueConstraint('user')
    )
    op.create_table('bot_workers',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('bot', sa.BigInteger(), nullable=True),
    sa.Column('worker', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['bot'], ['bots.id'], name='fk_bot_workers_bots_id_bot'),
    sa.ForeignKeyConstraint(['worker'], ['workers.id'], name='fk_bot_workers_workers_id_worker'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('bot', 'worker', name='uc_bot_workers_bot_worker')
    )
    op.create_table('worker_connections',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('worker', sa.BigInteger(), nullable=True),
    sa.Column('api_id', sa.BigInteger(), nullable=False),
    sa.Column('api_hash', sa.String(length=1024), nullable=False),
    sa.ForeignKeyConstraint(['worker'], ['workers.id'], name='fk_worker_connections_workers_id_worker'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('worker')
    )
    op.create_table('worker_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('worker', sa.BigInteger(), nullable=True),
    sa.Column('amount', sa.DECIMAL(precision=20, scale=2), nullable=True),
    sa.Column('marginal_amount', sa.DECIMAL(precision=20, scale=2), nullable=True),
    sa.Column('worker_amount', sa.DECIMAL(precision=20, scale=2), nullable=True),
    sa.Column('is_success', sa.Boolean(), nullable=True),
    sa.Column('receipt', sa.String(length=1024), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('type', sa.String(length=10), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['worker'], ['workers.id'], name='fk_worker_requests_workers_id_worker'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_worker_requests_date'), 'worker_requests', ['date'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_worker_requests_date'), table_name='worker_requests')
    op.drop_table('worker_requests')
    op.drop_table('worker_connections')
    op.drop_table('bot_workers')
    op.drop_table('workers')
    op.drop_table('user_payment_details')
    op.drop_index(op.f('ix_messages_date'), table_name='messages')
    op.drop_table('messages')
    op.drop_table('bot_users')
    op.drop_index(op.f('ix_users_last_activity'), table_name='users')
    op.drop_index(op.f('ix_users_first_touch'), table_name='users')
    op.drop_table('users')
    op.drop_table('transitions')
    op.drop_table('proxies')
    op.drop_table('bots')
    op.drop_index(op.f('ix_admin_requests_date'), table_name='admin_requests')
    op.drop_table('admin_requests')
    op.drop_table('admin_payment_details')
    # ### end Alembic commands ###