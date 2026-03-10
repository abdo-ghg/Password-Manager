import csv
import os
import bcrypt

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Data")
USERS_FILE = os.path.join(DATA_DIR, "users.csv")
USERS_FIELDS = ["email", "username", "password"]


def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def register_user(email, username, password):

    os.makedirs(DATA_DIR, exist_ok=True)

    file_exists = os.path.isfile(USERS_FILE)

    if file_exists:
        try:
            with open(USERS_FILE, "r", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["email"] == email or row["username"] == username:
                        return False
        except FileNotFoundError:
            file_exists = False

    hashed = hash_password(password)

    with open(USERS_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=USERS_FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow({"email": email, "username": username, "password": hashed.decode()})

    return True


def login_user(identifier, password):

    try:
        with open(USERS_FILE, "r") as f:
            reader = csv.DictReader(f)

            for row in reader:
                if row["email"] == identifier or row["username"] == identifier:

                    if bcrypt.checkpw(password.encode(), row["password"].encode()):
                        return row

    except FileNotFoundError:
        return None

    return None