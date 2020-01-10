# -*- coding: utf-8 -*-
from django.db import models
from Users.models import User
from .my_enum import *
from django.db.models import Q
import datetime


class TikTokAccountGroup(models.Model):
    Name = models.TextField(verbose_name='分组名字', max_length=150, null=False)
    Owner = models.ForeignKey(User, verbose_name='拥有者',
                              on_delete=models.CASCADE, null=True)


class TikTokAccount(models.Model):
    UserID = models.TextField(verbose_name='抖音UID', max_length=150, null=True)
    NickName = models.TextField(verbose_name='昵称', max_length=150, null=True)
    TikTokID = models.TextField(verbose_name='抖音号', max_length=150, null=True)
    Describe = models.TextField(verbose_name='描述', max_length=150, null=True)
    Attention = models.IntegerField(verbose_name='关注', null=False, default=0)
    Fans = models.IntegerField(verbose_name='粉丝', null=False, default=0)
    Praise = models.IntegerField(verbose_name='赞', null=False, default=0)
    Video = models.IntegerField(verbose_name='作品数', null=False, default=0)
    NumOfPraiseToOther = models.IntegerField(
        verbose_name='喜欢', null=False, default=0)
    ShareURL = models.TextField(verbose_name='短链接', max_length=150, null=False, default='')
    ShowWindowExists = models.BooleanField(
        verbose_name='是否电商', null=False, default=False)
    UpdateTime = models.DateTimeField(verbose_name='更新日期', null=True)
    Remark = models.TextField(verbose_name='备注', max_length=150, null=True)
    Group = models.ForeignKey(TikTokAccountGroup, verbose_name='分组',
                              on_delete=models.SET_NULL, null=True)
    IP = models.TextField(verbose_name='IP地址', max_length=150, null=True)
    Area = models.TextField(verbose_name='地区', max_length=150, null=True)
    Classification = models.ManyToManyField(
        'MaintenanceNumberMissionKeywordClassification', verbose_name='标签')
    BindURL = models.TextField(
        verbose_name='绑定主播URL', max_length=150, null=True)
    BindID = models.TextField(verbose_name='绑定主播ID', max_length=150, null=True)
    BindLongURL = models.TextField(
        verbose_name='绑定主播长链接', max_length=150, null=True)
    BindNickName = models.TextField(
        verbose_name='绑定主播昵称', max_length=150, null=True)
    NewDescribe = models.TextField(verbose_name='新描述', max_length=150, null=True)      
    Owner = models.ForeignKey(User, verbose_name='拥有者',
                              on_delete=models.CASCADE, null=True)      

    def GetSystemConfig(self, name):
        config = SystemConfig.objects.filter(Name=name)
        if config is not None and config.count() > 0:
            value = config.first().Value
            return int(value)
        else:
            return 1

    def GetClassificationString(self):
        if self.Classification is not None and self.Classification.all().count() > 0:
            ClassificationList = self.Classification.all()
            ClassificationString = ''
            for i in range(len(ClassificationList)):
                per = ClassificationList[i]
                ClassificationString = ClassificationString + per.Name + ','
            return ClassificationString[:-1]
        else:
            return ''

    def GetClassificationId(self):
        if self.Classification is not None and self.Classification.all().count() > 0:
            ClassificationList = self.Classification.all().values()
            ClassificationId = ''
            for i in range(len(ClassificationList)):
                per = ClassificationList[i]
                ClassificationId = ClassificationId + str(per["id"]) + ','
            return ClassificationId[:-1]
        else:
            return ''

    def GetTodayVideoCount(self):
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=1)
        my_filter = Q()
        my_filter = my_filter & Q(CreateTime__range=(start_date, end_date))
        my_filter = my_filter & Q(MobilePhone__TikTokAccount=self)
        return VideoMission.objects.filter(my_filter).count()

    def GetTodayGoodsCount(self):
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=1)
        my_filter = Q()
        my_filter = my_filter & Q(CreateTime__range=(start_date, end_date))
        my_filter = my_filter & Q(MobilePhone__TikTokAccount=self)
        my_filter = my_filter & ~Q(Video__Goods=None)
        return VideoMission.objects.filter(my_filter).count()

    def GetPID(self):
        if self.mobilephone_set is not None and self.mobilephone_set.count() > 0:
            mobilephone = self.mobilephone_set.first()
            if mobilephone.ALIConfig is not None:
                return mobilephone.ALIConfig.PID
            else:
                return ''
        else:
            return ''

    def GetIsOnline(self):
        isonline_second = self.GetSystemConfig('心跳存活判断秒数')
        if self.mobilephone_set is not None and self.mobilephone_set.count() > 0:
            mobilephone = self.mobilephone_set.first()
            starttime = datetime.datetime.now()
            endtime = starttime - datetime.timedelta(seconds=isonline_second)
            if mobilephone.HeartBeat is not None and mobilephone.HeartBeat > endtime:
                return True
            else:
                return False
        else:
            return False


class GoodClassification(models.Model):
    Name = models.TextField(verbose_name='商品分类名', max_length=150, null=False)
    Owner = models.ForeignKey(User, verbose_name='拥有者',
                              on_delete=models.CASCADE, null=True)


