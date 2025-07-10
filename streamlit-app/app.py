import datetime
import json
import random
import sqlite3

import datetime as datetime
import streamlit as st
import yaml
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from yaml import SafeLoader

from utils.auth import get_authenticator
from utils.menu_loader import load_menus, render_page
from utils.layout import add_separator_rainbow_sidebar
from utils.user_management import load_yaml, save_yaml
from db.db_handler import init_db
from utils.logging import log_message

emojis = [
    ":smiley_cat:",
    ":smile_cat:",
    ":heart_eyes_cat:",
    ":kissing_cat:",
    ":grinning:",
    ":smirk_cat:",
    ":scream_cat:",
    ":crying_cat_face:",
    ":joy_cat:",
    ":pouting_cat:",
    ":japanese_ogre:",
    ":japanese_goblin:",
    ":see_no_evil:",
    ":hear_no_evil:",
    ":speak_no_evil:",
]

import os

os.environ['ST_NOSETTINGS'] = 'true'


# 登录功能
def random_welcome(name):
    st.session_state["name"] = name
    return random.choice(emojis)  # 随机选择一个表情符号


# 初始化数据库
# init_db()

# Streamlit 应用配置
st.set_page_config(
    page_title="Biprogy統合管理プラットフォーム",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded",
)

conn = sqlite3.connect("data.db")
cursor = conn.cursor()
cursor.execute("SELECT id, name, route FROM menus")
menus = [{"id": row[0], "name": row[1], "route": row[2]} for row in cursor.fetchall()]
conn.close()
print("menus : ", menus)

# 获取 Authenticator 实例
authenticator = get_authenticator()
# authenticator, name, authentication_status, username = get_authenticator()
print("st.session_state", st.session_state)
if st.session_state["authentication_status"]:
    # authenticator.logout()
    authenticator.logout(button_name="ログアウト", location="sidebar")
    if "welcome" in st.session_state and st.session_state["welcome"] is not None:
        welcome = st.session_state["welcome"]
    else:
        welcome = random_welcome(st.session_state["name"])
        st.session_state["welcome"] = welcome

    if "name" in st.session_state:
        st.sidebar.success(f'ようこそ {welcome} *{st.session_state["name"]}*！')

    # add_separator_rainbow_sidebar()
    st.session_state.sidebar_state = "expanded"

    print(
        "st.session_state['authentication_status'] ",
        st.session_state["authentication_status"],
        st.session_state,
    )
    if st.session_state["username"] is not None:
        with open("config/config.yaml") as file:
            config = yaml.load(file, Loader=SafeLoader)
        user = config["credentials"]["usernames"][st.session_state["username"]]
        user["logged_in"] = True
        try:
            with open("config/config.yaml", "w") as file:
                yaml.dump(config, file)
        except Exception as e:
            print(e)
    print("log print")
    # log_message(f"ログインしました。", "INFO")

    # st.session_state.sidebar_state = 'collapsed' if st.session_state.sidebar_state == 'expanded' else 'expanded'
    # # Force an app rerun after switching the sidebar state.
    # st.experimental_rerun()
    menus = load_menus()
    # 使用 OptionMenu 创建侧边栏导航
    with st.sidebar:
        selected_menu = option_menu(
            "ナビゲーション",  # 菜单标题
            [menu["name"] for menu in menus],  # 菜单名称列表
            icons=[
                "house",
                "envelope",
                "cloud-upload",
                "instagram",
                "globe",
                "person",
                "",
                "",
                "bell"
            ],  # 可自定义图标
            menu_icon="cast",  # 菜单图标
            default_index=0,  # 默认选中第一个菜单
        )
    render_page(selected_menu, menus, authenticator)

    if (
            "login_datetime" in st.session_state
            and st.session_state["login_datetime"] is not None
    ):
        st.sidebar.info(f'ログイン：{st.session_state["login_datetime"]}')
    else:
        login_datetime = str(datetime.datetime.now())
        st.sidebar.info(f"ログイン：" f"\n\t{login_datetime}")
        st.session_state["login_datetime"] = login_datetime

    # 嵌入 JavaScript
    hide_animation_js = """
    <script>
        setTimeout(() => {
            const lottieDiv = document.getElementById('lottie-container');
            if (lottieDiv) {
                lottieDiv.style.display = 'none';
            }
        }, 5000); // 5 秒后隐藏
    </script>
    """

    # 读取本地JSON文件
    with open("assets/Animation - 1735602685829.json", "r") as file:
        animation_data = json.load(file)
    with st.sidebar:
        st.markdown("<div id='lottie-container'>", unsafe_allow_html=True)
        # 展示动画
        st_lottie(
            animation_data,
            speed=1,  # 动画播放速度
            reverse=False,  # 动画是否反转播放
            loop=True,  # 动画是否循环
            quality="high",  # 动画质量 (low, medium, high)
            height=300,  # 动画高度
            width=None,  # 动画宽度，默认根据高度调整比例
            key="lottie_animation_sidebar",
        )
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(hide_animation_js, unsafe_allow_html=True)

elif st.session_state["authentication_status"] is False:
    st.error("ユーザー/パスワードが誤りので、チェックしてください。")
elif st.session_state["authentication_status"] is None:
    print("logout", st.session_state)
    st.snow()
    # with open('config/config.yaml') as file:
    #     config = yaml.load(file, Loader=SafeLoader)
    #
    # user = config['credentials']['usernames'][st.session_state['username']]
    # user['logged_in'] = False
    # try:
    #     with open('config/config.yaml', "w") as file:
    #         yaml.dump(config, file)
    # except Exception as e:
    #     print(e)
    st.warning("ユーザー/パスワードを入力してください。")
# if authentication_status:
#     # 显示登录状态
#     st.sidebar.success(f"欢迎，{name} 👋")
#
#     # 动态加载菜单
#     menus = load_menus()
#
#     # 使用 OptionMenu 创建侧边栏导航
#     with st.sidebar:
#         selected_menu = option_menu(
#             "导航",  # 菜单标题
#             [menu["name"] for menu in menus],  # 菜单名称列表
#             icons=["house", "cloud-upload", "door-closed"],  # 可自定义图标
#             menu_icon="cast",  # 菜单图标
#             default_index=0,  # 默认选中第一个菜单
#         )
#
#     # 根据选中菜单渲染页面
#     render_page(selected_menu, menus, authenticator)
