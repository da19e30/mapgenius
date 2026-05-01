try:
    import spacy
    from spacy.util import minibatch, compounding
    SPACY_AVAILABLE = True
except ImportError:
    spacy = None
    minibatch = compounding = None
    SPACY_AVAILABLE = False

try:
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report
except ImportError:
    train_test_split = None
    classification_report = None
import os

if SPACY_AVAILABLE:
    # Load a small Spanish model; replace with appropriate model if needed
    try:
        nlp = spacy.load('es_core_news_sm')
    except Exception:
        nlp = spacy.blank('es')
else:
    nlp = None


class TransactionClassifier:
    """Clasificador de transacciones financieras usando spaCy TextCategorizer.

    Entrena un modelo con textos de transacciones y sus categorías (e.g., alimentación, transporte).
    """

    def __init__(self, model_path: str = 'models/transaction_classifier'):
        self.model_path = model_path
        self.textcat = None
        if SPACY_AVAILABLE and os.path.isdir(model_path):
            self.nlp = spacy.load(model_path)
            self.textcat = self.nlp.get_pipe('textcat')
        else:
            self.nlp = nlp

    def train(self, texts, labels, n_iter: int = 10):
        """Entrena el modelo."""
        if not SPACY_AVAILABLE:
            raise RuntimeError('spaCy is not installed, cannot train model')
        # Prepare training data
        unique_labels = list(set(labels))
        if 'textcat' not in self.nlp.pipe_names:
            textcat = self.nlp.add_pipe('textcat')
        else:
            textcat = self.nlp.get_pipe('textcat')
        for label in unique_labels:
            textcat.add_label(label)
        train_data = [(text, {'cats': {lbl: lbl == lab for lbl in unique_labels}})
                      for text, lab in zip(texts, labels)]
        optimizer = self.nlp.initialize(get_examples=lambda: [(self.nlp.make_doc(txt), annot) for txt, annot in train_data])
        for epoch in range(n_iter):
            losses = {}
            batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                docs = [self.nlp.make_doc(t) for t in texts]
                self.nlp.update(docs, annotations, sgd=optimizer, losses=losses)
            print(f'Epoch {epoch+1}/{n_iter} - Losses: {losses}')
        # Save model
        self.nlp.to_disk(self.model_path)
        self.textcat = self.nlp.get_pipe('textcat')
        return losses

    def predict(self, text: str) -> str:
        """Predice la categoría de una transacción."""
        if not SPACY_AVAILABLE or self.nlp is None:
            # fallback dummy classification
            return 'unknown'
        doc = self.nlp(text)
        if not self.textcat:
            raise RuntimeError('Modelo no entrenado')
        scores = doc.cats
        # Return label with highest score
        return max(scores, key=scores.get)

    def evaluate(self, texts, labels):
        if classification_report is None:
            return {}
        preds = [self.predict(t) for t in texts]
        report = classification_report(labels, preds)
        return report

# Helper to load existing classifier
def get_classifier():
    return TransactionClassifier()
