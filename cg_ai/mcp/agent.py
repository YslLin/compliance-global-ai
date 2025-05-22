import json
from typing import Any, TypedDict
from langgraph.graph import MessagesState
from datetime import datetime
from langgraph.graph import StateGraph
from langgraph.prebuilt import create_react_agent
import urllib.parse
import os.path

from loguru import logger

MODEL_NAME = os.getenv("MODEL_NAME")
llm = create_react_agent("openai:" + MODEL_NAME)


class State(MessagesState):
    """流转状态"""

    file_url: str
    check_list: list[str]
    content: str
    company_info: dict
    compliance: bool
    non_compliance_items: list[str] = []  # 存储不合规的具体项


def extract_text(state: State):
    """1. 提取文本"""
    logger.info("1. 提取文本")
    file_url = state["file_url"]
    # 获取文件扩展名 - 修复URL解析
    # 解析URL，移除查询参数
    parsed_url = urllib.parse.urlparse(file_url)
    path = parsed_url.path

    # 简单判断文件类型
    if any(ext in file_url.lower() for ext in ["jpg", "jpeg", "png", "bmp"]):
        file_extension = "jpeg"  # 默认作为jpeg处理
    else:
        # 获取实际文件扩展名
        file_extension = os.path.splitext(path)[1].lower().lstrip(".")
        if not file_extension:
            raise ValueError(f"无法识别的文件类型: {file_url}")

    logger.info(f"解析的文件类型: {file_extension}")
    content = ""

    try:
        # 根据文件类型选择不同的提取方式
        if file_extension in ["jpg", "jpeg", "png", "bmp"]:
            logger.info("正在提取图片文本...")
            from cg_ai.mcp.ocr import OCRClient

            # 使用OCR提取图片文本
            content = OCRClient.main(file_url)

        elif file_extension == "pdf":
            logger.info("正在提取PDF文本...")
            from PyPDF2 import PdfReader

            # 使用PDF解析库提取文本
            reader = PdfReader(file_url)
            for page in reader.pages:
                content += page.extract_text()

        elif file_extension in ["doc", "docx"]:
            logger.info("正在提取Word文本...")
            if file_extension == "docx":
                from docx import Document

                # 使用python-docx提取文本
                doc = Document(file_url)
                for para in doc.paragraphs:
                    content += para.text + "\n"
            else:
                # 处理.doc格式
                import textract

                content = textract.process(file_url).decode("utf-8")

        else:
            raise ValueError(f"不支持的文件类型: {file_extension}")

        logger.info(f"content 类型: {type(content)}, 长度: {len(content)}")
        return {"content": str(content)}
    except Exception as e:
        logger.error(f"文本提取失败: {str(e)}")
        raise


def inspect(state: State):
    """3. 检查合规性"""
    logger.info("3. 检查合规性")

    # 构建提示词，将公司信息融入到提示中
    prompt = f"""
    请根据以下信息进行合规性检查，并明确回答"合规"或"不合规"：
    只需要检查以下检查项，不要检查其他内容：
    
    公司信息: {json.dumps(state.get('company_info', {}), ensure_ascii=False)}
    当前日期: {datetime.now().strftime('%Y-%m-%d')}
    文档内容: {state.get('content', '')}
    
    检查项:
    {json.dumps(state['check_list'], ensure_ascii=False)}
    
    你的回答必须以"合规"或"不合规"开头，然后说明理由。
    如果不合规，请在说明后列出具体不合规项，每项一行，以"-"开头。
    
    请严格遵守以下格式：
    合规
    理由：
    或者
    不合规
    理由：
    """

    # 调用LLM进行检查
    llm_response = llm.invoke(prompt)
    response_text = (
        llm_response.content if hasattr(llm_response, "content") else str(llm_response)
    )
    logger.info(response_text)

    # 判断LLM回答是否表示合规
    is_compliant = False
    non_compliance_items = []

    if response_text.strip().startswith("合规"):
        is_compliant = True
    else:
        # 提取不合规项
        lines = response_text.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("-"):
                non_compliance_items.append(line[1:].strip())

    return {"compliance": is_compliant, "non_compliance_items": non_compliance_items}