class Goods(models.Model):
    Pic1 = models.TextField(verbose_name='图片1', null=True)
    Pic2 = models.TextField(verbose_name='图片2', null=True)
    Pic3 = models.TextField(verbose_name='图片3', null=True)
    Pic4 = models.TextField(verbose_name='图片4', null=True)
    Pic5 = models.TextField(verbose_name='图片5', null=True)
    Title = models.TextField(verbose_name='标题', max_length=150, null=False)
    OutSidePlatformID = models.TextField(
        verbose_name='外部ID', max_length=150, null=False)
    Price = models.DecimalField(
        verbose_name='售价', max_digits=18, decimal_places=2, null=False, default=0)
    Sales = models.IntegerField(verbose_name='淘宝销量', null=False, default=0)
    CommissionPercent = models.DecimalField(
        verbose_name='佣金比例', max_digits=18, decimal_places=2, default=0)
    OutSidePlatformURL = models.TextField(
        verbose_name='外部URL', max_length=150, null=True)
    CreateTime = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    GoodClassifications = models.ManyToManyField(GoodClassification)
    Owner = models.ForeignKey(User, verbose_name='拥有者',
                              on_delete=models.CASCADE, null=True)
    SubTitle = models.TextField(
        verbose_name='短标题', max_length=150, null=False, default='')

    def GetCategoryString(self):
        if self.GoodClassifications.all().count() > 0:
            CategoryList = self.GoodClassifications.all().values()
            CategoryString = ''
            for i in range(len(CategoryList)):
                Category = CategoryList[i]
                CategoryString = CategoryString + Category["Name"] + ','
            return CategoryString[:-1]
        else:
            return ''

    def GetCategoryId(self):
        if self.GoodClassifications.all().count() > 0:
            CategoryList = self.GoodClassifications.all().values()
            CategoryId = ''
            for i in range(len(CategoryList)):
                Category = CategoryList[i]
                CategoryId = CategoryId + str(Category["id"]) + ','
            return CategoryId[:-1]
        else:
            return ''

    def GetUnusedVideoCount(self):
        video_filter = Q()
        video_filter = video_filter & Q(Goods=self)
        video_filter = video_filter & Q(videomission=None)
        video_list = Videos.objects.filter(video_filter)
        return video_list.count()
 
    def GetUnusedVideoIDList(self):
        video_filter = Q()
        video_filter = video_filter & Q(Goods=self)
        video_filter = video_filter & Q(videomission=None)
        video_list = Videos.objects.filter(video_filter)
        return list(video_list.values_list('id', flat=True))


class VideoClassification(models.Model):
    Name = models.TextField(verbose_name='视频分类名', max_length=150, null=False)
    Owner = models.ForeignKey(User, verbose_name='拥有者',
                              on_delete=models.CASCADE, null=True)


class Videos(models.Model):
    Title = models.TextField(verbose_name='标题', max_length=150, null=True)
    URL = models.FileField(verbose_name='视频文件',
                           upload_to='videos/%Y/%m/%d/', null=True)
    CreateTime = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    Remark = models.TextField(verbose_name='备注', max_length=150, null=True)
    VideoClassifications = models.ManyToManyField(VideoClassification)
    Owner = models.ForeignKey(User, verbose_name='拥有者',
                              on_delete=models.CASCADE, null=True)
    Goods = models.ForeignKey(Goods, verbose_name='商品',
                              on_delete=models.SET_NULL, null=True)
    VideoKeyword = models.TextField(
        verbose_name='视频话题', max_length=150, null=True)
    FileName = models.TextField(verbose_name='文件名', max_length=150, null=True)              

    def GetCategoryString(self):
        if self.VideoClassifications.all().count() > 0:
            CategoryList = self.VideoClassifications.all().values()
            CategoryString = ''
            for i in range(len(CategoryList)):
                Category = CategoryList[i]
                CategoryString = CategoryString + Category["Name"] + ','
            return CategoryString[:-1]
        else:
            return ''

    def GetCategoryId(self):
        if self.VideoClassifications.all().count() > 0:
            CategoryList = self.VideoClassifications.all().values()
            CategoryId = ''
            for i in range(len(CategoryList)):
                Category = CategoryList[i]
                CategoryId = CategoryId + str(Category["id"]) + ','
            return CategoryId[:-1]
        else:
            return ''

    def GetCommodityName(self):
        if self.Goods is not None:
            return self.Goods.Title
        else:
            return ''

    def GetCommodityId(self):
        if self.Goods is not None:
            return self.Goods.id
        else:
            return ''

    def GetVideoStatus(self):
        missions = VideoMission.objects.filter(Video=self, Status=2)
        if missions.count() > 0:
            return True
        else:
            return False


class Works(models.Model):
    TikTokAccount = models.ForeignKey(
        TikTokAccount, verbose_name='作者', on_delete=models.CASCADE)
    ShareURL = models.TextField(verbose_name='短链接', max_length=150, null=True)
    VideoID = models.TextField(verbose_name='视频ID', max_length=150, null=True)
    NumOfPraiseGet = models.IntegerField(
        verbose_name='点赞量', null=False, default=0)
    NumOfComments = models.IntegerField(
        verbose_name='评论量', null=False, default=0)
    NumOfShare = models.IntegerField(verbose_name='分享量', null=False, default=0)
    UpdateTime = models.DateTimeField(verbose_name='更新日期', null=True)
    Video = models.ForeignKey(Videos, verbose_name='关联视频',
                              on_delete=models.SET_NULL, null=True)
    Pic = models.TextField(verbose_name='视频封面', max_length=150, null=True)
    Describe = models.TextField(verbose_name='视频描述', max_length=150, null=True)
    LongURL = models.TextField(verbose_name='长链接', max_length=150, null=True)
    NumOfPlay = models.IntegerField(verbose_name='播放量', null=False, default=0)
    UploadTime = models.DateTimeField(verbose_name='视频上传日期', null=False)


