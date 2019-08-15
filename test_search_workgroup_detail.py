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
#from config import base
from config import base, user_base
from  public import  random_num
#from public import account
from public import account,workgroup
import requests, json
import random

#引入查询工作组列表
#from case.workgroupmanagement.test_search_workgroup_list import SearchWorkGroupList

'''
20190111现需求
进入列表，查询工作组编号
值workGroupId为必填项，且只做精确查询
'''

class SearchWorkGroupDetail(unittest.TestCase):
    '''刘婉莹 查看工作组详情'''

    url = base.base_url + "/getWorkGroup@workGroupAdmin"
    print("现执行用例——查看工作组详情"+url+"\n")

    #查询工作组列表的url
    url_workGroupAdmin = base.base_url + "/listWorkGroups@workGroupAdmin"

    # 执行切换页码
    def get_page_result(self, page):
        # print("zhi", page)
        body = {
            "content": {
                "pageRequest": {
                    "page": page
                    #"size": 0
                }
            }
        }
        resp = requests.post(self.url_workGroupAdmin, json=body)
        js = resp.json()
        return js

    # 拿到列表总数据量 totalElements、所有工作组编号id workGroup_list
    def get_totalElements(self):
        print("拿取总数据量、工作组编号，现请求工作组列表：",self.url_workGroupAdmin)
        #获取列表总数据量totalElements
        body = {
            "content": {
                "pageRequest": {
                    "page": 1
                    #"size": 0
                }
            }
        }
        resp = requests.post(self.url_workGroupAdmin, json=body)
        print(resp.status_code, resp.json())
        js_01 = resp.json()
        totalElements = js_01["content"]["totalElements"]
        print("获取列表总数据量成功--", totalElements, "条")

        #获取列表总数页数tmp,根据总数页数tmp，遍历页面，拿到所有工作组编号id
        tmp = 0  # 总页数
        workGroup_list = []
        #如果总数量大于1页，且最后1页非10条数据
        if (totalElements % 10 > 0 and totalElements>10):
            tmp = totalElements // 10 + 1
            #print("tmp1",tmp)
            for j in range(1, tmp):
                    for i in range(0, 10):
                        js_02 = self.get_page_result(j)
                        workGroup_list.append(js_02["content"]["elements"][i]["id"])
            print("now is workGroup_list:{}，\nid个数{}".format(workGroup_list, len(workGroup_list)))
            print("如果总数量大于1页，且最后1页非10条数据，现整10页id整理完成")
            for i1 in range(0, totalElements%10):
                js_02 = self.get_page_result(tmp)
                workGroup_list.append(js_02["content"]["elements"][i1]["id"])
            print("now is workGroup_list:{}，\nid个数{}".format(workGroup_list,len(workGroup_list)))
            print("如果总数量大于1页，且最后1页非10条数据，现所有id整理完成")

        #总数量不大于1页，且存在数据
        elif (totalElements > 0 and totalElements < 10):
            tmp = 1
            for i in range(0, totalElements):
                js_02 = self.get_page_result(1)
                workGroup_list.append(js_02["content"]["elements"][i]["id"])
            print("now is workGroup_list:{}，\nid个数{}".format(workGroup_list, len(workGroup_list)))
            print("总数量不大于1页，且存在数据，现所有id整理完成")
        ##如果总数量大于1页，且最后1页整10条数据
        else:
            tmp = totalElements // 10
            for j in range(1, tmp):
                for i in range(0, 10):
                    js_02 = self.get_page_result(j)
                    workGroup_list.append(js_02["content"]["elements"][i]["id"])
            print("now is workGroup_list:{}，\nid个数{}".format(workGroup_list, len(workGroup_list)))
            print("总数量是10的倍数，现所有id整理完成")

        return totalElements,workGroup_list

    # 成功实例，断言
    def get_assertion_success(self, js):
        # 校验返回的状态码
        self.assertEqual(js["code"], 200, "返回的状态码不是200！")
        print("现在执行-成功-断言01结束")
        # 校验返回的状态
        self.assertEqual(js["success"], True, "返回的状态不是True！")
        print("现在执行-成功-断言02结束")
        # 校验返回的message
        self.assertEqual(js["message"], "OK", "返回的message不是OK！")
        print("现在执行-成功-断言03结束")
        # 校验返回的数据数量
        # self.assertEqual(js["content"]["numberOfElements"], 1, "当前页面列表显示筛选结果不是1条！")

    # 异常录入实例，断言
    def get_assertion_failure(self, js):
        # 校验返回的状态码
        self.assertEqual(js["code"], 400, "录入非str类型id，此处应返回状态码400，现返回：" + str(js["code"]))
        print("现在执行-失败-断言01结束")
        # 校验返回的状态
        self.assertEqual(js["success"], False, "录入异常类型id，返回的状态应是False，现返回：" + str(js["success"]))
        print("现在执行-失败-断言02结束")
        # 校验返回的message
        self.assertEqual(js["message"], "工作组不存在","录入非工作组id，返回的message异常，现返回：" + js["message"])
        print("现在执行-失败-断言03结束")

    def creat_workgroup_result(self):
        '''新建工作组，返回创建工作组信息body、创建成功后工作组中id'''
        username, password, user_id = account.create_account()
        print("登陆信息获取完成")
        print("username, password, user_id___:",username, password, user_id)
        url = base.base_url + "/createWorkGroup@workGroupAdmin"
        body = {
            "content": {
                "workGroupForm": {
                    "province": random_num.randomString(),
                    "contact": random_num.randomString(),
                    "email": random_num.randomString(),
                    "name": random_num.randomString(),
                    "city": random_num.randomString(),
                    "accessUrl": random_num.randomString(),
                    "address": random_num.randomString(),
                    "type": user_base.WorkGroupType_Internal,
                    "mobile": random_num.randomString(),
                    "leaderAccountId": user_id,
                    "invoiceUrl": random_num.randomString(),
                    "accountNo": random_num.randomString(),
                    "accountBank": random_num.randomString(),
                    "invoiceTitle": random_num.randomString(),
                    "accountName": random_num.randomString(),
                    "licenseUrl": random_num.randomString(),
                    "logoUrl": random_num.randomString(),
                    "remark": random_num.randomString(),
                }
            }
        }
        resp = requests.post(url, json=body)
        workGroupId = resp.json()["content"]
        print("创建工作组成功,工作组id:",workGroupId)
        print("创建工作组成功,返回：",json.dumps(resp.json()))
        return body,workGroupId

    # 执行工作组编号查询
    def get_workGroupId_result(self, workGroupId):
        body = {
            "content": {
                "workGroupId": workGroupId
            }
        }
        resp = requests.post(self.url, json=body)
        print("查询成功返回：", json.dumps(resp.json()))
        return resp.json()

    def test_search_workGroupId_success(self):
        #随机查询4个id
        totalElements, workGroup_list=self.get_totalElements()
        for num in range (0,4):
            workGroupId_01 = workGroup_list[random.randint(0, len(workGroup_list))]
            print("现执行-成功-用例，第{}次工作组编号查询，查询编号是{}".format(num + 1, workGroupId_01))
            js = self.get_workGroupId_result(workGroupId_01)
            self.get_assertion_success(js)

        #新建工作组（），查询id，比对结果
        js_01,workGroupId_02=self.creat_workgroup_result()
        print("拿到创建工作组的工作组id：",workGroupId_02)
        print("拿到创建工作组的信息body：",js_01)
        js_02=self.get_workGroupId_result(workGroupId_02)
        print("搜索创建的工作组的id，返回结果：",js_02)
        print("此处开始断言-")
        self.get_assertion_success(js_02)
        print("此处开始断言-比较创建数据和查询结果")
        check_list = ["province", "contact", "email", "name", "city", "accessUrl", "address", "type", "mobile",
                      "leaderAccountId",
                      # "invoiceUrl",
                      "accountNo", "accountBank", "invoiceTitle", "accountName",
                      # "licenseUrl", "logoUrl",
                      "remark"]
        for check_element in check_list:
            self.assertEqual(js_01["content"]["workGroupForm"][check_element], js_02["content"][check_element],
                             "校验创建与搜索结果{}不一致！".format(check_element))
            print(" now is checking :",check_element)

    def test_search_workGroupId_failure(self):
        #查询不存在的工作组id
        num=0
        workGroupId_list=["fgj34566SDDD","!@#$%&^%新年快乐","12345678990","qw^^{{123新年好"]
        for workGroupId in workGroupId_list:
            print("现执行-失败-用例，第{}次工作组编号查询，查询编号是{}".format(num + 1, workGroupId))
            js = self.get_workGroupId_result(workGroupId)
            print("执行失败实例搜索返回：",js)
            self.get_assertion_failure(js)





if __name__ == "__main__":
    unittest.main()


