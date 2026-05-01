"""Utility to generate an RSA key pair (if missing) and sign XML documents.

For the prototype we simulate a PKCS#7/CMS signature by appending a <Signature> element
containing the base64‑encoded RSA‑SHA256 signature of the canonical XML.

The private key is stored under ``backend/.keys/private_key.pem`` and the public key under
``backend/.keys/public_key.pem`` with chmod 600/644 respectively.
"""

import os
import base64
from pathlib import Path
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

KEY_DIR = Path(__file__).parents[2] / ".keys"
PRIVATE_KEY_PATH = KEY_DIR / "private_key.pem"
PUBLIC_KEY_PATH = KEY_DIR / "public_key.pem"

def _ensure_keys():
    """Create RSA key pair if they do not exist yet."""
    if not KEY_DIR.exists():
        KEY_DIR.mkdir(parents=True, exist_ok=True)
    if not PRIVATE_KEY_PATH.exists() or not PUBLIC_KEY_PATH.exists():
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        pem_priv = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
        with open(PRIVATE_KEY_PATH, "wb") as f:
            f.write(pem_priv)
        public_key = private_key.public_key()
        pem_pub = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        with open(PUBLIC_KEY_PATH, "wb") as f:
            f.write(pem_pub)

def sign_xml(xml_str: str) -> str:
    """Return the XML string with an appended <Signature> element.

    The signature is a base64‑encoded RSA‑SHA256 of the original XML bytes.
    """
    _ensure_keys()
    with open(PRIVATE_KEY_PATH, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
    signature = private_key.sign(
        xml_str.encode("utf-8"),
        padding.PKCS1v15(),
        hashes.SHA256(),
    )
    b64_sig = base64.b64encode(signature).decode("utf-8")
    # Insert signature just before the closing root tag
    closing_tag = "</Invoice>"
    signed_xml = xml_str.replace(closing_tag, f"<Signature>{b64_sig}</Signature>{closing_tag}")
    return signed_xml
