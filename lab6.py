from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "patriotism-secret"
quotes = [
    "Swaraj is my birthright and I shall have it. – Bal Gangadhar Tilak",
    "Tum mujhe khoon do, main tumhe azadi dunga. – Subhas Chandra Bose",
    "The best way to find yourself is to lose yourself in the service of others. – Mahatma Gandhi",
    "Inquilab Zindabad! – Bhagat Singh",
    "Freedom is not worth having if it does not include the freedom to make mistakes. – Mahatma Gandhi",
    "Jai Hind! – Subhas Chandra Bose"
]
quiz_data = [
    {
        "quote": "Swaraj is my birthright and I shall have it.",
        "options": ["Mahatma Gandhi", "Bal Gangadhar Tilak", "Bhagat Singh", "Lala Lajpat Rai"],
        "answer": "Bal Gangadhar Tilak"
    },
    {
        "quote": "Give me blood and I will give you freedom.",
        "options": ["Subhas Chandra Bose", "Bhagat Singh", "Rani Lakshmibai", "Jawaharlal Nehru"],
        "answer": "Subhas Chandra Bose"
    },
    {
        "quote": "Inquilab Zindabad!",
        "options": ["Sardar Patel", "Bal Gangadhar Tilak", "Bhagat Singh", "Lal Bahadur Shastri"],
        "answer": "Bhagat Singh"
    },
    {
        "quote": "The weak can never forgive. Forgiveness is the attribute of the strong.",
        "options": ["Jawaharlal Nehru", "Mahatma Gandhi", "B. R. Ambedkar", "Subhas Chandra Bose"],
        "answer": "Mahatma Gandhi"
    },
    {
        "quote": "Jai Jawan Jai Kisan.",
        "options": ["Indira Gandhi", "Lal Bahadur Shastri", "Rajendra Prasad", "Bhagat Singh"],
        "answer": "Lal Bahadur Shastri"
    },
    {
        "quote": "You must be the change you wish to see in the world.",
        "options": ["Mahatma Gandhi", "B. R. Ambedkar", "Sardar Patel", "Rajendra Prasad"],
        "answer": "Mahatma Gandhi"
    }
]

@app.route("/")
def home():
    random_quote = random.choice(quotes)
    return render_template("home.html", quote=random_quote)

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "score" not in session:
        session["score"] = 0
        session["q_index"] = 0
        random.shuffle(quiz_data)

    if request.method == "POST":
        selected = request.form.get("option")
        correct = quiz_data[session["q_index"]]["answer"]
        if selected == correct:
            session["score"] += 1
        session["q_index"] += 1

        if session["q_index"] >= len(quiz_data):
            final_score = session["score"]
            session.clear()
            return render_template("result.html", score=final_score, total=len(quiz_data))

    question = quiz_data[session["q_index"]]
    return render_template("quiz.html", question=question, qnum=session["q_index"]+1, total=len(quiz_data))

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)