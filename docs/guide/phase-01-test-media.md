# Phase 01 - Test Media and Camera Simulator

## STEP 1.1 – [P0 MVP] Install FFmpeg and GStreamer
- **Goal:** The team can inspect, trim and publish test video on Windows or Linux.
- **Implements:** FR-001, FR-002, TR-ING-001.
- **Owner / Time:** CV/ML; 40 minutes.
- **Prerequisites:** Phase 0 complete.
- **Why this step:** FFmpeg prepares evidence and test clips, while GStreamer/OpenCV must read RTSP streams.
- **Do this (numbered micro-steps):**
  1. Install FFmpeg for Windows using a package manager or the official build; add `bin` to PATH.
  2. Install GStreamer runtime and development packages; add `bin` to PATH.
  3. Verify with PowerShell:
  ```powershell
  ffmpeg -version
  gst-launch-1.0 --version
  ```
  4. On Ubuntu:
  ```bash
  sudo apt-get update
  sudo apt-get install -y ffmpeg gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly
  ffmpeg -version
  gst-launch-1.0 --version
  ```
- **Expected result:** FFmpeg and GStreamer print version information.
- **Verify (must pass before continuing):**
  ```powershell
  ffmpeg -i test.mp4 -f null - 2>&1 | Select-String "Duration|Stream"
  ```
- **If it fails:** `ffmpeg not recognized`: reopen terminal after PATH update. `gst plugin missing`: install `gstreamer1.0-libav` on Linux or full Windows runtime plus development installer. DLL missing: install Visual C++ redistributable.
- **Git commit:** `git commit --allow-empty -m "chore: verify media toolchain"`
- **Done when:** FFmpeg and GStreamer decode a test file.

## STEP 1.2 – [P0 MVP] Collect legal test media
- **Goal:** Golden clips exist for day, night, fog/rain, vehicles, plates and fences.
- **Implements:** TST-001, TST-005.
- **Owner / Time:** CV/ML and Docs; 120 minutes.
- **Prerequisites:** Step 1.1.
- **Why this step:** Golden clips give repeatable ground truth and prevent model demos from being irreproducible.
- **Do this (numbered micro-steps):**
  1. Create `datasets/golden`.
  2. Only use public-domain/CC clips or videos recorded by the team with consent.
  3. Record a clip under each scenario: day person, day vehicle, fence crossing, night, rain/fog, plate and loitering.
  4. Create `datasets/golden/manifest.json`:
  ```json
  {
    "clips": [
      {"clip_id":"day-person-01","source":"team-recorded","license":"team-consent","fps":25,"duration_seconds":30,"expected_events":["person","vehicle"]},
      {"clip_id":"fence-cross-01","source":"team-recorded","license":"team-consent","fps":25,"duration_seconds":30,"expected_events":["virtual_fence"]}
    ]
  }
  ```
- **Expected result:** Each clip has source and licence metadata.
- **Verify (must pass before continuing):**
  ```powershell
  Get-ChildItem datasets/golden -Recurse
  ```
- **If it fails:** Unknown license: remove the clip. Privacy concern: blur identities and obtain consent. Corrupted MP4: re-export with FFmpeg.
- **Git commit:** `git add datasets/golden/manifest.json && git commit -m "test: add golden clip manifest"`
- **Done when:** Every clip has an entry, source and license.

