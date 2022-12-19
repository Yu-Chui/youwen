"""empty message

Revision ID: 39b42359cd72
Revises: d772a3aa2cf7
Create Date: 2022-10-18 15:57:22.740538

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '39b42359cd72'
down_revision = 'd772a3aa2cf7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('username', sa.String(length=200), nullable=False))
    op.drop_index('user_name', table_name='user')
    op.create_unique_constraint(None, 'user', ['username'])
    op.drop_column('user', 'user_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('user_name', mysql.VARCHAR(length=200), nullable=False))
    op.drop_constraint(None, 'user', type_='unique')
    op.create_index('user_name', 'user', ['user_name'], unique=False)
    op.drop_column('user', 'username')
    # ### end Alembic commands ###
