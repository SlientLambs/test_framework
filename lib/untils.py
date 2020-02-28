# TODO: 框架工具函数
import os
import libs.xlrd as xlrd
from bin.config import DATA_DIR, TESTCASE_DIR, TEMPLATE_FILE


def _find_all_excels():
    """
    搜索所有Excel文件，然后以列表方式返回已经打开的Excel对象
    :return: 包含所有Excel对象的列表
    """
    excels = []
    for e in os.listdir(DATA_DIR):
        if (e.endswith('.xlsx') or e.endswith('.xls')) and e.startswith('t'):
            filename = os.path.join(DATA_DIR, e)
            excel = xlrd.open_workbook(filename)
            excels.append(excel)
    return excels


def _naming_cases():
    """
    命名测试模块，便于区分和准备定位测试数据
    :return: 本项目唯一的测试模块名列表
    """
    file_name_list = []
    for f in os.listdir(DATA_DIR):
        if f.startswith('t'):
            file_name_list.append(f.split('.')[0][8:])
    return file_name_list


def _get_excel_data(excel_object):
    """
    获取该Excel文件下所有Sheet的测试数据，构造成{'casename1':[{row1},{row2}],'casename2':[{row1},{row2}]}形式的字典
    :param: Excel对象
    :return: 通过该Excel文件下所有Sheet构造的测试数据字典
    """
    excel_data = {}
    for sheet in excel_object.sheets():
        sheet_data = []
        for j in range(2, sheet.nrows):
            # 将列名与列值进行打包
            zipped = zip(sheet.row_values(1), sheet.row_values(j))
            # 用打包后的数据生成字典
            di = dict(zipped)
            sheet_data.append(di)
        # 生成sheet与其对应数据的字典
        excel_data[sheet.name] = sheet_data
    return excel_data


def get_all_test_data():
    """
    获取所有测试数据
    :return: 返回包含所有测试数据的字典
    """
    all_excels = _find_all_excels()
    name_list = _naming_cases()
    all_test_data = {}
    for i in range(0, len(name_list)):
        # 生成测试模块名与其对应的字典
        all_test_data[name_list[i]] = _get_excel_data(all_excels[i])
    return all_test_data


test_data = get_all_test_data()


def generate_test_cases():
    """
    使用模板生成测试用例脚本
    :return:
    """
    excels = _find_all_excels()
    file_name_list = _naming_cases()
    case_name = []
    global i
    i = 0

    for f in os.listdir(DATA_DIR):
        case_name.append(f.split('.')[0])

    for i in range(0, len(excels)):

        for sheet in excels[i].sheets():
            file_name = file_name_list[i]
            class_name = ''.join([n.capitalize() for n in (file_name + '_' + sheet.name).split('_')])
            sheet_name = sheet.name
            test_method = sheet.name
            template = TEMPLATE_FILE

            with open(template, encoding='utf-8') as t:
                content = t.read()

            case = TESTCASE_DIR + '%s_%s.py' % (case_name[i], sheet_name)

            with open(case, 'w', encoding='utf-8') as c:
                c.write(
                    content % {'class_name': class_name, 'file_name': file_name,
                               'sheet_name': sheet_name, 'test_method': test_method}
                )

        i += 1
