"""Materialize the frozen R2 Reality Capsule from native Git object bytes.

This module never calls run_reality_certificate. Reality execution belongs to
a later dispatch after the R3 freeze has been accepted.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path
from typing import Any

EXPECTED_BLOB_SHA = "b265043bc4dac9ee2ca45057fcca18e451c51e25"
CAPSULE_FILENAME = "docs/first-principles/v5.0.8/REAL-CAPSULE-SOURCE-R2.py"


class MaterializationError(RuntimeError):
    """The frozen capsule could not be materialized exactly."""


def materialize_frozen_capsule(
    git_repository: str | Path,
    object_id: str = EXPECTED_BLOB_SHA,
) -> dict[str, Any]:
    """Return a fresh namespace containing the callable frozen certificate.

    The caller is responsible for the later Reality timing and invocation.
    """
    if not re.fullmatch(r"[0-9a-f]{40}", object_id):
        raise MaterializationError("INVALID_OBJECT_ID")

    command = [
        "git",
        "-C",
        str(git_repository),
        "cat-file",
        "blob",
        object_id,
    ]
    completed = subprocess.run(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        shell=False,
        text=False,
    )
    if completed.returncode != 0 or not isinstance(completed.stdout, bytes):
        raise MaterializationError("GIT_BLOB_READ_FAILED")

    source_bytes = completed.stdout
    header = b"blob " + str(len(source_bytes)).encode("ascii") + b"\x00"
    actual_sha = hashlib.sha1(header + source_bytes).hexdigest()
    if actual_sha != EXPECTED_BLOB_SHA:
        raise MaterializationError("FROZEN_BLOB_SHA_MISMATCH")
    if not source_bytes.isascii():
        raise MaterializationError("FROZEN_BLOB_NOT_ASCII")

    code = compile(source_bytes, CAPSULE_FILENAME, "exec")
    namespace: dict[str, Any] = {"__name__": "_frozen_reality_capsule_r2_"}
    exec(code, namespace, namespace)
    if not callable(namespace.get("run_reality_certificate")):
        raise MaterializationError("CERTIFICATE_NOT_CALLABLE")
    return namespace
