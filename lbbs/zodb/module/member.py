import datetime
from .user import User
import persistent
import jwt


class Member(User):
    def __init__(self, user_id: int, password: str, name: str, role: str) -> None:
        """
        role : Student/Teacher
        """
        super().__init__(user_id, password, name)
        self._role = role
        self._borrow_list = persistent.list.PersistentList()

    @staticmethod
    def authenticate(root, username: str, password: str) -> tuple:
        """
        require root of the zodb
        return str of access token if username and password is matched, otherwise return None
        """
        member_lst = list(root.member.values())
        for member in member_lst:
            if username == member.get_name():
                is_auth = member.verify(password)
                if is_auth:
                    KEY = "sample_secret_key"
                    ACCESS_DURATION = 30
                    token = jwt.encode(
                        {
                            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                            + datetime.timedelta(minutes=ACCESS_DURATION),
                            "member_id": member.get_id(),
                            "permission": "member"
                        },
                        KEY,
                        algorithm="HS256",
                    )
                    return member.get_id(), member.get_name(), token
                break
        return None

    def get_borrow_list(self) -> list:
        return self._borrow_list.copy()

    def add_borrowing(self, borrowing) -> None:
        self._borrow_list.append(borrowing)

    def __str__(self) -> str:
        return f"{self._user_id}-{self._name}-{self._role}"
