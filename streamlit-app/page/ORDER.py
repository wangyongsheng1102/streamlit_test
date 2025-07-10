import streamlit as st
from PIL import Image
from utils.layout import add_separator_rainbow

# 示例菜品数据
menu_items = [
    {"name": "汉堡", "image_path": "assets/hamburger.jpg", "options": ["加芝士", "去芝士"]},
    {"name": "披萨", "image_path": "assets/pizza.jpg", "options": ["加蘑菇", "去蘑菇"]},
    {"name": "可乐", "image_path": "assets/coca-cola.jpg", "options": ["加冰", "去冰"]}
]


def display_menu(menu_items):
    for i, item in enumerate(menu_items):
        if i % 3 == 0:
            st.write("<hr>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            display_item(item, f"item_{i}_col1")
        with col2:
            display_item(item, f"item_{i}_col2")
        with col3:
            display_item(item, f"item_{i}_col3")


def display_item(item, key_prefix):
    image = Image.open(item["image_path"])

    # 创建一个 expander，点击图片时展开
    expander = st.expander(item["name"], expanded=False)

    with expander:
        st.image(image, use_container_width=True)

        # 显示选项复选框
        option_values = {}
        for idx, option in enumerate(item["options"]):
            option_values[option] = st.checkbox(option, key=f"{key_prefix}_{idx}_{option}")

        # 显示选项结果
        st.write("选项选择：")
        for option, value in option_values.items():
            if value:
                st.write(f"- {option}")


def render():
    """カレンダー"""
    st.title(":pig_nose: :gray[_オーダー_] :pig_nose:")
    add_separator_rainbow()
    display_menu(menu_items)
