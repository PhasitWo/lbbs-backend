from enum import Enum
import persistent


class BookStatus(Enum):
    AVAILABLE = "available"
    BORROW = "borrow"
    RESERVE = "reserve"


class Book(persistent.Persistent):
    def __init__(
        self, unique_id: str, status: BookStatus = BookStatus.AVAILABLE
    ) -> None:
        self.__unique_id = unique_id
        self.__status = status

    def setStatus(self, status: BookStatus) -> None:
        """
        status has to be type: BookStatus, for consistency across database
        """
        # if not isinstance(status, BookStatus):
        #     print(
        #         f"[CLASS Book] the status argument has wrong type, status stays the same as '{self.__status.value}'"
        #     )
        #     return 0
        self.__status = status

    def __str__(self) -> str:
        return f"{self.__unique_id}-{self.__status.value}"
