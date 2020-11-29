"""
提供在校学生日报的功能
"""

from typing import Dict
from selenium import webdriver
import os
import time


def in_daily_report(config: Dict[str, str], is_moring):
    """
    在校学生的日报功能，输入要上报的参数
    :param config:
    :param is_moring:
    :return:
    """

    # 导入浏览器驱动
    browser = None
    abspath = os.path.split(os.path.abspath(__file__))[0]
    if config['browser'] == 'chrome':
        executable_path = os.path.join(
            os.path.join(abspath, 'chromedriver'), 'chromedriver_' + config['operating_system']
        )
        browser = webdriver.Chrome(executable_path=executable_path)
        browser.get(url='https://selfreport.shu.edu.cn')

    # 登陆
    browser.find_element_by_id('username').send_keys(config['student_id'])
    time.sleep(0.3)
    browser.find_element_by_id('password').send_keys(config['password'])
    time.sleep(0.3)
    browser.find_element_by_id('submit').click()
    time.sleep(0.3)

    # 进入在校学生日报
    browser.find_element_by_id('lnkReport').click()
    time.sleep(0.3)

    if is_moring:
        browser.find_element_by_id('p1_Button1').click()
    else:
        browser.find_element_by_id('p1_Button2').click()
    time.sleep(0.3)

    # 填写信息
    browser.find_element_by_id('p1_ChengNuo-inputEl-icon').click()  # 承诺
    time.sleep(0.3)

    browser.find_element_by_id('p1_BaoSRQ-inputEl').click()  # 日期
    time.sleep(0.3)

    browser.find_element_by_id('fineui_30').click()  # 今天
    time.sleep(0.3)

    browser.find_element_by_id('fineui_0-inputEl-icon')  # 身体状况良好
    time.sleep(0.3)

    browser.find_element_by_id('p1_TiWen-inputEl').clear()  # 体温清空
    time.sleep(0.3)

    browser.find_element_by_id('p1_TiWen-inputEl').send_keys(config['temperature'])  # 体温填写
    time.sleep(0.3)

    if config['campus'] == 0:  # 当天是否在校
        browser.find_element_by_id('fineui_5-inputEl-icon').click()
    elif config['campus'] == 1:
        browser.find_element_by_id('fineui_6-inputEl-icon').click()
    elif config['campus'] == 2:
        browser.find_element_by_id('fineui_7-inputEl-icon').click()
    elif config['campus'] == 3:
        browser.find_element_by_id('fineui_8-inputEl-icon').click()
    elif config['campus'] == 4:
        browser.find_element_by_id('fineui_9-inputEl-icon').click()
    time.sleep(0.3)

    browser.find_element_by_id('p1_ddlSheng-inputEl').click()
    time.sleep(0.3)

    browser.find_element_by_css_selector('body > ul:nth-child(2) > li:nth-child(4)').click()    # 当天所在省
    time.sleep(0.3)

    browser.find_element_by_id('p1_ddlShi-inputEl').click()
    time.sleep(0.3)

    browser.find_element_by_css_selector('body > ul:nth-child(3) > li:nth-child(2)').click()    # 当天所在市
    time.sleep(0.3)

    browser.find_element_by_id('p1_ddlXian-inputEl').click()
    time.sleep(0.3)

    browser.find_element_by_css_selector('body > ul:nth-child(4) > li:nth-child(10)').click()    # 当天所在县区
    time.sleep(0.3)

    browser.find_element_by_id('fineui_11-inputEl-icon').click()  # 过去14天是否在中高风险地区逗留
    time.sleep(0.3)

    browser.find_element_by_id('fineui_13-inputEl-icon').click()  # 上海同住人员是否有近14天来自中高风险地区的人
    time.sleep(0.3)

    browser.find_element_by_id('p1_XiangXDZ-inputEl').clear()
    time.sleep(0.3)

    browser.find_element_by_id('p1_XiangXDZ-inputEl').send_keys(config['address'])  # 具体地址
    time.sleep(0.3)

    browser.find_element_by_id('p1_QueZHZJC-inputEl').click()
    time.sleep(0.3)

    browser.find_element_by_css_selector('body > ul:nth-child(5) > li:nth-child(2)').click()  # 是否曾与确诊患者有密切接触
    time.sleep(0.3)

    browser.find_element_by_id('fineui_15-inputEl-icon').click()  # 当天是否隔离
    time.sleep(0.3)

    browser.find_element_by_id('fineui_21-inputEl-icon').click()  # 11月10日至11月24日是否与来自中高风险地区发热人员密切接触
    time.sleep(0.3)

    browser.find_element_by_id('fineui_23-inputEl-icon').click()  # 11月10日至11月24日是否乘坐公共交通途径中高风险地区
    time.sleep(0.3)

    browser.find_element_by_id('fineui_26-inputEl-icon').click()  # 当天健康码颜色
    time.sleep(0.3)

    browser.find_element_by_id('fineui_27-inputEl-icon').click()  # 截止今天是否连续14天健康码为绿色
    time.sleep(0.3)

    browser.find_element_by_id('p1_ctl00_btnSubmit').click()      # 提交
    time.sleep(0.3)

    browser.find_element_by_id('fineui_34').click()
    time.sleep(3)   # 暂停运行3秒，查看填报结果
    browser.close()

