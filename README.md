 🚀 AI Resume Analyzer (Flask Project)

📌 Features
- User Signup & Login (Authentication)
- Secure Password Hashing (bcrypt)
- Resume Upload (PDF)
- Extract Resume Text
- Dashboard

 🛠 Tech Stack
- Python (Flask)
- MySQL
- HTML
- PyPDF2

 ⚙️ Setup Instructions

1. Clone repository
2. Install dependencies
   pip install -r requirements.txt

3. Setup MySQL database
   Create database:
   resume_app

   Create table:
   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(100),
       email VARCHAR(100),
       password BLOB
   );

4. Run app
   python app.py

5. Open browser:
   http://127.0.0.1:5000

 📂 Folder Structure

resume_analyzer/
│
├── app.py
├── requirements.txt
├── README.md
├── uploads/
└── templates/
    ├── home.html
    ├── signup1.html
    ├── login1.html
    └── dashboard.html

💡 Future Improvements
- AI Resume Scoring
- Skill Extraction
- Learning Roadmap Generator
-Job Role Matching