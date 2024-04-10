from .user import User
import BTrees
import persistent

class Member(User):
    def __init__(self, user_id: str, password: str, name: str, role: str) -> None:
        """
        role : Student/Teacher
        """
        super().__init__(user_id, password, name)
        self._role = role
        self._borrow_list = persistent.list.PersistentList()

    def get_borrow_list(self) -> list:
        return self._borrow_list.copy()

    def add_borrowing(self, borrowing) -> None:
        self._borrow_list.append(borrowing)

    def __str__(self) -> str:
        return f"{self._user_id}-{self._name}-{self._role}"
