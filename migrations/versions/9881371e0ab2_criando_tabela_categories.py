"""criando tabela products

Revision ID: 9881371e0ab2
Revises: 7f8acfa2ab21
Create Date: 2022-04-29 17:12:29.394421

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9881371e0ab2'
down_revision = '7f8acfa2ab21'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('available_amount', sa.Integer(), nullable=False),
    sa.Column('flag', sa.String(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['category'], ['categories.name'], ),
    sa.ForeignKeyConstraint(['flag'], ['boxes.flag'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    # ### end Alembic commands ###
