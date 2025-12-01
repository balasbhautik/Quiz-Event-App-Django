# 📘 Django Quiz & Events Application

A full-featured web application built using **Django**, **Django REST Framework**, and **TailwindCSS**, enabling users to browse quizzes, submit answers, view results, and check upcoming events. Includes full authentication, submission tracking, result evaluation, and a clean UI.

## 🚀 Features

### 🔐 User Features
- User Registration & Login  
- Profile Update  
- Change Password  
- View Profile Details  
- JWT Authentication for APIs  

### 🧠 Quiz Features
- List all available quizzes  
- Dynamic questions (MCQ, True/False, Text)  
- Automatic scoring system  
- Stores user answers and submission history  
- Detailed result page with correct answers  

### 🎉 Event Features
- List all upcoming events  
- Event detail page  
- Includes title, description, date, and location  

### 🎨 UI/Frontend
- TailwindCSS-based modern UI  
- Clean and mobile-responsive templates  

## 🛠 Technology Stack

| Component | Technology |
|----------|------------|
| Backend | Django |
| API | Django REST Framework |
| Frontend | Django Templates + TailwindCSS |
| Authentication | JWT + Session Auth |
| DB | SQLite |
| Language | Python 3.x |

## 📂 Project Structure

```
project/
│── manage.py
│── README.md
│── requirements.txt
│── quiz/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── templates/quiz/
│── events/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/events/
│── user_accounts/
│   ├── views.py
│   ├── serializers.py
│   ├── authentication/
│── templates/
│── static/
```

## 🗃 Database Schema

### **Quiz Module**
- Quiz → (title, description, created_at, updated_at)
- Question → (quiz_id, text, question_type)
- Answer → (question_id, text, is_correct)
- UserSubmission → (quiz_id, user_id, score, submitted_at)
- UserAnswer → (submission_id, question_id, answer, is_correct)

### **Event Module**
- Event → (title, description, date, location)

## 🔄 Quiz Flow Explanation

1. View quizzes  
2. Select a quiz  
3. Attempt questions  
4. Submit answers  
5. System evaluates  
6. Score saved  
7. Results displayed  
8. Submission history stored  

## ▶️ Setup and Installation

### Step 1: Clone the Git Repository  
```sh
git clone https://github.com/<your-username>/Quiz-Event-App-Django.git
cd Quiz-Event-App-Django
```

### Step 2: Virtual environment
```sh
python -m venv env
source env/bin/activate
```

### Step 2: Install dependencies
```sh
pip install -r requirements.txt
```

### Step 4: Migrate database
```sh
python manage.py migrate
```

### Step 4: Migrate database
```sh
python manage.py migrate
```

### Step 5: Run server
```sh
python manage.py runserver
```

## 🔐 JWT Authentication

### Generate Token  
POST `/api/login/`

## 📝 Documentation  
PDF included: *Django_Quiz_Events_Documentation.pdf*

## 🤝 Contributing  
Pull requests welcome.

## 📜 License  
For educational and interview purposes.
