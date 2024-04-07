import persistent
import bcrypt


class User(persistent.Persistent):
    def __init__(self, user_id: str, password: str, name: str) -> None:
        self.__user_id = user_id
        self.__name = name
        self.__salt = bcrypt.gensalt()
        self.__password = bcrypt.hashpw(password.encode(), self.__salt)

    def verify(self, password: str) -> bool:
        """
        Return True if the password is correct, or False otherwise.
        """
        inp_psw = bcrypt.hashpw(password.encode(), self.__salt)
        if inp_psw == self.__password:
            return True
        return False
