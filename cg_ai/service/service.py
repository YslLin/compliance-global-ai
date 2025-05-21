import json
from typing import Any
import httpx
from pydantic import BaseModel
from loguru import logger

from cg_ai.models.schema import CompanyInfo, FileInfo
from cg_ai.config.config import file_check, java_api




class ApiResponse(BaseModel):
    """API 响应数据模型"""

    code: int
    msg: str
    data: Any


def get_company_info(company_id: int) -> CompanyInfo:
    """查询公司信息"""
    logger.info(f"查询公司信息: {company_id}")

    try:
        # 构建请求参数
        params = {"customerId": company_id}

        # 构建请求头
        headers = {
            "Content-Type": "application/json",
            # "Authorization": f"Bearer {state.get('api_token', '')}"
        }

        # API 端点
        api_url = f"{java_api['base_url']}{java_api['get_company_info']}"

        # 使用 httpx 同步方式发送 HTTP 请求
        with httpx.Client() as client:
            response = client.get(
                url=api_url, params=params, headers=headers, timeout=10.0
            )
            response.raise_for_status()
            # 解析响应内容
            result = response.json()
            # 使用 Pydantic 模型验证响应数据
            validated_response = ApiResponse.model_validate(result)

            # 处理响应数据
            if validated_response.code != 200:
                logger.error(validated_response.msg)
                return None

            # 更新状态
            company_info = CompanyInfo(**validated_response.data)
            logger.info(f"company_info: {company_info}")
            return company_info
    except httpx.HTTPError as e:
        # 处理 HTTP 错误
        logger.error(f"HTTP 请求错误: {str(e)}")
        return None
    except Exception as e:
        # 处理其他异常
        logger.error(f"处理数据时出错: {str(e)}")
        return None


def get_file_info(examine_id: int) -> list[FileInfo]:
    """查询文件检查信息"""
    logger.info(f"查询文件检查信息: {examine_id}")

    try:

        # 构建请求参数
        params = {"examineId": examine_id}

        # 构建请求头
        headers = {
            "Content-Type": "application/json",
            # "Authorization": f"Bearer {state.get('api_token', '')}"
        }

        # API 端点
        api_url = f"{java_api['base_url']}{java_api['get_file_info']}"

        # 使用 httpx 同步方式发送 HTTP 请求
        with httpx.Client() as client:
            response = client.get(
                url=api_url, params=params, headers=headers, timeout=10.0
            )
            response.raise_for_status()
            # 解析响应内容
            result = response.json()
            # 使用 Pydantic 模型验证响应数据
            validated_response = ApiResponse.model_validate(result)

            # 处理响应数据
            if validated_response.code != 200:
                logger.error(validated_response.msg)
                return None

            # 更新状态
            file_info_list = [FileInfo(**item) for item in validated_response.data]
            logger.info(f"file_info: {file_info_list}")
            return file_info_list
    except httpx.HTTPError as e:
        # 处理 HTTP 错误
        logger.error(f"HTTP 请求错误: {str(e)}")
        return None
    except Exception as e:
        # 处理其他异常
        logger.error(f"处理数据时出错: {str(e)}")
        return None


def save_compliance_result(
    company_id: int, examine_id: int, compliance_result: list[FileInfo]
) -> bool:
    """保存合规结果"""
    logger.info(f"保存合规结果: {company_id}, {examine_id}, {compliance_result}")

    try:
        # 将 FileInfo 对象列表转换为字典列表
        # compliance_result_dict = [item.model_dump() for item in compliance_result]

        # 构建请求参数
        params = [item.model_dump() for item in compliance_result]

        # 构建请求头
        headers = {
            "Content-Type": "application/json",
            # "Authorization": f"Bearer {state.get('api_token', '')}"
        }

        # API 端点
        api_url = f"{java_api['base_url']}{java_api['save_compliance_result']}"

        # 使用 httpx 同步方式发送 HTTP 请求
        with httpx.Client() as client:
            response = client.post(
                url=api_url, json=params, headers=headers, timeout=10.0
            )
            response.raise_for_status()
            # 解析响应内容
            result = response.json()
            # 使用 Pydantic 模型验证响应数据
            validated_response = ApiResponse.model_validate(result)

            # 处理响应数据
            if validated_response.code != 200:
                logger.error(validated_response.msg)
                return None

            # 更新状态
            logger.info(f"保存合规结果成功")
            return True
    except httpx.HTTPError as e:
        # 处理 HTTP 错误
        logger.error(f"HTTP 请求错误: {str(e)}")
        return False
    except Exception as e:
        # 处理其他异常
        logger.error(f"处理数据时出错: {str(e)}")
        return False


def compliance_file(
    examine_id: int, company_info: CompanyInfo, file_info_list: list[FileInfo]
) -> list[FileInfo]:
    from cg_ai.mcp.client import mcp_client

    """合规文件"""
    logger.info("合规文件")

    try:
        for file_info in file_info_list:
            try:
                file_type = str(file_info.fileId)
                if file_type not in file_check:
                    logger.error(f"文件类型 {file_type} 不存在")
                    file_info.resultStatus = "fail"
                    file_info.resultDesc = "文件类型不存在"
                    continue

                check_items = file_check[file_type]
                result = mcp_client.run_tool(
                    "inspect",
                    {
                        "file_url": file_info.fileUrl,
                        "company_info": company_info,
                        "check_items": check_items,
                    },
                )
                result = json.loads(result)
                logger.info(
                    f"文件类型 {file_type} 合规结果: {json.dumps(result, ensure_ascii=False)}"
                )
                file_info.resultStatus = "success" if result["compliance"] else "fail"
                file_info.resultDesc = "\n".join(result["non_compliance_items"]) if result["non_compliance_items"] else ""
            except Exception as e:
                logger.error(f"合规异常: {str(e)}")
                file_info.resultStatus = "fail"
                file_info.resultDesc = "合规异常"

        save_result = save_compliance_result(
            company_info.id, examine_id, file_info_list
        )
        if not save_result:
            logger.error("保存合规结果失败")
            return None
    except Exception as e:
        logger.error(f"处理数据时出错: {str(e)}")
        return None

    return file_info_list
