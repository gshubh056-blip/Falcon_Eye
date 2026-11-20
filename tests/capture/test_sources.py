from datetime import UTC
from pathlib import Path

import cv2
import numpy as np
import pytest
from capture_node.drivers.base import CaptureSourceError, OpenCVFrameSource
from capture_node.drivers.file import FileVideoSource
from capture_node.drivers.phone import PhoneStreamSource


def test_file_video_source_emits_ordered_timestamped_bgr_frames(
    synthetic_video: Path,
) -> None:
    with FileVideoSource(synthetic_video, "synthetic-camera") as source:
        frames = list(source.frames())

    assert [frame.frame_id for frame in frames] == [0, 1, 2]
    assert all(frame.camera_id == "synthetic-camera" for frame in frames)
    assert all(
        (frame.width, frame.height, frame.image_bgr.shape) == (32, 24, (24, 32, 3))
        for frame in frames
    )
    assert all(frame.captured_at.tzinfo == UTC for frame in frames)
    assert all(
        earlier.monotonic_ns <= later.monotonic_ns
        for earlier, later in zip(frames, frames[1:], strict=False)
    )


def test_file_source_reports_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Video file does not exist"):
        FileVideoSource(tmp_path / "missing.avi", "camera-1")


def test_source_rejects_read_after_close(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeCapture:
        def isOpened(self) -> bool:
            return True

        def read(self) -> tuple[bool, np.ndarray]:
            return False, np.empty((0, 0, 3), dtype=np.uint8)

        def release(self) -> None:
            pass

    monkeypatch.setattr(cv2, "VideoCapture", lambda _source: FakeCapture())
    source = OpenCVFrameSource(0, "camera-1")
    source.close()

    with pytest.raises(CaptureSourceError, match="closed"):
        source.read()


@pytest.mark.parametrize(
    "url",
    (
        "rtsp://192.0.2.1/live",
        "http://user:pass@192.0.2.1/live",
        "http://192.0.2.1/live?token=secret",
        "not-a-url",
    ),
)
def test_phone_source_rejects_unsupported_or_credentialed_urls(url: str) -> None:
    with pytest.raises(CaptureSourceError, match="HTTP"):
        PhoneStreamSource(url, "phone-camera")


def test_phone_source_uses_http_stream_without_logging_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeCapture:
        def __init__(self) -> None:
            self.reads: list[tuple[bool, np.ndarray]] = [
                (True, np.zeros((24, 32, 3), dtype=np.uint8)),
                (False, np.empty((0, 0, 3), dtype=np.uint8)),
            ]

        def isOpened(self) -> bool:
            return True

        def read(self) -> tuple[bool, np.ndarray]:
            return self.reads[0]

        def release(self) -> None:
            pass

    fake_capture = FakeCapture()
    urls: list[str | int] = []

    def create_capture(source: str | int) -> FakeCapture:
        urls.append(source)
        return fake_capture

    monkeypatch.setattr(cv2, "VideoCapture", create_capture)
    source = PhoneStreamSource("http://192.0.2.10:8080/video", "phone-camera")

    frame = source.read()
    source.close()

    assert urls == ["http://192.0.2.10:8080/video"]
    assert frame is not None
    assert frame.camera_id == "phone-camera"
    assert (frame.width, frame.height) == (32, 24)
