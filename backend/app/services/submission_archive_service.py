from __future__ import annotations

import os
from io import BytesIO
from pathlib import Path, PurePosixPath
from zipfile import BadZipFile, ZipFile

from app.schemas.assignments import CodeFile


class SubmissionArchiveService:
    max_archive_bytes = 5 * 1024 * 1024
    max_files = 80
    max_file_bytes = 200 * 1024
    max_total_text_bytes = 1024 * 1024

    text_extensions = {
        ".css",
        ".csv",
        ".env",
        ".html",
        ".ini",
        ".java",
        ".js",
        ".json",
        ".jsx",
        ".md",
        ".py",
        ".rst",
        ".sql",
        ".toml",
        ".ts",
        ".tsx",
        ".txt",
        ".vue",
        ".xml",
        ".yaml",
        ".yml",
    }
    text_filenames = {"dockerfile", "makefile", "requirements.txt"}
    ignored_path_parts = {"__MACOSX", ".git", "node_modules", ".venv", "venv"}

    def parse_zip(self, archive_bytes: bytes) -> list[CodeFile]:
        if not archive_bytes:
            raise ValueError("上传文件不能为空。")
        if len(archive_bytes) > self.max_archive_bytes:
            raise ValueError("压缩包超过 5MB，请压缩核心代码后再上传。")

        try:
            with ZipFile(BytesIO(archive_bytes)) as archive:
                files = self._read_code_files(archive)
        except BadZipFile as error:
            raise ValueError("上传文件不是有效的 zip 压缩包。") from error

        if not files:
            raise ValueError("压缩包中未识别到可分析的文本代码文件。")
        return files

    def parse_directory(self, root: Path) -> list[CodeFile]:
        if not root.exists() or not root.is_dir():
            raise ValueError("仓库目录不存在，无法分析。")

        files: list[CodeFile] = []
        total_text_bytes = 0
        for current_root, dirnames, filenames in os.walk(root):
            dirnames[:] = sorted(
                dirname for dirname in dirnames if dirname not in self.ignored_path_parts
            )
            for filename in sorted(filenames):
                if len(files) >= self.max_files:
                    break
                path = Path(current_root) / filename
                if not path.is_file() or path.is_symlink():
                    continue
                relative_path = path.relative_to(root).as_posix()
                safe_path = self._safe_path(relative_path)
                if safe_path is None or not self._is_text_path(safe_path):
                    continue
                file_size = path.stat().st_size
                if file_size > self.max_file_bytes:
                    continue
                total_text_bytes += file_size
                if total_text_bytes > self.max_total_text_bytes:
                    raise ValueError("仓库内文本文件总量超过 1MB，请只提交本次作业核心代码。")

                content_bytes = path.read_bytes()
                if b"\x00" in content_bytes:
                    continue
                try:
                    content = content_bytes.decode("utf-8")
                except UnicodeDecodeError:
                    content = content_bytes.decode("utf-8", errors="replace")
                files.append(CodeFile(path=safe_path, content=content))
            if len(files) >= self.max_files:
                break

        if not files:
            raise ValueError("仓库中未识别到可分析的文本代码文件。")
        return files

    def _read_code_files(self, archive: ZipFile) -> list[CodeFile]:
        files: list[CodeFile] = []
        total_text_bytes = 0
        for member in archive.infolist():
            if member.is_dir():
                continue
            path = self._safe_path(member.filename)
            if path is None or not self._is_text_path(path):
                continue
            if member.file_size > self.max_file_bytes:
                continue
            total_text_bytes += member.file_size
            if total_text_bytes > self.max_total_text_bytes:
                raise ValueError("压缩包内文本文件总量超过 1MB，请只上传本次作业核心代码。")

            content_bytes = archive.read(member)
            if b"\x00" in content_bytes:
                continue
            try:
                content = content_bytes.decode("utf-8")
            except UnicodeDecodeError:
                content = content_bytes.decode("utf-8", errors="replace")
            files.append(CodeFile(path=path, content=content))
            if len(files) >= self.max_files:
                break
        return files

    def _safe_path(self, raw_path: str) -> str | None:
        raw_normalized = raw_path.replace("\\", "/")
        if raw_normalized.startswith("/"):
            return None
        normalized = raw_normalized.strip()
        path = PurePosixPath(normalized)
        if not normalized or path.is_absolute():
            return None
        if any(part in {"", ".", ".."} for part in path.parts):
            return None
        if any(part in self.ignored_path_parts for part in path.parts):
            return None
        return path.as_posix()

    def _is_text_path(self, path: str) -> bool:
        filename = path.rsplit("/", 1)[-1].lower()
        if filename in self.text_filenames:
            return True
        suffix = PurePosixPath(filename).suffix.lower()
        return suffix in self.text_extensions
