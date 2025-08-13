import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

nlp = spacy.load("en_core_web_sm")
vader = SentimentIntensityAnalyzer()

MISINFORMATION_CLAIMS = [
    "drinking hot water cures covid-19",
    "vaccines cause autism",
    "climate change is a hoax",
    "masks don't work"
]

def extract_health_entities(text):
    doc = nlp(text)
    return [
        {"text": ent.text, "label": ent.label_}
        for ent in doc.ents
        if ent.label_ in {"DISEASE", "ORG", "GPE", "NORP", "PRODUCT"}
    ]

def detect_misinformation(text):
    lower = text.lower()
    return any(claim in lower for claim in MISINFORMATION_CLAIMS)

def analyze_sentiment(text):
    score = vader.polarity_scores(text)
    compound = score['compound']
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# # Sample texts
# sample_posts = [
#     # Misinformation
#     "Drinking hot water cures COVID-19. Try it!",
#     "Some still believe that vaccines cause autism.",
#     "Masks don't work. Stop falling for the scam.",
#     "Climate change is a hoax. Just a way to control us.",

#     # Health - Positive
#     "Doctors at WHO are doing an amazing job!",
#     "New AI-based diagnostic tool launched by Mayo Clinic.",
#     "Finally, free cancer screenings in Lagos this week.",
#     "Health services in rural India are improving rapidly.",
#     "Telemedicine in Australia has reduced wait times.",

#     # Health - Negative
#     "Poor hospital conditions in Delhi worsen patient outcomes.",
#     "Shortage of insulin in some parts of Cairo.",
#     "Mental health crisis is growing worldwide.",
#     "Hospitals in UK are overwhelmed again.",
#     "No ICU beds left in São Paulo!",

#     # Health - Neutral
#     "Attended a mental health workshop in Paris.",
#     "Annual vaccination campaign begins in Germany.",
#     "National Health Report released by CDC.",
#     "Health awareness week starts next Monday.",
#     "Visited a new clinic in Lagos. Impressed.",

#     # Disease - Mixed
#     "COVID-19 cases are rising again in Tokyo.",
#     "Malaria vaccine shows 70% success in trials.",
#     "Outbreak of measles in parts of Nigeria.",
#     "Research on HIV cure is making progress.",
#     "Latest flu strain identified in Canada.",

#     # Pollution - Mixed
#     "AQI in New Delhi crosses 300. Dangerous!",
#     "Smog has reduced visibility in Moscow.",
#     "New clean energy law passed in Berlin.",
#     "Lagos launches anti-pollution awareness drive.",
#     "Pollution alert issued for Cairo tomorrow.",

#     # Climate Change - Mixed
#     "Record heatwave in UK due to climate change.",
#     "New York introduces carbon-neutral building mandate.",
#     "Rising sea levels threaten Venice.",
#     "Youth rallies in Brazil for climate justice.",
#     "UN climate summit to be held in Tokyo.",

#     # More Misinformation
#     "5G towers are the real cause of COVID!",
#     "Vitamin C alone can prevent all diseases!",
#     "Flu shots make you sicker. Don’t take them.",
#     "Bill Gates wants to microchip people through vaccines.",
#     "Eating garlic can kill the coronavirus. Totally proven!",

#     # More Health/Disease - Positive
#     "Harvard Medical School develops new cancer therapy.",
#     "Free COVID testing centers open in NYC.",
#     "Mental health apps are helping millions globally.",
#     "Researchers in Japan develop universal flu vaccine.",
#     "Community clinics in Nigeria offering 24/7 care."
# ]

# # Generate dataset
# records = []

# for i, text in enumerate(sample_posts):
#     topic = "Misinformation" if detect_misinformation(text) else (
#         "Health" if "clinic" in text.lower() or "hospital" in text.lower() or "mental" in text.lower() else
#         "Disease" if "covid" in text.lower() or "flu" in text.lower() or "vaccine" in text.lower() or "malaria" in text.lower() else
#         "Pollution" if "smog" in text.lower() or "aqi" in text.lower() or "pollution" in text.lower() else
#         "Climate Change" if "climate" in text.lower() or "heatwave" in text.lower() or "carbon" in text.lower() else
#         "General"
#     )
#     sentiment = analyze_sentiment(text)
#     misinformation = detect_misinformation(text)
#     entities = extract_health_entities(text)

#     records.append({
#         "post_id": i + 1,
#         "text": text,
#         "topic": topic,
#         "sentiment": sentiment,
#         "misinformation": misinformation,
#         "entities": entities
#     })

# df = pd.DataFrame(records)
# print(df.head(10))  # Show top 10 rows

# # Optional: Save to CSV
# df.to_csv("sample_50_health_social_posts.csv", index=False)
# print("✅ Dataset with 50 posts saved.")
