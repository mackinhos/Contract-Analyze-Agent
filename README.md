# 智能合同审查agent

## 项目简介

智能合同审查agent是一个基于人工智能的合同风险分析与建议系统。该应用使用Streamlit构建用户界面，集成了目前领先的AI大模型来自动分析合同文档，识别潜在风险，并提供专业的修改建议。该系统还提供了合同合规性评分功能，帮助用户评估合同的法律合规性。


## 功能特性

### 🎯 核心功能
- **智能合同分析**：使用AI模型深度分析合同内容
- **风险评估**：自动识别高、中、低三个等级的风险点
- **合规性评分**：为合同提供0-100分的合规性评分
- **可视化展示**：通过图表直观展示风险分布和评分结果
- **详细报告**：生成包含合同概述、风险分析、缺失条款的完整报告

### 📄 文件支持
- **PDF格式**：支持PDF文档的文本提取和分析
- **Word文档**：支持.docx和.doc格式的Word文档
- **文本文件**：支持.txt格式的纯文本文件
- **文件大小限制**：最大支持10MB的文件上传

### 🎨 用户界面
- **响应式设计**：适配不同屏幕尺寸
- **直观操作**：简洁的用户界面，易于使用
- **实时预览**：上传文件后即时显示内容预览
- **交互式图表**：使用Plotly提供交互式数据可视化

## 技术架构

### 🛠️ 技术栈
- **前端框架**：Streamlit
- **AI模型**：强大开源大模型（GLM-4.5）
- **文档处理**：PyPDF2, python-docx
- **数据可视化**：Plotly
- **配置管理**：python-dotenv

### 📁 项目结构
```
contract-agent/
├── app.py                 # 主应用程序文件
├── config.py             # 配置文件
├── contract_analyzer.py  # 合同分析核心模块
├── requirements.txt      # 依赖列表
└── README.md            # 项目文档
```

## 安装说明

### 📋 环境要求
- Python 3.8+
- 200MB以上可用磁盘空间
- 稳定的网络（用于API调用和依赖下载安装）

### 🚀 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd contract-agent
   ```

2. **创建虚拟环境**（推荐）
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **配置环境变量**
- 直接修改config.py，将第8行的 `'your_api_key_here'` 替换为你的真实API密钥
- 或者创建 `.env` 文件并添加以下内容：
   ```env
   MODELSCOPE_API_KEY=your_api_key_here
   ```

## 使用说明

### 🏃 运行应用

在项目根目录下运行：
```bash
streamlit run app.py
```

应用将在浏览器中自动打开，默认本地地址为 `http://localhost:8501`

### 📖 使用流程

1. **上传合同文件**
   - 点击侧边栏的文件上传按钮
   - 选择支持的文件格式（PDF、Word、TXT）
   - 文件大小需小于10MB

2. **配置分析选项**
   - 选择分析详细程度：快速、标准、深度
   - 点击"开始分析"按钮

3. **查看分析结果**
   - **合同预览**：显示上传合同的文本内容预览
   - **合规性评分**：显示AI对合同的合规性评分
   - **风险分布图**：可视化展示不同等级风险的数量分布
   - **详细报告**：包含合同概述、风险分析、缺失条款等完整信息

### 📊 分析报告内容

#### 合同概述
- 合同总体描述
- 主要条款总结
- 关键信息提取

#### 风险分析
- **风险类型**：识别的具体风险类别
- **风险描述**：详细的风险说明
- **风险等级**：高、中、低三个等级
- **相关条款**：风险对应的合同条款
- **修改建议**：针对风险的具体改进建议

#### 缺失条款
- **缺失条款名称**：合同中缺少的重要条款
- **重要性级别**：条款的重要程度
- **建议内容**：建议添加的具体条款内容

## 配置说明

### ⚙️ 主要配置项

在 `config.py` 文件中可以配置以下参数：

