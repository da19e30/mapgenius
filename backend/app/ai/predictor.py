try:
    import pandas as pd
except ImportError:
    pd = None

try:
    from sklearn.linear_model import LinearRegression
except ImportError:
    LinearRegression = None

try:
    import joblib
except ImportError:
    joblib = None

import os
from datetime import datetime

class CashFlowPredictor:
    """Predictor simple de flujo de caja usando regresión lineal."""

    def __init__(self, model_path: str = 'models/cashflow_predictor.pkl'):
        self.model_path = model_path
        self.model = None
        if joblib and os.path.isfile(model_path):
            try:
                self.model = joblib.load(model_path)
            except Exception:
                self.model = None

    def _prepare_features(self, df):
        if pd is None:
            raise RuntimeError('pandas not installed')
        df = df.copy()
        df['timestamp'] = pd.to_datetime(df['transaction_date']).astype(int) / 10**9
        X = df[['timestamp']]
        y = df['amount'].astype(float)
        return X, y

    def train(self, df):
        if pd is None or LinearRegression is None:
            raise RuntimeError('Required libraries not installed')
        X, y = self._prepare_features(df)
        self.model = LinearRegression()
        self.model.fit(X, y)
        # Save model for later use
        if joblib:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump(self.model, self.model_path)
        return self.model

    def predict_future(self, days_ahead: int = 30) -> float:
        if not self.model:
            raise RuntimeError('Modelo de predicción no entrenado')
        future_ts = (datetime.utcnow().timestamp() + days_ahead * 86400)
        pred = self.model.predict([[future_ts]])
        return float(pred[0])

# Helper singleton
def get_predictor():
    return CashFlowPredictor()
