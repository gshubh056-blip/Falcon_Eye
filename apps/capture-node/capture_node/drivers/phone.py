from urllib.parse import urlsplit

from .base import CaptureSourceError, OpenCVFrameSource


class PhoneStreamSource(OpenCVFrameSource):
    def __init__(self, url: str, camera_id: str) -> None:
        try:
            parsed = urlsplit(url)
            valid_url = (
                parsed.scheme in {"http", "https"}
                and bool(parsed.hostname)
                and parsed.username is None
                and parsed.password is None
                and not parsed.query
                and not parsed.fragment
            )
        except ValueError:
            valid_url = False
        if not valid_url:
            raise CaptureSourceError(
                "Phone stream must be an HTTP(S) URL without embedded credentials or tokens."
            )
        super().__init__(url, camera_id)
