from google import genai
import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

models = client.models.list()

print("Available Models:\n")
for m in models:
    print(m.name)
