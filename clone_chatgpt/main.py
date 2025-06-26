# 引入streamlit别名st
import streamlit as st
# 引入记忆
from langchain.memory import ConversationBufferMemory

# 引入utils文件的get_chat_response定义函数
from utils import get_chat_response

# 添加大标题
st.title("💬 克隆ChatGPT")

# 添加侧边栏
with st.sidebar:
    openai_api_key = st.text_input("请输入OpenAI API Key：", type="password")
    st.markdown("[获取OpenAI API key](https://platform.openai.com/account/api-keys)")

# 如果memory不在对话状态里
if "memory" not in st.session_state:
    # 在消息状态初始化一个memory的键，值是ConversationBufferMemory返回的内容
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
    # 设置初始会话状态
    st.session_state["messages"] = [{"role": "ai",
                                     "content": "你好，我是你的AI助手，有什么可以帮你的吗？"}]

# 用for循环迭代会话状态里的内容
for message in st.session_state["messages"]:
    # 让每条消息都在页面上展示出来
    st.chat_message(message["role"]).write(message["content"])

# st.chat_input函数专门用来输入对话消息
prompt = st.chat_input()
#如果输入消息
if prompt:
    # 未提供API秘钥
    if not openai_api_key:
        # 提示输入秘钥
        st.info("请输入你的OpenAI API Key")
        st.stop()
    # 将用户输入的内容储存进会话消息状态里
    st.session_state["messages"].append({"role": "human", "content": prompt})
    # 输入内容展示出来
    st.chat_message("human").write(prompt)

    # 展示加载程序，直到回复完成
    with st.spinner("AI正在思考中，请稍等..."):
        response = get_chat_response(prompt, st.session_state["memory"],
                                     openai_api_key)
    # 将AI回复生成字典，赋值给msg变量
    msg = {"role": "ai", "content": response}
    # 将AI回复添加进消息状态里
    st.session_state["messages"].append(msg)
    # 将AI消息展示出来
    st.chat_message("ai").write(response)