# 🙏 Chaldean Catholic Prayer Web App

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

A responsive web application built using Django and HTML to provide Chaldean Catholic prayers and liturgical content online.
This project is dedicated to preserving and sharing the traditional prayers of the Chaldean Catholic Church.

---

## ✨ Features

- 🕊️ Browse a curated list of Chaldean prayers
- 🔎 Filter prayers by category (e.g., Morning, Evening, Mass)
- 📖 Responsive HTML layout (Bootstrap or custom CSS)
- 🔐 Admin panel for adding/editing prayers (Django admin)
- 👤 Optional user authentication (login/register)

---

## 🧰 Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3, Bootstrap (or Tailwind)
- **Database**: SQLite (development) / PostgreSQL (production-ready)
- **Hosting**: Localhost, PythonAnywhere, or Render (optional)

---

## 🚀 Getting Started

### ✅ Prerequisites

Ensure you have the following installed:

- [Python 3.8+](https://www.python.org/)
- [pip](https://pip.pypa.io/en/stable/)
- [Git](https://git-scm.com/)

---

### 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AustinAbro1/ChaldeanCatholicPrayerWeb.git
   cd ChaldeanCatholicPrayerWeb

2. **Setup a Virtual Env**
   python -m venv venv
   source venv/bin/activate       # On Windows: venv\Scripts\activate

3. **Install Dependencies**
   pip install -r requirements.txt

4. **Run Migrations**
   python manage.py migrate

5. **Start the Server**
   python manage.py runserver

# Important Credits and Other Notes
For this project, I utilized a YouTube video tutorial (link: Python Django 7 Hour Course), on Traversy Media conducted by Dennis Ivy.
I also utilized the designs that he used in the tutorial, while the formatting is not all the same, 
I did use the design style as you can see if you compare both applications, the one I made and the one shown in the tutorial, 
there are slight differences but overall I pulled his theme from his designer from this GitHub repository: StudyBud/theme at master · Traversy-Media/StudyBud · GitHub
I also utilized AI tools to help with adjusting these designs and formatting as well, also with the color scheme I decided to go with. 
I also utilized AI tools to find why my website at times may be throwing errors, to find things such as misspellings or other mistakes I made. 
I also utilized it to help with making this Software Design Specification Document.
Used Data for Chaldean Prayers from: Our Prayers - Chaldean Diocese of St. Thomas the Apostle U.S.A
