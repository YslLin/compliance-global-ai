import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

MODEL_NAME = os.getenv("MODEL_NAME")


async def main():
    client = MultiServerMCPClient(
        {
            "compliance": {
                "command": "uv",
                "args": [
                    "--directory",
                    "/Users/silvayang/Documents/PycharmProjects/my-projects/compliance-global-ai/compliance_global_ai/",
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
    tools = await client.get_tools()
    for tool in tools:
        if tool.name == "inspect":
            print(tool.name)
            print(tool.description)
            args = {
                "file_url": "https://img0.baidu.com/it/u=980771503,1131783134&fm=253&app=120&f=JPEG?w=500&h=667",
                "company_info": {"name": "自贡市一品堂商贸有限责任公司"},
                "check_items": ["name_check"],
            }
            result = await tool.ainvoke(args)
            print(result)

    # agent = create_react_agent(MODEL_NAME, tools)
    # math_response = await agent.ainvoke(
    #     {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    # )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