class Agent(models.Model):
    Subscriber = models.ForeignKey(User, verbose_name='用户',
                                   on_delete=models.CASCADE, null=False, related_name='Subscriber')
    UserSystem = models.ForeignKey(User, verbose_name='顶级用户',
                                   on_delete=models.CASCADE, null=False, related_name='UserSystem')
    UserALevel = models.ForeignKey(User, verbose_name='上级用户',
                                   on_delete=models.CASCADE, null=True, related_name='UserALevel')
    UserBLevel = models.ForeignKey(User, verbose_name='上上级用户',
                                   on_delete=models.CASCADE, null=True, related_name='UserBLevel')
    UserSystemPercent = models.DecimalField(
        verbose_name='顶级用户提成', max_digits=18, decimal_places=2, null=False, default=0)
    UserALevelPercent = models.DecimalField(
        verbose_name='上级用户提成', max_digits=18, decimal_places=2, null=False, default=0)
    UserBLevelPercent = models.DecimalField(
        verbose_name='上上级用户提成', max_digits=18, decimal_places=2, null=False, default=0)


class ALIConfig(models.Model):
    NickName = models.TextField(verbose_name='昵称', max_length=150, null=True)
    PID = models.TextField(
        verbose_name='PID', max_length=150, null=False, default='')
    Remark = models.TextField(verbose_name='备注', max_length=150, null=True)
    Status = models.IntegerField(
        verbose_name='状态', null=False, choices=ALIStatus, default=0)
    Category = models.ManyToManyField(GoodClassification)
    LASTPID = models.TextField(
        verbose_name='LASTPID', max_length=150, null=False, default='')
    Owner = models.ForeignKey(User, verbose_name='拥有者',
                              on_delete=models.CASCADE, null=True)        

    def GetCategoryString(self):
        if self.Category.all().count() > 0:
            CategoryList = self.Category.all().values()
            CategoryString = ''
            for i in range(len(CategoryList)):
                Category = CategoryList[i]
                CategoryString = CategoryString + Category["Name"] + ','
            return CategoryString[:-1]
        else:
            return ''

    def GetCategoryId(self):
        if self.Category.all().count() > 0:
            CategoryList = self.Category.all().values()
            CategoryId = ''
            for i in range(len(CategoryList)):
                Category = CategoryList[i]
                CategoryId = CategoryId + str(Category["id"]) + ','
            return CategoryId[:-1]
        else:
            return ''


class MobilePhone(models.Model):
    IMEI = models.TextField(verbose_name='IMEI码', max_length=150, null=False)
    TikTokAccount = models.ForeignKey(
        TikTokAccount, verbose_name='抖音账号', on_delete=models.SET_NULL, null=True)
    SysID = models.CharField(verbose_name='GUID', max_length=64, null=False)
    Enable = models.BooleanField(
        verbose_name='是否可用', null=False, default=False)
    StatusInfo = models.TextField(
        verbose_name='状态信息', max_length=150, null=True)
    Agent = models.ForeignKey(Agent, verbose_name='代理',
                              on_delete=models.SET_NULL, null=True)
    ALIConfig = models.ForeignKey(ALIConfig, verbose_name='阿里妈妈配置',
                                  on_delete=models.SET_NULL, null=True)
    Remark = models.TextField(verbose_name='备注', max_length=500, null=True)
    HeartBeat = models.DateTimeField(verbose_name='心跳时间', null=True)
    MissionPlanTemplate = models.ForeignKey('MissionPlanTemplate', verbose_name='计划任务模板',
                                            on_delete=models.SET_NULL, null=True)
    Owner = models.ForeignKey(User, verbose_name='拥有者',
                              on_delete=models.CASCADE, null=True)                                            


class VideoMission(models.Model):
    MobilePhone = models.ForeignKey(
        MobilePhone, verbose_name='手机ID', on_delete=models.SET_NULL, null=True)
    Status = models.IntegerField(
        verbose_name='状态', null=False, choices=TaskStatus, default=0)
    Owner = models.ForeignKey(User, verbose_name='拥有者',
                              on_delete=models.SET_NULL, null=True)
    VideoURL = models.TextField(verbose_name='视频地址', max_length=150, null=True)
    VideoTitle = models.TextField(
        verbose_name='视频标题', max_length=150, null=True)
    VideoKeyword = models.TextField(
        verbose_name='视频话题', max_length=150, null=True)
    GoodURL = models.TextField(
        verbose_name='最终商品地址', max_length=500, null=True)
    GoodTitle = models.TextField(
        verbose_name='商品标题', max_length=150, null=True)
    GoodCategory = models.TextField(
        verbose_name='商品类别', max_length=150, null=True)
    Video = models.ForeignKey(
        Videos, verbose_name='关联视频ID', on_delete=models.SET_NULL, null=True)
    CreateTime = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    UpdateTime = models.DateTimeField(verbose_name='更新日期', auto_now=True)
    StartTime = models.DateTimeField(verbose_name='任务开始日期', null=False)
    Priority = models.IntegerField(
        verbose_name='优先级', null=False, default=0)
    FailReason = models.TextField(verbose_name='失败原因', null=True)

    def Relaunch(self):
        self.Status = 0
        self.FailReason = ''
        now = datetime.datetime.now()
        self.StartTime = now
        self.save()


