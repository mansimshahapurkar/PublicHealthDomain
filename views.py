# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.conf import settings

from django.contrib.auth import get_user_model

from django.contrib.auth.models import User
from django.contrib import messages

from .models import *
from .views import *
from .nlp_pipeline import *

import os
import pandas as pd
import spacy
import seaborn as sns
import matplotlib.pyplot as plt


# Import your NLP & Sentiment logic
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# For image output
from io import BytesIO
import base64

# Set seaborn style
sns.set(style="whitegrid")

nlp = spacy.load("en_core_web_sm")
vader = SentimentIntensityAnalyzer()

# Sample misinformation claims
MISINFORMATION_CLAIMS = [
    "drinking hot water cures covid-19",
    "vaccines cause autism",
    "climate change is a hoax",
    "masks don't work",
    "5g towers are the real cause of covid",
    "flu shots make you sicker"
]


def base(request):
    return render(request, 'base.html')


# Registration view
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Registration successful. You can now login.")
        return redirect('login')

    return render(request, 'registration/signup.html')

# Login view
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')  # Redirect superusers to Django admin
            return redirect('base')        # Redirect regular users to your landing page
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'registration/login.html')




from .models import Message

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def send_message(request):
    if request.method == 'POST':
        receiver_username = request.POST.get('receiver')
        content = request.POST.get('content')

        try:
            receiver = User.objects.get(username=receiver_username)
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
            messages.success(request, "Message sent!")
        except User.DoesNotExist:
            messages.error(request, "User does not exist")

        return redirect('inbox')

    # Exclude the current user from recipient list
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'messaging/send_message.html', {'users': users})

@login_required
def inbox(request):
    messages_received = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'messaging/inbox.html', {'messages': messages_received})