## STEP 1.3 – [P0 MVP] Run MediaMTX
- **Goal:** A looped video is available as RTSP and HLS for every team member.
- **Implements:** FR-001, FR-002, TR-ING-001.
- **Owner / Time:** DevOps; 45 minutes.
- **Prerequisites:** FFmpeg, Docker Desktop.
- **Why this step:** MediaMTX makes a fake camera behave like a real RTSP source.
- **Do this (numbered micro-steps):**
  1. Create `deploy/docker-compose/compose.media.yaml`:
  ```yaml
  services:
    mediamtx:
      image: bluenviron/mediamtx:latest
      ports:
        - "8554:8554"
        - "8888:8888"
        - "8889:8889"
      volumes:
        - ./mediamtx.yml:/mediamtx.yml:ro
  ```
  2. Create `deploy/docker-compose/mediamtx.yml`:
  ```yaml
  rtsp: yes
  rtspAddress: :8554
  hls: yes
  hlsAddress: :8888
  webRTC: yes
  webrtcAddress: :8889
  paths:
    falcon:
      source: publisher
  ```
  3. Start MediaMTX:
  ```powershell
  cd deploy/docker-compose
  docker compose -f compose.media.yaml up -d
  ```
  4. Publish a loop:
  ```powershell
  ffmpeg -stream_loop -1 -re -i ../../datasets/golden/day-person-01.mp4 -c copy -f rtsp rtsp://localhost:8554/falcon
  ```
- **Expected result:** FFmpeg connects and prints frame statistics.
- **Verify (must pass before continuing):**
  ```powershell
  ffprobe -rtsp_transport tcp -show_entries format=duration -of default=nw=1 rtsp://localhost:8554/falcon
  curl http://localhost:8888/falcon/index.m3u8
  ```
- **If it fails:** `bind port`: stop another MediaMTX container. `connection refused`: wait for container startup. VLC cannot H264: MediaMTX is up but VLC codec support is missing.
- **Git commit:** `git add deploy/docker-compose/compose.media.yaml deploy/docker-compose/mediamtx.yml && git commit -m "feat: add MediaMTX demo simulator"`
- **Done when:** RTSP and HLS URLs return data.

## STEP 1.4 – [P0 MVP] Read RTSP from OpenCV
- **Goal:** A Python test reads the simulated stream at a stable FPS.
- **Implements:** FR-002, FR-005, TR-ING-001.
- **Owner / Time:** CV/ML; 30 minutes.
- **Prerequisites:** Step 1.3.
- **Why this step:** OpenCV fallback confirms that the capture contract works outside GStreamer.
- **Do this (numbered micro-steps):**
  1. Create `scripts/test_rtsp.py`:
  ```python
  """Read and display frames from an RTSP source."""
  import cv2

  def main() -> None:
      capture = cv2.VideoCapture("rtsp://localhost:8554/falcon")
      capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
      if not capture.isOpened():
          raise RuntimeError("Could not open RTSP stream")
      for frame_number in range(100):
          ok, frame = capture.read()
          if not ok:
              raise RuntimeError(f"Frame read failed at {frame_number}")
      print("Read 100 RTSP frames")
      capture.release()

  if __name__ == "__main__":
      main()
  ```
  2. Install the first pinned package set:
  ```powershell
  py -3.12 -m pip install opencv-python-headless==4.10.0.84
  py -3.12 scripts/test_rtsp.py
  ```
- **Expected result:** Terminal prints `Read 100 RTSP frames`.
- **Verify (must pass before continuing):**
  ```powershell
  py -3.12 scripts/test_rtsp.py
  ```
- **If it fails:** `Could not open`: verify MediaMTX and FFmpeg publisher. `latency`: set OpenCV TCP transport or use GStreamer next.
- **Git commit:** `git add scripts/test_rtsp.py && git commit -m "test: verify RTSP frame capture"`
- **Done when:** 100 consecutive frames decode without failure.

## Phase checklist
- [ ] FFmpeg and GStreamer are installed.
- [ ] Legal golden clips exist.
- [ ] MediaMTX exposes RTSP and HLS.
- [ ] OpenCV reads 100 frames.

## Phase demo
Open VLC at `rtsp://localhost:8554/falcon`, open HLS in browser, and show the same loop in the Python read test.

## Rollback
Stop MediaMTX with `docker compose -f compose.media.yaml down`. Remove test media only if it is not licensed for the project.

## Time summary
Phase 1 takes approximately 235 minutes, split across CV/ML and DevOps.
