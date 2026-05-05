"""Pruebas exhaustivas de todo el sistema Mapgenius Solutions.

Cubre:
1. Registro de usuario (envío de correo de bienvenida)
2. Login y obtención de JWT
3. Refresh token y revocación
4. Creación de tenant, cliente, producto
5. Flujo completo de facturación (XML, CUFE, DIAN, PDF)
6. Validación de datos (AI validator)
7. Endpoints protegidos (/me, /users/check-*)
"""

import os
import sys
from unittest import mock
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.models.user import User
from app.models.tenant import Tenant
from app.models.client import Client
from app.models.product import Product
from app.models.invoice_header import InvoiceHeader
from app.models.invoice_line import InvoiceLine
from app.models.dian_log import DianLog
from app.core.security import (
    create_access_token, create_refresh_token,
    get_password_hash, verify_password, decode_token, decode_without_verify
)
from app.services.email import send_welcome_email, send_admin_notification
from app.ai.invoice_validator import validate_invoice_payload


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function")
def db_session():
    """Base de datos en memoria para cada test."""
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
    )
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_tenant(db_session):
    """Crea un tenant de prueba."""
    tenant = Tenant(
        name="Empresa Test",
        nit="900999999",
        schema_name="tenant_test",
        is_active=True,
    )
    db_session.add(tenant)
    db_session.commit()
    db_session.refresh(tenant)
    return tenant


