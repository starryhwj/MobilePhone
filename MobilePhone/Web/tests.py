from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth import login, authenticate
from .views import *
from .models import *
from Users.models import User
from django.db import connection
import os
import json
import datetime
from django.contrib.auth.hashers import check_password, make_password


class SuperUserUnitTest(TestCase):

    # begin 初始化测试数据
    @classmethod
    def setUpTestData(cls):
        # 所有test运行前运行一次
        cls.init_store_procedure()
        cls.client = Client()
        cls.datatable_param = {
            'pagination[page]': 1,
            'pagination[pages]': 10,
            'pagination[perpage]': 10,
        }
        cls.sessionKey = '70002101725758f9633c6a482fdc6fc117b86195c32805ab8757fe67da7d96bb7cc79d01005663771' 

        # begin User 测试用例
        cls.super_user_username = 'admin'
        cls.super_user_password = '123456'
        cls.super_user = User.objects.create_superuser(username=cls.super_user_username, email='', password=cls.super_user_password)
        cls.super_user.is_pass = True
        cls.super_user.is_superuser = True
        cls.super_user.save()

        cls.blevel_user_username = 'bLevel'
        cls.blevel_user_password = '123456'
        cls.blevel_user = User.objects.create_user(username=cls.blevel_user_username, email='', password=cls.blevel_user_password)
        cls.blevel_user.leader = cls.super_user
        cls.blevel_user.usersystem = cls.super_user
        cls.blevel_user.money = 1
        cls.blevel_user.save()

        cls.alevel_user_username = 'aLevel'
        cls.alevel_user_password = '123456'
        cls.alevel_user = User.objects.create_user(username=cls.alevel_user_username, email='', password=cls.alevel_user_password)
        cls.alevel_user.phone = '123456789'
        cls.alevel_user.leader = cls.blevel_user
        cls.alevel_user.usersystem = cls.super_user
        cls.alevel_user.true_name = 'aLevelTrueName'
        cls.alevel_user.save()

        cls.lastlevel_user_username = 'lastLevel'
        cls.lastlevel_user_password = '123456'
        cls.lastlevel_user = User.objects.create_user(username=cls.lastlevel_user_username, email='', password=cls.lastlevel_user_password)
        cls.lastlevel_user.leader = cls.alevel_user
        cls.lastlevel_user.usersystem = cls.super_user
        cls.lastlevel_user.save()
        # end User 测试用例

        # begin TaoBaoSession 测试用例
        TaoBaoSession.objects.create(Owner=cls.super_user, SessionKey=cls.sessionKey, Ext_Date=datetime.datetime.now(), Ext_Time=1000000)
        # end TaoBaoSession 测试用例       

        # begin SystemConfig 测试用例
        SystemConfig.objects.create(Name='心跳存活判断秒数', Value=300)
        SystemConfig.objects.create(Name='刷粉人数上限默认值', Value=100)
        SystemConfig.objects.create(Name='关注人数上限默认值', Value=100)     
        SystemConfig.objects.create(Name='刷粉点赞与评论间隔人数', Value=5)                       
        # end SystemConfig 测试用例

        # begin MaintenanceNumberMissionKeywordClassification 测试用例
        cls.tag = MaintenanceNumberMissionKeywordClassification.objects.create(Name='标签1', Owner=cls.super_user)
        MaintenanceNumberMissionKeywordClassification.objects.create(Name='标签2', Owner=cls.super_user)
        # begin MaintenanceNumberMissionKeywordClassification 测试用例    
         
        # begin TikTokAccountGroup 测试用例
        group = TikTokAccountGroup.objects.create(Name='账号分组1', Owner=cls.super_user)
        TikTokAccountGroup.objects.create(Name='账号分组2', Owner=cls.super_user)
        # end TikTokAccountGroup 测试用例

        # begin Agent 测试用例
        cls.blevel_agent = Agent.objects.create(Subscriber=cls.blevel_user, UserSystem=cls.super_user)
        cls.alevel_agent = Agent.objects.create(Subscriber=cls.alevel_user, UserSystem=cls.super_user, UserALevel=cls.blevel_user)
        Agent.objects.create(Subscriber=cls.lastlevel_user, UserSystem=cls.super_user, UserALevel=cls.alevel_user, UserBLevel=cls.blevel_user)
        # end Agent 测试用例

        # begin TikTokAccount 测试用例
        cls.no_showWindowExists_TikTokAccount = TikTokAccount.objects.create(NickName='noShowWindowExists', Group=group, Remark='hasTag', NewDescribe='NewDescribe', Owner=cls.super_user)
        cls.no_showWindowExists_TikTokAccount.Classification.add(cls.tag)
        cls.has_showWindowExists_TikTokAccount = TikTokAccount.objects.create(NickName='hasShowWindowExists', ShowWindowExists=True, Owner=cls.super_user)        
        cls.heartbeat_TikTokAccount = TikTokAccount.objects.create(NickName='heartbeat', Owner=cls.super_user)             
        # end TikTokAccount 测试用例

        # begin ALIConfig 测试用例
        aliconfig1 = ALIConfig.objects.create(NickName='PID1', PID='mm_33692955_1064550345_109727950251', LASTPID='109727950251', Owner=cls.super_user)
        aliconfig2 = ALIConfig.objects.create(NickName='PID2', PID='mm_33692955_1064550345_109843650472', LASTPID='109843650472', Owner=cls.super_user)        
        # end ALIConfig 测试用例

        # begin MissionPlanTemplate 测试用例
        cls.missionplantemplate = MissionPlanTemplate.objects.create(Name='测试模板1', Owner=cls.super_user, RecordDate=datetime.datetime.now())
        # end MissionPlanTemplate 测试用例

        # begin MobilePhone测试用例
        cls.mobilephone = MobilePhone.objects.create(IMEI='noAgentnoCommodity', SysID='noAgentnoCommodity', Remark='noAgentnoCommodity', 
                                                     Enable=True, HeartBeat=datetime.datetime.now(), ALIConfig=aliconfig1, MissionPlanTemplate=cls.missionplantemplate, Owner=cls.super_user)
        MobilePhone.objects.create(IMEI='bLevel', SysID='bLevel', Agent=cls.blevel_agent, TikTokAccount=cls.no_showWindowExists_TikTokAccount, Remark='oldremark', ALIConfig=aliconfig2, Owner=cls.super_user)
        MobilePhone.objects.create(IMEI='hasCommodity', SysID='hasCommodity', TikTokAccount=cls.has_showWindowExists_TikTokAccount, Owner=cls.super_user)   
        MobilePhone.objects.create(IMEI='sameAgent', SysID='sameAgent', Agent=cls.blevel_agent, TikTokAccount=cls.heartbeat_TikTokAccount, HeartBeat=datetime.datetime.now(), Owner=cls.super_user)             
        # end MobilePhone测试用例

        # begin GoodClassification 测试用例
        goodclassification = GoodClassification.objects.create(Name='商品分类1', Owner=cls.super_user)
        # end GoodClassification 测试用例

        # begin Goods 测试用例
        goods = Goods.objects.create(Title='商品1', OutSidePlatformID='528731068410', SubTitle='商品1', Owner=cls.super_user)
        goods.GoodClassifications.add(goodclassification)
        goods2 = Goods.objects.create(Title='商品2', OutSidePlatformID='575598741328', SubTitle='商品2', Owner=cls.super_user)        
        # end Goods 测试用例    
         
        # begin VideoClassifications 测试用例  
        cls.videoclassification = VideoClassification.objects.create(Name='视频分类1', Owner=cls.super_user)    
        # end VideoClassifications 测试用例      
         
        # begin Videos 测试用例
        cls.video1 = Videos.objects.create(Owner=cls.super_user, Goods=goods, Title='hasgoods', VideoKeyword='keyword1')
        cls.video1.VideoClassifications.add(cls.videoclassification)
        cls.video2 = Videos.objects.create(Owner=cls.super_user, Title='nogoods', VideoKeyword='keyword2')      
        cls.video3 = Videos.objects.create(Owner=cls.super_user, Title='nogoods', VideoKeyword='keyword3')  
        cls.video4 = Videos.objects.create(Owner=cls.super_user, Title='nogoods', VideoKeyword='keyword4')                    
        # end Videos 测试用例  

        # begin VideoMission 测试用例
        VideoMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, Video=cls.video1, 
                                    Status=0, StartTime=datetime.datetime.now(), VideoTitle='video1', GoodTitle='商品1')
        VideoMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, Video=cls.video2, Status=1, StartTime=datetime.datetime.now(), VideoKeyword='keyword2')
        VideoMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, Video=cls.video3, Status=2, StartTime=datetime.datetime.now())
        VideoMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, Video=cls.video4, Status=3, StartTime=datetime.datetime.now())        
        # end VideoMission 测试用例

        # begin FollowMission 测试用例
        FollowMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, 
                                    Status=0, StartTime=datetime.datetime.now(), EndTime=datetime.datetime.now())
        FollowMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, Status=1, StartTime=datetime.datetime.now(), EndTime=datetime.datetime.now())
        FollowMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, Status=2, StartTime=datetime.datetime.now(), EndTime=datetime.datetime.now())
        FollowMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, Status=3, StartTime=datetime.datetime.now(), EndTime=datetime.datetime.now())        
        # end FollowMission 测试用例   
        
        # begin MaintenanceNumberMission 测试用例
        MaintenanceNumberMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, 
                                    Status=0, StartTime=datetime.datetime.now(), EndTime=datetime.datetime.now())
        MaintenanceNumberMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, Status=1, StartTime=datetime.datetime.now(), EndTime=datetime.datetime.now())
        MaintenanceNumberMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, Status=2, StartTime=datetime.datetime.now(), EndTime=datetime.datetime.now())
        MaintenanceNumberMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, Status=3, StartTime=datetime.datetime.now(), EndTime=datetime.datetime.now())        
        # end MaintenanceNumberMission 测试用例    

        # begin MaintenanceNumberMissionKeyword 测试用例
        cls.maintenancenumbermissionkeyword = MaintenanceNumberMissionKeyword.objects.create(Name='关键词1', Classification=cls.tag, Owner=cls.super_user)
        MaintenanceNumberMissionKeyword.objects.create(Name='关键词2', Classification=cls.tag, Owner=cls.super_user)
        MaintenanceNumberMissionKeyword.objects.create(Name='关键词3', Owner=cls.super_user)        
        # end MaintenanceNumberMissionKeyword 测试用例  
         
        # begin MutualBrushMission 测试用例
        MutualBrushMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, 
                                    Status=0, StartTime=datetime.datetime.now())
        MutualBrushMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, Status=1, StartTime=datetime.datetime.now())
        MutualBrushMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, Status=2, StartTime=datetime.datetime.now())
        MutualBrushMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, Status=3, StartTime=datetime.datetime.now())   
        # end MutualBrushMission 测试用例      
         
        # begin ScanMission 测试用例
        ScanMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, 
                                    Status=0, StartTime=datetime.datetime.now(), EndTime=datetime.datetime.now())
        ScanMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, Status=1, StartTime=datetime.datetime.now(), EndTime=datetime.datetime.now())
        ScanMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, Status=2, StartTime=datetime.datetime.now(), EndTime=datetime.datetime.now())
        ScanMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, Status=3, StartTime=datetime.datetime.now(), EndTime=datetime.datetime.now())
        # end ScanMission 测试用例 
        
        # begin CommentLibrary 测试用例
        CommentLibrary.objects.create(Text='评论库1', Owner=cls.super_user)
        CommentLibrary.objects.create(Text='评论库2', Owner=cls.super_user)
        # end CommentLibrary 测试用例  

        # begin Order 测试用例
        Order.objects.create(ADZone_ID='109727950251', Goods=goods, ALIConfig=aliconfig1, Trade_Parent_ID='737709442123689270', 
                            Item_Title='商品1', TK_Status=12, TK_Create_Time=datetime.datetime.now())
        Order.objects.create(ADZone_ID='109727950251', Goods=goods2, ALIConfig=aliconfig1, Trade_Parent_ID='578756022363535177', 
                            Item_Title='商品2', TK_Status=3, TK_Create_Time=datetime.datetime.now())
        Order.objects.create(ADZone_ID='109843650472', Goods=goods, ALIConfig=aliconfig2, Trade_Parent_ID='578251093939958373', 
                            Item_Title='商品1', TK_Status=12, TK_Create_Time=(datetime.datetime.now() - datetime.timedelta(days=1)))
        # end Order 测试用例

        # begin AgentApplyForWithdraw 测试用例
        AgentApplyForWithdraw.objects.create(Agent=cls.alevel_agent, ApplyDate=datetime.datetime.now(), Money=1)
        # end AgentApplyForWithdraw 测试用例

        # begin MaintenanceNumberMissionPlan 测试用例
        MaintenanceNumberMissionPlan.objects.create(MissionPlanTemplate=cls.missionplantemplate, StartTime=datetime.datetime.now(), EndTime=datetime.datetime.now(), Title='养号任务')
        # end MaintenanceNumberMissionPlan 测试用例

        # begin ScanMissionPlan 测试用例
        ScanMissionPlan.objects.create(MissionPlanTemplate=cls.missionplantemplate, StartTime=datetime.datetime.now(), EndTime=datetime.datetime.now(), Title='刷粉任务')
        # end ScanMissionPlan 测试用例 

        # begin FollowMissionPlan 测试用例
        FollowMissionPlan.objects.create(MissionPlanTemplate=cls.missionplantemplate, StartTime=datetime.datetime.now(), EndTime=datetime.datetime.now(), Title='关注任务')
        # end FollowMissionPlan 测试用例    

        # begin TreasureMissionPlan 测试用例
        TreasureMissionPlan.objects.create(MissionPlanTemplate=cls.missionplantemplate, StartTime=datetime.datetime.now(), EndTime=datetime.datetime.now(), Title='刷宝任务')
        # end TreasureMissionPlan 测试用例                    

        # begin TreasureMission 测试用例
        TreasureMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, 
                                    Status=0, StartTime=datetime.datetime.now(), EndTime=datetime.datetime.now())
        TreasureMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, Status=1, StartTime=datetime.datetime.now(), EndTime=datetime.datetime.now())
        TreasureMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, Status=2, StartTime=datetime.datetime.now(), EndTime=datetime.datetime.now())
        TreasureMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, Status=3, StartTime=datetime.datetime.now(), EndTime=datetime.datetime.now())
        # end TreasureMission 测试用例 

        # begin WatchLiveMission 测试用例
        WatchLiveMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, 
                                    Status=0, StartTime=datetime.datetime.now(), EndTime=datetime.datetime.now(), CommentText='')
        WatchLiveMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, Status=1, StartTime=datetime.datetime.now(), EndTime=datetime.datetime.now())
        WatchLiveMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, Status=2, StartTime=datetime.datetime.now(), EndTime=datetime.datetime.now())
        WatchLiveMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, Status=3, StartTime=datetime.datetime.now(), EndTime=datetime.datetime.now())
        # end WatchLiveMission 测试用例   

        # begin ChangeSignatureMission 测试用例
        ChangeSignatureMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, 
                                    Status=0, StartTime=datetime.datetime.now(), TikTokAccount=cls.no_showWindowExists_TikTokAccount)
        ChangeSignatureMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, 
                                    Status=1, StartTime=datetime.datetime.now(), TikTokAccount=cls.no_showWindowExists_TikTokAccount)
        ChangeSignatureMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, 
                                    Status=2, StartTime=datetime.datetime.now(), TikTokAccount=cls.no_showWindowExists_TikTokAccount)
        ChangeSignatureMission.objects.create(Owner=cls.super_user, MobilePhone=cls.mobilephone, 
                                    Status=3, StartTime=datetime.datetime.now(), TikTokAccount=cls.no_showWindowExists_TikTokAccount)
        # end ChangeSignatureMission 测试用例   

    def init_store_procedure():
        with open('D:\\Work\MobilePhone\\unittest vanilla data\\CalcAgentIncome.sql', 'r') as file_obj:
            contents = file_obj.read()
            with connection.cursor() as cursor:
                cursor.execute(contents.rstrip())   

        with open('D:\\Work\MobilePhone\\unittest vanilla data\\VAllMissions.sql', 'r') as file_obj:
            contents = file_obj.read()
            with connection.cursor() as cursor:
                cursor.execute(contents.rstrip())                    

        with open('D:\\Work\MobilePhone\\unittest vanilla data\\CalcAgentMissionIncome.sql', 'r') as file_obj:
            contents = file_obj.read()
            with connection.cursor() as cursor:
                cursor.execute(contents.rstrip())   

    # end 初始化测试数据

    # begin 淘宝验证
    def test_taobaoverify(self):
        response = self.client.post(reverse('Web:taobaoverify'))
        self.assertEqual(response.content, b'f00c25378e73a2bbb92a9a1859fb7f05')
    # end 淘宝验证

    # begin 账户总览
    def test_index_superuser(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:index'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/index.html')  # 判断渲染的模板是否正确

    def test_index_agent(self):
        self.client.login(username=self.blevel_user_username, password=self.blevel_user_password)
        response = self.client.post(reverse('Web:index'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/Agent/AgentIndex.html')  # 判断渲染的模板是否正确        
    # end 账户总览

    # begin 设备管理
    def test_devicemanage(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:DeviceManage'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/DeviceManage/DeviceManage.html')  # 判断渲染的模板是否正确

    def test_getdevice_isagent_is_none_and_iscommodity_is_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()           
        response = self.client.post(reverse('Web:GetDevice'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数

    def test_getdevice_isagent_is_not_none_and_iscommodity_is_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()            
        param.update({
            'isagent': 'True'
        })
        response = self.client.post(reverse('Web:GetDevice'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数       

    def test_getdevice_isagent_is_none_and_iscommodity_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()        
        param.update({
            'iscommodity': 'True'
        })
        response = self.client.post(reverse('Web:GetDevice'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数              

    def test_getdevice_generalSearch_and_devicecolumn_is_remark(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalDeviceSearch]': 'Agent',
            'query[devicecolumn]': 'remark'
        })
        response = self.client.post(reverse('Web:GetDevice'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数      

    def test_getdevice_generalSearch_and_devicecolumn_is_tiktok(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalDeviceSearch]': 'has',
            'query[devicecolumn]': 'tiktok'
        })
        response = self.client.post(reverse('Web:GetDevice'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数          

    def test_getdevice_generalSearch_and_devicecolumn_is_agent(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalDeviceSearch]': 'b',
            'query[devicecolumn]': 'agent'
        })
        response = self.client.post(reverse('Web:GetDevice'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数   

    def test_getdevice_generalSearch_and_devicecolumn_is_id_digit(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalDeviceSearch]': '1',
            'query[devicecolumn]': 'id'
        })
        response = self.client.post(reverse('Web:GetDevice'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数     

    def test_getdevice_generalSearch_and_devicecolumn_is_id_str(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalDeviceSearch]': 'a',
            'query[devicecolumn]': 'id'
        })
        response = self.client.post(reverse('Web:GetDevice'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数           

    def test_getdevice_generalSearch_and_devicecolumn_is_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalDeviceSearch]': 'has',
        })
        response = self.client.post(reverse('Web:GetDevice'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数                      
    
    def test_getdevice_status_is_true(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[device_status]': True,
        })
        response = self.client.post(reverse('Web:GetDevice'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数                 

    def test_getdevice_status_is_false(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[device_status]': False,
        })
        response = self.client.post(reverse('Web:GetDevice'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 3) # 判断数据条数    

    def test_getdevice_isonline_is_true(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[isonline]': True,
        })
        response = self.client.post(reverse('Web:GetDevice'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数    

    def test_getdevice_isonline_is_false(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[isonline]': False,
        })
        response = self.client.post(reverse('Web:GetDevice'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数                              
    
    def test_getdevice_tag_is_str(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[tag]': '标签1,',
        })
        response = self.client.post(reverse('Web:GetDevice'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数   

    def test_getdevice_tag_is_none_type(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[tag]': '-1,',
        })
        response = self.client.post(reverse('Web:GetDevice'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 3) # 判断数据条数        

    def test_getdevice_group_is_str(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[group]': '账号分组1,',
        })
        response = self.client.post(reverse('Web:GetDevice'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数   

    def test_getdevice_group_is_none_type(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[group]': '-1,',
        })
        response = self.client.post(reverse('Web:GetDevice'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 3) # 判断数据条数                 
    
    def test_getdevicenamebyids_ids_is_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'ids': '',
        }
        response = self.client.post(reverse('Web:GetDeviceNameByIDs'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['ids']
        self.assertEqual(data_list, '') # 判断数据     

    def test_getdevicenamebyids_ids_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'ids': '1,',
        }
        response = self.client.post(reverse('Web:GetDeviceNameByIDs'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['ids']
        self.assertEqual(data_list, '1') # 判断数据          
    
    def test_getdeviceremark(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'id': 1,
        }
        response = self.client.post(reverse('Web:GetDeviceRemark'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, '1') # 判断数据 
        remark_result = response_json['remark']
        self.assertEqual(remark_result, 'noAgentnoCommodity') # 判断数据         

    def test_editdeviceremark(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        mobile = MobilePhone.objects.get(id=2)
        self.assertEqual(mobile.Remark, 'oldremark') # 判断数据      
        param = {
            'id': 2,
            'remark': 'newremark'
        }
        response = self.client.post(reverse('Web:EditDeviceRemark'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        mobile = MobilePhone.objects.get(id=2)
        self.assertEqual(mobile.Remark, 'newremark') # 判断数据     

    def test_editdeviceenable(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        mobile = MobilePhone.objects.get(id=2)
        self.assertFalse(mobile.Enable) # 判断数据      
        param = {
            'id': 2,
        }
        response = self.client.post(reverse('Web:EditDeviceEnable'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        mobile = MobilePhone.objects.get(id=2)
        self.assertTrue(mobile.Enable) # 判断数据                   
                  
    # end 设备管理

    # begin 账号分组
    def test_accountgroup(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:AccountGroup'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/MyAccount/AccountGroup.html')  # 判断渲染的模板是否正确   

    def test_getaccountgroup(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()           
        response = self.client.post(reverse('Web:GetAccountGroup'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数

    def test_createaccountgroup(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'name': '测试新增'
        }         
        response = self.client.post(reverse('Web:CreateAccountGroup'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        accountgrouplist = TikTokAccountGroup.objects.all()
        self.assertEqual(accountgrouplist.count(), 3) # 判断数据条数

    def test_editaccountgroup(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        TikTokAccountGroup.objects.create(Name='旧数据')
        accountgroup = TikTokAccountGroup.objects.get(Name='旧数据')
        self.assertEqual(accountgroup.Name, '旧数据') # 判断数据          
        param = {
            'id': accountgroup.id,
            'name': '新数据'
        }         
        response = self.client.post(reverse('Web:EditAccountGroup'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        accountgroup = TikTokAccountGroup.objects.get(id=accountgroup.id)
        self.assertEqual(accountgroup.Name, '新数据') # 判断数据条数      

    def test_delete_accountgroup_by_ids(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        TikTokAccountGroup.objects.create(Name='测试删除')
        accountgrouplistbefore = TikTokAccountGroup.objects.all()
        self.assertEqual(accountgrouplistbefore.count(), 3) # 判断数据条数     
        accountgroup = TikTokAccountGroup.objects.get(Name='测试删除')         
        param = {
            'ids': str(accountgroup.id) + ','
        }         
        response = self.client.post(reverse('Web:DeleteAccountGroup'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:AccountGroup'))  # 判断跳转
        accountgrouplist = TikTokAccountGroup.objects.all()
        self.assertEqual(accountgrouplist.count(), 2) # 判断数据条数        
    # end 账号分组

    # begin 账号列表
    def test_accountlist(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:AccountList'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/MyAccount/AccountList.html')  # 判断渲染的模板是否正确       

    def test_getaccount_generalSearch_and_tiktokaccountcolumn_is_nickname(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalAccountSearch]': 'has',
            'query[tiktokaccountcolumn]': 'nickname'
        })
        response = self.client.post(reverse('Web:GetAccount'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数      

    def test_getaccount_generalSearch_and_tiktokaccountcolumn_is_remark(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalAccountSearch]': 'has',
            'query[tiktokaccountcolumn]': 'remark'
        })
        response = self.client.post(reverse('Web:GetAccount'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数     

    def test_getaccount_generalSearch_and_tiktokaccountcolumn_is_mobileid_digit(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalAccountSearch]': '2',
            'query[tiktokaccountcolumn]': 'mobileid'
        })
        response = self.client.post(reverse('Web:GetAccount'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数    

    def test_getaccount_generalSearch_and_tiktokaccountcolumn_is_mobileid_str(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalAccountSearch]': 'a',
            'query[tiktokaccountcolumn]': 'mobileid'
        })
        response = self.client.post(reverse('Web:GetAccount'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 3) # 判断数据条数            

    def test_getaccount_generalSearch_and_tiktokaccountcolumn_is_agentname(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalAccountSearch]': 'bLevel',
            'query[tiktokaccountcolumn]': 'agentname'
        })
        response = self.client.post(reverse('Web:GetAccount'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数          

    def test_getaccount_status_is_true(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[tiktokaccount_status]': True,
        })
        response = self.client.post(reverse('Web:GetAccount'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数                 

    def test_getaccount_status_is_false(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[tiktokaccount_status]': False,
        })
        response = self.client.post(reverse('Web:GetAccount'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数    

    def test_getaccount_showwindowexists_is_true(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[showwindowexists]': True,
        })
        response = self.client.post(reverse('Web:GetAccount'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数                 

    def test_getaccount_showwindowexists_is_false(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[showwindowexists]': False,
        })
        response = self.client.post(reverse('Web:GetAccount'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数    

    def test_getaccount_tag_is_str(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[tag]': '标签1,',
        })
        response = self.client.post(reverse('Web:GetAccount'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数   

    def test_getaccount_tag_is_none_type(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[tag]': '-1,',
        })
        response = self.client.post(reverse('Web:GetAccount'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数        

    def test_getaccount_group_is_str(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[group]': '账号分组1,',
        })
        response = self.client.post(reverse('Web:GetAccount'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数   

    def test_getaccount_group_is_none_type(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[group]': '-1,',
        })
        response = self.client.post(reverse('Web:GetAccount'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数               

    def test_editaccountlist(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'id': 3,
            'groupid': 2,
            'remark': '测试修改',
            'classficationid': '1,2,'
        }
        response = self.client.post(reverse('Web:EditAccountList'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        titokaccount = TikTokAccount.objects.get(id=3)
        self.assertEqual(titokaccount.Group.id, 2) # 判断数据          
        self.assertEqual(titokaccount.Remark, '测试修改') # 判断数据                               
    
    def test_getaccountlistbyid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'id': 1,
        }
        response = self.client.post(reverse('Web:GetAccountListByID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, 1) # 判断数据 
        classificationid_result = response_json['classificationid']
        self.assertEqual(classificationid_result, '1') # 判断数据     
    
    def test_getworks_pic_is_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        with open('D:\\Work\MobilePhone\\unittest vanilla data\\hasgoods.mp4', 'br') as fp:
            res = self.client.post(reverse('Web:UploadMyVideo'), { 'dataid': self.video1.id, 'file': fp })
        video = Videos.objects.get(id=self.video1.id)
        work = Works.objects.create(TikTokAccount=self.no_showWindowExists_TikTokAccount, Video=video, UploadTime=datetime.datetime.now())
        param = self.datatable_param.copy()
        response = self.client.post(reverse('Web:GetWorks'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 0) # 判断数据条数
        video.URL.delete()

    def test_getworks_pic_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        with open('D:\\Work\MobilePhone\\unittest vanilla data\\hasgoods.mp4', 'br') as fp:
            res = self.client.post(reverse('Web:UploadMyVideo'), { 'dataid': self.video1.id, 'file': fp })
        video = Videos.objects.get(id=self.video1.id)
        work = Works.objects.create(TikTokAccount=self.no_showWindowExists_TikTokAccount, Video=video, UploadTime=datetime.datetime.now(), Pic='1')
        param = self.datatable_param.copy()
        response = self.client.post(reverse('Web:GetWorks'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数  
        video.URL.delete()        

    def test_getworks_accountid_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        with open('D:\\Work\MobilePhone\\unittest vanilla data\\hasgoods.mp4', 'br') as fp:
            res = self.client.post(reverse('Web:UploadMyVideo'), { 'dataid': self.video1.id, 'file': fp })
        video = Videos.objects.get(id=self.video1.id)
        work = Works.objects.create(TikTokAccount=self.no_showWindowExists_TikTokAccount, Video=video, UploadTime=datetime.datetime.now(), Pic='1')
        param = self.datatable_param.copy()
        param.update({
            'query[accountid]': '1',
        })
        response = self.client.post(reverse('Web:GetWorks'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数  
        video.URL.delete() 

    def test_getworks_goodid_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        with open('D:\\Work\MobilePhone\\unittest vanilla data\\hasgoods.mp4', 'br') as fp:
            res = self.client.post(reverse('Web:UploadMyVideo'), { 'dataid': self.video1.id, 'file': fp })
        video = Videos.objects.get(id=self.video1.id)
        work = Works.objects.create(TikTokAccount=self.no_showWindowExists_TikTokAccount, Video=video, UploadTime=datetime.datetime.now(), Pic='1')
        param = self.datatable_param.copy()
        param.update({
            'query[goodid]': '1',
        })
        response = self.client.post(reverse('Web:GetWorks'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数     
        video.URL.delete()      
        
    # end 账号列表

    # begin 阿里妈妈配置
    def test_aliconfig(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:ALIConfig'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/CommodityManage/ALIConfig.html')  # 判断渲染的模板是否正确   

    def test_getaliconfig(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()           
        response = self.client.post(reverse('Web:GetALIConfig'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数

    def test_createaliconfig(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'nickname': '测试新增',
            'pid': '1_2_3'
        }         
        response = self.client.post(reverse('Web:CreateALIConfig'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        aliconfiglist = ALIConfig.objects.all()
        self.assertEqual(aliconfiglist.count(), 3) # 判断数据条数

    def test_editaliconfig(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        ALIConfig.objects.create(NickName='旧数据')
        aliconfig = ALIConfig.objects.get(NickName='旧数据')
        self.assertEqual(aliconfig.NickName, '旧数据') # 判断数据          
        param = {
            'id': aliconfig.id,
            'nickname': '新数据',
            'pid': '1_2_3'
        }         
        response = self.client.post(reverse('Web:EditALIConfig'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        aliconfig = ALIConfig.objects.get(id=aliconfig.id)
        self.assertEqual(aliconfig.NickName, '新数据') # 判断数据    
        self.assertEqual(aliconfig.LASTPID, '3') # 判断数据          

    def test_delete_aliconfig_by_ids(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        ALIConfig.objects.create(NickName='测试删除')
        aliconfiglistbefore = ALIConfig.objects.all()
        self.assertEqual(aliconfiglistbefore.count(), 3) # 判断数据条数     
        aliconfig = ALIConfig.objects.get(NickName='测试删除')         
        param = {
            'ids': str(aliconfig.id) + ','
        }         
        response = self.client.post(reverse('Web:DeleteALIConfig'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:ALIConfig'))  # 判断跳转
        aliconfiglist = ALIConfig.objects.all()
        self.assertEqual(aliconfiglist.count(), 2) # 判断数据条数     

    def test_getaliconfigbyid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'id': 1,
        }
        response = self.client.post(reverse('Web:GetALIConfigByID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, 1) # 判断数据 
        nickname_result = response_json['nickname']
        self.assertEqual(nickname_result, 'PID1') # 判断数据              
      
    # end 阿里妈妈配置

    # begin 我的商品
    def test_mycommodity(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:MyCommodity'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/CommodityManage/MyCommodity.html')  # 判断渲染的模板是否正确        
    
    def test_getmycommodity_generalSearch_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalCommoditySearch]': '1',
        })
        response = self.client.post(reverse('Web:GetMyCommodity'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数                 

    def test_getmycommodity_commoditytype_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[commoditytype]': '1,',
        })
        response = self.client.post(reverse('Web:GetMyCommodity'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数    

    def test_getmycommodity_commoditytype_is_none_type(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[commoditytype]': '-1,',
        })
        response = self.client.post(reverse('Web:GetMyCommodity'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数          
    
    def test_createmycommodity_outsideplatformid_is_exists(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'outsideplatformid': '528731068410',
        }         
        response = self.client.post(reverse('Web:CreateMyCommodity'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        msg = response_json['msg']
        self.assertEqual(msg, '该商品已存在，无法再次新增') # 判断数据  

    def test_createmycommodity_outsideplatformid_is_not_exists(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'outsideplatformid': '3',
            'title': '商品3',
            'price': 1,
            'sales': 1,
            'commissionpercent': 1,
            'subtitle': '商品3',
        }         
        response = self.client.post(reverse('Web:CreateMyCommodity'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        goodslist = Goods.objects.all()
        self.assertEqual(goodslist.count(), 3) # 判断数据条数    
    
    def test_delete_mycommodity_by_ids(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        Goods.objects.create(Title='测试删除', OutSidePlatformID='609085313143', SubTitle='商品3', Owner=self.super_user)        
        goodslistbefore = Goods.objects.all()
        self.assertEqual(goodslistbefore.count(), 3) # 判断数据条数     
        goods = Goods.objects.get(Title='测试删除')         
        param = {
            'ids': str(goods.id) + ','
        }         
        response = self.client.post(reverse('Web:DeleteMyCommodity'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:MyCommodity'))  # 判断跳转
        goodslist = Goods.objects.all()
        self.assertEqual(goodslist.count(), 2) # 判断数据条数     

    def test_editmycommodity(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        Goods.objects.create(Title='旧数据', OutSidePlatformID='609085313143', SubTitle='商品3', Owner=self.super_user)
        goods = Goods.objects.get(Title='旧数据')
        self.assertEqual(goods.Title, '旧数据') # 判断数据          
        param = {
            'id': goods.id,
            'subtitle': '新数据',
            'category': '1,'
        }         
        response = self.client.post(reverse('Web:EditMyCommodity'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        goods = Goods.objects.get(id=goods.id)
        self.assertEqual(goods.SubTitle, '新数据') # 判断数据   
        self.assertEqual(goods.GoodClassifications.count(), 1) # 判断数据             

    def test_getmycommoditybyid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'id': 1,
        }
        response = self.client.post(reverse('Web:GetMyCommodityById'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, 1) # 判断数据 
        title_result = response_json['title']
        self.assertEqual(title_result, '商品1') # 判断数据              
        subtitle_result = response_json['subtitle']
        self.assertEqual(subtitle_result, '商品1') # 判断数据      
        outsideplatformid_result = response_json['outsideplatformid']
        self.assertEqual(outsideplatformid_result, '528731068410') # 判断数据                     

    def test_uploamutidvideo(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        with open('D:\\Work\MobilePhone\\unittest vanilla data\\hasgoods.mp4', 'br') as fp:
            res = self.client.post(reverse('Web:UploadMutiVideo'), { 'guid': '123-456-789', 'file': fp })
        with open('D:\\Work\MobilePhone\\unittest vanilla data\\nothasgoods.mp4', 'br') as fp:
            res = self.client.post(reverse('Web:UploadMutiVideo'), { 'guid': '123-456-789', 'file': fp })            
        videolist = list(Videos.objects.filter(Remark='123-456-789'))
        self.assertEqual(len(videolist), 2) # 判断数据条数
        for i in range(len(videolist)):
            video = videolist[i]
            video.URL.delete()  

    def test_createmutivideo(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        with open('D:\\Work\MobilePhone\\unittest vanilla data\\hasgoods.mp4', 'br') as fp:
            res = self.client.post(reverse('Web:UploadMutiVideo'), { 'guid': '123-456-789', 'file': fp })
        with open('D:\\Work\MobilePhone\\unittest vanilla data\\nothasgoods.mp4', 'br') as fp:
            res = self.client.post(reverse('Web:UploadMutiVideo'), { 'guid': '123-456-789', 'file': fp })            
        param = {
            'title': 'title1\ntitle2',
            'remark': 'remark',
            'category': '1,',
            'commodityid': 2,
            'videokeyword': 'keyword1\nkeyword2',
            'guid': '123-456-789',
        }
        response = self.client.post(reverse('Web:CreateMutiVideo'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        videolist = list(Videos.objects.filter(Remark='remark'))
        self.assertEqual(len(videolist), 2) # 判断数据条数               
        video1 = videolist[0]
        self.assertEqual(video1.Title, 'title1') # 判断数据 
        self.assertEqual(video1.Remark, 'remark') # 判断数据 
        self.assertEqual(video1.VideoClassifications.count(), 1) # 判断数据 
        self.assertEqual(video1.Goods.id, 2) # 判断数据 
        self.assertEqual(video1.VideoKeyword, 'keyword1') # 判断数据                                 
        video1.URL.delete()
        video2 = videolist[1]
        self.assertEqual(video2.Title, 'title2') # 判断数据 
        self.assertEqual(video2.Remark, 'remark') # 判断数据 
        self.assertEqual(video2.VideoClassifications.count(), 1) # 判断数据 
        self.assertEqual(video2.Goods.id, 2) # 判断数据 
        self.assertEqual(video2.VideoKeyword, 'keyword2') # 判断数据                                 
        video2.URL.delete()        
        
    def test_createmutimission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        with open('D:\\Work\MobilePhone\\unittest vanilla data\\hasgoods.mp4', 'br') as fp:
            res = self.client.post(reverse('Web:UploadMutiVideo'), { 'guid': '123-456-789', 'file': fp })
        with open('D:\\Work\MobilePhone\\unittest vanilla data\\nothasgoods.mp4', 'br') as fp:
            res = self.client.post(reverse('Web:UploadMutiVideo'), { 'guid': '123-456-789', 'file': fp })            
        CreateMutiVideoParam = {
            'title': 'title1\ntitle2',
            'remark': 'remark',
            'category': '1,',
            'commodityid': 2,
            'videokeyword': 'keyword1\nkeyword2',
            'guid': '123-456-789',
        }
        response = self.client.post(reverse('Web:CreateMutiVideo'), data=CreateMutiVideoParam)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        videolist = list(Videos.objects.filter(Remark='remark'))
        self.assertEqual(len(videolist), 2) # 判断数据条数  
        CreateMutiMissionParam = {
            'deviceid': '1,2',
            'commodityid': 2
        }
        response = self.client.post(reverse('Web:CreateMutiMission'), data=CreateMutiMissionParam)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        videomissionlist = VideoMission.objects.all()
        self.assertEqual(len(videomissionlist), 6) # 判断数据条数          
        video1 = videolist[0]                               
        video1.URL.delete()
        video2 = videolist[1]                                
        video2.URL.delete()        
        
    def test_removeuploamutidvideo(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        with open('D:\\Work\MobilePhone\\unittest vanilla data\\hasgoods.mp4', 'br') as fp:
            res = self.client.post(reverse('Web:UploadMutiVideo'), { 'guid': '123-456-789', 'file': fp })        
        videolist = list(Videos.objects.filter(Remark='123-456-789'))
        self.assertEqual(len(videolist), 1) # 判断数据条数
        param = {
            'uuid': 'hasgoods.mp4',
        }
        response = self.client.post(reverse('Web:RemoveUploadMutiVideo'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        videolist = list(Videos.objects.filter(Remark='123-456-789'))
        self.assertEqual(len(videolist), 0) # 判断数据条数        
    # end 我的商品

    # begin 商品类别
    def test_commoditycategory(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:CommodityCategory'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/CommodityManage/CommodityCategory.html')  # 判断渲染的模板是否正确   

    def test_getcommoditycategory(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()           
        response = self.client.post(reverse('Web:GetCommodityCategory'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数

    def test_createcommoditycategory(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'name': '测试新增',
        }         
        response = self.client.post(reverse('Web:CreateCommodityCategory'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        goodclassificationlist = GoodClassification.objects.all()
        self.assertEqual(goodclassificationlist.count(), 2) # 判断数据条数

    def test_editcommoditycategory(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        GoodClassification.objects.create(Name='旧数据', Owner=self.super_user)
        goodclassification = GoodClassification.objects.get(Name='旧数据')
        self.assertEqual(goodclassification.Name, '旧数据') # 判断数据          
        param = {
            'id': goodclassification.id,
            'name': '新数据',
        }         
        response = self.client.post(reverse('Web:EditCommodityCategory'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        goodclassification = GoodClassification.objects.get(id=goodclassification.id)
        self.assertEqual(goodclassification.Name, '新数据') # 判断数据        

    def test_delete_commoditycategory_by_ids(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        GoodClassification.objects.create(Name='测试删除', Owner=self.super_user)
        goodclassificationbefore = GoodClassification.objects.all()
        self.assertEqual(goodclassificationbefore.count(), 2) # 判断数据条数     
        goodclassification = GoodClassification.objects.get(Name='测试删除')         
        param = {
            'ids': str(goodclassification.id) + ','
        }         
        response = self.client.post(reverse('Web:DeleteCommodityCategory'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:CommodityCategory'))  # 判断跳转
        goodclassificationlist = GoodClassification.objects.all()
        self.assertEqual(goodclassificationlist.count(), 1) # 判断数据条数     

    def test_getcommoditycategorybyid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'id': 1,
        }
        response = self.client.post(reverse('Web:GetCommodityCategoryByID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, 1) # 判断数据 
        nickname_result = response_json['name']
        self.assertEqual(nickname_result, '商品分类1') # 判断数据              
      
    # end 商品类别

    # begin 我的视频

    def test_myvideo(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:MyVideo'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/VideoManage/MyVideo.html')  # 判断渲染的模板是否正确   

    def test_getmyvideo_generalSearch_and_tiktokaccountcolumn_is_myvideocolumn(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalVideoSearch]': 'has',
            'query[myvideocolumn]': 'myvideocolumn'
        })
        response = self.client.post(reverse('Web:GetMyVideo'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数      

    def test_getmyvideo_generalSearch_and_tiktokaccountcolumn_is_keyword(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalVideoSearch]': 'keyword1',
            'query[myvideocolumn]': 'keyword'
        })
        response = self.client.post(reverse('Web:GetMyVideo'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数   

    def test_getmyvideo_generalSearch_and_tiktokaccountcolumn_is_goodtitle(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalVideoSearch]': '商品1',
            'query[myvideocolumn]': 'goodtitle'
        })
        response = self.client.post(reverse('Web:GetMyVideo'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数                  
    
    def test_getmyvideo_videotype_is_int(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[videotype]': '1,',
        })
        response = self.client.post(reverse('Web:GetMyVideo'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数   

    def test_getmyvideo_videotype_is_none_type(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[videotype]': '-1,',
        })
        response = self.client.post(reverse('Web:GetMyVideo'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 3) # 判断数据条数               

    def test_getmyvideo_videostatus_is_true(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[videostatus]': 'True',
        })
        response = self.client.post(reverse('Web:GetMyVideo'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数   

    def test_getmyvideo_videostatus_is_false(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[videostatus]': 'False',
        })
        response = self.client.post(reverse('Web:GetMyVideo'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 3) # 判断数据条数   

    def test_getmyvideo_hascommodity_is_true(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[hascommodity]': 'True',
        })
        response = self.client.post(reverse('Web:GetMyVideo'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数   

    def test_getmyvideo_hascommodity_is_false(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[hascommodity]': 'False',
        })
        response = self.client.post(reverse('Web:GetMyVideo'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 3) # 判断数据条数   
            
    def test_createmyvideo_get(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.get(reverse('Web:CreateMyVideo'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        videolist = Videos.objects.all()
        self.assertEqual(videolist.count(), 5) # 判断数据条数                 
        
    def test_createmyvideo_post(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.get(reverse('Web:CreateMyVideo'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        video_id = response_json['dataid']
        param = {
            'title': 'title1',
            'remark': 'remark',
            'category': '1,',
            'commodityid': 2,
            'videokeyword': 'keyword1',
            'dataid': video_id,
        }
        response = self.client.post(reverse('Web:CreateMyVideo'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        video = Videos.objects.get(id=video_id)          
        self.assertEqual(video.Title, 'title1') # 判断数据 
        self.assertEqual(video.Remark, 'remark') # 判断数据 
        self.assertEqual(video.VideoClassifications.count(), 1) # 判断数据 
        self.assertEqual(video.Goods.id, 2) # 判断数据 
        self.assertEqual(video.VideoKeyword, 'keyword1') # 判断数据                                 
        
    def test_uploadmyvideo(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.get(reverse('Web:CreateMyVideo'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        video_id = response_json['dataid']
        with open('D:\\Work\MobilePhone\\unittest vanilla data\\hasgoods.mp4', 'br') as fp:
            res = self.client.post(reverse('Web:UploadMyVideo'), { 'dataid': video_id, 'file': fp })          
        video = Videos.objects.get(id=video_id)
        self.assertIsNotNone(video.URL) # 判断数据条数
        video.URL.delete()

    def test_delete_myvideo_by_ids(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.get(reverse('Web:CreateMyVideo'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        videolist = Videos.objects.all()
        self.assertEqual(videolist.count(), 5) # 判断数据条数    
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        video_id = response_json['dataid']        
        param = {
            'ids': str(video_id) + ','
        }         
        response = self.client.post(reverse('Web:DeleteMyVideo'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:MyVideo'))  # 判断跳转
        videolist = Videos.objects.all()
        self.assertEqual(videolist.count(), 4) # 判断数据条数     

    def test_editmyvideo(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.get(reverse('Web:CreateMyVideo'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        video_id = response_json['dataid']
        param = {
            'title': 'title1',
            'remark': 'remark',
            'category': '1,',
            'commodityid': 2,
            'videokeyword': 'keyword1',
            'dataid': video_id,
        }
        response = self.client.post(reverse('Web:CreateMyVideo'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        video = Videos.objects.get(id=video_id)          
        self.assertEqual(video.Title, 'title1') # 判断数据 
        self.assertEqual(video.Remark, 'remark') # 判断数据 
        self.assertEqual(video.VideoClassifications.count(), 1) # 判断数据 
        self.assertEqual(video.Goods.id, 2) # 判断数据 
        self.assertEqual(video.VideoKeyword, 'keyword1') # 判断数据        
        param = {
            'title': 'newtitle1',
            'remark': 'newremark',
            'category': '',
            'commodityid': 1,
            'videokeyword': 'newkeyword1',
            'id': video_id,
        }
        response = self.client.post(reverse('Web:EditMyVideo'), data=param)  
        self.assertEqual(response.status_code, 200)  # 判断状态码
        video = Videos.objects.get(id=video_id)          
        self.assertEqual(video.Title, 'newtitle1') # 判断数据 
        self.assertEqual(video.Remark, 'newremark') # 判断数据 
        self.assertEqual(video.VideoClassifications.count(), 0) # 判断数据 
        self.assertEqual(video.Goods.id, 1) # 判断数据 
        self.assertEqual(video.VideoKeyword, 'newkeyword1') # 判断数据                             
    
    def test_getmyvideobyid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.get(reverse('Web:CreateMyVideo'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        video_id = response_json['dataid']
        param = {
            'title': 'title1',
            'remark': 'remark',
            'category': '1,',
            'commodityid': 2,
            'videokeyword': 'keyword1',
            'dataid': video_id,
        }
        response = self.client.post(reverse('Web:CreateMyVideo'), data=param)
        with open('D:\\Work\MobilePhone\\unittest vanilla data\\hasgoods.mp4', 'br') as fp:
            res = self.client.post(reverse('Web:UploadMyVideo'), { 'dataid': video_id, 'file': fp })          
        video = Videos.objects.get(id=video_id)
        self.assertIsNotNone(video.URL) # 判断数据      
        param = {
            'id': video_id,
        }
        response = self.client.post(reverse('Web:GetMyVideobyID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        title_result = response_json['title']
        self.assertEqual(title_result, 'title1') # 判断数据              
        keyword_result = response_json['videokeyword']
        self.assertEqual(keyword_result, 'keyword1') # 判断数据        
        video.URL.delete()          

    def test_getmyvideourlbyid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.get(reverse('Web:CreateMyVideo'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        video_id = response_json['dataid']
        param = {
            'title': 'title1',
            'remark': 'remark',
            'category': '1,',
            'commodityid': 2,
            'videokeyword': 'keyword1',
            'dataid': video_id,
        }
        response = self.client.post(reverse('Web:CreateMyVideo'), data=param)
        with open('D:\\Work\MobilePhone\\unittest vanilla data\\hasgoods.mp4', 'br') as fp:
            res = self.client.post(reverse('Web:UploadMyVideo'), { 'dataid': video_id, 'file': fp })          
        video = Videos.objects.get(id=video_id)
        self.assertIsNotNone(video.URL) # 判断数据      
        param = {
            'id': video_id,
        }
        response = self.client.post(reverse('Web:GetMyVideoURLByID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        url_result = response_json['url']
        self.assertEqual(url_result, video.URL.url) # 判断数据                 
        video.URL.delete()          
      
    def test_createvideomission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.get(reverse('Web:CreateMyVideo'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        video_id = response_json['dataid']
        with open('D:\\Work\MobilePhone\\unittest vanilla data\\hasgoods.mp4', 'br') as fp:
            res = self.client.post(reverse('Web:UploadMyVideo'), { 'dataid': video_id, 'file': fp })          
        video = Videos.objects.get(id=video_id)
        self.assertIsNotNone(video.URL) # 判断数据条数     
        CreateVideoParam = {
            'deviceid': '1',
            'dataid': video_id,
            'keyword': 'keyword1',
        }
        response = self.client.post(reverse('Web:CreateVideoMission'), data=CreateVideoParam)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        videomissionlist = VideoMission.objects.all()
        self.assertEqual(len(videomissionlist), 5) # 判断数据条数 
        video.URL.delete()  
          
    def test_removeuploadmyvideo(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.get(reverse('Web:CreateMyVideo'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        video_id = response_json['dataid']
        with open('D:\\Work\MobilePhone\\unittest vanilla data\\hasgoods.mp4', 'br') as fp:
            res = self.client.post(reverse('Web:UploadMyVideo'), { 'dataid': video_id, 'file': fp })          
        video = Videos.objects.get(id=video_id)
        self.assertIsNotNone(video.URL) # 判断数据条数  
        videolist = Videos.objects.all()
        self.assertEqual(videolist.count(), 5) # 判断数据条数            
        param = {
            'uuid': 'hasgoods.mp4',
        }
        response = self.client.post(reverse('Web:RemoveUploadMyVideo'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        videolist = Videos.objects.all()
        self.assertEqual(videolist.count(), 5) # 判断数据条数        
    
    # end 我的视频

    # begin 视频标签
    def test_videolabel(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:VideoLabel'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/VideoManage/VideoLabel.html')  # 判断渲染的模板是否正确   

    def test_getvideolabel(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()           
        response = self.client.post(reverse('Web:GetVideoLabel'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数

    def test_createvideolabel(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'name': '测试新增',
        }         
        response = self.client.post(reverse('Web:CreateVideoLabel'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        videoclassificationlist = VideoClassification.objects.all()
        self.assertEqual(videoclassificationlist.count(), 2) # 判断数据条数

    def test_editvideolabel(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        VideoClassification.objects.create(Name='旧数据', Owner=self.super_user)
        videoclassification = VideoClassification.objects.get(Name='旧数据')
        self.assertEqual(videoclassification.Name, '旧数据') # 判断数据          
        param = {
            'id': videoclassification.id,
            'name': '新数据',
        }         
        response = self.client.post(reverse('Web:EditVideoLabel'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        videoclassification = VideoClassification.objects.get(id=videoclassification.id)
        self.assertEqual(videoclassification.Name, '新数据') # 判断数据        

    def test_delete_videolabel_by_ids(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        VideoClassification.objects.create(Name='测试删除', Owner=self.super_user)
        videoclassificationbefore = VideoClassification.objects.all()
        self.assertEqual(videoclassificationbefore.count(), 2) # 判断数据条数     
        videoclassification = VideoClassification.objects.get(Name='测试删除')         
        param = {
            'ids': str(videoclassification.id) + ','
        }         
        response = self.client.post(reverse('Web:DeleteVideoLabel'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:VideoLabel'))  # 判断跳转
        videoclassificationlist = VideoClassification.objects.all()
        self.assertEqual(videoclassificationlist.count(), 1) # 判断数据条数     

    def test_getvideolabelbyid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'id': 1,
        }
        response = self.client.post(reverse('Web:GetVideoLabelByID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, 1) # 判断数据 
        nickname_result = response_json['name']
        self.assertEqual(nickname_result, '视频分类1') # 判断数据              
       
    # end 视频标签

    # begin 视频任务
    def test_videomission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:VideoMission'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/VideoManage/VideoMission.html')  # 判断渲染的模板是否正确       

    def test_getvideomission_generalSearch_and_tiktokaccountcolumn_is_videotitle(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalVideoMissionSearch]': 'video1',
            'query[videomissioncolumn]': 'videotitle'
        })
        response = self.client.post(reverse('Web:GetVideoMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数      

    def test_getvideomission_generalSearch_and_tiktokaccountcolumn_is_keyword(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalVideoMissionSearch]': 'keyword2',
            'query[videomissioncolumn]': 'keyword'
        })
        response = self.client.post(reverse('Web:GetVideoMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数    

    def test_getvideomission_generalSearch_and_tiktokaccountcolumn_is_goodtitle(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalVideoMissionSearch]': '商品1',
            'query[videomissioncolumn]': 'goodtitle'
        })
        response = self.client.post(reverse('Web:GetVideoMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数   

    def test_getvideomission_generalSearch_and_tiktokaccountcolumn_is_mobileid_digit(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalVideoMissionSearch]': '1',
            'query[videomissioncolumn]': 'mobileid'
        })
        response = self.client.post(reverse('Web:GetVideoMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数           

    def test_getvideomission_generalSearch_and_tiktokaccountcolumn_is_mobileid_str(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalVideoMissionSearch]': 'a',
            'query[videomissioncolumn]': 'mobileid'
        })
        response = self.client.post(reverse('Web:GetVideoMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数                   
    
    def test_getvideomission_status_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[status]': '0,1,',
        })
        response = self.client.post(reverse('Web:GetVideoMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数      
    
    def test_getvideomission_commoditytype_is_int(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[commoditytype]': '1,',
        })
        response = self.client.post(reverse('Web:GetVideoMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数  

    def test_getvideomission_commoditytype_is_none_type(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[commoditytype]': '-1,',
        })
        response = self.client.post(reverse('Web:GetVideoMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 3) # 判断数据条数                
    
    def test_getvideomission_videotype_is_int(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[videotype]': '1,',
        })
        response = self.client.post(reverse('Web:GetVideoMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数  

    def test_getvideomission_videotype_is_none_type(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[videotype]': '-1,',
        })
        response = self.client.post(reverse('Web:GetVideoMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 3) # 判断数据条数                

    def test_getvideomission_starttime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        param = self.datatable_param.copy()
        param.update({
            'query[starttime]': date,
        })
        response = self.client.post(reverse('Web:GetVideoMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数  

    def test_getvideomission_endtime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        param = self.datatable_param.copy()
        param.update({
            'query[endtime]': date,
        })
        response = self.client.post(reverse('Web:GetVideoMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 0) # 判断数据条数          
    
    def test_getvideomission_starttime_is_not_none_and_endtime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        startdate = datetime.datetime.now() - datetime.timedelta(days=1)
        enddate = datetime.datetime.now() + datetime.timedelta(days=1)        
        param = self.datatable_param.copy()
        param.update({
            'query[starttime]': startdate,
            'query[endtime]': enddate,
        })
        response = self.client.post(reverse('Web:GetVideoMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数          
   
    def test_delete_videomission_by_ids(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)      
        param = {
            'ids': '1,'
        }         
        response = self.client.post(reverse('Web:DeleteVideoMission'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:VideoMission'))  # 判断跳转
        videomissionlist = VideoMission.objects.all()
        self.assertEqual(videomissionlist.count(), 3) # 判断数据条数     

    def test_editvideomission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        videomission = VideoMission.objects.get(id=1)
        self.assertIsNone(videomission.VideoKeyword) # 判断数据          
        param = {
            'id': videomission.id,
            'videokeyword': 'videokeyword1',
        }         
        response = self.client.post(reverse('Web:EditVideoMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        videomission = VideoMission.objects.get(id=videomission.id)
        self.assertEqual(videomission.VideoKeyword, 'videokeyword1') # 判断数据        

    def test_getvideomissionbyid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'id': 1,
        }
        response = self.client.post(reverse('Web:GetVideoMissionByID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, 1) # 判断数据 
        videotitle_result = response_json['videotitle']
        self.assertEqual(videotitle_result, 'video1') # 判断数据        
        goodtitle_result = response_json['goodtitle']
        self.assertEqual(goodtitle_result, '商品1') # 判断数据                
       
    def test_relaunchvideomission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        videomission = VideoMission.objects.get(id=4)
        self.assertEqual(videomission.Status, 3)  # 判断数据           
        param = {
            'id': 4,
        }
        response = self.client.post(reverse('Web:RelaunchVideoMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        videomission = VideoMission.objects.get(id=4)
        self.assertEqual(videomission.Status, 0)  # 判断数据                      
           
    # end 视频任务 
   
    # begin 关注任务
    def test_publishfollowmission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:PublishFollowMission'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/MissionManage/PublishFollowMission.html')  # 判断渲染的模板是否正确        

    def test_getfollowmission_generalSearch_is_digit(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalFollowMissionSearch]': '1',
        })
        response = self.client.post(reverse('Web:GetFollowMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数           

    def test_getfollowmission_generalSearch_is_str(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalFollowMissionSearch]': 'a',
        })
        response = self.client.post(reverse('Web:GetFollowMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数                   
    
    def test_getfollowmission_status_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[followmissionstatus]': '0,1,',
        })
        response = self.client.post(reverse('Web:GetFollowMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数      
    
    def test_getfollowmission_starttime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        param = self.datatable_param.copy()
        param.update({
            'query[starttime]': date,
        })
        response = self.client.post(reverse('Web:GetFollowMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数  

    def test_getfollowmission_endtime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        param = self.datatable_param.copy()
        param.update({
            'query[endtime]': date,
        })
        response = self.client.post(reverse('Web:GetFollowMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 0) # 判断数据条数          
    
    def test_getfollowmission_starttime_is_not_none_and_endtime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        startdate = datetime.datetime.now() - datetime.timedelta(days=1)
        enddate = datetime.datetime.now() + datetime.timedelta(days=1)        
        param = self.datatable_param.copy()
        param.update({
            'query[starttime]': startdate,
            'query[endtime]': enddate,
        })
        response = self.client.post(reverse('Web:GetFollowMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数          
   
    def test_delete_followmission_by_ids(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)      
        param = {
            'ids': '1,'
        }         
        response = self.client.post(reverse('Web:DeleteFollowMission'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:PublishFollowMission'))  # 判断跳转
        followmissionlist = FollowMission.objects.all()
        self.assertEqual(followmissionlist.count(), 3) # 判断数据条数     

    def test_createfollowmission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)                               
        param = {
            'deviceid': '1',
            'fansexismale': 'true',
            'fansexisfemale': 'false',
            'fansexisnone': 'true',
            'starttime': '',
            'endtime': '',
        }         
        response = self.client.post(reverse('Web:CreateFollowMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        followmissionlist = FollowMission.objects.all()
        self.assertEqual(followmissionlist.count(), 5) # 判断数据条数                        

    def test_editfollowmission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        followmission = FollowMission.objects.get(id=1)
        self.assertFalse(followmission.FanSexIsMale) # 判断数据   
        self.assertFalse(followmission.FanSexIsFemale) # 判断数据
        self.assertFalse(followmission.FanSexIsNone) # 判断数据                       
        param = {
            'id': followmission.id,
            'fansexismale': 'true',
            'fansexisfemale': 'true',
            'fansexisnone': 'true',
            'starttime': '',
            'endtime': '',
        }         
        response = self.client.post(reverse('Web:EditFollowMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        followmission = FollowMission.objects.get(id=followmission.id)
        self.assertTrue(followmission.FanSexIsMale) # 判断数据 
        self.assertTrue(followmission.FanSexIsFemale) # 判断数据
        self.assertTrue(followmission.FanSexIsNone) # 判断数据                 

    def test_getfollowmissionbyid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'id': 1,
        }
        response = self.client.post(reverse('Web:GetFollowMissionByID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, 1) # 判断数据 
        fansexismale_result = response_json['fansexismale']
        self.assertFalse(fansexismale_result) # 判断数据        
        fansexisfemale_result = response_json['fansexisfemale']
        self.assertFalse(fansexisfemale_result) # 判断数据   
        fansexisnone_result = response_json['fansexisnone']
        self.assertFalse(fansexisnone_result) # 判断数据                         
                             
    # end 关注任务

    # begin 养号任务
    def test_publishmaintenancenumbermission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:PublishMaintenanceNumberMission'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/MissionManage/PublishMaintenanceNumberMission.html')  # 判断渲染的模板是否正确        

    def test_getmaintenancenumbermission_generalSearch_is_digit(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalMaintenanceNumberMissionSearch]': '1',
        })
        response = self.client.post(reverse('Web:GetMaintenanceNumberMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数           

    def test_getmaintenancenumbermission_generalSearch_is_str(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalMaintenanceNumberMissionSearch]': 'a',
        })
        response = self.client.post(reverse('Web:GetMaintenanceNumberMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数                   
    
    def test_getmaintenancenumbermission_status_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[maintenancenumbermissionstatus]': '0,1,',
        })
        response = self.client.post(reverse('Web:GetMaintenanceNumberMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数      
    
    def test_getmaintenancenumbermission_starttime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        param = self.datatable_param.copy()
        param.update({
            'query[starttime]': date,
        })
        response = self.client.post(reverse('Web:GetMaintenanceNumberMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数  

    def test_getmaintenancenumbermission_endtime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        param = self.datatable_param.copy()
        param.update({
            'query[endtime]': date,
        })
        response = self.client.post(reverse('Web:GetMaintenanceNumberMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 0) # 判断数据条数          
    
    def test_getmaintenancenumbermission_starttime_is_not_none_and_endtime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        startdate = datetime.datetime.now() - datetime.timedelta(days=1)
        enddate = datetime.datetime.now() + datetime.timedelta(days=1)        
        param = self.datatable_param.copy()
        param.update({
            'query[starttime]': startdate,
            'query[endtime]': enddate,
        })
        response = self.client.post(reverse('Web:GetMaintenanceNumberMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数          
    
    def test_delete_maintenancenumbermission_by_ids(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)      
        param = {
            'ids': '1,'
        }         
        response = self.client.post(reverse('Web:DeleteMaintenanceNumberMission'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:PublishMaintenanceNumberMission'))  # 判断跳转
        maintenancenumbermissionlist = MaintenanceNumberMission.objects.all()
        self.assertEqual(maintenancenumbermissionlist.count(), 3) # 判断数据条数     

    def test_createmaintenancenumbermission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)                               
        param = {
            'deviceid': '1',
            'starttime': '',
            'endtime': '',
        }         
        response = self.client.post(reverse('Web:CreateMaintenanceNumberMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        maintenancenumbermissionlist = MaintenanceNumberMission.objects.all()
        self.assertEqual(maintenancenumbermissionlist.count(), 5) # 判断数据条数                        

    def test_editmaintenancenumbermission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        maintenancenumbermission = MaintenanceNumberMission.objects.get(id=1)                      
        param = {
            'id': maintenancenumbermission.id,
            'starttime': '',
            'endtime': '',
        }         
        response = self.client.post(reverse('Web:EditMaintenanceNumberMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码         

    def test_getmaintenancenumbermissionbyid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'id': 1,
        }
        response = self.client.post(reverse('Web:GetMaintenanceNumberMissionByID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, 1) # 判断数据 
        status_result = response_json['status']
        self.assertEqual(status_result, 0) # 判断数据               
                      
    # end 养号任务

    # begin 养号任务关键字
    def test_publishmaintenancenumbermissionkeyword(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:PublishMaintenanceNumberMissionKeyword'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/MyLabel/MaintenanceNumberMissionKeyword.html')  # 判断渲染的模板是否正确        

    def test_getmaintenancenumbermissionkeyword_generalSearch_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalMaintenanceNumberMissionKeywordSearch]': '关键词1',
        })
        response = self.client.post(reverse('Web:GetMaintenanceNumberMissionKeyword'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数           

    def test_getmaintenancenumbermissionkeyword_tag_is_int(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[tag]': '1,',
        })
        response = self.client.post(reverse('Web:GetMaintenanceNumberMissionKeyword'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数  

    def test_getmaintenancenumbermissionkeyword_tag_is_none_type(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[tag]': '-1,',
        })
        response = self.client.post(reverse('Web:GetMaintenanceNumberMissionKeyword'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数          
    
    def test_delete_maintenancenumbermissionkeyword_by_ids(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)      
        param = {
            'ids': '1,'
        }         
        response = self.client.post(reverse('Web:DeleteMaintenanceNumberMissionKeyword'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:PublishMaintenanceNumberMissionKeyword'))  # 判断跳转
        maintenancenumbermissionkeywordlist = MaintenanceNumberMissionKeyword.objects.all()
        self.assertEqual(maintenancenumbermissionkeywordlist.count(), 2) # 判断数据条数     

    def test_createmaintenancenumbermissionkeyword_name_is_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)                               
        param = {
            'name': '',
        }         
        response = self.client.post(reverse('Web:CreateMaintenanceNumberMissionKeyword'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        msg = response_json['msg']
        self.assertIsNone(msg) # 判断数据        
    
    def test_createmaintenancenumbermissionkeyword_name_is_not_none_and_category_is_none_and_name_is_not_exists(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)                               
        param = {
            'name': '新增数据',
        }         
        response = self.client.post(reverse('Web:CreateMaintenanceNumberMissionKeyword'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        status = response_json['status']
        self.assertEqual(status, 'OK') # 判断数据     
        jump = response_json['jump']
        self.assertEqual(jump, reverse('Web:PublishMaintenanceNumberMissionKeyword')) # 判断数据   
        maintenancenumbermissionkeywordlist = MaintenanceNumberMissionKeyword.objects.all()
        self.assertEqual(maintenancenumbermissionkeywordlist.count(), 4) # 判断数据条数               

    def test_createmaintenancenumbermissionkeyword_name_is_not_none_and_category_is_not_none_and_name_is_not_exists(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)                               
        param = {
            'name': '新增数据',
            'category': '1,',
        }         
        response = self.client.post(reverse('Web:CreateMaintenanceNumberMissionKeyword'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        status = response_json['status']
        self.assertEqual(status, 'OK') # 判断数据      
        jump = response_json['jump']
        self.assertEqual(jump, reverse('Web:PublishMaintenanceNumberMissionKeyword')) # 判断数据          
        maintenancenumbermissionkeywordlist = MaintenanceNumberMissionKeyword.objects.all()
        self.assertEqual(maintenancenumbermissionkeywordlist.count(), 4) # 判断数据条数            
    
    def test_createmaintenancenumbermissionkeyword_name_is_not_none_and_category_is_not_none_and_name_is_exists(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)                               
        param = {
            'name': '关键词1',
            'category': '1,',
        }         
        response = self.client.post(reverse('Web:CreateMaintenanceNumberMissionKeyword'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        status = response_json['status']
        self.assertEqual(status, 'OK') # 判断数据      
        jump = response_json['jump']
        self.assertEqual(jump, reverse('Web:PublishMaintenanceNumberMissionKeyword')) # 判断数据          
        maintenancenumbermissionkeywordlist = MaintenanceNumberMissionKeyword.objects.all()
        self.assertEqual(maintenancenumbermissionkeywordlist.count(), 3) # 判断数据条数            
    
    def test_createmaintenancenumbermissionkeyword_name_is_muti_and_category_is_not_none_and_name_is_not_exists(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)                               
        param = {
            'name': '新增数据1 新增数据2',
            'category': '1,',
        }         
        response = self.client.post(reverse('Web:CreateMaintenanceNumberMissionKeyword'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        status = response_json['status']
        self.assertEqual(status, 'OK') # 判断数据      
        jump = response_json['jump']
        self.assertEqual(jump, reverse('Web:PublishMaintenanceNumberMissionKeyword')) # 判断数据          
        maintenancenumbermissionkeywordlist = MaintenanceNumberMissionKeyword.objects.all()
        self.assertEqual(maintenancenumbermissionkeywordlist.count(), 5) # 判断数据条数            
    
    def test_editmaintenancenumbermissionkeyword_name_is_not_none_and_category_is_none_and_name_is_not_exists(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)   
        maintenancenumbermissionkeyword = MaintenanceNumberMissionKeyword.objects.get(id=1) 
        self.assertEqual(maintenancenumbermissionkeyword.Name, '关键词1')                            
        param = {
            'id': 1,
            'name': '新数据',
        }         
        response = self.client.post(reverse('Web:EditMaintenanceNumberMissionKeyword'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        status = response_json['status']
        self.assertEqual(status, 'OK') # 判断数据     
        jump = response_json['jump']
        self.assertEqual(jump, reverse('Web:PublishMaintenanceNumberMissionKeyword')) # 判断数据   
        maintenancenumbermissionkeyword = MaintenanceNumberMissionKeyword.objects.get(id=1) 
        self.assertEqual(maintenancenumbermissionkeyword.Name, '新数据')              
            
    def test_editmaintenancenumbermissionkeyword_name_is_not_none_and_category_is_not_none_and_name_is_not_exists(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)   
        maintenancenumbermissionkeyword = MaintenanceNumberMissionKeyword.objects.get(id=1) 
        self.assertEqual(maintenancenumbermissionkeyword.Name, '关键词1')                            
        param = {
            'id': 1,
            'name': '新数据',
            'category': '1'
        }         
        response = self.client.post(reverse('Web:EditMaintenanceNumberMissionKeyword'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        status = response_json['status']
        self.assertEqual(status, 'OK') # 判断数据     
        jump = response_json['jump']
        self.assertEqual(jump, reverse('Web:PublishMaintenanceNumberMissionKeyword')) # 判断数据   
        maintenancenumbermissionkeyword = MaintenanceNumberMissionKeyword.objects.get(id=1) 
        self.assertEqual(maintenancenumbermissionkeyword.Name, '新数据')              
            
    def test_editmaintenancenumbermissionkeyword_name_is_not_none_and_category_is_not_none_and_name_is_exists(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)   
        maintenancenumbermissionkeyword = MaintenanceNumberMissionKeyword.objects.get(id=1) 
        self.assertEqual(maintenancenumbermissionkeyword.Name, '关键词1')                            
        param = {
            'id': 1,
            'name': '关键词2',
            'category': '1'
        }         
        response = self.client.post(reverse('Web:EditMaintenanceNumberMissionKeyword'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        status = response_json['status']
        self.assertEqual(status, 'NG') # 判断数据     
        msg = response_json['msg']
        self.assertEqual(msg, '该关键词已存在，无法保存') # 判断数据   
        maintenancenumbermissionkeyword = MaintenanceNumberMissionKeyword.objects.get(id=1) 
        self.assertEqual(maintenancenumbermissionkeyword.Name, '关键词1')                
        
    def test_getmaintenancenumbermissionkeywordbyid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'id': 1,
        }
        response = self.client.post(reverse('Web:GetMaintenanceNumberMissionKeywordByID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, 1) # 判断数据 
        name_result = response_json['name']
        self.assertEqual(name_result, '关键词1') # 判断数据               

    def test_getmaintenancenumbermissionkeywordnamesbyid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'ids': '1,2,',
        }
        response = self.client.post(reverse('Web:GetMaintenanceNumberMissionKeywordNamesByID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        ids = response_json['ids']
        self.assertEqual(ids, '1,2') # 判断数据 
        keyword_name_string = response_json['keyword_name_string']
        self.assertEqual(keyword_name_string, '关键词1-标签1,关键词2-标签1') # 判断数据               
             
    # end 养号任务关键字

    # begin 养号任务关键字类型
    def test_publishmaintenancenumbermissionkeywordclassification(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:PublishMaintenanceNumberMissionKeywordClassification'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/MyLabel/MaintenanceNumberMissionKeywordClassification.html')  # 判断渲染的模板是否正确   

    def test_getmaintenancenumbermissionkeywordclassification_generalSearch_is_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()           
        response = self.client.post(reverse('Web:GetMaintenanceNumberMissionKeywordClassification'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数

    def test_getmaintenancenumbermissionkeywordclassification_generalSearch_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()         
        param.update({
            'query[generalMaintenanceNumberMissionKeywordClassificationSearch]': '1',
        })  
        response = self.client.post(reverse('Web:GetMaintenanceNumberMissionKeywordClassification'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数        

    def test_createmaintenancenumbermissionkeywordclassification_name_is_not_exists(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'name': '测试新增',
        }         
        response = self.client.post(reverse('Web:CreateMaintenanceNumberMissionKeywordClassification'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        msg = response_json['msg']
        self.assertEqual(msg, reverse('Web:PublishMaintenanceNumberMissionKeywordClassification')) # 判断数据
        maintenancenumbermissionkeywordclassificationlist = MaintenanceNumberMissionKeywordClassification.objects.all()
        self.assertEqual(maintenancenumbermissionkeywordclassificationlist.count(), 3) # 判断数据条数

    def test_createmaintenancenumbermissionkeywordclassification_name_is_exists(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'name': '标签1',
        }         
        response = self.client.post(reverse('Web:CreateMaintenanceNumberMissionKeywordClassification'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        msg = response_json['msg']
        self.assertEqual(msg, '该标签已存在，无法新增') # 判断数据        
        maintenancenumbermissionkeywordclassificationlist = MaintenanceNumberMissionKeywordClassification.objects.all()
        self.assertEqual(maintenancenumbermissionkeywordclassificationlist.count(), 2) # 判断数据条数        

    def test_editmaintenancenumbermissionkeywordclassification_name_is_not_exists(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        MaintenanceNumberMissionKeywordClassification.objects.create(Name='旧数据')
        maintenancenumbermissionkeywordclassification = MaintenanceNumberMissionKeywordClassification.objects.get(Name='旧数据')
        self.assertEqual(maintenancenumbermissionkeywordclassification.Name, '旧数据') # 判断数据          
        param = {
            'id': maintenancenumbermissionkeywordclassification.id,
            'name': '新数据',
        }         
        response = self.client.post(reverse('Web:EditMaintenanceNumberMissionKeywordClassification'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        msg = response_json['msg']
        self.assertEqual(msg, reverse('Web:PublishMaintenanceNumberMissionKeywordClassification')) # 判断数据
        maintenancenumbermissionkeywordclassification = MaintenanceNumberMissionKeywordClassification.objects.get(id=maintenancenumbermissionkeywordclassification.id)
        self.assertEqual(maintenancenumbermissionkeywordclassification.Name, '新数据') # 判断数据  

    def test_editmaintenancenumbermissionkeywordclassification_name_is_exists(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        MaintenanceNumberMissionKeywordClassification.objects.create(Name='旧数据')
        maintenancenumbermissionkeywordclassification = MaintenanceNumberMissionKeywordClassification.objects.get(Name='旧数据')
        self.assertEqual(maintenancenumbermissionkeywordclassification.Name, '旧数据') # 判断数据          
        param = {
            'id': maintenancenumbermissionkeywordclassification.id,
            'name': '标签1',
        }         
        response = self.client.post(reverse('Web:EditMaintenanceNumberMissionKeywordClassification'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        msg = response_json['msg']
        self.assertEqual(msg, '该标签已存在，无法保存') # 判断数据
        maintenancenumbermissionkeywordclassification = MaintenanceNumberMissionKeywordClassification.objects.get(id=maintenancenumbermissionkeywordclassification.id)
        self.assertEqual(maintenancenumbermissionkeywordclassification.Name, '旧数据') # 判断数据                 

    def test_delete_maintenancenumbermissionkeywordclassification_by_ids(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        MaintenanceNumberMissionKeywordClassification.objects.create(Name='测试删除')
        maintenancenumbermissionkeywordclassificationbefore = MaintenanceNumberMissionKeywordClassification.objects.all()
        self.assertEqual(maintenancenumbermissionkeywordclassificationbefore.count(), 3) # 判断数据条数     
        maintenancenumbermissionkeywordclassification = MaintenanceNumberMissionKeywordClassification.objects.get(Name='测试删除')         
        param = {
            'ids': str(maintenancenumbermissionkeywordclassification.id) + ','
        }         
        response = self.client.post(reverse('Web:DeleteMaintenanceNumberMissionKeywordClassification'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:PublishMaintenanceNumberMissionKeywordClassification'))  # 判断跳转
        maintenancenumbermissionkeywordclassificationlist = MaintenanceNumberMissionKeywordClassification.objects.all()
        self.assertEqual(maintenancenumbermissionkeywordclassificationlist.count(), 2) # 判断数据条数     

    def test_getmaintenancenumbermissionkeywordclassificationbyid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'id': 1,
        }
        response = self.client.post(reverse('Web:GetMaintenanceNumberMissionKeywordClassificationByID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, 1) # 判断数据 
        nickname_result = response_json['name']
        self.assertEqual(nickname_result, '标签1') # 判断数据              
       
    # end 养号任务关键字类型

    # begin 互刷任务
    def test_publishmutualbrushmission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:PublishMutualBrushMission'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/MissionManage/PublishMutualBrushMission.html')  # 判断渲染的模板是否正确  

    def test_getmutualbrushmission_generalSearch_is_digit(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalMutualBrushMissionSearch]': '1',
        })
        response = self.client.post(reverse('Web:GetMutualBrushMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数           

    def test_getmutualbrushmission_generalSearch_is_str(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalMutualBrushMissionSearch]': 'a',
        })
        response = self.client.post(reverse('Web:GetMutualBrushMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数                   
    
    def test_getmutualbrushmission_status_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[mutualbrushmissionstatus]': '0,1,',
        })
        response = self.client.post(reverse('Web:GetMutualBrushMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数      
    
    def test_getmutualbrushmission_starttime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        param = self.datatable_param.copy()
        param.update({
            'query[starttime]': date,
        })
        response = self.client.post(reverse('Web:GetMutualBrushMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数  

    def test_getmutualbrushmission_endtime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        param = self.datatable_param.copy()
        param.update({
            'query[endtime]': date,
        })
        response = self.client.post(reverse('Web:GetMutualBrushMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 0) # 判断数据条数          
    
    def test_getmutualbrushmission_starttime_is_not_none_and_endtime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        startdate = datetime.datetime.now() - datetime.timedelta(days=1)
        enddate = datetime.datetime.now() + datetime.timedelta(days=1)        
        param = self.datatable_param.copy()
        param.update({
            'query[starttime]': startdate,
            'query[endtime]': enddate,
        })
        response = self.client.post(reverse('Web:GetMutualBrushMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数          
      
    def test_delete_mutualbrushmission_by_ids(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)      
        param = {
            'ids': '1,'
        }         
        response = self.client.post(reverse('Web:DeleteMutualBrushMission'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:PublishMutualBrushMission'))  # 判断跳转
        mutualbrushmissionlist = MutualBrushMission.objects.all()
        self.assertEqual(mutualbrushmissionlist.count(), 3) # 判断数据条数     

    def test_createmutualbrushmission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)                               
        param = {
            'deviceid': '1,2',
            'starttime': '',
            'islikerate': '50',
            'videourl': '1',
            'commenttext': 'commenttext1\ncommenttext2',
            'isfollowcount': '1',
            'missionincome': "1.00",
        }         
        response = self.client.post(reverse('Web:CreateMutualBrushMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        mutualbrushmissionlist = MutualBrushMission.objects.all()
        self.assertEqual(mutualbrushmissionlist.count(), 6) # 判断数据条数     
        mutualbrushmission1 = MutualBrushMission.objects.get(id=5)  
        mutualbrushmission2 = MutualBrushMission.objects.get(id=6)          
        self.assertEqual(mutualbrushmission1.VideoURL, '1') # 判断数据  
        self.assertEqual(mutualbrushmission1.CommentText, 'commenttext1') # 判断数据   
        self.assertEqual(mutualbrushmission1.MissionIncome, 1.00) # 判断数据                   
        self.assertEqual(mutualbrushmission2.VideoURL, '1') # 判断数据           
        self.assertEqual(mutualbrushmission2.CommentText, 'commenttext2') # 判断数据    
        self.assertEqual(mutualbrushmission2.MissionIncome, 1.00) # 判断数据                
        if mutualbrushmission1.IsLike :
            self.assertFalse(mutualbrushmission2.IsLike) # 判断数据 
        else:
            self.assertTrue(mutualbrushmission2.IsLike) # 判断数据   
        if mutualbrushmission1.IsFollow :
            self.assertFalse(mutualbrushmission2.IsFollow) # 判断数据 
        else:
            self.assertTrue(mutualbrushmission2.IsFollow) # 判断数据                                 

    def test_editmutualbrushmission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        mutualbrushmission = MutualBrushMission.objects.get(id=1)    
        self.assertIsNone(mutualbrushmission.VideoURL) # 判断数据          
        self.assertFalse(mutualbrushmission.IsLike) # 判断数据 
        self.assertIsNone(mutualbrushmission.CommentText) # 判断数据                       
        param = {
            'id': mutualbrushmission.id,
            'starttime': '',
            'videourl': 'videourl',
            'islike': 'true',
            'commenttext': 'commenttext',
            'isfollow': 'true',
        }         
        response = self.client.post(reverse('Web:EditMutualBrushMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        mutualbrushmission = MutualBrushMission.objects.get(id=1)
        self.assertEqual(mutualbrushmission.VideoURL, 'videourl') # 判断数据          
        self.assertTrue(mutualbrushmission.IsLike) # 判断数据 
        self.assertTrue(mutualbrushmission.IsFollow) # 判断数据 
        self.assertEqual(mutualbrushmission.CommentText, 'commenttext') # 判断数据            

    def test_getmutualbrushmissionbyid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'id': 1,
        }
        response = self.client.post(reverse('Web:GetMutualBrushMissionByID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, 1) # 判断数据 
        status_result = response_json['status']
        self.assertEqual(status_result, 0) # 判断数据             
        mobilephoneid_result = response_json['mobilephoneid']
        self.assertEqual(mobilephoneid_result, 1) # 判断数据    
        videourl_result = response_json['videourl']
        self.assertIsNone(videourl_result) # 判断数据   
        commenttext_result = response_json['commenttext']
        self.assertIsNone(commenttext_result) # 判断数据    
        islike_result = response_json['islike']
        self.assertFalse(islike_result) # 判断数据    
        isfollow_result = response_json['isfollow']
        self.assertFalse(isfollow_result) # 判断数据                                          
                      
    # end 互刷任务

    # begin 刷粉任务
    def test_publishscanmission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:PublishScanMission'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/MissionManage/PublishScanMission.html')  # 判断渲染的模板是否正确  

    def test_getscanmission_generalSearch_is_digit(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalScanMissionSearch]': '1',
        })
        response = self.client.post(reverse('Web:GetScanMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数           

    def test_getscanmission_generalSearch_is_str(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalScanMissionSearch]': 'a',
        })
        response = self.client.post(reverse('Web:GetScanMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数                   
    
    def test_getscanmission_status_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[scanmissionstatus]': '0,1,',
        })
        response = self.client.post(reverse('Web:GetScanMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数      
    
    def test_getscanmission_starttime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        param = self.datatable_param.copy()
        param.update({
            'query[starttime]': date,
        })
        response = self.client.post(reverse('Web:GetScanMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数  

    def test_getscanmission_endtime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        param = self.datatable_param.copy()
        param.update({
            'query[endtime]': date,
        })
        response = self.client.post(reverse('Web:GetScanMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 0) # 判断数据条数          
    
    def test_getscanmission_starttime_is_not_none_and_endtime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        startdate = datetime.datetime.now() - datetime.timedelta(days=1)
        enddate = datetime.datetime.now() + datetime.timedelta(days=1)        
        param = self.datatable_param.copy()
        param.update({
            'query[starttime]': startdate,
            'query[endtime]': enddate,
        })
        response = self.client.post(reverse('Web:GetScanMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数          
      
    def test_delete_scanmission_by_ids(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)      
        param = {
            'ids': '1,'
        }         
        response = self.client.post(reverse('Web:DeleteScanMission'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:PublishScanMission'))  # 判断跳转
        scanmissionlist = ScanMission.objects.all()
        self.assertEqual(scanmissionlist.count(), 3) # 判断数据条数     

    def test_createscanmission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)                               
        param = {
            'deviceid': '1',
            'starttime': '',
            'endtime': '',
            'fansexismale': 'true', 
            'commenttext': '评论库1\n评论库3'          
        }         
        response = self.client.post(reverse('Web:CreateScanMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        scanmissionlist = ScanMission.objects.all()
        self.assertEqual(scanmissionlist.count(), 5) # 判断数据条数  
        scanmission = ScanMission.objects.get(id=5)      
        self.assertEqual(scanmission.PeopleLimit, 100) # 判断数据 
        self.assertEqual(scanmission.Interval, 5) # 判断数据 
        self.assertTrue(scanmission.FanSexIsMale) # 判断数据   
        self.assertFalse(scanmission.FanSexIsFemale) # 判断数据 
        self.assertFalse(scanmission.FanSexIsNone) # 判断数据 
        self.assertEqual(scanmission.CommentTextID, '1,4') # 判断数据        

    def test_editscanmission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        scanmission = ScanMission.objects.get(id=1)    
        self.assertEqual(scanmission.PeopleLimit, 0) # 判断数据 
        self.assertEqual(scanmission.Interval, 0) # 判断数据 
        self.assertFalse(scanmission.FanSexIsMale) # 判断数据   
        self.assertFalse(scanmission.FanSexIsFemale) # 判断数据 
        self.assertFalse(scanmission.FanSexIsNone) # 判断数据 
        self.assertIsNone(scanmission.CommentTextID) # 判断数据                        
        param = {
            'id': scanmission.id,
            'starttime': '',
            'endtime': '',
            'fansexismale': 'true', 
            'commenttext': '评论库1\n评论库2',
            'interval': '10',
            'peoplelimit': '200',
        }         
        response = self.client.post(reverse('Web:EditScanMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        scanmission = ScanMission.objects.get(id=1)
        self.assertEqual(scanmission.PeopleLimit, 200) # 判断数据 
        self.assertEqual(scanmission.Interval, 10) # 判断数据 
        self.assertTrue(scanmission.FanSexIsMale) # 判断数据   
        self.assertFalse(scanmission.FanSexIsFemale) # 判断数据 
        self.assertFalse(scanmission.FanSexIsNone) # 判断数据 
        self.assertEqual(scanmission.CommentTextID, '1,2') # 判断数据                

    def test_getscanmissionbyid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'id': 1,
        }
        response = self.client.post(reverse('Web:GetScanMissionByID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, 1) # 判断数据 
        status_result = response_json['status']
        self.assertEqual(status_result, 0) # 判断数据             
        mobilephoneid_result = response_json['mobilephoneid']
        self.assertEqual(mobilephoneid_result, 1) # 判断数据    
        peoplelimit_result = response_json['peoplelimit']
        self.assertEqual(peoplelimit_result, 0) # 判断数据   
        interval_result = response_json['interval']
        self.assertEqual(interval_result, 0) # 判断数据          
        commenttext_result = response_json['commenttext']
        self.assertEqual(commenttext_result, '') # 判断数据    
        fansexismale_result = response_json['fansexismale']
        self.assertFalse(fansexismale_result) # 判断数据     
        fansexisfemale_result = response_json['fansexisfemale']
        self.assertFalse(fansexisfemale_result) # 判断数据  
        fansexisnone_result = response_json['fansexisnone']
        self.assertFalse(fansexisnone_result) # 判断数据                                                
    
    # end 刷粉任务

    # begin 评论库
    def test_commentlibrary(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:CommentLibrary'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/MissionManage/CommentLibrary.html')  # 判断渲染的模板是否正确   

    def test_getcommentlibrary_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalCommentLibrarySearch]': '1',
        })
        response = self.client.post(reverse('Web:GetCommentLibrary'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数

    def test_getcommentlibrary_is_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        response = self.client.post(reverse('Web:GetCommentLibrary'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数        

    def test_createcommentlibrary(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'text': '测试新增',
        }         
        response = self.client.post(reverse('Web:CreateCommentLibrary'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        commentlibrarylist = CommentLibrary.objects.all()
        self.assertEqual(commentlibrarylist.count(), 3) # 判断数据条数

    def test_editcommentlibrary(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        CommentLibrary.objects.create(Text='旧数据')
        commentlibrary = CommentLibrary.objects.get(Text='旧数据')
        self.assertEqual(commentlibrary.Text, '旧数据') # 判断数据          
        param = {
            'id': commentlibrary.id,
            'text': '新数据',
        }         
        response = self.client.post(reverse('Web:EditCommentLibrary'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        commentlibrary = CommentLibrary.objects.get(id=commentlibrary.id)
        self.assertEqual(commentlibrary.Text, '新数据') # 判断数据        

    def test_delete_commentlibrary_by_ids(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        CommentLibrary.objects.create(Text='测试删除')
        commentlibrarybefore = CommentLibrary.objects.all()
        self.assertEqual(commentlibrarybefore.count(), 3) # 判断数据条数     
        commentlibrary = CommentLibrary.objects.get(Text='测试删除')         
        param = {
            'ids': str(commentlibrary.id) + ','
        }         
        response = self.client.post(reverse('Web:DeleteCommentLibrary'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:CommentLibrary'))  # 判断跳转
        commentlibrarylist = CommentLibrary.objects.all()
        self.assertEqual(commentlibrarylist.count(), 2) # 判断数据条数     

    def test_getcommentlibrarybyid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'id': 1,
        }
        response = self.client.post(reverse('Web:GetCommentLibraryByID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, 1) # 判断数据 
        text_result = response_json['text']
        self.assertEqual(text_result, '评论库1') # 判断数据              
  
    # end 评论库

    # begin 代理审核
    def test_agentverify(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:AgentVerify'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/MyAgent/AgentVerify.html')  # 判断渲染的模板是否正确  

    def test_getagentverify_generalSearch_and_agentVerifycolumn_is_username(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalAgentVerifySearch]': 'alevel',
            'query[agentVerifycolumn]': 'username'
        })
        response = self.client.post(reverse('Web:GetAgentVerify'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数      

    def test_getagentverify_generalSearch_and_agentVerifycolumn_is_leader(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalAgentVerifySearch]': 'blevel',
            'query[agentVerifycolumn]': 'leader'
        })
        response = self.client.post(reverse('Web:GetAgentVerify'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数    

    def test_getagentverify_generalSearch_and_agentVerifycolumn_is_truename(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalAgentVerifySearch]': 'truename',
            'query[agentVerifycolumn]': 'truename'
        })
        response = self.client.post(reverse('Web:GetAgentVerify'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数   

    def test_getagentverify_generalSearch_and_agentVerifycolumn_is_phone(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalAgentVerifySearch]': '1',
            'query[agentVerifycolumn]': 'phone'
        })
        response = self.client.post(reverse('Web:GetAgentVerify'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数           

    def test_passagentverifyassuperuser(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'ids': '4,'
        }         
        response = self.client.post(reverse('Web:PassAgentVerifyASSuperUser'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:AgentVerify'))  # 判断跳转
        user = User.objects.get(id=4)
        self.assertTrue(user.is_pass) # 判断数据 
        self.assertTrue(user.is_superuser) # 判断数据 
        agentlist = Agent.objects.all()
        self.assertEqual(agentlist.count(), 3) # 判断数据条数  
        relationslist = TopUserRelations.objects.all()
        self.assertEqual(relationslist.count(), 1) # 判断数据条数  

    def test_passagentverifyasmainuser(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'ids': '4,'
        }         
        response = self.client.post(reverse('Web:PassAgentVerifyASMainUser'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:AgentVerify'))  # 判断跳转
        user = User.objects.get(id=4)
        self.assertTrue(user.is_pass) # 判断数据 
        self.assertTrue(user.is_mainuser) # 判断数据 
        agentlist = Agent.objects.all()
        self.assertEqual(agentlist.count(), 3) # 判断数据条数  
        relationslist = TopUserRelations.objects.all()
        self.assertEqual(relationslist.count(), 1) # 判断数据条数  

    def test_passagentverifyasagent(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'ids': '4,'
        }         
        response = self.client.post(reverse('Web:PassAgentVerifyASAgent'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:AgentVerify'))  # 判断跳转
        user = User.objects.get(id=4)
        self.assertTrue(user.is_pass) # 判断数据 
        agentlist = Agent.objects.all()
        self.assertEqual(agentlist.count(), 4) # 判断数据条数  
        agent = Agent.objects.get(id=4)
        self.assertEqual(agent.UserSystem.username, 'admin') # 判断数据
        self.assertEqual(agent.UserALevel.username, 'aLevel') # 判断数据
        self.assertEqual(agent.UserBLevel.username, 'bLevel') # 判断数据                
    
    def test_notpassagentverify(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'ids': '4,'
        }         
        response = self.client.post(reverse('Web:NotPassAgentVerify'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:AgentVerify'))  # 判断跳转
        userlist = User.objects.all()
        self.assertEqual(userlist.count(), 3) # 判断数据条数  
 
    # end 代理审核

    # begin 代理列表
    def test_agentlist(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:AgentList'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/MyAgent/AgentList.html')  # 判断渲染的模板是否正确  

    def test_getagentlist_generalSearch_and_agentlistcolumn_is_username(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalAgentSearch]': 'alevel',
            'query[agentlistcolumn]': 'username'
        })
        response = self.client.post(reverse('Web:GetAgentList'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数      

    def test_getagentlist_generalSearch_and_agentlistcolumn_is_alevel(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalAgentSearch]': 'blevel',
            'query[agentlistcolumn]': 'alevel'
        })
        response = self.client.post(reverse('Web:GetAgentList'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数    

    def test_getagentlist_generalSearch_and_agentlistcolumn_is_blevel(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalAgentSearch]': 'bLevel',
            'query[agentlistcolumn]': 'blevel'
        })
        response = self.client.post(reverse('Web:GetAgentList'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数   

    def test_editagentlist(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'id': 3,
            'UserSystemPercent': '30',
            'UserALevelPercent': '20',
            'UserBLevelPercent': '10',
            'deviceid': '1'
        }         
        response = self.client.post(reverse('Web:EditAgentList'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        agent = Agent.objects.get(id=3)
        self.assertEqual(agent.UserSystemPercent, 30) # 判断数据   
        self.assertEqual(agent.UserALevelPercent, 20) # 判断数据
        self.assertEqual(agent.UserBLevelPercent, 10) # 判断数据  
        device = MobilePhone.objects.get(id=1)   
        self.assertEqual(device.Agent.id, 3) # 判断数据  

    def test_getagentlistbyid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'id': 3,
        }
        response = self.client.post(reverse('Web:GetAgentListByID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, 3) # 判断数据 
        username_result = response_json['username']
        self.assertEqual(username_result, 'lastLevel') # 判断数据    
        alevelusername_result = response_json['alevelusername']
        self.assertEqual(alevelusername_result, 'aLevel') # 判断数据 
        blevelusername_result = response_json['blevelusername']
        self.assertEqual(blevelusername_result, 'bLevel') # 判断数据                                 
  
    def test_resetpassword(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        self.blevel_user.password = make_password('1')
        self.blevel_user.save()
        self.assertTrue(check_password('1',  self.blevel_user.password))
        param = {
            'id': 1,
        }
        response = self.client.post(reverse('Web:ResetPassword'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        user = User.objects.get(username='bLevel')
        self.assertTrue(check_password('123456',  user.password))
    # end 代理列表

    # begin 代理账号信息
    def test_agentdetail(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:AgentDetail'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/MyAgent/AgentDetail.html')  # 判断渲染的模板是否正确  

    def test_getagentdetail_generalSearch_and_agentdetailcolumn_is_username(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalAgentDetailSearch]': 'alevel',
            'query[agentdetailcolumn]': 'username'
        })
        response = self.client.post(reverse('Web:GetAgentDetail'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数      

    def test_getagentdetail_generalSearch_and_agentdetailcolumn_is_truename(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalAgentDetailSearch]': 'truename',
            'query[agentdetailcolumn]': 'truename'
        })
        response = self.client.post(reverse('Web:GetAgentDetail'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数    

    def test_getagentdetail_generalSearch_and_agentdetailcolumn_is_phone(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalAgentDetailSearch]': '123',
            'query[agentdetailcolumn]': 'phone'
        })
        response = self.client.post(reverse('Web:GetAgentDetail'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数   

    def test_editagentdetail(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'dataid': 3,
            'true_name': 'true_name',
            'phone': 'phone',
            'wechat': 'wechat',
            'wechat_nickname': 'wechat_nickname',
            'sex': 1,
            'platform': 'platform',
            'platform_id': 'platform_id',
            'platform_password': 'platform_password',
            'platform_is_certification': 1,
            'platform_certification_true_name': 'platform_certification_true_name',
            'platform_certification_id_card': 'platform_certification_id_card',            
        }         
        response = self.client.post(reverse('Web:EditAgentDetail'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        agent = Agent.objects.get(id=3)
        self.assertEqual(agent.Subscriber.true_name, 'true_name') # 判断数据   
        self.assertEqual(agent.Subscriber.phone, 'phone') # 判断数据
        self.assertEqual(agent.Subscriber.wechat, 'wechat') # 判断数据  
        self.assertEqual(agent.Subscriber.wechat_nickname, 'wechat_nickname') # 判断数据   
        self.assertEqual(agent.Subscriber.sex, 1) # 判断数据
        self.assertEqual(agent.Subscriber.platform, 'platform') # 判断数据  
        self.assertEqual(agent.Subscriber.platform_id, 'platform_id') # 判断数据   
        self.assertEqual(agent.Subscriber.platform_password, 'platform_password') # 判断数据
        self.assertTrue(agent.Subscriber.platform_is_certification) # 判断数据    
        self.assertEqual(agent.Subscriber.platform_certification_true_name, 'platform_certification_true_name') # 判断数据   
        self.assertEqual(agent.Subscriber.platform_certification_id_card, 'platform_certification_id_card') # 判断数据                      

    def test_getagentdetailbyid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'id': 3,
        }
        response = self.client.post(reverse('Web:GetAgentDetailByID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, 3) # 判断数据 
        username_result = response_json['username']
        self.assertEqual(username_result, 'lastLevel') # 判断数据                                         

    # end 代理账号信息

    # begin 订单管理
    def test_order(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:Order'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/CommodityManage/Order.html')  # 判断渲染的模板是否正确  

    def test_getorder(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        response = self.client.post(reverse('Web:GetOrder'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 3) # 判断数据条数      

    def test_getorder_accountid_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[accountid]': '1'
        })        
        response = self.client.post(reverse('Web:GetOrder'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数           

    def test_getorder_goodid_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[goodid]': '1'
        })        
        response = self.client.post(reverse('Web:GetOrder'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数  

    def test_getorder_agentid_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[agentid]': '1'
        })        
        response = self.client.post(reverse('Web:GetOrder'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数  

    def test_getorder_generalSearch_is_not_none_and_ordercolumn_is_goodtitle(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalOrderSearch]': '商品1',
            'query[ordercolumn]': 'goodtitle',
        })        
        response = self.client.post(reverse('Web:GetOrder'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数    

    def test_getorder_generalSearch_is_not_none_and_ordercolumn_is_orderid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalOrderSearch]': '737709442123689270',
            'query[ordercolumn]': 'orderid',
        })        
        response = self.client.post(reverse('Web:GetOrder'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数     

    def test_getorder_generalSearch_is_not_none_and_ordercolumn_is_agentname(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalOrderSearch]': 'bLevel',
            'query[ordercolumn]': 'agentname',
        })        
        response = self.client.post(reverse('Web:GetOrder'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数                               
    
    def test_getorder_orderStatus_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[orderStatus]': '12,'
        })        
        response = self.client.post(reverse('Web:GetOrder'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数  
    
    def test_getorder_createtime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[createtime]': '1,'
        })        
        response = self.client.post(reverse('Web:GetOrder'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数      
    # end 订单管理

    # begin 提现管理
    def test_cashmanage(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:CashManage'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/MyAgent/CashManage.html')  # 判断渲染的模板是否正确  

    def test_createagentapplyforwithdraw_money_is_0(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'money': '0'
        }      
        response = self.client.post(reverse('Web:CreateAgentApplyForWithdraw'), data=param)  
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        msg = response_json['msg']
        self.assertEqual(msg, '金额不能为0') # 判断数据   

    def test_createagentapplyforwithdraw_money_is_more_than_1(self):
        self.client.login(username=self.blevel_user_username, password=self.blevel_user_password)
        param = {
            'money': '1.1'
        }      
        response = self.client.post(reverse('Web:CreateAgentApplyForWithdraw'), data=param)  
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        msg = response_json['msg']
        self.assertEqual(msg, '金额不能超过1.00元') # 判断数据      

    def test_createagentapplyforwithdraw_money_is_less_than_1_and_is_not_super_user(self):
        self.client.login(username=self.blevel_user_username, password=self.blevel_user_password)
        param = {
            'money': '0.5'
        }      
        response = self.client.post(reverse('Web:CreateAgentApplyForWithdraw'), data=param)  
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        msg = response_json['msg']
        self.assertEqual(msg, reverse('Web:AgentWithdraw')) # 判断数据   
        user = User.objects.get(username='bLevel')
        self.assertEqual(user.money, 0.5) # 判断数据 
        agentapplyforwithdrawlist = AgentApplyForWithdraw.objects.all()
        self.assertEqual(agentapplyforwithdrawlist.count(), 2) # 判断数据条数      

    def test_getagentapplyforwithdraw_generalSearch_is_not_none_and_cashmanagecolumn_is_username(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalCashManageSearch]': 'aLevel',
            'query[cashmanagecolumn]': 'username',
        })        
        response = self.client.post(reverse('Web:GetAgentApplyForWithdraw'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数    

    def test_getagentapplyforwithdraw_generalSearch_is_not_none_and_cashmanagecolumn_is_leader(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalCashManageSearch]': 'bLevel',
            'query[cashmanagecolumn]': 'leader',
        })        
        response = self.client.post(reverse('Web:GetAgentApplyForWithdraw'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数  

    def test_getagentapplyforwithdraw_generalSearch_is_not_none_and_cashmanagecolumn_is_truename(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalCashManageSearch]': 'truename',
            'query[cashmanagecolumn]': 'truename',
        })        
        response = self.client.post(reverse('Web:GetAgentApplyForWithdraw'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数  

    def test_getagentapplyforwithdraw_generalSearch_is_not_none_and_cashmanagecolumn_is_phone(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalCashManageSearch]': '123',
            'query[cashmanagecolumn]': 'phone',
        })        
        response = self.client.post(reverse('Web:GetAgentApplyForWithdraw'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数                                               
    
    def test_getagentapplyforwithdraw_status_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[status]': '0,',
        })        
        response = self.client.post(reverse('Web:GetAgentApplyForWithdraw'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数  
    
    def test_passagentapplyforwithdraw(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'id': '1'
        }         
        response = self.client.post(reverse('Web:PassAgentApplyForWithdraw'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:CashManage'))  # 判断跳转
        agentapplyforwithdraw = AgentApplyForWithdraw.objects.get(id=1)
        self.assertEqual(agentapplyforwithdraw.IsPass, 1) # 判断数据 
    
    def test_notpassagentapplyforwithdraw(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'id': '1'
        }         
        response = self.client.post(reverse('Web:NotPassAgentApplyForWithdraw'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:CashManage'))  # 判断跳转
        agentapplyforwithdraw = AgentApplyForWithdraw.objects.get(id=1)
        self.assertEqual(agentapplyforwithdraw.IsPass, 2) # 判断数据 
        self.assertEqual(agentapplyforwithdraw.Agent.Subscriber.money, 1) # 判断数据
     
    # end 提现管理

    # begin 任务模板
    def test_missionplantemplate(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:MissionPlanTemplate'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/MissionManage/MissionPlanTemplate.html')  # 判断渲染的模板是否正确  

    def test_getmissionplantemplate(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()      
        response = self.client.post(reverse('Web:GetMissionPlanTemplate'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数    

    def test_delete_missionplantemplate_by_ids(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'ids': '1,'
        }         
        response = self.client.post(reverse('Web:DeleteMissionPlanTemplate'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:MissionPlanTemplate'))  # 判断跳转
        missionplantemplatelist = MissionPlanTemplate.objects.all()
        self.assertEqual(missionplantemplatelist.count(), 0) # 判断数据条数     

    def test_createmissionplantemplate(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'name': '测试模板2'
        }         
        response = self.client.post(reverse('Web:CreateMissionPlanTemplate'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        missionplantemplatelist = MissionPlanTemplate.objects.all()
        self.assertEqual(missionplantemplatelist.count(), 2) # 判断数据条数  

    def test_getdevicebytemplateid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'id': '1'
        }         
        response = self.client.post(reverse('Web:GetDeviceByTemplateID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, '1') # 判断数据 
        mobilephoneid_result = response_json['mobilephoneid']
        self.assertEqual(mobilephoneid_result, '1') # 判断数据  

    def test_deliverdevice(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'deviceid': '2',
            'id': '1'
        }         
        response = self.client.post(reverse('Web:DeliverDevice'), data=param)
        mobile = MobilePhone.objects.get(id=2)
        self.assertEqual(mobile.MissionPlanTemplate.id, 1) # 判断数据  

    # end 任务模板

    # begin 编辑任务模板
    def test_editmissionplantemplate(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:EditMissionPlanTemplate'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/MissionManage/EditMissionPlanTemplate.html')  # 判断渲染的模板是否正确  
    
    def test_editmissionplantemplatebyid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.get('/EditMissionPlanTemplate/1/')
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/MissionManage/EditMissionPlanTemplate.html')  # 判断渲染的模板是否正确  
    
    def test_delete_event_by_ids_eventtype_is_养号任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'eventtype': '养号任务',
            'dataid': '1'
        }         
        response = self.client.post(reverse('Web:DeleteEvent'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        maintenancenumbermissionplanlist = MaintenanceNumberMissionPlan.objects.all()
        self.assertEqual(maintenancenumbermissionplanlist.count(), 0) # 判断数据条数     

    def test_delete_event_by_ids_eventtype_is_刷粉任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'eventtype': '刷粉任务',
            'dataid': '1'
        }         
        response = self.client.post(reverse('Web:DeleteEvent'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        scanmissionplanlist = ScanMissionPlan.objects.all()
        self.assertEqual(scanmissionplanlist.count(), 0) # 判断数据条数

    def test_delete_event_by_ids_eventtype_is_关注任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'eventtype': '关注任务',
            'dataid': '1'
        }         
        response = self.client.post(reverse('Web:DeleteEvent'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        followmissionplanlist = FollowMissionPlan.objects.all()
        self.assertEqual(followmissionplanlist.count(), 0) # 判断数据条数

    def test_delete_event_by_ids_eventtype_is_刷宝任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'eventtype': '刷宝任务',
            'dataid': '1'
        }         
        response = self.client.post(reverse('Web:DeleteEvent'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        treasuremissionplanlist = TreasureMissionPlan.objects.all()
        self.assertEqual(treasuremissionplanlist.count(), 0) # 判断数据条数                     
    
    def test_createevent_eventtype_is_养号任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'eventtype': '养号任务',
            'templateid': '1',
            'strattime_str': '2019-12-25 16:00:00',
        }         
        response = self.client.post(reverse('Web:CreateEvent'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        maintenancenumbermissionplanlist = MaintenanceNumberMissionPlan.objects.all()
        self.assertEqual(maintenancenumbermissionplanlist.count(), 2) # 判断数据条数     

    def test_createevent_eventtype_is_刷粉任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'eventtype': '刷粉任务',
            'templateid': '1',
            'strattime_str': '2019-12-25 16:00:00',
        }         
        response = self.client.post(reverse('Web:CreateEvent'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        scanmissionplanlist = ScanMissionPlan.objects.all()
        self.assertEqual(scanmissionplanlist.count(), 2) # 判断数据条数     

    def test_createevent_eventtype_is_关注任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'eventtype': '关注任务',
            'templateid': '1',
            'strattime_str': '2019-12-25 16:00:00',
        }         
        response = self.client.post(reverse('Web:CreateEvent'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        followmissionplanlist = FollowMissionPlan.objects.all()
        self.assertEqual(followmissionplanlist.count(), 2) # 判断数据条数     

    def test_createevent_eventtype_is_刷宝任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'eventtype': '刷宝任务',
            'templateid': '1',
            'strattime_str': '2019-12-25 16:00:00',
        }         
        response = self.client.post(reverse('Web:CreateEvent'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        treasuremissionplanlist = TreasureMissionPlan.objects.all()
        self.assertEqual(treasuremissionplanlist.count(), 2) # 判断数据条数     

    def test_geteventsbytemplateid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'templateid': 1,
        }
        response = self.client.post(reverse('Web:GetEventsByTemplateID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        self.assertEqual(len(response_json), 4) # 判断数据条数                                        
       
    def test_geteventbyid_eventtype_is_养号任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'eventtype': '养号任务',
            'dataid': '1',
        }         
        response = self.client.post(reverse('Web:GetEventByID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, 1) # 判断数据 
        type_result = response_json['type']
        self.assertEqual(type_result, '养号任务') # 判断数据    

    def test_geteventbyid_eventtype_is_刷粉任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'eventtype': '刷粉任务',
            'dataid': '1',
        }         
        response = self.client.post(reverse('Web:GetEventByID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, 1) # 判断数据 
        type_result = response_json['type']
        self.assertEqual(type_result, '刷粉任务') # 判断数据

    def test_geteventbyid_eventtype_is_关注任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'eventtype': '关注任务',
            'dataid': '1',
        }         
        response = self.client.post(reverse('Web:GetEventByID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, 1) # 判断数据 
        type_result = response_json['type']
        self.assertEqual(type_result, '关注任务') # 判断数据

    def test_geteventbyid_eventtype_is_刷宝任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'eventtype': '刷宝任务',
            'dataid': '1',
        }         
        response = self.client.post(reverse('Web:GetEventByID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, 1) # 判断数据 
        type_result = response_json['type']
        self.assertEqual(type_result, '刷宝任务') # 判断数据                      
    
    def test_editevent_eventtype_is_养号任务_and_endtime_str_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'eventtype': '养号任务',
            'dataid': '1',
            'strattime_str': '2019-12-26 16:00:00',
            'endtime_str': '2019-12-26 18:00:00',
        }         
        response = self.client.post(reverse('Web:EditEvent'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        maintenancenumbermissionplan = MaintenanceNumberMissionPlan.objects.get(id=1)  
        self.assertEqual(maintenancenumbermissionplan.StartTime, datetime.datetime(2019, 12, 26, 16, 0)) # 判断数据
        self.assertEqual(maintenancenumbermissionplan.EndTime, datetime.datetime(2019, 12, 26, 18, 0)) # 判断数据

    def test_editevent_eventtype_is_养号任务_and_endtime_str_is_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'eventtype': '养号任务',
            'dataid': '1',
            'strattime_str': '2019-12-26 16:00:00',
            'endtime_str': '',
        }         
        response = self.client.post(reverse('Web:EditEvent'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        maintenancenumbermissionplan = MaintenanceNumberMissionPlan.objects.get(id=1)  
        self.assertEqual(maintenancenumbermissionplan.StartTime, datetime.datetime(2019, 12, 26, 16, 0)) # 判断数据
        self.assertEqual(maintenancenumbermissionplan.EndTime, datetime.datetime(2019, 12, 26, 17, 0)) # 判断数据

    def test_editevent_eventtype_is_刷粉任务_and_endtime_str_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'eventtype': '刷粉任务',
            'dataid': '1',
            'strattime_str': '2019-12-26 16:00:00',
            'endtime_str': '2019-12-26 18:00:00',
        }         
        response = self.client.post(reverse('Web:EditEvent'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        scanmissionplan = ScanMissionPlan.objects.get(id=1)  
        self.assertEqual(scanmissionplan.StartTime, datetime.datetime(2019, 12, 26, 16, 0)) # 判断数据
        self.assertEqual(scanmissionplan.EndTime, datetime.datetime(2019, 12, 26, 18, 0)) # 判断数据

    def test_editevent_eventtype_is_刷粉任务_and_endtime_str_is_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'eventtype': '刷粉任务',
            'dataid': '1',
            'strattime_str': '2019-12-26 16:00:00',
            'endtime_str': '',
        }         
        response = self.client.post(reverse('Web:EditEvent'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        scanmissionplan = ScanMissionPlan.objects.get(id=1)  
        self.assertEqual(scanmissionplan.StartTime, datetime.datetime(2019, 12, 26, 16, 0)) # 判断数据
        self.assertEqual(scanmissionplan.EndTime, datetime.datetime(2019, 12, 26, 17, 0)) # 判断数据        
      
    def test_editevent_eventtype_is_关注任务_and_endtime_str_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'eventtype': '关注任务',
            'dataid': '1',
            'strattime_str': '2019-12-26 16:00:00',
            'endtime_str': '2019-12-26 18:00:00',
        }         
        response = self.client.post(reverse('Web:EditEvent'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        followmissionplan = FollowMissionPlan.objects.get(id=1)  
        self.assertEqual(followmissionplan.StartTime, datetime.datetime(2019, 12, 26, 16, 0)) # 判断数据
        self.assertEqual(followmissionplan.EndTime, datetime.datetime(2019, 12, 26, 18, 0)) # 判断数据

    def test_editevent_eventtype_is_关注任务_and_endtime_str_is_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'eventtype': '关注任务',
            'dataid': '1',
            'strattime_str': '2019-12-26 16:00:00',
            'endtime_str': '',
        }         
        response = self.client.post(reverse('Web:EditEvent'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        followmissionplan = FollowMissionPlan.objects.get(id=1)  
        self.assertEqual(followmissionplan.StartTime, datetime.datetime(2019, 12, 26, 16, 0)) # 判断数据
        self.assertEqual(followmissionplan.EndTime, datetime.datetime(2019, 12, 26, 17, 0)) # 判断数据  

    def test_editevent_eventtype_is_刷宝任务_and_endtime_str_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'eventtype': '刷宝任务',
            'dataid': '1',
            'strattime_str': '2019-12-26 16:00:00',
            'endtime_str': '2019-12-26 18:00:00',
        }         
        response = self.client.post(reverse('Web:EditEvent'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        treasuremissionplan = TreasureMissionPlan.objects.get(id=1)  
        self.assertEqual(treasuremissionplan.StartTime, datetime.datetime(2019, 12, 26, 16, 0)) # 判断数据
        self.assertEqual(treasuremissionplan.EndTime, datetime.datetime(2019, 12, 26, 18, 0)) # 判断数据

    def test_editevent_eventtype_is_刷宝任务_and_endtime_str_is_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'eventtype': '刷宝任务',
            'dataid': '1',
            'strattime_str': '2019-12-26 16:00:00',
            'endtime_str': '',
        }         
        response = self.client.post(reverse('Web:EditEvent'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        treasuremissionplan = TreasureMissionPlan.objects.get(id=1)  
        self.assertEqual(treasuremissionplan.StartTime, datetime.datetime(2019, 12, 26, 16, 0)) # 判断数据
        self.assertEqual(treasuremissionplan.EndTime, datetime.datetime(2019, 12, 26, 17, 0)) # 判断数据             
    
    def test_editeventdetail_eventtype_is_养号任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)    
        maintenancenumbermissionplan = MaintenanceNumberMissionPlan.objects.get(id=1)  
        self.assertIsNone(maintenancenumbermissionplan.Description) # 判断数据           
        param = {
            'eventtype': '养号任务',
            'dataid': '1',
            'description': '新描述',
        }         
        response = self.client.post(reverse('Web:EditEventDetail'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        maintenancenumbermissionplan = MaintenanceNumberMissionPlan.objects.get(id=1)  
        self.assertEqual(maintenancenumbermissionplan.Description, '新描述') # 判断数据

    def test_editeventdetail_eventtype_is_刷粉任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)    
        scanmissionplan = ScanMissionPlan.objects.get(id=1)  
        self.assertIsNone(scanmissionplan.Description) # 判断数据   
        self.assertEqual(scanmissionplan.PeopleLimit, 0) # 判断数据
        self.assertEqual(scanmissionplan.Interval, 0) # 判断数据
        self.assertFalse(scanmissionplan.FanSexIsMale) # 判断数据
        self.assertIsNone(scanmissionplan.CommentTextID) # 判断数据        
        param = {
            'eventtype': '刷粉任务',
            'dataid': '1',
            'description': '新描述',
            'peoplelimit': '10',
            'interval': '10',
            'fansexismale': 'true',
            'commenttext': '评论库1'
        }         
        response = self.client.post(reverse('Web:EditEventDetail'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        scanmissionplan = ScanMissionPlan.objects.get(id=1)  
        self.assertEqual(scanmissionplan.Description, '新描述') # 判断数据 
        self.assertEqual(scanmissionplan.PeopleLimit, 10) # 判断数据
        self.assertEqual(scanmissionplan.Interval, 10) # 判断数据  
        self.assertTrue(scanmissionplan.FanSexIsMale) # 判断数据
        self.assertEqual(scanmissionplan.CommentTextID, '1') # 判断数据              
    
    def test_editeventdetail_eventtype_is_关注任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)    
        followmissionplan = FollowMissionPlan.objects.get(id=1)  
        self.assertIsNone(followmissionplan.Description) # 判断数据   
        self.assertEqual(followmissionplan.PeopleLimit, 0) # 判断数据
        self.assertFalse(followmissionplan.FanSexIsMale) # 判断数据      
        param = {
            'eventtype': '关注任务',
            'dataid': '1',
            'description': '新描述',
            'peoplelimit': '10',
            'fansexismale': 'true',
        }         
        response = self.client.post(reverse('Web:EditEventDetail'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        followmissionplan = FollowMissionPlan.objects.get(id=1)  
        self.assertEqual(followmissionplan.Description, '新描述') # 判断数据 
        self.assertEqual(followmissionplan.PeopleLimit, 10) # 判断数据
        self.assertTrue(followmissionplan.FanSexIsMale) # 判断数据     
    
    def test_editeventdetail_eventtype_is_刷宝任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)    
        treasuremissionplan = TreasureMissionPlan.objects.get(id=1)  
        self.assertIsNone(treasuremissionplan.Description) # 判断数据           
        param = {
            'eventtype': '刷宝任务',
            'dataid': '1',
            'description': '新描述',
        }         
        response = self.client.post(reverse('Web:EditEventDetail'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        treasuremissionplan = TreasureMissionPlan.objects.get(id=1)  
        self.assertEqual(treasuremissionplan.Description, '新描述') # 判断数据    
    # end 编辑任务模板

    # begin 全部任务
    def test_allmissions(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:AllMissions'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/MissionManage/AllMissions.html')  # 判断渲染的模板是否正确   

    def test_getallmissions(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'pagination[page]': 1,
            'pagination[pages]': 10,
            'pagination[perpage]': 100,
        }   
        response = self.client.post(reverse('Web:GetAllMissions'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 32) # 判断数据条数         

    def test_getallmissions_generalSearch_is_not_none_and_ordercolumn_is_tiktok(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalAllMissionsSearch]': 'noShowWindowExists',
            'query[allmissioncolumn]': 'tiktok',
        })        
        response = self.client.post(reverse('Web:GetAllMissions'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 0) # 判断数据条数    

    def test_getallmissions_generalSearch_is_not_none_and_ordercolumn_is_id(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalAllMissionsSearch]': '1',
            'query[allmissioncolumn]': 'id',
        })        
        response = self.client.post(reverse('Web:GetAllMissions'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 10) # 判断数据条数    

    def test_getallmissions_missionName_is_视频任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[missionname]': '视频任务,',
        })        
        response = self.client.post(reverse('Web:GetAllMissions'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数 

    def test_getallmissions_missionName_is_互刷任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[missionname]': '互刷任务,',
        })        
        response = self.client.post(reverse('Web:GetAllMissions'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数  

    def test_getallmissions_missionName_is_养号任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[missionname]': '养号任务,',
        })        
        response = self.client.post(reverse('Web:GetAllMissions'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数  

    def test_getallmissions_missionName_is_刷粉任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[missionname]': '刷粉任务,',
        })        
        response = self.client.post(reverse('Web:GetAllMissions'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数  

    def test_getallmissions_missionName_is_关注任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[missionname]': '关注任务,',
        })        
        response = self.client.post(reverse('Web:GetAllMissions'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数  

    def test_getallmissions_missionName_is_刷宝任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[missionname]': '刷宝任务,',
        })        
        response = self.client.post(reverse('Web:GetAllMissions'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数  

    def test_getallmissions_missionName_is_观看直播任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[missionname]': '观看直播任务,',
        })        
        response = self.client.post(reverse('Web:GetAllMissions'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数       

    def test_getallmissions_missionName_is_修改签名任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[missionname]': '修改签名任务,',
        })        
        response = self.client.post(reverse('Web:GetAllMissions'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数                                                                  
 
    def test_getallmissions_status_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'pagination[page]': 1,
            'pagination[pages]': 10,
            'pagination[perpage]': 100,
            'query[allmissionstatus]': '0,1,',
        }
        response = self.client.post(reverse('Web:GetAllMissions'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 16) # 判断数据条数      
    
    def test_getallmissions_starttime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        param = {
            'pagination[page]': 1,
            'pagination[pages]': 10,
            'pagination[perpage]': 100,
            'query[starttime]': date,
        }
        response = self.client.post(reverse('Web:GetAllMissions'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 32) # 判断数据条数  

    def test_getallmissions_endtime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        param = {
            'pagination[page]': 1,
            'pagination[pages]': 10,
            'pagination[perpage]': 100,
            'query[endtime]': date,
        }
        response = self.client.post(reverse('Web:GetAllMissions'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 0) # 判断数据条数          
    
    def test_getallmissions_starttime_is_not_none_and_endtime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        startdate = datetime.datetime.now() - datetime.timedelta(days=1)
        enddate = datetime.datetime.now() + datetime.timedelta(days=1)        
        param = {
            'pagination[page]': 1,
            'pagination[pages]': 10,
            'pagination[perpage]': 100,
            'query[starttime]': startdate,
            'query[endtime]': enddate,
        }
        response = self.client.post(reverse('Web:GetAllMissions'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 32) # 判断数据条数            

    def test_delete_allmission_by_ids_missionname_is_视频任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)      
        param = {
            'id': '1',
            'missionname': '视频任务'
        }         
        response = self.client.post(reverse('Web:DeleteAllMissions'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:AllMissions'))  # 判断跳转
        videomissionlist = VideoMission.objects.all()
        self.assertEqual(videomissionlist.count(), 3) # 判断数据条数    

    def test_delete_allmission_by_ids_missionname_is_互刷任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)      
        param = {
            'id': '1',
            'missionname': '互刷任务'
        }         
        response = self.client.post(reverse('Web:DeleteAllMissions'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:AllMissions'))  # 判断跳转
        mutualbrushmissionlist = MutualBrushMission.objects.all()
        self.assertEqual(mutualbrushmissionlist.count(), 3) # 判断数据条数    

    def test_delete_allmission_by_ids_missionname_is_养号任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)      
        param = {
            'id': '1',
            'missionname': '养号任务'
        }         
        response = self.client.post(reverse('Web:DeleteAllMissions'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:AllMissions'))  # 判断跳转
        maintenancenumbermissionlist = MaintenanceNumberMission.objects.all()
        self.assertEqual(maintenancenumbermissionlist.count(), 3) # 判断数据条数   

    def test_delete_allmission_by_ids_missionname_is_刷粉任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)      
        param = {
            'id': '1',
            'missionname': '刷粉任务'
        }         
        response = self.client.post(reverse('Web:DeleteAllMissions'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:AllMissions'))  # 判断跳转
        scanmissionlist = ScanMission.objects.all()
        self.assertEqual(scanmissionlist.count(), 3) # 判断数据条数 

    def test_delete_allmission_by_ids_missionname_is_关注任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)      
        param = {
            'id': '1',
            'missionname': '关注任务'
        }         
        response = self.client.post(reverse('Web:DeleteAllMissions'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:AllMissions'))  # 判断跳转
        followmissionlist = FollowMission.objects.all()
        self.assertEqual(followmissionlist.count(), 3) # 判断数据条数            

    def test_delete_allmission_by_ids_missionname_is_刷宝任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)      
        param = {
            'id': '1',
            'missionname': '刷宝任务'
        }         
        response = self.client.post(reverse('Web:DeleteAllMissions'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:AllMissions'))  # 判断跳转
        treasuremissionlist = TreasureMission.objects.all()
        self.assertEqual(treasuremissionlist.count(), 3) # 判断数据条数    

    def test_delete_allmission_by_ids_missionname_is_观看直播任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)      
        param = {
            'id': '1',
            'missionname': '观看直播任务'
        }         
        response = self.client.post(reverse('Web:DeleteAllMissions'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:AllMissions'))  # 判断跳转
        watchlivemissionlist = WatchLiveMission.objects.all()
        self.assertEqual(watchlivemissionlist.count(), 3) # 判断数据条数      

    def test_delete_allmission_by_ids_missionname_is_修改签名任务(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)      
        param = {
            'id': '1',
            'missionname': '修改签名任务'
        }         
        response = self.client.post(reverse('Web:DeleteAllMissions'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:AllMissions'))  # 判断跳转
        changesignaturemissionlist = ChangeSignatureMission.objects.all()
        self.assertEqual(changesignaturemissionlist.count(), 3) # 判断数据条数
        account = TikTokAccount.objects.get(id=1)
        self.assertEqual(account.NewDescribe, '') # 判断数据条数                                       
    # end 全部任务

    # begin 挖宝任务
    def test_treasuremission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:TreasureMission'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/MissionManage/TreasureMission.html')  # 判断渲染的模板是否正确  

    def test_gettreasuremission_generalSearch_is_digit(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalTreasureMissionSearch]': '1',
        })
        response = self.client.post(reverse('Web:GetTreasureMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数           

    def test_gettreasuremission_generalSearch_is_str(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalTreasureMissionSearch]': 'a',
        })
        response = self.client.post(reverse('Web:GetTreasureMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数                   
    
    def test_gettreasuremission_status_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[treasuremissionstatus]': '0,1,',
        })
        response = self.client.post(reverse('Web:GetTreasureMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数      
    
    def test_gettreasuremission_starttime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        param = self.datatable_param.copy()
        param.update({
            'query[starttime]': date,
        })
        response = self.client.post(reverse('Web:GetTreasureMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数  

    def test_gettreasuremission_endtime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        param = self.datatable_param.copy()
        param.update({
            'query[endtime]': date,
        })
        response = self.client.post(reverse('Web:GetTreasureMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 0) # 判断数据条数          
    
    def test_gettreasuremission_starttime_is_not_none_and_endtime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        startdate = datetime.datetime.now() - datetime.timedelta(days=1)
        enddate = datetime.datetime.now() + datetime.timedelta(days=1)        
        param = self.datatable_param.copy()
        param.update({
            'query[starttime]': startdate,
            'query[endtime]': enddate,
        })
        response = self.client.post(reverse('Web:GetTreasureMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数          
      
    def test_delete_treasuremission_by_ids(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)      
        param = {
            'ids': '1,'
        }         
        response = self.client.post(reverse('Web:DeleteTreasureMission'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:TreasureMission'))  # 判断跳转
        treasuremissionlist = TreasureMission.objects.all()
        self.assertEqual(treasuremissionlist.count(), 3) # 判断数据条数     

    def test_createtreasuremission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)                               
        param = {
            'deviceid': '1',
            'starttime': '',
            'endtime': '',        
        }         
        response = self.client.post(reverse('Web:CreateTreasureMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        treasuremissionlist = TreasureMission.objects.all()
        self.assertEqual(treasuremissionlist.count(), 5) # 判断数据条数      

    def test_edittreasuremission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)                       
        param = {
            'id': 1,
            'starttime': '',
            'endtime': '',
        }         
        response = self.client.post(reverse('Web:EditTreasureMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
              
    def test_gettreasuremissionbyid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'id': 1,
        }
        response = self.client.post(reverse('Web:GetTreasureMissionByID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, 1) # 判断数据 
        status_result = response_json['status']
        self.assertEqual(status_result, 0) # 判断数据                                                           
  
    # end 挖宝任务

    # begin 代理我的收益
    def test_agentincome(self):
        self.client.login(username=self.blevel_user_username, password=self.blevel_user_password)
        response = self.client.post(reverse('Web:AgentIncome'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/Agent/AgentIncome.html')  # 判断渲染的模板是否正确  

    # end 代理我的收益

    # begin 代理余额提现
    def test_agentwithdraw(self):
        self.client.login(username=self.blevel_user_username, password=self.blevel_user_password)
        response = self.client.post(reverse('Web:AgentWithdraw'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/Agent/AgentWithdraw.html')  # 判断渲染的模板是否正确  

    def test_getagentwithdrawlist(self):
        self.client.login(username=self.alevel_user_username, password=self.alevel_user_password)
        param = self.datatable_param.copy()
        response = self.client.post(reverse('Web:GetAgentWithdrawList'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数           
        
    # end 代理余额提现

    # begin 代理账号数据
    def test_agentaccountdata(self):
        self.client.login(username=self.blevel_user_username, password=self.blevel_user_password)
        response = self.client.post(reverse('Web:AgentAccountData'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/Agent/AgentAccountData.html')  # 判断渲染的模板是否正确      

    def test_getagentaccountdata(self):
        self.client.login(username=self.blevel_user_username, password=self.blevel_user_password)
        param = {
            'num': 0
        }
        response = self.client.post(reverse('Web:GetAgentAccountData'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
    # end 代理账号数据

    # begin 观看直播任务
    def test_watchlivemission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:WatchLiveMission'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/MissionManage/WatchLiveMission.html')  # 判断渲染的模板是否正确  

    def test_getwatchlivemission_generalSearch_is_digit(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalWatchLiveMissionSearch]': '1',
        })
        response = self.client.post(reverse('Web:GetWatchLiveMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数           

    def test_getwatchlivemission_generalSearch_is_str(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalWatchLiveMissionSearch]': 'a',
        })
        response = self.client.post(reverse('Web:GetWatchLiveMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数                   
    
    def test_getwatchlivemission_status_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[watchlivemissionstatus]': '0,1,',
        })
        response = self.client.post(reverse('Web:GetWatchLiveMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数      
    
    def test_getwatchlivemission_starttime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        param = self.datatable_param.copy()
        param.update({
            'query[starttime]': date,
        })
        response = self.client.post(reverse('Web:GetWatchLiveMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数  

    def test_getwatchlivemission_endtime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        param = self.datatable_param.copy()
        param.update({
            'query[endtime]': date,
        })
        response = self.client.post(reverse('Web:GetWatchLiveMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 0) # 判断数据条数          
    
    def test_getwatchlivemission_starttime_is_not_none_and_endtime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        startdate = datetime.datetime.now() - datetime.timedelta(days=1)
        enddate = datetime.datetime.now() + datetime.timedelta(days=1)        
        param = self.datatable_param.copy()
        param.update({
            'query[starttime]': startdate,
            'query[endtime]': enddate,
        })
        response = self.client.post(reverse('Web:GetWatchLiveMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数          
      
    def test_delete_watchlivemission_by_ids(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)      
        param = {
            'ids': '1,'
        }         
        response = self.client.post(reverse('Web:DeleteWatchLiveMission'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:WatchLiveMission'))  # 判断跳转
        watchlivemissionlist = WatchLiveMission.objects.all()
        self.assertEqual(watchlivemissionlist.count(), 3) # 判断数据条数     

    def test_createwatchlivemission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)                               
        param = {
            'deviceid': '1,2',
            'starttime': '',
            'targeturl': '1',
            'commenttext': '#norepeatcommenttext1\n#norepeatcommenttext2\ncommenttext1\ncommenttext2',
            'missionincome': '1.00',
        }         
        response = self.client.post(reverse('Web:CreateWatchLiveMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        watchlivemissionlist = WatchLiveMission.objects.all()
        self.assertEqual(watchlivemissionlist.count(), 6) # 判断数据条数     
        watchlivemission1 = WatchLiveMission.objects.get(id=5)  
        watchlivemission2 = WatchLiveMission.objects.get(id=6)          
        self.assertEqual(watchlivemission1.TargetURL, '1') # 判断数据  
        self.assertEqual(watchlivemission1.CommentText, 'commenttext1|commenttext2|#norepeatcommenttext1') # 判断数据  
        self.assertEqual(watchlivemission1.MissionIncome, 1.00) # 判断数据            
        self.assertEqual(watchlivemission2.TargetURL, '1') # 判断数据           
        self.assertEqual(watchlivemission2.CommentText, 'commenttext1|commenttext2|#norepeatcommenttext2') # 判断数据 
        self.assertEqual(watchlivemission2.MissionIncome, 1.00) # 判断数据                                          

    def test_editwatchlivemission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        mutualbrushmission = MutualBrushMission.objects.get(id=1)    
        self.assertIsNone(mutualbrushmission.VideoURL) # 判断数据          
        self.assertIsNone(mutualbrushmission.CommentText) # 判断数据                       
        param = {
            'id': mutualbrushmission.id,
            'starttime': '',
            'endtime': '',
            'targeturl': 'targeturl',
            'commenttext': 'commenttext1\ncommenttext2',
        }         
        response = self.client.post(reverse('Web:EditWatchLiveMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        watchlivemission = WatchLiveMission.objects.get(id=1)
        self.assertEqual(watchlivemission.TargetURL, 'targeturl') # 判断数据          
        self.assertEqual(watchlivemission.CommentText, 'commenttext1|commenttext2') # 判断数据            

    def test_getwatchlivemissionbyid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'id': 1,
        }
        response = self.client.post(reverse('Web:GetWatchLiveMissionByID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, 1) # 判断数据 
        status_result = response_json['status']
        self.assertEqual(status_result, 0) # 判断数据                                                      
                      
      
    # end 观看直播任务

    # begin 签名管理
    def test_signaturemanage(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:SignatureManage'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/SignatureManage/SignatureManagePage.html')  # 判断渲染的模板是否正确  

    def test_getsignaturemanage_generalSearch_and_signaturemanagecolumn_is_nickname(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalSignatureManageSearch]': 'has',
            'query[signaturemanagecolumn]': 'nickname'
        })
        response = self.client.post(reverse('Web:GetSignatureManage'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数        

    def test_getsignaturemanage_generalSearch_and_signaturemanagecolumn_is_mobileid_digit(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalSignatureManageSearch]': '2',
            'query[signaturemanagecolumn]': 'mobileid'
        })
        response = self.client.post(reverse('Web:GetSignatureManage'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数    

    def test_getsignaturemanage_generalSearch_and_signaturemanagecolumn_is_mobileid_str(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalSignatureManageSearch]': 'a',
            'query[signaturemanagecolumn]': 'mobileid'
        })
        response = self.client.post(reverse('Web:GetSignatureManage'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 3) # 判断数据条数                   
  
    def test_getsignaturemanagebyid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'id': 1,
        }
        response = self.client.post(reverse('Web:GetSignatureManageByID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, 1) # 判断数据 
        newdescribe_result = response_json['newdescribe']
        self.assertEqual(newdescribe_result, 'NewDescribe') # 判断数据     
           
    def test_createchangesignaturemission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)                               
        param = {
            'deviceid': '1',
            'id': '1',
            'newdescribe': 'newnewdescribe',
        }         
        response = self.client.post(reverse('Web:CreateChangeSignatureMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        changesignaturemissionlist = ChangeSignatureMission.objects.all()
        self.assertEqual(changesignaturemissionlist.count(), 5) # 判断数据条数     
        changesignaturemission = ChangeSignatureMission.objects.get(id=5)        
        self.assertEqual(changesignaturemission.TikTokAccount.id, 1) # 判断数据  
        self.assertEqual(changesignaturemission.TikTokAccount.NewDescribe, 'newnewdescribe') # 判断数据 
        self.assertEqual(changesignaturemission.Describe, changesignaturemission.TikTokAccount.Describe) # 判断数据
        self.assertEqual(changesignaturemission.NewDescribe, changesignaturemission.TikTokAccount.NewDescribe) # 判断数据  
        self.assertEqual(changesignaturemission.MobilePhone.id, 1) # 判断数据 

    def test_muticreatechangesignaturemission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)                               
        param = {
            'accountids': '1,2,',
            'newdescribe': 'newnewdescribe',
        }         
        response = self.client.post(reverse('Web:MutiCreateChangeSignatureMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        changesignaturemissionlist = ChangeSignatureMission.objects.all()
        self.assertEqual(changesignaturemissionlist.count(), 5) # 判断数据条数     
        changesignaturemission1 = ChangeSignatureMission.objects.get(id=6)           
        self.assertEqual(changesignaturemission1.TikTokAccount.id, 2) # 判断数据  
        self.assertEqual(changesignaturemission1.TikTokAccount.NewDescribe, 'newnewdescribe') # 判断数据 
        self.assertEqual(changesignaturemission1.Describe, changesignaturemission1.TikTokAccount.Describe) # 判断数据
        self.assertEqual(changesignaturemission1.NewDescribe, changesignaturemission1.TikTokAccount.NewDescribe) # 判断数据  
        self.assertEqual(changesignaturemission1.MobilePhone.id, 3) # 判断数据                                                               
           
    # end 签名管理

    # begin 修改签名任务
    def test_changesignaturemission(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:ChangeSignatureMission'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/MissionManage/ChangeSignatureMissionPage.html')  # 判断渲染的模板是否正确  

    def test_getchangesignaturemission_generalSearch_is_digit(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalChangeSignatureMissionSearch]': '1',
        })
        response = self.client.post(reverse('Web:GetChangeSignatureMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数           

    def test_getchangesignaturemission_generalSearch_is_str(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[generalChangeSignatureMissionSearch]': 'a',
        })
        response = self.client.post(reverse('Web:GetChangeSignatureMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数                   
    
    def test_getchangesignaturemission_status_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[changesignaturemissionstatus]': '0,1,',
        })
        response = self.client.post(reverse('Web:GetChangeSignatureMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数      
    
    def test_getchangesignaturemission_starttime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        param = self.datatable_param.copy()
        param.update({
            'query[starttime]': date,
        })
        response = self.client.post(reverse('Web:GetChangeSignatureMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数  

    def test_getchangesignaturemission_endtime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        param = self.datatable_param.copy()
        param.update({
            'query[endtime]': date,
        })
        response = self.client.post(reverse('Web:GetChangeSignatureMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 0) # 判断数据条数          
    
    def test_getchangesignaturemission_starttime_is_not_none_and_endtime_is_not_none(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        startdate = datetime.datetime.now() - datetime.timedelta(days=1)
        enddate = datetime.datetime.now() + datetime.timedelta(days=1)        
        param = self.datatable_param.copy()
        param.update({
            'query[starttime]': startdate,
            'query[endtime]': enddate,
        })
        response = self.client.post(reverse('Web:GetChangeSignatureMission'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 4) # 判断数据条数          

    def test_getchangesignaturemission_group_is_int(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[group]': '1,',
        })
        response = self.client.post(reverse('Web:GetSignatureManage'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数   

    def test_getchangesignaturemission_group_is_none_type(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        param.update({
            'query[group]': '-1,',
        })
        response = self.client.post(reverse('Web:GetSignatureManage'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 2) # 判断数据条数                 

    def test_delete_changesignaturemission_by_ids(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)      
        param = {
            'ids': '1,'
        }         
        response = self.client.post(reverse('Web:DeleteChangeSignatureMission'), data=param)
        self.assertEqual(response.status_code, 302)  # 判断状态码
        self.assertEqual(response.url, reverse('Web:ChangeSignatureMission'))  # 判断跳转
        changesignaturemissionlist = ChangeSignatureMission.objects.all()
        self.assertEqual(changesignaturemissionlist.count(), 3) # 判断数据条数
        account = TikTokAccount.objects.get(id=1)
        self.assertEqual(account.NewDescribe, '') # 判断数据条数

 
    # end 修改签名任务

    # begin 设备分配
    def test_devicedeliver(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        response = self.client.post(reverse('Web:DeviceDeliver'))
        self.assertEqual(response.status_code, 200)  # 判断状态码
        self.assertTemplateUsed(response, 'pages/DeviceManage/DeviceDeliver.html')  # 判断渲染的模板是否正确  

    def test_getdevicedeliver(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = self.datatable_param.copy()
        response = self.client.post(reverse('Web:GetDeviceDeliver'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        data_list = response_json['data']
        self.assertEqual(len(data_list), 1) # 判断数据条数    

    def test_userdevicedeliver(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)
        param = {
            'deviceid': '2',
            'id': '2'
        }         
        response = self.client.post(reverse('Web:UserDeviceDeliver'), data=param)
        mobile = MobilePhone.objects.get(id=2)
        self.assertEqual(mobile.Owner.id, 2) # 判断数据  

    def test_getdevicebyuserid(self):
        self.client.login(username=self.super_user_username, password=self.super_user_password)       
        param = {
            'id': '1'
        }         
        response = self.client.post(reverse('Web:GetDeviceByUserID'), data=param)
        self.assertEqual(response.status_code, 200)  # 判断状态码
        response_str = str(response.content,'utf-8')
        response_json = json.loads(response_str)
        id_result = response_json['dataid']
        self.assertEqual(id_result, '1') # 判断数据 
        mobilephoneid_result = response_json['mobilephoneid']
        self.assertEqual(mobilephoneid_result, '1,2,3,4') # 判断数据  
    # end 设备分配