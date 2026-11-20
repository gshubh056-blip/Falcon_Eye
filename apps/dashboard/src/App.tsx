import { useEffect, useRef, useState } from "react";
import * as cocoSsd from "@tensorflow-models/coco-ssd";
import "@tensorflow/tfjs";
import { alertIdFromHash, routeFromHash, routes } from "./routes";
import { findMotionRegions, type MotionRegion } from "./motionDetection";

type Alert = {
  id: string;
  severity: "info" | "low" | "medium" | "high" | "critical";
  status: "new" | "acknowledged" | "escalated" | "resolved" | "false_positive";
  title: string;
  description: string;
  created_at: string;
  camera_id?: string;
  event_id?: string;
  escalation_level?: number;
  false_positive_reason?: string | null;
};

type Camera = {
  id: string;
  name: string;
  status: string;
  protocol: string;
  camera_type: string;
  label: string;
};

type EventRecord = {
  id: string;
  camera_id: string;
  event_type: string;
  confidence: number;
  created_at: string;
  label: string;
};

type Device = {
  id: string;
  hostname: string;
  status: string;
  software_version: string;
  last_seen: string;
};

type DetectionRecord = {
  id: string;
  camera_id: string;
  detected_at: string;
  model_id: string;
  model_version: string;
  detections: Array<{
    label: string;
    confidence: number;
    x: number;
    y: number;
    width: number;
    height: number;
  }>;
  person_count: number;
  vehicle_count: number;
};

async function fetchJson<T>(path: string): Promise<T> {
  const response = await fetch(`http://127.0.0.1:8000${path}`);
  if (!response.ok) throw new Error(`Request failed: ${response.status}`);
  return response.json() as Promise<T>;
}

export function App() {
  const [route, setRoute] = useState(routeFromHash(window.location.hash));
  const [selectedAlertId, setSelectedAlertId] = useState(alertIdFromHash(window.location.hash));
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [cameras, setCameras] = useState<Camera[]>([]);
  const [events, setEvents] = useState<EventRecord[]>([]);
  const [devices, setDevices] = useState<Device[]>([]);
  const [detections, setDetections] = useState<DetectionRecord[]>([]);
  const [apiStatus, setApiStatus] = useState("Connecting...");
  const [socketStatus, setSocketStatus] = useState("Disconnected");

  useEffect(() => {
    const onHashChange = () => {
      setRoute(routeFromHash(window.location.hash));
      setSelectedAlertId(alertIdFromHash(window.location.hash));
    };
    window.addEventListener("hashchange", onHashChange);
    return () => window.removeEventListener("hashchange", onHashChange);
  }, []);

  useEffect(() => {
    fetchJson<{ status: string; mode: string }>("/health")
      .then((health) => setApiStatus(`${health.status} · ${health.mode}`))
      .catch(() => setApiStatus("Unavailable"));

    fetchJson<{ items: Alert[] }>("/api/v1/alerts")
      .then((payload) => setAlerts(payload.items))
      .catch(() => setAlerts([]));

    fetchJson<{ items: Camera[] }>("/api/v1/cameras")
      .then((payload) => setCameras(payload.items))
      .catch(() => setCameras([]));

    fetchJson<{ items: EventRecord[] }>("/api/v1/events")
      .then((payload) => setEvents(payload.items))
      .catch(() => setEvents([]));

    fetchJson<{ items: Device[] }>("/api/v1/devices")
      .then((payload) => setDevices(payload.items))
      .catch(() => setDevices([]));

    const loadDetections = () => {
      fetchJson<{ items: DetectionRecord[] }>("/api/v1/detections")
        .then((payload) => setDetections(payload.items))
        .catch(() => setDetections([]));
    };
    loadDetections();
    const detectionInterval = window.setInterval(loadDetections, 2000);

    const socket = new WebSocket("ws://127.0.0.1:8000/ws/v1/operator");
    socket.onopen = () => setSocketStatus("Connected");
    socket.onclose = () => setSocketStatus("Disconnected");
    socket.onmessage = (event) => {
      const update = JSON.parse(event.data) as { label?: string };
      if (update.label) setSocketStatus(`Connected · ${update.label}`);
    };
    return () => {
      window.clearInterval(detectionInterval);
      socket.close();
    };
  }, []);

  const reloadAlerts = () => {
    fetchJson<{ items: Alert[] }>("/api/v1/alerts")
      .then((payload) => setAlerts(payload.items))
      .catch(() => setAlerts([]));
  };

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <img className="brand" src="/brand/falcon-wordmark.svg" alt="FALCON EYE" />
        <nav aria-label="Primary navigation">
          {routes.map(([key, label]) => (
            <a
              key={key}
              className={route === key ? "nav-link active" : "nav-link"}
              href={`#/${key}`}
            >
              {label}
              {key === "alerts" && <span className="count">{alerts.length}</span>}
            </a>
          ))}
        </nav>
        <div className="user-card">
          <span className="avatar">OP</span>
          <div>
            <strong>Demo Operator</strong>
            <small>Authentication pending</small>
          </div>
        </div>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <div>
            <span className="eyebrow">DEMO BOP · LOCAL EDGE</span>
            <h1>{routes.find(([key]) => key === route)?.[1]}</h1>
          </div>
          <div className="status">
            <span>API: {apiStatus}</span>
            <span>Stream: {socketStatus}</span>
          </div>
        </header>

        {route === "live" && <LiveView />}
        {route === "alerts" && (
          <AlertsView
            alerts={alerts}
            selectedId={selectedAlertId}
            onReload={reloadAlerts}
          />
        )}
        {route === "cameras" && (
          <CamerasView cameras={cameras} detections={detections} />
        )}
        {route === "events" && <EventsView events={events} />}
        {route === "database" && <DatabaseView />}
        {route === "health" && <HealthView devices={devices} />}
        {route === "settings" && <SettingsView />}
      </section>
    </main>
  );
}

