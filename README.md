# Code2Flow MCP 服务器

这是一个将 code2flow 命令行工具包装为 MCP (Model Context Protocol) 服务器的项目。它允许 AI 应用程序通过标准化的 MCP 协议生成和访问代码调用图。

## 功能特点

- 分析源代码并生成调用图
- 支持多种编程语言（Python、JavaScript、Ruby、PHP）
- 通过 MCP 协议提供服务，易于与 AI 应用集成
- 图像以 PNG 格式输出

## 安装要求

- Python 3.7+
- Windows 11 或其他支持的操作系统
- PowerShell 或其他命令行终端

## 安装步骤

1. 克隆此仓库
```
git clone <repository-url>
cd code2flow-mcp-server
```

2. 创建并激活虚拟环境（推荐）
```
python -m venv venv
.\venv\Scripts\Activate.ps1  # 在 PowerShell 中
```

3. 安装依赖项
```
pip install -r requirements.txt
```

## 使用方法

1. 启动 MCP 服务器
```
python server.py
```

2. 服务器将在 http://localhost:8000 启动

3. 使用 MCP 协议与服务器交互，调用 `generate_call_graph` 工具来生成代码调用图

### 示例（使用 Python MCP 客户端）

```python
from mcp.client import MCPClient

async def main():
    # 连接到服务器
    client = MCPClient("http://localhost:8000")
    
    # 创建新会话
    session = await client.create_session()
    
    # 调用工具生成调用图
    result = await session.call_tool("generate_call_graph", {
        "source_paths": ["path/to/your/code"],
        "language": "python"
    })
    
    # 获取资源 ID
    print(result)
    
    # 在实际应用中，您可以使用资源 ID 获取图像内容
```

## 配置选项

生成调用图时支持以下参数：

- `source_paths`：要分析的源代码文件或目录的路径列表
- `output_path`：（可选）输出文件的路径
- `language`：（可选）源代码语言（python、js、ruby、php）
- `exclude`：（可选）要排除的文件模式列表
- `include`：（可选）要包含的文件模式列表

## 许可证

MIT 