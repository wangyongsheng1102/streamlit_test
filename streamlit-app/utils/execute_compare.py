import os.path
import shutil
import xml.dom.minidom as xmldom
import xml.etree.ElementTree as ET
import zipfile

import cv2
import imutils
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim


# pic_no_cell = []


def compare_pics(image1_path, image2_path, row_info, temp_dir, tmp_file_name):
    imageA = cv2.imread(image1_path)
    imageB = cv2.imread(image2_path)
    os.makedirs(os.path.join(temp_dir, tmp_file_name, 'evidence_check'), exist_ok=True)
    if imageA.shape[0] != imageB.shape[0] or imageA.shape[1] != imageB.shape[1]:
        return None

    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    template_paths = [f for f in os.listdir(os.path.join(temp_dir, '../exclude-pic')) if f.endswith('.png')]
    index_date1 = template_paths.index("date1.png")
    index_port1 = template_paths.index("port1.png")
    templates = [cv2.imread(os.path.join(temp_dir, '../exclude-pic', template_path), cv2.IMREAD_GRAYSCALE) for
                 template_path in template_paths]

    mask = np.ones(grayB.shape, dtype=np.uint8) * 255

    threshold = 0.9

    for i, template in enumerate(templates):
        template_w, template_h = template.shape[::-1]

        if i == index_port1:
            result_a = cv2.matchTemplate(grayA, template, cv2.TM_CCOEFF_NORMED)
            min_val_a, max_val_a, min_loc_a, max_loc_a = cv2.minMaxLoc(result_a)
            result_b = cv2.matchTemplate(grayB, template, cv2.TM_CCOEFF_NORMED)
            min_val_b, max_val_b, min_loc_b, max_loc_b = cv2.minMaxLoc(result_b)
            if max_val_a < max_val_b:
                return "reverse"
            if max_val_a > threshold and max_val_b > threshold \
                    and max_val_a == max_val_b:
                # and ((max_val_a - max_val_b) < 0.05 or (max_val_b - max_val_a) < 0.05):
                return "marusame"

        # 模板匹配
        result = cv2.matchTemplate(grayB, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print("※" * 10, "image2_path:", image2_path)
        print("※" * 10, "template:", template_paths[i])
        print("※" * 10, "max_val:", max_val)
        if i == index_date1:
            max_loc_list = list(max_loc)
            max_loc_list[0] = max_loc[0]
            max_loc_list[1] = max_loc[1] + 16

            max_loc = tuple(max_loc_list)
            print(max_loc)

        if max_val > threshold:
            # 更新掩膜
            cv2.rectangle(mask, max_loc, (max_loc[0] + template_w, max_loc[1] + template_h), (0, 0, 0), -1)

    # 应用掩膜到图片A和B
    maskedA = cv2.bitwise_and(grayA, grayA, mask=mask)
    maskedB = cv2.bitwise_and(grayB, grayB, mask=mask)
    test_imageA = os.path.join("G:/image-compare", os.path.basename(image1_path))
    cv2.imwrite(test_imageA, maskedA)
    test_image = os.path.join("G:/image-compare", os.path.basename(image2_path))
    cv2.imwrite(test_image, maskedB)

    try:
        (score, diff) = compare_ssim(maskedA, maskedB, full=True)
    except Exception as e:
        return None
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))

    offset = -15

    thresh = cv2.threshold(diff, 0, 255,
                           cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    nb_differences = 0
    for c in cnts:
        if c[:, 0, 0].max() >= 1900:
            continue
        # if c.shape[0] <= 2:
        #     continue
        txt = str(nb_differences + 1)
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(imageB, txt, (x, y + h + offset), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 0, 0), 2)
        image_output = os.path.join(temp_dir, tmp_file_name, "evidence_check", os.path.basename(image2_path))
        cv2.imwrite(image_output, imageB)
        nb_differences += 1

    if nb_differences != 0:
        print("!!!!!" * 20, nb_differences)

        # result_excel_ins(os.path.join(get_program_path(),
        #                               get_str_before_first_dot(
        #                                   get_str_after_last_dot(EXCEL_TOTAL_MAP["EXCEL_EVIDENCE"], "\\"), ".")
        #                               + "-比較結果.xlsx"),
        #                  image_output,
        #                  row_info, nb_differences)
    return nb_differences, image_output

    # cv2.imwrite(os.path.join(os.path.dirname(os.path.abspath(args['first'])), "out.png"), imageB)
    # cv2.imshow("Modified", imageB)

    # cv2.imshow("Diff", diff)
    # cv2.imshow("Thresh", thresh)
    # cv2.waitKey(0)