function LiveView() {
  return (
    <section className="page-grid live-grid">
      <div className="live-panel" aria-label="Live video placeholder">
        <div className="crosshair" />
        <p>LIVE WALL</p>
        <strong>NO CAMERA SOURCE CONNECTED</strong>
      </div>
      <aside className="right-panel">
        <h2>Unacknowledged alerts</h2>
        <div className="metric-grid">
          <Metric label="NEW" value="1" tone="high" />
          <Metric label="CAMERAS" value="1" tone="neutral" />
          <Metric label="ONLINE" value="0" tone="neutral" />
        </div>
        <div className="banner">All values are synthetic until a real integration is verified.</div>
      </aside>
    </section>
  );
}

function AlertsView({
  alerts,
  selectedId,
  onReload,
}: {
  alerts: Alert[];
  selectedId?: string;
  onReload: () => void;
}) {
  const [search, setSearch] = useState("");
  const [detail, setDetail] = useState<{
    item: Alert;
    actions: Array<{ action: string; previous_status: string; new_status: string; acted_at: string }>;
  } | null>(null);
  const [detailError, setDetailError] = useState("");
  const [mutationError, setMutationError] = useState("");
  const [reason, setReason] = useState("");

  useEffect(() => {
    if (!selectedId) {
      setDetail(null);
      return;
    }
    setDetailError("");
    fetchJson<{
      item: Alert;
      actions: Array<{ action: string; previous_status: string; new_status: string; acted_at: string }>;
    }>(`/api/v1/alerts/${selectedId}`)
      .then(setDetail)
      .catch((error: Error) => setDetailError(error.message));
  }, [selectedId]);

  const mutate = async (action: "acknowledge" | "escalate" | "resolve" | "false_positive") => {
    if (!selectedId) return;
    setMutationError("");
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/v1/alerts/${selectedId}/${action.replace("_", "-")}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            actor: "demo-operator",
            purpose: "Operator alert review",
            reason: action === "false_positive" ? reason : null,
            idempotency_key: crypto.randomUUID(),
          }),
        },
      );
      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.detail ?? "Mutation failed");
      }
      setDetail({ item: payload.item, actions: detail?.actions ?? [] });
      setReason("");
      onReload();
      const refreshed = await fetchJson<{
        item: Alert;
        actions: Array<{ action: string; previous_status: string; new_status: string; acted_at: string }>;
      }>(`/api/v1/alerts/${selectedId}`);
      setDetail(refreshed);
    } catch (error) {
      setMutationError(error instanceof Error ? error.message : "Mutation failed");
    }
  };

  const filtered = alerts.filter((alert) =>
    `${alert.title} ${alert.description} ${alert.status}`
      .toLowerCase()
      .includes(search.toLowerCase()),
  );

  if (selectedId) {
    return (
      <section className="page">
        <div className="toolbar">
          <div>
            <button className="text-button" onClick={() => { window.location.hash = "#/alerts"; }}>
              ← Alert inbox
            </button>
            <h2>Alert detail</h2>
          </div>
        </div>
        {detailError ? (
          <div className="error-state" role="alert">{detailError}</div>
        ) : !detail ? (
          <div className="empty-state" role="status">Loading alert...</div>
        ) : (
          <div className="detail-grid">
            <article className="detail-card">
              <span className={`severity-pill ${detail.item.severity}`}>{detail.item.severity}</span>
              <h3>{detail.item.title}</h3>
              <p>{detail.item.description}</p>
              <dl>
                <div><dt>Status</dt><dd>{detail.item.status}</dd></div>
                <div><dt>Camera</dt><dd>{detail.item.camera_id}</dd></div>
                <div><dt>Event</dt><dd>{detail.item.event_id}</dd></div>
                <div><dt>Escalation</dt><dd>{detail.item.escalation_level ?? 0}</dd></div>
              </dl>
              <div className="action-row">
                <button className="button" onClick={() => void mutate("acknowledge")} disabled={detail.item.status !== "new"}>
                  Acknowledge
                </button>
                <button className="button secondary" onClick={() => void mutate("escalate")} disabled={!["new", "acknowledged"].includes(detail.item.status)}>
                  Escalate
                </button>
                <button className="button secondary" onClick={() => void mutate("resolve")} disabled={["resolved", "false_positive"].includes(detail.item.status)}>
                  Resolve
                </button>
              </div>
              <label className="reason-field">
                False-positive reason
                <input
                  value={reason}
                  onChange={(event) => setReason(event.target.value)}
                  placeholder="Required reason"
                />
              </label>
              <button
                className="button danger"
                onClick={() => void mutate("false_positive")}
                disabled={reason.trim().length === 0 || ["resolved", "false_positive"].includes(detail.item.status)}
              >
                Mark false positive
              </button>
              {mutationError && <div className="error-state" role="alert">{mutationError}</div>}
            </article>
            <aside className="action-card">
              <h3>Action history</h3>
              {detail.actions.length === 0 ? (
                <p className="empty">No actions recorded.</p>
              ) : (
                detail.actions.map((action, index) => (
                  <article className="action-record" key={`${action.action}-${index}`}>
                    <strong>{action.action}</strong>
                    <span>{action.previous_status} → {action.new_status}</span>
                    <time>{action.acted_at}</time>
                  </article>
                ))
              )}
            </aside>
          </div>
        )}
      </section>
    );
  }

  return (
    <section className="page">
      <div className="toolbar">
        <div>
          <span className="section-label">TEST WORKFLOW</span>
          <h2>Alert inbox</h2>
        </div>
        <label className="search">
          <span>Search alerts</span>
          <input
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="/"
          />
        </label>
      </div>
      {filtered.length === 0 ? (
        <EmptyState text="No alerts received." />
      ) : (
        <div className="table-card">
          {filtered.map((alert) => (
            <article
              className="alert-row clickable"
              key={alert.id}
              role="button"
              tabIndex={0}
              onClick={() => { window.location.hash = `#/alerts/${alert.id}`; }}
              onKeyDown={(event) => {
                if (event.key === "Enter") window.location.hash = `#/alerts/${alert.id}`;
              }}
            >
              <span className={`severity-pill ${alert.severity}`}>{alert.severity}</span>
              <div>
                <h3>{alert.title}</h3>
                <p>{alert.description}</p>
              </div>
              <span className="state">{alert.status}</span>
              <time>{alert.created_at}</time>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}

function CamerasView({
  cameras,
  detections,
}: {
  cameras: Camera[];
  detections: DetectionRecord[];
}) {
  const latest = detections[0];
  return (
    <section className="page">
      <div className="toolbar">
        <div><span className="section-label">CONFIGURATION</span><h2>Cameras</h2></div>
        <button className="button secondary" disabled>ADD CAMERA</button>
      </div>
      <BrowserCameraPreview />
      <section className="detection-summary" aria-label="Detection database summary">
        <div>
          <span className="section-label">OBJECT DETECTION DATABASE</span>
          <strong>{latest ? latest.person_count : 0} people</strong>
          <span>{latest ? latest.vehicle_count : 0} vehicles</span>
        </div>
        <div>
          <strong>{detections.length} stored result{detections.length === 1 ? "" : "s"}</strong>
          <span>
            {latest
              ? `${latest.model_id} · ${latest.model_version}`
              : "No approved detector is connected"}
          </span>
        </div>
      </section>
      <div className="card-grid">
        {cameras.map((camera) => (
          <article className="asset-card" key={camera.id}>
            <span className="asset-status disconnected">{camera.status}</span>
            <h3>{camera.name}</h3>
            <dl>
              <div><dt>Protocol</dt><dd>{camera.protocol}</dd></div>
              <div><dt>Mode</dt><dd>{camera.camera_type}</dd></div>
              <div><dt>Source</dt><dd>{camera.label}</dd></div>
            </dl>
          </article>
        ))}
      </div>
    </section>
  );
}

function BrowserCameraPreview() {
  const motionFrameWidth = 160;
  const motionFrameHeight = 90;
  const videoRef = useRef<HTMLVideoElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const motionBaselineRef = useRef<Uint8ClampedArray | null>(null);
  const consecutiveMotionFramesRef = useRef(0);
  const lastMotionAlertAtRef = useRef(0);
  const nextMotionAlertIdRef = useRef(0);
  const lastPersonInferenceAtRef = useRef(0);
  const personModelRef = useRef<cocoSsd.ObjectDetection | null>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [devices, setDevices] = useState<MediaDeviceInfo[]>([]);
  const [selectedDeviceId, setSelectedDeviceId] = useState("");
  const [status, setStatus] = useState("Permission not requested");
  const [cameraError, setCameraError] = useState("");
  const [videoAspectRatio, setVideoAspectRatio] = useState("16 / 9");
  const [motionRegions, setMotionRegions] = useState<MotionRegion[]>([]);
  const [motionAlerts, setMotionAlerts] = useState<
    { id: number; detectedAt: string; regionCount: number }[]
  >([]);
  const [motionStatus, setMotionStatus] = useState("Waiting for camera");
  const [motionError, setMotionError] = useState("");
  const [personCount, setPersonCount] = useState(0);
  const [personBoxes, setPersonBoxes] = useState<
    Array<{ x: number; y: number; width: number; height: number; confidence: number }>
  >([]);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    video.srcObject = stream;
    if (!stream) return;

    void video.play().catch(() => {
      if (video.srcObject !== stream) return;
      setStatus("Preview unavailable");
      setCameraError("The camera connected, but the browser could not start video playback.");
    });
  }, [stream]);

  useEffect(() => {
    let active = true;
    setMotionStatus("Loading person detector");
    cocoSsd
      .load({ base: "lite_mobilenet_v2" })
      .then((model) => {
        if (!active) return;
        personModelRef.current = model;
        setMotionStatus("Person detector ready");
      })
      .catch((error: Error) => {
        if (!active) return;
        setMotionError(`Person detector unavailable: ${error.message}`);
      });
    return () => {
      active = false;
    };
  }, []);

  useEffect(
    () => () => {
      streamRef.current?.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    },
    [],
  );

  useEffect(() => {
    if (!stream) return;

    const canvas = document.createElement("canvas");
    canvas.width = motionFrameWidth;
    canvas.height = motionFrameHeight;
    const context = canvas.getContext("2d", { willReadFrequently: true });
    const inferenceCanvas = document.createElement("canvas");
    const inferenceContext = inferenceCanvas.getContext("2d", { willReadFrequently: true });
    if (!context) {
      setMotionStatus("Analysis unavailable");
      setMotionError("This browser cannot process camera frames locally.");
      return;
    }

    motionBaselineRef.current = null;
    consecutiveMotionFramesRef.current = 0;
    setMotionError("");
    setMotionStatus("Calibrating local motion analysis");

    const sampleFrame = () => {
      const video = videoRef.current;
      if (!video || video.readyState < HTMLMediaElement.HAVE_CURRENT_DATA) return;

      let currentFrame: Uint8ClampedArray;
      try {
        context.drawImage(video, 0, 0, motionFrameWidth, motionFrameHeight);
        currentFrame = new Uint8ClampedArray(
          context.getImageData(0, 0, motionFrameWidth, motionFrameHeight).data,
        );
      } catch (error) {
        if (!(error instanceof DOMException)) throw error;
        window.clearInterval(intervalId);
        setMotionStatus("Analysis unavailable");
        setMotionError("The browser could not read camera frames for local analysis.");
        return;
      }

      const inferenceNow = Date.now();
      if (
        inferenceContext &&
        personModelRef.current &&
        inferenceNow - lastPersonInferenceAtRef.current >= 2000
      ) {
        lastPersonInferenceAtRef.current = inferenceNow;
        void personModelRef
          .current!.detect(video, 20)
          .then((predictions) => {
            const people = predictions
              .filter((prediction) => prediction.class === "person")
              .filter((prediction) => prediction.score >= 0.5)
              .map((prediction) => {
                const [x, y, width, height] = prediction.bbox;
                return {
                  x: x / video.videoWidth,
                  y: y / video.videoHeight,
                  width: width / video.videoWidth,
                  height: height / video.videoHeight,
                  confidence: prediction.score,
                };
              });
            setPersonCount(people.length);
            setPersonBoxes(people);

            const detectedAt = new Date(inferenceNow).toISOString();
            void fetch("http://127.0.0.1:8000/api/v1/detections", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                camera_id: "browser-local-camera",
                detected_at: detectedAt,
                model_id: "tensorflow-coco-ssd",
                model_version: "lite_mobilenet_v2",
                detections: people.map((person) => ({
                  label: "person",
                  confidence: person.confidence,
                  x: person.x,
                  y: person.y,
                  width: person.width,
                  height: person.height,
                })),
                idempotency_key: `person-${inferenceNow}-browser-local-camera`,
              }),
            }).catch(() => {
              setMotionError("Person detections were found, but could not be saved locally.");
            });
          })
          .catch((error: Error) => {
            setMotionError(`Person analysis failed: ${error.message}`);
          });
      }

      const previousFrame = motionBaselineRef.current;
      motionBaselineRef.current = currentFrame;
      if (!previousFrame) {
        setMotionStatus("Monitoring locally");
        return;
      }

      const regions = findMotionRegions(
        currentFrame,
        previousFrame,
        motionFrameWidth,
        motionFrameHeight,
      );
      setMotionRegions(regions);

      if (regions.length === 0) {
        consecutiveMotionFramesRef.current = 0;
        setMotionStatus("Monitoring locally");
        return;
      }

      consecutiveMotionFramesRef.current += 1;
      setMotionStatus("Motion activity · local only");
      const motionNow = Date.now();
      if (consecutiveMotionFramesRef.current >= 2 && motionNow - lastMotionAlertAtRef.current >= 3000) {
        lastMotionAlertAtRef.current = motionNow;
        const detectedAt = new Date(motionNow).toISOString();
        setMotionAlerts((previousAlerts) => [
          {
            id: nextMotionAlertIdRef.current++,
            detectedAt,
            regionCount: regions.length,
          },
          ...previousAlerts,
        ].slice(0, 5));
        void fetch("http://127.0.0.1:8000/api/v1/detections", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            camera_id: "browser-local-camera",
            detected_at: detectedAt,
            model_id: "browser-motion-demo",
            model_version: "pixel-difference-1",
            detections: regions.map((region) => ({
              label: "motion",
              confidence: 1,
              x: region.x / motionFrameWidth,
              y: region.y / motionFrameHeight,
              width: region.width / motionFrameWidth,
              height: region.height / motionFrameHeight,
            })),
            idempotency_key: `motion-${nextMotionAlertIdRef.current}-${motionNow}`,
          }),
        }).catch(() => {
          setMotionError("Motion was detected, but it could not be saved to the local database.");
        });
      }
    };

    const intervalId = window.setInterval(sampleFrame, 200);
    return () => {
      window.clearInterval(intervalId);
      motionBaselineRef.current = null;
      consecutiveMotionFramesRef.current = 0;
    };
  }, [stream]);

  const stopCamera = () => {
    streamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = null;
    setStream(null);
    setStatus("Stopped");
    setCameraError("");
    setMotionStatus("Waiting for camera");
    setMotionError("");
    setMotionRegions([]);
    setPersonCount(0);
    setPersonBoxes([]);
    setVideoAspectRatio("16 / 9");
  };

  const startCamera = async () => {
    setCameraError("");
    if (!window.isSecureContext || !navigator.mediaDevices?.getUserMedia) {
      setStatus("Unavailable");
      setCameraError("Camera access requires localhost or a secure HTTPS page.");
      return;
    }

    const previousStream = streamRef.current;
    setMotionError("");
    setStatus("Requesting camera permission");
    try {
      const nextStream = await navigator.mediaDevices.getUserMedia({
        audio: false,
        video: selectedDeviceId ? { deviceId: { exact: selectedDeviceId } } : true,
      });

      streamRef.current = nextStream;
      setStream(nextStream);
      setPersonCount(0);
      setPersonBoxes([]);
      previousStream?.getTracks().forEach((track) => track.stop());
      setStatus("Connected · local preview");

      const videoTrack = nextStream.getVideoTracks()[0];
      const activeDeviceId = videoTrack?.getSettings().deviceId;
      if (activeDeviceId) setSelectedDeviceId(activeDeviceId);
      videoTrack?.addEventListener(
        "ended",
        () => {
          if (streamRef.current !== nextStream) return;
          streamRef.current = null;
          setStream(null);
          setStatus("Disconnected");
          setCameraError("The camera stream ended.");
          setMotionStatus("Waiting for camera");
          setMotionRegions([]);
          setPersonCount(0);
          setPersonBoxes([]);
        },
        { once: true },
      );

      try {
        const availableDevices = await navigator.mediaDevices.enumerateDevices();
        if (streamRef.current === nextStream) {
          setDevices(availableDevices.filter((device) => device.kind === "videoinput"));
        }
      } catch (error) {
        if (!(error instanceof DOMException)) throw error;
        setCameraError("Camera connected, but the browser could not list available cameras.");
      }
    } catch (error) {
      const message = cameraErrorMessage(error);
      if (!message) throw error;
      setStatus(previousStream ? "Previous camera remains connected" : "Not connected");
      setCameraError(message);
    }
  };

  return (
    <section className="camera-preview-card">
      <div className="camera-preview-header">
        <div>
          <span className="section-label">LOCAL CAMERA DEMO</span>
          <h3>Laptop, USB, or phone-as-webcam</h3>
          <p>Start only when ready; your browser may ask for camera permission.</p>
        </div>
        <span className={`asset-status ${stream ? "connected" : "disconnected"}`}>
          {status}
        </span>
      </div>
      <div className="camera-preview-window" style={{ aspectRatio: stream ? videoAspectRatio : undefined }}>
        {stream ? (
          <>
            <video
              ref={videoRef}
              autoPlay
              muted
              playsInline
              aria-label="Local camera preview"
              onLoadedMetadata={(event) => {
                const { videoWidth, videoHeight } = event.currentTarget;
                if (videoWidth > 0 && videoHeight > 0) {
                  setVideoAspectRatio(`${videoWidth} / ${videoHeight}`);
                }
              }}
            />
            <svg
              className="motion-overlay"
              viewBox={`0 0 ${motionFrameWidth} ${motionFrameHeight}`}
              preserveAspectRatio="none"
              aria-hidden="true"
            >
              {personBoxes.map((person, index) => (
                <g key={`${person.x}-${person.y}-${index}`}>
                  <rect
                    className="person-box"
                    x={person.x * motionFrameWidth}
                    y={person.y * motionFrameHeight}
                    width={person.width * motionFrameWidth}
                    height={person.height * motionFrameHeight}
                  />
                  <text
                    className="person-label"
                    x={person.x * motionFrameWidth}
                    y={Math.max(5, person.y * motionFrameHeight - 1)}
                  >
                    PERSON {Math.round(person.confidence * 100)}%
                  </text>
                </g>
              ))}
              {motionRegions.map((region, index) => (
                <g key={`${region.x}-${region.y}-${index}`}>
                  <rect x={region.x} y={region.y} width={region.width} height={region.height} />
                  <text x={region.x} y={Math.max(5, region.y - 1)}>MOTION</text>
                </g>
              ))}
            </svg>
          </>
        ) : (
          <div className="camera-preview-empty">
            <div className="crosshair" />
            <strong>CAMERA PREVIEW OFF</strong>
          </div>
        )}
      </div>
      <div className="camera-preview-controls">
        <label className="camera-select">
          Camera device
          <select
            value={selectedDeviceId}
            onChange={(event) => setSelectedDeviceId(event.target.value)}
            disabled={devices.length === 0}
          >
            <option value="">Default camera</option>
            {devices.map((device, index) => (
              <option key={device.deviceId} value={device.deviceId}>
                {device.label || `Camera ${index + 1}`}
              </option>
            ))}
          </select>
        </label>
        {stream ? (
          <>
            <button className="button secondary" onClick={() => void startCamera()}>
              Switch camera
            </button>
            <button className="button danger" onClick={stopCamera}>
              Stop camera
            </button>
          </>
        ) : (
          <button
            className="button"
            onClick={() => void startCamera()}
            disabled={status === "Requesting camera permission"}
          >
            {status === "Requesting camera permission" ? "Requesting camera…" : "Start camera"}
          </button>
        )}
      </div>
      <div className="detector-gate" role="note">
        <strong>TensorFlow COCO person detection is active · vehicle detection is also available.</strong>
        <span>Only detections labeled “person” are counted. The model runs locally in this browser tab.</span>
      </div>
      <section className="motion-panel" aria-label="Local motion demo">
        <div className="motion-panel-heading">
          <strong>LOCAL PERSON ANALYSIS · COCO-SSD</strong>
          <span>{personCount} person{personCount === 1 ? "" : "s"} · {motionStatus}</span>
        </div>
        <p>
          {motionError ||
            "Highlights pixel changes only; lighting changes or camera movement may trigger activity. Motion records are labeled demo-only and are stored locally; this is not person/vehicle detection."}
        </p>
        {motionAlerts.length > 0 ? (
          <ol className="motion-alert-list" aria-label="Local motion activity history">
            {motionAlerts.map((alert) => (
              <li key={alert.id} role="status">
                <strong>Motion activity · review only</strong>
                <span>{alert.regionCount} highlighted region{alert.regionCount === 1 ? "" : "s"}</span>
                <time dateTime={alert.detectedAt}>
                  {new Date(alert.detectedAt).toLocaleTimeString()}
                </time>
              </li>
            ))}
          </ol>
        ) : (
          <span className="motion-empty">No local motion activity recorded this session.</span>
        )}
      </section>
      <p className="camera-preview-notice">
        Person frames are analyzed locally with TensorFlow COCO-SSD. Person counts and boxes are saved to local SQLite; no frame is uploaded.
      </p>
      {cameraError && <div className="error-state" role="alert">{cameraError}</div>}
    </section>
  );
}

