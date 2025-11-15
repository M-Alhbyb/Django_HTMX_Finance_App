# Django HTMX Finance App

A modern personal finance tracking application built with **Django**, **HTMX**, and **TailwindCSS**. The project focuses on simplicity, speed, and an interactive user experience without needing a full JavaScript frontend framework.

---

## 🚀 Features

* Add, edit, and delete transactions dynamically using HTMX
* Categorize income and expenses
* Real-time balance and analytics updates
* Django-based authentication system
* Responsive UI
* Clean and minimal code structure
* Import and Export data easily.

---

## 🛠️ Tech Stack

* **Backend:** Django 4+
* **Frontend:** HTMX + TailwindCSS
* **Database:** SQLite (default) or PostgreSQL
* **Template Engine:** Django Templates

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/M-Alhbyb/Django_HTMX_Finance_App.git
cd Django_HTMX_Finance_App
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Run the server

```bash
python manage.py runserver
```

---

## 🧩 Project Structure

```
├── finance_project/
│   ├── templates/
│   ├── static/
│   ├── views.py
│   ├── models.py
│   ├── urls.py
├── tracker/
├── static/
├── staticfiles/
├── manage.py
```

---

## ⚡ HTMX Usage Examples

### Dynamic Transaction Table Update

```html
<div hx-get="/transactions/" hx-trigger="load" hx-target="#transactions-table"></div>
```

### Inline Form Submission

```html
<form hx-post="/add/" hx-target="#transactions-table" hx-swap="outerHTML">
```

---

## 🖼️ Screenshots

*(Add screenshots here after deployment)*

---

## 🌍 Deployment

This App Live Previews:

* **Render:** [https://pasha-finance-app.onrender.com](https://pasha-finance-app.onrender.com)
---

## 🤝 Contribution

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

This project is licensed under the MIT License.
