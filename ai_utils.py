from google import genai
import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

MODEL = "models/gemini-flash-latest"


def get_ai_summary(text):
    try:
        prompt = f"Summarize the following text in concise sentences:\n\n{text[:4000]}"

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text

    except Exception as e:
        print("Error fetching summary:", e)
        return "Error: Could not generate summary."


def analyze_sentiment(text_summary):
    try:
        prompt = (
            "Analyze the sentiment of this text. "
            "Return ONLY one word: Positive, Negative, or Neutral.\n\n"
            f"{text_summary}"
        )

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:
        print("Error fetching sentiment:", e)
        return "Neutral"

def extract_keywords(text):
    """
    Extracts 5 important keywords using Gemini.
    Returns a clean Python list.
    """
    try:
        prompt = (
            "Extract the 5 most important keywords or entities from this text. "
            "Return ONLY a comma-separated list. "
            "Example: Finance, Growth, Q3 Report\n\n"
            f"Text:\n{text[:4000]}"
        )

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        clean = response.text.strip()

        keywords = [k.strip() for k in clean.split(",") if k.strip()]

        return keywords

    except Exception as e:
        print(f"Error fetching keywords: {e}")
        return []