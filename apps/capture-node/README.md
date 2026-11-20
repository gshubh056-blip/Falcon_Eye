# Capture node

The current capture increment decodes BGR frames from a local video file, a
local OpenCV camera device, or an optional HTTP(S) phone stream. Each frame has
a camera ID, sequential frame ID, UTC timestamp, monotonic timestamp, and image
dimensions. It does not perform object detection or claim a connected camera
until that source returns frames.

Run from the repository root in PowerShell:

```powershell
uv run --directory apps/capture-node python -m capture_node.cli `
  --video "C:\path\to\approved-demo-video.mp4" `
  --camera-id demo-file-camera `
  --max-frames 20
```

For a local camera, use `--device-index 0`. For a phone stream, set
`$env:FALCON_PHONE_STREAM_URL` to a local HTTP(S) video URL and pass
`--phone-stream`; URL credentials and query tokens are deliberately rejected
so they cannot leak through process arguments or logs. Stream compatibility
must be tested on the named device before it is claimed.

The JSON output is frame-receipt metadata only. Person/vehicle detections remain
unavailable until the approved model/license gate is satisfied and the detector
adapter is implemented.

