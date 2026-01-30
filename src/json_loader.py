import json
from src.exceptions import JsonFileNotFound, JsonParseError
from typing import List, Dict, Any

class JsonLoader:
    """Loader JSON files with proper error handling."""

    def __init__(self, filepath: str):
        self.filepath: str = filepath

    def load(self) -> List[Dict[str, Any]]:
        """Load JSON data and validate it is a non-empty list of dicts."""

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

        except FileNotFoundError:
            raise JsonFileNotFound(self.filepath)

        except json.JSONDecodeError as e:
            raise JsonParseError(self.filepath, e)

        if not isinstance(data, list) or not data:
            raise JsonParseError(self.filepath, "Expected a non-empty list of objects!")

        return data