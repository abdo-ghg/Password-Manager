# Password Manager

Streamlit password manager app with user authentication, password generation, strength checking, and saved-password management.

## Requirements

- Python 3.10+
- pip

Dependencies are in `requirements.txt`.

## Run Locally

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run App/app.py
```

## Deployment Ready Files

- `requirements.txt`: Python dependencies.
- `Procfile`: Web start command for platforms like Render/Railway/Heroku-like environments.
- `.streamlit/config.toml`: Streamlit server configuration for hosted environments.
- `.gitignore`: Ignores generated runtime CSV data.

## Deploy (Render / Railway / Heroku-like)

Use these settings:

- Build command:

```bash
pip install -r requirements.txt
```

- Start command:

```bash
streamlit run App/app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
```

## Deploy (Streamlit Community Cloud)

Use:

- Main file path: `App/app.py`
- Python version: 3.10+
- Requirements file: `requirements.txt`

## Data Storage Note

- Runtime files are stored in `Data/users.csv` and `Data/passwords.csv`.
- On many hosting platforms, filesystem data is ephemeral. For production, use persistent storage (database or mounted volume).

