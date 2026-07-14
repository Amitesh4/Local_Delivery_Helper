# 📦 Local Delivery Helper

A full-stack web application designed to streamline local delivery logistics, complete with user authentication, registration, and dynamic CRUD database workflows. This application acts as a centralized helper system for managing order/delivery statuses securely and efficiently.

---

## 🚀 Key Features
* **User Authentication:** Complete login and registration system ensuring restricted access to authorized users.
* **Full CRUD Functionality:** Seamlessly Create, Read, Update, and Delete delivery data entries dynamically.
* **Secure Storage Architecture:** Utilizes an isolated database structure via an instance folder architecture to maintain clear separation of logic and data records.

---

## 🛠️ Tech Stack & Tools
* **Backend & Logic:** Python, Flask framework
* **Frontend UI:** HTML5 template components, CSS3
* **Version Control:** Git & GitHub

---

## 📁 Project Structure
```text
├── instance/          # (Kept local) Secure local database instances
├── templates/         # UI layout and user view templates
├── venv/              # (Kept local) Isolated Python environment dependencies
├── flask_app.py       # Core application initialization, routing, and CRUD logic
├── .gitignore         # Filters environments and localized database instances
└── README.md          # Project documentation
