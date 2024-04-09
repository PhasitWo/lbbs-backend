from .user import User
import BTrees
import persistent

class Member(User):
    def __init__(self, user_id: str, password: str, name: str, role: str) -> None:
        """
        role : Student/Teacher
        """
        super().__init__(user_id, password, name)
        self.__role = role
        self.__borrow_list = persistent.list.PersistentList()

    def get_borrow_list(self) -> list:
        return self.__borrow_list

    def add_borrowing(self, borrowing) -> None:
        self.__borrow_list.append(borrowing)

    def __str__(self) -> str:
        return f"{self.__user_id}-{self.__name}-{self.__role}"
