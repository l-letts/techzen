"""empty message

Revision ID: 5d64de5d9c94
Revises: 62d83293fa6b
Create Date: 2022-05-10 19:23:08.531185

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d64de5d9c94'
down_revision = '62d83293fa6b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student', sa.Column('status', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('student', 'status')
    # ### end Alembic commands ###
