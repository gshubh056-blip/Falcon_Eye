# Phase 02 - Walking Skeleton

## STEP 2.1 – [P0 MVP] Create the Python virtual environment
- **Goal:** A repeatable CPU-only Python environment exists.
- **Implements:** TRD Section 2.
- **Owner / Time:** CV/ML; 20 minutes.
- **Prerequisites:** Phase 0 and Python 3.12.
- **Why this step:** A virtual environment keeps YOLO and OpenCV packages out of global Python.
- **Do this (numbered micro-steps):**
  1. Enter the project:
  ```powershell
  cd C:\Users\<user>\OneDrive\Pictures\OneDrive\Desktop\Falcon_Eye
  py -3.12 -m venv .venv
  .\.venv\Scripts\Activate.ps1
  python --version
  python -m pip install --upgrade pip
  ```
  ```bash
  cd /path/to/Falcon_Eye
  python3.12 -m venv .venv
  source .venv/bin/activate
  python --version
  python -m pip install --upgrade pip
  ```
  2. Create `requirements.txt` with pinned CPU package baseline:
  ```text
  opencv-python-headless==4.10.0.84
  numpy==2.1.1
  ultralytics==8.3.23
  pydantic==2.9.2
  pydantic-settings==2.5.2
  PyYAML==6.0.2
  pytest==8.3.3
  ruff==0.6.9
  black==24.8.0
  mypy==1.11.2
  structlog==24.4.0
  ```
  3. Install:
  ```powershell
  python -m pip install -r requirements.txt
  ```
- **Expected result:** `pip check` reports no broken requirements.
- **Verify (must pass before continuing):**
  ```powershell
  python -c "import cv2, ultralytics, numpy; print(cv2.__version__)"
  python -m pip check
  ```
- **If it fails:** NumPy/OpenCV conflict: recreate `.venv` and install exact requirements. PyTorch download timeout: rerun with network; do not use GPU packages for CPU baseline.
- **Git commit:** `git add requirements.txt && git commit -m "chore: add pinned CPU Python environment"`
- **Done when:** The environment imports CV2, Ultralytics and NumPy and `pip check` passes.

## STEP 2.2 – [P0 MVP] Add shared configuration
- **Goal:** Capture and detector settings come from YAML and environment variables.
- **Implements:** TR-ING-001, TR-DET-001.
- **Owner / Time:** Backend/DB; 30 minutes.
- **Prerequisites:** Step 2.1.
- **Why this step:** Configuration avoids hard-coded RTSP URLs and model thresholds.
- **Do this (numbered micro-steps):**
  1. Create `deploy/config/falcon-demo.yaml`:
  ```yaml
  environment: demo
  capture:
    transport: tcp
    reconnect_initial_seconds: 2
    reconnect_max_seconds: 30
  detection:
    model: yolov8n.pt
    input_size: 640
    confidence: 0.40
    nms_iou: 0.55
    analytics_fps: 12
  ```
  2. Create `apps/capture-node/config.py`:
  ```python
  """Load demo configuration for capture and detection."""
  from pathlib import Path
  import yaml
  from pydantic_settings import BaseSettings

  class Settings(BaseSettings):
      falcon_env: str = "demo"
      rtsp_url: str = "rtsp://localhost:8554/falcon"
      model_dir: str = "./models/registry"

  def load_yaml(path: str = "deploy/config/falcon-demo.yaml") -> dict:
      config_path = Path(path)
      if not config_path.exists():
          raise FileNotFoundError(config_path)
      with config_path.open("r", encoding="utf-8") as handle:
          return yaml.safe_load(handle)
  ```
- **Expected result:** Importing `config.py` loads YAML without exceptions.
- **Verify (must pass before continuing):**
  ```powershell
  python -c "from apps.capture_node.config import load_yaml; print(load_yaml()['environment'])"
  ```
- **If it fails:** Python hyphen module import: use Python package folders with underscores; Step 2.3 normalizes paths.
- **Git commit:** `git add deploy/config apps/capture-node/config.py && git commit -m "feat: add shared demo configuration"`
- **Done when:** Settings and YAML load in both local environments.

## STEP 2.3 – [P0 MVP] Implement StreamReader
- **Goal:** One reusable reader opens and reconnects to an RTSP stream.
- **Implements:** FR-002, FR-005, FR-006.
- **Owner / Time:** CV/ML; 60 minutes.
- **Prerequisites:** Step 2.2.
- **Why this step:** The reconnect reader protects the pipeline from temporary camera outages.
- **Do this (numbered micro-steps):**
  1. Rename package folders to valid Python names using hyphens only for directories? Create `apps/capture_node/capture.py`.
  2. Create complete file:
  ```python
  """RTSP stream reader with bounded exponential reconnect."""
  import logging
  import time
  import cv2
  import numpy as np

  logger = logging.getLogger(__name__)

  class StreamReader:
      def __init__(self, url: str, initial: float = 2.0, maximum: float = 30.0) -> None:
          self.url = url
          self.initial = initial
          self.maximum = maximum

      def open(self) -> cv2.VideoCapture:
          delay = self.initial
          while True:
              capture = cv2.VideoCapture(self.url, cv2.CAP_FFMPEG)
              capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
              if capture.isOpened():
                  logger.info("Stream connected", extra={"url": self.url})
                  return capture
              capture.release()
              logger.warning("Stream unavailable", extra={"delay_seconds": delay})
              time.sleep(delay)
              delay = min(delay * 2, self.maximum)

      def read(self, capture: cv2.VideoCapture) -> tuple[bool, np.ndarray | None]:
          return capture.read()
  ```
  3. Add `apps/capture_node/__init__.py`:
  ```python
  """FALCON capture package."""
  ```
