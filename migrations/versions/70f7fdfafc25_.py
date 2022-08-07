"""empty message

Revision ID: 70f7fdfafc25
Revises: 24c8b37053aa
Create Date: 2022-08-07 00:58:07.932146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70f7fdfafc25'
down_revision = '24c8b37053aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('genre', sa.String(length=255), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('pages', sa.Integer(), nullable=True),
    sa.Column('read', sa.Boolean(), nullable=True),
    sa.Column('shared', sa.Boolean(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('book')
    # ### end Alembic commands ###
