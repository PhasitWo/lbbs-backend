from .user import User


class Librarian(User):
    # TODO should we add anything to make this class different from the super class?
    def __str__(self) -> str:
        return f"Librarian-{self.__user_id}-{self.__name}"
