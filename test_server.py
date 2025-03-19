import os
import asyncio
import tempfile
from pathlib import Path

async def test_mcp_server():
    """
    测试MCP服务器的基本功能
    
    注意: 请确保服务器正在运行 (python server.py)
    """
    try:
        # 这里我们使用subprocess来调用命令行工具，模拟MCP客户端的调用
        import subprocess
        
        print("=== 开始测试Code2Flow MCP服务器 ===")
        
        # 创建一个简单的Python文件用于测试
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
        
        # 直接使用code2flow命令生成图
        output_path = os.path.join(test_dir, "output.png")
        print(f"正在生成调用图...")
        
        try:
            result = subprocess.run(
                ["code2flow", test_file_path, "--output", output_path],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"调用图生成成功: {output_path}")
            
            if os.path.exists(output_path):
                print(f"图像文件大小: {os.path.getsize(output_path)} 字节")
            else:
                print("警告: 无法找到生成的图像文件")
        except subprocess.CalledProcessError as e:
            print(f"生成调用图失败: {e.stderr}")
        except FileNotFoundError:
            print("未找到code2flow命令，请确保已正确安装")
        
        print("\n=== 测试完成 ===")
        
    except Exception as e:
        print(f"测试过程中出现错误: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_mcp_server()) 