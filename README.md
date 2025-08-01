# 📄 Resume Extractor & Job Application Portal

---

An AI-powered web application built with **Streamlit** that:
✅ Extracts information from uploaded resumes (PDF, DOCX, Image) using **Gemini API**
✅ Allows **user sign-up and login** with SQLite database
✅ Displays a list of available jobs and lets users **apply for jobs**
✅ Tracks **applied jobs** and shows "Applied" status persistently
✅ Has an **auto-seeding feature** to add sample jobs to the database

---

## 🚀 Features

* **User Authentication**: Sign-up and login system using SQLite.
* **Resume Parsing**: Extracts:

  * First Name
  * Last Name
  * Education (Degree, Institution, Year)
  * Experience (Role, Company, Duration)
* **AI-Powered Extraction**: Uses **Gemini API** for accurate information extraction.
* **Job Portal**: Lists available jobs with "Apply" buttons.

---

## 🛠 Tech Stack

* **Frontend & Backend**: [Streamlit](https://streamlit.io/)
* **AI Model**: Google **Gemini API**
* **Database**: SQLite (local file-based database)
* **OCR**: PyPDF2, python-docx, pytesseract
* **Language**: Python 3.x

---

## 📂 Project Structure

```
resume-extractor-job-portal/
│
├── app.py                # Main Streamlit app file
├── database.py           # SQLite database connection and functions
├── extractors.py         # Resume text extraction logic
|--- Pages
    |-- Resume Extractor.py
├── requirements.txt      # Required Python packages
├── .env                  # Environment variables (API keys)
└── README.md             # Project documentation
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/vineeth191004/Resume-Information-Extractor.git
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Run the App

```bash
streamlit run app.py
```

---

## 🛠 How It Works

### 1. Login / Signup

* New users can **sign up**.
* Existing users can **log in**.

### 2. Resume Upload

* Upload a PDF, DOCX, or Image file.
* AI extracts:

  * First Name
  * Last Name
  * Education
  * Experience

### 3. Job Application

* View available jobs.
* Click "Apply" for a job → Application saved to the database.
* "Applied" status appears instead of the button.

---

## 📊 Database Schema

### Users Table

| Column   | Type    | Description     |
| -------- | ------- | --------------- |
| id       | INTEGER | Primary Key     |
| username | TEXT    | Unique username |
| password | TEXT    | User password   |

### Jobs Table

| Column   | Type    | Description  |
| -------- | ------- | ------------ |
| id       | INTEGER | Primary Key  |
| title    | TEXT    | Job title    |
| company  | TEXT    | Company name |
| location | TEXT    | Job location |

### Applications Table

| Column      | Type    | Description              |
| ----------- | ------- | ------------------------ |
| id          | INTEGER | Primary Key              |
| user\_id    | INTEGER | Foreign key (users.id)   |
| job\_id     | INTEGER | Foreign key (jobs.id)    |
| first\_name | TEXT    | Extracted first name     |
| last\_name  | TEXT    | Extracted last name      |
| education   | TEXT    | Extracted education info |
| experience  | TEXT    | Extracted experience     |

---

## 🧾 Sample Jobs Auto-Inserted

When the database is initialized, these jobs are added:

```sql
INSERT INTO jobs (title, company, location) 
VALUES 
('Data Scientist', 'Google', 'Bangalore'),
('ML Engineer', 'Amazon', 'Hyderabad'),
('AI Researcher', 'OpenAI', 'Remote');
```

---

## 📌 Requirements

See `requirements.txt`:

```
streamlit
google-generativeai
PyPDF2
python-docx
pytesseract
pillow
python-dotenv
sqlite3 (builtin)
```

---

## 🏆 Usage

1. Start the app.
2. Sign up or log in.
3. Upload your resume.
4. View extracted details.
5. Apply for jobs.
