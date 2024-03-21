__version__ = "0.3.3.0"

import hashlib
import http
import os.path
import platform
import stat
import urllib.request

ARCHIVE_SHA256 = {
    "darwin-x86_64": (
        "https://github.com/jessfraz/dockfmt/releases/download/v0.3.3/dockfmt-darwin-amd64",
        "074a27d10a6529c6e86f1c3f9d8f37cfc92d17da4a804a824899474d678100dc",
    ),
    "linux-arm64": (
        "https://github.com/jessfraz/dockfmt/releases/download/v0.3.3/dockfmt-linux-arm64",
        "3eb64f8360286e802146eae89f2b5a215064bbbe66ed0a9b08c6bfc6e3f5cbd3",
    ),
    "linux-x86_64": (
        "https://github.com/jessfraz/dockfmt/releases/download/v0.3.3/dockfmt-linux-amd64",
        "f6bc025739cf4f56287e879c75c11cc73ebafdf93a57c9bcd8805d1ab82434a0",
    ),
    "windows-x86_64": (
        "https://github.com/jessfraz/dockfmt/releases/download/v0.3.3/dockfmt-windows-amd64",
        "dc16dca0dab0aa53afd4c0480ac2bf904424ff8464d4d2bf9700a08a8970ea99",
    ),
}
BASE_URL = "https://github.com/jessfraz/dockfmt/releases/download"


def get_download_url() -> tuple[str, str]:
    os, arch = platform.system().lower(), platform.machine().lower()
    if (
        os == "windows"
        or "x86" in arch
        or "amd" in arch
        or "i386" in arch
        or "i686" in arch
    ):
        arch = "x86_64"
    elif "arm" in arch or arch == "aarch64":
        arch = "arm64"

    try:
        url, sha256 = ARCHIVE_SHA256[f"{os}-{arch}"]
    except KeyError:
        # Fall back to x86 on m1 macs
        if arch == "arm64" and os == "darwin":
            arch = "x86_64"
        url, sha256 = ARCHIVE_SHA256[f"{os}-{arch}"]

    return url, sha256


def download(url: str, sha256: str) -> bytes:
    with urllib.request.urlopen(url) as resp:
        code = resp.getcode()
        if code != http.HTTPStatus.OK:
            raise ValueError(f"HTTP failure. Code: {code}")
        data = resp.read()

    checksum = hashlib.sha256(data).hexdigest()
    if checksum != sha256:
        raise ValueError(f"sha256 mismatch, expected {sha256}, got {checksum}")

    return data


def save_executable(data: bytes, base_dir: str) -> None:
    exe = "dockfmt" if platform.system() != "Windows" else "dockfmt.exe"
    output_path = os.path.join(base_dir, exe)
    os.makedirs(base_dir, exist_ok=True)

    with open(output_path, "wb") as fp:
        fp.write(data)

    # Mark as executable.
    # https://stackoverflow.com/a/14105527
    mode = os.stat(output_path).st_mode
    mode |= stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    os.chmod(output_path, mode)


def main() -> None:
    url, sha = get_download_url()
    data = download(url, sha)
    save_executable(data, base_dir=".")


if __name__ == "__main__":
    main()
