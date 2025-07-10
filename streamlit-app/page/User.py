import base64

import pandas as pd
import streamlit as st
import yaml
from st_aggrid import AgGrid
from streamlit_authenticator import Hasher
from streamlit_lottie import st_lottie
from utils.user_management import load_yaml, save_yaml

from utils.layout import add_separator_rainbow

from streamlit.components.v1 import html
from yaml import SafeLoader

from utils.logging import log_message


# @st.dialog("Are you sure you want cancel changes?")
# def show_dialog():
#     def on_click_yes():
#         print("yes")
#         st.rerun()
#
#     def on_click_no():
#         print("No")
#         st.rerun()
#
#     cols = st.columns(2)
#     with cols[0]:
#         st.button("No", on_click=on_click_no)
#     with cols[1]:
#         st.button("Yes", on_click=on_click_yes)


def render():
    st.title(":ok_woman: :gray[_ユーザー管理_] :no_good:")
    add_separator_rainbow()

    log_message(f"ページ「ユーザー管理」は表示しました。", "INFO")

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
            🚀 ユーザー情報
        </div>
        """
    st.markdown(widget_html, unsafe_allow_html=True)

    users_data = load_yaml()

    users = users_data["credentials"]["usernames"]
    print("!" * 50, users)

    # # 选择操作
    # action = st.radio("选择操作", ["查看用户", "添加用户", "更新用户", "删除用户"])
    # 使用 radio 与自定义图标
    # action = st.radio(
    #     label="选择操作",
    #     options=["查看用户", "添加用户", "更新用户", "删除用户"],
    #     format_func=lambda x: f"🔍 {x}" if x == "查看用户"
    #     else f"➕ {x}" if x == "添加用户"
    #     else f"✏️ {x}" if x == "更新用户"
    #     else f"❌ {x}",  # 可以根据选项添加不同的符号
    # )

    # # 使用自定义 CSS 设置 selectbox 宽度
    # st.markdown("""
    #     <style>
    #         .streamlit-expanderHeader {
    #             width: 50px;  /* 设置宽度 */
    #         }
    #     </style>
    # """, unsafe_allow_html=True)
    #
    # # 创建 selectbox
    # options = ["查看用户", "添加用户", "更新用户", "删除用户"]
    # action = st.selectbox('Choose an option:', options)

    # with st.container():
    #     st.markdown('<style>div.row-widget.stSelectbox { width: 50px; }</style>', unsafe_allow_html=True)
    #     options = ["查看用户", "添加用户", "更新用户", "删除用户"]
    #     action = st.selectbox('Choose an option:', options)

    # # 创建 1 列布局容器
    # col1 = st.columns([1])[0]
    #
    # # 在列中放置 selectbox
    # with col1:
    #     options = ["查看用户", "添加用户", "更新用户", "删除用户"]
    #     action = st.selectbox('Choose an option:', options)

    action = st.selectbox(
        "", ["ユーザー一覧", "ユーザー新規", "ユーザー更新", "ユーザー削除"]
    )
    st.divider()

    if action == "ユーザー一覧":
        show_users(users)
    elif action == "ユーザー新規":
        add_user()
    elif action == "ユーザー更新":
        update_user(users)
    elif action == "ユーザー削除":
        delete_user(users)

    # st.button("Cancel", key="sample_key", on_click=show_dialog)


