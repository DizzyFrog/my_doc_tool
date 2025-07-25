import sys
import os

def resource_path(relative_path):
    """
    获取资源文件的绝对路径，兼容 PyInstaller 打包和开发环境
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path) 