"""
oracle_rca -

Author: hanayo
Date： 2024/3/29
"""
import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys

def wait_for_load(driver, sec: int, xpath_str):
    """
    等待页面加载出来后再点击
    :param driver: 浏览器对象
    :param sec: 默认等待时间
    :param xpath_str: 对象按钮的xpath
    :return: 无
    """
    wait_obj = WebDriverWait(driver, sec)
    wait_obj.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, xpath_str)
        )
    )


def get_month():
    now = datetime.datetime.now()
    year, month = now.year, now.month - 1
    if month == 1:
        year -= 1
        month = 12
    info_str = f"手机费用报销{year}年{month}月"
    return info_str


class OracleRpa:
    def __init__(self):
        self.main_url = "https://fa-euxo-saasfaprod1.fa.ocs.oraclecloud.com/"
        self.max_worker = 2
        self.username = "江海"
        self.info_str = f"{self.username}{get_month()}"

        self.option = webdriver.EdgeOptions()
        self.option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.option.add_experimental_option('useAutomationExtension', False)
        self.ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                  "Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"

    def do_one(self):
        driver = webdriver.Edge(options=self.option)
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": self.ua})
        # 将webdriver属性置为undefined
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                               {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})

        driver.get(self.main_url)

        # 创建显示等待对象，等sso按钮加载出来
        wait_for_load(driver, 10, '//*[@id="idcs-signin-idp-signin-form"]/div')
        # sso登录
        sso_button = driver.find_element(By.XPATH, '//*[@id="idcs-signin-idp-signin-form"]/div')
        sso_button.click()

        # 密码登录
        # uname_input = driver.find_element(By.XPATH, '//*[@id="idcs-signin-basic-signin-form-username"]')
        # uname_input.send_keys("kayotin")
        # pwd_input = driver.find_element(By.XPATH, '//*[@id="idcs-signin-basic-signin-form-password|input"]')
        # pwd_input.send_keys("123456")
        # pw_login_btn = driver.find_element(By.XPATH, '//*[@id="idcs-signin-basic-signin-form-submit"]/button')
        # pw_login_btn.click()

        # 等待主页按钮刷出来
        wait_for_load(driver, 10, '//*[@id="pt1:_UISpgl52u"]')
        # 点击主页按钮
        time.sleep(1)
        home_btn = driver.find_element(By.XPATH, '//*[@id="pt1:_UISpgl52u"]')
        home_btn.click()

        # 等待费用按钮刷出来
        # try:
        #     wait_for_load(driver, 10, '//*[@id="itemNode_my_information_expenses"]')
        # except TimeoutException:
        #     home_btn.click()

        # 点击费用
        wait_for_load(driver, 10, '//*[@id="itemNode_my_information_expenses"]')
        expense_btn = driver.find_element(By.XPATH, '//*[@id="itemNode_my_information_expenses"]')
        time.sleep(1)
        expense_btn.click()

        # 点击创建报表
        wait_for_load(driver, 10, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt0:pt12:r2:0:pgl14"]')
        report_btn = driver.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:_FOTsr1:0:pt0:pt12:r2:0:pgl14"]')
        time.sleep(1)
        report_btn.click()

        # 等待费用报表页面加载出来
        wait_for_load(driver, 10, '//*[@id="pt1:_FOr1:1:_FONSr2:0:MAnt2:1:AP1:it1::content"]')

        # 点击创建项
        time.sleep(1)
        create_btn = driver.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:MAnt2:1:AP1:c0012"]')
        create_btn.click()

        # 开始填写手机报销
        # 选择费用类型下拉框
        wait_for_load(driver, 10, '//*[@id="pt1:_FOr1:1:_FONSr2:0:MAnt2:2:AP1:ExpenseTemplateId::content"]')
        time.sleep(1)
        type_select = driver.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:MAnt2:2:'
                                                    'AP1:ExpenseTemplateId::content"]')
        Select(type_select).select_by_value('6')
        # 选择手机费
        type_detail_select = driver.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:MAnt2:2:'
                                                           'AP1:ExpenseTypeId::content"]')
        Select(type_detail_select).select_by_value('4')
        # 填写金额
        input_money = driver.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:MAnt2:2:'
                                                    'AP1:ReceiptAmount::content"]')
        input_money.send_keys("88")
        # 填写说明
        time.sleep(1)
        input_info = driver.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:MAnt2:2:AP1:Description::content"]')

        input_info.send_keys(self.info_str)
        # 点击保存
        save_btn = driver.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:MAnt2:2:AP1:SaveAndCloseButton"]')
        save_btn.click()

        # 填写用途
        wait_for_load(driver, 10, '//*[@id="pt1:_FOr1:1:_FONSr2:0:MAnt2:1:AP1:it1::content"]')
        time.sleep(1)
        input_use = driver.find_element(By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:MAnt2:1:AP1:it1::content"]')
        input_use.send_keys(self.info_str)

        # 最终保存
        action = webdriver.ActionChains(driver)
        action.key_down(Keys.ALT).send_keys("s").key_up(Keys.ALT).perform()
        input("按回车键关闭")


if __name__ == '__main__':
    my_oracle = OracleRpa()
    my_oracle.do_one()
