from dataclasses import dataclass


@dataclass
class ErrorDTO:
    """Problem-Details error message format -> https://www.rfc-editor.org/rfc/rfc9457.html"""

    _type: str
    _status: str
    _title: str
    _detail: str
    _instance: str

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, val: str) -> None:
        self._type = val

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, val: str) -> None:
        self._status = val

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, val: str) -> None:
        self._title = val

    @property
    def detail(self) -> str:
        return self._detail

    @detail.setter
    def detail(self, val: str) -> None:
        self._detail = val

    @property
    def instance(self) -> str:
        return self._instance

    @instance.setter
    def instance(self, val: str) -> None:
        self._instance = val
