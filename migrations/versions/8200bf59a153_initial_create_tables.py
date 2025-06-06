"""Initial create tables

Revision ID: 8200bf59a153
Revises: 5bf32d143597
Create Date: 2025-06-06 11:46:59.745552

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8200bf59a153'
down_revision = '5bf32d143597'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('pizzas') as batch_op:
        batch_op.alter_column('name', existing_type=sa.String(), nullable=False)
        batch_op.alter_column('ingredients', existing_type=sa.String(), nullable=False)

    with op.batch_alter_table('restaurants') as batch_op:
        batch_op.alter_column('name', existing_type=sa.String(), nullable=False)
        batch_op.alter_column('address', existing_type=sa.String(), nullable=False)


def downgrade():
    with op.batch_alter_table('restaurants') as batch_op:
        batch_op.alter_column('address', existing_type=sa.String(), nullable=True)
        batch_op.alter_column('name', existing_type=sa.String(), nullable=True)

    with op.batch_alter_table('pizzas') as batch_op:
        batch_op.alter_column('ingredients', existing_type=sa.String(), nullable=True)
        batch_op.alter_column('name', existing_type=sa.String(), nullable=True)
