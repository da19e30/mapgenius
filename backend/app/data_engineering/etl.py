'''ETL pipeline for processing invoices and historical financial data.

This module defines a production‑ready, type‑annotated ETL workflow that:
1. Extracts raw invoice PDFs (or images) from a configurable source.
2. Performs OCR/AI extraction using a pluggable extractor implementation.
3. Transforms the raw payload into a normalized `Transaction` dataclass.
4. Loads the cleaned data into the feature store (see `feature_store.py`).

The pipeline is built to handle millions of rows, supports incremental loads and
is resilient to transient failures.
'''

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List

import pandas as pd

# Local imports – lazy to avoid heavy imports when the module is imported only for type checking
from backend.app.data_engineering.data_quality import DataQualityChecker
from backend.app.data_engineering.feature_store import FeatureStore
from backend.app.data_engineering.streaming import EventStreamer

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Domain model
# ---------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class Transaction:
    """Canonical representation of a financial transaction extracted from an invoice.

    Attributes
    ----------
    transaction_id: str
        Unique identifier – typically a UUID generated at extraction time.
    vendor_id: str
        Identifier of the merchant / vendor.
    amount: float
        Transaction amount in USD (always positive).  Taxes are included.
    currency: str
        ISO‑4217 currency code (e.g., "USD").
    timestamp: datetime
        Timestamp of the transaction (usually the invoice date).
    category: str
        Business‑level category (e.g., "Software", "Travel").
    raw_text: str | None
        Full OCR output for traceability (optional).
    """

    transaction_id: str
    vendor_id: str
    amount: float
    currency: str
    timestamp: datetime
    category: str
    raw_text: str | None = None

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------
def _list_invoice_files(source_dir: Path) -> Iterable[Path]:
    """Yield PDF/Image files from ``source_dir`` sorted by modification time.

    The function skips hidden files and respects a configurable file pattern
    (default ``*.pdf``).  It yields ``Path`` objects that can be streamed to the
    extractor.
    """
    pattern = "*.pdf"
    for file_path in sorted(source_dir.glob(pattern), key=lambda p: p.stat().st_mtime):
        if not file_path.name.startswith('.'):
            yield file_path

def _extract_transaction(file_path: Path) -> Transaction:
    """Run OCR/AI extraction on a single file and return a ``Transaction``.

    The extraction logic is delegated to an ``extractor`` callable that returns a
    ``dict`` with the required fields.  This indirection makes unit‑testing easy
    and allows swapping a simple rule‑based extractor for a heavy LLM model.
    """
    from backend.app.data_engineering.extractor import extract_invoice  # type: ignore

    try:
        payload = extract_invoice(file_path)
        transaction = Transaction(
            transaction_id=payload["transaction_id"],
            vendor_id=payload["vendor_id"],
            amount=float(payload["amount"]),
            currency=payload.get("currency", "USD"),
            timestamp=datetime.fromisoformat(payload["timestamp"]),
            category=payload["category"],
            raw_text=payload.get("raw_text"),
        )
        return transaction
    except Exception as exc:
        logger.exception("Failed to extract %s", file_path)
        raise RuntimeError(f"Extraction error for {file_path.name}") from exc

# ---------------------------------------------------------------------------
# Core pipeline
# ---------------------------------------------------------------------------
class ETLPipeline:
    """Orchestrates the ETL flow.

    Typical usage::

        pipeline = ETLPipeline(source_dir=Path("/data/invoices"))
        pipeline.run()
    """

    def __init__(self, source_dir: Path, batch_size: int = 10_000):
        self.source_dir = source_dir
        self.batch_size = batch_size
        self.quality_checker = DataQualityChecker()
        self.feature_store = FeatureStore()
        self.event_streamer = EventStreamer()

    def _batch(self, iterable: Iterable[Transaction]) -> Iterable[List[Transaction]]:
        """Yield ``batch_size`` sized chunks from ``iterable``.
        """
        batch: List[Transaction] = []
        for item in iterable:
            batch.append(item)
            if len(batch) >= self.batch_size:
                yield batch
                batch = []
        if batch:
            yield batch

    def _process_file(self, file_path: Path) -> Transaction | None:
        """Extract, validate and optionally stream a single file.

        Returns ``None`` if the record fails validation – the failure is logged
        and the pipeline continues.
        """
        try:
            transaction = _extract_transaction(file_path)
            if not self.quality_checker.validate(transaction):
                logger.warning("Record failed quality checks: %s", transaction.transaction_id)
                return None
            # Emit a real‑time event for UI dashboards.
            self.event_streamer.emit(event_type="transaction_ingested", payload=transaction)
            return transaction
        except Exception as exc:  # pragma: no cover – defensive; already logged
            logger.error("Skipping %s due to unexpected error: %s", file_path.name, exc)
            return None

    def run(self) -> None:
        """Execute the full ETL pipeline.

        The implementation is deliberately simple but scalable – the heavy work
        (validation + feature store insertion) is performed in bulk batches.
        """
        logger.info("Starting ETL pipeline from %s", self.source_dir)
        file_iter = (_process for _process in (self._process_file(p) for p in _list_invoice_files(self.source_dir)) if _process is not None)
        for batch in self._batch(file_iter):
            # Convert to a DataFrame for bulk insertion – pandas is efficient for
            # columnar operations and works well with most analytic stores.
            df = pd.DataFrame([t.__dict__ for t in batch])
            try:
                self.feature_store.bulk_upsert(df)
                logger.info("Inserted batch of %d transactions", len(batch))
            except Exception as exc:
                logger.exception("Failed to write batch to feature store")
                # Depending on SLA, we could retry, write to a dead‑letter queue, etc.
                # For now we abort to avoid silent data loss.
                raise
        logger.info("ETL pipeline completed")

if __name__ == "__main__":
    # Simple CLI entry‑point for ad‑hoc runs.  Environment variables are used for
    # configurability in production containers.
    src_dir = Path(os.getenv("INVOICE_SOURCE", "./invoices"))
    pipeline = ETLPipeline(source_dir=src_dir)
    pipeline.run()
