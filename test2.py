import json
import requests
import pymysql
import pytest
import allure

# 用例号
@allure.testcase("DAP007-DAP013")
@allure.severity('P1')
@allure.title('Regional DAP generate and compare')
@allure.description('Regional DAP generate and compare')
# 填入相关的故事
@allure.story('https://jira.nike.com/browse/GCT-6966')
# 设置参数，用逗号分隔
@pytest.mark.parametrize('pousheng','really')
class TestApiDemo(object):

    # 使用request库发送请求
    def __send_api_request__(self):
        pass

    # 使用pymysql建立数据库连接
    def __mysql_connection__(self):
        pass

    # 比较api获取的结果和mysql中查询出的结果
    def __compare_result__(self):
        pass

    # 测试主体
    def run(self):
        self.__send_api_request__()
        self.__mysql_connection__()
        self.__compare_result__()
        assert 1==1


if __name__ == '__main__':
    runner = TestApiDemo()
    runner.run()