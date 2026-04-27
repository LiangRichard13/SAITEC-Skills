"""Image Detect Tools - MCP tools for image AIGC detection"""
import os
import httpx
from typing import Optional
from mcp.server.fastmcp import FastMCP

API_BASE = os.getenv("CORE_API_BASE", "http://127.0.0.1:8000")
HTTP_TIMEOUT = httpx.Timeout(timeout=120.0, connect=10.0)


def register_image_tools(mcp: FastMCP):
    """Register image detection tools to the MCP server."""

    def _headers() -> dict:
        api_key = os.getenv("SAITEC_API_KEY", "")
        return {"X-API-Key": api_key}

    # --- Tools ---

    @mcp.tool()
    async def detect_image(
        image_uri: str,
        method: str = "deepfake_defenders",
        threshold: float = 0.55,
        return_visuals: bool = True,
    ) -> dict:
        """
        Detect if an image is AI-generated (AIGC detection).

        Args:
            image_uri: Image path, supports server_path:/path, file:///path, /path formats.
            method: Detection method, 'deepfake_defenders', 'mapnet', or 'tamper_yolo'. Default 'deepfake_defenders'.
            threshold: Decision threshold, default 0.55.
            return_visuals: Whether to return visual results, default True.

        Returns:
            Detection result including task_id, status, and detection results.
        """
        payload = {
            "image_uri": image_uri,
            "method": method,
            "threshold": threshold,
            "return_visuals": return_visuals,
        }

        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            resp = await client.post(
                f"{API_BASE}/api/v1/skills/image-detect/detect",
                json=payload,
                headers=_headers(),
            )
            resp.raise_for_status()
            return resp.json()

    @mcp.tool()
    async def batch_detect_images(
        items: list[dict],
        method: str = "tamper_yolo",
    ) -> dict:
        """
        Batch detect if multiple images are AI-generated.

        Args:
            items: List of image items, each containing 'id' and 'image_uri'.
            method: Detection method, 'deepfake_defenders', 'mapnet', or 'tamper_yolo'. Default 'tamper_yolo'.

        Returns:
            Batch detection result with task_id and status.
        """
        payload = {
            "method": method,
            "items": items,
        }

        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            resp = await client.post(
                f"{API_BASE}/api/v1/skills/image-detect/batch",
                json=payload,
                headers=_headers(),
            )
            resp.raise_for_status()
            return resp.json()

    @mcp.tool()
    async def get_image_task(task_id: str) -> dict:
        """
        Get image detection task details.

        Args:
            task_id: The task ID to query.

        Returns:
            Task details including status, method, result, and artifact URIs.
        """
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            resp = await client.get(
                f"{API_BASE}/api/v1/skills/image-detect/tasks/{task_id}",
                headers=_headers(),
            )
            resp.raise_for_status()
            return resp.json()

    @mcp.tool()
    async def get_image_task_artifacts(task_id: str) -> dict:
        """
        Get image detection task artifacts.

        Args:
            task_id: The task ID to query.

        Returns:
            Artifact paths list.
        """
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            resp = await client.get(
                f"{API_BASE}/api/v1/skills/image-detect/tasks/{task_id}/artifacts",
                headers=_headers(),
            )
            resp.raise_for_status()
            return resp.json()
