from pydantic import BaseModel, Field, validator


class RegistrationModel(BaseModel):
    login: str = Field(min_length=6)
    password: str = Field(min_length=8)

    @validator("login")
    def validate_login(cls, login: str) -> str:
        assert " " not in login, "No spaces allowed in login"
        return login

class DeleteModel(BaseModel):
    login: str = Field(min_length=6)
    password: str = Field(min_length=8)

    def get_fields(self):
        return self.login, self.password

class BaseUserModel(BaseModel):
    id: str
    login: str


class UserModel(BaseUserModel):
    followers: int
    follows: int
