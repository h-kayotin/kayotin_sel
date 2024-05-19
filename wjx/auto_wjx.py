"""
auto_wjx - 问卷星自动填写问卷

Author: hanayo
Date： 2024/2/29
"""
import random
import sys
import time

import requests
import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import utils
from concurrent.futures import ThreadPoolExecutor
from threading import RLock
from selenium.common.exceptions import NoSuchElementException


# 对选择题做处理
handle_type_dict = {
    '3': utils.single_choice,  # 单选
    '4': utils.multi_choice,  # 多选
    '5': utils.single_scale,  # 单量表题
    '7': utils.select,  # 矩阵多选
    '8': utils.single_slide,
    '11': utils.sort,
    '12': utils.multi_slide
}


class MyWjx:

    def __init__(self, url, num):
        self.wj_url = url
        # 一共做几份
        self.total_num = num
        self.answers = config.answers
        self.txt_answers = config.answer_list
        self.api = config.api
        self.ua = config.UA
        self.option = webdriver.EdgeOptions()
        self.option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.option.add_experimental_option('useAutomationExtension', False)
        # 每道题之间的间隔时间
        self.sleep_sec = 0.4
        # 记录已经做了几份
        self.job_count = 0
        # 同时做几份
        self.max_workers = 4
        # 线程锁
        self.lock = RLock()

    def get_ip_proxy(self):
        """获取代理IP"""
        ip = requests.get(self.api).text
        self.option.add_argument(f'--proxy-server={ip}')

    def fill_in(self):
        """填写一份问卷"""
        driver = webdriver.Edge(options=self.option)
        # 随机User-agent
        num = random.randint(0, 2)
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": self.ua[num]})
        # 将webdriver属性置为undefined
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                               {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})

        driver.get(self.wj_url)

        # 从题号1开始
        index = 1
        # 获取网页上题目总量，然后遍历
        questions = driver.find_elements(By.CLASS_NAME, "field.ui-field-contain")
        for i in range(1, len(questions) + 1):
            xpath = '//*[@id="div{}"]'.format(i)
            question = driver.find_element(By.XPATH, xpath)
            # 获取题目类型
            ques_type = question.get_attribute("type")
            if ques_type in handle_type_dict:
                index = handle_type_dict[ques_type](driver, i, self.answers, index)
            elif ques_type == '2':
                index = utils.fill_blank(driver, i, self.txt_answers, index)
            elif ques_type == '6':
                xpath = '//*[@id="div{}"]/div[1]/div[2]/span'.format(i)
                if driver.find_element(By.XPATH, xpath).text.find("【") != -1:
                    index = utils.multi_matrix_scale(driver, i, self.answers, index, num)
                else:
                    index = utils.single_matrix_scale(driver, i, self.answers, index, num)
            else:
                print("没有该题型")
                sys.exit(0)
            time.sleep(self.sleep_sec)

        # 提交
        time.sleep(0.5)
        submit_button = driver.find_element(By.XPATH, '//*[@id="ctlNext"]')
        submit_button.click()
        time.sleep(1)

        # 请点击智能验证码进行验证！
        try:
            confirm = driver.find_element(By.XPATH, '//*[@id="layui-layer1"]/div[3]/a')
            confirm.click()
            time.sleep(1)
        except NoSuchElementException:
            print("本次无需验证")

        # 点击按钮开始智能验证
        try:
            button = driver.find_element(By.XPATH, '//*[@id="SM_BTN_WRAPPER_1"]')
            button.click()
            time.sleep(0.5)
        except NoSuchElementException:
            # 这个报错太长了就不打印了
            pass

        # 滑块验证
        try:
            slider = driver.find_element(By.XPATH, '//*[@id="nc_1__scale_text"]/span')
            time.sleep(0.3)
            if str(slider.text).startswith("请按住滑块，拖动到最右边"):
                width = slider.size.get('width')
                ActionChains(driver).drag_and_drop_by_offset(slider, width, 0).perform()
                time.sleep(1)
        except NoSuchElementException:
            pass

        # 关闭浏览器，退出
        time.sleep(2)
        driver.quit()

        # 计数统计
        self.lock.acquire()
        self.job_count += 1
        self.lock.release()
        print(f"已完成{self.job_count}份")

    def do_works(self):
        """使用进程池子多线程得做问卷"""
        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            for i in range(self.total_num):
                pool.submit(self.fill_in)


if __name__ == '__main__':
    my_url = "https://www.wjx.cn/vm/rJoCZrn.aspx"
    my_wjx = MyWjx(my_url, 2)
    # my_wjx.fill_in() 做1份
    # 多进程做多份
    my_wjx.do_works()


        
        




