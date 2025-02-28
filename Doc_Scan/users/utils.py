from openai import OpenAI
import numpy as np
import json
from django.conf import settings

def get_openai_similarity(text1, text2):
    prompt = (
        f"Analyze the similarity between these two texts and provide:\n"
        f"1. A similarity percentage score (0-100%).\n"
        f"2. A short, one-line common content or similarity between them.\n\n"
        f"Text 1: {text1[:1000]}\n"
        f"Text 2: {text2[:1000]}\n\n"
        f"Response format (JSON): {{\"similarity_score\": <score>, \"similar_content\": \"<content>\"}}"
    )

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You analyze text similarity and extract key common content."},
            {"role": "user", "content": prompt}
        ]
    )

    response = completion.choices[0].message.content.strip()

    try:
        result = json.loads(response)  # Use JSON instead of eval for safety
        return result.get("similarity_score", 0), result.get("similar_content", "No similar content found.")
    except json.JSONDecodeError:
        return 0, "Error processing similarity result."
