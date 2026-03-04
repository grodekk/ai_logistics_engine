from pathlib import Path


def build_fullpath(filepath):
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    return data_dir / filepath