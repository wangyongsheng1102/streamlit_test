import datetime
import os.path
import time
import xml.etree.ElementTree as ET

import pandas as pd
# import psycopg2
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu

from utils.execute_utils import copy_folder, del_folder, parse_excel
from utils.execute_compare import compare_pics, pic_no_info_create, unzip
from utils.layout import add_separator_rainbow

from utils.logging import log_message

# pic_no_cell = []


def render():
    """文件上传和分析页面"""
    st.title(":pig_nose: :gray[_エビデンスチェック_] :pig_nose:")
    uploaded_file = st.file_uploader("Excelファイル", type=["xlsx"])
    add_separator_rainbow()

    if uploaded_file:
        try:
            if "エビデンス" not in uploaded_file.name:
                raise ValueError("エビデンスファイルを選んでください。")
            if uploaded_file.name.endswith(".xlsx"):
                temp_dir = os.path.join(os.getcwd(), "temp_upload")
                os.makedirs(temp_dir, exist_ok=True)
                copy_folder(os.path.join(os.getcwd(), "exclude-pic"), os.path.join(temp_dir, "exclude-pic"))
                tmp_file = os.path.join(os.getcwd(), "temp_upload", str(datetime.datetime.now()).
                                        replace('-', '').replace('.', '').
                                        replace(' ', '').replace('-', '').
                                        replace(':', '') + ".xlsx")
                # 将上传的文件保存到临时目录
                # file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(tmp_file, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                # shutil.copyfile(file_path, tmp_file)
                zip_dir = unzip(tmp_file)
                if os.path.exists(os.path.join(zip_dir, 'xl', 'drawings', 'drawing1.xml')) is False:
                    raise

                workbook_path = os.path.join(zip_dir, 'xl', 'workbook.xml')
                # 解析 workbook.xml
                tree = ET.parse(workbook_path)
                root = tree.getroot()
                # 命名空间处理
                ns = {'x': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                sheet_names = []
                for index, sheet in enumerate(root.findall('x:sheets/x:sheet', ns)):
                    sheet_names.append(sheet.get('name'))
                print("sheet_names : ", sheet_names)

                sheet_to_xml = {}
                for index, sheet_name in enumerate(sheet_names, start=1):
                    sheet_xml_path = os.path.join(zip_dir, f'xl/worksheets/sheet{index}.xml')
                    sheet_to_xml[sheet_name] = sheet_xml_path
                print("sheet_to_xml : ", sheet_to_xml)

                drawing_to_sheet = {}
                for sheet_name, sheet_xml_path in sheet_to_xml.items():
                    rels_file_path = sheet_xml_path.replace("/worksheets/", "/worksheets/_rels/").replace(".xml",
                                                                                                          ".xml.rels")
                    if os.path.exists(rels_file_path):
                        tree = ET.parse(rels_file_path)
                        root = tree.getroot()
                        namespace = {'ns': 'http://schemas.openxmlformats.org/package/2006/relationships'}
                        target_value = root.find('.//ns:Relationship', namespace).get('Target')
                        if target_value.find("drawing") >= 0:
                            drawing_to_sheet[target_value.split("drawings/")[1]] = sheet_name
                        print(target_value)
                print("drawing_to_sheet : ", drawing_to_sheet)

                combined_mapping = {}
                for sheet, xml in sheet_to_xml.items():
                    # 查找对应的 drawing
                    drawings = [drawing for drawing, sheet_name in drawing_to_sheet.items() if sheet_name == sheet]
                    combined_mapping[sheet] = {
                        "xml": xml,
                        "drawings": drawings
                    }
                # 输出结果
                print("Combined Mapping:")
                pic_no_cell = []
                for sheet, info in combined_mapping.items():
                    print(f"{sheet}: XML -> {info['xml']}, Drawings -> {info['drawings']}")
                    if sheet == "データ比較" or sheet == "ファイル比較":
                        continue
                    if len(info['drawings']) == 1:
                        xml_name = info['drawings'][0]
                        if os.path.exists(os.path.join(zip_dir, 'xl', 'drawings', xml_name)) is True:
                            pic_no_cell = pic_no_info_create(zip_dir, xml_name, sheet)

                sorted_list = sorted(
                    pic_no_cell,
                    key=lambda x: (str(x['xml']), int(x['row']), int(x['column']))
                )
                # print("※ sorted_list : ", sorted_list)

                sorted_list_new = []
                for index, sort_item in enumerate(sorted_list):
                    if sort_item['column'] == '1':
                        if sort_item['anchor'] == 'one':
                            sort_item['row'] = str(int(sort_item['row']) + 1)
                        sorted_list_new.append(sort_item)
                        continue
                    if sort_item['column'] == '15' and sorted_list[index - 1]['column'] == '1':
                        if sort_item['anchor'] == 'one':
                            if sorted_list[index - 1]['anchor'] == 'one':
                                sort_item['row'] = str(int(sort_item['row']) + 1)
                                sorted_list_new.append(sort_item)
                                continue
                            if sorted_list[index - 1]['anchor'] == 'two':
                                sort_item['row'] = str(int(sort_item['row']) + 1)
                                sorted_list_new.append(sort_item)
                                continue
                        if sort_item['anchor'] == 'two':
                            sorted_list_new.append(sort_item)
                            continue
                # print("※ sorted_list_new : ", sorted_list_new)

                # 假设 sorted_list_new 已经生成
                grouped_data = {}

                for item in sorted_list_new:
                    row_key = item['row']
                    xml_key = item['xml']

                    # 使用元组 (row_key, xml_key) 作为组合键
                    combined_key = (row_key, xml_key)

                    # 初始化字典
                    if combined_key not in grouped_data:
                        grouped_data[combined_key] = []  # 创建一个列表以存储条目

                    grouped_data[combined_key].append(item)  # 将项目添加到对应的组合键下

                # 打印结果
                print("※ grouped_data : ", grouped_data)

                for key, group in grouped_data.items():
                    if len(group) >= 2:
                        pic1 = group[0]['pic']
                        pic2 = group[1]['pic']
                        col1 = group[0]['column']
                        col2 = group[1]['column']

                        # st.markdown("""
                        #             <script>
                        #                 window.scrollTo(0, document.body.scrollHeight);
                        #             </script>
                        #         """, unsafe_allow_html=True)

                        # scroll_code = """
                        # document.querySelector('body').scrollTo(0, document.body.scrollHeight);
                        # """
                        # streamlit_js_eval(scroll_code, key=f"scroll_{key}")

                        # scroll_script = """
                        # <script>
                        #     function scrollToBottom(){
                        #         window.scrollTo(0, document.body.scrollHeight);
                        #     }
                        #     scrollToBottom();
                        # </script>
                        # """
                        # st.components.v1.html(scroll_script, height=0)

                        if col1 != "1" or col2 != "15":
                            st.write(5, [None, "sheet「" + group[0]['xml'] + "」" + "row「" + str(
                                int(group[0]['row'])) + "」",
                                         "キャプチャーの位置が間違っています。", "✕", "ー"])
                        print(f"row {key}: pic1={pic1}, pic2={pic2}, col1={col1}, col2={col2}")
                        image1_path = os.path.join(temp_dir,
                                                   os.path.basename(tmp_file).split(".")[0],
                                                   "xl",
                                                   "media",
                                                   pic1)
                        image2_path = os.path.join(temp_dir,
                                                   os.path.basename(tmp_file).split(".")[0],
                                                   "xl",
                                                   "media",
                                                   pic2)

                        difference_count, output_path = compare_pics(image1_path, image2_path,
                                                                     "ROW_INFO : " + group[0]['xml'] + "|" + str(
                                                                         int(group[0]['row'])),
                                                                     temp_dir, os.path.basename(tmp_file).split(".")[0])
                        print("※" * 10, "difference_count", difference_count)
                        if difference_count is None:
                            image = Image.open(output_path)
                            st.image(image,
                                     caption="シート「" + group[0]['xml'] + "」" + "行目「" + str(int(group[0]['row'])) + "」"
                                             + "現新キャプチャーのピクセルは一致していませんので、チェックしてください。", use_container_width=True)
                            st.divider()
                        elif difference_count == 'reverse':
                            image = Image.open(output_path)
                            st.image(image,
                                     caption="シート「" + group[0]['xml'] + "」" + "行目「" + str(int(group[0]['row'])) + "」"
                                             + "現新キャプチャーは位置が逆になっていますか？確認してください。", use_container_width=True)
                            st.divider()
                        elif difference_count == 'marusame':
                            image = Image.open(output_path)
                            st.image(image,
                                     caption="シート「" + group[0]['xml'] + "」" + "行目「" + str(int(group[0]['row'])) + "」"
                                             + "現新キャプチャーのピクセルがまったく同じです。確認してください。", use_container_width=True)
                            st.divider()
                        elif difference_count > 0:
                            image = Image.open(output_path)
                            st.image(image,
                                     caption="シート「" + group[0]['xml'] + "」" + "行目「" + str(int(group[0]['row'])) + "」"
                                             + "キャプチャーには「" + str(difference_count) + "」処違うことがある。",
                                     use_container_width=True)
                            st.divider()
                        else:
                            image = Image.open(output_path)
                            st.image(image,
                                     caption="シート「" + group[0]['xml'] + "」" + "行目「" + str(int(group[0]['row'])) + "」"
                                             + "よくできました。",
                                     use_container_width=True)
                            st.divider()
                    else:
                        image = Image.open(output_path)
                        st.image(image,
                                 caption="シート「" + group[0]['xml'] + "」" + "行目「" + str(int(group[0]['row'])) + "」"
                                         + "現新キャプチャーが不足です",
                                 use_container_width=True)
                        st.divider()
                del_folder(os.path.join(temp_dir, os.path.basename(tmp_file).split(".")[0]))
                os.remove(os.path.join(temp_dir, os.path.basename(tmp_file).split(".")[0] + ".zip"))
                os.remove(os.path.join(temp_dir, os.path.basename(tmp_file).split(".")[0] + ".xlsx"))
            st.success("ファイル処理成功: 比較完了。", icon="✅")
        except Exception as e:
            st.error(f"ファイル処理失敗: {e}")
