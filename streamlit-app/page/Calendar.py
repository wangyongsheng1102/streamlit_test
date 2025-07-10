import streamlit as st
from streamlit_calendar import calendar
# import calendar
from datetime import datetime, timedelta
from utils.layout import add_separator_rainbow

# 日历数据示例：假定这些是日本的公共假期
japanese_holidays = {
    "2023-01-01": "新年",
    "2023-02-11": "成人节",
    "2023-03-21": "建国纪念日",
    "2023-04-29": "天皇诞生日",
    "2023-05-03": "宪法纪念日",
    "2023-05-04": "绿色星期一",
    "2023-05-05": "儿童节",
    "2023-07-18": "海之日",
    "2023-08-11": "山之日",
    "2023-12-23": "劳礼节日"
}


def get_holiday_date(selected_date):
    return japanese_holidays.get(selected_date.strftime("%Y-%m-%d"), "")


def render():
    """カレンダー"""
    st.title(":pig_nose: :gray[_カレンダー_] :pig_nose:")
    add_separator_rainbow()

    # 获取当前日期
    current_date = datetime.now()

    events = [
        {
            "tltle": "Event1",
            "color": "#FF6C6A",
            "start": "2025-01-08",
            "end": "2025-01-08",
            "resourceId": "a"
        },
        {
            "tltle": "Event2",
            "color": "#FF6C6C",
            "start": "2025-01-09",
            "end": "2025-01-09",
            "resourceId": "b"
        }
    ]

    calendar_resources = [
        {"id": "a", "building": "Building A", "title": "Room A"},
        {"id": "b", "building": "Building B", "title": "Room B"}
    ]

    calendar_option = {
        "editable": "true",
        "navLinks": "true",
        "selectable": "true",
        "resources": calendar_resources
    }

    # 添加日历选择器
    selected_date = calendar(
        events=events,
        options={
            **calendar_option,
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "dayGridDay,dayGridWeek,dayGridMonth"
            },
            # "initialView": "dayGridMonth"
        },
        # options={
        #     **calendar_option,
        #     "initialView": "resourceTimeGridDay",
        #     "resourceGroupField": "building"
        # },
        key="daygrid"
    )

    # if selected_date:
    #     holiday_name = get_holiday_date(selected_date)
    #     st.write(f"你选择了 {selected_date.strftime('%Y-%m-%d')}，这一天是 {holiday_name}。")
