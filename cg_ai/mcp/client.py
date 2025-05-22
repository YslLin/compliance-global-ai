"""mcp 客户端"""

import asyncio
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from loguru import logger

MODEL_NAME = os.getenv("MODEL_NAME")


class MCPClient:

    def __init__(self):
        self.client = MultiServerMCPClient(
            {
                "compliance": {
                    "command": "uv",
                    "args": [
                        "--directory",
                        "/Users/silvayang/Documents/PycharmProjects/my-projects/compliance-global-ai/cg_ai/mcp/",
                        "run",
                        "server.py",
                    ],
                    "env": {
                        "MODEL_NAME": MODEL_NAME,
                        "OPENAI_BASE_URL": os.getenv("OPENAI_BASE_URL"),
                        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
                        "OCR_ACCESS_KEY_ID": os.getenv("OCR_ACCESS_KEY_ID"),
                        "OCR_ACCESS_KEY_SECRET": os.getenv("OCR_ACCESS_KEY_SECRET"),
                    },
                    "description": "mcp 服务，合规检查",
                    "transport": "stdio",
                }
            }
        )

        self.tools = asyncio.run(self.client.get_tools())

        self.agent = create_react_agent("openai:" + MODEL_NAME, self.tools)

    def get_tools(self):
        return self.tools

    def invoke(self, prompt: str):
        response = asyncio.run(
            self.agent.ainvoke({"messages": [{"role": "user", "content": prompt}]})
        )
        return response

    def run_tool(self, tool_name: str, args: dict):
        for tool in self.tools:
            if tool.name == tool_name:
                logger.info(f"LLM: {MODEL_NAME}, 执行工具: {tool_name}")
                return asyncio.run(tool.ainvoke(args))
        raise ValueError(f"Tool {tool_name} not found")


mcp_client = MCPClient()

if __name__ == "__main__":

    # prompt = f"what's (3 + 5) x 12?"
    # print(mcp_client.invoke(prompt))
    result = mcp_client.run_tool(
        "inspect",
        {
            "file_url": "https://www.baidu.com",
            "company_info": {"name": "test"},
            "check_items": ["name_check", "valid_period_check"],
        },
    )
    print(result)
