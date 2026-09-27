"""Shared strict validation and reproducible serialization."""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
from typing import Any

class ValidationError(ValueError):
    """A declared model, data or interface contract was violated."""


def number(value: Any, name: str, low: float | None = None,
           high: float | None = None, *, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        raise ValidationError(f'{name}: a finite number is required')
    value = float(value)
    if not math.isfinite(value):
        raise ValidationError(f'{name}: NaN and infinity are not accepted')
    if positive and value <= 0:
        raise ValidationError(f'{name}: must be positive')
    if low is not None and value < low:
        raise ValidationError(f'{name}: must be >= {low}')
    if high is not None and value > high:
        raise ValidationError(f'{name}: must be <= {high}')
    return value


def integer(value: Any, name: str, low: int, high: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
        raise ValidationError(f'{name}: integer in [{low}, {high}] required')
    return value


def object_keys(obj: Any, allowed: set[str], required: set[str] = frozenset()) -> dict:
    if not isinstance(obj, dict):
        raise ValidationError('Expected a JSON object')
    extra, missing = set(obj) - allowed, required - set(obj)
    if extra or missing:
        raise ValidationError(f'Unknown fields: {sorted(extra)}; missing fields: {sorted(missing)}')
    return obj


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(',', ':'), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def load_json(path: str | Path, max_bytes: int = 4_000_000) -> Any:
    path = Path(path)
    if path.stat().st_size > max_bytes:
        raise ValidationError('JSON file exceeds the declared size limit')
    def pairs(items):
        obj = {}
        for key, value in items:
            if key in obj:
                raise ValidationError(f'Duplicate JSON key: {key}')
            obj[key] = value
        return obj
    def reject(token):
        raise ValidationError(f'Non-finite JSON constant: {token}')
    try:
        return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs,
                          parse_constant=reject)
    except (json.JSONDecodeError, RecursionError) as exc:
        raise ValidationError('Malformed JSON') from exc


def write_json(path: str | Path, value: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True, allow_nan=False) + '\n', encoding='utf-8')


def source_digest() -> str:
    """Hash shipped executable Python and model/catalog data, not mutable output logs."""
    root = Path(__file__).parent
    entries = {}
    for p in sorted(root.rglob('*')):
        if p.is_file() and (p.suffix == '.py' or p.parent.name == 'data'):
            entries[p.relative_to(root).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return digest(entries)
