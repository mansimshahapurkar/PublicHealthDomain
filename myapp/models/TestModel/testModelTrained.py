import joblib

# Load the saved model
model = joblib.load("topic_classifier.pkl")

# Sample texts to test
test_texts = [
    "The local hospital introduced new mental health services.",
    "Google and Microsoft are collaborating on a new AI platform.",
    "WHO released new guidelines to fight malaria.",
    "The UN warns of catastrophic climate impacts from carbon emissions.",
    "5G towers are the real cause of people's sickness."
]

# Predict topics
predictions = model.predict(test_texts)

# Show results
for text, topic in zip(test_texts, predictions):
    print(f"Text: {text}\nPredicted Topic: {topic}\n{'-'*60}")