# 显示用户信息
def show_users(users):
    # st.markdown("### ユーザー一覧")
    # st.write("**ユーザー一覧**")
    st.markdown(
        """
        <style>
            body {
                margin: 0;
                padding: 0;
                overflow: hidden;
                height: 100%;
                background-color: #f0f0f0;
            }

            .snowflakes {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 9999;
            }

            .snowflake {
                position: absolute;
                top: -10px;
                width: 10px;
                height: 10px;
                background-color: #fff;
                border-radius: 50%;
                opacity: 0.8;
                animation: snowfall linear infinite;
            }

            @keyframes snowfall {
                0% {
                    transform: translateY(-100px) translateX(0);
                }
                100% {
                    transform: translateY(100vh) translateX(var(--translate-x));
                }
            }

            /* Create multiple snowflakes */
            .snowflake:nth-child(1) {
                left: 5%;
                animation-duration: 10s;
                --translate-x: 20px;
            }
            .snowflake:nth-child(2) {
                left: 15%;
                animation-duration: 12s;
                --translate-x: -30px;
            }
            .snowflake:nth-child(3) {
                left: 25%;
                animation-duration: 8s;
                --translate-x: 10px;
            }
            .snowflake:nth-child(4) {
                left: 35%;
                animation-duration: 14s;
                --translate-x: -20px;
            }
            .snowflake:nth-child(5) {
                left: 45%;
                animation-duration: 16s;
                --translate-x: 30px;
            }
            .snowflake:nth-child(6) {
                left: 55%;
                animation-duration: 18s;
                --translate-x: -40px;
            }
            .snowflake:nth-child(7) {
                left: 65%;
                animation-duration: 12s;
                --translate-x: 10px;
            }
            .snowflake:nth-child(8) {
                left: 75%;
                animation-duration: 14s;
                --translate-x: -25px;
            }
            .snowflake:nth-child(9) {
                left: 85%;
                animation-duration: 10s;
                --translate-x: 15px;
            }
            .snowflake:nth-child(10) {
                left: 95%;
                animation-duration: 16s;
                --translate-x: -35px;
            }
        </style>

        <div class="snowflakes">
            <div class="snowflake"></div>
            <div class="snowflake"></div>
            <div class="snowflake"></div>
            <div class="snowflake"></div>
            <div class="snowflake"></div>
            <div class="snowflake"></div>
            <div class="snowflake"></div>
            <div class="snowflake"></div>
            <div class="snowflake"></div>
            <div class="snowflake"></div>
        </div>
    """,
        unsafe_allow_html=True,
    )
    user_list = []
    for user, content in users.items():
        user_list.append(
            [
                user,
                content["name"],
                content["password"],
                content["email"],
                content["roles"],
                content["logged_in"],
                content["failed_login_attempts"],
            ]
        )
    user_data = pd.DataFrame(user_list)
    user_data.columns = [
        "ログインID",
        "ユーザー名",
        "パスワード",
        "Email",
        "ロール",
        "登録状況",
        "失敗回数",
    ]
    user_data = user_data.set_index("ログインID")
    # st.dataframe(user_data)
    # AgGrid(user_data)
    st.data_editor(
        user_data,
        column_config={
            "ログインID": "ログインID",
            "ユーザー名": "ユーザー名",
            "パスワード": "パスワード",
            "Email": "Email",
            "ロール": "ロール",
            "登録状況": "登録状況",
            "失敗回数": "失敗回数",
        },
        disabled=[
            "ログインID",
            "ユーザー名",
            "パスワード",
            "Email",
            "ロール",
            "登録状況",
            "失敗回数",
        ],
        hide_index=True,
        use_container_width=True,
    )


def add_user():
    # user_list = [['', '', '', '', '', False, '']]
    st.write("新規ユーザーを入力してください。")
    user_list = []
    user_data = pd.DataFrame(
        user_list,
        columns=[
            "ログインID",
            "ユーザー名",
            "パスワード",
            "Email",
            "ロール",
            "登録状況",
            "失敗回数",
        ],
    )
    # user_data = user_data.set_index('ログインID')
    edited_data = st.data_editor(
        user_data,
        column_config={
            "ログインID": "ログインID",
            "ユーザー名": "ユーザー名",
            "パスワード": "パスワード",
            "Email": "Email",
            "ロール": "ロール",
            "登録状況": "登録状況",
            "失敗回数": "失敗回数",
        },
        use_container_width=True,
        disabled=["登録状況"],
        hide_index=True,
        num_rows="dynamic",
    )
    if st.button("新規"):
        print(edited_data)
        # with open('config/config.yaml') as file:
        #     config = yaml.load(file, Loader=SafeLoader)
        # user = config['credentials']['usernames'][st.session_state['username']]
        # user['logged_in'] = True
        # try:
        #     with open('config/config.yaml', "w") as file:
        #         yaml.dump(config, file)
        # except Exception as e:
        #     print(e)


