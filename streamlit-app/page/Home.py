import json

import streamlit as st
import random

from streamlit_lottie import st_lottie
from utils.layout import add_separator_rainbow

from utils.logging import log_message


# 加载 Lottie 动画文件
def load_lottie_file(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def render():
    print("top_page", st.session_state["name"])
    st.title(":cherry_blossom: :gray[_トップページ_] :cherry_blossom:")
    add_separator_rainbow()

    if "name" in st.session_state and st.session_state["name"] is not None:
        st.markdown(f'*{st.session_state["name"][:1]}さん、お疲れさまでした。*')
        st.markdown("_今日も頑張りましょう。_")
        st.balloons()

    # 使用本地的 JSON 文件
    lottie_animation = load_lottie_file("config/Animation - 1735471531444.json")

    # 展示动画
    st_lottie(
        lottie_animation,
        speed=1,  # 动画播放速度
        reverse=False,  # 动画是否反转播放
        loop=True,  # 动画是否循环
        quality="high",  # 动画质量 (low, medium, high)
        height=300,  # 动画高度
        width=None,  # 动画宽度，默认根据高度调整比例
        key="lottie_animation",
    )
