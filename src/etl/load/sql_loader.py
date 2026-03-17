from types import SimpleNamespace

class SQLLoader:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self._load()

    def _load(self):
        for path in self.base_dir.rglob("*.sql"):
            parts = path.relative_to(self.base_dir).parts
            self._set_nested(self, parts[:-1], path.stem, path.read_text(encoding="utf-8"))

    @staticmethod
    def _set_nested(obj, dirs, name, content):
        for d in dirs:
            if not hasattr(obj, d):
                setattr(obj, d, SimpleNamespace())
            obj = getattr(obj, d)
        setattr(obj, name, content)