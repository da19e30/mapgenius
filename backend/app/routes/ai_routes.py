from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.invoice import Invoice
from app.models.financial_data import FinancialData
from app.models.user import User
from app.services.auth import get_current_user
from app.ai.classifier import get_classifier
from app.ai.predictor import get_predictor
from app.ai.insights import generate_insights
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter(prefix="/ai", tags=["ai"])

class TransactionRequest(BaseModel):
    description: str
    amount: float
    currency: str = "USD"
    transaction_date: str  # ISO format
    user_id: int

class PredictionResponse(BaseModel):
    future_cash_flow: float
    days_ahead: int

@router.post("/classify", response_model=Dict[str, str])
async def classify_transaction(request: TransactionRequest,
                               db: Session = Depends(get_db),
                               current_user: User = Depends(get_current_user)):
    """Clasifica automáticamente la categoría de una transacción usando el modelo de IA."""
    if current_user.id != request.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="No está autorizado a clasificar esta transacción")
    classifier = get_classifier()
    try:
        category = classifier.predict(request.description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en clasificación: {str(e)}")
    # Persistir en FinancialData
    fd = FinancialData(
        user_id=request.user_id,
        invoice_id=None,
        category=category,
        amount=str(request.amount),
        currency=request.currency,
        transaction_date=request.transaction_date,
        confidence_score=1.0
    )
    db.add(fd)
    db.commit()
    db.refresh(fd)
    return {"category": category, "financial_data_id": str(fd.id)}

@router.get("/predict", response_model=PredictionResponse)
async def predict_cash_flow(days_ahead: int = 30,
                            db: Session = Depends(get_db),
                            current_user: User = Depends(get_current_user)):
    """Predice el flujo de caja futuro del usuario basado en datos históricos."""
    records = db.query(FinancialData).filter(FinancialData.user_id == current_user.id).all()
    if not records:
        raise HTTPException(status_code=404, detail="No hay datos financieros para predecir")
    # Convertir a DataFrame amigable para el predictor
    try:
        import pandas as pd
    except ImportError:
        raise HTTPException(status_code=500, detail="Pandas is required for predictions but is not installed.")
    df = pd.DataFrame([{
        "amount": r.amount,
        "transaction_date": r.transaction_date
    } for r in records])
    predictor = get_predictor()
    if predictor.model is None:
        # Entrenar rápidamente con los datos disponibles
        predictor.train(df)
    future_amount = predictor.predict_future(days_ahead)
    return PredictionResponse(future_cash_flow=round(future_amount, 2), days_ahead=days_ahead)

@router.get("/insights", response_model=Dict[str, Any])
async def get_insights(db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    """Genera insights financieros para el usuario actual."""
    records = db.query(FinancialData).filter(FinancialData.user_id == current_user.id).all()
    if not records:
        raise HTTPException(status_code=404, detail="No hay datos financieros disponibles")
    # Convertir a lista de dicts
    data = [{
        "category": r.category,
        "amount": r.amount,
        "transaction_date": r.transaction_date,
        "rfc_emisor": getattr(r, 'rfc_emisor', None)
    } for r in records]
    insights = generate_insights(data)
    return insights
