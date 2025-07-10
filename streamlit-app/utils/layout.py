import streamlit as st


def add_separator_rainbow():
    st.markdown("""
        <style>
            .rainbow-line {
                height: 2px;  /* 调整线的高度 */
                background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet); /* 彩虹渐变 */
                border: none;
                margin: 20px 0;  /* 控制上下的间距 */
            }
        </style>
        <div class="rainbow-line"></div>
    """, unsafe_allow_html=True)


def add_separator_rainbow_sidebar():
    st.sidebar.markdown("""
        <style>
            .rainbow-line {
                height: 2px;  /* 调整线的高度 */
                background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet); /* 彩虹渐变 */
                border: none;
                margin: 20px 0;  /* 控制上下的间距 */
            }
        </style>
        <div class="rainbow-line"></div>
    """, unsafe_allow_html=True)
