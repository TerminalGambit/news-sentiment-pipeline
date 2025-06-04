"""
FinBERT playground web application.
"""

from flask import Flask, jsonify, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Load FinBERT pipeline once at startup
finbert = pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    probs = None
    text = ""
    if request.method == "POST":
        text = request.form.get("text", "")
        if text.strip():
            # Get all class probabilities
            outputs = finbert(text, return_all_scores=True)[0]
            result = max(outputs, key=lambda x: x["score"])
            probs = {o["label"]: o["score"] for o in outputs}
    return render_template(
        "finbert_playground.html",
        result=result,
        probs=probs,
        text=text,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
