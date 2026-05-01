"""Alembic migration – create core tables for facturación electrónica.

Creates:
- clients
- products
- invoice_headers
- invoice_lines
- dian_logs

Revision ID: 20240430_01
Revises: None (initial migration for new entities)
Create Date: 2024-04-30 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20240430_01'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # clients
    op.create_table(
        'clients',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('nit', sa.String(length=20), nullable=False, unique=True, index=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('address', sa.Text, nullable=True),
        sa.Column('tax_regime', sa.String(length=100), nullable=False),
    )

    # products
    op.create_table(
        'products',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('code', sa.String(length=50), nullable=False, unique=True, index=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('price', sa.Float, nullable=False),
        sa.Column('iva_percent', sa.Float, nullable=False, server_default='19.0'),
        sa.Column('dian_class', sa.String(length=20), nullable=True),
        sa.Column('unit', sa.String(length=20), nullable=False, server_default='unidad'),
    )

    # invoice_headers
    op.create_table(
        'invoice_headers',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('client_id', sa.Integer, sa.ForeignKey('clients.id'), nullable=False, index=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False, index=True),
        sa.Column('issue_date', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('subtotal', sa.Float, nullable=False),
        sa.Column('iva_total', sa.Float, nullable=False),
        sa.Column('total_amount', sa.Float, nullable=False),
        sa.Column('currency', sa.String(length=3), nullable=False, server_default='COP'),
        sa.Column('cufe', sa.String(length=64), nullable=False, unique=True, index=True),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='pending'),
        sa.Column('xml_path', sa.String(length=512), nullable=True),
        sa.Column('pdf_path', sa.String(length=512), nullable=True),
    )

    # invoice_lines
    op.create_table(
        'invoice_lines',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('invoice_id', sa.Integer, sa.ForeignKey('invoice_headers.id'), nullable=False, index=True),
        sa.Column('product_id', sa.Integer, sa.ForeignKey('products.id'), nullable=False),
        sa.Column('quantity', sa.Float, nullable=False, server_default='1'),
        sa.Column('unit_price', sa.Float, nullable=False),
        sa.Column('total_price', sa.Float, nullable=False),
        sa.Column('iva_percent', sa.Float, nullable=False, server_default='19.0'),
        sa.Column('iva_amount', sa.Float, nullable=False),
    )

    # dian_logs
    op.create_table(
        'dian_logs',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('invoice_cufe', sa.String(length=64), nullable=False, index=True),
        sa.Column('request_xml_path', sa.String(length=512), nullable=False),
        sa.Column('response_status', sa.String(length=20), nullable=False),
        sa.Column('response_detail', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    )


def downgrade():
    op.drop_table('dian_logs')
    op.drop_table('invoice_lines')
    op.drop_table('invoice_headers')
    op.drop_table('products')
    op.drop_table('clients')
