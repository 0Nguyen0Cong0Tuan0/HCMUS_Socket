class Intro:
    name = "Tuan"

    @staticmethod
    def myAge():
        print("I am 10 years old")

    def hello(self):
        print(f"My name is {self.name}")
        Intro.myAge()
    
    def bark(self):
        print("HEllo")

class Student:

    def autoo(self):
        Intro.bark()

a = Student()
a.autoo()