"""
第二章 2.5.3 集成MCP工具层 — Weather MCP 服务端

【章节学习重点】
- FastMCP 结合 HTTP 客户端实现外部 API 封装为 MCP 工具
- streamable-http 传输协议的特点：通过 HTTP 端点暴露服务，适合远程调用和独立部署
- 工具组合模式：将基础工具（地理编码+天气查询）组合为高级工具（城市名→天气）

【代码功能】
封装 Open-Meteo 的地理编码与天气查询 API，通过 streamable-http 传输协议提供城市天气检索工具。
提供三个工具：地理编码、经纬度天气查询、城市名直接查天气（组合前两者）。

【实现思路】
1. 创建 FastMCP 实例，命名为 "Weather"
2. 定义 Open-Meteo 公共 API 地址（无需 API Key）：
   - WEATHER_URL：根据经纬度查询当前天气
   - GEOCODE_URL：根据城市名查询经纬度
3. 注册三个工具函数：
   - geocode_city(name, country, language)：城市名→经纬度
   - get_current_weather(lat, lon)：经纬度→当前天气
   - get_current_weather_by_city(name, country, language)：城市名→当前天气（组合工具）
4. 使用 httpx.Client 发送 HTTP 请求，设置超时时间
5. 通过 mcp.run(transport="streamable-http") 启动 HTTP 服务

【关键参数说明】
- name: 城市名称（如 "上海"、"Beijing"）
- country: 可选的国家代码过滤（如 "CN"）
- language: 返回结果的语言，默认 "zh"（中文）
- lat/lon: 纬度/经度，浮点数
- httpx.Client(timeout=10): HTTP 客户端，超时10秒
- transport="streamable-http": 使用 HTTP 协议暴露服务，默认端口8000，路径 /mcp

【应用场景】
- 为智能体提供实时天气查询能力
- 演示如何将外部 REST API 封装为 MCP 工具
- streamable-http 模式适合需要独立部署或远程访问的工具服务
- 工具组合模式展示了如何将原子工具组合为更高级的业务工具
"""
import sys
from mcp.server.fastmcp import FastMCP
import httpx
from typing import Dict, Any, Optional

mcp = FastMCP("Weather")

OPEN_METEO_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
OPEN_METEO_GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"

@mcp.tool()
def geocode_city(name: str, country: Optional[str] = None, language: str = "zh") -> Dict[str, Any]:
    """将城市名解析为经纬度，返回首个匹配结果的基础信息。"""
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
    print(f"-----> [Weather Server] Geocoding {name} to {top.get('latitude')}, {top.get('longitude')}", file=sys.stderr)
    return {
        "name": top.get("name"),
        "lat": top.get("latitude"),
        "lon": top.get("longitude"),
        "country": top.get("country"),
    }

@mcp.tool()
def get_current_weather(lat: float, lon: float) -> Dict[str, Any]:
    """根据经纬度查询当前天气，返回温度、风速等核心指标。"""
    params = {"latitude": lat, "longitude": lon, "current_weather": True}
    with httpx.Client(timeout=10) as client:
        r = client.get(OPEN_METEO_WEATHER_URL, params=params)
        r.raise_for_status()
        payload = r.json()
    cw = payload.get("current_weather") or {}
    print(f"-----> [Weather Server] Getting current weather for {lat}, {lon}: {cw}", file=sys.stderr)
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
    """城市名 -> 当前天气（内部先地理编码再查询天气）。"""
    g = geocode_city(name=name, country=country, language=language)
    if "error" in g:
        return g
    w = get_current_weather(lat=g["lat"], lon=g["lon"])
    print(f"-----> [Weather Server] Getting current weather by city {name}: {w}", file=sys.stderr)
    return {**g, **w}

if __name__ == "__main__":
    print("Starting Weather MCP Server (streamable-http) on http://localhost:8000/mcp ...")
    mcp.run(transport="streamable-http")