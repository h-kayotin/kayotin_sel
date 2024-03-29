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
        # 创建显示等待对象
        wait_obj = WebDriverWait(driver, 10)
        wait_obj.until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, 'oj-button-label')
            )
        )
        buttons = driver.find_elements(By.CLASS_NAME, "oj-button-label")
        print(len(buttons))
        # sso_login_bn = buttons[1]
        # sso_login_bn.click()

        input("按回车键关闭")


if __name__ == '__main__':
    my_oracle = OracleRpa()
    my_oracle.do_one()