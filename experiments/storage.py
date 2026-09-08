from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any


def canonical_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def path_sha256(path: Path) -> str:
    if path.is_file():
        return file_sha256(path)
    if not path.is_dir():
        raise ValueError(f"cannot hash missing path: {path}")
    entries = [
        {"path": str(child.relative_to(path)), "sha256": file_sha256(child)}
        for child in sorted(candidate for candidate in path.rglob("*") if candidate.is_file())
    ]
    return canonical_hash(entries)


def write_json_new(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    descriptor = os.open(path, flags, 0o644)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False, default=str)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())


def write_json_atomic(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False, default=str)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    temporary.replace(path)


def existing_execution_keys(raw_root: Path) -> dict[str, Path]:
    found: dict[str, Path] = {}
    if not raw_root.exists():
        return found
    for path in raw_root.rglob("*.json"):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        key = payload.get("execution_key")
        if isinstance(key, str):
            found[key] = path
    return found
