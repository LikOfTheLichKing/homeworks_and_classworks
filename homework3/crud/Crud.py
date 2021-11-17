import json
from typing import Any


class UserCRUD:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.data = None
        self.read_from_file()

    def read_from_file(self) -> None:
        with open(self.filename, "r") as file:
            self.data = json.load(file)

    @staticmethod
    def check_password_valid(password: str) -> bool:
        return len(password) < 8

    def check_info_on_data(self, login: str, password: str):
        return login in self.data and self.data[login]["password"] == password

    def write_to_file(self) -> None:
        with open(self.filename, "w") as file:
            json.dump(self.data, file)
        self.read_from_file()

    def add_new(self, login: str, data: dict[str, Any]) -> None:
        if login in self.data:
            raise ValueError("User with login {login} already exists")
        self.check_password_valid(password=data["password"])
        self.set_item(login, data)

    def set_item(self, login: str, data: dict[str, Any]) -> None:
        self.data[login] = data
        self.write_to_file()

    def get_item(self, login: str) -> dict[str, Any] | None:
        if login not in self.data:
            return None

        return self.data[login]

    def delete_item(self, login: str, password: str) -> None:
        if self.check_info_on_data(login=login, password=password):
            del self.data[login]
            self.write_to_file()

    def change_password(self, login: str, password: str, new_password: str) -> None:
        user = self.get_item(login)
        if None != user and self.check_info_on_data(login=login, password=password):
            if self.check_password_valid(password=new_password):
                self.data[login]["password"] = new_password
                self.write_to_file()

    def get_all_users(self) -> dict:
        return self.data

    def get_users_names(self) -> list[str]:
        names = [i for i in self.get_all_users()]
        return names
