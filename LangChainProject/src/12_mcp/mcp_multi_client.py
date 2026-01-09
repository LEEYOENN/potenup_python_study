import asyncio
import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()

# 실제 실행 파트 작성
async def main():
    print("멀티 클라이언트 세팅중...")

    client = MultiServerMCPClient(
        {
            "Math" : {
                "command" : "python",
                "args" : [r"C:\Users\user\potenup\python7month\LangChainProject\src\12_mcp\odd_math_server.py"],
                "transport" : "stdio"
            },
            "Weather" : {
                "url" : "http://localhost:8100/mcp",
                "transport" : "streamable_http"
            },
            # "mcp_weather_server": {
            #     "transport": "stdio",
            #     "command": "npx",
            #     "args": [
            #         "-y",
            #         "@smithery/cli@latest",
            #         "run",
            #         "@isdaniel/mcp_weather_server",
            #         "--key", "b633f6f2-8119-4cf0-a22d-27097bef9530",
            #         "--profile", "economic-leopon-VNf7M9",
            #     ],
            # }
        }

    )
    
    tools = await client.get_tools()
    for item in tools:
        print("가져온 도구는:", item.name)
    
    # Agent 만들기
    model = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0
    )

    agent_excutor = create_react_agent(
        model,
        tools
    )
########################################################################

    # 더하기 도구 체크
    response = await agent_excutor.ainvoke(
        {"messages": [HumanMessage(content="1+2를 이상하게 계산하면?")]}
    )

    print(response["messages"][-1].content)

    # 곱하기 도구 체크
    response = await agent_excutor.ainvoke(
        {"messages": [HumanMessage(content="1*2를 이상하게 계산하면?")]}
    )

    print(response["messages"][-1].content)

    # 날씨 도구 체크
    response = await agent_excutor.ainvoke(
        {"messages": [HumanMessage(content="석촌역의 날씨는?")]}
    )

    print(response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
