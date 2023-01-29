"""relationships

Revision ID: 93ee7fd23674
Revises: f5581745697e
Create Date: 2023-01-29 21:26:47.656848

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '93ee7fd23674'
down_revision = 'f5581745697e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file_model', sa.Column('user_id', postgresql.UUID(), nullable=True))
    op.create_foreign_key(None, 'file_model', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'file_model', type_='foreignkey')
    op.drop_column('file_model', 'user_id')
    # ### end Alembic commands ###