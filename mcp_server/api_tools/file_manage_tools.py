"""File Manage Tools - MCP tools for file upload, download and management"""
import os
import base64
import httpx
from pathlib import Path
from mcp.server.fastmcp import FastMCP

API_BASE = os.getenv("CORE_API_BASE", "http://127.0.0.1:8000")
HTTP_TIMEOUT = httpx.Timeout(timeout=30.0, connect=10.0)


def register_file_manage_tools(mcp: FastMCP):
    """Register file management tools to the MCP server."""

    def _headers() -> dict:
        api_key = os.getenv("SAITEC_API_KEY", "")
        return {"X-API-Key": api_key}

    # --- Tools ---

    @mcp.tool()
    async def upload_file(
        file_path: str,
        file_type: str,
    ) -> dict:
        """
        Upload a local file to the server (only supports image and dataset types).

        Args:
            file_path: Local path to the file, e.g., '/home/user/images/photo.png'.
            file_type: File type, must be 'image' or 'dataset'.

        Returns:
            File metadata including file_id, sha256, size_bytes, file_type, filename, created_at.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        filename = path.name
        file_content = base64.b64encode(path.read_bytes()).decode("utf-8")

        payload = {
            "file_content": file_content,
            "filename": filename,
            "file_type": file_type,
        }

        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            resp = await client.post(
                f"{API_BASE}/api/v1/skills/file-manage/upload",
                json=payload,
                headers=_headers(),
            )
            resp.raise_for_status()
            return resp.json()

    @mcp.tool()
    async def download_file(file_id: str) -> dict:
        """
        Download a file by file_id.

        Args:
            file_id: The UUID of the file to download.

        Returns:
            File content as streaming response.
        """
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            resp = await client.get(
                f"{API_BASE}/api/v1/skills/file-manage/files/{file_id}",
                headers=_headers(),
            )
            resp.raise_for_status()
            return resp.json()

    @mcp.tool()
    async def list_files(
        skip: int = 0,
        limit: int = 100,
    ) -> dict:
        """
        List user's private files (excludes task-associated files).

        Args:
            skip: Number of records to skip, default 0.
            limit: Number of records to return, default 100, max 1000.

        Returns:
            Paginated file list with total count.
        """
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            resp = await client.get(
                f"{API_BASE}/api/v1/skills/file-manage/files",
                params={"skip": skip, "limit": limit},
                headers=_headers(),
            )
            resp.raise_for_status()
            return resp.json()

    @mcp.tool()
    async def list_task_files(task_id: str) -> dict:
        """
        List output files for a specific task.

        Args:
            task_id: The task ID to query.

        Returns:
            List of task output files with file_id, storage_uri, role, size_bytes, sha256, created_at.
        """
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            resp = await client.get(
                f"{API_BASE}/api/v1/skills/file-manage/tasks/{task_id}/files",
                headers=_headers(),
            )
            resp.raise_for_status()
            return resp.json()
