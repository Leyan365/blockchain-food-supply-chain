import json
from pathlib import Path

from werkzeug.security import check_password_hash


class UserService:
    def __init__(self, users_file='data/users.json'):
        self.users_file = Path(users_file)

    def get_user_by_email(self, email):
        email = (email or '').strip().lower()
        for user in self._load_users():
            if user.get('email', '').lower() == email:
                return user
        return None

    def verify_user_password(self, email, password):
        user = self.get_user_by_email(email)
        if not user:
            return None

        if check_password_hash(user.get('password_hash', ''), password or ''):
            return user
        return None

    def _load_users(self):
        if not self.users_file.exists():
            return []

        try:
            with self.users_file.open('r', encoding='utf-8') as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError):
            return []

        return data.get('users', [])


user_service = UserService()
