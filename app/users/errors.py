from pydantic import EmailStr


class EmailAlreadyExistsError(Exception):
    def __init__(self, email: str| EmailStr):
        super().__init__(f"User with email {email} already exists")
        self.email = email


class UserNotFoundError(Exception):
    def __init__(self, user_id: int):
        super().__init__(f"User {user_id} not found")
        self.user_id = user_id