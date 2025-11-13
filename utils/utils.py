def greet(name:str, age:int):
    return f"Hello, {name.title()}!. Your age is {age} years old."

msg = greet("rozer", 28)
print(msg)
class Person:
    nationality:str = ""
    def __init__(self, name:str, age:int, nationality:str) -> None:
        self.name = name
        self.age = age
        self.nationality = nationality

    def say_hello(self):
        return f"My name is {self.name}.Your age is {self.age} years old."

person = Person("robert", 32,"Indian")
print(person.say_hello())