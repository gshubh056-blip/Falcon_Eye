from pathlib import Path

import cv2
import numpy as np
import pytest


@pytest.fixture
def synthetic_video(tmp_path: Path) -> Path:
    path = tmp_path / "synthetic.avi"
    writer = cv2.VideoWriter(
        str(path),
        cv2.VideoWriter_fourcc(*"MJPG"),
        5.0,
        (32, 24),
    )
    if not writer.isOpened():
        pytest.skip("OpenCV has no MJPG video writer in this environment.")
    try:
        for value in (20, 80, 140):
            image = np.full((24, 32, 3), value, dtype=np.uint8)
            writer.write(image)
    finally:
        writer.release()
    return path
