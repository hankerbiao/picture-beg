import requests
import logging
import json
from typing import Generator, Dict, Any
import sseclient

# 创建日志记录器
logger = logging.getLogger("ai_processor")


class AIProcessor:
    """AI文本处理类"""

    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model
        logger.info(f"初始化AI处理器: {base_url}, 模型: {model}")

    def process_text(self, text: str, enter_text=None) -> str:
        """
        使用AI模型处理文本
        
        Args:
            text: 要处理的文本
            enter_text: 额外的文本输入（未使用，但保留接口一致性）
            
        Returns:
            处理后的文本
        """
        if not text or len(text.strip()) == 0:
            logger.warning("输入文本为空")
            return ""

        try:

            prompt = f"""
请根据以下要求和参考示例，优化所提供文本的格式。

**核心要求：**
1.  **保留原文核心内容**：除了明确指示需要移除的内容外，不得修改文本的原始语句和核心信息。
2.  **优化排版与可读性**：重点在于调整各级标题、段落结构和列表格式，使其清晰、规范、易读。

**必须移除的内容 (不应出现在最终输出中)：**
1.  **页码标识**：例如 “第 n 页”、“第n页 共n页” 或任何类似的页码信息。
2.  **文档元数据/辅助信息**：例如 “变更记录”、“修订历史”、“制定日期”、“生效日期”、“版本号”、“目录”等部分。如果这些信息作为独立的章节或段落出现，请直接删除。

**格式优化细节 (请严格参考提供的示例)：**
1.  **层级标题**：确保各级标题（如 `### 1.` 和 `#### 1.1.`）结构清晰，层级分明。
2.  **段落划分**：合理划分段落，确保每个段落讨论一个核心点。
3.  **列表项**：
    * 主要列表项使用 `- **加粗文本**` 的格式。
    * 次级列表项（如对主要列表项的解释或示例）使用 `o 普通文本` 并进行适当缩进。

**参考格式示例：**
---

### 1. 投标项目管理的目的

#### 1.1. 提高中标概率

- **精准响应招标文件**
  o 仔细研究招标文件的要求，包括技术规格、商务条款、交付期限等，确保投标文件能够准确、全面地响应这些要求。通过精心准备投标文件，展示公司的实力和优势，增加评委对投标方案的认可度。
  o 例如，在项目投标中，对招标文件中规定的软硬件技术参数、质量标准等进行详细分析，制定针对性的解决方案，以提高中标可能性。

- **突出竞争优势**
  o 分析竞争对手的情况，找出自身的独特优势和差异化竞争点。在投标文件中重点突出这些优势，如先进的技术、丰富的经验、良好的口碑等，使公司在众多投标者中脱颖而出。
  o 比如，在同类型项目投标中，强调公司拥有完整的可切和客户实际需求的方案、高效的项目管理团队以及成功的类似项目案例。
---

请开始处理以下文本：
{text}
"""

            if enter_text:
                prompt += f"\n\n下面内容为重要的链接信息，追加到正文后面：\n{enter_text}"
            print(prompt)
            # 构建API请求
            headers = {
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 1024 * 130
            }

            logger.info(f"发送请求到AI模型: {self.model}")
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )

            # 检查响应
            if response.status_code == 200:
                result = response.json()
                processed_text = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                logger.info(f"AI处理成功，输出长度: {len(processed_text)}")
                return processed_text
            else:
                logger.error(f"AI处理失败: HTTP {response.status_code}, {response.text}")
                return f"AI处理失败: {response.status_code}"

        except Exception as e:
            logger.error(f"AI处理异常: {str(e)}")
            return f"处理文本时出错: {str(e)}"
