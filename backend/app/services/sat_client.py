"""Cliente de integración con el SAT (México).

Este cliente sigue la misma interfaz que ``DIANClient`` para simplificar el uso.
Se encarga de:
- Generar XML de factura electrónica conforme al esquema del SAT.
- Firmar el XML con una clave privada PEM (configurable vía ``SAT_PRIVATE_KEY``).
- Enviar el XML al endpoint del SAT (simulado en este MVP).
"""

import os
import base64
from lxml import etree
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import requests
from typing import Dict

class SATClient:
    def __init__(self):
        self.private_key_path = os.getenv("SAT_PRIVATE_KEY", "backend/keys/sat_private_key.pem")
        self.certificate_path = os.getenv("SAT_CERTIFICATE", "backend/keys/sat_certificate.pem")
        self.endpoint = os.getenv("SAT_ENDPOINT", "https://sandbox.sat.gob.mx/recepcion/v1")
        # cargar clave
        with open(self.private_key_path, "rb") as f:
            self.private_key = serialization.load_pem_private_key(f.read(), password=None)
        with open(self.certificate_path, "rb") as f:
            self.certificate = f.read()

    def _build_xml(self, invoice_data: Dict) -> bytes:
        root = etree.Element("Invoice")
        for k, v in invoice_data.items():
            elem = etree.SubElement(root, k)
            elem.text = str(v)
        return etree.tostring(root, xml_declaration=True, encoding="utf-8")

    def _sign_xml(self, xml_bytes: bytes) -> bytes:
        signature = self.private_key.sign(xml_bytes, padding.PKCS1v15(), hashes.SHA256())
        root = etree.fromstring(xml_bytes)
        sig_elem = etree.SubElement(root, "Signature")
        sig_elem.text = base64.b64encode(signature).decode()
        cert_elem = etree.SubElement(root, "Certificate")
        cert_elem.text = base64.b64encode(self.certificate).decode()
        return etree.tostring(root, xml_declaration=True, encoding="utf-8")

    def generate_xml(self, invoice_data: Dict) -> bytes:
        xml = self._build_xml(invoice_data)
        return self._sign_xml(xml)

    def send(self, signed_xml: bytes) -> Dict:
        try:
            response = requests.post(
                self.endpoint,
                data=signed_xml,
                headers={"Content-Type": "application/xml"},
                timeout=30,
            )
            response.raise_for_status()
            return {"status": "sent", "detail": response.text}
        except Exception as exc:
            return {"status": "error", "detail": str(exc)}
