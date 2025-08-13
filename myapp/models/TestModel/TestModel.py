import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

# Load data
df = pd.read_csv("labeled_data.csv")

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(df["text"], df["topic"], test_size=0.2, random_state=42)

# Pipeline: TF-IDF + Classifier
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression(max_iter=1000))
])

# Train
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "topic_classifier.pkl")
