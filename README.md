# Process-Monitoring-Agent-with-Django-Backend-Project
A real-time process monitoring agent with a Django backend and Python agent. Displays system processes in a live, tree-structured UI with CPU &amp; memory usage. Built for professional system monitoring and task management.

📄 README.md
# 🖥️ Process Monitoring Agent (Django + Python)

A powerful and simple **process monitoring web application** built with Django and Python. This project allows you to track and display real-time process trees from multiple machines using a background agent and a web-based frontend.

---

## 📌 Features

✅ Real-time system process monitoring  
✅ Tree-structured view of all running processes  
✅ CPU and memory usage of each process  
✅ Host-wise filtering and search  
✅ Lightweight agent (Python script) for Windows  
✅ REST API powered by Django + DRF  
✅ Modern responsive frontend using plain HTML/CSS/JS

---

## 🧠 Architecture Overview

```
[Agent Script] --> [Django Backend] --> [Frontend Dashboard]
        ↑
     (Runs on Host)
```
- The agent collects running process data using `psutil`
- Sends it to the Django backend via REST API
- Frontend fetches and displays data in tree form using JavaScript

---

## 🚀 How to Run

### 🧱 Step 1: Setup Backend (Django)

```bash
# Create virtual environment (optional)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
python manage.py runserver
```

Server will start at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

### 🤖 Step 2: Run Agent Script

```bash
cd agent
python agent.py
```

> This will collect system process data and upload it to the backend every 10 seconds.


🗃 Folder Structure
process_monitoring_project/
│
├── agent/                   # Python script for collecting & uploading process data
│   ├── agent.py
│   └── config.ini           # Backend URL & API key
│
├── process_monitoring_project/
│   ├── monitoring/          # Django app (models, views, serializers)
│   ├── config/              # Django settings
│   └── manage.py
│
├── frontend/                # HTML, CSS, JS for UI (served by Django)
│   ├── index.html
│   ├── styles.css
│   └── script.js
│
├── db.sqlite3
└── README.md

🔒 API Key (Optional Security)

Agent sends API key while uploading snapshot:
You can configure it in config.ini file inside agent/.

```ini
[agent]
backend_url = http://127.0.0.1:8000
api_key = your-secret-key
```
📄 License

This project is built for professional evaluation purposes and intended to demonstrate real-world Django development skills.
Usage beyond this scope is not authorized without prior consent.

👨‍💻 Author

Prince Gangwar
🎓 Django Developer | Backend Enthusiast
🔗 LinkedIn Profile (https://www.linkedin.com/in/prince-gangwar-15742b249/)