class MutualBrushMission(models.Model):
    MobilePhone = models.ForeignKey(
        MobilePhone, verbose_name='手机ID', on_delete=models.SET_NULL, null=True)
    Status = models.IntegerField(
        verbose_name='状态', null=False, choices=TaskStatus, default=0)
    Owner = models.ForeignKey(User, verbose_name='拥有者',
                              on_delete=models.SET_NULL, null=True)
    VideoURL = models.TextField(verbose_name='视频地址', max_length=150, null=True)
    IsLike = models.BooleanField(
        verbose_name='是否点赞', null=False, default=False)
    IsFollow = models.BooleanField(
        verbose_name='是否关注', null=False, default=False)        
    CommentText = models.TextField(
        verbose_name='评论内容', max_length=500, null=True)
    CreateTime = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    UpdateTime = models.DateTimeField(verbose_name='更新日期', auto_now=True)
    StartTime = models.DateTimeField(verbose_name='任务开始日期', null=False)
    Priority = models.IntegerField(
        verbose_name='优先级', null=False, default=0)
    FailReason = models.TextField(verbose_name='失败原因', null=True)
    MissionIncome = models.DecimalField(verbose_name='任务收益',
        max_digits=18, decimal_places=2, null=False, default=0) 
    IsCalc = models.BooleanField(
        verbose_name='任务收益是否已统计', null=False, default=False)
    CalcDate = models.DateTimeField(verbose_name='任务收益统计日期', null=True)    


class CommentLibrary(models.Model):
    Text = models.TextField(verbose_name='评论内容', max_length=150, null=True)
    CreateTime = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    Owner = models.ForeignKey(User, verbose_name='拥有者',
                              on_delete=models.CASCADE, null=True)    


class MaintenanceNumberMissionKeywordClassification(models.Model):
    Name = models.TextField(verbose_name='养号任务关键字类别',
                            max_length=150, null=False)
    Owner = models.ForeignKey(User, verbose_name='拥有者',
                              on_delete=models.CASCADE, null=True)


class MaintenanceNumberMissionKeyword(models.Model):
    Name = models.TextField(verbose_name='养号任务关键字', max_length=150, null=False)
    Classification = models.ForeignKey(MaintenanceNumberMissionKeywordClassification, verbose_name='类别',
                                       on_delete=models.SET_NULL, null=True)
    Owner = models.ForeignKey(User, verbose_name='拥有者',
                              on_delete=models.CASCADE, null=True)                                       


class MaintenanceNumberMission(models.Model):
    MobilePhone = models.ForeignKey(
        MobilePhone, verbose_name='手机ID', on_delete=models.SET_NULL, null=True)
    Status = models.IntegerField(
        verbose_name='状态', null=False, choices=TaskStatus, default=0)
    Owner = models.ForeignKey(User, verbose_name='拥有者',
                              on_delete=models.SET_NULL, null=True)
    CreateTime = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    UpdateTime = models.DateTimeField(verbose_name='更新日期', auto_now=True)
    StartTime = models.DateTimeField(verbose_name='任务开始日期', null=False)
    EndTime = models.DateTimeField(verbose_name='任务结束日期', null=True)
    Priority = models.IntegerField(
        verbose_name='优先级', null=False, default=0)
    FailReason = models.TextField(verbose_name='失败原因', null=True)

    def GetCategoryString(self):
        if self.MobilePhone is not None and self.MobilePhone.TikTokAccount is not None:
            return self.MobilePhone.TikTokAccount.GetClassificationString()
        else:
            return ''

    def GetCategoryId(self):
        if self.Keyword.all().count() > 0:
            KeywordList = self.Keyword.all().values()
            KeywordId = ''
            for i in range(len(KeywordList)):
                per = KeywordList[i]
                KeywordId = KeywordId + str(per["id"]) + ','
            return KeywordId[:-1]
        else:
            return ''


class ScanMission(models.Model):
    MobilePhone = models.ForeignKey(
        MobilePhone, verbose_name='手机ID', on_delete=models.SET_NULL, null=True)
    Status = models.IntegerField(
        verbose_name='状态', null=False, choices=TaskStatus, default=0)
    Owner = models.ForeignKey(User, verbose_name='拥有者',
                              on_delete=models.SET_NULL, null=True)
    PeopleLimit = models.IntegerField(
        verbose_name='刷粉人数上限', null=False, default=0)
    Interval = models.IntegerField(verbose_name='间隔', null=False, default=0)
    FanSexIsMale = models.BooleanField(
        verbose_name='粉丝性别男', null=False, default=False)
    FanSexIsFemale = models.BooleanField(
        verbose_name='粉丝性别女', null=False, default=False)
    FanSexIsNone = models.BooleanField(
        verbose_name='粉丝性别无', null=False, default=False)
    CreateTime = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    UpdateTime = models.DateTimeField(verbose_name='更新日期', auto_now=True)
    StartTime = models.DateTimeField(verbose_name='任务开始日期', null=False)
    EndTime = models.DateTimeField(verbose_name='任务结束日期', null=True)
    Priority = models.IntegerField(
        verbose_name='优先级', null=False, default=0)
    CommentTextID = models.TextField(
        verbose_name='评论库ID字符串', max_length=150, null=True)
    FailReason = models.TextField(verbose_name='失败原因', null=True)
    IsDirectional = models.BooleanField(
        verbose_name='是否定向', null=False, default=False)    

    def GetCommentText(self):
        if self.CommentTextID is not None and len(self.CommentTextID) > 0:
            commenttext = ''
            CommentTextID_list = self.CommentTextID.split(',')
            for i in range(len(CommentTextID_list)):
                commenttextid = CommentTextID_list[i]
                commentlibrary = CommentLibrary.objects.filter(
                    id=commenttextid)
                if commentlibrary.count() > 0:
                    text = commentlibrary.first().Text
                    commenttext = commenttext + text + '\n'
            return commenttext
        else:
            return ''


