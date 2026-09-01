import uuid
from datetime import datetime
from typing import Any, Optional


class AppError(Exception):
    def __init__(self, message: str, user_message: Optional[str] = None):
        super().__init__(message)
        self.message: str = message
        self.user_message: str = user_message or message
        self.error_id: str = str(uuid.uuid4())[:8]
        self.timestamp: datetime = datetime.now()

    def to_dict(self) -> dict:
        return {
            "error": self.__class__.__name__,
            "message": self.user_message,
            "error_id": self.error_id,
            "timestamp": self.timestamp.isoformat(),
        }


class InfrastructureError(AppError):
    pass


class BusinessLogicError(AppError):
    pass


# Infrastructure errors
class JsonFileNotFound(InfrastructureError):
    def __init__(self, filepath: str):
        self.filepath: str = filepath
        super().__init__(
            message=f"File not found: {filepath}", user_message="Data File is missing! Please contact support."
        )


class JsonParseError(InfrastructureError):
    def __init__(self, filepath: str, original_error: Any):
        self.filepath: str = filepath
        self.original_error: Any = original_error
        super().__init__(
            message=f"JSON parsing error in {filepath}: {original_error}",
            user_message="Data file is corrupted! Please contact support.",
        )


class DatabaseError(InfrastructureError):
    pass


class ConnectionLostError(DatabaseError):
    pass


class BulkInsertError(DatabaseError):
    pass
