# TODO：测试过程执行文件
# 把项目路径加入PYTHONPATH
import os
import sys


path = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
sys.path.append(path)

from time import strftime
from unittest import defaultTestLoader
from lib.untils import generate_test_cases
from bin.config import TESTCASE_DIR, REPORT_DIR
from libs.BeautifulReport import BeautifulReport

generate_test_cases()
tests = defaultTestLoader.discover(TESTCASE_DIR, pattern='test*.py')
runner = BeautifulReport(tests)
runner.report(
    filename='Report' + strftime('_%y%m%d_%H-%M-%S') + '.html',
    report_dir=REPORT_DIR,
    description='系统接口测试报告',
)
