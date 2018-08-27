"""empty message

Revision ID: 8958fdf1725c
Revises: 
Create Date: 2018-06-12 10:22:39.717362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8958fdf1725c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('letter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('letter', sa.String(length=1), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('letter')
    )
    op.create_table('city',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('regionName', sa.String(length=16), nullable=True),
    sa.Column('cityCode', sa.Integer(), nullable=True),
    sa.Column('pinYin', sa.String(length=64), nullable=True),
    sa.Column('c_letter', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['c_letter'], ['letter.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('city')
    op.drop_table('letter')
    # ### end Alembic commands ###
