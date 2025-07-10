import streamlit as st

from utils.layout import add_separator_rainbow

from utils.logging import log_message


def render():
    st.title(":gray[_ファイルアップロード_] :sunglasses:")
    add_separator_rainbow()
    uploaded_file = st.file_uploader("选择一个文件")
    if uploaded_file:
        st.success(f"文件 `{uploaded_file.name}` 上传成功！", icon="✅")
