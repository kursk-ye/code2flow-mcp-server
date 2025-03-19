# Code2Flow MCP 服务器

这是一个将 code2flow 命令行工具包装为 MCP (Model Context Protocol) 服务器的项目。它允许 AI 应用程序通过标准化的 MCP 协议生成和访问代码调用图。

## 功能特点

- 分析源代码并生成调用图
- 支持多种编程语言（Python、JavaScript、Ruby、PHP）
- 通过 MCP 协议提供服务，易于与 AI 应用集成
- 图像以 PNG 格式输出
- 提供版本检查和代码复杂度分析功能

## 安装要求

- Python 3.7+
- Windows 11 或其他支持的操作系统
- PowerShell 或其他命令行终端
- 已安装 code2flow 命令行工具

## 安装步骤

1. 克隆此仓库
```
git clone https://github.com/kursk-ye/code2flow-mcp-server.git
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

4. 安装 code2flow 命令行工具
```
pip install code2flow
```

## 使用方法

### 直接使用 Python 运行

1. 启动 MCP 服务器
```
python server.py
```

### 使用 MCP 工具运行

1. 使用 MCP Inspector 工具
```
mcp dev server.py
```

2. 安装到 Claude Desktop
```
mcp install server.py
```

3. 添加到 Cursor MCP 配置
```json
"code2flow": {
  "command": "cmd",
  "args": [
    "/c",
    "python",
    "path/to/server.py"
  ]
}
```

## 可用工具

服务器提供以下 MCP 工具：

1. `generate_call_graph` - 生成代码调用图
2. `check_code2flow_version` - 检查 code2flow 版本
3. `analyze_code_complexity` - 分析代码复杂度

## 可用资源

服务器提供以下 MCP 资源：

1. `help://code2flow` - 帮助文档
2. `languages://supported` - 支持的语言列表
3. `call-graph://图像ID` - 生成的调用图图像

### 示例（使用 Python MCP 客户端）

```python
import asyncio
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
    
    # 检查code2flow版本
    version_info = await session.call_tool("check_code2flow_version")
    print(version_info)
    
    # 分析代码复杂度
    complexity = await session.call_tool("analyze_code_complexity", {
        "source_path": "path/to/your/code",
        "language": "python"
    })
    print(complexity)

if __name__ == "__main__":
    asyncio.run(main())
```

## 配置选项

生成调用图时支持以下参数：

- `source_paths`：要分析的源代码文件或目录的路径列表
- `output_path`：（可选）输出文件的路径
- `language`：（可选）源代码语言（python、js、ruby、php）
- `exclude`：（可选）要排除的文件模式列表
- `include`：（可选）要包含的文件模式列表

## 文件结构

- `server.py` - 主服务器代码
- `mcp_client_example.py` - 客户端示例代码
- `test_server.py` - 测试代码
- `requirements.txt` - 依赖文件

## 许可证

MIT 