#coding=utf-8
import unittest
import os
import sys
base_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#获取当前项目路径并添加到path中
sys.path.append(base_path)
from config import base, user_base
from public import  random_num
from public import account,workgroup
import requests, json

class CreatWorkGroup(unittest.TestCase):
    '''新建工作组'''

    def test_creat_workgroup_must(self):
        '''新建工作组，只输入必填项内容'''
        username, password, user_id = account.create_account()
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
        # print(body)
        # print(user_id)
        resp = requests.post(url, json=body)
        js = resp.json()
        # print(js)
        print(json.dumps(js))
        workgroup_id = js["content"]
        print(workgroup_id)
        workgroup1 = workgroup.test_search_workgroup_by_workgroupid(workgroup_id)
        body_group = body["content"]["workGroupForm"]
        print(json.dumps(workgroup1))
        for k, v in body_group.items():
            for k1, v1 in workgroup1.items():
                if k == k1:
                    print(v, v1)
                    self.assertEqual(v, v1, "创建信息与查询结果不一致")

    def test_creat_workgroup_must(self):
        '''新建工作组，只输入必填项内容-创建外部工作组类型'''
        username, password, user_id = account.create_account()
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
                    "type": user_base.WorkGroupType_External,
                    "mobile": random_num.randomString(),
                    "leaderAccountId": user_id
                }
            }
        }
        # print(body)
        # print(user_id)
        resp = requests.post(url, json=body)
        js = resp.json()
        # print(js)
        print(json.dumps(js))
        workgroup_id = js["content"]
        print(workgroup_id)
        workgroup1 = workgroup.test_search_workgroup_by_workgroupid(workgroup_id)
        body_group = body["content"]["workGroupForm"]
        print(json.dumps(workgroup1))
        for k, v in body_group.items():
            for k1, v1 in workgroup1.items():
                if k == k1:
                    print(v, v1)
                    self.assertEqual(v, v1, "创建信息与查询结果不一致")

    def test_creat_workgroup_all(self):
        '''新建工作组，输入所有字段内容'''
        username, password, user_id = account.create_account()
        url =base.base_url + "/createWorkGroup@workGroupAdmin"
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
        js = resp.json()
        print(json.dumps(js))
        workgroup_id = js["content"]
        print(workgroup_id)
        workgroup1 =  workgroup.test_search_workgroup_by_workgroupid(workgroup_id)
        # print(json.dumps(workgroup1))
        body_workgroup = body["content"]["workGroupForm"]
        # print(json.dumps(body_workgroup))
        for k, v in body_workgroup.items():
            for k1, v1 in workgroup1.items():
                if k == k1:
                    print(v, v1)
                    self.assertEqual(v, v1, "创建工作组信息不一致")

    def test_cteat_workgroup_leaderAccountId_repeat(self):
        '''新建工作组，必填项字段leader登录账号编号输入已关联其它工作组的编号'''
        username, password, user_id = account.create_account()
        workgroup_id = workgroup.test_add_work_group(user_id)
        url = base.base_url + "/createWorkGroup@workGroupAdmin"
        body = {
            "content": {
                "workGroupForm": {
                    "province": "31",
                    # 31为上海市id
                    "contact": random_num.randomContacter(),
                    "email": random_num.randomEmail(),
                    "name": random_num.randomWorkGroupName(),
                    "city": "3101",
                    # 3101为上海市的区域id
                    "accessUrl": random_num.randomAccessUrl(),
                    "address": random_num.randomAddress(),
                    "type": user_base.WorkGroupType_Internal,
                    "mobile": random_num.randomPhone(),
                    "leaderAccountId": user_id
                }
            }
        }
        resp = requests.post(url, json=body)
        js = resp.json()
        print(json.dumps(js))
        self.assertEqual(js["success"], False, "创建工作组，必填项leaderAccountId字段输入已关联其它工作组的编号，响应代号不一致")
        self.assertEqual(js["code"], 400, "创建工作组时，必填项leaderAccountId字段输入已关联其它工作组的编号，执行结果不一致")
        # self.assertEqual(js["content"]["message"], "有用户已经加入了工作组", "创建工作组时，必填项leaderAccountId字段输入已关联其它工作组的编号，提示信息不一致")

    def test_cteat_workgroup_no_all(self):
        '''新建工作组，不传任何参数'''
        url = base.base_url + "/createWorkGroup@workGroupAdmin"
        body = {
           "content": {
               "workGroupForm": {
               }
           }
        }
        resp = requests.post(url, json=body)
        js = resp.json()
        print(json.dumps(js))
        self.assertEqual(js["success"], False, "创建工作组，不传任何参数时，响应代号不一致")
        self.assertEqual(js["code"], 400, "创建工作组时，不传任何参数时，执行结果不一致")
        self.assertTrue("Error" in js["errorCode"])

    def test_creat_workgroup_must_onlyone_no(self):
        '''创建工作组，必填项某一个参数不传'''
        username, password, user_id = account.create_account()
        url = base.base_url + "/createWorkGroup@workGroupAdmin"
        list = {
            "province": "31",
            "contact": "工作组联系人XXX1",
            "email": "zytest@jiagouyun.cn",
            "name": "工作组名称",
            "city": "3101",
            "accessUrl": "123",
            "address": "科苑路399号",
            "type": user_base.WorkGroupType_Internal,
            "mobile": "182",
            "leaderAccountId": user_id,
            "invoiceUrl": "123456",
            "accountNo": "622112341234",
            "accountBank": "招商银行",
            "invoiceTitle": "驻云测试公司",
            "accountName": "驻云测试",
            "licenseUrl": "1234",
            "logoUrl": "12345",
            "remark": "备注20190113",
        }
        for kl, vl in list.items():
            if kl in ["province", "contact", "email", "name", "city", "accessUrl", "address", "type", "mobile", "leaderAccountId"]:
                print("参数",kl)
                listnew = list.copy()
                del listnew[kl]
                # print(listnew)
                body = {
                    "content": {
                        "workGroupForm": listnew
                    }
                }
                resp = requests.post(url, json=body)
                js = resp.json()
                print(json.dumps(js))
                self.assertEqual(js["success"], False, "新建工作组时，参数" + kl + "不传时，响应代号不一致")
                self.assertEqual(js["code"], 400, "新建工作组时，参数" + kl + "不传时，执行结果不一致")
                self.assertTrue("Error" in js["errorCode"])
                if kl != "type":
                    self.assertEqual(js["message"], "[workGroupForm." + kl + "] 不能为空", "创建工作组时,必填项" + kl + "字段不传，提示信息不一致")
                else:
                    self.assertEqual(js["message"], "[workGroupForm." + kl + "] 不能为null",
                                     "创建工作组时,必填项" + kl + "字段不传，提示信息不一致")

    def test_cteat_workgroup_value_is_various(self):
        '''新建工作组，所有字段填写字符串、int、blooe不同类型的值'''
        username, password, user_id = account.create_account()
        url = base.base_url + "/createWorkGroup@workGroupAdmin"
        types = {
            "布尔类型": True,
            "数字": 1,
            "字符串类型": "test"
        }
        list = {
                    "province": "31",
                    "contact": "工作组联系人XXX",
                    "email": "zytest@jiagouyun.cn",
                    "name": "工作组名称",
                    "city": "3101",
                    "accessUrl": "123",
                    "address": "科苑路399号",
                    "type": user_base.WorkGroupType_Internal,
                    "mobile": "182",
                    "leaderAccountId": user_id,
                    "invoiceUrl": "123456",
                    "accountNo": "622112341234",
                    "accountBank": "招商银行",
                    "invoiceTitle": "驻云测试公司",
                    "accountName": "驻云测试",
                    "licenseUrl": "1234",
                    "logoUrl": "12345",
                    "remark": "备注20190113"
                }
        for kl, vl in list.items():
            if kl not in ['type', 'leaderAccountId']:
                print("参数", kl)
                for kt, vt in types.items():
                    username, password, user_id = account.create_account()
                    listnew = list.copy()
                    listnew["leaderAccountId"] = user_id
                    print("类型", kt)
                    listnew[kl] = vt
                    print(listnew)
                    body = {
                        "content": {
                            "workGroupForm": listnew
                        }
                    }

                    resp = requests.post(url, json=body)
                    js = resp.json()
                    # print(js)
                    print(json.dumps(js))
                    self.assertEqual(js["success"], True, "新建工作组，字段" + kl + "与填写类型为" + kt + "时，响应代号不一致")
                    self.assertEqual(js["code"], 200, "新建工作组，字段" + kl + "与填写类型为" + kt + "时，执行结果不一致")
                    workgroup_id = js["content"]
                    print(workgroup_id)
                    workgroup1 = workgroup.test_search_workgroup_by_workgroupid(workgroup_id)
                    print(json.dumps(workgroup1))
                    for bk, bv in listnew.items():
                        if bk in (workgroup1):      #判断输入的参数是否在返回的结果中
                            wv = workgroup1[bk]   #返回的结果中去获取同输入的参数相等的参数的值
                            if bv == True:
                                bv = str(bv).lower()  #将输入的布尔型值转换成小写的字符串
                                print(bv, wv)
                            self.assertEqual(bv,wv, "创建信息与查询结果不一致")

if __name__ == "__main__":
        unittest.main()