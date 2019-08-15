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
20190114现需求
进入列表，录入工作组编号，执行解散
值workGroupId为必填项
且无论输入任何内容，接口都返回200

添加工作组--搜索比对结果，验证工作组存在--执行解散--搜索验证工作组不存在、原成员无工作组

验证未通过处在188行、250行
'''

class DissolveWorkGroup(unittest.TestCase):
    '''刘婉莹  解散工作组'''
    url = base.base_url + "/dissolveWorkGroup@workGroupAdmin"
    print("现执行用例——解散工作组" + url + "\n")

    #新建工作组，返回创建工作组信息body、创建成功后工作组中id
    def creat_workgroup_result(self):
        username, password, user_id = account.create_account()
        print("user_id",user_id)

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
                    "leaderAccountId": user_id
                }
            }
        }
        resp = requests.post(url, json=body)
        workGroupId = resp.json()["content"]
        self.assertion_success(resp.json())
        print("创建工作组成功,工作组id:",workGroupId)
        print("创建工作组成功,返回：",json.dumps(resp.json()))
        return body, workGroupId

    # 给工作组添加成员
    def addmember_result(self,workGroupId):
        username_01, password_01, user_id_01 = account.create_account()
        username_02, password_02, user_id_02 = account.create_account()
        url= base.base_url + "/addMembers@workGroupMemberAdmin"
        body={
            "content": {
                "memberAccountIds": [
                    user_id_01,
                    user_id_02
                ],
                "workGroupId": workGroupId
            }
        }
        resp=requests.post(url, json=body)
        self.assertion_success(resp.json())
        print("工作组添加成员完成，成员id:",user_id_01,user_id_02)
        print("工作组添加成员成功，返回:",json.dumps(resp.json()))
        return resp.json()

    # 查询工作组详情
    def get_search_workGroupId_result(self, workGroupId):

        url=base.base_url+"/getWorkGroup@workGroupAdmin"
        body = {
            "content": {
                "workGroupId": workGroupId
            }
        }
        resp = requests.post(url, json=body)
        print("查询工作组详情，返回：", json.dumps(resp.json()))
        # self.assertion_success(resp.json())
        return resp.json()

    # 查询工作组成员列表
    def get_listWorkGroupMembers_result(self,workGroupId):

        url = base.base_url + "/listWorkGroupMembers@workGroupMemberAdmin"
        body = {
            "content": {
                "queryForm": {
                    "workGroupId": workGroupId
                }
            }
        }
        resp = requests.post(url, json=body)
        print("查询工作组成员列表，返回：", json.dumps(resp.json()))
        # self.assertion_success(resp.json())
        # self.assertEqual(3, resp.json()["content"]["totalElements"], "返回的成员数量不是3！")

        return resp.json()

    # 成功断言
    def assertion_success(self, js):
        # 校验返回的状态码
        self.assertEqual(200,js["code"], "返回的状态码不是200！")
        print("现在执行-成功-断言01结束")
        # 校验返回的状态
        self.assertEqual(True,js["success"],  "返回的状态不是True！")
        print("现在执行-成功-断言02结束")
        # 校验返回的message
        self.assertEqual("OK",js["message"], "返回的message不是OK！")
        print("现在执行-成功-断言03结束")

    # 搜索失败断言
    def search_workGroupId_assertion_failure(self, js):
        # 校验返回的状态码
        self.assertEqual(js["code"], 400, "尝试搜索已删除工作组Id，此处应返回状态码400，现返回：" + str(js["code"]))
        print("现在执行-搜索失败-断言01结束")
        # 校验返回的状态
        self.assertEqual(js["success"], False, "尝试搜索已删除工作组Id，返回的状态应是False，现返回：" + str(js["success"]))
        print("现在执行-搜索失败-断言02结束")
        # 校验返回的message
        self.assertEqual(js["message"], "工作组不存在",
                         "尝试搜索已删除工作组Id,返回的message应是 工作组不存在 ，现返回：" + js["message"])
        print("现在执行-搜索失败-断言03结束")


    # 新建工作组，查询id，比对结果，返回工作组id
    # 确认这个工作组id确实是我所创建的工作组id，即将要删除的工作组确实存在
    def creatAndSearch_workGroupId(self):
        js_01,workGroupId_02=self.creat_workgroup_result()
        print("拿到创建工作组的工作组id：",workGroupId_02)
        print("拿到创建工作组的信息body：",js_01)
        js_02=self.get_search_workGroupId_result(workGroupId_02)
        print("搜索创建的工作组的id，返回结果：",js_02)
        print("此处开始断言-")
        self.assertion_success(js_02)
        print("此处开始断言-比较创建数据和查询结果")
        check_list =["province","contact","email","name","city","accessUrl","address","type","mobile","leaderAccountId"]
        for check_element in check_list:
            self.assertEqual(js_01["content"]["workGroupForm"][check_element], js_02["content"][check_element],
                             "校验创建与搜索结果{}不一致！".format(check_element))
            print(" now is checking :",check_element)
        print("校验完成，创建工作组成功！")
        print("workGroupId_02：",workGroupId_02)
        return workGroupId_02

    #解散工作组成功用例-工作组中添加2个成员，共3个
    def test_dissolve_workGroup_success(self):

        #创建工作组拿到Id、校验工作组存在
        workGroupId=self.creatAndSearch_workGroupId()
        #添加2个成员
        js_addmember=self.addmember_result(workGroupId)
        self.assertion_success(js_addmember)
        #查询工作组成员列表，验证成员，查看成员
        js_search_list=self.get_listWorkGroupMembers_result(workGroupId)

        list_member=[]
        for i in js_search_list["content"]["elements"]:
            list_member.append(i["id"])
        print("工作组成员id:",list_member)
        self.assertion_success(js_search_list)
        self.assertEqual(3, js_search_list["content"]["totalElements"], "返回的成员数量不是3！")
        #执行解散工作组
        js_dissolve=self.dissolve_workGroup_result(workGroupId)
        self.assertion_success(js_dissolve)

        # 尝试搜索，验证结果

        #1.查询工作组详情
        js_search=self.get_search_workGroupId_result(workGroupId)
        self.search_workGroupId_assertion_failure(js_search)
        #2.查看原成员账号详情
        #此处应验证（0，3），0位置，验证未通过,已提交BUG，验证通过
        list_length=len(js_search_list["content"]["elements"])
        for member in range(0,3):
            print("共3个成员，现验证第{}个:{}".format(member+1,list_member[member]))
            resp_account=self.getAccount_result(list_member[member])
            self.assertion_success(resp_account)
            self.assertEqual(None,resp_account["content"]["workGroupId"],
                             "验证解散后原成员账号,工作组id应是NULL，现显示：{}！".format(resp_account["content"]["workGroupId"]))
            print("现验证查询账号详情，工作组id显示null完成！")



    #执行解散工作组
    def dissolve_workGroup_result(self,workGroupId):
        body = {
            "content": {
                "workGroupId": workGroupId
            }
        }
        resp = requests.post(self.url, json=body)
        print("执行解散，返回：", json.dumps(resp.json()))
        return resp.json()
    #查看账号详情
    def getAccount_result(self,accountId):
        url = base.base_url + "/getAccount@accountAdmin"
        body = {
            "content": {
                "accountId": accountId
            }
        }
        resp = requests.post(url, json=body)
        print("执行解散，返回：", json.dumps(resp.json()))
        return resp.json()

    #解散工作组成功用例-工作组中未添加成员，仅创建者
    def test_dissolve_workGroup_oneMember_success(self):

        #创建工作组拿到Id、校验工作组存在
        workGroupId=self.creatAndSearch_workGroupId()

        # 查询工作组成员列表，验证成员，查看成员
        js_search_list = self.get_listWorkGroupMembers_result(workGroupId)
        member=js_search_list["content"]["elements"][0]["id"]
        print("工作组成员id:", member)
        self.assertion_success(js_search_list)
        self.assertEqual(1, js_search_list["content"]["totalElements"], "返回的成员数量不是1！")
        # 执行解散工作组
        js_dissolve = self.dissolve_workGroup_result(workGroupId)
        self.assertion_success(js_dissolve)

        # 尝试搜索，验证结果

        # 1.查询工作组详情
        js_search = self.get_search_workGroupId_result(workGroupId)
        self.search_workGroupId_assertion_failure(js_search)
        # 2.查看原成员账号详情
        # 此处，验证未通过，解散后创建工作组的用户，查询返回异常，验证通过
        resp_account = self.getAccount_result(member)
        self.assertion_success(resp_account)
        self.assertEqual(None, resp_account["content"]["workGroupId"],
                         "验证解散后原成员账号,工作组id应是NULL，现显示：{}！".format(resp_account["content"]["workGroupId"]))
        print("现验证查询账号详情，工作组id显示null完成！")

