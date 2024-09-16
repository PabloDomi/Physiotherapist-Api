"""date for patient stats

Revision ID: db7eaeed3f43
Revises: cad036e97664
Create Date: 2024-09-16 10:33:30.612718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db7eaeed3f43'
down_revision = 'cad036e97664'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('patient_stats', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', sa.DateTime()))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('patient_stats', schema=None) as batch_op:
        batch_op.drop_column('date')

    # ### end Alembic commands ###
