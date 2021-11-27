import string
import random


cars_names = [
    "Aston Martin",
    "Audi",
    "BMW",
    "Cadillac",
    "Chevrolet",
    "Datsun",
    "Ferrari",
    "Ford",
    "Honda",
    "Mercedes",
    "Nissan",
    "Porsche",
    "Rolls-Royce",
    "Toyota",
    "Volkswagen",
    "Subaru",
]


def random_vin_number() -> str:
    vin_number = "".join(random.choices(string.ascii_uppercase + string.digits, k=17))
    return vin_number


def random_name() -> str:
    name = random.choice(cars_names)
    return name


class Car:
    def __init__(self, model: str, vin_number: str, name: str) -> None:
        self.model = model
        self.vin_number = vin_number
        self.name = name

        if self.name is None:
            self.set_name(random_name())

        if self.vin_number is None:
            self.set_vin_number(random_vin_number())

    def set_vin_number(self, vin_number) -> None:
        self.vin_number = vin_number

    def set_name(self, name) -> None:
        self.name = name


class Human:
    def __init__(self, name: str, age: int, cars: list[Car]):

        self.name = name
        self.age = age
        self.cars = cars
        self.current_car = None  # В моей версии python еще нету Optional

    def set_current_car(self, number_of_car):
        if number_of_car >= 0 or number_of_car >= len(self.cars) - 1:
            self.current_car = self.cars[number_of_car]
        else:
            raise ValueError("No such cars")


def choose_current_car(human: Human) -> None:
    output_str = (
        "Choose new current car for " + human.name + " (enter number). Cars list:"
    )

    for i in range(len(human.cars)):
        output_str += "\n" + str(i + 1) + ") " + str(human.cars[i].name)

    number_of_car = int(input(output_str + "\n")) - 1

    try:
        human.set_current_car(number_of_car)
        print("New current car: " + human.current_car.name)
    except ValueError:
        print("Incorrect number")


all_cars = [Car(model="AM20", vin_number=None, name=None) for i in range(0, 10)]

yuriy = Human(name="Yuriy", age=42, cars=all_cars[0:5])
platon = Human(name="Platon", age=35, cars=all_cars[5:10])


def main() -> None:
    choose_current_car(yuriy)
    choose_current_car(platon)


if __name__ == "__main__":
    main()
