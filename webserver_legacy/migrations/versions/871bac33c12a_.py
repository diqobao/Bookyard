"""empty message

Revision ID: 871bac33c12a
Revises: aec932bc7ced
Create Date: 2017-12-06 19:25:15.333789

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '871bac33c12a'
down_revision = 'aec932bc7ced'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
	op.alter_column('ratings', 'rating',
	           existing_type=mysql.INTEGER(display_width=11),
	           nullable=True,
	           existing_server_default=sa.text("'0'"))
	# op.alter_column('users', 'id', primary_key=True, autoincrement=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('ratings', 'rating',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False,
               existing_server_default=sa.text("'0'"))
    # ### end Alembic commands ###