```python
class Config:
    # ModelScope API配置
    MODELSCOPE_API_KEY = os.getenv('MODELSCOPE_API_KEY')
    MODELSCOPE_BASE_URL = 'https://api-inference.modelscope.cn/v1'
    MODEL_NAME = 'ZhipuAI/GLM-4.5'
    
    # 应用配置
    APP_TITLE = "智能合同审查助手"
    APP_DESCRIPTION = "基于AI的合同风险分析与建议系统"
    
    # 文件上传配置
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.doc', '.txt']
```

### 🔧 自定义配置

1. **修改API密钥**：在 `.env` 文件中设置自己的ModelScope API密钥
2. **调整文件大小限制**：修改 `MAX_FILE_SIZE` 参数
3. **更改AI模型**：修改 `MODEL_NAME` 参数
4. **自定义应用信息**：修改 `APP_TITLE` 和 `APP_DESCRIPTION`

## API集成

### 🔑 ModelScope API

本项目使用ModelScope平台提供的大模型服务，集成了ZhipuAI的GLM-4.5模型进行合同分析。

#### API配置
- **Base URL**: `https://api-inference.modelscope.cn/v1`
- **模型名**: `ZhipuAI/GLM-4.5`
- **认证方式**: API Key

#### 获取API密钥
1. 访问 [ModelScope官网](https://modelscope.cn/)
2. 注册并登录账号
3. 在控制台中创建API密钥
4. 将密钥配置到 `.env` 文件中

## 故障排除

### ❗ 常见问题

#### 1. 文件上传失败
- **问题**：上传文件时提示"文件过大"
- **解决**：确保文件大小小于10MB，超过需要修改配置中的 `MAX_FILE_SIZE`

#### 2. 分析失败
- **问题**：点击分析按钮后显示错误信息
- **解决**：
  - 检查网络连接
  - 验证API密钥是否正确配置
  - 确认API服务是否正常

#### 3. PDF文件读取失败
- **问题**：上传PDF文件后无法读取内容
- **解决**：
  - 确保PDF文件不是扫描件（图片格式）
  - 检查PDF文件是否损坏
  - 尝试重新转换PDF格式

#### 4. API调用超时
- **问题**：分析过程中出现超时错误
- **解决**：
  - 检查网络连接稳定性
  - 减少合同文本长度
  - 选择"快速"分析模式

### 🐛 调试模式

如需启用调试模式，可以在应用运行时查看终端输出的错误信息，或修改代码中的日志级别。

## 开发说明

### 🔄 代码结构

#### `app.py` - 主应用程序
- Streamlit应用入口
- 用户界面构建
- 文件处理逻辑
- 结果展示逻辑

#### `config.py` - 配置管理
- 应用配置参数
- API配置
- 环境变量管理

#### `contract_analyzer.py` - 核心分析模块
- AI模型集成
- 合同分析逻辑
- 结果格式化
- 错误处理

### 🧪 扩展功能

#### 如何添加新的文件格式支持
1. 在 `app.py` 中添加新的文件读取函数
2. 在 `config.py` 中更新 `ALLOWED_EXTENSIONS`
3. 在文件上传组件中添加新的文件类型

#### 自定义AI模型
1. 在 `config.py` 中修改 `MODEL_NAME`
2. 在 `contract_analyzer.py` 中调整提示词模板
3. 根据新模型的输出格式调整结果解析逻辑

#### 增加新的分析维度
1. 在 `ContractAnalyzer.analyze_contract` 方法中扩展提示词
2. 更新结果展示逻辑
3. 添加相应的可视化组件

## 许可证

本项目采用 MIT 许可证。详情请参阅 LICENSE 文件。

## 贡献指南

我们欢迎社区贡献！如果您想要为项目做出贡献，请遵循以下步骤：

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 更新日志

### v1.0.0 
- 初始版本发布
- 支持PDF、Word、TXT文件格式
- 集成AI合同分析功能
- 提供风险评分和可视化展示

---

**注意**：本工具提供的分析结果仅供参考，不构成法律建议。重要的合同决策请咨询专业法律人士。
        