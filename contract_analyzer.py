import openai
from typing import Dict, List, Any
import json
import re
from config import Config

class ContractAnalyzer:
    def __init__(self):
        self.client = openai.OpenAI(
            base_url=Config.MODELSCOPE_BASE_URL,
            api_key=Config.MODELSCOPE_API_KEY
        )
        
    def analyze_contract(self, contract_text: str) -> Dict[str, Any]:
        """分析合同文本并返回结构化结果"""
        
        prompt = f"""
        作为专业的合同审查专家，请仔细分析以下合同内容，并提供详细的分析报告。
        
        合同内容：
        {contract_text}
        
        请按以下JSON格式返回分析结果：
        {{
            "summary": "合同总体概述",
            "risks": [
                {{
                    "type": "风险类型",
                    "description": "风险描述",
                    "severity": "高/中/低",
                    "clause": "相关条款",
                    "suggestion": "修改建议"
                }}
            ],
            "missing_clauses": [
                {{
                    "clause": "缺失条款名称",
                    "importance": "重要性级别",
                    "recommendation": "建议添加的内容"
                }}
            ],
            "compliance_score": 85,
            "key_points": ["要点1", "要点2"]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=Config.MODEL_NAME,
                messages=[
                    {"role": "system", "content": "你是一个专业的合同审查专家，具有丰富的法律知识和实践经验。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            result = response.choices[0].message.content
            # 清理可能的markdown格式
            result = re.sub(r'```json\n|\n```', '', result).strip()
            return json.loads(result)
            
        except Exception as e:
            return {
                "error": f"分析失败: {str(e)}",
                "summary": "无法分析合同",
                "risks": [],
                "missing_clauses": [],
                "compliance_score": 0,
                "key_points": []
            }
    
    def get_clause_suggestions(self, clause_type: str, context: str) -> List[str]:
        """获取特定条款的改进建议"""
        
        prompt = f"""
        针对以下{clause_type}条款，请提供3-5条具体的改进建议：
        
        当前条款内容：
        {context}
        
        请以简洁的要点形式返回建议。
        """
        
        try:
            response = self.client.chat.completions.create(
                model=Config.MODEL_NAME,
                messages=[
                    {"role": "system", "content": "你是合同条款优化专家"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=500
            )
            
            suggestions = response.choices[0].message.content.strip().split('\n')
            return [s.strip('- ').strip() for s in suggestions if s.strip()]
            
        except Exception:
            return ["建议获取失败，请稍后重试"]