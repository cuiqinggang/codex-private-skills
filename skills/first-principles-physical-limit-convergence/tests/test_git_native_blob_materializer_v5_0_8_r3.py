"""R3 materialization validation; the Reality Certificate is never called."""

from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

RUNTIME_DIR = Path(__file__).resolve().parents[1] / "runtime"
sys.path.insert(0, str(RUNTIME_DIR))
import git_native_blob_materializer_v5_0_8_r3 as materializer

WRONG_EXISTING_BLOB = "de30a26c9c3f67084910f42931bac3201da991a9"


class GitNativeBlobMaterializerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        value = os.environ.get("R3_GIT_REPOSITORY")
        if not value:
            raise RuntimeError("R3_GIT_REPOSITORY is required")
        cls.git_repository = Path(value)

    def test_exact_frozen_blob_materializes_1000_times(self) -> None:
        for i in range(1000):
            with self.subTest(iteration=i):
                namespace = materializer.materialize_frozen_capsule(
                    self.git_repository
                )
                self.assertEqual(
                    namespace["__name__"], "_frozen_reality_capsule_r2_"
                )
                self.assertTrue(
                    callable(namespace.get("run_reality_certificate"))
                )

    def test_wrong_existing_blob_blocked_100_times(self) -> None:
        for i in range(100):
            with self.subTest(iteration=i):
                with self.assertRaisesRegex(
                    materializer.MaterializationError,
                    "FROZEN_BLOB_SHA_MISMATCH",
                ):
                    materializer.materialize_frozen_capsule(
                        self.git_repository, WRONG_EXISTING_BLOB
                    )

    def test_git_transport_keeps_raw_bytes(self) -> None:
        original_run = subprocess.run
        observed = []

        def capture(*args, **kwargs):
            observed.append((args, kwargs))
            return original_run(*args, **kwargs)

        with patch.object(materializer.subprocess, "run", side_effect=capture):
            materializer.materialize_frozen_capsule(self.git_repository)

        self.assertEqual(len(observed), 1)
        args, kwargs = observed[0]
        self.assertIsInstance(args[0], list)
        self.assertEqual(args[0][0], "git")
        self.assertEqual(args[0][-1], materializer.EXPECTED_BLOB_SHA)
        self.assertIs(kwargs["shell"], False)
        self.assertIs(kwargs["text"], False)
        self.assertIs(kwargs["stdout"], subprocess.PIPE)


if __name__ == "__main__":
    unittest.main()
