from pydantic import EmailStr


class NotFoundError(Exception):
    def __init__(self, entity: str, entity_id: int):
        super().__init__(f"{entity} {entity_id} not found")
        self.entity = entity
        self.entity_id = entity_id


class EmailAlreadyExistsError(Exception):
    def __init__(self, email: str| EmailStr):
        super().__init__(f"User with email {email} already exists")
        self.email = email