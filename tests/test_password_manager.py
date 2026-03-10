import os
import sys
import string
import tempfile
import unittest


# Make App modules importable when tests run from project root.
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
APP_DIR = os.path.join(PROJECT_ROOT, "App")
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

import authentication
import file_management
import password_checker
import password_generator


class TestAuthentication(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.users_file = os.path.join(self.temp_dir.name, "users.csv")
        authentication.USERS_FILE = self.users_file

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_hash_password_returns_hashed_bytes(self):
        hashed = authentication.hash_password("MyPass123!")
        self.assertIsInstance(hashed, bytes)
        self.assertNotEqual(hashed.decode(), "MyPass123!")

    def test_register_user_success_and_duplicate_block(self):
        created = authentication.register_user("a@example.com", "user1", "Pass123!")
        self.assertTrue(created)

        duplicate_email = authentication.register_user("a@example.com", "user2", "Pass123!")
        duplicate_username = authentication.register_user("b@example.com", "user1", "Pass123!")
        self.assertFalse(duplicate_email)
        self.assertFalse(duplicate_username)

    def test_login_user_by_email_and_username(self):
        authentication.register_user("test@example.com", "testuser", "Pass123!")

        by_email = authentication.login_user("test@example.com", "Pass123!")
        by_username = authentication.login_user("testuser", "Pass123!")

        self.assertIsNotNone(by_email)
        self.assertIsNotNone(by_username)
        self.assertEqual(by_email["username"], "testuser")
        self.assertEqual(by_username["email"], "test@example.com")

    def test_login_user_invalid_or_missing_file(self):
        self.assertIsNone(authentication.login_user("notfound", "wrong"))

        authentication.register_user("x@example.com", "xuser", "Pass123!")
        self.assertIsNone(authentication.login_user("x@example.com", "WrongPass"))


class TestFileManagement(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.passwords_file = os.path.join(self.temp_dir.name, "passwords.csv")
        file_management.PASSWORD_FILE = self.passwords_file

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_encrypt_decrypt_round_trip(self):
        original = "MySecret!123"
        encrypted = file_management.encrypt_password(original)
        decrypted = file_management.decrypt_password(encrypted)

        self.assertNotEqual(encrypted, original)
        self.assertEqual(decrypted, original)

    def test_save_and_get_passwords(self):
        file_management.save_password("u@example.com", "github", "u@example.com", "P@ss123", "Strong")
        file_management.save_password("other@example.com", "google", "other@example.com", "Abc123!", "Moderate")

        results = file_management.get_passwords("u@example.com")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["website"], "github")
        self.assertEqual(results[0]["email"], "u@example.com")
        self.assertEqual(results[0]["password"], "P@ss123")
        self.assertEqual(results[0]["strength"], "Strong")

    def test_update_password(self):
        file_management.save_password("u@example.com", "github", "u@example.com", "OldPass1!", "Moderate")
        file_management.update_password("u@example.com", "github", "NewPass2@", "Strong")

        results = file_management.get_passwords("u@example.com")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["password"], "NewPass2@")
        self.assertEqual(results[0]["strength"], "Strong")

    def test_delete_password(self):
        file_management.save_password("u@example.com", "github", "u@example.com", "Pass1!", "Moderate")
        file_management.save_password("u@example.com", "gitlab", "u@example.com", "Pass2@", "Strong")

        file_management.delete_password("u@example.com", "github")
        results = file_management.get_passwords("u@example.com")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["website"], "gitlab")


class TestPasswordChecker(unittest.TestCase):
    def test_password_checker_scoring(self):
        self.assertEqual(password_checker.password_checker("abc"), 1)  # lowercase only
        self.assertEqual(password_checker.password_checker("Abcdef12"), 4)
        self.assertEqual(password_checker.password_checker("Abcdef12!"), 5)

    def test_password_strength_boundaries(self):
        self.assertEqual(password_checker.password_strength(0), "Weak")
        self.assertEqual(password_checker.password_strength(2), "Weak")
        self.assertEqual(password_checker.password_strength(3), "Moderate")
        self.assertEqual(password_checker.password_strength(4), "Moderate")
        self.assertEqual(password_checker.password_strength(5), "Strong")

    def test_check_password_strength_integration(self):
        self.assertEqual(password_checker.check_password_strength("abc"), "Weak")
        self.assertEqual(password_checker.check_password_strength("Abcdef12"), "Moderate")
        self.assertEqual(password_checker.check_password_strength("Abcdef12!"), "Strong")


class TestPasswordGenerator(unittest.TestCase):
    def test_generate_password_length(self):
        pw = password_generator.generate_password(length=24)
        self.assertEqual(len(pw), 24)

    def test_generate_password_respects_disabled_groups(self):
        pw = password_generator.generate_password(length=40, numbers=False, symbols=False, uppercase=False)
        allowed = set(string.ascii_lowercase)
        self.assertTrue(set(pw).issubset(allowed))

    def test_generate_password_with_all_enabled_uses_allowed_pool(self):
        pw = password_generator.generate_password(length=64, numbers=True, symbols=True, uppercase=True)
        allowed = set(string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation)
        self.assertTrue(set(pw).issubset(allowed))


if __name__ == "__main__":
    unittest.main()
