"""
第三章 3.4.6 优化问答页面 — Streamlit 前端入口（集成RAG）

【章节学习重点】
- Streamlit 会话状态管理：runner、history、_prefill
- 知识库管理功能的集成：初始化和更新按钮
- 快捷示例的扩展：新增知识库相关示例问题

【代码功能】
Streamlit 前端入口，提供聊天界面和知识库管理功能。
在第二章原有问答界面基础上，新增了知识库初始化/更新按钮和规章制度相关示例问题。

【实现思路】
1. 页面配置和会话状态初始化
2. 快捷示例区域：4个示例按钮（天气、计算、总结、规章制度）
3. 对话历史展示
4. 输入表单和发送逻辑
5. 侧边栏：会话重置 + 知识库管理（初始化/更新）

【关键参数说明】
- st.session_state.runner: AgentRunner 实例，封装模型+工具+中间件+RAG
- st.session_state.history: 前端聊天记录
- init_company_kb(delete_existing=False): 初始化知识库（不删除已有数据）
- init_company_kb(delete_existing=True): 更新知识库（删除旧数据后重建）

【应用场景】
- 企业知识库问答系统的前端界面
- 知识库的按需初始化和更新管理
"""
import streamlit as st
from agent.runner import build_runner
from agent.company_kb import init_company_kb


st.set_page_config(
    page_title="AgentQ-RAG — 企业问答智能体",
    page_icon="🤖",
    layout="centered",
)

# --- 初始化 ---
if "runner" not in st.session_state:
    # AgentRunner：封装模型+工具+中间件（复用同一个实例）
    st.session_state.runner = build_runner()
if "history" not in st.session_state:
    # history：前端展示的聊天记录（列表保存角色和文本）
    st.session_state.history = []
if "_prefill" not in st.session_state:
    # _prefill：输入框的预填内容，示例按钮会写入它
    st.session_state._prefill = ""

st.title("AgentQ-RAG — 企业问答智能体")

# 快捷示例（不改后端，仅便于输入）
with st.expander("示例问题（点一下即可带入输入框）", expanded=False):
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("今天上海天气怎样？"):
        st.session_state._prefill = "今天上海天气怎样？"
        st.rerun()
    if c2.button("计算 (3+5)*12"):
        st.session_state._prefill = "计算 (3+5)*12"
        st.rerun()
    if c3.button("帮我总结：LangChain 作用是什么？"):
        st.session_state._prefill = "帮我总结：LangChain 作用是什么？"
        st.rerun()
    if c4.button("员工迟到了有什么处理规定？"):
        st.session_state._prefill = "员工迟到了有什么处理规定？"
        st.rerun()

# 展示历史
for role, content in st.session_state.history:
    with st.chat_message("user" if role == "user" else "assistant"):
        st.markdown(content)

# 输入区域：使用 form + text_input，支持预填
with st.form(key="chat_form", clear_on_submit=True):
    user_text = st.text_input(
        "输入",
        value=st.session_state._prefill,
        placeholder="例如：今天上海天气怎样？ 或 计算 (3+5)*12 或 员工迟到了有什么处理规定？",
        label_visibility="collapsed",
    )
    sent = st.form_submit_button("发送")

# 发送
if sent:
    st.session_state._prefill = ""
    prompt = (user_text or "").strip()
    if prompt:
        st.session_state.history.append(("user", prompt))
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            # 调用 AgentRunner（runner.py中）的 invoke 方法，传入用户输入的 prompt
            reply = st.session_state.runner.invoke(prompt)
        except Exception as e:
            reply = f"抱歉，发生错误：{e}"

        st.session_state.history.append(("assistant", reply))
        with st.chat_message("assistant"):
            st.markdown(reply)

# 侧边栏
with st.sidebar:
    st.subheader("会话控制")
    if st.button("清空会话 / 重置记忆", use_container_width=True):
        # 重建 runner（清空短期记忆），清空历史
        st.session_state.runner = build_runner()
        st.session_state.history = []
        st.session_state._prefill = ""
        st.rerun()

    st.markdown("---")
    st.subheader("知识库管理")
    if st.button("初始化知识库"):
        try:
            init_company_kb(delete_existing=False)
            st.success("知识库初始化完成（如已存在则复用原有数据）。")
        except Exception as e:
            st.error(f"初始化失败：{e}")
    if st.button("更新知识库"):
        try:
            init_company_kb(delete_existing=True)
            st.success("知识库已更新（删除旧数据后重新构建完成）。")
        except Exception as e:
            st.error(f"更新失败：{e}")