"""Cria a tabela canais.

Revision ID: 0001
Revises:
"""

from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "canais",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("nome", sa.String(100), nullable=False),
        sa.Column("sistema_origem", sa.String(), nullable=False),
        sa.Column("sistema_destino", sa.String(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("ambiente", sa.String(20), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("canais")
