import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Load dataset
data = pd.read_csv("spam.csv", encoding="latin-1")

# Keep only first two columns safely
data = data.iloc[:, :2]
data.columns = ["label", "text"]

# Convert labels
data["label"] = data["label"].map({"ham": 0, "spam": 1})

# Clean data
data = data.dropna()

X = data["text"]
y = data["label"]

# Train-test split (good ML practice)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Better ML pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english", ngram_range=(1,2))),
    ("clf", LogisticRegression(max_iter=200))
])

# Train model
model.fit(X_train, y_train)

# Accuracy check
accuracy = model.score(X_test, y_test)
print("Accuracy:", accuracy)

# Save model
joblib.dump(model, "model.pkl")

print("Model trained successfully!")