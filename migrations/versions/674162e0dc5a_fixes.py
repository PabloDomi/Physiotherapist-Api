"""fixes

Revision ID: 674162e0dc5a
Revises: b75266d91327
Create Date: 2024-08-13 10:51:57.563879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '674162e0dc5a'
down_revision = 'b75266d91327'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('routine_exercise')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('routine_exercise',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('routine_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('exercise_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercises.id'], name='routine_exercise_exercise_id_fkey'),
    sa.ForeignKeyConstraint(['routine_id'], ['routines.id'], name='routine_exercise_routine_id_fkey'),
    sa.PrimaryKeyConstraint('id', 'routine_id', 'exercise_id', name='routine_exercise_pkey')
    )
    # ### end Alembic commands ###
