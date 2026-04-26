"""
第二章 2.1.5 使用Qwen系列模型生成图片

【章节学习重点】
- 通义万相（Wanx）是阿里云的AI图片生成模型
- LangChain 生态不仅限于文本模型，还可集成多模态生成能力
- 直接使用 dashscope SDK 调用图片生成接口

【代码功能】
演示如何使用阿里云 DashScope SDK 的 ImageSynthesis 接口调用通义万相模型生成图片。
根据文本提示词生成对应风格的图片，支持 Base64 和 URL 两种输出格式。

【实现思路】
1. 导入 dashscope.ImageSynthesis 和 base64 模块
2. 调用 ImageSynthesis.call() 方法，传入模型名、提示词、API Key 和图片尺寸
3. 检查返回状态码，根据输出格式（Base64 或 URL）处理结果
4. 如果是 Base64 格式，解码后保存为本地图片文件

【关键参数说明】
- model: "wanx-v1" 为通义万相图片生成模型
- prompt: 图片描述提示词，越详细生成效果越好。支持风格描述（如"插画风格"、"写实风格"）
- api_key: 阿里云 DashScope API Key
- size: 图片尺寸，如 "1024*1024"（正方形）、"1024*1536"（竖版）等

【输出格式说明】
- b64_json: 图片的 Base64 编码，需要解码后保存为文件
- url: 图片的临时访问链接，可直接在浏览器中查看（有时效限制）

【应用场景】
- 根据文本描述自动生成配图
- 电商商品图生成
- 创意设计辅助
- 内容创作中的图文结合
"""
from dashscope import ImageSynthesis
import base64

result = ImageSynthesis.call(
    model="wanx-v1",
    prompt="在阳光下的现代城市街头，一只戴着墨镜的橙色猫咪喝咖啡，插画风格。",
    api_key="xxxxxxxx",
    size="1024*1024",
)

if result.status_code == 200:
    output = result.output
    if "b64_json" in output["results"][0]:
        image_base64 = output["results"][0]["b64_json"]
        image_data = base64.b64decode(image_base64)
        with open("qwen_image.png", "wb") as f:
            f.write(image_data)
        print("✅ 已生成图片：qwen_image.png")
    elif "url" in output["results"][0]:
        print("✅ 图片生成成功：", output["results"][0]["url"])
    else:
        print("⚠️ 未找到可解析的图片数据：", output)
else:
    print("❌ 调用失败：", result.message)
