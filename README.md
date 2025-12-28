# Job Portal

A fully functional **Job Portal** web application built using **Python Django** and **Bootstrap**. This platform allows users to search and filter jobs by category, view job details, and apply for positions. It also includes user authentication and API support for developers.  

---

## Features

- **Job Listings:** Browse available jobs with detailed descriptions.
- **Search & Filter:** Search jobs and filter them by category (e.g., Education, IT, Sales, Communication).
- **Apply for Jobs:** Users can view and apply for job openings.
- **User Authentication:** Login and registration system for applicants.
- **Responsive Design:** Fully responsive UI built using **Bootstrap**.
- **API Support:** RESTful API endpoints for accessing job listings programmatically.

---

## Technologies Used

- **Backend:** Python Django  
- **Frontend:** HTML, CSS, Bootstrap  
- **Database:** SQLite (default Django database)  
- **Others:** Django REST Framework (for API), Django templating, static files handling  

---

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Job-Portal.git
cd Job-Portal

2. **Create and activate a virtual environment**

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

3. **Install dependencies**

pip install -r requirements.txt

4. **Apply migrations**

python manage.py migrate

5.** Run the server**

python manage.py runserver

6. Open your browser and go to http://127.0.0.1:8000/ to see the application.
