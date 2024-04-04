class Student:
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

    def __str__(self) -> str:
        return f"{self.id}-{self.name}"