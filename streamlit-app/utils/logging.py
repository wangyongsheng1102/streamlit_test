import streamlit as st
import logging
import uuid
from datetime import datetime

# 设置日志记录
log_file = 'streamlit_app.log'

# 创建日志记录器
logger = logging.getLogger('streamlit')
logger.setLevel(logging.INFO)

# 创建日志文件处理器
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

# 创建日志格式
formatter = logging.Formatter('%(asctime)s - %(session_id)s - %(levelname)s - '
                              '%(real_name)s - %(username)s - %(roles)s - %(message)s')
file_handler.setFormatter(formatter)

# 添加文件处理器到日志器
logger.addHandler(file_handler)

# SessionState管理，生成唯一的会话ID
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())  # 使用uuid生成唯一会话ID


# 定义一个简单的日志函数
def log_message(message, level="INFO"):
    extra = {'session_id': st.session_state.session_id,
             'real_name': st.session_state.name,
             'username': st.session_state.username,
             'roles': st.session_state.roles}
    print("※" * 50, extra)
    if level == "INFO":
        logger.info(message, extra=extra)
    elif level == "ERROR":
        logger.error(message, extra=extra)
    elif level == "WARNING":
        logger.warning(message, extra=extra)