def get_target_by_id(zip_dir, draw_file_name, rids):
    drawing_file_path = os.path.join(zip_dir, 'xl', 'drawings', '_rels',
                                     draw_file_name.replace(".xml", ".xml.rels"))
    tree = ET.parse(drawing_file_path)
    root = tree.getroot()
    namespace = {'ns': 'http://schemas.openxmlformats.org/package/2006/relationships'}
    relationship = root.find(f".//ns:Relationship[@Id='{rids}']", namespace)
    if relationship is not None:
        return relationship.get('Target').split("/media/")[1]
    else:
        return None


def pic_no_info_create(zip_dir, xml_name, sheet_name):
    pic_no_cell = []
    dom_obj = xmldom.parse(zip_dir + os.sep + 'xl' + os.sep + 'drawings' + os.sep + xml_name)
    element = dom_obj.documentElement

    def _f(subElementObj):
        for anchor in subElementObj:
            xdr_from = anchor.getElementsByTagName('xdr:from')[0]
            pic_col = xdr_from.childNodes[0].firstChild.data
            pic_row = xdr_from.childNodes[2].firstChild.data

            if anchor.getElementsByTagName('xdr:pic'):
                pic_id = \
                    anchor.getElementsByTagName('xdr:pic')[0].getElementsByTagName('xdr:nvPicPr')[
                        0].getElementsByTagName('xdr:cNvPr')[0].getAttribute('id')
                embed_id = \
                    anchor.getElementsByTagName('xdr:pic')[0].getElementsByTagName('xdr:blipFill')[
                        0].getElementsByTagName(
                        'a:blip')[0].getAttribute('r:embed')
                embed = get_target_by_id(zip_dir, xml_name, embed_id)
                pic_no_cell.append({
                    'pic_id': pic_id,
                    'pic': embed,
                    'row': str(int(pic_row) + 1),
                    'column': pic_col,
                    'xml': sheet_name,
                    'anchor': "two"
                })

    def __f(subElementObj):
        for anchor in subElementObj:
            xdr_from = anchor.getElementsByTagName('xdr:from')[0]
            pic_col = xdr_from.childNodes[0].firstChild.data
            pic_row = xdr_from.childNodes[2].firstChild.data

            if anchor.getElementsByTagName('xdr:pic'):
                pic_id = \
                    anchor.getElementsByTagName('xdr:pic')[0].getElementsByTagName('xdr:nvPicPr')[
                        0].getElementsByTagName('xdr:cNvPr')[0].getAttribute('id')
                embed_id = \
                    anchor.getElementsByTagName('xdr:pic')[0].getElementsByTagName('xdr:blipFill')[
                        0].getElementsByTagName(
                        'a:blip')[0].getAttribute('r:embed')
                embed = get_target_by_id(zip_dir, xml_name, embed_id)
                pic_no_cell.append({
                    'pic_id': pic_id,
                    'pic': embed,
                    'row': pic_row,
                    'column': pic_col,
                    'xml': sheet_name,
                    'anchor': "one"
                })

    sub_twoCellAnchor = element.getElementsByTagName("xdr:twoCellAnchor")
    _f(sub_twoCellAnchor)
    sub_oneCellAnchor = element.getElementsByTagName("xdr:oneCellAnchor")
    if sub_oneCellAnchor is not None:
        __f(sub_oneCellAnchor)
    return pic_no_cell


def unzip(file_path):
    file_name = os.path.basename(file_path)
    new_name = str(file_name.split('.')[0]) + '.zip'
    dir_path = os.path.dirname(os.path.abspath(file_path))
    new_path = os.path.join(dir_path, new_name)
    if os.path.exists(new_path):
        os.remove(new_path)
    shutil.copyfile(file_path, new_path)

    with zipfile.ZipFile(new_path, 'r') as file_zip:
        print(file_zip.namelist())
    file_zip = zipfile.ZipFile(new_path, 'r')
    zip_file_name = new_name.split('.')[0]
    zip_dir = os.path.join(dir_path, zip_file_name)
    for files in file_zip.namelist():
        file_zip.extract(files, zip_dir)
    file_zip.close()

    return zip_dir