@login_required
def submit_feedback(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        Feedback.objects.create(user=request.user, message=message)
        messages.success(request, "Feedback submitted.")
        return redirect('submit_feedback')
    return render(request, 'feedback/submit_feedback.html')

# views.py
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('edit_profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'registration/edit_profile.html', {'form': form})


# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# dashboard
@login_required
def dashboard(request):
    # Load dataset
    csv_path = os.path.join(settings.BASE_DIR, 'myapp', 'models', 'synthetic_social_sentiment_data.csv')
    df = pd.read_csv(csv_path, parse_dates=['timestamp'])

    # Latest month analysis
    df['month'] = df['timestamp'].dt.to_period('M').astype(str)
    latest_month = df['month'].max()
    recent_df = df[df['month'] == latest_month]

    # Get total sentiments per topic
    topic_sentiments = recent_df.groupby(['topic', 'sentiment']).size().unstack(fill_value=0)

    # Predict trending topic = topic with highest total mentions
    topic_sentiments["Total"] = topic_sentiments.sum(axis=1)
    trending_topic = topic_sentiments["Total"].idxmax()

    # Highest negative sentiment topic
    highest_negative_topic = topic_sentiments["Negative"].idxmax()

    # Suggestion logic
    suggestions = []
    if highest_negative_topic == "Pollution":
        suggestions.append("⚠️ Increase in negative sentiment on pollution. Recommend awareness campaigns.")
    if highest_negative_topic == "Health":
        suggestions.append("🩺 Public health concern rising. Suggest emergency health services review.")
    if trending_topic == "Climate Change":
        suggestions.append("🌍 Climate change is trending. Recommend promoting eco-friendly initiatives.")
    
    # Top 3 concern locations (by negative sentiment)
    top_negative_locations = (
        recent_df[recent_df['sentiment'] == "Negative"]
        .groupby("location").size().sort_values(ascending=False).head(3).index.tolist()
    )

    return render(request, 'dashboard/dashboard.html', {
        'latest_month': latest_month,
        'trending_topic': trending_topic,
        'highest_negative_topic': highest_negative_topic,
        'suggestions': suggestions,
        'top_locations': top_negative_locations,
    })


# model

# Load dataset from 'Tmodel' directory
def load_data():
    csv_path = os.path.join(settings.BASE_DIR, 'myapp', 'models', 'synthetic_social_sentiment_data.csv')
    return pd.read_csv(csv_path, parse_dates=['timestamp'])

# Home summary view
def summary_view(request):
    df = load_data()
    summary = df.groupby(['topic', 'sentiment']).size().unstack(fill_value=0)
    summary["Total"] = summary.sum(axis=1)
    summary_dict = summary.reset_index().to_dict(orient='records')
    return render(request, 'prediction/summary.html', {'summary': summary_dict})

# Plot sentiment distribution bar chart
def plot_sentiment_distribution(df):
    summary = df.groupby(['topic', 'sentiment']).size().reset_index(name='count')
    plt.figure(figsize=(8, 6))
    sns.barplot(x='topic', y='count', hue='sentiment', data=summary)
    plt.title('Sentiment Distribution by Topic')
    plt.ylabel('Number of Posts')
    plt.xlabel('Topic')
    plt.xticks(rotation=30)
    plt.tight_layout()
    return plot_to_base64()

# Plot sentiment trend over time
def plot_sentiment_trend(df):
    df['month'] = df['timestamp'].dt.to_period('M').astype(str)
    trend = df.groupby(['month', 'topic', 'sentiment']).size().reset_index(name='count')
    g = sns.FacetGrid(trend, col='topic', hue='sentiment', col_wrap=2, height=4, aspect=1.4, sharey=False)
    g.map(sns.lineplot, 'month', 'count')
    g.add_legend()
    g.set_titles("{col_name}")
    g.set_xticklabels(rotation=45)
    plt.tight_layout()
    return plot_to_base64()

# Utility: convert current matplotlib figure to base64
def plot_to_base64():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')
    plt.close()
    return graphic

# Render sentiment distribution chart
def sentiment_distribution_view(request):
    df = load_data()
    chart = plot_sentiment_distribution(df)
    return render(request, 'prediction/chart.html', {'chart': chart, 'title': 'Sentiment Distribution'})

# Render sentiment trend chart
def sentiment_trend_view(request):
    df = load_data()
    chart = plot_sentiment_trend(df)
    return render(request, 'prediction/chart.html', {'chart': chart, 'title': 'Sentiment Trend Over Time'})

def health_terms_view(request):
    df = load_data()

    # Let's assume we analyze a specific topic (e.g., health-related social media posts)
    health_related_posts = df[df['topic'].str.contains("health", case=False, na=False)]
    
    ner_results = []

    for _, row in health_related_posts.iterrows():
        text = row['content']  # assuming the column with text data is named 'content'
        entities = extract_health_entities(text)
        ner_results.append({
            "text": text,
            "entities": entities
        })

    return render(request, 'prediction/health_terms.html', {'results': ner_results})

# Load CSV
def load_data_main():
    csv_path = os.path.join(settings.BASE_DIR, 'myapp', 'models', 'sample_health_social_posts.csv')
    return pd.read_csv(csv_path)

# NER extraction
def extract_health_entities(text):
    doc = nlp(text)
    return [
        {"text": ent.text, "label": ent.label_}
        for ent in doc.ents
        if ent.label_ in {"DISEASE", "ORG", "GPE", "NORP", "PRODUCT"}
    ]

# Misinformation detection
def detect_misinformation(text):
    lower = text.lower()
    return any(claim in lower for claim in MISINFORMATION_CLAIMS)

# Sentiment analysis
def analyze_sentiment(text):
    score = vader.polarity_scores(text)
    compound = score['compound']
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Main dashboard view
def health_insight_dashboard(request):
    df = load_data_main()

    insights = []

    # Filter relevant rows
    health_df = df[df['topic'].str.contains("health|disease|misinformation", case=False, na=False)]

    for _, row in health_df.iterrows():
        text = row['text']
        topic = row.get('topic', 'Unknown')

        insights.append({
            "text": text,
            "topic": topic,
            "sentiment": analyze_sentiment(text),
            "misinformation": detect_misinformation(text),
            "entities": extract_health_entities(text)
        })

    # Summary statistics
    total = len(insights)
    misinfo_count = sum(1 for i in insights if i['misinformation'])
    sentiment_counts = {
        "Positive": sum(1 for i in insights if i['sentiment'] == "Positive"),
        "Negative": sum(1 for i in insights if i['sentiment'] == "Negative"),
        "Neutral": sum(1 for i in insights if i['sentiment'] == "Neutral"),
    }

    return render(request, 'prediction/health_dashboard.html', {
        "insights": insights,
        "total": total,
        "misinfo_count": misinfo_count,
        "sentiment_counts": sentiment_counts
    })

# 
from django.shortcuts import render
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import spacy

nlp = spacy.load("en_core_web_sm")
vader = SentimentIntensityAnalyzer()

MISINFORMATION_CLAIMS = [
    "drinking hot water cures covid-19",
    "vaccines cause autism",
    "climate change is a hoax",
    "masks don't work",
    "5g towers are the real cause of covid",
    "vitamin c alone can prevent all diseases",
    "flu shots make you sicker",
    "bill gates wants to microchip people through vaccines",
    "eating garlic can kill the coronavirus"
]

# Boost positive sentiment when key phrases are detected
POSITIVE_PHRASES = [
    "breakthrough", "significantly improves", "new therapy",
    "increases survival rate", "promising results", "positive outcome",
    "successful treatment", "life-saving", "hopeful development"
]

def extract_health_entities_t(text):
    doc = nlp(text)
    return [
        {"text": ent.text, "label": ent.label_}
        for ent in doc.ents
    ]

def detect_misinformation_t(text):
    lower = text.lower()
    return any(claim in lower for claim in MISINFORMATION_CLAIMS)

def analyze_sentiment_t(text):
    score = vader.polarity_scores(text)
    # Boost sentiment score if any positive phrases are present
    if any(phrase in text.lower() for phrase in POSITIVE_PHRASES):
        score['compound'] += 0.3
    compound = score['compound']
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def classify_topic(text):
    lower = text.lower()
    if detect_misinformation_t(text):
        return "Misinformation"
    elif any(word in lower for word in ["clinic", "hospital", "mental", "therapy"]):
        return "Health"
    elif any(word in lower for word in ["covid", "flu", "vaccine", "malaria", "cancer", "survival", "new therapy"]):
        return "Disease"
    elif any(word in lower for word in ["smog", "aqi", "pollution"]):
        return "Pollution"
    elif any(word in lower for word in ["climate", "heatwave", "carbon"]):
        return "Climate Change"
    else:
        return "General"

def classify_text(request):
    result = {}
    if request.method == "POST":
        input_text = request.POST.get("text")

        result["input_text"] = input_text
        result["sentiment"] = analyze_sentiment_t(input_text)
        result["misinformation"] = detect_misinformation_t(input_text)
        result["entities"] = extract_health_entities_t(input_text)
        result["topic"] = classify_topic(input_text)

    return render(request, "classify/classify.html", result)
