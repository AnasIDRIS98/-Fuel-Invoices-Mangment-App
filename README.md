# ⛽ Fuel Invoices Management App  
### (Desktop Application – PySide6 + SQLite + Secure Auth)  

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/UI-PySide6-green?logo=qt)](https://doc.qt.io/qtforpython/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-v1.0-orange)]()
[![Security](https://img.shields.io/badge/Security-Encrypted%20Passwords-success?logo=lock)]()
![WhatsApp Image 2025-11-09 at 21 50 06_d6db834e](https://github.com/user-attachments/assets/be2ec551-1983-47d5-8977-48db04d185b1)

---

## 🧭 Overview

*Fuel Invoices Management App* is a desktop-based application built to manage, track, and audit fuel invoices efficiently.  
Originally developed for *Concorp Petroleum, it enables smooth handling of invoice data with **secure local authentication, **persistent storage, and **modern UI/UX* powered by *PySide6*.

Built for everyday operational reliability and long-term scalability.

---

## 🧩 Key Features

✅ Add, edit, and view invoices  
✅ Persistent *SQLite* database (auto-created invoices.db)  
✅ Secure authentication with salted password hashing (*PBKDF2-HMAC-SHA256*)  
✅ Audit logging for all critical user actions  
✅ Excel and PDF export options  
✅ Decimal-based arithmetic for precise financial calculations  
✅ Clean, distraction-free UI with modal dialogs  
✅ Cross-platform (Windows, macOS, Linux)  

---

## 📂 Project Structure

Fuel-Invoices-Mangment-App/
│
├── app/
│   ├── main.py             # Application entry point
│   ├── ui/                 # PySide6 UI components
│   ├── database.py         # SQLite schema and CRUD logic
│   ├── auth.py             # Authentication & user management
│   ├── audit.py            # Audit logging system
│   └── utils/              # Helpers & utility scripts
│
├── app/assets/             # Placeholder images, icons, animations
├── data/                   # Local database storage
│   └── invoices.db
│
├── requirements.txt
├── LICENSE
└── README.md

---

## 🚀 Installation & Setup

1️⃣ *Clone the repository*
```bash
git clone https://github.com/AnasIDRIS98/Fuel-Invoices-Mangment-App.git
cd Fuel-Invoices-Mangment-App

2️⃣ Create and activate virtual environment

python -m venv .venv

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

3️⃣ Install dependencies

pip install --upgrade pip
pip install -r requirements.txt

4️⃣ Run the app

python app/main.py

💡 Note: The database (data/invoices.db) is automatically created on first launch.

⸻

🔐 Security Highlights
	•	Password Hashing: PBKDF2-HMAC-SHA256 (200k iterations, unique salt)
	•	Password Policy: Must include uppercase, lowercase, digits, and special characters
	•	Audit Trail: Logs all user logins, CRUD actions, imports/exports
	•	Encryption Ready: Supports optional encrypted backups
	•	Data Hygiene: Sensitive fields cleared after use
	•	⚠ Never commit data/invoices.db or credentials to public repos.

⸻


<details>
<summary>📘 <b>Version History (click to expand)</b></summary>


Version	Description	Key Fixes / Changes
v0.1	Streamlit prototype	Manual entry, no persistence
v0.2	Improved Streamlit UI	Added filters & Excel export
v0.3	SQLite persistence	Accurate decimals + bulk import
v1.0	PySide6 migration	Authentication, audit logs, UI overhaul

</details>



⸻


<details>
<summary>🧱 <b>Development Roadmap (click to expand)</b></summary>


Short Term (1–3 months)
	•	Role-based access control (RBAC)
	•	Undo/restore & soft delete
	•	Unit testing for core modules

Mid Term (3–6 months)
	•	REST API (FastAPI)
	•	Encrypted DB backups
	•	Enhanced PDF templates with branding

Long Term (6–12+ months)
	•	SSO / LDAP integration
	•	Signed installers (PyInstaller)
	•	Cloud sync & analytics dashboard

</details>



⸻

🧰 Tech Stack

Layer	Technology
Frontend	PySide6 (Qt for Python)
Backend	SQLite + Python
Authentication	PBKDF2-HMAC-SHA256
Reporting	ReportLab (PDF Export)
Data Handling	pandas, decimal
Environment	venv (Python Virtualenv)


⸻

🧑‍💻 Author

👤 Anas Idris
🛠 Software Engineer & Data Systems Developer
🏢 Concorp Petroleum
📫 LinkedIn | GitHub

⸻

⚖ License

This project is licensed under the MIT License.
You are free to use, modify, and distribute it with proper attribution.

⸻

⭐ Support & Feedback

If you find this project useful, please ⭐ star the repo!
Feedback and feature suggestions are welcome in the Issues section.

⸻
