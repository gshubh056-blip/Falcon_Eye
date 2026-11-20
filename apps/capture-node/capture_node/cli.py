import argparse
import json
import os
import sys
from pathlib import Path

from .drivers.base import CaptureSourceError, FrameSource, OpenCVFrameSource
from .drivers.file import FileVideoSource
from .drivers.phone import PhoneStreamSource


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read timestamped frames from a local camera or demo video."
    )
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--video", type=Path, help="Local video file to replay.")
    source_group.add_argument(
        "--phone-stream",
        action="store_true",
        help="Read FALCON_PHONE_STREAM_URL from the environment.",
    )
    source_group.add_argument(
        "--device-index",
        type=int,
        help="Open a local OpenCV camera device, commonly index 0.",
    )
    parser.add_argument("--camera-id", required=True)
    parser.add_argument("--max-frames", type=int)
    return parser


def _create_source(args: argparse.Namespace) -> FrameSource:
    if args.max_frames is not None and args.max_frames < 1:
        raise ValueError("--max-frames must be greater than zero.")
    if args.video is not None:
        return FileVideoSource(args.video, args.camera_id)
    if args.phone_stream:
        url = os.environ.get("FALCON_PHONE_STREAM_URL")
        if not url:
            raise ValueError("FALCON_PHONE_STREAM_URL is required for --phone-stream.")
        return PhoneStreamSource(url, args.camera_id)
    if args.device_index is not None:
        if args.device_index < 0:
            raise ValueError("--device-index must not be negative.")
        return OpenCVFrameSource(args.device_index, args.camera_id)
    raise ValueError("A video source must be selected.")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        source = _create_source(args)
        source_kind = (
            "file"
            if args.video is not None
            else "phone_stream"
            if args.phone_stream
            else "camera_device"
        )
        with source:
            frame_count = 0
            while args.max_frames is None or frame_count < args.max_frames:
                frame = source.read()
                if frame is None:
                    stream_failed = source_kind != "file"
                    print(
                        json.dumps(
                            {
                                "camera_id": args.camera_id,
                                "source_status": (
                                    "stream_read_failed" if stream_failed else "end_of_file"
                                ),
                                "frames_read": frame_count,
                            }
                        ),
                        flush=True,
                    )
                    return 1 if stream_failed or frame_count == 0 else 0
                print(
                    json.dumps(
                        {
                            "camera_id": frame.camera_id,
                            "frame_id": frame.frame_id,
                            "captured_at": frame.captured_at.isoformat(),
                            "monotonic_ns": frame.monotonic_ns,
                            "width": frame.width,
                            "height": frame.height,
                            "source_status": "frame_received",
                        }
                    ),
                    flush=True,
                )
                frame_count += 1
    except (CaptureSourceError, FileNotFoundError, ValueError) as exc:
        print(f"capture-source: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
