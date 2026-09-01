import json
from typing import Any, Dict, List

from src.core.exceptions import JsonFileNotFound, JsonParseError


class JsonLoader:
    @staticmethod
    def load(filepath) -> List[Dict[str, Any]]:
        """Load JSON data and validate it is a non-empty list of dicts."""

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

        except FileNotFoundError:
            raise JsonFileNotFound(filepath)

        except json.JSONDecodeError as e:
            raise JsonParseError(filepath, e)

        if not isinstance(data, list) or not data:
            raise JsonParseError(filepath, "Expected a non-empty list of objects!")

        return data
