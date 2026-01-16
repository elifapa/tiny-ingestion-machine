from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PushRequest(_message.Message):
    __slots__ = ("payload", "timestamp")
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    payload: str
    timestamp: int
    def __init__(self, payload: _Optional[str] = ..., timestamp: _Optional[int] = ...) -> None: ...

class PushResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class PullRequest(_message.Message):
    __slots__ = ("number_of_messages",)
    NUMBER_OF_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    number_of_messages: int
    def __init__(self, number_of_messages: _Optional[int] = ...) -> None: ...

class PullResponse(_message.Message):
    __slots__ = ("id", "payload", "timestamp")
    ID_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    id: str
    payload: str
    timestamp: int
    def __init__(self, id: _Optional[str] = ..., payload: _Optional[str] = ..., timestamp: _Optional[int] = ...) -> None: ...