class FollowMission(models.Model):
    MobilePhone = models.ForeignKey(
        MobilePhone, verbose_name='手机ID', on_delete=models.SET_NULL, null=True)
    Status = models.IntegerField(
        verbose_name='状态', null=False, choices=TaskStatus, default=0)
    Owner = models.ForeignKey(User, verbose_name='拥有者',
                              on_delete=models.SET_NULL, null=True)
    PeopleLimit = models.IntegerField(
        verbose_name='关注人数上限', null=False, default=0)
    FanSexIsMale = models.BooleanField(
        verbose_name='粉丝性别男', null=False, default=False)
    FanSexIsFemale = models.BooleanField(
        verbose_name='粉丝性别女', null=False, default=False)
    FanSexIsNone = models.BooleanField(
        verbose_name='粉丝性别无', null=False, default=False)
    CreateTime = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    UpdateTime = models.DateTimeField(verbose_name='更新日期', auto_now=True)
    StartTime = models.DateTimeField(verbose_name='任务开始日期', null=False)
    EndTime = models.DateTimeField(verbose_name='任务结束日期', null=True)
    Priority = models.IntegerField(
        verbose_name='优先级', null=False, default=0)
    FailReason = models.TextField(verbose_name='失败原因', null=True)


class Order(models.Model):
    TB_Paid_Time = models.DateTimeField(null=True)
    TK_Paid_Time = models.DateTimeField(null=True)
    Pay_Price = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, default=0)
    Pub_Share_Fee = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, default=0)
    TK_Earning_Time = models.DateTimeField(null=True)
    ADZone_ID = models.TextField(max_length=150, null=True)
    Pub_Share_Rate = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, default=0)
    Trade_ID = models.TextField(max_length=150, null=True)
    Subsidy_Rate = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, default=0)
    TK_Total_Rate = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, default=0)
    Item_Img = models.TextField(max_length=150, null=True)
    Pub_Share_Pre_Fee = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, default=0)
    Alipay_Total_Price = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, default=0)
    Item_Title = models.TextField(max_length=150, null=True)
    Subsidy_Fee = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, default=0)
    Alimama_Share_Fee = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, default=0)
    Trade_Parent_ID = models.TextField(max_length=150, null=True)
    Order_Type = models.TextField(max_length=150, null=True)
    TK_Create_Time = models.DateTimeField(null=True)
    TK_Status = models.IntegerField(null=False, default=0)
    Item_Price = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, default=0)
    Item_ID = models.TextField(max_length=150, null=True)
    ADZone_Name = models.TextField(max_length=150, null=True)
    Total_Commission_Rate = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, default=0)
    Item_Link = models.TextField(max_length=500, null=True)
    Site_ID = models.TextField(max_length=150, null=True)
    Income_Rate = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, default=0)
    Total_Commission_Fee = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, default=0)
    UpdateTime = models.DateTimeField(verbose_name='更新日期', auto_now=True)
    Alimama_Rate = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, default=0)
    Click_Time = models.DateTimeField(null=True)
    Deposit_Price = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, default=0)
    Flow_Source = models.TextField(max_length=150, null=True)
    Item_Category_Name = models.TextField(max_length=150, null=True)
    Item_Num = models.IntegerField(null=False, default=0)
    Pub_ID = models.TextField(max_length=150, null=True)
    Refund_Tag = models.IntegerField(null=False, default=0)
    Seller_Nick = models.TextField(max_length=150, null=True)
    Seller_Shop_Title = models.TextField(max_length=150, null=True)
    Site_Name = models.TextField(max_length=150, null=True)
    Subsidy_Type = models.TextField(max_length=150, null=True)
    TB_Deposit_Time = models.TextField(max_length=150, null=True)
    Terminal_Type = models.TextField(max_length=150, null=True)
    TK_Commission_Fee_For_Media_Platform = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, default=0)
    TK_Commission_Pre_Fee_For_Media_Platform = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, default=0)
    TK_Commission_Rate_For_Media_Platform = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, default=0)
    TK_Deposit_Time = models.TextField(max_length=150, null=True)
    TK_Order_Role = models.IntegerField(null=False, default=2)
    ALIConfig = models.ForeignKey(ALIConfig, verbose_name='阿里妈妈配置',
                                  on_delete=models.SET_NULL, null=True)
    Goods = models.ForeignKey(Goods, verbose_name='商品',
                              on_delete=models.SET_NULL, null=True)
    IsCalc = models.BooleanField(
        verbose_name='是否已统计', null=False, default=False)    
    CalcDate = models.DateField(verbose_name='统计日期', null=True)        


class Refund(models.Model):
    Order = models.ForeignKey(
        Order, verbose_name='订单ID', on_delete=models.CASCADE, null=False)
    TB_Trade_Parent_ID = models.TextField(max_length=150, null=True)
    TK_Subsidy_Fee_Refund3rd_Pub = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, default=0)
    TK_Commission_Fee_Refund3rd_Pub = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, default=0)
    TK_Subsidy_Fee_Refund_Pub = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, default=0)
    TK_Commission_Fee_Refund_Pub = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, default=0)
    TK_Refund_Suit_Time = models.DateTimeField(null=True)
    TK_Refund_Time = models.DateTimeField(null=True)
    Earning_Time = models.DateTimeField(null=True)
    TB_Trade_Create_Time = models.DateTimeField(null=True)
    Refund_Status = models.IntegerField(null=False, default=0)
    TB_Auction_Title = models.TextField(max_length=150, null=True)
    Refund_Fee = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, default=0)
    UpdateTime = models.DateTimeField(verbose_name='更新日期', auto_now=True)


class MissionPlanTemplate(models.Model):
    Name = models.TextField(verbose_name='标题', max_length=150, null=True)
    RecordDate = models.DateField(verbose_name='记录日期', null=True)
    CreateTime = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    Owner = models.ForeignKey(User, verbose_name='拥有者',
                              on_delete=models.SET_NULL, null=True)


