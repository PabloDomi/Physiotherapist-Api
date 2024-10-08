"""tablet patient table

Revision ID: 3b7465667325
Revises: d20bbfd9285f
Create Date: 2024-07-03 09:08:33.780199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b7465667325'
down_revision = 'd20bbfd9285f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tablet_patients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tablet_id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.Column('treatment_time', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tablet_patients')
    # ### end Alembic commands ###
