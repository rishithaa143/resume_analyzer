from flask import Flask, request, render_template, redirect, session
import mysql.connector
import bcrypt
import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader

app = Flask(__name__)
app.secret_key = "secret123"


UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rishi2006",
    database="resume_app"
)
cursor = conn.cursor()



@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return render_template("home.html")


@app.route("/signup1", methods=["GET", "POST"])
def signup1():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if username == "" or email == "" or password == "":
            return "Fields should not be empty "

        if len(password) < 6:
            return "Password too short "

        # check existing email
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            return "Email already exists "

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_password)
        )
        conn.commit()

        return redirect("/login1")

    return render_template("signup1.html")

@app.route("/login1", methods=["GET", "POST"])
def login1():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        result = cursor.fetchone()

        if result:
            stored_password = result[3]

            if bcrypt.checkpw(password.encode(), stored_password):
                session["user"] = username
                return redirect("/dashboard")
            else:
                return "Wrong password "
        else:
            return "User not found "

    return render_template("login1.html")


@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html")
    return redirect("/login1")

@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/login1")

@app.route("/upload", methods=["POST","GET"])
def upload():
    if "user" not in session:
        return redirect("/login1")

    file = request.files["resume"]

    if file.filename == "":
        return "No file selected "

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(filepath)

    reader = PdfReader(filepath)
    text = ""

    for page in reader.pages:
       text += page.extract_text()

    skills = extract_skills(text)
    score = calculate_score(skills)
    session["skills"] = skills
    session["score"] = score
 
    return redirect("/results")

@app.route("/results")
def results():
    if "user" not in session:
        return redirect("/login1")

    skills = session.get("skills", [])
    score = session.get("score", 0)

    return render_template("results.html", skills=skills, score=score)


def extract_skills(text):
    skills_list = ["python", "java", "sql", "html", "css", "javascript", "flask", "mysql"]

    found_skills = []

    text = text.lower()

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return found_skills
def calculate_score(skills):
    total_skills = 8
    score = (len(skills) / total_skills) * 100
    return round(score)



if __name__ == "__main__":
    app.run(debug=True)