def update_user(users):
    user_id_list = []
    for user, content in users.items():
        user_id_list.append([user, content["name"]])
    st.write("更新ユーザーを選んでください")
    user_id = st.selectbox("", user_id_list)

    if user_id:
        print("users[user_id[0]]", users[user_id[0]])
        user_list = [
            [
                user_id[0],
                users[user_id[0]]["name"],
                users[user_id[0]]["password"],
                users[user_id[0]]["email"],
                users[user_id[0]]["roles"],
                users[user_id[0]]["logged_in"],
                users[user_id[0]]["failed_login_attempts"],
            ]
        ]
        print("user_list", user_list)
        user_data = pd.DataFrame(
            user_list,
            columns=[
                "ログインID",
                "ユーザー名",
                "パスワード",
                "Email",
                "ロール",
                "登録状況",
                "失敗回数",
            ],
        )
        edited_data = st.data_editor(
            user_data,
            column_config={
                "ログインID": "ログインID",
                "ユーザー名": "ユーザー名",
                "パスワード": "パスワード",
                "Email": "Email",
                "ロール": "ロール",
                "登録状況": "登録状況",
                "失敗回数": "失敗回数",
            },
            disabled=["ログインID", "登録状況"],
            hide_index=True,
            use_container_width=True,
        )
        # AgGrid(user_data, enableFiltering=True)
        if st.button("更新"):
            update_data = edited_data.iloc[0]
            print("更新：", update_data["ロール"])
            with open("config/config.yaml") as file:
                config = yaml.load(file, Loader=SafeLoader)
            user = config["credentials"]["usernames"][user_id[0]]
            user["name"] = update_data["ユーザー名"]
            user["password"] = Hasher.hash(update_data["パスワード"])
            user["email"] = update_data["Email"]
            user["roles"] = update_data["ロール"]
            user["failed_login_attempts"] = update_data["失敗回数"]
            try:
                with open("config/config.yaml", "w") as file:
                    yaml.dump(config, file)
            except Exception as e:
                print(e)
            st.success(f"ユーザー「{user_id[0]}」が更新成功！", icon="✅")


def delete_user(users):
    user_id_list = []
    for user, content in users.items():
        user_id_list.append([user, content["name"]])
    st.write("削除ユーザーを選んでください")
    user_id = st.selectbox("", user_id_list)

    if user_id:
        print("users[user_id[0]]", users[user_id[0]])
        user_list = [
            [
                user_id[0],
                users[user_id[0]]["name"],
                users[user_id[0]]["password"],
                users[user_id[0]]["email"],
                users[user_id[0]]["roles"],
                users[user_id[0]]["logged_in"],
                users[user_id[0]]["failed_login_attempts"],
            ]
        ]
        print("user_list", user_list)
        user_data = pd.DataFrame(
            user_list,
            columns=[
                "ログインID",
                "ユーザー名",
                "パスワード",
                "Email",
                "ロール",
                "登録状況",
                "失敗回数",
            ],
        )
        edited_data = st.data_editor(
            user_data,
            column_config={
                "ログインID": "ログインID",
                "ユーザー名": "ユーザー名",
                "パスワード": "パスワード",
                "Email": "Email",
                "ロール": "ロール",
                "登録状況": "登録状況",
                "失敗回数": "失敗回数",
            },
            disabled=[
                "ログインID",
                "ユーザー名",
                "パスワード",
                "Email",
                "ロール",
                "登録状況",
                "失敗回数",
            ],
            hide_index=True,
            use_container_width=True,
        )
        # AgGrid(user_data, enableFiltering=True)
        if st.button("削除"):
            # 当点击按钮时，显示一个选择框来模拟弹出确认框
            confirm = st.radio("确认删除该用户吗？", ("请选择", "是", "否"))
            if confirm == "是":
                with open("config/config.yaml", "r", encoding="utf-8") as file:
                    config = yaml.safe_load(file)
                usernames = config["credentials"]["usernames"]
                del usernames[user_id[0]]
                with open("config/config.yaml", "w", encoding="utf-8") as file:
                    yaml.dump(
                        config, file, default_flow_style=False, allow_unicode=True
                    )
                st.success(f"ユーザー「{user_id[0]}」が削除成功！", icon="✅")
            elif confirm == "否":
                st.warning("操作已取消!")
