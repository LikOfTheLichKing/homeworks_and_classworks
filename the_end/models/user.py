from pydantic import BaseModel, Field, validator


class RegistrationModel(BaseModel):
    login: str = Field(min_length=6)
    password: str = Field(min_length=8)

    @validator("login")
    def validate_login(cls, login: str) -> None:
        assert " " not in login, "No spaces allowed in login"
        return login


class UserModel(BaseModel):
    id: str
    login: str
