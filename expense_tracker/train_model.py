import os
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Sample training data (you can expand this later)
descriptions = [
    "pizza", "burger", "restaurant bill", "groceries", "bus ticket", "uber ride",
    "movie ticket", "netflix subscription", "electricity bill", "mobile recharge"
]
categories = [
    "Food", "Food", "Food", "Groceries", "Transport", "Transport",
    "Entertainment", "Entertainment", "Utilities", "Utilities"
]

# Create and train model
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(descriptions)

model = MultinomialNB()
model.fit(X, categories)

# Save model and vectorizer
model_dir = os.path.join("expenses", "models")
os.makedirs(model_dir, exist_ok=True)

joblib.dump((model, vectorizer), os.path.join(model_dir, "expense_classifier.pkl"))

print("Model trained and saved to 'expenses/models/expense_classifier.pkl'")
