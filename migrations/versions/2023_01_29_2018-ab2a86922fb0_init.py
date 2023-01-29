"""init

Revision ID: ab2a86922fb0
Revises: 
Create Date: 2023-01-29 20:18:23.461983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab2a86922fb0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file_model',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('path', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_file_model_created_at'), 'file_model', ['created_at'], unique=False)
    op.create_index(op.f('ix_file_model_id'), 'file_model', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_file_model_id'), table_name='file_model')
    op.drop_index(op.f('ix_file_model_created_at'), table_name='file_model')
    op.drop_table('file_model')
    # ### end Alembic commands ###