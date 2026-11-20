from pathlib import Path

from .base import OpenCVFrameSource


class FileVideoSource(OpenCVFrameSource):
    def __init__(self, path: str | Path, camera_id: str) -> None:
        video_path = Path(path).expanduser()
        if not video_path.is_file():
            raise FileNotFoundError(f"Video file does not exist: {video_path}")
        super().__init__(str(video_path), camera_id)
