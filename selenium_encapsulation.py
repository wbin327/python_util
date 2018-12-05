# coding:utf-8
"""
封装selenium
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class By(object):
    """
    Set of supported locator strategies.
    """

    ID = "id"
    XPATH = "xpath"
    LINK_TEXT = "link text"
    PARTIAL_LINK_TEXT = "partial link text"
    NAME = "name"
    TAG_NAME = "tag name"
    CLASS_NAME = "class name"
    CSS_SELECTOR = "css selector"


class SeleniumEncapsulation(object):
    DEFAULT_TIME = 10
    DEFAULT_BY = 'id'
    DEFAULT_BROWSER = 'chrome'

    def __init__(self, driver_path=None, browser='chrome'):
        """
        创建浏览器实例
        :param kwargs: 字典类型的参数
        :return: None
        """

        # 浏览器驱动路径
        if not driver_path:
            raise Exception('请在实例化对象时，传入浏览器驱动路径driver_path')

        # 设置默认值
        if browser.lower() == 'chrome':
            self.driver = webdriver.Chrome(driver_path)
        if browser.lower() == 'firefox':
            self.driver = webdriver.Firefox()
        if browser.lower() == 'ie':
            self.driver = webdriver.Ie()

    def close(self):
        """
        关闭一个标签页
        :return: None
        """
        self.driver.close()

    def quit(self):
        """
        关闭整个浏览器，部署在服务器上时，最后需要使用这个方法关闭浏览器进程，否则进程会一直挂在后台，占用资源
        :return: None
        """
        self.driver.quit()

    def get(self, url: str):
        """
        使浏览器打开一个页面，并返回该页面的html
        :param url: 网址
        :return: None
        """
        self.driver.get(url)

    def wait(self, **kwargs: dict):
        """
        显示等待页面加载，防止页面未完成加载就执行脚本，导致页面上原本可以找到的元素，因为没有加载的问题而找不到
        参数说明
        1.wait_time, int类型,页面等待时间，默认值为10
        2.by, str类型,定位方式，例如css,xpath
        3.location,str类型，具体的定位，例如#id
        4.wait_func, 等待判断函数
        :param kwargs: 字典类型的参数
        :return: None
        """

        # 等待的页面元素出现的方式，例如等待页面直到该元素可以被点击
        wait_func_map = {
            # 该元素可以被定位
            'located': 'presence_of_element_located',
            # 元素可以被点击
            'click': 'element_to_be_clickable',
            # 元素可见
            'visibility': 'visibility_of_element_located',
            # 元素不可见
            'invisibility': 'invisibility_of_element_located',
            # 元素可以被选择
            'selected': 'element_to_be_selected',
        }

        # 获取等待页面加载的时间，默认为10
        wait_time = kwargs.get('wait_time', self.DEFAULT_TIME)
        # 等待页面元素出现的方式
        wait_func = kwargs['wait_func']
        # 获取页面元素定位的方式, 默认为根据id进行定位
        by = kwargs.get('by', self.DEFAULT_BY)
        # 定位,必填参数，因为每个页面的元素的定位都不同
        location = kwargs['location']

        wait = WebDriverWait(self.driver, wait_time)
        ec_func = getattr(EC, wait_func_map[wait_func])
        wait.until(ec_func((by, location)))

    def find_element(self, by=By.ID, location=None):
        """
        查询页面元素
        :param by:selenium.webdriver.common.by
        :param location:具体的元素定位
        :return: 返回一个查询到的页面元素实例
        """
        if not location:
            raise Exception('查询页面元素时请传入页面元素的定位location')
        return self.driver.find_element(by, location)

    def find_elements(self, by=By.ID, location=None):
        """
        查询页面元素
        :param by:selenium.webdriver.common.by
        :param location:具体的元素定位
        :return: 返回一个列表，保存所有查询到的页面元素实例
        """
        if not location:
            raise Exception('查询页面元素时请传入页面元素的定位location')
        return self.driver.find_elements(by, location)

    @staticmethod
    def transform_select(element):
        select = Select(element)
        return select

    @staticmethod
    def select(select: object, value, method='index'):
        if method == 'index':
            select.select_by_index(value)
        if method == 'text':
            select.select_by_visible_text(value)
        if method == 'value':
            select.select_by_value(value)

    ############################################      页面操作          ###############################################

    def send_keys(self, element, text=''):
        """输入值到文本框中"""
        element.send_keys(text)


if __name__ == '__main__':
    driver_path = '/Users/pundix053/WorkSpace/script/chromedriver'
    browser = SeleniumEncapsulation(driver_path=driver_path)
    browser.get('https://www.baidu.com')
    browser.wait(wait_time=10, by=By.id, location='u1', wait_func='located')
    browser.quit()