function cameraErrorMessage(error: unknown): string | undefined {
  if (error instanceof DOMException) {
    if (error.name === "NotAllowedError" || error.name === "SecurityError") {
      return "Camera permission is blocked. In site controls beside the address bar, open Site settings and set Camera to Allow. Also check Windows camera privacy settings, then reload and try again.";
    }
    if (error.name === "NotFoundError" || error.name === "DevicesNotFoundError") {
      return "No camera was found. Connect a camera and try again.";
    }
    if (error.name === "NotReadableError" || error.name === "TrackStartError") {
      return "The camera is busy or unavailable. Close other camera apps and try again.";
    }
    return `Camera request failed: ${error.message}`;
  }
  if (error instanceof TypeError) {
    return "The browser rejected the camera settings. Check the selected device and try again.";
  }
  return undefined;
}

function EventsView({ events }: { events: EventRecord[] }) {
  return (
    <section className="page">
      <div className="toolbar">
        <div><span className="section-label">AUDITABLE TEST RECORDS</span><h2>Events</h2></div>
      </div>
      <div className="table-card">
        {events.map((event) => (
          <article className="event-row" key={event.id}>
            <div>
              <span className="section-label">{event.label}</span>
              <h3>{event.event_type}</h3>
            </div>
            <span>Confidence: {event.confidence.toFixed(2)}</span>
            <time>{event.created_at}</time>
          </article>
        ))}
      </div>
    </section>
  );
}

