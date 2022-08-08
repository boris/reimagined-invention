"""empty message

Revision ID: a56eb0f88d08
Revises: ab8d661b4728
Create Date: 2022-08-07 22:43:43.906499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a56eb0f88d08'
down_revision = 'ab8d661b4728'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('author', sa.Column('name', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('author', 'name')
    # ### end Alembic commands ###