import json
from pathlib import Path

from capture_node.cli import main


def test_capture_cli_labels_decoded_frames_without_claiming_detection(
    synthetic_video: Path,
    capsys,
) -> None:
    exit_code = main(
        [
            "--video",
            str(synthetic_video),
            "--camera-id",
            "synthetic-camera",
            "--max-frames",
            "2",
        ]
    )

    output = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
    assert exit_code == 0
    assert len(output) == 2
    assert [item["frame_id"] for item in output] == [0, 1]
    assert all(item["source_status"] == "frame_received" for item in output)
    assert all("detections" not in item for item in output)
