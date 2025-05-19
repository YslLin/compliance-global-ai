import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import json
from mcp.server.fastmcp import FastMCP
from mcp.server import stdio
from src import agent

FILE_KEY_CHECK_ITEMS = {
    "name_check": '检查文档内容中的"公司名称"是否与公司信息一致',
    "valid_period_check": '检查文档内容中的"有效期"是否过期',
}

# 初始化FastMCP服务器
mcp = FastMCP("compliance")


@mcp.tool()
async def inspect(file_url: str, company_info: dict, check_items: list[str]) -> str:
    """执行文件合规检查，返回合规检查结果

    参数:
        file_url: 文件的url
        company_info: 公司信息
        check_items: 检查项

    返回:
        compliance: 是否合规
        non_compliance_items: 不合规项
    """
    result = {"compliance": False, "non_compliance_items": []}
    check_list = []
    for check_item in check_items:
        if check_item not in FILE_KEY_CHECK_ITEMS:
            result["non_compliance_items"] = ["检查项不存在"]
            return json.dumps(result, ensure_ascii=False)

        check_list.append(FILE_KEY_CHECK_ITEMS[check_item])

    if not check_list:
        result["non_compliance_items"] = ["检查项不存在"]
        return json.dumps(result, ensure_ascii=False)

    state = agent.State(
        file_url=file_url,
        company_info=company_info,
        check_list=check_list,
    )

    # 执行图
    response = agent.graph.invoke(state)
    result["compliance"] = response["compliance"]
    result["non_compliance_items"] = response["non_compliance_items"]
    return json.dumps(result, ensure_ascii=False)


async def main() -> None:
    """Main entry point for the package when run as a module."""
    await mcp.run(transport="stdio")


if __name__ == "__main__":

    # 如果要使用stdio方式（适用于本地开发和测试）
    mcp.run(transport="stdio")

    # import asyncio
    # result = asyncio.run(
    #     inspect(
    #         "1",
    #         "https://img0.baidu.com/it/u=980771503,1131783134&fm=253&app=120&f=JPEG?w=500&h=667",
    #         {"name": "自贡市一品堂商贸有限责任公司"},
    #     )
    # )
    # print(result)
