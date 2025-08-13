import random
import pandas as pd
from faker import Faker

# Initialize Faker
fake = Faker()

# Define topics, sentiments, and sample locations
topics = ["Health", "Pollution", "Climate Change", "Disease", "Misinformation"]
sentiments = ["Positive", "Negative", "Neutral"]
locations = [
    "New York, USA", "Delhi, India", "London, UK", "Tokyo, Japan",
    "Lagos, Nigeria", "São Paulo, Brazil", "Cairo, Egypt", "Sydney, Australia",
    "Toronto, Canada", "Berlin, Germany", "Moscow, Russia", "Paris, France"
]

# Function to generate a large pool of varied phrases
def generate_phrases(base_list, count=10000):
    phrases = []
    for i in range(count):
        base = random.choice(base_list)
        suffix = fake.sentence(nb_words=5)
        phrases.append(f"{base}. {suffix}")
        if len(phrases) >= count:
            break
    return phrases

# Define base phrases for each topic/sentiment
base_phrases = {
    "Health": {
        "Positive": [
            "Vaccination drives are working well",
            "Health services are improving",
            "Doctors are doing great",
            "More people have access to healthcare",
            "Telemedicine is helping rural areas"
        ],
        "Negative": [
            "Hospitals are overwhelmed",
            "Medical help is hard to find",
            "Poor healthcare access",
            "Shortage of essential medicines",
            "Emergency services are delayed"
        ],
        "Neutral": [
            "Visited the clinic today",
            "Waiting time was average",
            "Received check-up",
            "Annual health report released",
            "Discussing mental health awareness"
        ]
    },
    "Pollution": {
        "Positive": [
            "Air quality improved",
            "Pollution levels dropped",
            "Cleaner air lately",
            "New clean energy project launched",
            "City enforces pollution control"
        ],
        "Negative": [
            "Smog everywhere",
            "Pollution causing breathing issues",
            "Toxic air in the city",
            "Water bodies are polluted",
            "Factory emissions worsening air"
        ],
        "Neutral": [
            "AQI levels unchanged",
            "Wearing mask outside",
            "Weather is hazy",
            "Environment report published",
            "Air quality monitoring ongoing"
        ]
    },
    "Climate Change": {
        "Positive": [
            "Great climate action plans",
            "Climate change awareness rising",
            "Green initiatives growing",
            "Youth rallies for climate",
            "Carbon emissions dropping"
        ],
        "Negative": [
            "Frequent floods",
            "Heatwaves are worsening",
            "Melting glaciers faster",
            "Climate change denial increasing",
            "Wildfires devastate forests"
        ],
        "Neutral": [
            "Discussing climate policy",
            "Reports on global warming",
            "Scientists studying sea levels",
            "UN holds climate summit",
            "Debate on carbon taxes"
        ]
    },
    "Disease": {
        "Positive": [
            "Breakthrough in cancer research",
            "New vaccines showing great promise",
            "Progress in HIV treatment",
            "Malaria eradication efforts succeed",
            "Advances in mental health treatment"
        ],
        "Negative": [
            "COVID-19 cases on the rise again",
            "Hospitals overwhelmed with flu patients",
            "Malaria spreading rapidly in certain regions",
            "Outbreak of new viral disease reported",
            "More people suffering from mental health issues"
        ],
        "Neutral": [
            "Research on disease prevention ongoing",
            "Latest flu season statistics released",
            "New disease cases reported in the region",
            "Discussing healthcare policies for disease control",
            "Meeting on improving disease surveillance systems"
        ]
    },
    "Misinformation": {
        "Positive": [
            "Vaccines are safe and proven effective",
            "Climate change is backed by scientific consensus",
            "Masks help reduce COVID-19 spread",
            "Global warming is a real and pressing issue",
            "Studies confirm water fluoridation is beneficial"
        ],
        "Negative": [
            "COVID-19 is just a common cold",
            "Vaccines cause autism, don't trust them",
            "Climate change is a hoax created by governments",
            "Masks don't work, stop wearing them",
            "Big Pharma is hiding the truth about diseases"
        ],
        "Neutral": [
            "There's a lot of confusion around vaccines",
            "People are still debating the facts about climate change",
            "Some still question the efficacy of masks",
            "Misinformation about the virus is spreading",
            "Scientific studies continue to contradict each other"
        ]
    }
}

# Generate 10,000+ synthetic phrases per category
phrase_dict = {}
for topic in topics:
    phrase_dict[topic] = {}
    for sentiment in sentiments:
        base_list = base_phrases[topic][sentiment]
        phrase_dict[topic][sentiment] = generate_phrases(base_list, 10000)

# Create 200,000 social media posts
num_records = 200000
data = []

for i in range(num_records):
    topic = random.choice(topics)
    sentiment = random.choice(sentiments)
    location = random.choice(locations)
    text = random.choice(phrase_dict[topic][sentiment])
    timestamp = fake.date_time_between(start_date='-2y', end_date='now')

    data.append({
        "post_id": i + 1,
        "text": text,
        "topic": topic,
        "sentiment": sentiment,
        "location": location,
        "timestamp": timestamp
    })

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
csv_filename = "synthetic_social_sentiment_data_with_diseases_and_misinformation.csv"
df.to_csv(csv_filename, index=False)
print(f"✅ Dataset saved as {csv_filename} with {len(df)} rows.")
