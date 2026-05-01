"""Utility functions for tax‑authority integration.

* generate_xml – builds a minimal XML document for an invoice (placeholder).
* send_to_authority – placeholder that would call the real DIAN/SAT web‑service.
"""

from lxml import etree
from datetime import datetime
from typing import Dict

def generate_xml(data: Dict) -> bytes:
    """Create a simple XML representation of an invoice.

    The real implementation must follow the XSD mandated by DIAN/SAT.
    Here we build a minimal compliant‑ish structure for early testing.
    """
    root = etree.Element("Invoice")
    etree.SubElement(root, "ID").text = str(data.get("id"))
    etree.SubElement(root, "Date").text = data.get("issued_at").isoformat()
    etree.SubElement(root, "Total").text = f"{data.get('total_amount'):.2f}"
    etree.SubElement(root, "Currency").text = data.get("currency", "USD")
    etree.SubElement(root, "Issuer").text = data.get("issuer", "UNKNOWN")
    etree.SubElement(root, "Receiver").text = data.get("receiver", "UNKNOWN")
    return etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8")

def validate_xml(xml_blob: bytes) -> None:
    """Validate that *xml_blob* is well‑formed XML.

    Raises ``ValueError`` if the document cannot be parsed.
    """
    try:
        etree.fromstring(xml_blob)
    except etree.XMLSyntaxError as exc:
        raise ValueError(f"XML syntax error: {exc}")


def send_to_authority(xml_blob: bytes, country: str) -> Dict:
    """Placeholder for real SOAP/REST call to DIAN (CO) or SAT (MX).

    Returns a dict with ``status`` (sent/accepted/rejected) and optional ``detail``.
    In production this would handle certificates, signing, error handling, etc.
    """
    # Simulación básica: siempre “sent” con timestamp
    return {
        "status": "sent",
        "detail": f"XML enviado a {country} en {datetime.utcnow().isoformat()}",
    }
