"""
oracel_rca - 

Author: hanayo
Date： 2024/3/29
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions


class OracleRpa:
    def __init__(self):
        self.main_url = "https://fa-euxo-saasfaprod1.fa.ocs.oraclecloud.com/"
        self.max_worker = 2

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
        wait_obj = WebDriverWait(driver, 10)
        wait_obj.until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@id="idcs-signin-idp-signin-form"]/div')
            )
        )
        # sso登录
        # sso_button = driver.find_element(By.XPATH, '//*[@id="idcs-signin-idp-signin-form"]/div')
        # sso_button.click()

        # 密码登录
        uname_input = driver.find_element(By.XPATH, '//*[@id="idcs-signin-basic-signin-form-username"]')
        uname_input.send_keys("kayotin")
        pwd_input = driver.find_element(By.XPATH, '//*[@id="idcs-signin-basic-signin-form-password|input"]')
        pwd_input.send_keys("123456")
        pw_login_btn = driver.find_element(By.XPATH, '//*[@id="idcs-signin-basic-signin-form-submit"]/button')
        pw_login_btn.click()

        input("按回车键关闭")


if __name__ == '__main__':
    my_oracle = OracleRpa()
    my_oracle.do_one()
