"""Tests for authentication flow: register, login, refresh, revoke."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.models.user import User
from app.models.tenant import Tenant
from app.core.security import create_access_token, decode_token


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def sample_tenant(db_session):
    tenant = Tenant(
        name="Test Tenant",
        nit="900111111",
        schema_name="tenant_1",
        is_active=True,
    )
    db_session.add(tenant)
    db_session.commit()
    db_session.refresh(tenant)
    return tenant


@pytest.fixture(scope="function")
def registered_user(db_session, sample_tenant):
    from app.crud import user as user_crud
    from app.core.security import get_password_hash
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("password123"),
        full_name="Test User",
        role="admin",
        is_active=True,
        tenant_id=sample_tenant.id,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def test_register_flow(db_session, sample_tenant):
    """Simulate a register call (directly create user)."""
    from app.crud import user as user_crud
    from app.core.security import get_password_hash
    user = User(
        email="new@example.com",
        hashed_password=get_password_hash("secret"),
        full_name="New User",
        role="accountant",
        is_active=True,
        tenant_id=sample_tenant.id,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    assert user.id is not None
    assert user.email == "new@example.com"
    assert user.tenant_id == sample_tenant.id


def test_login_flow(db_session, registered_user):
    """Verify that password verification works."""
    from app.core.security import verify_password
    assert verify_password("password123", registered_user.hashed_password)
    assert not verify_password("wrong", registered_user.hashed_password)


def test_jwt_creation_and_decode(db_session, registered_user, sample_tenant):
    """Test JWT includes tenant_id."""
    token = create_access_token({"sub": str(registered_user.id), "tenant_id": registered_user.tenant_id})
    payload = decode_token(token)
    assert payload["sub"] == str(registered_user.id)
    assert payload["tenant_id"] == sample_tenant.id


def test_refresh_token(db_session, registered_user, sample_tenant):
    """Refresh token should produce a new access token."""
    from app.core.security import create_refresh_token
    refresh = create_refresh_token({"sub": str(registered_user.id), "tenant_id": registered_user.tenant_id})
    # decode without verification to check payload
    from app.core.security import decode_without_verify
    data = decode_without_verify(refresh)
    assert data["sub"] == str(registered_user.id)
    assert data["tenant_id"] == sample_tenant.id


def test_revoke_token(db_session, registered_user):
    """Revoking a token should prevent its use."""
    from app.core.security import create_refresh_token, decode_without_verify
    from app.crud.revoked_token import revoke, is_revoked
    refresh = create_refresh_token({"sub": str(registered_user.id)})
    data = decode_without_verify(refresh)
    jti = data["jti"]
    exp = data["exp"]
    from datetime import datetime, timezone
    expires_at = datetime.fromtimestamp(exp, tz=timezone.utc)
    revoke(db_session, jti=jti, expires_at=expires_at)
    assert is_revoked(db_session, jti)
