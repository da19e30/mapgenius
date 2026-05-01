try:
    import pandas as pd
except ImportError:
    pd = None
from collections import Counter
from datetime import datetime

class FinancialInsights:
    """Genera insights financieros a partir de los registros de FinancialData."""

    def __init__(self, df):
        if pd is None:
            raise RuntimeError('pandas not installed')
        self.df = df.copy()
        self.df['amount'] = pd.to_numeric(self.df['amount'], errors='coerce')
        self.df['transaction_date'] = pd.to_datetime(self.df['transaction_date'], errors='coerce')
        self.df.dropna(subset=['amount', 'transaction_date'], inplace=True)

    def category_distribution(self):
        dist = self.df.groupby('category')['amount'].sum().to_dict()
        return {k: round(v, 2) for k, v in dist.items()}

    def monthly_trend(self):
        self.df['month'] = self.df['transaction_date'].dt.to_period('M').astype(str)
        trend = self.df.groupby('month')['amount'].sum().reset_index()
        return [{'month': row['month'], 'total': round(row['amount'], 2)} for _, row in trend.iterrows()]

    def top_rfc_emitters(self, top_n: int = 5):
        if 'rfc_emisor' not in self.df.columns:
            return []
        cnt = Counter(self.df['rfc_emisor'].dropna())
        return [{'rfc': rfc, 'count': cnt[rfc]} for rfc, _ in cnt.most_common(top_n)]

    def unusual_spending_alert(self, threshold: float = 2.0):
        self.df['month'] = self.df['transaction_date'].dt.to_period('M')
        monthly = self.df.groupby(['category', 'month'])['amount'].sum().reset_index()
        alerts = []
        for cat, group in monthly.groupby('category'):
            mean = group['amount'].mean()
            std = group['amount'].std(ddof=0) or 0
            for _, row in group.iterrows():
                if std and row['amount'] > mean + threshold * std:
                    alerts.append({
                        'category': cat,
                        'month': str(row['month']),
                        'amount': round(row['amount'], 2),
                        'message': f'Gasto inusual en {cat} para {row["month"]}'
                    })
        return alerts

def generate_insights(records: list):
    if not records:
        return {}
    if pd is None:
        return {}
    df = pd.DataFrame(records)
    insights = FinancialInsights(df)
    return {
        'category_distribution': insights.category_distribution(),
        'monthly_trend': insights.monthly_trend(),
        'top_rfc_emitters': insights.top_rfc_emitters(),
        'unusual_spending_alerts': insights.unusual_spending_alert()
    }
