#!/usr/bin/env python3
import time
import io
import os
import json
import requests
import pyperclip
from PIL import ImageGrab, Image
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.live import Live
from rich.text import Text
from rich.layout import Layout
from rich.box import ROUNDED, DOUBLE, HEAVY
from rich import print as rprint
from rich.prompt import Prompt
from rich.markdown import Markdown
from datetime import datetime

# 初始化 Rich 控制台
console = Console()

# 服务器 API URL
API_URL = 'http://10.2.49.13:8000/api/images/upload'

# 配置
CONFIG = {
    "检查间隔": 1,  # 秒
    "保存目录": "images",
    "日志文件": "log.txt",
    "最大历史记录": 5,
    "项目名称": "",  # 将在启动时设置
}

# 历史记录
history = []

def get_clipboard_content():
    """获取剪贴板中的文本和图片内容"""
    # 尝试获取文本内容
    try:
        text = pyperclip.paste()
    except:
        text = None
    
    # 尝试获取图片内容
    try:
        image = ImageGrab.grabclipboard()
    except:
        image = None
    
    return {"text": text, "image": image}

def ensure_images_dir():
    """确保 images 目录存在，如果不存在则创建"""
    if not os.path.exists(CONFIG["保存目录"]):
        os.makedirs(CONFIG["保存目录"])
        console.print(f"[bold green]已创建[/bold green] '{CONFIG['保存目录']}' 目录")

def get_project_name():
    """获取项目名称"""
    console.print(Panel(
        "[bold]请输入当前项目名称，用于图片命名前缀[/bold]", 
        title="[bold cyan]项目设置[/bold cyan]", 
        border_style="cyan",
        box=ROUNDED
    ))
    
    # 获取用户输入
    project_name = Prompt.ask(
        "[bold green]项目名称>[/bold green]", 
        default="项目"
    )
    
    # 确保项目名称不含特殊字符
    import re
    project_name = re.sub(r'[\\/*?:"<>|]', "_", project_name)
    
    return project_name.strip()

def get_filename_from_user(default_name):
    """提示用户输入文件名"""
    # 移除默认名称中可能已有的项目名称前缀
    if CONFIG["项目名称"] and default_name.startswith(f"{CONFIG['项目名称']}_"):
        display_name = default_name[len(CONFIG["项目名称"])+1:]
    else:
        display_name = default_name
        
    console.print(Panel(
        f"[bold]请输入文件名（不含扩展名）或按回车使用默认名称[/bold]", 
        title=f"[bold cyan]{display_name}[/bold cyan]", 
        border_style="cyan",
        box=ROUNDED
    ))
    try:
        # 设置输入超时，避免无限等待
        import signal
        
        # 定义超时处理函数
        def timeout_handler(signum, frame):
            raise TimeoutError("输入超时")
        
        # 设置 30 秒超时
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(30)
        
        # 获取用户输入
        user_input = Prompt.ask("[bold green]>[/bold green]", default=display_name)
        
        # 取消超时警报
        signal.alarm(0)
        
        # 添加项目名称前缀
        if user_input and CONFIG["项目名称"]:
            final_name = f"{CONFIG['项目名称']}_{user_input.strip()}"
        else:
            final_name = user_input.strip() or display_name
            
        return final_name
    except (TimeoutError, KeyboardInterrupt):
        console.print("\n[yellow]使用默认文件名。[/yellow]")
        if CONFIG["项目名称"] and not default_name.startswith(f"{CONFIG['项目名称']}_"):
            return f"{CONFIG['项目名称']}_{default_name}"
        return default_name

