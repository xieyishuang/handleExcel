import json
import logging as log
import requests
import pymysql
import pytest
import allure


class TestApiDemo(object):

    # 使用request库发送请求
    def __send_api_request__(self):
        url = ""
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        log.info('Api status code is %s', response.status_code)
        return response.content

    # 使用pymysql建立数据库连接
    def __mysql_connection__(self):
        db = pymysql.connect("localhost","root","LBLB1212@@","dbforpymysql")
        cursor = db.cursor()
        sql = ''
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    # 比较api获取的结果和mysql中查询出的结果
    def __compare_result__(self):
        apiresult = self.__send_api_request__()
        dbresult  = self.__mysql_connection__()
       #Compare apiresult with dbresult，这里要自己处理的，不能直接这么写，我给的是伪代码
        if apiresult == dbresult:
            return True
        else:
            log.info('%s is unavailable in XXXXX',apiresult)
            log.info('%s is unavailable in YYYYY',dbresult)
            return False


    # 测试主体
    # 用例号
    @allure.testcase("DAP007-DAP013")
    @allure.severity('P1')
    @allure.title('Regional DAP generate and compare')
    @allure.description('Regional DAP generate and compare')
    # 填入相关的故事
    @allure.story('https://jira.nike.com/browse/GCT-6966')
    # 设置参数，用逗号分隔
    @pytest.mark.parametrize('pousheng', 'really')
    def run(self):
        assert self.__compare_result__() == True



if __name__ == '__main__':
    runner = TestApiDemo()
    runner.run()