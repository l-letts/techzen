"""empty message

Revision ID: f0b43d832415
Revises: 584cafe50a28
Create Date: 2022-04-19 22:40:12.150874

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0b43d832415'
down_revision = '584cafe50a28'
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
    sa.Column('moratorium', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('loanid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('loan')
    # ### end Alembic commands ###
