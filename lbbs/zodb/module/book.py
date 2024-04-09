import persistent
from .constant import BookStatus
from datetime import date


class Book(persistent.Persistent):
    def __init__(
        self, unique_id: str, status: BookStatus = BookStatus.AVAILABLE
    ) -> None:
        self.__unique_id = unique_id
        self.__status = status
        self.__expected_date = None  # expected date to be available again

    def set_status(self, status: BookStatus) -> None:
        """
        status has to be type: BookStatus, for consistency across database
        """
        self.__status = status

    def set_expected_date(self, expected_date: date) -> None:
        self.__expected_date = expected_date

    def get_book_data(self) -> dict:
        return {
            "unique_id": self.__unique_id,
            "status": self.__status,
            "expected_date": self.__expected_date,
        }

    def __str__(self) -> str:
        return f"{self.__unique_id}-{self.__status.value}"
