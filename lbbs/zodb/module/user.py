import persistent
import bcrypt


class User(persistent.Persistent):
    def __init__(self, user_id: str, password: str, name: str) -> None:
        self._user_id = user_id
        self._name = name
        self._salt = bcrypt.gensalt()
        self._password = bcrypt.hashpw(password.encode(), self._salt)

    def verify(self, password: str) -> bool:
        """
        Return True if the password is correct, or False otherwise.
        """
        inp_psw = bcrypt.hashpw(password.encode(), self._salt)
        if inp_psw == self._password:
            return True
        return False