class MaintenanceNumberMissionPlan(models.Model):
    MissionPlanTemplate = models.ForeignKey(
        MissionPlanTemplate, verbose_name='模板ID', on_delete=models.CASCADE, null=True)
    Title = models.TextField(verbose_name='标题', max_length=150, null=True)
    Description = models.TextField(
        verbose_name='任务描述', max_length=150, null=True)
    StartTime = models.DateTimeField(verbose_name='任务开始日期', null=False)
    EndTime = models.DateTimeField(verbose_name='任务结束日期', null=True)


class ScanMissionPlan(models.Model):
    MissionPlanTemplate = models.ForeignKey(
        MissionPlanTemplate, verbose_name='模板ID', on_delete=models.CASCADE, null=True)
    Title = models.TextField(verbose_name='标题', max_length=150, null=True)
    Description = models.TextField(
        verbose_name='任务描述', max_length=150, null=True)
    PeopleLimit = models.IntegerField(
        verbose_name='刷粉人数上限', null=False, default=0)
    Interval = models.IntegerField(verbose_name='间隔', null=False, default=0)
    StartTime = models.DateTimeField(verbose_name='任务开始日期', null=False)
    EndTime = models.DateTimeField(verbose_name='任务结束日期', null=True)
    FanSexIsMale = models.BooleanField(
        verbose_name='粉丝性别男', null=False, default=False)
    FanSexIsFemale = models.BooleanField(
        verbose_name='粉丝性别女', null=False, default=False)
    FanSexIsNone = models.BooleanField(
        verbose_name='粉丝性别无', null=False, default=False)
    CommentTextID = models.TextField(
        verbose_name='评论库ID字符串', max_length=150, null=True)

    def GetCommentText(self):
        if self.CommentTextID is not None and len(self.CommentTextID) > 0:
            commenttext = ''
            CommentTextID_list = self.CommentTextID.split(',')
            for i in range(len(CommentTextID_list)):
                commenttextid = CommentTextID_list[i]
                commentlibrary = CommentLibrary.objects.filter(
                    id=commenttextid)
                if commentlibrary.count() > 0:
                    text = commentlibrary.first().Text
                    commenttext = commenttext + text + '\n'
            return commenttext
        else:
            return ''


class FollowMissionPlan(models.Model):
    MissionPlanTemplate = models.ForeignKey(
        MissionPlanTemplate, verbose_name='模板ID', on_delete=models.CASCADE, null=True)
    Title = models.TextField(verbose_name='标题', max_length=150, null=True)
    Description = models.TextField(
        verbose_name='任务描述', max_length=150, null=True)
    PeopleLimit = models.IntegerField(
        verbose_name='关注人数上限', null=False, default=0)
    StartTime = models.DateTimeField(verbose_name='任务开始日期', null=False)
    EndTime = models.DateTimeField(verbose_name='任务结束日期', null=True)
    FanSexIsMale = models.BooleanField(
        verbose_name='粉丝性别男', null=False, default=False)
    FanSexIsFemale = models.BooleanField(
        verbose_name='粉丝性别女', null=False, default=False)
    FanSexIsNone = models.BooleanField(
        verbose_name='粉丝性别无', null=False, default=False)


class SystemConfig(models.Model):
    Name = models.TextField(verbose_name='字段', max_length=150, null=True)
    Value = models.TextField(verbose_name='值', max_length=150, null=True)


class TaoBaoSession(models.Model):
    Owner = models.ForeignKey(User, verbose_name='拥有者',
                              on_delete=models.CASCADE, null=True)
    SessionKey = models.TextField(
        verbose_name='授权码', max_length=500, null=True)
    Ext_Time = models.BigIntegerField(
        verbose_name='授权有效期毫秒数', null=False, default=0)
    Ext_Date = models.DateTimeField(verbose_name='授权有效期', null=False)
    TaoBao_User_ID = models.TextField(
        verbose_name='淘宝USERID', max_length=150, null=True)
    TaoBao_User_NickName = models.TextField(
        verbose_name='淘宝昵称', max_length=150, null=True)


class PIDDaySummary(models.Model):
    ALIConfig = models.ForeignKey(
        ALIConfig, verbose_name='PID', on_delete=models.SET_NULL, null=True)
    Summary_Date = models.DateField(verbose_name='统计日期', null=False)
    Paid_Order_Count = models.IntegerField(
        verbose_name='付款笔数', null=False, default=0)
    Paid_Pre_Fee = models.DecimalField(
        verbose_name='付款预估收入', max_digits=18, decimal_places=2, null=True, default=0)
    Earn_Pre_Fee = models.DecimalField(
        verbose_name='结算预估收入', max_digits=18, decimal_places=2, null=True, default=0)


class WorksDaySummary(models.Model):
    Work = models.ForeignKey(
        Works, verbose_name='抖音视频', on_delete=models.CASCADE)
    Summary_Date = models.DateField(verbose_name='统计日期', null=False)
    NumOfPraiseGet = models.IntegerField(
        verbose_name='点赞量', null=False, default=0)
    NumOfComments = models.IntegerField(
        verbose_name='评论量', null=False, default=0)
    NumOfShare = models.IntegerField(verbose_name='分享量', null=False, default=0)
    NumOfPlay = models.IntegerField(verbose_name='播放量', null=False, default=0)


