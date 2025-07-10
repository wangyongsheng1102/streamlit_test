import streamlit as st
import streamlit_authenticator as stauth
import yaml
from streamlit_authenticator import LoginError
from yaml import SafeLoader


# from db.db_handler import get_users


def get_authenticator():
    # 从数据库获取用户信息
    # users = get_users()
    with open('config/config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    # print("config", config)

    # 构建用户名、姓名和加密密码列表
    # usernames = [user["username"] for user in users]
    # print("usernames", usernames)
    # names = [user["name"] for user in users]
    # print("names", names)
    # hashed_passwords = [user["password"] for user in users]
    # print("hashed_passwords", hashed_passwords)

    # 创建 Authenticator 实例
    # authenticator = stauth.Authenticate(
    #     credentials={"usernames": {usernames[i]: {"name": names[i], "password": hashed_passwords[i]} for i in
    #                                range(len(users))}},
    #     cookie_name="streamlit_auth",
    #     key="auth",
    #     cookie_expiry_days=7,
    # )
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    # username = st.text_input(label="用户名", key="username")
    # password = st.text_input(label="密码", type="password", key="password")
    # login_button = st.button("登录")

    # # 登录验证
    # name, authentication_status, username = authenticator.login("main")

    try:
        fields = {
            "username": "ユーザー",
            "password": "パスワード",
            "login": "ログイン"
        }
        login_result = authenticator.login(location="main", fields=fields)
    except LoginError as e:
        st.error(e)
    # if login_result is None:
    #     print("登录失败或返回了 None。")
    #     # 处理登录失败或返回 None 的情况
    # else:
    #     authentication_status, username = login_result
    #     # 继续执行后续逻辑
    #     print(f"用户名：{name}, 状态：{authentication_status}, 用户名：{username}")
    # print("st.session_state['authentication_status']", st.session_state['authentication_status'])
    return authenticator
    # return authenticator, name, authentication_status, username