graph_builder = StateGraph(State)

# 添加 nodes
graph_builder.add_node(extract_text)
# graph_builder.add_node(query_info)
graph_builder.add_node(inspect)

# 添加 edges
graph_builder.set_entry_point("extract_text")
# graph_builder.add_edge("extract_text", "query_info")
graph_builder.add_edge("extract_text", "inspect")

# compile 编译图
graph = graph_builder.compile()

if __name__ == "__main__":
    state = State(
        file_key="1",
        file_url="https://img0.baidu.com/it/u=980771503,1131783134&fm=253&app=120&f=JPEG?w=500&h=667",
        # file_url="https://q2.itc.cn/q_70/images03/20250423/91f6d8873d084e4784abf7806bf9f328.png",
        # file_url="src/data/格灵深瞳：格灵深瞳公司章程.pdf",
        # file_url="src/data/德儒巴-产品宣传单.pdf",
        # file_url="src/data/劳动合同.doc",
        # file_url="src/data/AI生成-数据出境风险自评估报告.docx",
        company_id=1,
        check_list=[
            '检查文档内容中的"公司名称"是否与公司信息一致',
            # "检查有效期是否过期",
        ],
        # content='{ "algo_version": "", "angle": 0, "codes": [ { "data": "", "points": [ { "x": 97, "y": 502 }, { "x": 169, "y": 502 }, { "x": 169, "y": 578 }, { "x": 97, "y": 578 } ], "type": "QRcode" } ], "data": { "title": "营业执照", "creditCode": "510302000014926", "companyName": "自贡市一品堂商贸有限责任公司", "companyType": "有限责任公司(自然人投资或控股)", "businessAddress": "自贡市自流井区五星街西巷12组10号附9号", "legalPerson": "曹文军", "businessScope": "销售预:包装食品兼散装食品(食品流通许可证有效期至2016年2月29日)。销售;蔬菜、水果、工艺品、化妆品、", "registeredCapital": "叁万元人民币", "RegistrationDate": "2013年03月15日", "validPeriod": "2013年03月15日至2033年03月14日", "validFromDate": "20130315", "validToDate": "20330314", "issueDate": "2014年10月28日", "companyForm": "" }, "figure": [ { "type": "round_stamp", "x": 348, "y": 522, "w": 89, "h": 92, "box": { "x": 391, "y": 567, "w": 88, "h": 84, "angle": 89 }, "points": [ { "x": 349, "y": 524 }, { "x": 433, "y": 523 }, { "x": 435, "y": 611 }, { "x": 350, "y": 611 } ] }, { "type": "qrcode", "x": 97, "y": 502, "w": 72, "h": 76, "box": { "x": 132, "y": 539, "w": 69, "h": 73, "angle": 0 }, "points": [ { "x": 98, "y": 504 }, { "x": 168, "y": 503 }, { "x": 167, "y": 576 }, { "x": 97, "y": 576 } ] }, { "type": "blicense_title", "x": 115, "y": 81, "w": 281, "h": 66, "box": { "x": 254, "y": 113, "w": 58, "h": 277, "angle": 88 }, "points": [ { "x": 118, "y": 87 }, { "x": 392, "y": 82 }, { "x": 394, "y": 140 }, { "x": 117, "y": 146 } ] }, { "type": "national_emblem", "x": 206, "y": 14, "w": 95, "h": 51, "box": { "x": 253, "y": 39, "w": 45, "h": 93, "angle": 88 }, "points": [ { "x": 207, "y": 18 }, { "x": 299, "y": 15 }, { "x": 299, "y": 61 }, { "x": 207, "y": 63 } ] } ], "ftype": 0, "height": 667, "orgHeight": 667, "orgWidth": 500, "prism_keyValueInfo": [ { "key": "title", "keyProb": 100, "value": "营业执照", "valuePos": [ { "x": 113, "y": 84 }, { "x": 396, "y": 75 }, { "x": 397, "y": 143 }, { "x": 112, "y": 151 } ], "valueProb": 100 }, { "key": "creditCode", "keyProb": 100, "value": "510302000014926", "valuePos": [ { "x": 322, "y": 166 }, { "x": 434, "y": 164 }, { "x": 434, "y": 176 }, { "x": 322, "y": 178 } ], "valueProb": 100 }, { "key": "companyName", "keyProb": 100, "value": "自贡市一品堂商贸有限责任公司", "valuePos": [ { "x": 197, "y": 206 }, { "x": 378, "y": 202 }, { "x": 378, "y": 216 }, { "x": 197, "y": 220 } ], "valueProb": 100 }, { "key": "companyType", "keyProb": 97, "value": "有限责任公司(自然人投资或控股)", "valuePos": [ { "x": 196, "y": 234 }, { "x": 391, "y": 231 }, { "x": 392, "y": 245 }, { "x": 196, "y": 248 } ], "valueProb": 97 }, { "key": "businessAddress", "keyProb": 100, "value": "自贡市自流井区五星街西巷12组10号附9号", "valuePos": [ { "x": 195, "y": 259 }, { "x": 462, "y": 254 }, { "x": 463, "y": 268 }, { "x": 195, "y": 273 } ], "valueProb": 100 }, { "key": "legalPerson", "keyProb": 100, "value": "曹文军", "valuePos": [ { "x": 196, "y": 292 }, { "x": 237, "y": 291 }, { "x": 237, "y": 305 }, { "x": 196, "y": 306 } ], "valueProb": 100 }, { "key": "businessScope", "keyProb": 100, "value": "销售预:包装食品兼散装食品(食品流通许可证有效期至2016年2月29日)。销售;蔬菜、水果、工艺品、化妆品、", "valuePos": [ { "x": 191, "y": 409 }, { "x": 469, "y": 405 }, { "x": 470, "y": 425 }, { "x": 191, "y": 428 } ], "valueProb": 99 }, { "key": "registeredCapital", "keyProb": 100, "value": "叁万元人民币", "valuePos": [ { "x": 195, "y": 322 }, { "x": 276, "y": 320 }, { "x": 276, "y": 335 }, { "x": 195, "y": 337 } ], "valueProb": 100 }, { "key": "RegistrationDate", "keyProb": 100, "value": "2013年03月15日", "valuePos": [ { "x": 196, "y": 354 }, { "x": 306, "y": 352 }, { "x": 306, "y": 366 }, { "x": 196, "y": 368 } ], "valueProb": 100 }, { "key": "validPeriod", "keyProb": 100, "value": "2013年03月15日至2033年03月14日", "valuePos": [ { "x": 195, "y": 382 }, { "x": 436, "y": 378 }, { "x": 436, "y": 394 }, { "x": 195, "y": 397 } ], "valueProb": 100 }, { "key": "validFromDate", "keyProb": 100, "value": "20130315", "valuePos": [ { "x": 195, "y": 382 }, { "x": 436, "y": 378 }, { "x": 436, "y": 394 }, { "x": 195, "y": 397 } ], "valueProb": 100 }, { "key": "validToDate", "keyProb": 100, "value": "20330314", "valuePos": [ { "x": 195, "y": 382 }, { "x": 436, "y": 378 }, { "x": 436, "y": 394 }, { "x": 195, "y": 397 } ], "valueProb": 100 }, { "key": "issueDate", "keyProb": 100, "value": "2014年10月28日", "valuePos": [ { "x": 335, "y": 617 }, { "x": 448, "y": 617 }, { "x": 449, "y": 627 }, { "x": 335, "y": 628 } ], "valueProb": 100 }, { "key": "companyForm", "keyProb": 100, "value": "", "valueProb": 100 } ], "sliceRect": { "x0": 25, "y0": 22, "x1": 486, "y1": 9, "x2": 500, "y2": 665, "x3": 12, "y3": 667 }, "width": 500 }',
        # company_info={
        #     "company_id": 1,
        #     "company_name": "德儒巴",
        # },
    )
    # extract_text(state)
    # query_info(state)
    # inspect(state)

    # 保存图的图片
    # save_graph_image(graph)

    # 执行图
    result = graph.invoke(state)
    logger.info(result)
