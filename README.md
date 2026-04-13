# Password Manager

A Streamlit-based password manager with account authentication, password generation, strength evaluation, and CRUD operations for saved credentials.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [How to Use](#how-to-use)
- [Data Storage](#data-storage)
- [Testing](#testing)
- [Deployment](#deployment)
- [Security Notes](#security-notes)
- [Known Issues](#known-issues)
- [Future Improvements](#future-improvements)

## Overview

This project provides a simple personal password manager UI built with Streamlit.

Main capabilities:
- User registration and login.
- Secure hashing for account passwords using bcrypt.
- Password generation with configurable options.
- Password strength scoring (Weak, Moderate, Strong).
- Save, view, update, and delete stored credentials.

## Features

- Authentication
	- Register with email, username, and password.
	- Login using either email or username.
	- User passwords are stored as bcrypt hashes.

- Password Generator
	- Configurable length (6 to 64).
	- Optional uppercase letters, numbers, and symbols.

- Strength Checker
	- Evaluates password based on length and character diversity.
	- Returns one of: Weak, Moderate, Strong.
	- Provides UI tips to improve weak passwords.

- Password Management
	- Save password entries per authenticated user.
	- View stored entries (toggle hidden/visible passwords).
	- Update existing entries.
	- Delete entries.

## Tech Stack

- Python 3.10+
- Streamlit
- bcrypt
- CSV file storage (local filesystem)

## Project Structure

```text
Password Manager/
├─ Procfile
├─ README.md
├─ requirements.txt
├─ System Requirment.txt
├─ App/
│  ├─ app.py
│  ├─ authentication.py
│  ├─ file_management.py
│  ├─ password_checker.py
│  └─ password_generator.py
├─ Data/
│  ├─ passwords.csv
│  └─ users.csv
├─ Photos/
└─ tests/
	 └─ test_password_manager.py
```

## Requirements

- OS: Windows, Linux, or macOS
- Python: 3.10 or newer
- pip
- Browser: Chrome, Edge, Firefox, or equivalent

Dependencies are listed in `requirements.txt`:
- streamlit>=1.30.0
- bcrypt>=4.0.1

## Quick Start

### 1. Clone the project

```bash
git clone <your-repository-url>
cd "Password Manager"
```

### 2. Create and activate virtual environment

Windows (PowerShell):

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

From project root:

```bash
streamlit run App/app.py
```

After launch, open the local URL shown by Streamlit (usually `http://localhost:8501`).

## How to Use

1. Create an account from the Register tab.
2. Log in with your email or username.
3. Use the sidebar to navigate features:
	 - Password Generator
	 - Check Strength
	 - Save Password
	 - View Passwords
	 - Update Password
	 - Delete Password
	 - Logout

## Data Storage

Data is persisted in local CSV files under `Data/`:

- `Data/users.csv`
	- Columns: `email`, `username`, `password`
	- `password` is stored as a bcrypt hash.

- `Data/passwords.csv`
	- Columns: `user_email`, `website`, `website_email`, `password`, `strength`
	- `password` is currently stored using Base64 encoding.

## Testing

Unit tests are available in `tests/test_password_manager.py`.

Run tests:

```bash
python -m unittest discover -s tests -q
```

Important note:
- The current `App/password_checker.py` contains interactive top-level input/print code, which can block automated test execution when the module is imported.
- To make tests fully non-interactive, move that interactive snippet under:

```python
if __name__ == "__main__":
		x = input("Enter your password: ")
		strength = check_password_strength(x)
		print(f"Password strength: {strength}")
```

## Deployment

### Procfile (already included)

`Procfile` uses:

```text
web: streamlit run App/app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
```

### Render / Railway / Heroku-like platforms

- Build command:

```bash
pip install -r requirements.txt
```

- Start command:

```bash
streamlit run App/app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
```

### Streamlit Community Cloud

- Main file path: `App/app.py`
- Python version: 3.10+
- Requirements file: `requirements.txt`

## Security Notes

- Good:
	- User account passwords are hashed with bcrypt.

- Important limitation:
	- Saved website passwords are only Base64-encoded, not encrypted.
	- Base64 is reversible encoding and should not be treated as secure storage.

For production-grade security:
- Replace CSV storage with a database.
- Encrypt credential data using a proper encryption strategy and key management.
- Use environment variables or a secrets manager for sensitive configuration.
- Enforce HTTPS/TLS in deployment.

## Known Issues

- `App/password_checker.py` runs interactive input at import time, which interferes with some automated workflows.
- CSV-based local storage is not suitable for concurrent multi-user production environments.

## Future Improvements

- Replace Base64 credential storage with real encryption.
- Move data storage from CSV to a database (for integrity and scale).
- Add password entry search/filter.
- Add per-entry metadata (creation date, update date).
- Add CI pipeline to run tests automatically.

