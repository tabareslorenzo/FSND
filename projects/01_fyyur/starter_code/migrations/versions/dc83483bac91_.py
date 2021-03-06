"""empty message

Revision ID: dc83483bac91
Revises: 86a752ad36dd
Create Date: 2020-04-06 11:23:28.780521

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc83483bac91'
down_revision = '86a752ad36dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('start_time', sa.String(length=120), nullable=False))
    op.drop_column('Show', 'time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('time', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
    op.drop_column('Show', 'start_time')
    # ### end Alembic commands ###
