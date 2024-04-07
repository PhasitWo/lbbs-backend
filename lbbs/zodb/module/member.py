from .user import User

class Member(User):
    def __init__(self, user_id: str, password: str, name: str, role: str) -> None:
        """
        role : Student/Teacher
        """
        super().__init__(user_id, password, name)
        self.__role = role

    # TODO
    def addBorrow(self):
         pass

    def __str__(self) -> str:
            return f"{self.__user_id}-{self.__name}-{self.__role}"