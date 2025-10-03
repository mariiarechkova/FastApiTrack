from app.core.security import create_access_token, verify_password
from app.users.repositories import UserRepository
from app.users.schemas import Token


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def login(self, email: str, password: str) -> Token:
        user = await self.repo.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password")
        token = create_access_token(user)
        return Token(access_token=token)
