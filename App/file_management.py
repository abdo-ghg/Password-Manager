import csv
import base64
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Data")
PASSWORD_FILE = os.path.join(DATA_DIR, "passwords.csv")
PASSWORD_FIELDS = ["user_email", "website", "website_email", "password", "strength"]


def _read_password_rows():
    """Read rows from either new header-based CSV or legacy headerless CSV."""
    if not os.path.isfile(PASSWORD_FILE) or os.path.getsize(PASSWORD_FILE) == 0:
        return []

    with open(PASSWORD_FILE, "r", newline="") as f:
        first_line = f.readline().strip()
        f.seek(0)

        if first_line.lower().startswith("user_email,"):
            reader = csv.DictReader(f)
            return [row for row in reader if row.get("user_email")]

        reader = csv.reader(f)
        rows = []
        for row in reader:
            if len(row) < 5:
                continue
            rows.append({
                "user_email": row[0],
                "website": row[1],
                "website_email": row[2],
                "password": row[3],
                "strength": row[4],
            })
        return rows


def encrypt_password(password):
    return base64.b64encode(password.encode()).decode()


def decrypt_password(password):
    return base64.b64decode(password.encode()).decode()


def save_password(user_email, website, website_email, password, strength):

    encrypted = encrypt_password(password)
    os.makedirs(DATA_DIR, exist_ok=True)
    needs_header = not os.path.isfile(PASSWORD_FILE) or os.path.getsize(PASSWORD_FILE) == 0

    with open(PASSWORD_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=PASSWORD_FIELDS)
        if needs_header:
            writer.writeheader()
        writer.writerow({
            "user_email": user_email,
            "website": website,
            "website_email": website_email,
            "password": encrypted,
            "strength": strength,
        })


def get_passwords(user_email):

    results = []

    try:
        for row in _read_password_rows():
            if row["user_email"] == user_email:
                results.append({
                    "website": row["website"],
                    "email": row["website_email"],
                    "password": decrypt_password(row["password"]),
                    "strength": row["strength"],
                })

    except FileNotFoundError:
        pass

    return results


def delete_password(user_email, website):

    rows = []

    for row in _read_password_rows():
        if not (row["user_email"] == user_email and row["website"] == website):
            rows.append(row)

    with open(PASSWORD_FILE, "w", newline="") as f:

        writer = csv.DictWriter(f, fieldnames=PASSWORD_FIELDS)

        writer.writeheader()
        writer.writerows(rows)


def update_password(user_email, website, new_password, strength):

    rows = []

    encrypted = encrypt_password(new_password)

    for row in _read_password_rows():
        if row["user_email"] == user_email and row["website"] == website:
            row["password"] = encrypted
            row["strength"] = strength

        rows.append(row)

    with open(PASSWORD_FILE, "w", newline="") as f:

        writer = csv.DictWriter(f, fieldnames=PASSWORD_FIELDS)

        writer.writeheader()
        writer.writerows(rows)