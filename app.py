import streamlit as st
import os
from pathlib import Path
import PyPDF2
import docx
from contract_analyzer import ContractAnalyzer
from config import Config
import plotly.graph_objects as go
import plotly.express as px

# 页面配置
st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .risk-card {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .high-risk {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
    }
    .medium-risk {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
    }
    .low-risk {
        background-color: #e8f5e8;
        border-left: 5px solid #4caf50;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 初始化分析器
@st.cache_resource
def init_analyzer():
    try:
        analyzer = ContractAnalyzer()
        # 测试连接
        if not analyzer.test_connection():
            st.error("API连接失败，请检查配置")
            return None
        return analyzer
    except Exception as e:
        st.error(f"初始化失败: {str(e)}")
        return None

analyzer = init_analyzer()

# 如果分析器初始化失败，显示错误信息并停止执行
if analyzer is None:
    st.stop()

# 文件处理函数
def read_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"读取PDF失败: {e}")
        return ""

def read_docx(file):
    try:
        doc = docx.Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        st.error(f"读取Word文档失败: {e}")
        return ""

def read_txt(file):
    try:
        return file.read().decode('utf-8')
    except UnicodeDecodeError:
        return file.read().decode('gb2312')

# 主界面
st.markdown('<h1 class="main-header">📋 智能合同审查助手</h1>', unsafe_allow_html=True)
st.markdown("**基于AI的合同风险分析与建议系统**")

# 侧边栏
with st.sidebar:
    st.header("🔧 功能菜单")
    
    # 文件上传
    uploaded_file = st.file_uploader(
        "上传合同文件",
        type=['pdf', 'docx', 'doc', 'txt'],
        help="支持PDF、Word和文本格式"
    )
    
    if uploaded_file is not None:
        file_size = len(uploaded_file.getbuffer())
        if file_size > Config.MAX_FILE_SIZE:
            st.error("文件过大，请上传小于10MB的文件")
        else:
            st.success(f"✅ 已上传: {uploaded_file.name}")
    
    # 分析选项
    st.subheader("⚙️ 分析选项")
    detail_level = st.select_slider(
        "分析详细程度",
        options=["快速", "标准", "深度"],
        value="标准"
    )
    
    analyze_button = st.button("🔍 开始分析", type="primary", use_container_width=True)

# 主内容区域
col1, col2 = st.columns([2, 1])

with col1:
    if uploaded_file is not None:
        st.subheader("📄 合同预览")
        
        # 读取文件内容
        file_extension = Path(uploaded_file.name).suffix.lower()
        contract_text = ""
        
        if file_extension == '.pdf':
            contract_text = read_pdf(uploaded_file)
        elif file_extension in ['.docx', '.doc']:
            contract_text = read_docx(uploaded_file)
        elif file_extension == '.txt':
            contract_text = read_txt(uploaded_file)
        
        if contract_text:
            # 显示预览（前1000字符）
            preview_text = contract_text[:1000] + "..." if len(contract_text) > 1000 else contract_text
            st.text_area("合同内容预览", preview_text, height=300)
            
            # 分析合同
            if analyze_button:
                with st.spinner("🤖 AI正在分析合同，请稍候..."):
                    analysis_result = analyzer.analyze_contract(contract_text)
                    
                if "error" not in analysis_result:
                    st.session_state['analysis'] = analysis_result
                    st.success("✅ 分析完成！")
                else:
                    st.error(f"分析失败: {analysis_result['error']}")

with col2:
    st.subheader("📊 分析结果")
    
    if 'analysis' in st.session_state:
        analysis = st.session_state['analysis']
        
        # 合规性评分
        score = analysis.get('compliance_score', 0)
        st.markdown(f"""
        <div class="metric-card">
            <h3>合规性评分</h3>
            <h1>{score}%</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # 风险统计
        risks = analysis.get('risks', [])
        risk_counts = {'高': 0, '中': 0, '低': 0}
        for risk in risks:
            risk_counts[risk.get('severity', '中')] += 1
        
        fig = go.Figure(data=[
            go.Bar(x=list(risk_counts.keys()), y=list(risk_counts.values()),
                   marker_color=['#f44336', '#ff9800', '#4caf50'])
        ])
        fig.update_layout(title="风险等级分布", height=200)
        st.plotly_chart(fig, use_container_width=True)

# 详细分析结果
if 'analysis' in st.session_state:
    analysis = st.session_state['analysis']
    
    st.subheader("📋 详细分析报告")
    
    # 合同概述
    with st.expander("📝 合同概述", expanded=True):
        st.write(analysis.get('summary', '暂无概述'))
    
    # 风险分析
    risks = analysis.get('risks', [])
    if risks:
        st.subheader("⚠️ 风险分析")
        for risk in risks:
            severity_class = {
                '高': 'high-risk',
                '中': 'medium-risk',
                '低': 'low-risk'
            }.get(risk.get('severity', '中'), 'medium-risk')
            
            st.markdown(f"""
            <div class="risk-card {severity_class}">
                <h4>{risk.get('type', '未知风险')}</h4>
                <p><strong>严重程度：</strong>{risk.get('severity', '中')}</p>
                <p><strong>相关条款：</strong>{risk.get('clause', '未指定')}</p>
                <p><strong>描述：</strong>{risk.get('description', '无描述')}</p>
                <p><strong>建议：</strong>{risk.get('suggestion', '无建议')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # 缺失条款
    missing_clauses = analysis.get('missing_clauses', [])
    if missing_clauses:
        st.subheader("🔍 建议添加的条款")
        for clause in missing_clauses:
            st.info(f"**{clause.get('clause', '未知条款')}** - {clause.get('recommendation', '无建议')}")
    
    # 关键要点
    key_points = analysis.get('key_points', [])
    if key_points:
        st.subheader("🔑 关键要点")
        for point in key_points:
            st.success(f"• {point}")

# 底部信息
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>💡 提示：上传合同文件后点击"开始分析"即可获得AI驱动的专业合同审查报告</p>
    <p>技术支持：ModelScope 开源大模型 | 界面：Streamlit</p>
</div>
""", unsafe_allow_html=True)
