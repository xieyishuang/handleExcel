import json
import logging as log
from PIL import Image
import pytesseract
import requests
import pymysql
import pytest
import allure


class TestApiDemo(object):

    def __genereate_image__(self):
        url = "http://192.168.150.61:18080/captcha.jpg?uuid=afbf5ba5-63b2-448f-8c96-bb5714c512a1"
        response = requests.request("GET", url)
        file = open(r'C:\Users\renjie.yu\Desktop\test.png','wb')
        file.write(response.content)
        file.close()
        image = Image.open(r'C:\Users\renjie.yu\Desktop\test.png')
        content = pytesseract.image_to_string(image,lang="eng")
        return content



    # 使用request库发送请求
    def __send_api_request__(self):
        url = "http://192.168.150.61:18080/dms-api-server/complaintRisk/listForPage?org=RH&biz=TD&page=1&limit=1000&contact=&cusName=&cusId=&orgCusId="

        payload = {}
        headers = {
            'token': 'e2bc4cca1f4d2d54e9d2dba83bc68b11',
            'Accept': 'application/json'
        }
        r = requests.request("GET", url, headers=headers, data=payload)
        return r.content

    # 使用pymysql建立数据库连接
    def __mysql_connection__(self):
        db = pymysql.connect("192.168.3.145","all","112233","dms_ucrm")
        cursor = db.cursor()
        sql = '''   SELECT c.cus_id cusId,c.cus_name cusName
  ,r.org_id orgId,r.busi_type busiType,r.org_cus_id orgCusId,r.src_create_time dtAddTime,r.all_phone allPhone
  ,p.rep_level repLevel,p.rep_sign_time repSignTime ,p.rep_sign_desc repSignDesc,p.reg_level regLevel,p.reg_sign_time regSignTime,p.reg_sign_desc regSignDesc
  FROM cust_info c 
  LEFT JOIN cust_busi_emp_rel r ON r.cus_id = c.cus_id AND r.emp_type=1
  LEFT JOIN complaint_risk_sign p on p.org_id=r.org_id AND p.org_cus_id=r.org_cus_id 
  AND (p.busi_type=r.busi_type OR p.busi_type=0)
  WHERE c.cus_id in (SELECT cus_id from complaint_risk_sign)'''
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    # 比较api获取的结果和mysql中查询出的结果
    def __compare_result__(self):
        apiresult = self.__send_api_request__()
        apicompare = json.loads(apiresult)
        dbresult  = self.__mysql_connection__()
        assert apicompare['page']['totalCount'] == len(dbresult)


        lst = []
        lst1 = []

        for item in dbresult:
            dct = {}
            dct['cusId'] = item[0]
            dct['cusName'] = item[1]
            lst.append(dct)

        for item in apicompare['page']['list']:
            dct = {}
            for key in item.keys():
                if key == 'cusId':
                    dct['cusId'] = item['cusId']
                if key == 'cusName':
                    dct['cusName'] = item['cusName']
            lst1.append(dct)

        if lst1 == lst:
            return True
        else:
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

