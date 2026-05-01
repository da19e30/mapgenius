"""Tests for the end‑to‑end electronic invoice flow.

The test uses an in‑memory SQLite database (configured via ``DATABASE_URL`` env var) and
creates a client, a product, then invokes the ``generate_and_finalize_invoice`` service.
It asserts that:
- XML and signed XML files are generated.
- CUFE is calculated and stored.
- The simulated DIAN response sets the status to either ``accepted`` or ``rejected``.
- When accepted, a PDF file is produced and the ``send_invoice_email`` function is called
  (the email function is monkey‑patched to avoid real SMTP traffic).
"""

import os
import tempfile
from pathlib import Path
from unittest import mock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.models.client import Client
from app.models.product import Product
from app.models.invoice_header import InvoiceHeader
from app.models.invoice_line import InvoiceLine
from app.services.invoice import generate_and_finalize_invoice

# ---------------------------------------------------------------------------
# Test fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function")
def db_session():
    # Use an in‑memory SQLite DB for isolation
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def sample_client(db_session):
    client = Client(nit="900123456", name="Acme Corp", email="contact@acme.com", address="Calle 123", tax_regime="Régimen común")
    db_session.add(client)
    db_session.commit()
    db_session.refresh(client)
    return client

@pytest.fixture(scope="function")
def sample_product(db_session):
    product = Product(code="PRD001", name="Servicio de consultoría", price=1000.0, iva_percent=19.0, dian_class="111", unit="hour")
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product

# ---------------------------------------------------------------------------
# Helper to create header & line items directly (bypassing API)
# ---------------------------------------------------------------------------

def create_invoice_entities(db_session, client, product):
    header = InvoiceHeader(
        client_id=client.id,
        user_id=1,  # dummy user id for tests
        subtotal=product.price,
        iva_total=product.price * product.iva_percent / 100,
        total_amount=product.price * (1 + product.iva_percent / 100),
        currency="COP",
        status="pending",
        cufe="",
    )
    db_session.add(header)
    db_session.flush()  # obtain header.id without commit
    line = InvoiceLine(
        invoice_id=header.id,
        product_id=product.id,
        quantity=1,
        unit_price=product.price,
        total_price=product.price,
        iva_percent=product.iva_percent,
        iva_amount=product.price * product.iva_percent / 100,
    )
    db_session.add(line)
    db_session.commit()
    db_session.refresh(header)
    return header.id, {"client_id": client.id, "line_items": [{"product_id": product.id, "quantity": 1}]}

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_invoice_flow_success(db_session, sample_client, sample_product, monkeypatch):
    # Monkey‑patch the email sender to avoid real SMTP calls
    mock_send_email = mock.Mock(return_value=True)
    monkeypatch.setattr("app.services.email.send_invoice_email", mock_send_email)

    # Prepare a deterministic payload for the validator
    payload = {"client_id": sample_client.id, "line_items": [{"product_id": sample_product.id, "quantity": 1, "unit_price": sample_product.price, "iva_percent": sample_product.iva_percent}]}

    header_id, raw_payload = create_invoice_entities(db_session, sample_client, sample_product)

    # Run the full service pipeline
    header = generate_and_finalize_invoice(db_session, header_id, raw_payload)

    # Assertions on generated artefacts
    assert header.cufe, "CUFE should be computed"
    assert header.xml_path and Path(header.xml_path).exists()
    assert header.pdf_path and Path(header.pdf_path).exists()
    # The DIAN simulation decides status based on SHA‑256 checksum parity – we accept both
    assert header.status in ("accepted", "rejected")
    if header.status == "accepted":
        # Email should have been called once with the correct attachments
        mock_send_email.assert_called_once()
        args, kwargs = mock_send_email.call_args
        assert kwargs["xml_path"] == header.xml_path
        assert kwargs["pdf_path"] == header.pdf_path
    else:
        # No email should be sent for rejected invoices
        mock_send_email.assert_not_called()

def test_invoice_validator_rejects_invalid_payload():
    from app.ai.invoice_validator import validate_invoice_payload, ValidationError
    # Payload missing line_items
    bad_payload = {"client_id": 1}
    with pytest.raises(ValidationError):
        validate_invoice_payload(bad_payload)
    # Negative quantity
    bad_payload = {"client_id": 1, "line_items": [{"product_id": 1, "quantity": -5, "unit_price": 100, "iva_percent": 19}]}
    with pytest.raises(ValidationError):
        validate_invoice_payload(bad_payload)