function DatabaseView() {
  const [records, setRecords] = useState<DetectionRecord[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    const load = () => {
      fetchJson<{ items: DetectionRecord[] }>("/api/v1/detections")
        .then((payload) => {
          if (active) setRecords(payload.items);
        })
        .catch((loadError: Error) => {
          if (active) setError(loadError.message);
        });
    };
    load();
    const interval = window.setInterval(load, 2000);
    return () => {
      active = false;
      window.clearInterval(interval);
    };
  }, []);

  return (
    <section className="page">
      <div className="toolbar">
        <div>
          <span className="section-label">LOCAL SQLITE STORAGE</span>
          <h2>Detection database</h2>
        </div>
        <strong>{records.length} record{records.length === 1 ? "" : "s"}</strong>
      </div>
      {error && <div className="error-state" role="alert">{error}</div>}
      {records.length === 0 ? (
        <EmptyState text="No detection records have been saved yet." />
      ) : (
        <div className="table-card">
          {records.map((record) => (
            <article className="alert-row" key={record.id}>
              <span className="severity-pill info">{record.model_id}</span>
              <div>
                <h3>{record.person_count} people · {record.vehicle_count} vehicles</h3>
                <p>{record.detections.map((item) => `${item.label} (${Math.round(item.confidence * 100)}%)`).join(", ")}</p>
              </div>
              <span className="state">{record.camera_id}</span>
              <time>{new Date(record.detected_at).toLocaleString()}</time>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}

function HealthView({ devices }: { devices: Device[] }) {
  return (
    <section className="page">
      <div className="toolbar">
        <div><span className="section-label">LOCAL NODE</span><h2>System health</h2></div>
      </div>
      <div className="card-grid">
        {devices.map((device) => (
          <article className="asset-card" key={device.id}>
            <span className="asset-status degraded">{device.status}</span>
            <h3>{device.hostname}</h3>
            <dl>
              <div><dt>Software</dt><dd>{device.software_version}</dd></div>
              <div><dt>Last seen</dt><dd>{device.last_seen}</dd></div>
            </dl>
          </article>
        ))}
      </div>
    </section>
  );
}

function SettingsView() {
  return (
    <section className="page">
      <div className="toolbar">
        <div><span className="section-label">LOCAL CONFIGURATION</span><h2>Settings</h2></div>
      </div>
      <div className="settings-card">
        <h3>Development status</h3>
        <p>Authentication, database persistence, camera capture, inference, and evidence storage are not connected.</p>
        <div className="status-list">
          <span>API</span><strong>Running in synthetic mode</strong>
          <span>Database</span><strong>Not connected</strong>
          <span>Identity</span><strong>Not configured</strong>
          <span>Camera source</span><strong>Not connected</strong>
        </div>
      </div>
    </section>
  );
}

function Metric({ label, value, tone }: { label: string; value: string; tone: string }) {
  return (
    <article className={`metric ${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
    </article>
  );
}

function EmptyState({ text }: { text: string }) {
  return <div className="empty-state">{text}</div>;
}
