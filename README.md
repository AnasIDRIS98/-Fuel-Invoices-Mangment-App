
# Fuel-Invoices-Mangment-App

Desktop application (PySide6) for managing fuel invoices: add, view, export, and audit. This repository includes a production-oriented scaffold, secure local authentication, persistent SQLite storage, and UI improvements inspired by modern UX practices.

## Contents
- `app/` — application code (PySide6)
- `app/assets/` — placeholder assets (replace with real images and animations)
- `data/` — local SQLite DB will be created here (`invoices.db`)
- `requirements.txt`
- `README.md`
- `.gitignore`

## Complete Version Timeline and Resolved Issues

### v0.1 — Prototype (Streamlit)
- A very simple Streamlit-based interface for entering and displaying invoices.
- Manual save/load of CSV/Excel files.
- **Problems:** No persistent storage; all data was stored in-memory (Streamlit session) and was lost on reload or session end.

### v0.2 — UX Improvements (Streamlit)
- Added filters and fields for price/quantity/total and a button to export to Excel.
- **Problems:** The layout included a persistent sidebar that distracted users. There was no authentication, and financial calculations used floating-point arithmetic leading to inaccuracies.

### v0.3 — Persistence & Accuracy
- Migrated to a persistent SQLite-based storage (`data/invoices.db`), replacing volatile session-only storage.
- Replaced floating-point math with `decimal.Decimal` for correct financial calculations and set precision to 28 digits.
- Implemented a bulk import workflow (Excel/CSV) with preview before committing.
- **Resolved:** Data loss and arithmetic rounding errors.

### v1.0 — Security Hardening & Desktop Migration (PySide6)
- Migrated UI to PySide6 for a native desktop experience with better control over windows, modals, and transitions.
- Implemented local authentication with a `users` table in SQLite and secure password hashing (PBKDF2-HMAC-SHA256 with salt and 200k iterations).
- Enforced a password complexity policy (minimum length, upper/lower case, digits, special characters).
- Added `audit_log` to record all critical events: CRUD operations, login attempts, imports/exports, and UI interactions for analytics.
- Implemented a central login dialog with optional Lottie animation and a blurred refinery background (replace assets/refinery_bg.jpg).
- Implemented modal-like invoice listing and nested preview windows, as well as PDF export support via ReportLab (optional, requires package).
- UX polish: hide non-essential panels after login, show concise confirmations (toasts), and clear sensitive fields after use.

## Problems Encountered and their Solutions (detailed)
1. **Volatile session data (streamlit)**
   - Problem: data not persistent; lost after reload
   - Fix: moved to SQLite with proper CRUD functions and persistent DB file.

2. **Floating-point rounding errors**
   - Problem: inaccurate totals
   - Fix: use `decimal.Decimal` for all monetary arithmetic and set `getcontext().prec = 28`.

3. **Windows installation and PATH issues**
   - Problem: PowerShell ExecutionPolicy and missing pip in PATH caused install friction
   - Fix: documented venv activate commands and fallback `python -m pip install ...` approach.

4. **Optional packages failing (st_aggrid / streamlit-lottie)**
   - Fix: made optional and created fallback behaviors for both Streamlit and Desktop flows.

5. **Plain-text passwords in prototype**
   - Problem: major security flaw
   - Fix: implemented salted hashed passwords with PBKDF2 and enforced policy checks.

6. **No audit trail for operations**
   - Fix: audit_log table and logging on each critical path (insert/update/delete/login/export/ui events).

## Future Development Plans (Roadmap)
**Short term (1–3 months):**
- Role-based access control (RBAC) and fine-grained permissions.
- Undo/restore functionality and soft-deletes.
- Unit tests for DB and business logic.

**Mid term (3–6 months):**
- Add a lightweight REST API (FastAPI) for integrations.
- Scheduled encrypted backups for the DB file.
- Improved PDF templates and per-client branding options.

**Long term (6–12+ months):**
- Enterprise SSO/LDAP integration and central user management.
- Signed installers and cross-platform packaging (PyInstaller).
- Cloud-sync (optional, encrypted) and collaboration features.
- Analytics dashboard with scheduled reports.

## How to run
1. Create venv and activate it:
   ```bash
   python -m venv .venv
   # Windows (PowerShell)
   .\.venv\Scripts\Activate.ps1
   # or (CMD)
   .venv\Scripts\activate
   # Linux/macOS
   source .venv/bin/activate
   ```
2. Install requirements:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python app/main.py
   ```

## Security Notes
- Do not commit `data/invoices.db` to public repositories.
- Use encrypted backups for production data and consider using Postgres with encrypted volumes for production deployments.
