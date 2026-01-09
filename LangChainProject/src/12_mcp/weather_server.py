from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "Weather",
    host="0.0.0.0",
    port=8100
    ) # 외부에서 이 툴에 접근할 수 있도록 세팅

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for a location"""
    return "석촌역의 날씨는 비옵니다."

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http"
    )