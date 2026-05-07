#!/bin/bash
# MCP Server 启动脚本
# 使用方式: claude mcp add SAITEC-Skills /home/lcd/SAITEC-Skills/run_mcp.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source ~/miniconda3/etc/profile.d/conda.sh
conda activate skills

# 环境变量配置
export SAITEC_API_KEY=<your_api_key>
export CORE_API_BASE=<your_core_api_base>

python "$SCRIPT_DIR/mcp_server/server.py"
