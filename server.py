from mcp.server.fastmcp import FastMCP
import subprocess
import tempfile
import os
import base64
import json
from pathlib import Path
from typing import List, Optional, Dict, Any

# 创建MCP服务器
mcp = FastMCP("Code2Flow")

@mcp.tool()
def generate_call_graph(
    source_paths: List[str], 
    output_path: Optional[str] = None,
    language: Optional[str] = None,
    exclude: Optional[List[str]] = None,
    include: Optional[List[str]] = None
) -> str:
    """
    生成代码调用图并返回PNG图像路径
    
    参数:
    - source_paths: 要分析的源代码文件或目录的路径列表
    - output_path: 输出PNG文件的路径（可选，默认生成临时文件）
    - language: 源代码语言（可选，自动检测）
    - exclude: 要排除的文件或目录模式列表（可选）
    - include: 要包含的文件或目录模式列表（可选）
    
    返回:
    - 生成的PNG图像的资源URI
    """
    try:
        # 如果没有指定输出路径，创建临时文件
        if not output_path:
            temp_dir = tempfile.mkdtemp()
            output_path = os.path.join(temp_dir, "call_graph.png")
        
        # 构建命令行参数
        cmd = ["code2flow"]
        
        # 添加语言参数
        if language:
            cmd.extend(["--language", language])
        
        # 添加排除模式
        if exclude:
            for pattern in exclude:
                cmd.extend(["--exclude", pattern])
        
        # 添加包含模式
        if include:
            for pattern in include:
                cmd.extend(["--include", pattern])
        
        # 添加输出路径
        cmd.extend(["--output", output_path])
        
        # 添加源路径
        cmd.extend(source_paths)
        
        # 执行命令
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        # 注册生成的图像作为资源
        resource_id = register_image_resource(output_path)
        
        return f"成功生成调用图！资源ID: {resource_id}"
    except subprocess.CalledProcessError as e:
        print(f"生成调用图失败: {e.stderr}")
        return f"生成调用图失败: {e.stderr}"
    except Exception as e:
        print(f"处理请求时发生错误: {str(e)}")
        return f"处理请求时发生错误: {str(e)}"

@mcp.tool()
def check_code2flow_version() -> str:
    """
    检查安装的code2flow版本信息
    
    返回:
    - code2flow的版本信息
    """
    try:
        result = subprocess.run(
            ["code2flow", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        return f"已安装的code2flow版本: {result.stdout.strip()}"
    except subprocess.CalledProcessError as e:
        print(f"获取版本信息失败: {e.stderr}")
        return f"获取版本信息失败: {e.stderr}"
    except FileNotFoundError:
        error_msg = "未找到code2flow命令，请确保已正确安装"
        print(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"处理请求时发生错误: {str(e)}"
        print(error_msg)
        return error_msg

@mcp.tool()
def analyze_code_complexity(
    source_path: str,
    language: Optional[str] = None
) -> Dict[str, Any]:
    """
    分析源代码复杂度并返回结果
    
    参数:
    - source_path: 源代码文件或目录的路径
    - language: 源代码语言（可选，自动检测）
    
    返回:
    - 复杂度分析结果
    """
    try:
        # 构建命令行参数
        cmd = ["code2flow", "--analyze-only"]
        
        if language:
            cmd.extend(["--language", language])
        
        cmd.append(source_path)
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        # 解析输出结果
        analysis = {
            "file_count": 0,
            "function_count": 0,
            "class_count": 0,
            "raw_output": result.stdout
        }
        
        # 尝试从输出中提取一些基本信息
        for line in result.stdout.splitlines():
            if "Processing" in line and "source file(s)" in line:
                try:
                    analysis["file_count"] = int(line.split("Processing")[1].split("source")[0].strip())
                except:
                    pass
            
            # 这里可以添加更多解析逻辑，但实际输出格式需要根据code2flow的实际输出进行调整
        
        return analysis
    except subprocess.CalledProcessError as e:
        error_msg = f"分析失败: {e.stderr}"
        print(error_msg)
        return {"error": error_msg}
    except FileNotFoundError:
        error_msg = "未找到code2flow命令，请确保已正确安装"
        print(error_msg)
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"处理请求时发生错误: {str(e)}"
        print(error_msg)
        return {"error": error_msg}

def register_image_resource(image_path: str) -> str:
    """注册图像文件作为资源并返回资源ID"""
    # 为图像创建一个唯一ID
    image_id = os.path.basename(image_path)
    
    @mcp.resource(f"call-graph://{image_id}")
    def get_image_resource():
        """获取生成的调用图PNG图像"""
        with open(image_path, "rb") as f:
            content = f.read()
        return content, "image/png"
    
    return f"call-graph://{image_id}"

# 添加帮助资源
@mcp.resource("help://code2flow")
def get_help() -> str:
    """获取code2flow的帮助文档"""
    help_text = """
    # Code2Flow MCP服务器

    此服务器提供Code2Flow功能，用于生成代码调用图。

    ## 主要功能

    - `generate_call_graph`: 生成代码调用图并返回PNG图像
    - `check_code2flow_version`: 检查安装的code2flow版本信息
    - `analyze_code_complexity`: 分析源代码复杂度
    
    ## 使用示例

    ```python
    # 分析单个文件
    result = await session.call_tool("generate_call_graph", {
        "source_paths": ["path/to/file.py"]
    })
    
    # 分析整个目录
    result = await session.call_tool("generate_call_graph", {
        "source_paths": ["path/to/directory"],
        "language": "python",
        "exclude": ["**/test/**"]
    })
    
    # 检查版本
    version_info = await session.call_tool("check_code2flow_version")
    
    # 分析代码复杂度
    complexity = await session.call_tool("analyze_code_complexity", {
        "source_path": "path/to/analyze",
        "language": "python"
    })
    ```
    """
    return help_text, "text/markdown"

# 添加支持的语言资源
@mcp.resource("languages://supported")
def get_supported_languages() -> str:
    """获取code2flow支持的编程语言列表"""
    languages = {
        "python": {
            "name": "Python",
            "extension": ".py",
            "description": "Python编程语言"
        },
        "js": {
            "name": "JavaScript",
            "extension": ".js",
            "description": "JavaScript编程语言"
        },
        "ruby": {
            "name": "Ruby",
            "extension": ".rb",
            "description": "Ruby编程语言"
        },
        "php": {
            "name": "PHP",
            "extension": ".php",
            "description": "PHP编程语言"
        }
    }
    return json.dumps(languages, ensure_ascii=False, indent=2), "application/json"

if __name__ == "__main__":
    mcp.run() 