def upload_image_to_server(image_path, filename):
    """上传图片到服务器并返回响应"""
    try:
        with open(image_path, 'rb') as img_file:
            file_size = os.path.getsize(image_path)
            files = {'file': (f"{filename}.png", img_file, 'image/png')}
            data = {'description': ''}
            
            # 使用简单的状态显示替代进度条
            console.print("[cyan]正在上传图片到服务器...[/cyan]")
            
            try:
                response = requests.post(
                    API_URL, 
                    files=files, 
                    data=data
                )
                
                # 上传完成提示
                console.print("[bold green]✓[/bold green] 上传完成")
                
                if response.status_code == 201:
                    return response.json()
                else:
                    console.print(Panel(
                        f"[bold red]状态码:[/bold red] {response.status_code}\n[red]响应:[/red] {response.text}", 
                        title="[bold red]上传图片失败[/bold red]",
                        border_style="red",
                        box=HEAVY
                    ))
                    return None
            except Exception as e:
                console.print(Panel(
                    f"[bold red]错误:[/bold red] {str(e)}", 
                    title="[bold red]上传图片失败[/bold red]",
                    border_style="red",
                    box=HEAVY
                ))
                return None
    except Exception as e:
        console.print(Panel(
            f"[bold red]错误:[/bold red] {str(e)}", 
            title="[bold red]上传图片失败[/bold red]",
            border_style="red",
            box=HEAVY
        ))
        return None

def log_image_url(filename, response_data):
    """将图片 URL 记录到 log.txt 文件"""
    log_file = CONFIG["日志文件"]
    url = response_data.get("url", "")
    
    # 添加到历史记录
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.append({
        "时间": timestamp,
        "文件名": filename,
        "URL": url
    })
    
    # 保持历史记录在最大限制内
    if len(history) > CONFIG["最大历史记录"]:
        history.pop(0)
    
    log_entry = f"{filename}:{url}\n"
    
    with open(log_file, "a") as f:
        f.write(log_entry)
    
    console.print(f"URL 已记录到 [bold cyan]{log_file}[/bold cyan]")
    
    # 复制 URL 到剪贴板
    pyperclip.copy(url)
    console.print("[green]✓[/green] URL 已复制到剪贴板")

def display_image_info(image_data, is_current=False):
    """以表格形式显示图片信息"""
    if not image_data:
        return None
    
    status = "[bold green]当前[/bold green]" if is_current else "[bold blue]新的[/bold blue]"
    
    table = Table(
        title=f"{status}剪贴板图片", 
        box=ROUNDED,
        highlight=True,
        title_style="bold cyan"
    )
    
    table.add_column("属性", style="cyan", justify="right")
    table.add_column("值", style="green")
    
    table.add_row("尺寸", f"{image_data.size[0]}x{image_data.size[1]} 像素")
    table.add_row("格式", f"{image_data.format if hasattr(image_data, 'format') else '未知'}")
    table.add_row("模式", f"{image_data.mode}")
    
    return table

def display_upload_result(response_data, filename):
    """以表格形式显示上传结果"""
    if not response_data:
        return None
    
    table = Table(
        title="[bold green]上传成功[/bold green]", 
        box=ROUNDED,
        highlight=True,
        title_style="bold green"
    )
    
    table.add_column("属性", style="cyan", justify="right")
    table.add_column("值", style="green")
    
    table.add_row("原始文件名", response_data.get("original_filename", ""))
    table.add_row("文件路径", response_data.get("file_path", ""))
    table.add_row("URL", response_data.get("url", ""))
    table.add_row("大小", f"{response_data.get('size', '')} 字节")
    table.add_row("内容类型", response_data.get("content_type", ""))
    table.add_row("ID", str(response_data.get("id", "")))
    table.add_row("创建时间", response_data.get("created_at", ""))
    table.add_row("本地保存路径", f"{CONFIG['保存目录']}/{filename}.png")
    
    return table

def show_history():
    """显示历史记录"""
    if not history:
        console.print("[yellow]暂无历史记录[/yellow]")
        return
    
    table = Table(
        title="[bold cyan]最近上传历史[/bold cyan]", 
        box=ROUNDED,
        highlight=True,
        title_style="bold cyan"
    )
    
    table.add_column("时间", style="cyan")
    table.add_column("文件名", style="green")
    table.add_column("URL", style="blue")
    
    for item in history:
        table.add_row(item["时间"], item["文件名"], item["URL"])
    
    console.print(table)