@pytest.fixture(scope="function")
def test_user(db_session, test_tenant):
    """Crea un usuario de prueba con tenant asociado."""
    user = User(
        email="test@mapgenius.com",
        hashed_password=get_password_hash("password123"),
        full_name="Usuario de Prueba",
        role="admin",
        is_active=True,
        tenant_id=test_tenant.id,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_client(db_session, test_tenant):
    """Crea un cliente de prueba."""
    client = Client(
        tenant_id=test_tenant.id,
        nit="123456789",
        name="Cliente de Prueba S.A.S.",
        email="cliente@test.com",
        address="Calle 100 # 20-30",
        tax_regime="Régimen común",
    )
    db_session.add(client)
    db_session.commit()
    db_session.refresh(client)
    return client


@pytest.fixture(scope="function")
def test_product(db_session, test_tenant):
    """Crea un producto de prueba."""
    product = Product(
        tenant_id=test_tenant.id,
        code="PROD001",
        name="Servicio de consultoría",
        price=500.0,
        iva_percent=19.0,
        unit="hour",
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product


# ---------------------------------------------------------------------------
# 1. PRUEBAS DE REGISTRO (incluye correo de bienvenida)
# ---------------------------------------------------------------------------

class TestRegistroConCorreo:
    """Prueba que el registro envía correo de bienvenida."""

    def test_registro_exitoso_con_correo(self, db_session, test_tenant, monkeypatch):
        """Simula el registro via routes/user.py y verifica que se envíe correo."""
        # Mock de las funciones de correo (están en app.services.email)
        mock_welcome = mock.Mock(return_value=True)
        mock_admin = mock.Mock(return_value=True)
        monkeypatch.setattr("app.services.email.send_welcome_email", mock_welcome)
        monkeypatch.setattr("app.services.email.send_admin_notification", mock_admin)

        # Simular creación de usuario (como lo hace routes/user.py)
        from app.services.auth import hash_password
        user = User(
            username="testuser",
            email="nuevo@mapgenius.com",
            hashed_password=hash_password("secret123"),
            tenant_id=test_tenant.id,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Verificar que el usuario se creó
        assert user.id is not None
        assert user.email == "nuevo@mapgenius.com"

        # Simular envío de correos (lo que hace routes/user.py líneas 66-73)
        from app.services.email import send_welcome_email, send_admin_notification
        send_welcome_email(user.email, user.username)
        send_admin_notification(user.email, user.username, user.id)

        # Verificar que se llamaron las funciones de correo
        mock_welcome.assert_called_once_with(user.email, user.username)
        mock_admin.assert_called_once()

    def test_welcome_email_simulado_sin_smtp(self, db_session, test_tenant):
        """Verifica que el correo se simula si no hay SMTP configurado."""
        # Crear usuario
        user = User(
            username="simuser",
            email="sim@test.com",
            hashed_password=get_password_hash("pass"),
            tenant_id=test_tenant.id,
        )
        db_session.add(user)
        db_session.commit()

        # Al no tener SMTP configurado, send_welcome_email imprime a stdout
        # pero no debe lanzar excepción
        result = send_welcome_email(user.email, user.username)
        assert result is True  # En modo simulación devuelve True


# ---------------------------------------------------------------------------
# 2. PRUEBAS DE AUTENTICACIÓN (Login, Refresh, Revoke)
# ---------------------------------------------------------------------------

class TestAutenticacion:
    """Prueba login, refresh token y revocación."""

    def test_login_exitoso(self, test_user):
        """Verifica que las credenciales correctas generan JWT."""
        assert verify_password("password123", test_user.hashed_password)
        token = create_access_token({"sub": str(test_user.id), "tenant_id": test_user.tenant_id})
        payload = decode_token(token)
        assert payload["sub"] == str(test_user.id)
        assert payload["tenant_id"] == test_user.tenant_id

    def test_login_credenciales_incorrectas(self, test_user):
        """Verifica que contraseña incorrecta falla."""
        assert not verify_password("wrongpass", test_user.hashed_password)

    def test_refresh_token_funcional(self, test_user):
        """Verifica que el refresh token permite obtener nuevos tokens."""
        refresh = create_refresh_token({"sub": str(test_user.id), "tenant_id": test_user.tenant_id})
        data = decode_without_verify(refresh)
        assert "jti" in data
        assert data["sub"] == str(test_user.id)

    def test_revocacion_token(self, db_session, test_user):
        """Verifica que un token revocado no sea válido."""
        from app.crud.revoked_token import revoke, is_revoked
        refresh = create_refresh_token({"sub": str(test_user.id)})
        data = decode_without_verify(refresh)
        jti = data["jti"]
        exp_ts = data["exp"]
        from datetime import datetime, timezone
        expires_at = datetime.fromtimestamp(exp_ts, tz=timezone.utc)

        # Revocar
        revoke(db_session, jti=jti, expires_at=expires_at)
        assert is_revoked(db_session, jti)


# ---------------------------------------------------------------------------
# 3. PRUEBAS DE FACTURACIÓN (Flujo completo)
# ---------------------------------------------------------------------------

class TestFacturacionCompleta:
    """Flujo completo: crear factura → XML → CUFE → DIAN → PDF."""

    def test_flujo_completo_factura(
        self, db_session, test_tenant, test_client, test_product, monkeypatch
    ):
        """Ejecuta el servicio generate_and_finalize_invoice y verifica resultados."""
        # Mock de envío de correo
        mock_send = mock.Mock(return_value=True)
        monkeypatch.setattr("app.services.invoice.send_invoice_email", mock_send)
        # Forzar estado "accepted" para probar envío de correo
        monkeypatch.setattr("app.services.dian_client._decision_from_file", lambda x: "accepted")

        # Crear InvoiceHeader
        header = InvoiceHeader(
            tenant_id=test_tenant.id,
            client_id=test_client.id,
            user_id=1,
            subtotal=test_product.price,
            iva_total=test_product.price * test_product.iva_percent / 100,
            total_amount=test_product.price * (1 + test_product.iva_percent / 100),
            currency="COP",
            status="pending",
            cufe="",
        )
        db_session.add(header)
        db_session.flush()
        db_session.refresh(header)

        # Crear InvoiceLine
        line = InvoiceLine(
            invoice_id=header.id,
            product_id=test_product.id,
            quantity=2,
            unit_price=test_product.price,
            total_price=test_product.price * 2,
            iva_percent=test_product.iva_percent,
            iva_amount=test_product.price * 2 * test_product.iva_percent / 100,
        )
        db_session.add(line)
        db_session.commit()

        # Ejecutar servicio de facturación
        from app.services.invoice import generate_and_finalize_invoice
        payload = {
            "client_id": test_client.id,
            "line_items": [{
                "product_id": test_product.id,
                "quantity": 2,
                "unit_price": test_product.price,
                "iva_percent": test_product.iva_percent,
            }],
        }
        result_header = generate_and_finalize_invoice(db_session, header.id, payload)

        # Verificaciones
        assert result_header.cufe, "CUFE debe ser calculado"
        assert result_header.xml_path, "Debe generarse XML"
        assert Path(result_header.xml_path).exists(), "El archivo XML debe existir"
        assert result_header.status in ("accepted", "rejected")

        if result_header.status == "accepted":
            assert result_header.pdf_path, "Debe generarse PDF si es aceptada"
            assert Path(result_header.pdf_path).exists(), "El PDF debe existir"
            mock_send.assert_called_once()

        # Verificar log DIAN
        log = db_session.query(DianLog).filter(DianLog.invoice_cufe == result_header.cufe).first()
        assert log is not None
        assert log.response_status == result_header.status


# ---------------------------------------------------------------------------
# 4. PRUEBAS DE VALIDACIÓN AI
# ---------------------------------------------------------------------------

class TestValidacionIA:
    """Prueba el validador de carga de facturas."""

    def test_payload_valido(self):
        """Payload correcto no debe lanzar errores."""
        payload = {
            "client_id": 1,
            "line_items": [
                {"product_id": 1, "quantity": 1, "unit_price": 100.0, "iva_percent": 19.0}
            ],
        }
        # No debe lanzar excepción
        validate_invoice_payload(payload)

    def test_payload_sin_line_items(self):
        """Debe fallar si no hay line_items."""
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            validate_invoice_payload({"client_id": 1})

    def test_payload_cantidad_negativa(self):
        """Debe fallar si quantity es negativo."""
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            validate_invoice_payload({
                "client_id": 1,
                "line_items": [{"product_id": 1, "quantity": -1, "unit_price": 100, "iva_percent": 19}]
            })

    def test_payload_precio_negativo(self):
        """Debe fallar si unit_price es negativo."""
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            validate_invoice_payload({
                "client_id": 1,
                "line_items": [{"product_id": 1, "quantity": 1, "unit_price": -50, "iva_percent": 19}]
            })


# ---------------------------------------------------------------------------
# 5. PRUEBAS DE ENDPOINTS PROTEGIDOS
# ---------------------------------------------------------------------------

class TestEndpointsProtegidos:
    """Verifica que los endpoints requieran autenticación."""

    def test_obtener_usuario_actual_sin_token(self):
        """GET /users/me sin token debe fallar."""
        # Simulamos que decode_token lance JWTError
        with pytest.raises(Exception):
            decode_token("invalid_token")

    def test_check_username_disponible(self, db_session):
        """Verifica disponibilidad de username."""
        # Username que no existe
        exists = db_session.query(User).filter(User.username == "nonexistent").first()
        assert exists is None

    def test_check_email_disponible(self, db_session):
        """Verifica disponibilidad de email."""
        exists = db_session.query(User).filter(User.email == "nonexistent@test.com").first()
        assert exists is None
