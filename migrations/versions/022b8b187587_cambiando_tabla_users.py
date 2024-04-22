"""cambiando tabla users

Revision ID: 022b8b187587
Revises: f5bd9a1e40cf
Create Date: 2024-04-22 12:13:45.888810

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '022b8b187587'
down_revision = 'f5bd9a1e40cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('users_username_key', type_='unique')
        batch_op.drop_column('surname')
        batch_op.drop_column('username')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.VARCHAR(length=80), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('surname', sa.VARCHAR(length=80), autoincrement=False, nullable=False))
        batch_op.create_unique_constraint('users_username_key', ['username'])

    with op.batch_alter_table('routines', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('routines_patient_id_fkey', 'patients', ['id'], ['id'])

    # ### end Alembic commands ###