def show_welcome():
    """显示欢迎信息"""
    welcome_text = """
    # 📋 剪贴板监控工具
    
    **功能**:
    * 监控剪贴板文本和图片变化
    * 自动保存并上传图片
    * 记录和复制图片URL
    
    **操作提示**:
    * 按 [Ctrl+C] 停止监控
    * 复制图片后自动检测并处理
    * 上传成功后URL会自动复制到剪贴板
    """
    
    md = Markdown(welcome_text)
    console.print(Panel(md, border_style="cyan", box=DOUBLE))
    
    # 显示配置信息
    config_table = Table(box=ROUNDED, highlight=True)
    config_table.add_column("配置项", style="cyan", justify="right")
    config_table.add_column("值", style="green")
    
    for key, value in CONFIG.items():
        config_table.add_row(key, str(value))
    
    console.print(config_table)

def monitor_clipboard():
    """
    监控剪贴板的变化并显示新内容
    """
    ensure_images_dir()
    
    console.print(Panel(
        f"[bold green]剪贴板监控已启动。[/bold green] 当前项目: [bold cyan]{CONFIG['项目名称']}[/bold cyan] 按 Ctrl+C 停止。", 
        border_style="green",
        box=ROUNDED
    ))
    previous_content = get_clipboard_content()
    
    if previous_content["text"]:
        console.print("[cyan]当前剪贴板文本:[/cyan]")
        console.print(Panel(
            previous_content["text"], 
            border_style="blue",
            box=ROUNDED
        ))
    if previous_content["image"]:
        table = display_image_info(previous_content["image"], is_current=True)
        if table:
            console.print(table)
    
    try:
        # 使用单一的 Live 显示
        with Live(auto_refresh=True, refresh_per_second=4) as live:
            while True:
                current_content = get_clipboard_content()
                
                # 检查文本变化
                if current_content["text"] != previous_content["text"]:
                    console.print("\n[bold cyan]剪贴板文本已更改:[/bold cyan]")
                    console.print(Panel(
                        current_content["text"], 
                        border_style="blue",
                        box=ROUNDED
                    ))
                
                # 检查图片变化
                if current_content["image"] != previous_content["image"]:
                    if current_content["image"]:
                        # 暂停 Live 显示，避免冲突
                        live.stop()
                        
                        console.print("\n[bold cyan]剪贴板中有新图片:[/bold cyan]")
                        
                        table = display_image_info(current_content["image"])
                        if table:
                            console.print(table)
                        
                        # 生成带时间戳的默认文件名
                        timestamp = int(time.time())
                        default_name = f"clipboard_image_{timestamp}"
                        
                        # 询问用户文件名
                        custom_filename = get_filename_from_user(default_name)
                        
                        # 本地保存图片 - 修复文件名重复问题
                        image_path = os.path.join(CONFIG["保存目录"], f"{custom_filename}.png")
                        current_content["image"].save(image_path)
                        console.print(f"图片已本地保存至: [bold green]{image_path}[/bold green]")
                        
                        # 上传到服务器
                        response_data = upload_image_to_server(image_path, custom_filename)
                        
                        # 如果上传成功，记录 URL
                        if response_data:
                            log_image_url(custom_filename, response_data)
                            
                            # 显示上传结果
                            result_table = display_upload_result(response_data, custom_filename)
                            if result_table:
                                console.print(result_table)
                            
                            # 显示分隔线
                            console.print("─" * console.width, style="dim")
                            
                            # 显示历史记录
                            show_history()
                        
                        # 重新启动 Live 显示
                        live.start()
                    else:
                        console.print("\n[yellow]图片已从剪贴板移除[/yellow]")
                
                previous_content = current_content
                time.sleep(CONFIG["检查间隔"])  # 使用配置的检查间隔
    except KeyboardInterrupt:
        console.print("\n[bold red]剪贴板监控已停止。[/bold red]")
        # 显示历史记录
        show_history()

if __name__ == "__main__":
    show_welcome()
    # 获取项目名称
    CONFIG["项目名称"] = get_project_name()
    console.print(f"[bold green]已设置项目名称:[/bold green] [bold cyan]{CONFIG['项目名称']}[/bold cyan]")
    monitor_clipboard() 