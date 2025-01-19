# -*- coding: utf-8 -*-
import requests
import pandas as pd
from transformers import pipeline
import csv

# Create your own GitHub Token key here
GITHUB_TOKEN = 'your_token_here'
GITHUB_API_URL = "https://api.github.com/search/users?q="

# Initialize Hugging Face model for zero-shot classification
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Valid categories
VALID_CATEGORIES = ['Collaboration', 'Quality Assurance', 'Marketing', 'Development']

def fetch_github_data(category):
    """
    Fetch GitHub user data matching the category using GitHub API.
    """
    if category not in VALID_CATEGORIES:
        raise ValueError(f"Invalid category. Choose from {VALID_CATEGORIES}")

    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    url = f"{GITHUB_API_URL}{category} in:bio"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        leads = []
        for user in data.get("items", []):
            leads.append({"name": user['login'], "bio": user.get('bio', 'No bio available')})
        return leads
    else:
        raise Exception(f"Failed to fetch GitHub data: {response.json()}")

def process_leads(leads, category):
    """
    Rank leads based on relevance to the category using AI.
    """
    ranked_leads = []
    for lead in leads:
        bio = lead["bio"]
        result = classifier(bio, candidate_labels=[category])
        score = result["scores"][0]
        ranked_leads.append({"name": lead["name"], "bio": bio, "score": score})
    ranked_leads.sort(key=lambda x: x["score"], reverse=True)
    return ranked_leads

def save_to_csv(leads, filename):
    """
    Save the ranked leads to a CSV file.
    """
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "bio", "score"])
        writer.writeheader()
        writer.writerows(leads)

def generate_csv(category, output_file="leads.csv"):
    """
    Generate a CSV file containing ranked leads from GitHub data.
    """
    if category not in VALID_CATEGORIES:
        raise ValueError(f"Invalid category. Choose from {VALID_CATEGORIES}")

    print("Fetching GitHub data...")
    github_leads = fetch_github_data(category)

    print("Processing leads...")
    ranked_leads = process_leads(github_leads, category)

    print(f"Saving results to {output_file}...")
    save_to_csv(ranked_leads, output_file)

    print("CSV generation complete.")
