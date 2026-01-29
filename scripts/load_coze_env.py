#!/usr/bin/env python3
"""
Coze 环境变量加载器
从 .coze.env 文件加载环境变量
"""
import os
import sys
from pathlib import Path

def load_coze_env():
    """
    从 .coze.env 文件加载环境变量
    """
    # 获取项目根目录
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    env_file = os.path.join(workspace_path, ".coze.env")

    # 检查文件是否存在
    if not os.path.exists(env_file):
        print(f"[警告] 未找到 .coze.env 文件: {env_file}")
        return False

    # 读取文件并设置环境变量
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                # 跳过空行和注释
                if not line or line.startswith('#'):
                    continue

                # 解析 KEY=VALUE 格式
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    # 设置环境变量
                    os.environ[key] = value
                    print(f"[加载] {key}={'*' * (len(value) - 4)}{value[-4:]}")

        print(f"[成功] 已加载 .coze.env 文件")
        return True

    except Exception as e:
        print(f"[错误] 加载 .coze.env 文件失败: {e}")
        return False

if __name__ == "__main__":
    # 测试加载
    load_coze_env()

    # 打印环境变量
    print("\n[环境变量]")
    print(f"OPENAI_API_KEY: {'*' * (len(os.getenv('OPENAI_API_KEY', '')) - 4)}{os.getenv('OPENAI_API_KEY', '')[-4:]}")
    print(f"OPENAI_API_BASE: {os.getenv('OPENAI_API_BASE', 'None')}")
