# Camera compatibility

Compatibility is reported per named device and source type; the project does
not claim that every camera is supported. Capture validation below does not
validate object detection or analytics performance.

| Source/device | Transport/format | Result | Evidence / limitation |
|---|---|---|---|
| Laptop `720p HD Camera` | OpenCV device index 0; decoded BGR | Tested 2026-11-19 | Three frames captured at 640x480; metadata only, no frames saved or sent |
| Generated test video | MJPG AVI | Tested 2026-11-19 | Synthetic 32x24 fixture verifies frame shape, timestamp and sequence |
| Phone stream | HTTP(S) | Adapter fixture-tested | Fake capture backend only; no physical phone stream tested |
| Phone connected as laptop camera | OS camera device | Not tested | Use the OpenCV device index exposed by Windows |
| RTSP camera / NVR | RTSP | Not implemented | F2-02 pending; no device/profile compatibility claim |
| ONVIF camera | Discovery/PTZ | Not implemented | F2-02 pending; no discovery, authentication or PTZ claim |
| Browser camera (`getUserMedia`) | Local browser permission and media stream | Preview and local pixel-motion demo implemented; hardware verification pending | Frames stay in the tab; motion regions are not person/vehicle detections and are not sent to the API. No browser-to-capture transport or public camera endpoint exists. |

The browser motion overlay compares adjacent low-resolution frames and can react
to lighting changes, camera shake, or ordinary movement. Its local activity list
is a demonstration aid, not a security alert or object detector. It must not be
used to claim person/vehicle accuracy; the approved model, weights, and dataset
provenance gate remains in force.

The current capture CLI is a local development tool. Browser access must remain
behind explicit camera permission and authenticated operator access; do not
expose a camera feed publicly.
