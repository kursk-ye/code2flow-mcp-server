import asyncio
import json
import os
from typing import Dict, Any

# 这个例子使用的是模拟的MCP客户端
# 在真实场景中，你需要安装并使用实际的MCP客户端库

class MockMCPClient:
    """模拟的MCP客户端，用于演示"""
    
    def __init__(self, server_url: str = "http://localhost:8000"):
        self.server_url = server_url
        print(f"连接到MCP服务器: {server_url}")
    
    async def create_session(self):
        """创建一个新的会话"""
        print("创建新会话...")
        return MockMCPSession(self)

class MockMCPSession:
    """模拟的MCP会话，用于演示"""
    
    def __init__(self, client: MockMCPClient):
        self.client = client
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None):
        """
        调用服务器上的工具
        
        参数:
        - tool_name: 工具名称
        - arguments: 工具参数
        
        返回:
        - 工具执行结果
        """
        print(f"调用工具: {tool_name}")
        print(f"参数: {json.dumps(arguments, ensure_ascii=False, indent=2)}")
        
        # 在这里，我们实际上是调用本地的code2flow命令
        # 在真实场景中，这将通过MCP协议发送到服务器执行
        if tool_name == "generate_call_graph":
            import subprocess
            import tempfile
            
            source_paths = arguments.get("source_paths", [])
            output_path = arguments.get("output_path")
            language = arguments.get("language")
            
            if not source_paths:
                return {"error": "缺少必要参数: source_paths"}
            
            if not output_path:
                temp_dir = tempfile.mkdtemp()
                output_path = os.path.join(temp_dir, "call_graph.png")
            
            cmd = ["code2flow"]
            
            if language:
                cmd.extend(["--language", language])
            
            cmd.extend(["--output", output_path])
            cmd.extend(source_paths)
            
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                print(f"调用图生成成功: {output_path}")
                return {
                    "success": True,
                    "resource_id": f"call-graph://{os.path.basename(output_path)}",
                    "output_path": output_path
                }
            except subprocess.CalledProcessError as e:
                return {"error": f"生成调用图失败: {e.stderr}"}
            except FileNotFoundError:
                return {"error": "未找到code2flow命令，请确保已正确安装"}
        
        elif tool_name == "check_code2flow_version":
            # 模拟版本检查
            import subprocess
            
            try:
                result = subprocess.run(
                    ["code2flow", "--version"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                return {"version": result.stdout.strip()}
            except:
                return {"error": "无法获取版本信息"}
        
        else:
            return {"error": f"未知工具: {tool_name}"}
    
    async def read_resource(self, resource_uri: str):
        """
        读取资源内容
        
        参数:
        - resource_uri: 资源URI
        
        返回:
        - 资源内容和MIME类型
        """
        print(f"读取资源: {resource_uri}")
        
        # 在这个模拟实现中，我们只处理本地文件
        if resource_uri.startswith("call-graph://"):
            # 提取文件名
            filename = resource_uri.replace("call-graph://", "")
            
            try:
                with open(filename, "rb") as f:
                    content = f.read()
                return content, "image/png"
            except:
                return None, None
        
        elif resource_uri == "help://code2flow":
            help_text = """
            # Code2Flow MCP服务器
            
            此服务器提供Code2Flow功能，用于生成代码调用图。
            
            ## 主要功能
            
            - `generate_call_graph`: 生成代码调用图并返回PNG图像
            - `check_code2flow_version`: 检查安装的code2flow版本信息
            - `analyze_code_complexity`: 分析源代码复杂度
            """
            return help_text, "text/markdown"
        
        else:
            return None, None

async def main():
    """主函数，演示如何使用MCP客户端与服务器交互"""
    
    # 创建一个临时的测试文件
    import tempfile
    
    test_dir = tempfile.mkdtemp()
    test_file_path = os.path.join(test_dir, "test_file.py")
    
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write("""
def function1():
    print("This is function 1")
    function2()
    function3()

def function2():
    print("This is function 2")
    
def function3():
    print("This is function 3")
    
def main():
    function1()
    
if __name__ == "__main__":
    main()
""")
    
    print(f"创建测试文件: {test_file_path}")
    
    # 创建MCP客户端并与服务器交互
    client = MockMCPClient()
    session = await client.create_session()
    
    # 检查code2flow版本
    version_result = await session.call_tool("check_code2flow_version")
    print(f"版本信息: {version_result}")
    
    # 生成调用图
    output_path = os.path.join(test_dir, "output.png")
    graph_result = await session.call_tool("generate_call_graph", {
        "source_paths": [test_file_path],
        "output_path": output_path,
        "language": "python"
    })
    
    print(f"调用图生成结果: {graph_result}")
    
    # 如果成功，检查输出文件
    if graph_result.get("success") and os.path.exists(output_path):
        print(f"生成的图像文件大小: {os.path.getsize(output_path)} 字节")
    
    print("\n演示完成!")

if __name__ == "__main__":
    asyncio.run(main()) 