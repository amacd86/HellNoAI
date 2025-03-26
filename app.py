from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
import os

print("Starting Flask app...")

load_dotenv()
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_analysis_and_roast(text, mode):
    if mode == "detect-only":
        instruction = "Only detect and report whether the text seems AI-generated. Do not include a roast."
    elif mode == "nice":
        instruction = "Gently roast this text with kindness. Be funny and clever, but constructive — like a cool teacher."
    else:  # savage
        instruction = "Roast this content with sharp wit, sarcasm, and a little dramatic flair. Be bold, but don't be mean-spirited."

    prompt = f"""
You are an AI content detector and creative writing coach.

1. First, analyze whether this content sounds AI-generated or human.
2. Check the tone: corporate buzzwords, robotic phrasing, or casual and real?
3. Based on the selected mode, respond accordingly.

---
**Mode:** {mode}
**Instruction:** {instruction}

Now process this:

\"\"\"{text}\"\"\"

Respond in this format:
---
**AI Detection:** [Likely AI / Likely Human / Unclear]
**Tone Check:** [Your tone check here]
**Roast:** [Only if mode includes it]
---
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=1.0 if mode == "savage" else 0.8
    )

    return response.choices[0].message.content.strip()

@app.route("/", methods=["GET", "POST"])
def index():
    roast = ""
    if request.method == "POST":
        content = request.form["content"].strip()
        mode = request.form.get("mode", "savage")
        if content:
            roast = get_ai_analysis_and_roast(content, mode)
    return render_template("index.html", roast=roast)

if __name__ == "__main__":
    app.run(debug=True)
