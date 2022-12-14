"""empty message

Revision ID: 4b8c8caca17b
Revises: 48dca73a0074
Create Date: 2022-11-16 23:45:09.947190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b8c8caca17b'
down_revision = '48dca73a0074'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('results', schema=None) as batch_op:
        batch_op.drop_constraint('results_name_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('results', schema=None) as batch_op:
        batch_op.create_unique_constraint('results_name_key', ['name'])

    # ### end Alembic commands ###