class TikTokAccountDaySummary(models.Model):
    TikTokAccount = models.ForeignKey(
        TikTokAccount, verbose_name='抖音账号', on_delete=models.CASCADE)
    Summary_Date = models.DateField(verbose_name='统计日期', null=False)
    Attention = models.IntegerField(verbose_name='关注', null=False, default=0)
    Fans = models.IntegerField(verbose_name='粉丝', null=False, default=0)
    Praise = models.IntegerField(verbose_name='赞', null=False, default=0)
    Video = models.IntegerField(verbose_name='作品数', null=False, default=0)
    NumOfPraiseToOther = models.IntegerField(
        verbose_name='喜欢', null=False, default=0)


class CommodityDataAnalysis(models.Model):
    Goods = models.ForeignKey(Goods, verbose_name='商品',
                              on_delete=models.SET_NULL, null=True)
    WorksCount = models.IntegerField(
        verbose_name='视频数量', null=False, default=0)
    NumOfPraiseGet = models.IntegerField(
        verbose_name='点赞', null=False, default=0)
    NumOfComments = models.IntegerField(
        verbose_name='评论', null=False, default=0)
    NumOfShare = models.IntegerField(verbose_name='分享', null=False, default=0)
    NumOfPlay = models.IntegerField(verbose_name='播放', null=False, default=0)
    TodayOrder = models.IntegerField(
        verbose_name='今天销量', null=False, default=0)
    YestodayOrder = models.IntegerField(
        verbose_name='昨天销量', null=False, default=0)
    MonthOrder = models.IntegerField(
        verbose_name='本月销量', null=False, default=0)
    Owner = models.ForeignKey(User, verbose_name='拥有者',
                              on_delete=models.CASCADE, null=True)                                    


class WorksDataAnalysis(models.Model):
    Works = models.ForeignKey(
        Works, verbose_name='作品', on_delete=models.CASCADE)
    NumOfPraiseGet = models.IntegerField(
        verbose_name='点赞量', null=False, default=0)
    NumOfComments = models.IntegerField(
        verbose_name='评论量', null=False, default=0)
    NumOfShare = models.IntegerField(verbose_name='分享量', null=False, default=0)
    NumOfPlay = models.IntegerField(verbose_name='播放量', null=False, default=0)
    Owner = models.ForeignKey(User, verbose_name='拥有者',
                              on_delete=models.CASCADE, null=True)                                


class TikTokAccountDataAnalysis(models.Model):
    TikTokAccount = models.ForeignKey(
        TikTokAccount, verbose_name='抖音账号', on_delete=models.CASCADE)
    Summary_Date = models.DateField(verbose_name='统计日期', null=False)
    Attention = models.IntegerField(verbose_name='关注', null=False, default=0)
    Fans = models.IntegerField(verbose_name='粉丝', null=False, default=0)
    Praise = models.IntegerField(verbose_name='赞', null=False, default=0)
    Video = models.IntegerField(verbose_name='作品数', null=False, default=0)
    NumOfPraiseToOther = models.IntegerField(
        verbose_name='喜欢', null=False, default=0)
    TotalNumOfPlay = models.IntegerField(verbose_name='总播放量', null=False, default=0)
    FirstWorkNumOfPlay = models.IntegerField(
        verbose_name='作品1播放量', null=False, default=0)
    AttentionIncrease = models.IntegerField(verbose_name='关注增量', null=False, default=0)
    FansIncrease = models.IntegerField(verbose_name='粉丝增量', null=False, default=0)
    PraiseIncrease = models.IntegerField(verbose_name='赞增量', null=False, default=0)
    NumOfPraiseToOtherIncrease = models.IntegerField(
        verbose_name='喜欢增量', null=False, default=0)
    TotalNumOfPlayIncrease = models.IntegerField(verbose_name='总播放量增量', null=False, default=0)
    FirstWorkNumOfPlayIncrease = models.IntegerField(
        verbose_name='作品1播放量增量', null=False, default=0)   
    TotalNumOfComments = models.IntegerField(verbose_name='总评论量', null=False, default=0)
    TotalNumOfCommentsIncrease = models.IntegerField(verbose_name='评论增量', null=False, default=0)   
    Owner = models.ForeignKey(User, verbose_name='拥有者',
                              on_delete=models.CASCADE, null=True)                                            


class AgentMonthRealityIncome(models.Model):
    Agent = models.ForeignKey(Agent, verbose_name='代理',
                              on_delete=models.SET_NULL, null=True)    
    SummaryDate = models.DateField(verbose_name='统计日期', null=False)
    OrderMoney = models.DecimalField(verbose_name='结算金额',
        max_digits=18, decimal_places=2, null=False, default=0)      
    OrderCount = models.IntegerField(
        verbose_name='结算订单量', null=False, default=0)     
    MissionMoney = models.DecimalField(verbose_name='任务金额',
        max_digits=18, decimal_places=2, null=False, default=0)       
    TotalMoney = models.DecimalField(verbose_name='总金额',
        max_digits=18, decimal_places=2, null=False, default=0)     
    MutualBrushMissionCount = models.IntegerField(
        verbose_name='互刷任务量', null=False, default=0)
    WatchLiveMissionCount = models.IntegerField(
        verbose_name='观看直播任务量', null=False, default=0)                                     


class AgentApplyForWithdraw(models.Model):
    Agent = models.ForeignKey(Agent, verbose_name='代理',
                              on_delete=models.SET_NULL, null=True) 
    ApplyDate = models.DateTimeField(verbose_name='申请日期', null=False)    
    Money = models.DecimalField(verbose_name='申请金额',
        max_digits=18, decimal_places=2, null=False, default=0)   
    IsPass = models.IntegerField(
        verbose_name='是否通过', null=False, default=0)      
    ApproveDate = models.DateTimeField(verbose_name='审批日期', null=True)        
    ApproveUser = models.ForeignKey(User, verbose_name='审批人',
                              on_delete=models.SET_NULL, null=True)         
    Remark = models.TextField(verbose_name='备注', max_length=150, null=True)


