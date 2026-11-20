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
| Browser/USB enumerated camera | OS media device through `getUserMedia` | Demo preview and COCO-SSD person counting implemented | Requires browser permission and a named tested device; results are demo-only and not a production benchmark. |
| Phone HTTP stream | Browser `<video>` URL or capture adapter | HTTP URL supported by the demo UI; physical compatibility depends on the stream format | Credentials/tokens embedded in the URL are rejected; HTTPS mixed-content restrictions apply. |
| Local video file | Browser Blob URL | Supported for replay/demo | File stays local and is not uploaded by the browser preview. |
| RTSP CCTV/NVR | RTSP through capture/relay adapter | Not implemented in the browser | Requires an edge RTSP adapter and MediaMTX or equivalent relay; no universal compatibility claim. |
| ONVIF CCTV | ONVIF discovery/PTZ plus edge capture | Not implemented | Requires tested device profiles, authentication, and an adapter. |

The browser motion overlay compares adjacent low-resolution frames and can react
to lighting changes, camera shake, or ordinary movement. TensorFlow COCO-SSD
provides a demo person count and boxes only; it is not an approved production
detector or a person/vehicle accuracy claim. The licensed model, weights,
training-data provenance, benchmark, and registry gate remains in force.

The current capture CLI is a local development tool. Browser access must remain
behind explicit camera permission and authenticated operator access; do not
expose a camera feed publicly.
