"""PDF generation service for electronic invoices.

Uses a Jinja2 HTML template (``templates/invoice.html``) and WeasyPrint to create a PDF.
If WeasyPrint is not installed, the function falls back to creating a simple plain‑text
file so the pipeline does not break during development.
"""

import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Optional import – WeasyPrint provides accurate PDF rendering from HTML/CSS.
try:
    from weasyprint import HTML
    _WEASYPRINT_AVAILABLE = True
except Exception:
    _WEASYPRINT_AVAILABLE = False

TEMPLATE_DIR = Path(__file__).parents[2] / "templates"
ENV = Environment(
    loader=FileSystemLoader(str(TEMPLATE_DIR)),
    autoescape=select_autoescape(["html", "xml"]),
)

def render_invoice_pdf(data: dict, output_path: str) -> str:
    """Render ``data`` into a PDF file.

    Parameters
    ----------
    data: dict
        Context expected by ``templates/invoice.html`` (keys: emisor_name, emisor_nit,
        client, issue_date, cufe, lines, subtotal, iva_total, total_amount, currency).
    output_path: str
        Absolute path where the PDF will be written.

    Returns
    -------
    str
        The path to the generated PDF (same as ``output_path``).
    """
    template = ENV.get_template("invoice.html")
    html_content = template.render(**data)

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if _WEASYPRINT_AVAILABLE:
        HTML(string=html_content).write_pdf(output_path)
    else:
        # Fallback: write the HTML content with .pdf extension – useful for debugging
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
    return output_path