class AllMissions(models.Model):
    class Meta:
        managed = False
        db_table = "VAllMissions"
    MissionName = models.TextField(verbose_name='任务名', max_length=150, null=True)
    Status = models.IntegerField(verbose_name='状态', null=False, choices=TaskStatus, default=0)
    CreateTime = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    StartTime = models.DateTimeField(verbose_name='任务开始日期', null=False)
    EndTime = models.DateTimeField(verbose_name='任务结束日期', null=True)
    FailReason = models.TextField(verbose_name='失败原因', null=True)
    MobilePhone_id = models.IntegerField(verbose_name='设备id', null=False, default=0)   
    NickName = models.TextField(verbose_name='抖音账号', max_length=150, null=True)
    Owner_id = models.IntegerField(verbose_name='拥有者id', null=False, default=0)  


class TreasureMission(models.Model):
    MobilePhone = models.ForeignKey(
        MobilePhone, verbose_name='手机ID', on_delete=models.SET_NULL, null=True)
    Status = models.IntegerField(
        verbose_name='状态', null=False, choices=TaskStatus, default=0)
    Owner = models.ForeignKey(User, verbose_name='拥有者',
                              on_delete=models.SET_NULL, null=True)
    CreateTime = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    UpdateTime = models.DateTimeField(verbose_name='更新日期', auto_now=True)
    StartTime = models.DateTimeField(verbose_name='任务开始日期', null=False)
    EndTime = models.DateTimeField(verbose_name='任务结束日期', null=True)
    Priority = models.IntegerField(
        verbose_name='优先级', null=False, default=0)
    FailReason = models.TextField(verbose_name='失败原因', null=True)


class TreasureMissionPlan(models.Model):
    MissionPlanTemplate = models.ForeignKey(
        MissionPlanTemplate, verbose_name='模板ID', on_delete=models.CASCADE, null=True)
    Title = models.TextField(verbose_name='标题', max_length=150, null=True)
    Description = models.TextField(
        verbose_name='任务描述', max_length=150, null=True)
    StartTime = models.DateTimeField(verbose_name='任务开始日期', null=False)
    EndTime = models.DateTimeField(verbose_name='任务结束日期', null=True)


class WatchLiveMission(models.Model):
    MobilePhone = models.ForeignKey(
        MobilePhone, verbose_name='手机ID', on_delete=models.SET_NULL, null=True)
    Status = models.IntegerField(
        verbose_name='状态', null=False, choices=TaskStatus, default=0)
    Owner = models.ForeignKey(User, verbose_name='拥有者',
                              on_delete=models.SET_NULL, null=True)
    TargetURL = models.TextField(verbose_name='目标主播链接', max_length=150, null=True)
    CommentText = models.TextField(
        verbose_name='评论内容', max_length=500, null=True)
    CommentTimes = models.IntegerField(
        verbose_name='评论次数', null=False, default=0)        
    CreateTime = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    UpdateTime = models.DateTimeField(verbose_name='更新日期', auto_now=True)
    StartTime = models.DateTimeField(verbose_name='任务开始日期', null=False)
    EndTime = models.DateTimeField(verbose_name='任务结束日期', null=False)    
    Priority = models.IntegerField(
        verbose_name='优先级', null=False, default=0)
    FailReason = models.TextField(verbose_name='失败原因', null=True)
    MissionIncome = models.DecimalField(verbose_name='任务收益',
        max_digits=18, decimal_places=2, null=False, default=0) 
    IsCalc = models.BooleanField(
        verbose_name='任务收益是否已统计', null=False, default=False)
    CalcDate = models.DateTimeField(verbose_name='任务收益统计日期', null=True)


class ChangeSignatureMission(models.Model):
    MobilePhone = models.ForeignKey(
        MobilePhone, verbose_name='手机ID', on_delete=models.SET_NULL, null=True)
    Status = models.IntegerField(
        verbose_name='状态', null=False, choices=TaskStatus, default=0)
    Owner = models.ForeignKey(User, verbose_name='拥有者',
                              on_delete=models.SET_NULL, null=True)
    Describe = models.TextField(verbose_name='旧描述', max_length=150, null=True)  
    TikTokAccount = models.ForeignKey(
        TikTokAccount, verbose_name='抖音账号', on_delete=models.CASCADE, null=True)    
    NewDescribe = models.TextField(verbose_name='新描述', max_length=150, null=True)                              
    CreateTime = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    UpdateTime = models.DateTimeField(verbose_name='更新日期', auto_now=True)
    StartTime = models.DateTimeField(verbose_name='任务开始日期', null=False)
    Priority = models.IntegerField(
        verbose_name='优先级', null=False, default=0)
    FailReason = models.TextField(verbose_name='失败原因', null=True)


class TopUserRelations(models.Model):
    Subscriber = models.ForeignKey(User, verbose_name='用户',
                                   on_delete=models.CASCADE, null=False, related_name='TopUserRelationsSubscriber')
    Leader = models.ForeignKey(User, verbose_name='上级',
                                   on_delete=models.CASCADE, null=False, related_name='TopUserRelationsLeader')
              

class ScanVideoLibrary(models.Model):
    Keyword = models.TextField(verbose_name='关键字', null=False, default='')  
    VideoURL = models.TextField(verbose_name='目标视频URL', null=False, default='')  
    UseTime = models.DateTimeField(verbose_name='使用日期', null=True)    
    Status = models.IntegerField(
        verbose_name='状态', null=False, default=0)    