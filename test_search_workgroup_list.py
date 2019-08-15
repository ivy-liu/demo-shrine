#coding=utf-8
import unittest
import os
import sys
base_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#获取当前项目路径并添加到path中
sys.path.append(base_path)

import os
import sys
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
from config import base
from  public import  random_num
from public import account
import requests, json
import random
'''
20190110现需求
进入列表，默认显示页码1，页大小10
值page,size为必填项，传值空或0时，自动赋值page=1,size=10
'''

class SearchWorkGroupList(unittest.TestCase):
    '''刘婉莹 查询工作组列表'''

    url = base.base_url + "/listWorkGroups@workGroupAdmin"
    print("现执行用例——查看工作组列表" + url + "\n")

    # 拿到列表总数据量、总页数
    def get_totalElements(self):
        body = {
            "content": {
                "pageRequest": {
                    "page": 0,
                    "size": 0
                }
            }
        }
        resp = requests.post(self.url, json=body)
        print(resp.status_code, resp.json())
        js = resp.json()
        totalElements=js["content"]["totalElements"]
        print("获取列表总数量成功--",totalElements,"条")
        tmp = 0  # 总页数
        if (totalElements % 10 > 0 and totalElements>10):
            tmp = totalElements // 10 + 1
        elif(totalElements > 0 and totalElements<10):
            tmp=1
        else:
            tmp = totalElements // 10
        return totalElements,tmp

    #执行切换页码
    def get_page_result(self,page):
        body = {
            "content": {
                "pageRequest": {
                    "page": page,
                    "size": 0
                }
            }
        }
        resp = requests.post(self.url, json=body)
        print(resp.status_code, resp.json())
        return resp.json()

    #成功实例，断言
    def get_assertion_success(self,js):
        # 校验返回的状态码
        self.assertEqual(js["code"], 200, "返回的状态码不是200！")
        # 校验返回的状态
        self.assertEqual(js["success"], True, "返回的状态不是True！")
        # 校验返回的message
        self.assertEqual(js["message"], "OK", "返回的message不是OK！")

    #异常录入实例，断言
    def get_assertion_failure(self,js):
        # 校验返回的状态码
        self.assertEqual(js["code"], 400, "录入非int类型页码，此处应返回状态码400，现返回"+str(js["code"]))
        # 校验返回的状态
        self.assertEqual(js["success"], False, "录入非int类型页码，返回的状态应是False，现返回"+str(js["success"]))
        # 校验返回的message
        self.assertEqual(js["message"], "Deserialize json to bean error", "录入非int类型页码，返回的message异常，现返回"+js["message"])
        # 校验返回的数据数量
        #self.assertEqual(js["content"]["numberOfElements"], 10, "当前页面列表显示数据不是10条！")


    def test_defult_pagination(self):
        '''进入列表，默认显示页码1，页大小10'''
        page=0
        js = self.get_page_result(page)
        self.get_assertion_success(js)
        totalElements, tmp = self.get_totalElements()
        # 校验返回的当前页面数据数量
        if(totalElements>=10):
            self.assertEqual(js["content"]["numberOfElements"], 10, "初次打开列表，列表存在数据>=10，第1页显示不是10条！")
        else:
            self.assertEqual(js["content"]["numberOfElements"], totalElements, "初次打开列表，列表存在数据<10，第1页显示不是全部数据！")


    def test_search_pagination_success(self):
        '''录入页码，产生查询数据'''
        totalElements,tmp=self.get_totalElements()
        page=0
        size=0

        #切换至随机页
        if(tmp>10):
            count = 5 #大于10页，查看5次页码
            for num in range(count):
                print("现列表共{}页，大于10页执行5次，现执行第{}次".format(tmp,num+1))
                page = random.randint(1, tmp)
                print("现切换至第{}页".format(page))
                js=self.get_page_result(page)
                self.get_assertion_success(js)

        elif(tmp>1 and tmp<=10):
            count = 2 #小于10页，查看2次页码
            for num in range(count):
                print("现列表共{}页，执行2次，现执行第{}次".format(tmp, num + 1))
                page = random.randint(1, tmp)
                print("现切换至第{}页".format(page))
                js=self.get_page_result(page)
                self.get_assertion_success(js)
        else:
            #tmp=1,无页码可进行切换
            print("页码等于1，或当前列表空，无数据")

        #切换至最后1页
        theLastpage_numberOfElements = totalElements % 10
        js = self.get_page_result(tmp)
        self.get_assertion_success(js)
        if(theLastpage_numberOfElements>0):
            print("当前验证最后一页，此时总数量非10倍数")
            # 校验返回的当前页面数据数量
            self.assertEqual(js["content"]["numberOfElements"], theLastpage_numberOfElements, "总数量非10倍数，最后1页列表显示数据不等于总数量除以10取余！")
        else:
            # 校验返回的当前页面数据数量
            self.assertEqual(js["content"]["numberOfElements"], 10, "总数量时10倍数，最后1页列表显示数据不等于10！")

    def test_search_pagination_failure(self):
        '''录入异常页码，产生查询数据'''

        #录入非int类型页码
        page_list_01=["dfcnjDDUIbhjn","哈哈哈哈哈哈","!@#$%&^%$#sdfdv"]
        for page_01 in page_list_01:
            print("当前page传值：",page_01)
            js=self.get_page_result(page_01)
            self.get_assertion_failure(js)

        #录入不存在页码
        totalElements,tmp=self.get_totalElements()
        page_list_02=[]
        for i in range(0,6):
            add_elements = random.randint(tmp+1,100000)
            page_list_02.append(add_elements)
        print("page_list_02:",page_list_02)

        for page_02 in page_list_02:
            print("当前page传值：",page_02)
            js=self.get_page_result(page_02)
            self.get_assertion_success(js)
            # 校验返回的数据数量
            self.assertEqual(js["content"]["numberOfElements"], 0, "当前页码超过已有页数，列表显示数据不是0条！")
if __name__ == "__main__":
    unittest.main()



































