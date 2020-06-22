"""Change signature to varchar(255)

Revision ID: b547080fe4a2
Revises: 02a3f2cdcb86
Create Date: 2020-06-19 15:20:15.970452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b547080fe4a2'
down_revision = '02a3f2cdcb86'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('data_extrinsic', 'signature',
        existing_type=sa.String(length=128),
        type_=sa.String(length=255),
    )


def downgrade():
    op.alter_column('data_extrinsic', 'signature',
        existing_type=sa.String(length=255),
        type_=sa.String(length=128),
    )
