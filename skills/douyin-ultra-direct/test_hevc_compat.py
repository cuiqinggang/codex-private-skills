import hashlib, pathlib, tempfile, unittest
from unittest.mock import patch
import run

class CompatibilityRegression(unittest.TestCase):
    def test_h264_bypass(self):
        probe = dict(video="h264", audio="aac", duration=50.5, width=1080, height=1920)
        with patch.object(run, "ffprobe", return_value=probe), patch.object(run.subprocess, "run") as process:
            self.assertEqual(run.compatible_mp4(pathlib.Path("existing.mp4")), probe)
            process.assert_not_called()

    def test_encoder_failure_preserves_source(self):
        with tempfile.TemporaryDirectory() as folder:
            source = pathlib.Path(folder) / "source.part"
            source.write_bytes(b"original")
            probe = dict(video="hevc", audio="aac", duration=50.5, width=1080, height=1920)
            failure = run.subprocess.CompletedProcess([], 1, "", "encoder failure")
            with patch.object(run, "ffprobe", return_value=probe), patch.object(run.subprocess, "run", return_value=failure) as process:
                with self.assertRaisesRegex(RuntimeError, "HEVC_COMPATIBILITY_FAILED"):
                    run.compatible_mp4(source)
                self.assertEqual(process.call_count, 2)
                self.assertEqual(source.read_bytes(), b"original")

    def test_duration_mismatch_preserves_source(self):
        with tempfile.TemporaryDirectory() as folder:
            source = pathlib.Path(folder) / "source.part"
            source.write_bytes(b"original")
            before = dict(video="hevc", audio="aac", duration=50.5, width=1080, height=1920)
            after = dict(before, video="h264", duration=30)
            with patch.object(run, "ffprobe", side_effect=[before, after, after]), patch.object(run.subprocess, "run", return_value=run.subprocess.CompletedProcess([], 0, "", "")):
                with self.assertRaisesRegex(RuntimeError, "TRANSCODE_DURATION_MISMATCH"):
                    run.compatible_mp4(source)
                self.assertEqual(source.read_bytes(), b"original")

if __name__ == "__main__":
    unittest.main()
