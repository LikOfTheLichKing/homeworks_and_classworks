import string
import random


cars_names = ["Aston Martin", "Audi", "BMW", "Cadillac", "Chevrolet", "Datsun", "Ferrari", "Ford", "Honda", "Mercedes", "Nissan", "Porsche", "Rolls-Royce", "Toyota", "Volkswagen", "Subaru"]

class Car:
    def __init__(self, model: str):
        self.model = model
        self.vin_number = "".join(random.choices(string.ascii_uppercase + string.digits, k=17))
        self.name = cars_names[random.randint(0, len(cars_names)-1)]


class Human:
    def __init__(self, name: str, age: int, cars: list): #cars list will contain elements with class: Car

        self.name = name
        self.age = age
        self.cars = cars
        self.current_car = None

    def choose_current_car(self):
        number_in_cars_list = 0
        output_str = "Choose new current car for "+self.name+" (enter number). Cars list:\n"

        for i in range(0,len(self.cars)):
            output_str += str(i+1)+") "+self.cars[i].name+"\n"

        while number_in_cars_list < 1 or number_in_cars_list > len(self.cars):
            number_in_cars_list = int(input(output_str))

        self.current_car = self.cars[number_in_cars_list-1].name
        print("new current car:"+self.cars[number_in_cars_list-1].name)


all_cars = []
for i in range(0,10):
    all_cars.append(Car(model="AM20"))

yuriy = Human(name="Yuriy" , age=42, cars=all_cars[0:5])
platon = Human(name="Platon", age=35, cars=all_cars[5:10])

yuriy.choose_current_car()
platon.choose_current_car()