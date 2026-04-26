"""
第二章 2.4.4 MCP的使用 — Weather MCP服务端

【章节学习重点】
- MCP 服务的 HTTP 传输模式：streamable-http，适合独立部署的服务
- 多工具组合：一个 MCP 服务可注册多个相关工具
- 工具间的内部调用：get_current_weather_by_city 组合了 geocode_city 和 get_current_weather

【代码功能】
创建一个名为 "Weather" 的 MCP 服务，提供三个天气相关工具：
1. geocode_city: 城市名 → 经纬度
2. get_current_weather: 经纬度 → 天气信息
3. get_current_weather_by_city: 城市名 → 天气信息（组合前两个工具）
使用 streamable-http 传输协议，作为独立 HTTP 服务运行。

【实现思路】
1. 使用 FastMCP("Weather") 创建服务
2. 注册三个工具，第三个工具内部调用前两个实现完整流程
3. 使用 Open-Meteo 公共 API（无需 API Key）获取地理编码和天气数据
4. mcp.run(transport="streamable-http") 启动 HTTP 服务，默认端口 8000

【关键参数说明】
- OPEN_METEO_GEOCODE_URL: 地理编码 API，将城市名转为经纬度
- OPEN_METEO_WEATHER_URL: 天气查询 API，根据经纬度获取天气
- transport="streamable-http": HTTP 传输模式，端点路径为 /mcp
- httpx.Client: HTTP 客户端，用于调用 Open-Meteo API
- language="zh": 地理编码默认使用中文返回结果

【应用场景】
- 天气查询服务的标准化暴露
- 多个 Agent 共享同一套天气查询能力
- 演示 MCP 服务的 HTTP 部署模式
"""
from mcp.server.fastmcp import FastMCP
import httpx
from typing import Dict, Any, Optional

mcp = FastMCP("Weather")

OPEN_METEO_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
OPEN_METEO_GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"

@mcp.tool()
def geocode_city(name: str, country: Optional[str] = None, language: str = "zh") -> Dict[str, Any]:
    """将城市名解析为经纬度"""
    params = {"name": name, "count": 1, "language": language, "format": "json"}
    if country:
        params["country"] = country
    with httpx.Client(timeout=10) as client:
        r = client.get(OPEN_METEO_GEOCODE_URL, params=params)
        r.raise_for_status()
        data = r.json()
    results = data.get("results") or []
    if not results:
        return {"error": f"未找到城市：{name}"}
    top = results[0]
    return {
        "name": top.get("name"),
        "lat": top.get("latitude"),
        "lon": top.get("longitude"),
        "country": top.get("country"),
    }

@mcp.tool()
def get_current_weather(lat: float, lon: float) -> Dict[str, Any]:
    """根据经纬度查询当前天气"""
    params = {"latitude": lat, "longitude": lon, "current_weather": True}
    with httpx.Client(timeout=10) as client:
        r = client.get(OPEN_METEO_WEATHER_URL, params=params)
        r.raise_for_status()
        payload = r.json()
    cw = payload.get("current_weather") or {}
    return {
        "latitude": lat,
        "longitude": lon,
        "temperature": cw.get("temperature"),
        "windspeed": cw.get("windspeed"),
        "weathercode": cw.get("weathercode"),
        "time": cw.get("time"),
    }

@mcp.tool()
def get_current_weather_by_city(name: str, country: Optional[str] = None, language: str = "zh") -> Dict[str, Any]:
    """城市名 -> 当前天气（内部先地理编码再查询天气）"""
    g = geocode_city(name=name, country=country, language=language)
    if "error" in g:
        return g
    w = get_current_weather(lat=g["lat"], lon=g["lon"])
    return {**g, **w}

if __name__ == "__main__":
    print("Starting Weather MCP Server (streamable-http) on http://localhost:8000/mcp ...")
    mcp.run(transport="streamable-http")
