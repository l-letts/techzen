"""empty message

Revision ID: 62d83293fa6b
Revises: 26986f4716f7
Create Date: 2022-04-19 23:17:52.843851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62d83293fa6b'
down_revision = '26986f4716f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('loan',
    sa.Column('loanid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('loan_type', sa.String(length=255), nullable=True),
    sa.Column('loan_status', sa.String(length=255), nullable=True),
    sa.Column('sid', sa.Integer(), nullable=True),
    sa.Column('length', sa.Integer(), nullable=True),
    sa.Column('interestrate', sa.Integer(), nullable=True),
    sa.Column('loanamount', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.String(length=80), nullable=True),
    sa.Column('moratorium', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('loanid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('loan')
    # ### end Alembic commands ###
