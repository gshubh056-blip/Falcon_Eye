from __future__ import annotations

import time
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol, Self

import cv2
import numpy as np


class CaptureSourceError(RuntimeError):
    """Raised when a video source cannot provide valid frames."""


@dataclass(frozen=True, slots=True)
class CaptureFrame:
    camera_id: str
    frame_id: int
    captured_at: datetime
    monotonic_ns: int
    width: int
    height: int
    image_bgr: np.ndarray


class FrameSource(Protocol):
    def read(self) -> CaptureFrame | None: ...

    def frames(self) -> Iterator[CaptureFrame]: ...

    def close(self) -> None: ...

    def __enter__(self) -> Self: ...

    def __exit__(self, *_: object) -> None: ...


class _VideoCapture(Protocol):
    def isOpened(self) -> bool: ...

    def read(self) -> tuple[bool, np.ndarray]: ...

    def release(self) -> None: ...


class OpenCVFrameSource:
    def __init__(self, source: str | int, camera_id: str) -> None:
        if not camera_id.strip():
            raise ValueError("camera_id must not be blank.")
        self._camera_id = camera_id
        self._capture: _VideoCapture = cv2.VideoCapture(source)
        self._closed = False
        self._next_frame_id = 0
        if not self._capture.isOpened():
            self._capture.release()
            self._closed = True
            raise CaptureSourceError("Unable to open the configured video source.")

    def read(self) -> CaptureFrame | None:
        if self._closed:
            raise CaptureSourceError("The video source is closed.")

        success, image = self._capture.read()
        if not success:
            return None
        if not isinstance(image, np.ndarray) or image.ndim != 3 or image.shape[2] != 3:
            raise CaptureSourceError("The video source returned an invalid BGR frame.")

        height, width = image.shape[:2]
        if width <= 0 or height <= 0:
            raise CaptureSourceError("The video source returned an empty frame.")

        packet = CaptureFrame(
            camera_id=self._camera_id,
            frame_id=self._next_frame_id,
            captured_at=datetime.now(UTC),
            monotonic_ns=time.monotonic_ns(),
            width=width,
            height=height,
            image_bgr=image,
        )
        self._next_frame_id += 1
        return packet

    def frames(self) -> Iterator[CaptureFrame]:
        while (frame := self.read()) is not None:
            yield frame

    def close(self) -> None:
        if not self._closed:
            self._capture.release()
            self._closed = True

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
