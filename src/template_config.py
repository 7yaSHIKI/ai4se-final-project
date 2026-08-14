"""
模板配置
解决循环导入问题：独立配置 Jinja2Templates
"""
from fastapi.templating import Jinja2Templates

# 配置模板
templates = Jinja2Templates(directory="src/templates")
