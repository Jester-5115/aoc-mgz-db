"""add index on map name

Revision ID: 5f04067e5e7d
Revises: b13aecf90b4e
Create Date: 2019-09-15 15:23:42.610436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f04067e5e7d'
down_revision = 'b13aecf90b4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_event_maps_name'), 'event_maps', ['name'], unique=False)
    op.create_index(op.f('ix_maps_name'), 'maps', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_maps_name'), table_name='maps')
    op.drop_index(op.f('ix_event_maps_name'), table_name='event_maps')
    # ### end Alembic commands ###