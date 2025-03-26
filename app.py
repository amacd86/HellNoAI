from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
import os

print("Starting Flask app...")

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client with secure API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_analysis_and_roast(text):
    prompt = f"""
You are a brutally honest but insightful writing coach and content analyst.

You will:
1. Analyze the text for signs of AI-generated patterns (buzzwords, vague language, repetitive structure).
2. Judge the overall *vibe*: Is it robotic, overly formal, try-hard, or awkwardly human?
3. Deliver a roast that’s funny, sharp, and a little dramatic — but feels like it came from a clever human, not a chatbot.
4. Format your answer exactly like this:

---
**AI Detection:** [Likely AI / Likely Human / Unclear]
**Tone Check:** [Boring corporate / Overly formal / Weirdly robotic / Kinda human / Try-hard / Casual and real]
**Roast:** [Insert a witty, honest, slightly savage roast. No softballs.]
---

Now roast this content:

\"\"\"{text}\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=1.1
    )

    return response.choices[0].message.content.strip()

@app.route("/", methods=["GET", "POST"])
def index():
    roast = ""
    if request.method == "POST":
        content = request.form["content"].strip()  # Remove leading/trailing spaces
        if content:  # Only call OpenAI if there's actual content
            roast = get_ai_analysis_and_roast(content)
    return render_template("index.html", roast=roast)


if __name__ == "__main__":
    app.run(debug=True)
