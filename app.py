from flask import Flask,request,render_template,redirect,session
import mysql.connector
from PyPDF2 import PdfReader
import bcrypt
import os
from werkzeug.utils import secure_filename

app=Flask(__name__)
app.secret_key="secret 123"
UPLOAD_FOLDER="uploads"
app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="rishi2006",
    database="resume_app"
)
cursor=conn.cursor()

@app.route("/")
def home():
    if "user" in session :
        return redirect("/dashboard")
    else:
        return render_template("home.html")

@app.route("/signup1",methods=["GET","POST"])
def signup1():
  if request.method=="POST":
        username=request.form["username"]
        email=request.form["email"]
        password=request.form["password"]
        hashed_password=bcrypt.hashpw(password.encode(),bcrypt.gensalt())

        if username=="" or email=="" or password=="":
           return "fields should not be empty"
        if len(password)<6:
          return "password too short"

        cursor.execute("select * from users where email=%s",(email,))
        result=cursor.fetchone()
        if result:
            return "email already exists,please login"
        query=("insert into users (username,email,password)values(%s,%s,%s)")
        cursor.execute(query,(username,email,hashed_password))
        conn.commit()
        return redirect("/login1")
  return render_template("signup1.html")

@app.route("/login1",methods=["GET","POST"])
def login1():
   if request.method=="POST":
      username=request.form["username"]
      password=request.form["password"]

      cursor.execute("select * from users where username=%s",(username,))
      result=cursor.fetchone()

      if result:
        strong_password = result[3]

        if bcrypt.checkpw(password.encode(), strong_password):
            session["user"] = username
            return redirect("/dashboard")
        else:
            return "wrong password ❌"
      else:
        return "user not found ❌"

   return render_template("login1.html")

@app.route("/dashboard",methods=["POST","GET"])
def dashboard():
          if "user" in session:
              return render_template("dashboard.html")
          else:
           return redirect("/login1")
@app.route("/upload",methods=["GET","POST"])
def upload():
    if "user" not in session:
      return redirect("/login1")
    if request.method=="POST":
        file=request.files.get("resume")
        if not file or file.filename=="":
            return "no file selected"
        filename = secure_filename(file.filename)
        filepath=os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        reader=PdfReader(filepath)
        text=""
        for page in reader.pages:
           text +=page.extract_text() or ""
        skills = extract_skills(text)
        score = calculate_score(skills)

        return render_template("result.html", skills=skills, score=score, text=text)
    return redirect("/dashboard")
@app.route("/results")
def result():
    return render_template("result.html")

def extract_skills(text):
    skills_list = ["python", "java", "sql", "html", "css", "javascript", "flask", "mysql","powerbi"]

    found_skills = []
    text = text.lower()

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return found_skills
def calculate_score(skills):
    total_skills = 9
    score = (len(skills) / total_skills) * 100
    return round(score)

@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/login1")


if __name__=="__main__":
    app.run(debug=True)