"""empty message

Revision ID: c0c40d8ff457
Revises: b85d003a21e3
Create Date: 2022-05-14 01:43:03.164689

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c0c40d8ff457'
down_revision = 'b85d003a21e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('university', 'univeristy_contact')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('university', sa.Column('univeristy_contact', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
