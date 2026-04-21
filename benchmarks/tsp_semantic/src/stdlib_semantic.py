from collections import defaultdict
from pathlib import Path


def group_paths(items: list[str]) -> defaultdict[str, list[Path]]:
    grouped = defaultdict(list)
    for item in items:
        path = Path(item)
        grouped[path.suffix].append(path)
    return grouped


files = group_paths(["src/app.py", "tests/test_runner.py"])
python_files = files[".py"]
