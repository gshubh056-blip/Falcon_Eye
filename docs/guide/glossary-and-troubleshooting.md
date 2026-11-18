# Glossary and Troubleshooting

## Glossary

| Term | Meaning |
|---|---|
| Alembic | Python database migration tool |
| ANPR | Automatic Number Plate Recognition |
| bbox | Bounding box represented as x1/y1/x2/y2 |
| ByteTrack | Lightweight multi-object tracking algorithm |
| Docker Compose | Tool that starts multiple containers from one YAML file |
| Ed25519 | Digital signature algorithm used for evidence signing |
| FAISS | Vector similarity search library |
| GStreamer | Multimedia streaming pipeline framework |
| HLS | HTTP Live Streaming used by the browser |
| hypertable | TimescaleDB table partitioned by time |
| IoU | Intersection over Union, used to compare detections |
| MediaMTX | Local RTSP/HLS/WebRTC media server |
| MinIO | S3-compatible local object store |
| MQTT | Lightweight publish/subscribe messaging protocol |
| ONVIF | Standard for discovering/configuring IP cameras |
| ONNX | Portable neural-network model format |
| RTSP | Real-Time Streaming Protocol for live IP-camera video |
| SHA-256 | Cryptographic 256-bit hash function |
| TensorRT | NVIDIA TensorRT inference runtime |
| TimescaleDB | PostgreSQL extension for time-series data |
| WebRTC | Real-time browser video transport |
| XAI | Explainable AI: a human-readable reason for a result |

## Troubleshooting Matrix

| Symptom | Likely cause | Fix |
|---|---|---|
| `docker is not recognized` | Docker Desktop not installed or PATH not refreshed | Install Docker Desktop, enable WSL2, reopen terminal |
| `Cannot connect to RTSP` | Wrong transport, URL, port or credentials | Use `rtsp://` TCP URL and VLC/FFprobe test |
| `Could not open port 5432` | Existing PostgreSQL container or local service | Stop conflicting service or change Compose port |
| `ModuleNotFoundError` | Virtual environment not active | Activate `.venv` and reinstall from pinned requirements |
| `No matching YOLO model` | Package downloaded no internet or wrong filename | Place approved weight under `models/registry` |
| `CUDA out of memory` | Optional GPU overbooked | Use CPU or lower input size |
| `Object Store not ready` | MinIO container started before health check | Wait 20 seconds and run health endpoint |
| `MFA unavailable` | Demo key or issuer not configured | Use TOTP seed only in local demo and not Git |

## Stuck Protocol

Use the stuck prompt from `docs/guide/README.md`. Include the full error, OS, Python version, exact command, STEP ID, and relevant file paths. Do not paste secrets or private RTSP passwords.
