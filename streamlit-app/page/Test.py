import json

import streamlit as st
from streamlit_elements import elements, mui
from streamlit_lottie import st_lottie

from utils.layout import add_separator_rainbow


# 将 Lottie 动画嵌入到背景中
def lottie_background(filepath: str):
    with open(filepath, "r") as f:
        lottie_json = f.read()

    # HTML 和 CSS 代码，利用 lottie-player 平铺背景
    background_html = f"""
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
        }}
        #background {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
        }}
    </style>
    <div id="background">
        <lottie-player 
            autoplay 
            loop 
            background="transparent" 
            speed="1" 
            style="width: 100%; height: 100%;" 
            src='data:application/json;base64,{lottie_json.encode("utf-8").hex()}'>
        </lottie-player>
    </div>
    """
    return background_html


def set_background(gif_file):
    with open(gif_file, "rb") as f:
        gif_data = f.read()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url(data:image/gif;base64,{gif_data.decode("utf-8")});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# 加载 Lottie 动画文件
def load_lottie_file(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


# 自定义背景的 HTML 和 CSS
def set_lottie_background(json_url):
    st.markdown(
        f"""
        <style>
        /* 设置页面的背景 */
        .stApp {{
            background: url({json_url}) no-repeat center center fixed;
            background-size: cover;
            overflow: hidden;
        }}

        /* 移除 Streamlit 默认透明度 */
        .block-container {{
            background: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            padding: 20px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render():
    st.title(":gray[_テスト用_] :sunglasses:")
    add_separator_rainbow()

    # 自定义挂件 HTML 和 CSS
    st.markdown(
        """
    <style>
    /* 创建动态挂件 */
    #floating-widget {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: rgba(0, 123, 255, 0.9);
        color: white;
        padding: 10px 15px;
        border-radius: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        font-size: 16px;
        font-weight: bold;
        z-index: 9999; /* 确保挂件的优先级更高 */
        animation: bounce 2s infinite;
    }
    /* 动态效果 */
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    /* 调整 Streamlit iframe 的 z-index */
    iframe {
        z-index: 1;
    }
    </style>
    <div id="floating-widget">
        🚀 动态挂件覆盖效果
    </div>
    """,
        unsafe_allow_html=True,
    )

    background_css = """
    <style>
    body {
        background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #fbc2eb, #a1c4fd);
        background-size: 400% 400%;
        animation: gradientBG 10s ease infinite;
    }
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    </style>
    """
    st.markdown(background_css, unsafe_allow_html=True)

    # # 3D 地图
    # layer = pdk.Layer(
    #     "HexagonLayer",
    #     data=[{"lat": 37.78, "lon": -122.41}],
    #     get_position=["lon", "lat"],
    #     radius=200,
    #     elevation_scale=4,
    #     elevation_range=[0, 1000],
    #     extruded=True,
    # )
    # view_state = pdk.ViewState(latitude=37.78, longitude=-122.41, zoom=11, pitch=50)
    # st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

    # fig = go.Figure(
    #     data=[
    #         go.Bar(
    #             x=["A", "B", "C"], y=[10, 20, 30], marker_color=["red", "blue", "green"]
    #         )
    #     ]
    # )
    # st.plotly_chart(fig)

    # data = pd.DataFrame({"姓名": ["张三", "李四"], "年龄": [25, 30]})
    # AgGrid(data, editable=True, sortable=True)

    # with elements("layout"):
    #     with mui.Box(sx={"display": "flex", "flexDirection": "row", "gap": 2}):
    #         mui.Paper("模块 1", sx={"padding": 2, "flex": 1})
    #         mui.Paper("模块 2", sx={"padding": 2, "flex": 1})

    st.markdown(
        lottie_background("assets/Animation - 1735641118369.json"),
        unsafe_allow_html=True,
    )

    with elements("form"):
        with mui.Box(
            component="form",
            sx={"display": "flex", "flexDirection": "column", "gap": 2},
        ):
            mui.TextField(label="用户名", variant="outlined")
            mui.TextField(label="密码", type="password", variant="outlined")
            mui.Button("提交", variant="contained", color="primary", type="submit")

    with elements("styled"):
        mui.Button(
            "炫酷按钮",
            variant="contained",
            sx={
                "backgroundColor": "purple",
                "color": "white",
                "padding": "10px 20px",
                "borderRadius": "8px",
            },
        )

    # 加载背景 GIF 文件
    set_background("config/Animation - 1735471531444.json")

    # 示例 Lottie 动画的 JSON 文件 URL
    lottie_json_url = (
        "config/Animation - 1735471531444.json"  # 替换为你的 Lottie JSON 文件链接
    )
    # 设置 Lottie 背景
    set_lottie_background(lottie_json_url)

    # 使用本地的 JSON 文件
    lottie_animation = load_lottie_file("config/Animation - 1735470524650.json")

    # 展示动画
    st_lottie(
        lottie_animation,
        speed=1,  # 动画播放速度
        reverse=False,  # 动画是否反转播放
        loop=True,  # 动画是否循环
        quality="high",  # 动画质量 (low, medium, high)
        height=400,  # 动画高度
        width=None,  # 动画宽度，默认根据高度调整比例
        key="lottie_animation",
    )
