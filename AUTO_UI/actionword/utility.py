from selenium import webdriver
import time, requests, os
from public_method.config import Config,REPORT_PATH,DATA_PATH
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from public_method.log import logger

class Utility(object):

    driver = None       # 将driver定义为类级变量，不随实例化而被重新赋值为None

    def __init__(self,datafile=DATA_PATH+'/logdata.txt'):
        self.datafile = datafile

    @classmethod
    def get_webdriver(cls):
        if cls.driver is None:
            cls.driver = webdriver.Chrome()
            cls.driver.get(Config().get('URL'))
            try:
                cls.driver.maximize_window()
            except:
                pass
            cls.driver.implicitly_wait(10)
            time.sleep(5)
        return cls.driver

    def position_test(self, method, position):
        driver = Utility.get_webdriver()
        try:
            if method == u"link_text":
                ele = driver.find_element_by_link_text(position)
            elif method == u"id":
                ele = driver.find_element_by_id(position)
            elif method == u"xpath":
                ele = driver.find_element_by_xpath(position)
            elif method == u"css":
                ele = driver.find_element_by_css_selector(position)
            elif method == u"name":
                ele = driver.find_element_by_name(position)
        except Exception:
            print("没有这个元素")
            path = os.path.abspath('../report/')
            name = path + self.t + ".png"
            driver.get_screenshot_as_file(name)
        else:
            return ele

    # 这是一个打开网站的函数，通过data来接收url的值
    def open_test(self, data):
        driver = Utility.get_webdriver()
        # 最大化窗口
        driver.maximize_window()
        # 设置隐形等待时间
        driver.implicitly_wait(10)
        # 打开网站
        driver.get(data)

    #点击
    def click_test(self, method, position):
        ele = self.position_test(method, position)
        ele.click()

    #输入
    def input_test(self, method, position, data):
        ele = self.position_test(method, position)
        ele.clear()
        ele.send_keys(data)

    def q_input_test(self, method, position, data):
        driver = Utility.get_webdriver()
        #     data = data.encode("utf-8")      如果页面出现中文编码问题，就将excel中的unicode重新编码成utf-8
        ele = self.position_test(method, position)
        action = ActionChains(driver)
        #
        action.move_to_element(ele).click().send_keys(data).perform()

    def frame_test(self, method, position, data):
        driver = Utility.get_webdriver()
        if int(data) == 1:
            ele = self.position_test(method, position)
            driver.switch_to.frame(ele)
        elif int(data) == 0:
            driver.switch_to_default_content()
        elif int(data) == 2:
            driver.switch_to.parent_frame()

    #窗口切换
    def window_test(self):
        driver = Utility.get_webdriver()
        handle = driver.window_handles
        driver.switch_to.window(handle[-1])

    #鼠标点击拖拉到某个位置
    def drag_test(self, method, position, data):
        driver = Utility.get_webdriver()
        s = self.position_test(method, position)
        offset = str(data).split(",")
        action = ActionChains(driver)
        action.drag_and_drop_by_offset(s, int(offset[0]), int(offset[1])).perform()


    #检查元素
    def check_test(self, method, position, data):
        data = int(data)
        if data == 1:
            ele = self.position_test(method, position)
            if ele == None:
                raise Exception  # raise是由用户来手动的主动的抛出错误信息
        elif data == 0:
            ele = self.position_test(method, position)
            if ele != None:
                raise Exception

    def wait_test(self, data):
        time.sleep(int(data))

    #下拉选择
    def select_test(self, method, position, data):
        ele = self.position_test(method, position)
        s = Select(ele)
        s.select_by_visible_text(data)

    def move_test(self, method, position):
        driver = Utility.get_webdriver()
        ele = self.position_test(method, position)
        action = ActionChains(driver)
        action.click_and_hold().move_to_element(ele).release().perform()

    def keys_test(self, method, position, data):
        ele = self.position_test(method, position)
        if data == u'下箭头':
            ele.send_keys(Keys.ARROW_DOWN)
        elif data == u'回车':
            ele.send_keys(Keys.ENTER)
        elif data == u'HOME':
            ele.send_keys(Keys.HOME)

    def js_alert_test(self, data):
        driver = Utility.get_webdriver()
        alert = driver.switch_to.alert()
        data = int(data)
        if data == 1:
            alert.accept()
        elif data == 0:
            alert.dismiss()

    def open(self,data):
        data = Config().get(data)
        msg = f'打卡首页data={data}'
        logger.info(msg)
        #self.open_test(data)
        pass

    def input_user(self,method,position,data):
        msg = f'输入用户名method={method},position={position},data={data}'
        logger.info(msg)
        #self.input_test(method,position,data)
        pass

    def input_password(self,method,position,data):
        msg = f'输入密码method={method},position={position},data={data}'
        logger.info(msg)
        pass

    def input_checkcode(self,method,position,data):
        msg = f'输入验证码method={method},position={position},data={data}'
        logger.info(msg)
        pass

    def click_login(self,method,position):
        msg = f'提交method={method},position={position}'
        logger.info(msg)
        pass

if __name__ == '__main__':
    print(Utility.get_webdriver())