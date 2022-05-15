"""empty message

Revision ID: 5c2b709909f5
Revises: c0c40d8ff457
Create Date: 2022-05-14 01:45:45.292861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c2b709909f5'
down_revision = 'c0c40d8ff457'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('university',
    sa.Column('sid', sa.String(length=80), nullable=False),
    sa.Column('university_name', sa.String(length=255), nullable=True),
    sa.Column('student_major', sa.String(length=255), nullable=True),
    sa.Column('student_faculty', sa.String(length=255), nullable=True),
    sa.Column('student_tuition', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('sid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('university')
    # ### end Alembic commands ###
