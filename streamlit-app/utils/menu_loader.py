import streamlit as st
from page import Home, Upload, User, Work, WBS, Test, Evidence, Calendar, ORDER

# 页面渲染函数映射表
PAGE_RENDERERS = {
    "home": Home.render,
    "upload": Upload.render,
    "user": User.render,
    "work": Work.render,
    "wbs": WBS.render,
    "test": Test.render,
    "evidence": Evidence.render,
    "calendar": Calendar.render,
    "order": ORDER.render
}


# 从数据库加载菜单
def load_menus():
    from db.db_handler import get_menus
    return get_menus()


# 渲染选中的页面
def render_page(selected_menu, menus, authenticator):
    # 查找选中菜单对应的路由
    for menu in menus:
        if menu["name"] == selected_menu:
            route = menu["route"]
            break
    else:
        st.error("対応するページが見つかりません！")
        return

    # 渲染页面内容
    if route in PAGE_RENDERERS:
        PAGE_RENDERERS[route]()
    else:
        st.error("ページルーティングが設定されていません！")
