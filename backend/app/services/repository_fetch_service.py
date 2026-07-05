from __future__ import annotations

import subprocess
import tempfile
from ipaddress import ip_address, ip_network
from pathlib import Path
from urllib.parse import urlparse

from app.schemas.assignments import CodeFile
from app.services.submission_archive_service import SubmissionArchiveService


class RepositoryFetchService:
    clone_timeout_seconds = 25

    def __init__(self, archive_service: SubmissionArchiveService | None = None) -> None:
        self.archive_service = archive_service or SubmissionArchiveService()

    def fetch_repository_files(self, repository_url: str) -> list[CodeFile]:
        self._ensure_public_git_url(repository_url)
        with tempfile.TemporaryDirectory(prefix="zhichuang-repo-") as temp_dir:
            repo_path = Path(temp_dir) / "repo"
            self._clone(repository_url, repo_path)
            return self.archive_service.parse_directory(repo_path)

    def _clone(self, repository_url: str, repo_path: Path) -> None:
        try:
            subprocess.run(
                [
                    "git",
                    "clone",
                    "--depth",
                    "1",
                    "--single-branch",
                    repository_url,
                    str(repo_path),
                ],
                check=True,
                capture_output=True,
                text=True,
                timeout=self.clone_timeout_seconds,
            )
        except FileNotFoundError as error:
            raise ValueError("服务器未安装 git，暂不能拉取仓库。") from error
        except subprocess.TimeoutExpired as error:
            raise ValueError("仓库拉取超时，请只提交轻量公开仓库或改用 zip 上传。") from error
        except subprocess.CalledProcessError as error:
            detail = (error.stderr or error.stdout or "").strip()
            if len(detail) > 160:
                detail = detail[:160] + "..."
            message = "仓库拉取失败，请确认仓库地址可访问。"
            if detail:
                message = f"{message} Git 返回：{detail}"
            raise ValueError(message) from error

    def _ensure_public_git_url(self, repository_url: str) -> None:
        parsed = urlparse(repository_url.strip())
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("仓库链接必须是 http 或 https 开头的 Git 仓库地址。")
        hostname = (parsed.hostname or "").lower()
        if hostname in {"localhost", "0.0.0.0"} or hostname.startswith("127."):
            raise ValueError("仓库链接不能指向本机地址，请使用可访问的远程仓库。")
        try:
            address = ip_address(hostname)
        except ValueError:
            return
        blocked_networks = [
            ip_network("10.0.0.0/8"),
            ip_network("172.16.0.0/12"),
            ip_network("192.168.0.0/16"),
            ip_network("169.254.0.0/16"),
            ip_network("::1/128"),
            ip_network("fc00::/7"),
            ip_network("fe80::/10"),
        ]
        if any(address in network for network in blocked_networks):
            raise ValueError("仓库链接不能指向本机或内网地址，请使用可访问的远程仓库。")
