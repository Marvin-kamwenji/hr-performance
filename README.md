# 🍑 Peach HR - Human Resources Management System

**Peach HR** is a Django-based Human Resources application designed to streamline employee performance evaluation and benefits administration. It supports self-assessments, 360-degree feedback, and employee benefits management like health plans and wellness programs.

---

## 🚀 Features

### 🧑‍💼 Performance Evaluation Tool
- Manager-led performance reviews
- Self-assessments for employees
- 360-degree feedback support
- Goal setting and progress tracking

### 🩺 Benefits Administration
- Manage health insurance, retirement plans, wellness programs
- Employee enrollment portal
- HR admin tools to track and update benefit plans

---

## 🛠️ Tech Stack

- **Backend**: Django 5+
- **Database**: SQLite (dev), PostgreSQL (production recommended)
- **Authentication**: Django auth
- **Admin Interface**: Django Admin
- **API**: Django REST Framework *(optional based on your implementation)*

---

## 📦 Installation

### 🔧 Prerequisites

- Python 3.10+
- pip
- virtualenv (recommended)
- Git

### 🔌 Setup Instructions

```bash
# Clone the repo
git clone https://github.com/yourusername/peach-hr.git
cd peach-hr

# Create virtual environment
python -m venv venv
source venv/bin/activate  # on Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
