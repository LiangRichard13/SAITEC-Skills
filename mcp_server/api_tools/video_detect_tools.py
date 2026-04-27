"""Video Detect Tools - MCP tools for video AIGC detection"""
import os
import httpx
from typing import Optional
from mcp.server.fastmcp import FastMCP

API_BASE = os.getenv("CORE_API_BASE", "http://127.0.0.1:8000")
HTTP_TIMEOUT = httpx.Timeout(timeout=300.0, connect=10.0)


def register_video_tools(mcp: FastMCP):
    """Register video detection tools to the MCP server."""

    def _headers() -> dict:
        api_key = os.getenv("SAITEC_API_KEY", "")
        return {"X-API-Key": api_key}

    # --- Tools ---

    @mcp.tool()
    async def detect_video(
        video_uri: str,
        method: str = "video_multihead_attention",
        threshold: float = 0.55,
    ) -> dict:
        """
        Detect if a video is AI-generated (AIGC detection).

        Args:
            video_uri: Video path, supports server_path:/path, file:///path, /path formats.
            method: Detection method, default 'video_multihead_attention'.
            threshold: Decision threshold, default 0.55.

        Returns:
            Detection result including task_id, status, and detection results.
        """
        payload = {
            "video_uri": video_uri,
            "method": method,
            "threshold": threshold,
        }

        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            resp = await client.post(
                f"{API_BASE}/api/v1/skills/video-detect/detect",
                json=payload,
                headers=_headers(),
            )
            resp.raise_for_status()
            return resp.json()

    @mcp.tool()
    async def batch_detect_videos(
        items: list[dict],
    ) -> dict:
        """
        Batch detect if multiple videos are AI-generated.

        Args:
            items: List of video items, each containing 'id' and 'video_uri'.

        Returns:
            Batch detection result with task_id and status.
        """
        payload = {
            "items": items,
        }

        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            resp = await client.post(
                f"{API_BASE}/api/v1/skills/video-detect/batch",
                json=payload,
                headers=_headers(),
            )
            resp.raise_for_status()
            return resp.json()

    @mcp.tool()
    async def get_video_task(task_id: str) -> dict:
        """
        Get video detection task details.

        Args:
            task_id: The task ID to query.

        Returns:
            Task details including status, method, result, and artifact URIs.
        """
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            resp = await client.get(
                f"{API_BASE}/api/v1/skills/video-detect/tasks/{task_id}",
                headers=_headers(),
            )
            resp.raise_for_status()
            return resp.json()

    @mcp.tool()
    async def get_video_task_artifacts(task_id: str) -> dict:
        """
        Get video detection task artifacts.

        Args:
            task_id: The task ID to query.

        Returns:
            Artifact paths list.
        """
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            resp = await client.get(
                f"{API_BASE}/api/v1/skills/video-detect/tasks/{task_id}/artifacts",
                headers=_headers(),
            )
            resp.raise_for_status()
            return resp.json()
