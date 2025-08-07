import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ModelScope API配置
    MODELSCOPE_API_KEY = os.getenv('MODELSCOPE_API_KEY', 'your_api_key_here')
    MODELSCOPE_BASE_URL = 'https://api-inference.modelscope.cn/v1'
    MODEL_NAME = 'ZhipuAI/GLM-4.5'
    
    # 应用配置
    APP_TITLE = "智能合同审查助手"
    APP_DESCRIPTION = "基于AI的合同风险分析与建议系统"
    
    # 文件上传配置
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.doc', '.txt']