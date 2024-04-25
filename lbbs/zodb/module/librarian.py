import datetime

import jwt
from .user import User


class Librarian(User):
    @staticmethod
    def authenticate(root, username: str, password: str) -> str:
        """
        require root of the zodb
        return str of access token if username and password is matched, otherwise return None
        """
        librarian_lst = list(root.librarian.values())
        for librarian in librarian_lst:
            if username == librarian.get_name():
                is_auth = librarian.verify(password)
                if is_auth:
                    KEY = "sample_secret_key"
                    ACCESS_DURATION = 8
                    token = jwt.encode(
                        {
                            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                            + datetime.timedelta(hours=ACCESS_DURATION),
                            "librarian_id": librarian.get_id(),
                            "permission": "librarian",
                        },
                        KEY,
                        algorithm="HS256",
                    )
                    return librarian.get_id(), librarian.get_name(), token
                break
        return None, None, None

    def __str__(self) -> str:
        return f"Librarian-{self._user_id}-{self._name}"
