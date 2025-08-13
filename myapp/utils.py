import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set default plot style
sns.set(style="whitegrid")

def load_dataset(filepath: str) -> pd.DataFrame:
    """Loads the CSV dataset into a DataFrame."""
    return pd.read_csv(filepath, parse_dates=["timestamp"])

def sentiment_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a summary of sentiment counts per topic."""
    summary = df.groupby(['topic', 'sentiment']).size().unstack(fill_value=0)
    summary["Total"] = summary.sum(axis=1)
    return summary

def plot_sentiment_distribution(df: pd.DataFrame):
    """Visualizes sentiment distribution per topic."""
    summary = df.groupby(['topic', 'sentiment']).size().reset_index(name='count')

    plt.figure(figsize=(10, 6))
    sns.barplot(x='topic', y='count', hue='sentiment', data=summary)
    plt.title('Sentiment Distribution by Topic')
    plt.ylabel('Number of Posts')
    plt.xlabel('Topic')
    plt.legend(title='Sentiment')
    plt.tight_layout()
    plt.show()

def sentiment_over_time(df: pd.DataFrame):
    """Visualizes sentiment trends over time (monthly)."""
    df['month'] = df['timestamp'].dt.to_period('M')
    trend = df.groupby(['month', 'topic', 'sentiment']).size().reset_index(name='count')

    g = sns.FacetGrid(trend, col='topic', hue='sentiment', col_wrap=2, height=4, aspect=1.5)
    g.map_dataframe(sns.lineplot, x='month', y='count')
    g.add_legend()
    g.set_titles("{col_name}")
    g.set_axis_labels("Month", "Posts")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

import spacy

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

# Sample list of health-related keywords (customizable)
HEALTH_KEYWORDS = {"disease", "treatment", "vaccine", "virus", "pandemic", "covid", "mental health", "cancer", "depression", "diabetes"}

def extract_health_entities(text):
    doc = nlp(text)
    entities = []

    for ent in doc.ents:
        # Check if the entity label is related to health (customize as needed)
        if ent.label_ in {"DISEASE", "ORG", "PERSON", "GPE", "NORP", "PRODUCT"} or any(kw in ent.text.lower() for kw in HEALTH_KEYWORDS):
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start_char": ent.start_char,
                "end_char": ent.end_char
            })
    return entities
