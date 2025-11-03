# expenses/ai_utils.py
import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'expense_classifier.pkl')

# canonical choices used in model and forms (must match Expense.CATEGORY_CHOICES)
CANONICAL = {
    'food': 'Food',
    'pizza': 'Food',
    'restaurant': 'Food',
    'groceries': 'Food',
    'transport': 'Travel',
    'uber': 'Travel',
    'bus': 'Travel',
    'travel': 'Travel',
    'entertainment': 'Entertainment',
    'movie': 'Entertainment',
    'netflix': 'Entertainment',
    'utilities': 'Utilities',
    'electricity': 'Utilities',
    'sharing': 'Sharing',
    'other': 'Other',
    'others': 'Other',
}

model_tuple = None
if os.path.exists(MODEL_PATH):
    model_tuple = joblib.load(MODEL_PATH)  # expecting (vectorizer, model)

def normalize_prediction(pred):
    """Map model/fallback outputs to one of the Expense.CATEGORY_CHOICES values."""
    if not pred:
        return 'Other'
    key = str(pred).lower()
    # direct map
    if key in CANONICAL:
        return CANONICAL[key]
    # fallback heuristics
    for k, v in CANONICAL.items():
        if k in key:
            return v
    # if unknown, return Other
    return 'Other'

def predict_category(text: str) -> str:
    """Return a canonical category (one of Expense choices)."""
    text = (text or '').strip()
    if not text:
        return 'Other'

    # if model file exists, use it
    if model_tuple:
        vectorizer, model = model_tuple
        try:
            X = vectorizer.transform([text])
            pred = model.predict(X)[0]
            return normalize_prediction(pred)
        except Exception as e:
            print("ai_utils: model prediction failed:", e)

    # fallback rule-based
    t = text.lower()
    for k, v in CANONICAL.items():
        if k in t:
            return v

    return 'Other'