- **Expected result:** Reader reconnect loop can be imported and constructed.
- **Verify (must pass before continuing):**
  ```powershell
  python -c "from apps.capture_node.capture import StreamReader; print(StreamReader('rtsp://localhost:8554/falcon').url)"
  ```
- **If it fails:** OpenCV FFMPEG backend missing: reinstall `opencv-python-headless` with network access. Infinite reconnect in unit test: inject URL and close MediaMTX.
- **Git commit:** `git add apps/capture_node && git commit -m "feat: add reconnecting RTSP reader"`
- **Done when:** An unavailable stream raises no process exit and retries until it connects.

## STEP 2.4 – [P0 MVP] Implement CPU YOLO detector
- **Goal:** A frame produces person/vehicle detection boxes on CPU.
- **Implements:** FR-010, FR-013, TR-DET-001.
- **Owner / Time:** CV/ML; 60 minutes.
- **Prerequisites:** Step 2.3.
- **Why this step:** The detector is the first AI capability and establishes the shared output contract.
- **Do this (numbered micro-steps):**
  1. Create `apps/inference_service/detector.py`:
  ```python
  """CPU-first Ultralytics person and vehicle detector."""
  import logging
  import cv2
  import numpy as np
  from ultralytics import YOLO

  logger = logging.getLogger(__name__)
  ALLOWED = {0: "person", 2: "car", 5: "bus", 7: "truck"}

  class Detector:
      def __init__(self, model_path: str = "yolov8n.pt", confidence: float = 0.40) -> None:
          self.model = YOLO(model_path)
          self.confidence = confidence

      def infer(self, frame: np.ndarray) -> list[dict]:
          result = self.model.predict(frame, conf=self.confidence, imgsz=640, verbose=False)[0]
          detections: list[dict] = []
          for box in result.boxes:
              class_id = int(box.cls[0])
              if class_id not in ALLOWED:
                  continue
              x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().tolist()
              detections.append({"class": ALLOWED[class_id], "confidence": float(box.conf[0]), "bbox_xyxy": [x1, y1, x2, y2]})
          return detections
  ```
  2. Download pretrained weight only after license review:
  ```powershell
  New-Item -ItemType Directory -Force models/registry | Out-Null
  python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
  Copy-Item yolov8n.pt models/registry/yolov8n.pt
  ```
- **Expected result:** YOLO prints detections for a person/vehicle test frame.
- **Verify (must pass before continuing):**
  ```powershell
  python -c "from apps.inference_service.detector import Detector; import cv2; d=Detector('models/registry/yolov8n.pt'); print(d.infer(cv2.imread('datasets/golden/day-person-01.jpg')))"
  ```
- **If it fails:** License concern: stop and run Ultralytics/alternative license review. Missing weight: download in approved environment. Person/vehicle missed: lower confidence only in demo config to 0.30 and record baseline.
- **Git commit:** `git add apps/inference_service models/registry && git commit -m "feat: add CPU person vehicle detector"`
- **Done when:** At least one detection is emitted from the golden image.

## STEP 2.5 – [P0 MVP] Add FPS and stage latency logging
- **Goal:** The walking skeleton reports FPS and stage timings.
- **Implements:** NFR-001, NFR-002.
- **Owner / Time:** CV/ML; 45 minutes.
- **Prerequisites:** Step 2.4.
- **Why this step:** Timing evidence distinguishes a slow pipeline from a broken pipeline.
- **Do this (micro-steps):**
  1. Create `apps/inference_service/run_demo.py` that reads 300 frames, draws boxes, prints JSON summary, and logs no personal data.
  2. Use `time.perf_counter()` around capture, preprocessing, inference and draw.
  3. Run against MediaMTX.
- **Expected result:** Console displays FPS and P50/P95 capture, inference and draw latency.
- **Verify:**
  ```powershell
  python apps/inference_service/run_demo.py --source rtsp://localhost:8554/falcon --frames 300
  ```
- **If it fails:** Zero FPS: wait for stream publisher. Missing P95: use at least 100 frames. GPU not found: stay CPU-only.
- **Git commit:** `git add apps/inference_service/run_demo.py && git commit -m "perf: add skeleton latency measurement"`
- **Done when:** One 300-frame run reports capture, infer and FPS values.

## STEP 2.6 – [P0 MVP] Store one test event
- **Goal:** A first detection run creates `events` and `detections` test records.
- **Implements:** FR-080, DB-001.
- **Owner / Time:** Backend/DB; 45 minutes.
- **Prerequisites:** PostgreSQL from Phase 0.
- **Why this step:** M0 proves video output reaches persistent data.
- **Do this (micro-steps):**
  1. Install `psycopg[binary]`.
  2. Create `scripts/write_test_event.py` using `DATABASE_URL` and parameterized SQL.
  3. Insert one event and detection.
- **Expected result:** SQL query shows one event and one detection.
- **Verify:**
  ```powershell
  python scripts/write_test_event.py
  docker exec falcon-postgres-1 psql -U falcon -d falcon -c "select category,count(*) from events group by category;"
  ```
- **If it fails:** Database no events table: proceed to Phase 4 migration before continuing.
- **Git commit:** `git add scripts/write_test_event.py && git commit -m "feat: add skeleton event writer"`
- **Done when:** A detection run can write one database record.

## Phase checklist
- [ ] CPU virtual environment works.
- [ ] YAML and environment settings load.
- [ ] RTSP reconnect reader works.
- [ ] YOLO produces boxes.
- [ ] FPS and latency are logged.
- [ ] M0 is demonstrated.

## Phase demo
Show RTSP stream, green/red detection boxes, FPS, and one database event.

## Rollback
Stop the demo script with Ctrl+C, remove generated weights not approved, and restore the previous detector config.

## Time summary
Phase 2 takes approximately 260 minutes.
