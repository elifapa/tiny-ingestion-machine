from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PushRequest(_message.Message):
    __slots__ = ("topic_name", "partition_id", "payload", "timestamp")
    TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    PARTITION_ID_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    topic_name: str
    partition_id: int
    payload: str
    timestamp: int
    def __init__(self, topic_name: _Optional[str] = ..., partition_id: _Optional[int] = ..., payload: _Optional[str] = ..., timestamp: _Optional[int] = ...) -> None: ...

class PushResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class PullRequest(_message.Message):
    __slots__ = ("topic_name", "number_of_messages")
    TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    topic_name: str
    number_of_messages: int
    def __init__(self, topic_name: _Optional[str] = ..., number_of_messages: _Optional[int] = ...) -> None: ...

class PullResponse(_message.Message):
    __slots__ = ("topic_name", "id", "payload", "timestamp")
    TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    topic_name: str
    id: str
    payload: str
    timestamp: int
    def __init__(self, topic_name: _Optional[str] = ..., id: _Optional[str] = ..., payload: _Optional[str] = ..., timestamp: _Optional[int] = ...) -> None: ...

class AddTopicRequest(_message.Message):
    __slots__ = ("topic_name", "partition_count", "replication_factor")
    TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    PARTITION_COUNT_FIELD_NUMBER: _ClassVar[int]
    REPLICATION_FACTOR_FIELD_NUMBER: _ClassVar[int]
    topic_name: str
    partition_count: int
    replication_factor: int
    def __init__(self, topic_name: _Optional[str] = ..., partition_count: _Optional[int] = ..., replication_factor: _Optional[int] = ...) -> None: ...

class AddTopicResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class Topic(_message.Message):
    __slots__ = ("name", "partition_count", "replication_factor", "created_at")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PARTITION_COUNT_FIELD_NUMBER: _ClassVar[int]
    REPLICATION_FACTOR_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    name: str
    partition_count: int
    replication_factor: int
    created_at: int
    def __init__(self, name: _Optional[str] = ..., partition_count: _Optional[int] = ..., replication_factor: _Optional[int] = ..., created_at: _Optional[int] = ...) -> None: ...

class ListTopicsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListTopicsResponse(_message.Message):
    __slots__ = ("topics",)
    TOPICS_FIELD_NUMBER: _ClassVar[int]
    topics: _containers.RepeatedCompositeFieldContainer[Topic]
    def __init__(self, topics: _Optional[_Iterable[_Union[Topic, _Mapping]]] = ...) -> None: ...
