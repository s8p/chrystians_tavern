"""criando tabela client_orders

Revision ID: a5475f1bb14e
Revises: 9d36fab1c061
Create Date: 2022-04-29 17:29:36.967397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a5475f1bb14e"
down_revision = "9d36fab1c061"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "client_orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=True),
        sa.Column("client_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["client_id"],
            ["clients.id"],
        ),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["orders.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("client_orders")
    # ### end Alembic commands ###
