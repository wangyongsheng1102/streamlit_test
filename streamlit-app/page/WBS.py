import streamlit as st

from utils.layout import add_separator_rainbow

from utils.logging import log_message


def render():
    st.title(":notebook: :gray[_WBS管理_] :notebook:")
    add_separator_rainbow()

    # 自定义动态挂件（HTML 和 CSS）
    widget_html = """
            <style>
            #floating-widget {
                position: fixed;
                bottom: 20px;
                right: 20px;
                background-color: rgba(0, 123, 255, 0.8);
                color: white;
                padding: 10px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                animation: float 3s ease-in-out infinite;
                z-index: 1000;
            }
            @keyframes float {
                0% { transform: translateY(0); }
                50% { transform: translateY(-10px); }
                100% { transform: translateY(0); }
            }
            </style>
            <div id="floating-widget">
                🚀 WBS情報
            </div>
            """
    st.markdown(widget_html, unsafe_allow_html=True)

    action = st.selectbox(
        "", ["プレビュー表示", "結果コミット"]
    )
    st.divider()

    if action == "プレビュー表示":
        pass
    elif action == "結果コミット":
        pass
