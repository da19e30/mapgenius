"""Add revoked_tokens table for JWT revocation.

Revision ID: 20240501_01_add_revoked_tokens
Revises: 20240430_01_add_core_tables
Create Date: 2024-05-01 12:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20240501_01_add_revoked_tokens"
down_revision = "20240430_01_add_core_tables"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "revoked_tokens",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("jti", sa.String(length=255), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
    )
    # Optional: create index on created_at for cleanup queries
    op.create_index("ix_revoked_tokens_created_at", "revoked_tokens", ["created_at"])


def downgrade():
    op.drop_index("ix_revoked_tokens_created_at", table_name="revoked_tokens")
    op.drop_table("revoked_tokens")
