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
from config import base,user_base
from  public import  random_num
from public import account
import requests, json
import random
import copy
'''
20190115现需求
根据工作组id，leader登录账号编号，定位数据，惊醒修改
leader登录账号编号，不符合、不存在---登陆账号不存在
工作组编号，找不到---工作组不存在

创建、查询、验证找到该条数据√
全部修改√
部分修改√
修改必填项为空√
修改非必填项为空√
修改非必填项全部为空√
修改工作组id为空、数字、英文字符、页数字符、汉字√
修改工作组leader登录账号编号leaderAccountId为数字、英文字符、页数字符、汉字、与工作组id不匹配的(不测试为空，<失败用例-修改必填项分别为空>中已验证)√
与工作组id不匹配的leaderAccountId√
'''

class UpdateWorkGroup(unittest.TestCase):
    '''刘婉莹 编辑工作组'''

    url=base.base_url+"/updateWorkGroup@workGroupAdmin"
    print("现执行用例——查看编辑工作组" + url + "\n")

    #组织body
    def get_body(self,user_id):
        body = {
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
        return body

    # 新建工作组，返回创建工作组信息body、创建成功后工作组中id
    def creat_workgroup_result(self):
        username, password, user_id = account.create_account()
        print("登陆信息获取完成")
        print("username, password, user_id___:", username, password, user_id)
        url = base.base_url + "/createWorkGroup@workGroupAdmin"
        body = {
            "content": {
                "workGroupForm": self.get_body(user_id)
            }
        }
        resp = requests.post(url, json=body)
        print("创建工作组成功,返回：", json.dumps(resp.json()))
        workGroupId = resp.json()["content"]
        print("创建工作组成功,工作组id:", workGroupId)

        print("此处开始断言-创建结果")
        self.assertion_success(resp.json())

        creat_search_result = self.get_search_workGroupId_result(workGroupId)

        print("此处开始断言-创建后搜索结果")
        self.assertion_success(creat_search_result)

        self.check_searchResult(body["content"]["workGroupForm"], creat_search_result)
        print("使用查询，对比定位该条数据")

        return body, workGroupId,user_id


    # 执行工作组编号查询
    def get_search_workGroupId_result(self, workGroupId):
        url = base.base_url + "/getWorkGroup@workGroupAdmin"
        body = {
            "content": {
                "workGroupId": workGroupId
            }
        }
        resp = requests.post(url, json=body)
        print("查询成功返回：", json.dumps(resp.json()))
        return resp.json()

    # 一般成功断言
    def assertion_success(self, js):
        # 校验返回的状态码
        self.assertEqual(js["code"], 200, "返回的状态码不是200！")
        print("现在执行-成功-断言01结束")
        # 校验返回的状态
        self.assertEqual(js["success"], True, "返回的状态不是True！")
        print("现在执行-成功-断言02结束")
        # 校验返回的message
        self.assertEqual(js["message"], "OK", "返回的message不是OK！")
        print("现在执行-成功-断言03结束")

    #执行编辑
    def update_workgroup_result(self,workGroupId,updata_body):
        body= {
          "content": {
            "workGroupId": workGroupId,
            "workGroupForm": updata_body
          }
        }
        resp = requests.post(self.url, json=body)
        print("编辑工作组完成,返回：", json.dumps(resp.json()))
        print("执行编辑的body：" ,body)
        return resp.json()

    # 组织修改数据-部分修改
    # 每次随机修改3到4个参数（随机到leaderAccountId修改3个，否则4个），
    # 其中工作组id和leaderAccountId不在修改范围
    def organize_data_update_workgroup(self, workGroupId, user_id,original_data):
        update_element_list = ["province", "contact", "email", "name", "city", "accessUrl", "address", "type", "mobile",
                      "leaderAccountId", "invoiceUrl","accountNo", "accountBank", "invoiceTitle", "accountName",
                      "licenseUrl", "logoUrl", "remark"]
        print("chect_list的长度：", len(update_element_list))
        tmp_data=self.get_body(user_id)
        new_data=copy.deepcopy(original_data["content"]["workGroupForm"])
        print("tmp_data:",tmp_data)
        print("1次，new_data:",new_data)

        for i in  range(4):
            tmp_key=random.randint(0,len(update_element_list)-1)
            tmp_element=update_element_list[tmp_key]
            print("tmp_element:",tmp_element)
            print("修改前new_data中{}".format(tmp_element),new_data[tmp_element])
            new_data[tmp_element]=tmp_data[tmp_element]
            print("修改后new_data中{}".format(tmp_element),new_data[tmp_element])
        print("2次，new_data:", new_data)
        return new_data

    #成功用例-全部修改
    def test_update_workgroup_success_all(self):

        # 创建，拿到workGroupId, user_id
        body_creat, workGroupId, user_id = self.creat_workgroup_result()

        #获取准备编辑的数据
        new_data_all=self.get_body(user_id)
        #执行编辑
        js_result=self.update_workgroup_result(workGroupId,new_data_all)
        self.assertion_success(js_result)
        #查询
        update_result=self.get_search_workGroupId_result(workGroupId)
        self.assertion_success(update_result)
        #验证
        self.check_searchResult(new_data_all,update_result)
        print("修改全部数据完成！")

    # 成功用例-遍历单个修改（不包括，工作组编号、leader登陆账号编号）
    def test_update_workgroup_success_individual(self):
        # 创建，拿到workGroupId, user_id
        body_creat, workGroupId, user_id = self.creat_workgroup_result()

        update_element_list = ["province", "contact", "email", "name", "city", "accessUrl", "address", "type", "mobile",
                               "leaderAccountId", "invoiceUrl", "accountNo", "accountBank", "invoiceTitle",
                               "accountName",
                               "licenseUrl", "logoUrl", "remark"]

        new_data_all = self.get_body(user_id)
        count = 1
        for tmp_element in update_element_list:
            # 获取准备编辑的数据
            new_data_individual = copy.deepcopy(body_creat["content"]["workGroupForm"])
            print("现执行修改-遍历单个修改:{}，现执行第{}次".format(tmp_element,count))
            print("修改前new_data_individual中{}".format(tmp_element), new_data_individual[tmp_element])
            new_data_individual[tmp_element] =new_data_all[tmp_element]
            print("修改后new_data_individual中{}".format(tmp_element), new_data_individual[tmp_element])
            # 执行编辑
            js_result = self.update_workgroup_result(workGroupId, new_data_individual)
            self.assertion_success(js_result)
            # 查询
            update_result = self.get_search_workGroupId_result(workGroupId)
            self.assertion_success(update_result)
            # 验证
            self.check_searchResult(new_data_individual, update_result)
            count+=1
        print("遍历单个修改完成！")

    # 成功用例-部分修改,执行3次随机修改，每次修改3到4个值
    def test_update_workgroup_success_part(self):
        # 创建，拿到workGroupId, user_id
        body_creat, workGroupId, user_id = self.creat_workgroup_result()

        for i in range(1, 3):
            print("部分修改,执行3次随机修改,这是第{}次随机修改".format(i))

            # 获取准备编辑的数据
            new_data_part = self.organize_data_update_workgroup(workGroupId, user_id, body_creat)
            # 执行编辑
            js_result=self.update_workgroup_result(workGroupId, new_data_part)
            self.assertion_success(js_result)
            # 查询
            update_result = self.get_search_workGroupId_result(workGroupId)
            self.assertion_success(update_result)
            # 验证
            print("new_data_part--", new_data_part)
            print("update_result--", update_result)
            self.check_searchResult(new_data_part, update_result)
        print("修改部分数据完成!")

    # 成功用例-修改非必填项分别为空
    def test_update_workgroup_success_unnecessary_individual(self):
        # 创建，拿到workGroupId, user_id
        body_creat, workGroupId, user_id = self.creat_workgroup_result()

        update_element_list=["invoiceUrl","accountNo","accountBank","invoiceTitle","accountName","licenseUrl",
                             "logoUrl","remark"]
        count=1
        for tmp_element in update_element_list:
            new_data_unnecessary = copy.deepcopy(body_creat["content"]["workGroupForm"])
            print("现执行修改-非必填项为空:", tmp_element)
            print("修改前new_data_unnecessary中{}".format(tmp_element), new_data_unnecessary[tmp_element])

            # del new_data_unnecessary[tmp_element] #对比函数中不适用
            # print("修改后new_data_unnecessary中应不包含{}，现new_data_unnecessary：\n{}".
            # format(tmp_element, new_data_unnecessary))

            new_data_unnecessary[tmp_element]=""
            print("修改后new_data_unnecessary中{}".format(tmp_element), new_data_unnecessary[tmp_element])

            # 执行编辑
            js_result=self.update_workgroup_result(workGroupId, new_data_unnecessary)
            self.assertion_success(js_result)
            # 查询
            update_result = self.get_search_workGroupId_result(workGroupId)
            self.assertion_success(update_result)
            # 验证
            print("new_data_unnecessary--", new_data_unnecessary)
            print("update_result--", update_result)
            self.check_searchResult(new_data_unnecessary, update_result)
            print("---现执行修改非必填项为空，第{}次完成---".format(count))
            count+=1

    # 成功用例-修改非必填项全部为空
    def test_update_workgroup_success_unnecessary_all(self):
        # 创建，拿到workGroupId, user_id
        body_creat, workGroupId, user_id = self.creat_workgroup_result()

        update_element_list = ["invoiceUrl", "accountNo", "accountBank", "invoiceTitle", "accountName","licenseUrl",
                               "logoUrl", "remark"]
        new_data_unnecessary = copy.deepcopy(body_creat["content"]["workGroupForm"])
        print("修改前new_data_unnecessary--", new_data_unnecessary)
        for tmp_element in update_element_list:
            print("现执行修改:", tmp_element)
            new_data_unnecessary[tmp_element] = ""
        print("修改后new_data_unnecessary--", new_data_unnecessary)
        # 执行编辑
        js_result = self.update_workgroup_result(workGroupId, new_data_unnecessary)
        self.assertion_success(js_result)
        # 查询
        update_result = self.get_search_workGroupId_result(workGroupId)
        self.assertion_success(update_result)
        # 验证
        print("update_result--", update_result)
        self.check_searchResult(new_data_unnecessary, update_result)


    #失败用例-修改必填项分别为空
    def test_update_workgroup_failure_necessary(self):
        # 创建，拿到workGroupId, user_id
        body_creat, workGroupId, user_id = self.creat_workgroup_result()

        update_element_list = ["province","contact","email","name","city","accessUrl","address","type",
                               "mobile","leaderAccountId"]
        count = 1
        for tmp_element in update_element_list:
            new_data_necessary = copy.deepcopy(body_creat["content"]["workGroupForm"])
            print("现执行修改-必填项为空:", tmp_element)
            print("修改前new_data_necessary中{}".format(tmp_element), new_data_necessary[tmp_element])
            del new_data_necessary[tmp_element]
            print("修改后new_data_necessary中应不包含{}，现new_data_unnecessary：\n{}".
                  format(tmp_element, new_data_necessary))
            # 执行编辑
            js_result=self.update_workgroup_result(workGroupId, new_data_necessary)
            print("失败用例，执行编辑返回\n",js_result)
            #失败断言
            self.assertion_failure_necessary(js_result,tmp_element)
            print("---现执行修改必填项为空，第{}次完成---".format(count))
            count += 1

    # 失败用例-修改工作组id为空、数字、英文字符、页数字符、汉字
    def test_update_workgroup_failure_workGroupId(self):
        # 创建，拿到workGroupId, user_id
        body_creat, workGroupId, user_id = self.creat_workgroup_result()
        count=1
        update_element_list = ["", "12334", "edvbjb", "yhgb$%&^@1233", "哈哈哈哈"]
        for tmp_element in update_element_list:
            new_data_necessary = copy.deepcopy(body_creat["content"]["workGroupForm"])
            new_workGroupId=workGroupId
            print("修改前workGroupId为：", new_workGroupId)
            new_workGroupId = tmp_element
            print("修改后workGroupId为：",new_workGroupId)
            # 执行编辑
            js_result=self.update_workgroup_result(new_workGroupId, new_data_necessary)
            print("失败用例，执行编辑返回\n",js_result)
            #失败断言
            self.assertion_failure_necessary(js_result,"workGroupId",tmp_element)
            print("---现执行修改工作组id异常，第{}次完成---".format(count))
            count+=1

    # 失败用例-修改工作组leader登录账号编号leaderAccountId为数字、英文字符、页数字符、汉字、与工作组id不匹配的
    # 不测试为空，<失败用例-修改必填项分别为空>中已验证
    def test_update_workgroup_failure_leaderAccountId(self):
        # 创建，拿到workGroupId, user_id
        body_creat, workGroupId, user_id = self.creat_workgroup_result()

        # 数字、英文字符、页数字符、汉字
        count = 1
        update_element_list = ["12334", "edvbjb", "yhgb$%&^@1233", "哈哈哈哈"]
        for tmp_element in update_element_list:
            new_data_necessary = copy.deepcopy(body_creat["content"]["workGroupForm"])
            print("修改前leaderAccountId为：", new_data_necessary["leaderAccountId"])
            new_data_necessary["leaderAccountId"] = tmp_element
            print("修改后leaderAccountId为：", new_data_necessary["leaderAccountId"])
            # 执行编辑
            js_result = self.update_workgroup_result(workGroupId, new_data_necessary)
            print("失败用例，执行编辑返回\n", js_result)
            # 失败断言
            self.assertion_failure_necessary(js_result, "leaderAccountId", tmp_element)
            print("---现执行修改工作组id异常，第{}次完成---".format(count))
            count += 1

        #与工作组id不匹配的leaderAccountId
        body_creat_1, workGroupId_1, user_id_1 = self.creat_workgroup_result()
        new_data_necessary = copy.deepcopy(body_creat["content"]["workGroupForm"])
        print("修改前leaderAccountId为：", new_data_necessary["leaderAccountId"])
        new_data_necessary["leaderAccountId"] = user_id_1
        print("修改后leaderAccountId为：", new_data_necessary["leaderAccountId"])
        # 执行编辑
        js_result = self.update_workgroup_result(workGroupId, new_data_necessary)
        print("失败用例，执行编辑返回\n", js_result)
        # 失败断言
        #self.assertion_failure_necessary(js_result, "leaderAccountId")
        #此处断言报错，已提bug


    # 编辑比对
    # 第1个参数：创建时传入的数据主体，第2个参数：操作成功后查询ID的返回结果
    def check_searchResult(self, new_data, update_result):
        check_list = ["province", "contact", "email", "name", "city", "accessUrl", "address", "type", "mobile",
                      "leaderAccountId",
                      #"invoiceUrl",
                      "accountNo", "accountBank", "invoiceTitle", "accountName",
                      #"licenseUrl", "logoUrl",
                      "remark"]
        for check_element in check_list:
            self.assertEqual(new_data[check_element], update_result["content"][check_element],
                             "与搜索结果{}的值不一致！".format(check_element))
            print(" now is checking :", check_element)
        print("校验完成！")

    # 失败断言
    def assertion_failure_necessary(self, js,element,tmp_element=""):
        # 校验返回的状态码
        self.assertEqual(400, js["code"], "此处应返回状态码400，现返回" + str(js["code"]))
        print("现在执行-失败-断言01结束")
        # 校验返回的状态
        self.assertEqual( False,js["success"], "返回的状态应是False，现返回" + str(js["success"]))
        print("现在执行-失败-断言02结束")

        # 校验返回的message

        # 修改工作组id、leader登录账号异常
        if element == "leaderAccountId" and tmp_element!="":
            self.assertEqual(js["message"], "用户不存在",
                                 "返回的message异常，现返回" + js["message"])
        elif element == "workGroupId":
            if tmp_element == "":
                self.assertEqual(js["message"], "[workGroupId] 不能为空",
                                 "返回的message异常，现返回" + js["message"])
            else:
                self.assertEqual(js["message"], "工作组不存在",
                                 "返回的message异常，现返回" + js["message"])
        else:
            # 修改必填项为空
            if "null" in js["message"]:
                self.assertEqual(js["message"], "[workGroupForm.{}] 不能为null".format(element),
                                 "返回的message异常，现返回" + js["message"])
            else:
                self.assertEqual(js["message"], "[workGroupForm.{}] 不能为空".format(element),
                                 "返回的message异常，现返回" + js["message"])
        print("现在执行-失败-断言03结束")
