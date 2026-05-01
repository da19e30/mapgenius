import re
from datetime import datetime
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    spacy = None
    SPACY_AVAILABLE = False

# Load Spanish model for NER if needed
if SPACY_AVAILABLE:
    try:
        nlp = spacy.load('es_core_news_sm')
    except Exception:
        nlp = None
else:
    nlp = None

class OCREnhancer:
    """Mejora la extracción OCR usando expresiones regulares y NLP para detectar
    montos, fechas, RFC, y otros campos clave en texto de factura.
    """

    # Regex patterns for common invoice fields
    AMOUNT_PATTERN = r'(?:total|importe|monto|amount)[:\s]*[$]?\s*([\d.,]+)'
    DATE_PATTERNS = [
        r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b',
        r'\b(\d{4}[/-]\d{1,2}[/-]\d{1,2})\b',
        r'\b(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})\b',  # 15 de enero de 2023
    ]
    RFC_PATTERN = r'\b([A-Z&Ñ]{3,4}\d{6}[A-Z\d]{2,3})\b'  # Mexican RFC pattern
    RFC_PATTERN_ALT = r'(?:RFC|rfc)[:\s]*([A-Z&Ñ]{3,4}\d{6}[A-Z\d]{2,3})'

    def __init__(self):
        pass

    def enhance(self, text: str) -> dict:
        """Procesa texto OCR y extrae campos estructurados.

        Returns:
            dict con claves: total_amount, issue_date, rfc_emisor, rfc_receptor, etc.
        """
        result = {
            'total_amount': None,
            'issue_date': None,
            'rfc_emisor': None,
            'rfc_receptor': None,
            'currency': None,
            'invoice_number': None,
        }
        if not text:
            return result

        # Extraer monto total
        total = self._extract_total(text)
        if total:
            result['total_amount'] = total

        # Extraer fecha
        date = self._extract_date(text)
        if date:
            result['issue_date'] = date

        # Extraer RFC
        rfc = self._extract_rfc(text)
        if rfc:
            result['rfc_emisor'] = rfc

        # Extraer moneda (por contexto)
        currency = self._extract_currency(text)
        if currency:
            result['currency'] = currency

        # Extraer número de factura (folio)
        folio = self._extract_invoice_number(text)
        if folio:
            result['invoice_number'] = folio

        # Usar spaCy para NER si está disponible
        if nlp:
            doc = nlp(text[:1000])  # limitar longitud
            for ent in doc.ents:
                if ent.label_ == 'ORG' and not result['rfc_emisor']:
                    # podría ser razón social
                    pass

        return result

    def _extract_total(self, text: str):
        # Buscar patrones de total
        for pat in [self.AMOUNT_PATTERN]:
            matches = re.search(pat, text, re.IGNORECASE)
            if matches:
                amount_str = matches.group(1).replace(',', '')
                try:
                    return float(amount_str)
                except ValueError:
                    pass
        # fallback: buscar números con decimales más largos
        nums = re.findall(r'(?:^|\s)([\d,]+\.\d{2})(?:\s|$)', text)
        if nums:
            try:
                return float(nums[-1].replace(',', ''))
            except ValueError:
                pass
        return None

    def _extract_date(self, text: str):
        for pat in self.DATE_PATTERNS:
            match = re.search(pat, text)
            if match:
                date_str = match.group(1)
                # intentar parsear
                for fmt in ['%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d', '%Y-%m-%d', '%d/%m/%y', '%d-%m-%y']:
                    try:
                        return datetime.strptime(date_str, fmt).date().isoformat()
                    except ValueError:
                        continue
                # Formato "15 de enero de 2023"
                try:
                    # simple: extraer componentes
                    parts = date_str.split(' de ')
                    if len(parts) == 3:
                        day = int(parts[0])
                        month_map = {'enero':1,'febrero':2,'marzo':3,'abril':4,'mayo':5,'junio':6,
                                     'julio':7,'agosto':8,'septiembre':9,'octubre':10,'noviembre':11,'diciembre':12}
                        month = month_map.get(parts[1].lower())
                        year = int(parts[2])
                        if month:
                            return datetime(year, month, day).date().isoformat()
                except Exception:
                    pass
        return None

    def _extract_rfc(self, text: str):
        # Buscar patrón RFC con prefijo
        match = re.search(self.RFC_PATTERN_ALT, text, re.IGNORECASE)
        if match:
            return match.group(1)
        # buscar patrón simple
        match = re.search(self.RFC_PATTERN, text)
        if match:
            return match.group(1)
        return None

    def _extract_currency(self, text: str):
        if re.search(r'\$|USD|dólares?', text, re.IGNORECASE):
            return 'USD'
        if re.search(r'€|EUR|euros?', text, re.IGNORECASE):
            return 'EUR'
        if re.search(r'MXN|pesos? mexicanos?', text, re.IGNORECASE):
            return 'MXN'
        return None

    def _extract_invoice_number(self, text: str):
        # Buscar palabras como "Factura:", "Folio:", "No.", etc.
        pats = [r'(?:factura|folio|no\.?)[:\s]*([A-Z0-9\-]+)', r'\b(F[A-Z0-9]{5,})\b']
        for pat in pats:
            match = re.search(pat, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

# Singleton
def get_enhancer():
    return OCREnhancer()
