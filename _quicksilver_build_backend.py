"""Small dependency-free build backend for offline editable installs."""

from __future__ import annotations

import base64
import csv
import hashlib
import io
from pathlib import Path
import zipfile


NAME = "tensor-quicksilver-zk"
VERSION = "0.1.0"
SUMMARY = "Pedagogical pure-Python QuickSilver zero-knowledge proofs"
DIST = "tensor_quicksilver_zk"
DIST_INFO = f"{DIST}-{VERSION}.dist-info"
TAG = "py3-none-any"
PROJECT_ROOT = Path(__file__).resolve().parent


def get_requires_for_build_wheel(config_settings=None):
    return []


def get_requires_for_build_editable(config_settings=None):
    return []


def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
    return _write_metadata(metadata_directory)


def prepare_metadata_for_build_editable(metadata_directory, config_settings=None):
    return _write_metadata(metadata_directory)


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    files = []
    for path in sorted((PROJECT_ROOT / "quicksilver").glob("*.py")):
        files.append((path.relative_to(PROJECT_ROOT).as_posix(), path.read_bytes()))
    return _write_wheel(wheel_directory, files)


def build_editable(wheel_directory, config_settings=None, metadata_directory=None):
    pth = f"{DIST}_editable.pth"
    files = [(pth, f"{PROJECT_ROOT}\n".encode())]
    return _write_wheel(wheel_directory, files)


def _metadata():
    return (
        "Metadata-Version: 2.1\n"
        f"Name: {NAME}\n"
        f"Version: {VERSION}\n"
        f"Summary: {SUMMARY}\n"
        "Requires-Python: >=3.10\n"
        "Provides-Extra: dev\n"
        'Requires-Dist: pytest>=8; extra == "dev"\n'
        "Provides-Extra: test\n"
        'Requires-Dist: pytest>=8; extra == "test"\n'
        "\n"
    ).encode()


def _wheel_metadata():
    return (
        "Wheel-Version: 1.0\n"
        "Generator: quicksilver-build-backend\n"
        "Root-Is-Purelib: true\n"
        f"Tag: {TAG}\n"
        "\n"
    ).encode()


def _write_metadata(metadata_directory):
    dist_info = Path(metadata_directory) / DIST_INFO
    dist_info.mkdir(parents=True, exist_ok=True)
    (dist_info / "METADATA").write_bytes(_metadata())
    (dist_info / "WHEEL").write_bytes(_wheel_metadata())
    return DIST_INFO


def _write_wheel(wheel_directory, files):
    wheel_name = f"{DIST}-{VERSION}-{TAG}.whl"
    wheel_path = Path(wheel_directory) / wheel_name
    wheel_files = [
        *files,
        (f"{DIST_INFO}/METADATA", _metadata()),
        (f"{DIST_INFO}/WHEEL", _wheel_metadata()),
    ]

    record_rows = []
    with zipfile.ZipFile(wheel_path, "w", zipfile.ZIP_DEFLATED) as wheel:
        for path, data in wheel_files:
            wheel.writestr(path, data)
            digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=")
            record_rows.append((path, f"sha256={digest.decode()}", str(len(data))))

        record_path = f"{DIST_INFO}/RECORD"
        record_rows.append((record_path, "", ""))
        record = io.StringIO()
        writer = csv.writer(record, lineterminator="\n")
        writer.writerows(record_rows)
        wheel.writestr(record_path, record.getvalue().encode())

    return wheel_name
