"""Utilities to generate UBL‑2.1 XML for electronic invoices (DIAN).

The implementation focuses on the required elements for a minimal, valid invoice:
- Cabecera (Emisor, Receptor, Fecha, CUFE)
- Detalle de líneas (producto, cantidad, precio, IVA)
- Totales (Subtotal, IVA, Total)

The functions return the XML string, the computed CUFE (SHA‑256 hash of the canonical XML) and optionally write the file to disk.
"""

import hashlib
from lxml import etree
from datetime import datetime
from typing import List, Dict

NSMAP = {
    "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
    "cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
    "ext": "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2",
    "ds": "http://www.w3.org/2000/09/xmldsig#",
    "ubl": "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2",
}

def _create_element(tag: str, text: str | None = None, ns: str = "cbc"):
    el = etree.Element(f"{{{NSMAP[ns]}}}{tag}")
    if text is not None:
        el.text = str(text)
    return el

def generate_invoice_xml(header: Dict, lines: List[Dict]) -> str:
    """Build a minimal UBL‑2.1 Invoice XML.

    *header* expects keys: cufe, issue_date, currency, client (dict with nit, name, address, tax_regime).
    *lines* is a list of dicts with product_code, description, quantity, unit_price, iva_percent.
    """
    inv = etree.Element("{urn:oasis:names:specification:ubl:schema:xsd:Invoice-2}Invoice", nsmap=NSMAP)

    # Versión UBL
    inv.append(_create_element("CustomizationID", "2.1", ns="cbc"))
    inv.append(_create_element("ProfileID", "DIAN 2.1", ns="cbc"))
    inv.append(_create_element("ID", header["cufe"], ns="cbc"))
    inv.append(_create_element("IssueDate", header["issue_date"].split("T")[0], ns="cbc"))
    inv.append(_create_element("InvoiceTypeCode", "01", ns="cbc"))  # 01 = factura de venta
    inv.append(_create_element("DocumentCurrencyCode", header["currency"], ns="cbc"))

    # Emisor (hard‑coded for demo purposes)
    accounting_supplier = etree.SubElement(inv, f"{{{NSMAP['cac']}}}AccountingSupplierParty")
    party = etree.SubElement(accounting_supplier, f"{{{NSMAP['cac']}}}Party")
    party.append(_create_element("PartyIdentification", header["emisor_nit"], ns="cbc"))
    party.append(_create_element("PartyName", header["emisor_name"], ns="cbc"))
    # Receptor
    accounting_customer = etree.SubElement(inv, f"{{{NSMAP['cac']}}}AccountingCustomerParty")
    party_cust = etree.SubElement(accounting_customer, f"{{{NSMAP['cac']}}}Party")
    party_cust.append(_create_element("PartyIdentification", header["client"]["nit"], ns="cbc"))
    party_cust.append(_create_element("PartyName", header["client"]["name"], ns="cbc"))
    if header["client"].get("address"):
        address = etree.SubElement(party_cust, f"{{{NSMAP['cac']}}}PostalAddress")
        address.append(_create_element("StreetName", header["client"]["address"], ns="cbc"))

    # Totales
    legal_monetary = etree.SubElement(inv, f"{{{NSMAP['cac']}}}LegalMonetaryTotal")
    legal_monetary.append(_create_element("LineExtensionAmount", f"{header['subtotal']:.2f}", ns="cbc"))
    legal_monetary.append(_create_element("TaxInclusiveAmount", f"{header['total']:.2f}", ns="cbc"))
    legal_monetary.append(_create_element("PayableAmount", f"{header['total']:.2f}", ns="cbc"))

    # Detalle de líneas
    for idx, line in enumerate(lines, start=1):
        inv_line = etree.SubElement(inv, f"{{{NSMAP['cac']}}}InvoiceLine")
        inv_line.append(_create_element("ID", str(idx), ns="cbc"))
        inv_line.append(_create_element("InvoicedQuantity", str(line["quantity"]), ns="cbc"))
        inv_line.append(_create_element("LineExtensionAmount", f"{line['total_price']:.2f}", ns="cbc"))
        # Precio unitario
        price_el = etree.SubElement(inv_line, f"{{{NSMAP['cac']}}}Price")
        price_el.append(_create_element("PriceAmount", f"{line['unit_price']:.2f}", ns="cbc"))
        # Impuesto IVA
        tax_total = etree.SubElement(inv_line, f"{{{NSMAP['cac']}}}TaxTotal")
        tax_total.append(_create_element("TaxAmount", f"{line['iva_amount']:.2f}", ns="cbc"))
        tax_sub = etree.SubElement(tax_total, f"{{{NSMAP['cac']}}}TaxSubtotal")
        tax_sub.append(_create_element("TaxableAmount", f"{line['total_price']:.2f}", ns="cbc"))
        tax_sub.append(_create_element("TaxAmount", f"{line['iva_amount']:.2f}", ns="cbc"))
        tax_category = etree.SubElement(tax_sub, f"{{{NSMAP['cac']}}}TaxCategory")
        tax_category.append(_create_element("ID", "S", ns="cbc"))
        tax_category.append(_create_element("Percent", f"{line['iva_percent']}", ns="cbc"))
        # Descripción del ítem
        item = etree.SubElement(inv_line, f"{{{NSMAP['cac']}}}Item")
        item.append(_create_element("Description", line["description"], ns="cbc"))
        # Producto
        prod = etree.SubElement(inv_line, f"{{{NSMAP['cac']}}}Product")
        prod.append(_create_element("Name", line["product_name"], ns="cbc"))
        prod.append(_create_element("SellerItemIdentification", line["product_code"], ns="cbc"))

    # Serializar a string (pretty print disabled for canonical form)
    xml_bytes = etree.tostring(inv, encoding="utf-8", xml_declaration=True)
    return xml_bytes.decode("utf-8")

def compute_cufe(xml_str: str) -> str:
    """Compute the CUFE as the SHA‑256 hash of the canonical XML string.
    The DIAN spec uses a specific canonicalisation; for this demo we simply hash the UTF‑8 bytes.
    """
    digest = hashlib.sha256(xml_str.encode("utf-8")).hexdigest().upper()
    return digest
