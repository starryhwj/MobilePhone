from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import copy
from django.urls import reverse
from .models import *
from .json_encode import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import top.api
import re
from .my_enum import *
from django.db.models import Q
import random
import math
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import time
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.db import connection
import decimal
from django.contrib.auth.hashers import make_password


location_init = {
    'IsMyAccountMenu': False,
    'IsCommodityManageMenu': False,
    'IsVideoManageMenu': False,
    'IsMyAgentMenu': False,
    'IsMissionMenu': False,
    'IsMyLabelMenu': False,
    'IsMutualBrushMissionSubMenu': False,
    'IsDataAnalysisMenu': False,
    'IsSignatureManageMenu': False,
    'IsDeviceManageMenu': False,    
    'IsIndexPage': False,
    'IsDeviceManagePage': False,
    'IsAccountDataAnalysisPage': False,
    'IsAccountListPage': False,
    'IsALIConfigPage': False,
    'IsAlreadySendVideoPage': False,
    'IsCommodityDataAnalysisPage': False,
    'IsCommodityMissionManagePage': False,
    'IsCommoditySelectionPage': False,
    'IsMyCommodityPage': False,
    'IsMyVideoPage': False,
    'IsOrderCollectPage': False,
    'IsPublishCommodityMissionPage': False,
    'IsWorksDataAnalysisPage': False,
    'IsVideoLabelPage': False,
    'IsVideoMissionPage': False,
    'IsCommodityCategoryPage': False,
    'IsPublishFollowMissionPage': False,
    'IsPublishMaintenanceNumberMissionPage': False,
    'IsPublishMutualBrushMissionPage': False,
    'IsPublishScanMissionPage': False,
    'IsCommentLibraryPage': False,
    'IsAgentVerifyPage': False,
    'IsAgentListPage': False,
    'IsMaintenanceNumberMissionKeywordPage': False,
    'IsMaintenanceNumberMissionKeywordClassificationPage': False,
    'IsOrderPage': False,
    'IsCashManagePage': False,
    'IsAccountGroupPage': False,
    'IsMissionPlanTemplatePage': False,
    'IsAgentDetailPage': False,
    'IsAllMissionsPage': False,
    'IsTreasureMissionPage': False,
    'IsAgentIncomePage': False,
    'IsAgentWithdrawPage': False,
    'IsAgentAccountDataPage': False,
    'IsWatchLiveMissionPage': False,
    'IsSignatureManagePage': False,
    'IsChangeSignatureMissionPage': False,
    'IsDeviceDeliverPage': False,
}

# 抖音用
headers = {
    'user-agent': 'ozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Mobile Safari/537.36',
}

# 淘宝API
taobao_appKey = '28119282'
taobao_appSecret = '39e5038c96d0d1135f25783ba0ef6585'

# 第三方高佣API
vekey = 'V00003235Y79583203'

# begin 公共接口
@method_decorator(csrf_exempt, name='dispatch')
def devicedatatable(request):
    device_data_url = request.build_absolute_uri(reverse('Web:GetDevice'))
    getdevicenamebyids_url = request.build_absolute_uri(
        reverse('Web:GetDeviceNameByIDs'))
    owner_id_list = []
    if request.user.username == 'admin':
        owner_id_list = GetOwnerIDList(request.user.id, owner_id_list)        
    else:
        owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)         
    classifications = MaintenanceNumberMissionKeywordClassification.objects.filter(Owner__in=owner_id_list).values('Name').distinct()
    groups = TikTokAccountGroup.objects.filter(Owner__in=owner_id_list).values('Name').distinct()
    owners = []
    for i in range(len(owner_id_list)):
        owner_id = owner_id_list[i]
        user = User.objects.get(id=owner_id)
        owners.append(user)    
    context = {'classifications': classifications, 'groups': groups,
               'device_data_url': device_data_url, 'getdevicenamebyids_url': getdevicenamebyids_url,
               'owners': owners}
    return render(request, 'pages/control/DeviceDatatable.html', context)


@method_decorator(csrf_exempt, name='dispatch')
def orderdatatable(request):
    order_data_url = request.build_absolute_uri(reverse('Web:GetOrder'))
    context = {'order_data_url': order_data_url}
    return render(request, 'pages/control/OrderDatatable.html', context)    
# end 公共接口

# begin 淘宝验证

def taobaoverify(request):
    return HttpResponse('f00c25378e73a2bbb92a9a1859fb7f05')

# end 淘宝验证


# begin 第三方API授权

def taobaoreouth(request):
    session = request.GET.get('session')
    ext_time = int(request.GET.get('ext_time'))
    taobao_user_id = request.GET.get('user_id')
    taobao_user_nick = request.GET.get('user_nick')
    owner_id = request.GET.get('state')
    owner = User.objects.get(id=owner_id)
    taobaoSession_list = TaoBaoSession.objects.filter(Owner=owner)
    if taobaoSession_list.count() > 0:
        taobaoSession = taobaoSession_list.first()
        taobaoSession.SessionKey = session
        taobaoSession.Ext_Time = ext_time
        taobaoSession.Ext_Date = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(ext_time))
        taobaoSession.TaoBao_User_ID = taobao_user_id
        taobaoSession.TaoBao_User_NickName = taobao_user_nick
        taobaoSession.save()
    else:
        taobaoSession = TaoBaoSession()
        taobaoSession.Owner = owner
        taobaoSession.SessionKey = session
        taobaoSession.Ext_Time = ext_time
        taobaoSession.Ext_Date = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(ext_time))
        taobaoSession.TaoBao_User_ID = taobao_user_id
        taobaoSession.TaoBao_User_NickName = taobao_user_nick
        taobaoSession.save()
    return HttpResponseRedirect(reverse('Web:index'))


def get_user_session_ext_Date(userid):
    taobaoSession_list = TaoBaoSession.objects.filter(Owner_id=userid)
    if taobaoSession_list.count() > 0:
        taobaoSession = taobaoSession_list.first()
        day = (taobaoSession.Ext_Date - datetime.datetime.now()).days + 1
        return day
    else:
        return 0


def get_user_session_SessionKey(userid):
    taobaoSession_list = TaoBaoSession.objects.filter(Owner_id=userid)
    if taobaoSession_list.count() > 0:
        taobaoSession = taobaoSession_list.first()
        return taobaoSession.SessionKey
    else:
        return ''

# end 第三方API授权


# begin 账户总览

@login_required
def index(request):
    if request.user.is_superuser or request.user.is_mainuser:
        agenturl = request.build_absolute_uri(
            reverse('Users:register')) + '?invite_code=' + request.user.invite_code
        qrcodeurl = "http://qr.liantu.com/api.php?text=" + agenturl
        outh_api = 'http://mvapi.vephp.com/auth?vekey={}&state={}&recall_url={}'
        reouth_url = request.build_absolute_uri(reverse('Web:ReOuth'))
        outh_api = outh_api.format(vekey, request.user.id, reouth_url)
        resp = requests.get(outh_api)
        taobaoouthurl = str(resp.content, 'utf-8')
        outh_day = get_user_session_ext_Date(request.user.id)
        create_withdraw_url = request.build_absolute_uri(
            reverse('Web:CreateAgentApplyForWithdraw'))
        location = copy.deepcopy(location_init)
        location['IsIndexPage'] = True
        context = {'location': location,
                   'agenturl': agenturl, "qrcodeurl": qrcodeurl, 'taobaoouthurl': taobaoouthurl,
                   'outh_day': outh_day, 'create_withdraw_url': create_withdraw_url}
        return render(request, 'pages/index.html', context)
    else:
        agenturl = request.build_absolute_uri(
            reverse('Users:register')) + '?invite_code=' + request.user.invite_code
        qrcodeurl = "http://qr.liantu.com/api.php?text=" + agenturl
        create_withdraw_url = request.build_absolute_uri(
            reverse('Web:CreateAgentApplyForWithdraw'))

        user_id = request.user.id
        agent = Agent.objects.get(Subscriber__id=user_id)
        agent_id = agent.id
        # 今日预估收入
        now = datetime.date.today()
        begintime = str(now)
        endtime = str(now + datetime.timedelta(days=1))
        sql = "EXEC [CalcAgentIncome] {},'{}','{}',{},'{}'".format(
            agent_id, begintime, endtime, 0, 'Total')
        cur = connection.cursor()
        rows = cur.execute(sql).fetchall()
        OrderIncome = rows[0][0] if rows[0][0] is not None else 0
        sql = "EXEC [CalcAgentMissionIncome] {},'{}','{}'".format(
            agent_id, begintime, endtime)
        cur = connection.cursor()
        rows = cur.execute(sql).fetchall()
        MissionIncome = rows[0][0] if rows[0][0] is not None else 0
        TodayIncome = OrderIncome + MissionIncome

        # 本月预估收入
        now = datetime.date.today()
        endtime = str(now + datetime.timedelta(days=1))
        day = now.day
        if day > 25:
            begintime = str(datetime.datetime(now.year, now.month, 26))
        else:
            if now.month == 1:
                begintime = str(datetime.datetime(now.year - 1, 12, 26))
            else:
                begintime = str(datetime.datetime(now.year, now.month - 1, 26))
        sql = "EXEC [CalcAgentIncome] {},'{}','{}',{},'{}'".format(
            agent_id, begintime, endtime, 0, 'Total')
        cur = connection.cursor()
        rows = cur.execute(sql).fetchall()
        CurrentMonthOrderIncome = rows[0][0] if rows[0][0] is not None else 0
        sql = "EXEC [CalcAgentMissionIncome] {},'{}','{}'".format(
            agent_id, begintime, endtime)
        cur = connection.cursor()
        rows = cur.execute(sql).fetchall()
        CurrentMonthMissionIncome = rows[0][0] if rows[0][0] is not None else 0
        CurrentMonthIncome = CurrentMonthOrderIncome + CurrentMonthMissionIncome

        # 上月预估收入
        day = now.day
        if day > 25:
            endtime = str(datetime.datetime(now.year, now.month, 26))
            if now.month == 1:
                begintime = str(datetime.datetime(now.year - 1, 12, 26))
            else:
                begintime = str(datetime.datetime(now.year, now.month - 1, 26))
        else:
            if now.month == 1:
                endtime = str(datetime.datetime(now.year - 1, 12, 26))
                begintime = str(datetime.datetime(now.year - 1, 11, 26))
            else:
                endtime = str(datetime.datetime(now.year, now.month - 1, 26))
                if now.month == 2:
                    begintime = str(datetime.datetime(now.year - 1, 12, 26))
                else:
                    begintime = str(datetime.datetime(
                        now.year, now.month - 2, 26))
        sql = "EXEC [CalcAgentIncome] {},'{}','{}',{},'{}'".format(
            agent_id, begintime, endtime, 0, 'Total')
        cur = connection.cursor()
        rows = cur.execute(sql).fetchall()
        LastMonthOrderIncome = rows[0][0] if rows[0][0] is not None else 0
        sql = "EXEC [CalcAgentMissionIncome] {},'{}','{}'".format(
            agent_id, begintime, endtime)
        cur = connection.cursor()
        rows = cur.execute(sql).fetchall()
        LastMonthMissionIncome = rows[0][0] if rows[0][0] is not None else 0  
        LastMonthIncome = LastMonthOrderIncome + LastMonthMissionIncome      
        

        # 上月实际收入
        month_income_list = AgentMonthRealityIncome.objects.filter(
            Agent__id=agent_id).order_by('-SummaryDate')
        if month_income_list.count() > 0:
            month_income = month_income_list.first()
            LastMonthTruelyIncome = month_income.TotalMoney
        else:
            LastMonthTruelyIncome = 0

        location = copy.deepcopy(location_init)
        location['IsAgentIndexPage'] = True
        context = {'location': location,
                'agenturl': agenturl, "qrcodeurl": qrcodeurl,
                'create_withdraw_url': create_withdraw_url, 'TodayIncome': TodayIncome,
                'CurrentMonthIncome': CurrentMonthIncome, 'LastMonthIncome': LastMonthIncome,
                'LastMonthTruelyIncome': LastMonthTruelyIncome}
        return render(request, 'pages/Agent/AgentIndex.html', context)

# end 账户总览

# begin 设备管理
@login_required
def devicemanage(request):
    data_url = request.build_absolute_uri(reverse('Web:GetDevice'))
    agentdetail_url = request.build_absolute_uri(reverse('Web:AgentDetail'))
    acountlist_url = request.build_absolute_uri(reverse('Web:AccountList'))
    getdeviceremark_url = request.build_absolute_uri(
        reverse('Web:GetDeviceRemark'))
    editdeviceremark_url = request.build_absolute_uri(
        reverse('Web:EditDeviceRemark'))
    editdeviceenable_url = request.build_absolute_uri(
        reverse('Web:EditDeviceEnable'))
    owner_id_list = []
    if request.user.username == 'admin':
        owner_id_list = GetOwnerIDList(request.user.id, owner_id_list)        
    else:
        owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)                
    classifications = MaintenanceNumberMissionKeywordClassification.objects.filter(Owner__in=owner_id_list).values('Name').distinct()
    groups = TikTokAccountGroup.objects.filter(Owner__in=owner_id_list).values('Name').distinct()
    owners = []
    for i in range(len(owner_id_list)):
        owner_id = owner_id_list[i]
        user = User.objects.get(id=owner_id)
        owners.append(user)    
    location = copy.deepcopy(location_init)
    location['IsDeviceManagePage'] = True
    location['IsDeviceManageMenu'] = True
    context = {'location': location, 'data_url': data_url, 'getdeviceremark_url': getdeviceremark_url,
               'editdeviceremark_url': editdeviceremark_url, 'agentdetail_url': agentdetail_url,
               'acountlist_url': acountlist_url, 'classifications': classifications, 'groups': groups,
               'editdeviceenable_url': editdeviceenable_url, 'owners': owners}
    return render(request, 'pages/DeviceManage/DeviceManage.html', context)


@login_required
def getdevice(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    generalSearch = request.POST.get('query[generalDeviceSearch]')
    devicecolumn = request.POST.get('query[devicecolumn]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    status = request.POST.get('query[device_status]')
    isonline = request.POST.get('query[isonline]')
    isagent = request.POST.get('isagent')
    agentid = request.POST.get('agentid')
    isonline_second = GetSystemConfig('心跳存活判断秒数')
    tag = request.POST.get('query[tag]')
    group = request.POST.get('query[group]')
    iscommodity = request.POST.get('iscommodity')
    isuserdevicedeliver = request.POST.get('isuserdevicedeliver')
    owner = request.POST.get('query[owner]')

    if request.user.username == 'admin':
        owner_id_list = []
        if owner is not None and owner != '':
            owner_id_list.append(owner)
        else:         
            owner_id_list = GetOwnerIDList(request.user.id, owner_id_list)
    else:
        owner_id_list = []
        if owner is not None and owner != '':
            owner_id_list.append(owner)
        else:        
            owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)

    if isagent is not None:
        my_filter = Q()
        my_filter = my_filter & Q(Owner__id__in=owner_id_list)
        my_filter = my_filter & Q(Agent=None)   
        data_list = MobilePhone.objects.filter(my_filter)
    elif iscommodity is not None and iscommodity != '':
        my_filter = Q()
        my_filter = my_filter & Q(Owner__id__in=owner_id_list)
        my_filter = my_filter & Q(TikTokAccount__ShowWindowExists=True)           
        data_list = MobilePhone.objects.filter(my_filter)
    elif isuserdevicedeliver is not None and isuserdevicedeliver != '':
        user_owner_id_list = []
        if owner is not None and owner != '':
            user_owner_id_list.append(owner)
        else:         
            user_owner_id_list = GetOwnerIDList(request.user.id, owner_id_list)        
        my_filter = Q()
        my_filter = my_filter & Q(Owner__id__in=user_owner_id_list)        
        data_list = MobilePhone.objects.filter(my_filter)
    else:
        my_filter = Q()    
        my_filter = my_filter & Q(Owner__id__in=owner_id_list)
        data_list = MobilePhone.objects.filter(my_filter)

    if generalSearch is not None and generalSearch != '':
        search_filter = Q()
        if devicecolumn == 'remark':
            search_filter = search_filter | Q(Remark__contains=generalSearch)
        elif devicecolumn == 'tiktok':
            search_filter = search_filter | Q(
                TikTokAccount__NickName__contains=generalSearch)
        elif devicecolumn == 'agent':
            search_filter = search_filter | Q(
                Agent__Subscriber__username__contains=generalSearch)
        elif devicecolumn == 'id':
            if str.isdigit(generalSearch):
                search_filter = search_filter | Q(id=generalSearch)
        else:
            search_filter = search_filter | Q(Remark__contains=generalSearch)
            search_filter = search_filter | Q(
                TikTokAccount__NickName__contains=generalSearch)
            search_filter = search_filter | Q(
                Agent__Subscriber__username__contains=generalSearch)
            if str.isdigit(generalSearch):
                search_filter = search_filter | Q(id=generalSearch)
        data_list = data_list.filter(search_filter)

    if status is not None and status != '':
        data_list = data_list.filter(Enable=status)

    if isonline is not None and isonline != '':
        starttime = datetime.datetime.now()
        endtime = starttime - datetime.timedelta(seconds=isonline_second)
        if (isonline == 'True'):
            data_list = data_list.filter(HeartBeat__gte=endtime)
        else:
            isonline_filter = Q()
            isonline_filter = isonline_filter | Q(HeartBeat__lt=endtime)
            isonline_filter = isonline_filter | Q(HeartBeat=None)
            data_list = data_list.filter(isonline_filter)

    if tag is not None and tag != '':
        tag_filter = Q()
        if '-1' in tag:
            tag_filter = tag_filter | Q(TikTokAccount__Classification=None)
        tag_list = tag[:-1].split(',')
        tag_filter = tag_filter | Q(
            TikTokAccount__Classification__Name__in=tag_list)
        data_list = data_list.filter(tag_filter).distinct()

    if group is not None and group != '':
        group_filter = Q()
        if '-1' in group:
            group_filter = group_filter | Q(TikTokAccount__Group=None)
        group_list = group[:-1].split(',')
        group_filter = group_filter | Q(
            TikTokAccount__Group__Name__in=group_list)
        data_list = data_list.filter(group_filter)

    fields_list = MobilePhone._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')        

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values('id', 'Enable', 'TikTokAccount__NickName',
                                                 'TikTokAccount__TikTokID', 'Agent__Subscriber__username',
                                                 'Remark', 'HeartBeat', 'TikTokAccount__id', 'TikTokAccount__Group__Name',
                                                 'TikTokAccount__ShowWindowExists', 'StatusInfo', 'Owner__username')
    data = []
    for i in range(len(data_result)):
        heartbeat = data_result[i]['HeartBeat']
        if heartbeat is None:
            isonlinestatus = False
        else:
            starttime = datetime.datetime.now()
            isonlinestatus = (
                (starttime - heartbeat).seconds < isonline_second)
        data_result[i]['IsOnline'] = isonlinestatus
        if data_result[i]['TikTokAccount__id'] != None:
            TikTokAccount__id = data_result[i]['TikTokAccount__id']
            account = TikTokAccount.objects.get(id=TikTokAccount__id)
            data_result[i]['tag'] = account.GetClassificationString()
        else:
            data_result[i]['tag'] = ''
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def getdevicenamebyids(request):
    ids = request.POST.get('ids')
    id_list = ids[:-1].split(',')
    if len(id_list) > 0:
        context = {
            'ids': ids[:-1],
        }
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('Error')


@login_required
def getdeviceremark(request):
    data_id = request.POST.get('id')
    mobile = MobilePhone.objects.get(id=data_id)
    remark = mobile.Remark
    context = {'dataid': data_id, 'remark': remark}
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def editdeviceremark(request):
    data_id = request.POST.get('id')
    remark = request.POST.get('remark')
    mobile = MobilePhone.objects.get(id=data_id)
    mobile.Remark = remark
    mobile.save()
    return HttpResponse('OK')


@login_required
def editdeviceenable(request):
    data_id = request.POST.get('id')
    mobile = MobilePhone.objects.get(id=data_id)
    mobile.Enable = not mobile.Enable
    mobile.save()
    return HttpResponse('OK')

# end 设备管理

# begin 账号数据分析

@login_required
def accountdataanalysis(request):
    data_url = request.build_absolute_uri(
        reverse('Web:GetAccountDataAnalysis'))
    agentdetail_url = request.build_absolute_uri(reverse('Web:AgentDetail'))
    acountlist_url = request.build_absolute_uri(reverse('Web:AccountList'))
    owner_id_list = []
    owner_id_list = GetOwnerIDList(request.user.id, owner_id_list)
    groups = TikTokAccountGroup.objects.filter(Owner__id__in=owner_id_list).values('Name').distinct()
    classifications = MaintenanceNumberMissionKeywordClassification.objects.filter(Owner__id__in=owner_id_list).values('Name').distinct()
    owners = []
    for i in range(len(owner_id_list)):
        owner_id = owner_id_list[i]
        user = User.objects.get(id=owner_id)
        owners.append(user)
    devicemanage_url = request.build_absolute_uri(reverse('Web:DeviceManage'))  
    location = copy.deepcopy(location_init)
    location['IsAccountDataAnalysisPage'] = True
    location['IsDataAnalysisMenu'] = True
    context = {'location': location, 'data_url': data_url, 'groups': groups, 'classifications': classifications,
               'agentdetail_url': agentdetail_url, 'acountlist_url': acountlist_url, 'devicemanage_url': devicemanage_url,
               'owners': owners}
    return render(request, 'pages/DataAnalysis/AccountDataAnalysis.html', context)


@login_required
def getaccountdataanalysis(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    tag = request.POST.get('query[tag]')
    group = request.POST.get('query[group]')
    generalSearch = request.POST.get('query[generalAccountDataNanlysisSearch]')
    date = request.POST.get('query[date]')
    generalHistorySearch = request.POST.get('query[generalHistorySearch]')
    isHisroty = request.POST.get('ishistory')
    owner = request.POST.get('query[owner]')

    now = datetime.date.today()
    if isHisroty == 'false':
        if date is None or date == '':
            # 昨天
            TotalBeginTime = now - datetime.timedelta(days=1)
            TotalEndTime = TotalBeginTime
        elif date == '1':
            # 前天
            TotalBeginTime = now - datetime.timedelta(days=2)
            TotalEndTime = TotalBeginTime
    else:
        # 30天历史记录
        if generalHistorySearch is not None and generalHistorySearch != '':
            TotalEndTime = now - datetime.timedelta(days=1)
            TotalBeginTime = TotalEndTime - datetime.timedelta(days=29)
        else:
            TotalBeginTime = now + datetime.timedelta(days=1)
            TotalEndTime = now
            TikTokAccountDataAnalysis.objects.filter(Owner=request.user).delete()

    Interval = (TotalEndTime - TotalBeginTime).days + 1
    if Interval > 0:
        if isHisroty == 'false':
            if owner is not None and owner != '':
                account_list = TikTokAccount.objects.filter(Owner__id=owner)  
            else:
                owner_id_list = []
                owner_id_list = GetOwnerIDList(request.user.id, owner_id_list)
                account_list = TikTokAccount.objects.filter(Owner__id__in=owner_id_list)

            if generalSearch is not None and generalSearch != '':
                account_list = account_list.filter(NickName=generalSearch)

            if tag is not None and tag != '':
                tag_filter = Q()
                if '-1' in tag:
                    tag_filter = tag_filter | Q(Classification=None)
                tag_list = tag[:-1].split(',')
                tag_filter = tag_filter | Q(
                    Classification__Name__in=tag_list)
                account_list = account_list.filter(tag_filter)

            if group is not None and group != '':
                group_filter = Q()
                if '-1' in group:
                    group_filter = group_filter | Q(Group=None)
                group_list = group[:-1].split(',')
                group_filter = group_filter | Q(
                    Group__Name__in=group_list)
                account_list = account_list.filter(group_filter)                
 
        else:
            account_list = TikTokAccount.objects.filter(
                NickName=generalHistorySearch).all()
        TikTokAccountDataAnalysis.objects.filter(Owner=request.user).delete()
        for i in range(len(account_list)):
            for j in range(Interval):
                Summary_Date = TotalBeginTime + datetime.timedelta(days=j)
                account_id = account_list[i].id
                account = TikTokAccount.objects.get(id=account_id)
                data_analysis = TikTokAccountDataAnalysis()
                data_analysis.TikTokAccount = account
                data_analysis.Summary_Date = Summary_Date
                BeginTime = Summary_Date - datetime.timedelta(days=1)
                EndTime = Summary_Date

                TikTokAccountDaySummaryBegin_filter = Q()
                TikTokAccountDaySummaryBegin_filter = TikTokAccountDaySummaryBegin_filter & Q(
                    TikTokAccount_id=account_id)
                TikTokAccountDaySummaryBegin_filter = TikTokAccountDaySummaryBegin_filter & Q(
                    Summary_Date=BeginTime)
                NumBeginList = TikTokAccountDaySummary.objects.filter(TikTokAccountDaySummaryBegin_filter).aggregate(Attention=Coalesce(Sum('Attention'), 0), Fans=Coalesce(
                    Sum('Fans'), 0), Praise=Coalesce(Sum('Praise'), 0), Video=Coalesce(Sum('Video'), 0), NumOfPraiseToOther=Coalesce(Sum('NumOfPraiseToOther'), 0))
                TikTokAccountDaySummaryEnd_filter = Q()
                TikTokAccountDaySummaryEnd_filter = TikTokAccountDaySummaryEnd_filter & Q(
                    TikTokAccount_id=account_id)
                TikTokAccountDaySummaryEnd_filter = TikTokAccountDaySummaryEnd_filter & Q(
                    Summary_Date=EndTime)
                NumEndist = TikTokAccountDaySummary.objects.filter(TikTokAccountDaySummaryEnd_filter).aggregate(Attention=Coalesce(Sum('Attention'), 0), Fans=Coalesce(
                    Sum('Fans'), 0), Praise=Coalesce(Sum('Praise'), 0), Video=Coalesce(Sum('Video'), 0), NumOfPraiseToOther=Coalesce(Sum('NumOfPraiseToOther'), 0))

                WorksDaySummaryBegin_filter = Q()
                WorksDaySummaryBegin_filter = WorksDaySummaryBegin_filter & Q(
                    Work__TikTokAccount__id=account_id)
                WorksDaySummaryBegin_filter = WorksDaySummaryBegin_filter & Q(
                    Summary_Date=BeginTime)
                WorksBeginList = WorksDaySummary.objects.filter(
                    WorksDaySummaryBegin_filter).aggregate(NumOfPlay=Coalesce(Sum('NumOfPlay'), 0), NumOfComments=Coalesce(Sum('NumOfComments'), 0))

                WorksDaySummaryEnd_filter = Q()
                WorksDaySummaryEnd_filter = WorksDaySummaryEnd_filter & Q(
                    Work__TikTokAccount__id=account_id)
                WorksDaySummaryEnd_filter = WorksDaySummaryEnd_filter & Q(
                    Summary_Date=EndTime)
                WorksEndist = WorksDaySummary.objects.filter(
                    WorksDaySummaryEnd_filter).aggregate(NumOfPlay=Coalesce(Sum('NumOfPlay'), 0), NumOfComments=Coalesce(Sum('NumOfComments'), 0))

                FirstWorks_list = Works.objects.filter(
                    TikTokAccount__id=account_id).order_by('-UploadTime')
                if FirstWorks_list.count() > 0:
                    FirstWorks = FirstWorks_list.first()

                    FirstWorksDaySummaryBegin_filter = Q()
                    FirstWorksDaySummaryBegin_filter = FirstWorksDaySummaryBegin_filter & Q(
                        Work__id=FirstWorks.id)
                    FirstWorksDaySummaryBegin_filter = FirstWorksDaySummaryBegin_filter & Q(
                        Summary_Date=BeginTime)
                    FirstWorksBeginList = WorksDaySummary.objects.filter(
                        FirstWorksDaySummaryBegin_filter).aggregate(NumOfPlay=Coalesce(Sum('NumOfPlay'), 0))

                    FirstWorksDaySummaryEnd_filter = Q()
                    FirstWorksDaySummaryEnd_filter = FirstWorksDaySummaryEnd_filter & Q(
                        Work__id=FirstWorks.id)
                    FirstWorksDaySummaryEnd_filter = FirstWorksDaySummaryEnd_filter & Q(
                        Summary_Date=EndTime)
                    FirstWorksEndist = WorksDaySummary.objects.filter(
                        FirstWorksDaySummaryEnd_filter).aggregate(NumOfPlay=Coalesce(Sum('NumOfPlay'), 0))
                else:
                    FirstWorksBeginList = {'NumOfPlay': 0}
                    FirstWorksEndist = {'NumOfPlay': 0}

                # 作品数
                data_analysis.Video = NumEndist['Video']
                # 粉丝数
                data_analysis.Fans = NumEndist['Fans']
                # 关注数
                data_analysis.Attention = NumEndist['Attention']
                # 获赞数
                data_analysis.Praise = NumEndist['Praise']
                # 点赞数
                data_analysis.NumOfPraiseToOther = NumEndist['NumOfPraiseToOther']
                # 总播放数
                data_analysis.TotalNumOfPlay = WorksEndist['NumOfPlay']
                # 作品1播放数
                data_analysis.FirstWorkNumOfPlay = FirstWorksEndist['NumOfPlay']
                # 粉丝增量
                data_analysis.FansIncrease = NumEndist['Fans'] - NumBeginList['Fans']
                # 关注增量
                data_analysis.AttentionIncrease = NumEndist['Attention'] - NumBeginList['Attention']
                # 获赞增量
                data_analysis.PraiseIncrease = NumEndist['Praise'] - NumBeginList['Praise']
                # 点赞增量
                data_analysis.NumOfPraiseToOtherIncrease = NumEndist['NumOfPraiseToOther'] - NumBeginList['NumOfPraiseToOther']
                # 总播放增量
                data_analysis.TotalNumOfPlayIncrease = WorksEndist['NumOfPlay'] - WorksBeginList['NumOfPlay']
                # 作品1播放增量
                data_analysis.FirstWorkNumOfPlayIncrease = FirstWorksEndist['NumOfPlay'] - FirstWorksBeginList['NumOfPlay']
                # 总评论量
                data_analysis.TotalNumOfComments = WorksEndist['NumOfComments']                
                # 评论增量
                data_analysis.TotalNumOfCommentsIncrease = WorksEndist['NumOfComments'] - WorksBeginList['NumOfComments']
                data_analysis.Owner = request.user
                data_analysis.save()

    data_list = TikTokAccountDataAnalysis.objects.filter(Owner=request.user) 

    if field is not None and field != '':
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('-Summary_Date')

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values('TikTokAccount__id', 'Summary_Date', 'Attention', 'Fans', 'Praise', 'Video',
                                                 'NumOfPraiseToOther', 'TotalNumOfPlay', 'FirstWorkNumOfPlay', 'AttentionIncrease',
                                                 'FansIncrease', 'PraiseIncrease', 'NumOfPraiseToOtherIncrease',
                                                 'TotalNumOfPlayIncrease', 'FirstWorkNumOfPlayIncrease',
                                                 'TikTokAccount__Group__Name', 'TikTokAccount__mobilephone__Agent__Subscriber__username',
                                                 'TikTokAccount__NickName', 'TotalNumOfComments', 'TotalNumOfCommentsIncrease',
                                                 'TikTokAccount__mobilephone__id', 'TikTokAccount__Owner__username')
    data = []

    for i in range(len(data_result)):
        tiktokaccount_id = data_result[i]['TikTokAccount__id']
        tiktokaccount = TikTokAccount.objects.get(id=tiktokaccount_id)
        classification = tiktokaccount.GetClassificationString()
        data_result[i]['classification'] = classification
        todayvideocount = tiktokaccount.GetTodayVideoCount()
        data.append(data_result[i])

    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


def GetOwnerIDList(userid, owner_id_list):
    owner_id_list.append(userid)
    relation_list = list(TopUserRelations.objects.filter(Leader__id=userid).values_list('Subscriber__id', flat=True))
    if len(relation_list) == 0:
        return owner_id_list
    else:
        for i in range(len(relation_list)):
            owner_id_list = GetOwnerIDList(relation_list[i], owner_id_list)
        return owner_id_list


def GetOwnerIDUntilSuperuserList(userid, owner_id_list):
    owner_id_list.append(userid)
    relation_list = list(TopUserRelations.objects.filter(Leader__id=userid).values_list('Subscriber__id', flat=True))
    if len(relation_list) == 0:
        return owner_id_list
    else:
        for i in range(len(relation_list)):
            user = User.objects.get(id=relation_list[i])
            if user.is_superuser == False:
                owner_id_list = GetOwnerIDList(relation_list[i], owner_id_list)
            else:
                continue
        return owner_id_list
# end 账号数据分析

# begin 账号分组
@login_required
def accountgroup(request):
    data_url = request.build_absolute_uri(reverse('Web:GetAccountGroup'))
    create_url = request.build_absolute_uri(
        reverse('Web:CreateAccountGroup'))
    delete_url = request.build_absolute_uri(
        reverse('Web:DeleteAccountGroup'))
    get_by_id_url = request.build_absolute_uri(
        reverse('Web:GetAccountGroupByID'))
    edit_url = request.build_absolute_uri(reverse('Web:EditAccountGroup'))
    location = copy.deepcopy(location_init)
    location['IsAccountGroupPage'] = True
    location['IsMyAccountMenu'] = True
    context = {'location': location, 'data_url': data_url, 'delete_url': delete_url,
               'create_url': create_url, 'get_by_id_url': get_by_id_url, 'edit_url': edit_url}
    return render(request, 'pages/MyAccount/AccountGroup.html', context)


@login_required
def getaccountgroup(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')

    owner_id_list = []
    owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)
    data_list = TikTokAccountGroup.objects.filter(Owner__id__in=owner_id_list)

    fields_list = TikTokAccountGroup._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')        

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values('id', 'Name')
    data = []
    for i in range(len(data_result)):
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def delete_accountgroup_by_ids(request):
    ids = request.POST.get('ids')
    id_list = ids[:-1].split(',')
    if len(ids) > 0:
        TikTokAccountGroup.objects.filter(id__in=id_list).delete()
    return HttpResponseRedirect(reverse('Web:AccountGroup'))


@login_required
def createaccountgroup(request):
    try:
        name = request.POST.get('name')
        tiktokAccountGroup = TikTokAccountGroup()
        tiktokAccountGroup.Name = name
        tiktokAccountGroup.Owner = request.user
        tiktokAccountGroup.save()
        return HttpResponse(reverse('Web:AccountGroup'))
    except Exception as e:
        print(e)
        return HttpResponse("Error")


@login_required
def editaccountgroup(request):
    data_id = request.POST.get('id')
    name = request.POST.get('name')
    accountgroup = TikTokAccountGroup.objects.get(id=data_id)
    accountgroup.Name = name
    accountgroup.save()
    return HttpResponse(reverse('Web:AccountGroup'))


@login_required
def getaccountgroupbyid(request):
    data_id = request.POST.get('id')
    data = TikTokAccountGroup.objects.get(id=data_id)
    context = {
        'name': data.Name,
        'dataid': data.id,
    }
    if data is not None:
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('Error')

# end 账号分组

# begin 账号列表
@login_required
def accountlist(request):
    data_url = request.build_absolute_uri(reverse('Web:GetAccount'))
    get_by_id_url = request.build_absolute_uri(
        reverse('Web:GetAccountListByID'))
    edit_url = request.build_absolute_uri(reverse('Web:EditAccountList'))
    owner_id_list = []
    if request.user.username == 'admin':
        owner_id_list = GetOwnerIDList(request.user.id, owner_id_list)        
    else:
        owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)       
    groups = TikTokAccountGroup.objects.filter(Owner__id__in=owner_id_list).values('Name').distinct()
    edit_groups = TikTokAccountGroup.objects.filter(Owner=request.user)
    classifications = MaintenanceNumberMissionKeywordClassification.objects.filter(Owner__id__in=owner_id_list).values('Name').distinct()
    edit_classifications = MaintenanceNumberMissionKeywordClassification.objects.filter(Owner=request.user)
    agentdetail_url = request.build_absolute_uri(reverse('Web:AgentDetail'))
    devicemanage_url = request.build_absolute_uri(reverse('Web:DeviceManage'))
    works_url = request.build_absolute_uri(reverse('Web:GetWorks'))  
    owners = []
    for i in range(len(owner_id_list)):
        owner_id = owner_id_list[i]
        user = User.objects.get(id=owner_id)
        owners.append(user)      
    location = copy.deepcopy(location_init)
    location['IsAccountListPage'] = True
    location['IsMyAccountMenu'] = True
    context = {'location': location, 'data_url': data_url, 'get_by_id_url': get_by_id_url,
               'edit_url': edit_url, 'groups': groups,
               'classifications': classifications, 'agentdetail_url': agentdetail_url,
               'devicemanage_url': devicemanage_url, 'works_url': works_url, 'owners': owners,
               'edit_groups': edit_groups, 'edit_classifications': edit_classifications}
    return render(request, 'pages/MyAccount/AccountList.html', context)


@login_required
def getaccount(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    generalSearch = request.POST.get('query[generalAccountSearch]')
    tiktokaccountcolumn = request.POST.get('query[tiktokaccountcolumn]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    status = request.POST.get('query[tiktokaccount_status]')
    showwindowexists = request.POST.get('query[showwindowexists]')
    tag = request.POST.get('query[tag]')
    group = request.POST.get('query[group]')
    isonline_second = GetSystemConfig('心跳存活判断秒数')
    owner = request.POST.get('query[owner]')    

    if request.user.username == 'admin':
        owner_id_list = []
        if owner is not None and owner != '':
            owner_id_list.append(owner)
        else:         
            owner_id_list = GetOwnerIDList(request.user.id, owner_id_list)
    else:
        owner_id_list = []
        if owner is not None and owner != '':
            owner_id_list.append(owner)
        else:        
            owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)
    data_list = TikTokAccount.objects.filter(Owner__id__in=owner_id_list)

    if generalSearch is not None and generalSearch != '':
        serarch_filter = Q()
        if tiktokaccountcolumn == 'nickname':
            serarch_filter = serarch_filter | Q(
                NickName__contains=generalSearch)
        elif tiktokaccountcolumn == 'remark':
            serarch_filter = serarch_filter | Q(Remark__contains=generalSearch)
        elif tiktokaccountcolumn == 'mobileid':
            if str.isdigit(generalSearch):
                serarch_filter = serarch_filter | Q(mobilephone__id=generalSearch)
        elif tiktokaccountcolumn == 'agentname':
            serarch_filter = serarch_filter | Q(
                mobilephone__Agent__Subscriber__username__contains=generalSearch)
        else:
            serarch_filter = serarch_filter | Q(
                NickName__contains=generalSearch)
            serarch_filter = serarch_filter | Q(Remark__contains=generalSearch)
            serarch_filter = serarch_filter | Q(
                mobilephone__Agent__Subscriber__username__contains=generalSearch)
            if str.isdigit(generalSearch):
                serarch_filter = serarch_filter | Q(
                    mobilephone__id=generalSearch)
        data_list = data_list.filter(serarch_filter)

    if status is not None and status != '':
        starttime = datetime.datetime.now()
        endtime = starttime - datetime.timedelta(seconds=isonline_second)
        if (status == 'True'):
            data_list = data_list.filter(mobilephone__HeartBeat__gte=endtime)
        else:
            isonline_filter = Q()
            isonline_filter = isonline_filter | Q(
                mobilephone__HeartBeat__lt=endtime)
            isonline_filter = isonline_filter | Q(mobilephone__HeartBeat=None)
            data_list = data_list.filter(isonline_filter)

    if showwindowexists is not None and showwindowexists != '':
        data_list = data_list.filter(ShowWindowExists=showwindowexists)

    if tag is not None and tag != '':
        tag_filter = Q()
        if '-1' in tag:
            tag_filter = tag_filter | Q(Classification=None)
        tag_list = tag[:-1].split(',')
        tag_filter = tag_filter | Q(Classification__Name__in=tag_list)
        data_list = data_list.filter(tag_filter)

    if group is not None and group != '':
        group_filter = Q()
        if '-1' in group:
            group_filter = group_filter | Q(Group=None)
        group_list = group[:-1].split(',')
        group_filter = group_filter | Q(Group__Name__in=group_list)
        data_list = data_list.filter(group_filter)

    fields_list = TikTokAccount._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values('id', 'UserID', 'NickName', 'TikTokID', 'Describe',
                                                 'Attention', 'Fans', 'Praise', 'Video', 'NumOfPraiseToOther',
                                                 'UpdateTime', 'ShowWindowExists',
                                                 'Remark', 'IP', 'Area', 'Group__Name', 'mobilephone__Agent__Subscriber__username',
                                                 'mobilephone__id', 'ShareURL', 'BindNickName', 'Owner__username')
    data = []
    for i in range(len(data_result)):
        tiktokaccount_id = data_result[i]['id']
        tiktokaccount = TikTokAccount.objects.get(id=tiktokaccount_id)
        Info = '粉丝：' + str(tiktokaccount.Fans) + '  ' + '关注：' + str(tiktokaccount.Attention) + '  ' + '赞：' + \
            str(tiktokaccount.Praise) + '  ' + '作品数：' + str(tiktokaccount.Video) + \
            '  ' + '喜欢：' + str(tiktokaccount.NumOfPraiseToOther)
        data_result[i]['Info'] = Info
        classification = tiktokaccount.GetClassificationString()
        data_result[i]['classification'] = classification
        todayvideocount = tiktokaccount.GetTodayVideoCount()
        data_result[i]['todayvideocount'] = todayvideocount
        todaygoodscount = tiktokaccount.GetTodayGoodsCount()
        data_result[i]['todaygoodscount'] = todaygoodscount
        isonline = tiktokaccount.GetIsOnline()
        data_result[i]['IsOnline'] = isonline
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def editaccountlist(request):
    data_id = request.POST.get('id')
    groupid = request.POST.get('groupid')
    remark = request.POST.get('remark')
    bindurl = request.POST.get('bindurl')
    classficationid = request.POST.get('classficationid')
    classfication_list = []
    tiktokaccount = TikTokAccount.objects.get(id=data_id)
    if groupid == '-1':
        tiktokaccount.Group = None
    else:
        group = TikTokAccountGroup.objects.get(id=groupid)
        tiktokaccount.Group = group
    tiktokaccount.Remark = remark
    if bindurl != tiktokaccount.BindURL:
        tiktokaccount.BindURL = bindurl
        if bindurl != '' and bindurl.find('v.douyin.com') > 0:
            realurl = get_realaddress(bindurl)
            userid = re.search(r'user/(.*)\?', realurl).group(1)
            tiktokaccount.BindID = userid
            tiktokaccount.BindLongURL = realurl
            userinfo = get_user(userid)
            tiktokaccount.BindNickName = userinfo['nick_name']
        else:
            tiktokaccount.BindID = ''
            tiktokaccount.BindLongURL = ''
            tiktokaccount.BindNickName = ''

    if tiktokaccount.Classification is not None:
        tiktokaccount.Classification.clear()
    if classficationid is not None and classficationid != '':
        classfication_list = classficationid[:-1].split(',')
        if len(classfication_list) > 0:
            for i in range(len(classfication_list)):
                classfication_id = classfication_list[i]
                classfication = MaintenanceNumberMissionKeywordClassification.objects.get(
                    id=classfication_id)
                tiktokaccount.Classification.add(classfication)
    tiktokaccount.save()
    return HttpResponse(reverse('Web:AccountList'))


def get_realaddress(short_url):
    # allow_redirects = False 不允许跳转
    response = requests.get(
        url=short_url, headers=headers, allow_redirects=False)
    return response.headers['Location']


def get_user(user_id):
    api = 'https://www.iesdouyin.com/share/user/' + user_id
    res = requests.get(api, headers=headers)
    user_info = handle_user_decode(res.text)
    return user_info


def handle_user_decode(input_data):
    bs = BeautifulSoup(input_data, 'lxml')
    douyin_info = {}
    # 获取昵称
    douyin_info['nick_name'] = bs.find(class_='nickname').get_text()
    return douyin_info


@login_required
def getaccountlistbyid(request):
    account_id = request.POST.get('id')
    account = TikTokAccount.objects.get(id=account_id)
    if account is not None:
        ClassificationId = account.GetClassificationId()
        info = '粉丝：' + str(account.Fans) + '  ' + '关注：' + str(account.Attention) + '  ' + '赞：' + \
            str(account.Praise) + '  ' + '作品数：' + str(account.Video) + \
            '  ' + '喜欢：' + str(account.NumOfPraiseToOther)
        pid = account.GetPID()
        context = {
            'remark': account.Remark,
            'dataid': account.id,
            'classificationid': ClassificationId,
            'groupid': '-1' if account.Group is None else account.Group.id,
            'nickname': account.NickName,
            'tiktokid': account.TikTokID,
            'info': info,
            'url': account.ShareURL,
            'showwindowexists': account.ShowWindowExists,
            'pid': pid,
            'bindurl': account.BindURL,
        }
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('Error')


@login_required
def getworks(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    accountid = request.POST.get('query[accountid]')
    goodid = request.POST.get('query[goodid]')

    owner_id_list = []
    if request.user.username == 'admin':
        owner_id_list = GetOwnerIDList(request.user.id, owner_id_list)        
    else:
        owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)  

    data_filter = Q()
    data_filter = data_filter & Q(TikTokAccount__Owner__id__in=owner_id_list)
    data_filter = data_filter & ~Q(Pic=None)
    if accountid != None and accountid != '':
        data_filter = data_filter & Q(TikTokAccount__id=accountid)
        data_list = Works.objects.filter(data_filter)
    elif goodid != None and goodid != '':
        data_filter = data_filter & Q(Video__Goods__id=goodid)
        data_list = Works.objects.filter(data_filter)
    else:
        data_list = Works.objects.filter(data_filter)

    fields_list = Works._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('-UploadTime')

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values('id', 'ShareURL', 'NumOfPraiseGet', 'NumOfComments', 'NumOfShare',
                                                 'UpdateTime', 'Pic', 'Describe', 'NumOfPlay', 'UploadTime', 'TikTokAccount__NickName')
    data = []
    for i in range(len(data_result)):
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")

# end 账号列表

# begin 阿里妈妈配置
@login_required
def aliconfig(request):
    data_url = request.build_absolute_uri(
        reverse('Web:GetALIConfig'))
    create_url = request.build_absolute_uri(
        reverse('Web:CreateALIConfig'))
    delete_url = request.build_absolute_uri(
        reverse('Web:DeleteALIConfig'))
    get_by_id_url = request.build_absolute_uri(
        reverse('Web:GetALIConfigByID'))
    edit_url = request.build_absolute_uri(reverse('Web:EditALIConfig'))
    category = GoodClassification.objects.filter(Owner=request.user)
    location = copy.deepcopy(location_init)
    location['IsALIConfigPage'] = True
    location['IsCommodityManageMenu'] = True
    context = {'location': location, 'data_url': data_url, 'create_url': create_url,
               'delete_url': delete_url, 'get_by_id_url': get_by_id_url, 'edit_url': edit_url,
               'aliconfig_status': ALIStatus, 'category': category}
    return render(request, 'pages/CommodityManage/ALIConfig.html', context)


@login_required
def getaliconfig(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    generalSearch = request.POST.get(
        'query[generalALIConfigSearch]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    status = request.POST.get('query[aliconfigstatus]')

    owner_id_list = []
    owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)
    data_list = ALIConfig.objects.filter(Owner__id__in=owner_id_list)

    if generalSearch is not None and generalSearch != '':
        data_list = data_list.filter(NickName__contains=generalSearch)

    if status is not None:
        data_list = data_list.filter(Status=status)

    fields_list = ALIConfig._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values(
        'id', 'NickName', 'Status', 'PID', 'Remark')
    data = []
    for i in range(len(data_result)):
        aliconfig_id = data_result[i]['id']
        aliconfig = ALIConfig.objects.get(
            id=aliconfig_id)
        CategoryString = aliconfig.GetCategoryString()
        data_result[i]['CategoryString'] = CategoryString
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def delete_aliconfig_by_ids(request):
    ids = request.POST.get('ids')
    id_list = ids[:-1].split(',')
    if len(ids) > 0:
        ALIConfig.objects.filter(id__in=id_list).delete()
    return HttpResponseRedirect(reverse('Web:ALIConfig'))


@login_required
def createaliconfig(request):
    NickName = request.POST.get('nickname')
    PID = request.POST.get('pid')
    Remark = request.POST.get('remark')
    category = request.POST.get('category')
    category_list = []
    pid_list = PID.split('_')
    last_pid = pid_list[-1]
    aliconfig = ALIConfig()
    aliconfig.NickName = NickName
    aliconfig.PID = PID
    aliconfig.LASTPID = last_pid
    aliconfig.Remark = Remark
    aliconfig.Owner = request.user
    aliconfig.save()
    if category is not None and category != '':
        category_list = category[:-1].split(',')
        if len(category_list) > 0:
            for i in range(len(category_list)):
                category_id = category_list[i]
                category = GoodClassification.objects.get(
                    id=category_id)
                aliconfig.Category.add(category)
    return HttpResponse(reverse('Web:ALIConfig'))


@login_required
def editaliconfig(request):
    data_id = request.POST.get('id')
    nickname = request.POST.get('nickname')
    pid = request.POST.get('pid')
    remark = request.POST.get('remark')
    category = request.POST.get('category')
    category_list = []
    pid_list = pid.split('_')
    last_pid = pid_list[-1]
    aliconfig = ALIConfig.objects.get(id=data_id)
    aliconfig.NickName = nickname
    aliconfig.PID = pid
    aliconfig.LASTPID = last_pid
    aliconfig.Remark = remark
    aliconfig.Category.clear()
    if category is not None and category != '':
        category_list = category[:-1].split(',')
        if len(category_list) > 0:
            for i in range(len(category_list)):
                category_id = category_list[i]
                category = GoodClassification.objects.get(
                    id=category_id)
                aliconfig.Category.add(category)
    aliconfig.save()
    return HttpResponse(reverse('Web:ALIConfig'))


@login_required
def getaliconfigbyid(request):
    aliconfig_id = request.POST.get('id')
    aliconfig = ALIConfig.objects.get(id=aliconfig_id)
    if aliconfig is not None:
        CategoryId = aliconfig.GetCategoryId()
        context = {
            'nickname': aliconfig.NickName,
            'pid': aliconfig.PID,
            'remark': aliconfig.Remark,
            'dataid': aliconfig.id,
            'categoryid': CategoryId,
        }
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('Error')

# end 阿里妈妈配置


@login_required
def alreadysendvideo(request):
    location = copy.deepcopy(location_init)
    location['IsAlreadySendVideoPage'] = True
    location['IsVideoManageMenu'] = True
    context = {'location': location}
    return render(request, 'pages/VideoManage/AlreadySendVideo.html', context)


# begin 商品数据分析

@login_required
def commoditydataanalysis(request):
    data_url = request.build_absolute_uri(
        reverse('Web:GetCommodityDataAnalysis'))
    works_url = request.build_absolute_uri(reverse('Web:GetWorks'))
    owner_id_list = []
    owner_id_list = GetOwnerIDList(request.user.id, owner_id_list)    
    owners = []
    for i in range(len(owner_id_list)):
        owner_id = owner_id_list[i]
        user = User.objects.get(id=owner_id)
        owners.append(user)    
    location = copy.deepcopy(location_init)
    location['IsCommodityDataAnalysisPage'] = True
    location['IsDataAnalysisMenu'] = True
    context = {'location': location, 'data_url': data_url,
               'works_url': works_url, 'owners': owners}
    return render(request, 'pages/DataAnalysis/CommodityDataAnalysis.html', context)


@login_required
def getcommoditydataanalysis(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    generalSearch = request.POST.get(
        'query[generalCommodityDataAnalysisSearch]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    workstime = request.POST.get('query[workstime]')
    commodityDataAnalysisColumn = request.POST.get('query[commodityDataAnalysisColumn]')    
    owner = request.POST.get('query[owner]')    

    if owner is not None and owner != '':
        good_list = Goods.objects.filter(Owner__id=owner)  
    else:
        owner_id_list = []
        owner_id_list = GetOwnerIDList(request.user.id, owner_id_list)
        good_list = Goods.objects.filter(Owner__id__in=owner_id_list)       

    CommodityDataAnalysis.objects.filter(Owner=request.user).delete()
    now = datetime.date.today()
    for i in range(len(good_list)):
        good_id = good_list[i].id
        good = Goods.objects.annotate(WorksCount=Count('videos__works'), NumOfPlay=Coalesce(Sum('videos__works__NumOfPlay'), 0), NumOfPraiseGet=Coalesce(Sum(
            'videos__works__NumOfPraiseGet'), 0), NumOfComments=Coalesce(Sum('videos__works__NumOfComments'), 0), NumOfShare=Coalesce(Sum('videos__works__NumOfShare'), 0)).get(id=good_id)
        data_analysis = CommodityDataAnalysis()
        data_analysis.Goods = good
        WorkStatistic = getGoodsWorkStatisticByWorktime(good, workstime)
        # 视频数量
        data_analysis.WorksCount = WorkStatistic['WorksCount']
        # 播放量
        data_analysis.NumOfPlay = WorkStatistic['NumOfPlay']
        # 点赞量
        data_analysis.NumOfPraiseGet = WorkStatistic['NumOfPraiseGet']
        # 评论量
        data_analysis.NumOfComments = WorkStatistic['NumOfComments']
        # 分享量
        data_analysis.NumOfShare = WorkStatistic['NumOfShare']
        # 今日销量
        beginTime = now
        endTime = beginTime + datetime.timedelta(days=1)
        data_analysis.TodayOrder = good.order_set.filter(
            TK_Create_Time__range=(beginTime, endTime)).count()
        # 昨日销量
        beginTime = now + datetime.timedelta(days=-1)
        endTime = beginTime + datetime.timedelta(days=1)
        data_analysis.YestodayOrder = good.order_set.filter(
            TK_Create_Time__range=(beginTime, endTime)).count()
        # 本月销量
        beginTime = datetime.datetime(now.year, now.month, 1)
        if now.month == 12:
            endTime = datetime.datetime(now.year, 12, 31)
        else:
            endTime = datetime.datetime(
                now.year, now.month + 1, 1) - datetime.timedelta(days=1)
        data_analysis.MonthOrder = good.order_set.filter(
            TK_Create_Time__range=(beginTime, endTime)).count()
        data_analysis.Owner = request.user
        data_analysis.save()

    data_list = CommodityDataAnalysis.objects.filter(Owner=request.user)

    if generalSearch is not None and generalSearch != '':
        search_filter = Q()
        if commodityDataAnalysisColumn == 'title':
            search_filter = search_filter | Q(Goods__Title__contains=generalSearch)
        elif commodityDataAnalysisColumn == 'id':
            if str.isdigit(generalSearch):
                search_filter = search_filter | Q(Goods__id=generalSearch)
        else:
            search_filter = search_filter | Q(Goods__Title__contains=generalSearch)
            if str.isdigit(generalSearch):
                search_filter = search_filter | Q(Goods__id=generalSearch)
        data_list = data_list.filter(search_filter)

    if field is not None and field != '':
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values('id', 'Goods__id', 'Goods__Pic1', 'Goods__CreateTime', 'Goods__Title', 'WorksCount',
                                                 'NumOfPlay', 'NumOfPraiseGet', 'NumOfComments', 'NumOfShare',
                                                 'TodayOrder', 'YestodayOrder', 'MonthOrder', 'Goods__Owner__username')
    data = []
    for i in range(len(data_result)):
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


def getGoodsWorkStatisticByWorktime(good, workstime):
    WorksStatistic = {'WorksCount': 0, 'NumOfPlay': 0,
                      'NumOfPraiseGet': 0, 'NumOfComments': 0, 'NumOfShare': 0}
    # 0:全部 1:今天 2:昨天 3:本月 4:上月 5:上上月
    beginTime = ''
    endTime = ''
    now = datetime.date.today()
    if workstime is None or workstime == '0':
        WorksStatistic['WorksCount'] = good.WorksCount
        WorksStatistic['NumOfPlay'] = good.NumOfPlay
        WorksStatistic['NumOfPraiseGet'] = good.NumOfPraiseGet
        WorksStatistic['NumOfComments'] = good.NumOfComments
        WorksStatistic['NumOfShare'] = good.NumOfShare
    elif workstime == '1':
        beginTime = now + datetime.timedelta(days=1)
        WorksCountFilter = Q()
        WorksCountFilter = WorksCountFilter & Q(
            videos__works__UploadTime__lte=beginTime)
        WorksCountFilter = WorksCountFilter & Q(id=good.id)
        # 视频数量
        WorksCountList = Goods.objects.aggregate(
            WorksCount=Count('videos__works', filter=WorksCountFilter))
        WorksStatistic['WorksCount'] = WorksCountList['WorksCount']

        works_id_filter = Goods.objects.filter(
            WorksCountFilter).values_list('videos__works__id', flat=True)
        works_id_list = list(works_id_filter)
        if len(works_id_list) > 0 and works_id_list[0] != None:
            summary_date = now - datetime.timedelta(days=1)
            WorksDaySummary_filter = Q()
            WorksDaySummary_filter = WorksDaySummary_filter & Q(
                Work_id__in=works_id_list)
            WorksDaySummary_filter = WorksDaySummary_filter & Q(
                Summary_Date=summary_date)
            # 播放量, 点赞量， 评论量， 分享量
            NumList = WorksDaySummary.objects.filter(WorksDaySummary_filter).aggregate(NumOfPlay=Coalesce(Sum('NumOfPlay'), 0), NumOfPraiseGet=Coalesce(
                Sum('NumOfPraiseGet'), 0), NumOfComments=Coalesce(Sum('NumOfComments'), 0), NumOfShare=Coalesce(Sum('NumOfShare'), 0))
            WorksStatistic['NumOfPlay'] = good.NumOfPlay - NumList['NumOfPlay']
            WorksStatistic['NumOfPraiseGet'] = good.NumOfPraiseGet - \
                NumList['NumOfPraiseGet']
            WorksStatistic['NumOfComments'] = good.NumOfComments - \
                NumList['NumOfComments']
            WorksStatistic['NumOfShare'] = good.NumOfShare - \
                NumList['NumOfShare']
    elif workstime == '2':
        beginTime = now
        WorksCountFilter = Q()
        WorksCountFilter = WorksCountFilter & Q(
            videos__works__UploadTime__lte=beginTime)
        WorksCountFilter = WorksCountFilter & Q(id=good.id)
        WorksCountList = Goods.objects.aggregate(
            WorksCount=Count('videos__works', filter=WorksCountFilter))
        WorksStatistic['WorksCount'] = WorksCountList['WorksCount']

        works_id_filter = Goods.objects.filter(
            WorksCountFilter).values_list('videos__works__id', flat=True)
        works_id_list = list(works_id_filter)
        if len(works_id_list) > 0 and works_id_list[0] != None:
            summary_date = now - datetime.timedelta(days=1)
            WorksDaySummary_filter = Q()
            WorksDaySummary_filter = WorksDaySummary_filter & Q(
                Work_id__in=works_id_list)
            WorksDaySummary_filter = WorksDaySummary_filter & Q(
                Summary_Date=summary_date)
            # 播放量, 点赞量， 评论量， 分享量
            NumList = WorksDaySummary.objects.filter(WorksDaySummary_filter).aggregate(NumOfPlay=Coalesce(Sum('NumOfPlay'), 0), NumOfPraiseGet=Coalesce(
                Sum('NumOfPraiseGet'), 0), NumOfComments=Coalesce(Sum('NumOfComments'), 0), NumOfShare=Coalesce(Sum('NumOfShare'), 0))
            WorksStatistic['NumOfPlay'] = NumList['NumOfPlay']
            WorksStatistic['NumOfPraiseGet'] = NumList['NumOfPraiseGet']
            WorksStatistic['NumOfComments'] = NumList['NumOfComments']
            WorksStatistic['NumOfShare'] = NumList['NumOfShare']
    elif workstime == '3':
        beginTime = now + datetime.timedelta(days=1)
        WorksCountFilter = Q()
        WorksCountFilter = WorksCountFilter & Q(
            videos__works__UploadTime__lte=beginTime)
        WorksCountFilter = WorksCountFilter & Q(id=good.id)
        WorksCountList = Goods.objects.aggregate(
            WorksCount=Count('videos__works', filter=WorksCountFilter))
        WorksStatistic['WorksCount'] = WorksCountList['WorksCount']

        works_id_filter = Goods.objects.filter(
            WorksCountFilter).values_list('videos__works__id', flat=True)
        works_id_list = list(works_id_filter)
        if len(works_id_list) > 0 and works_id_list[0] != None:
            this_month_start = datetime.datetime(now.year, now.month, 1)
            summary_date = this_month_start - datetime.timedelta(days=1)
            WorksDaySummary_filter = Q()
            WorksDaySummary_filter = WorksDaySummary_filter & Q(
                Work_id__in=works_id_list)
            WorksDaySummary_filter = WorksDaySummary_filter & Q(
                Summary_Date=summary_date)
            # 播放量, 点赞量， 评论量， 分享量
            NumList = WorksDaySummary.objects.filter(WorksDaySummary_filter).aggregate(NumOfPlay=Coalesce(Sum('NumOfPlay'), 0), NumOfPraiseGet=Coalesce(
                Sum('NumOfPraiseGet'), 0), NumOfComments=Coalesce(Sum('NumOfComments'), 0), NumOfShare=Coalesce(Sum('NumOfShare'), 0))
            WorksStatistic['NumOfPlay'] = good.NumOfPlay - NumList['NumOfPlay']
            WorksStatistic['NumOfPraiseGet'] = good.NumOfPraiseGet - \
                NumList['NumOfPraiseGet']
            WorksStatistic['NumOfComments'] = good.NumOfComments - \
                NumList['NumOfComments']
            WorksStatistic['NumOfShare'] = good.NumOfShare - \
                NumList['NumOfShare']
    elif workstime == '4':
        this_month_start = datetime.datetime(now.year, now.month, 1)
        last_month_end = this_month_start - datetime.timedelta(days=1)
        beginTime = last_month_end
        WorksCountFilter = Q()
        WorksCountFilter = WorksCountFilter & Q(
            videos__works__UploadTime__lte=beginTime)
        WorksCountFilter = WorksCountFilter & Q(id=good.id)
        WorksCountList = Goods.objects.aggregate(
            WorksCount=Count('videos__works', filter=WorksCountFilter))
        WorksStatistic['WorksCount'] = WorksCountList['WorksCount']

        works_id_filter = Goods.objects.filter(
            WorksCountFilter).values_list('videos__works__id', flat=True)
        works_id_list = list(works_id_filter)
        if len(works_id_list) > 0 and works_id_list[0] != None:
            this_month_start = datetime.datetime(now.year, now.month, 1)
            last_month_end = this_month_start - datetime.timedelta(days=1)
            last_month_start = datetime.datetime(
                last_month_end.year, last_month_end.month, 1)
            summary_date_begin = last_month_start - datetime.timedelta(days=1)
            summary_date_end = last_month_end
            WorksDaySummaryBegin_filter = Q()
            WorksDaySummaryBegin_filter = WorksDaySummaryBegin_filter & Q(
                Work_id__in=works_id_list)
            WorksDaySummaryBegin_filter = WorksDaySummaryBegin_filter & Q(
                Summary_Date=summary_date_begin)
            # 播放量, 点赞量， 评论量， 分享量
            NumBeginList = WorksDaySummary.objects.filter(WorksDaySummaryBegin_filter).aggregate(NumOfPlay=Coalesce(Sum('NumOfPlay'), 0), NumOfPraiseGet=Coalesce(
                Sum('NumOfPraiseGet'), 0), NumOfComments=Coalesce(Sum('NumOfComments'), 0), NumOfShare=Coalesce(Sum('NumOfShare'), 0))

            WorksDaySummaryEnd_filter = Q()
            WorksDaySummaryEnd_filter = WorksDaySummaryEnd_filter & Q(
                Work_id__in=works_id_list)
            WorksDaySummaryEnd_filter = WorksDaySummaryEnd_filter & Q(
                Summary_Date=summary_date_end)
            NumEndist = WorksDaySummary.objects.filter(WorksDaySummaryEnd_filter).aggregate(NumOfPlay=Coalesce(Sum('NumOfPlay'), 0), NumOfPraiseGet=Coalesce(
                Sum('NumOfPraiseGet'), 0), NumOfComments=Coalesce(Sum('NumOfComments'), 0), NumOfShare=Coalesce(Sum('NumOfShare'), 0))

            WorksStatistic['NumOfPlay'] = NumEndist['NumOfPlay'] - \
                NumBeginList['NumOfPlay']
            WorksStatistic['NumOfPraiseGet'] = NumEndist['NumOfPraiseGet'] - \
                NumBeginList['NumOfPraiseGet']
            WorksStatistic['NumOfComments'] = NumEndist['NumOfComments'] - \
                NumBeginList['NumOfComments']
            WorksStatistic['NumOfShare'] = NumEndist['NumOfShare'] - \
                NumBeginList['NumOfShare']
    elif workstime == '5':
        this_month_start = datetime.datetime(now.year, now.month, 1)
        last_month_end = this_month_start - datetime.timedelta(days=1)
        last_month_start = datetime.datetime(
            last_month_end.year, last_month_end.month, 1)
        beginTime = last_month_start - datetime.timedelta(days=1)
        WorksCountFilter = Q()
        WorksCountFilter = WorksCountFilter & Q(
            videos__works__UploadTime__lte=beginTime)
        WorksCountFilter = WorksCountFilter & Q(id=good.id)
        WorksCountList = Goods.objects.aggregate(
            WorksCount=Count('videos__works', filter=WorksCountFilter))
        WorksStatistic['WorksCount'] = WorksCountList['WorksCount']

        works_id_filter = Goods.objects.filter(
            WorksCountFilter).values_list('videos__works__id', flat=True)
        works_id_list = list(works_id_filter)
        if len(works_id_list) > 0 and works_id_list[0] != None:
            this_month_start = datetime.datetime(now.year, now.month, 1)
            last_month_end = this_month_start - datetime.timedelta(days=1)
            last_month_start = datetime.datetime(
                last_month_end.year, last_month_end.month, 1)
            last_last_month_end = last_month_start - datetime.timedelta(days=1)
            last_last_month_start = datetime.datetime(
                last_last_month_end.year, last_last_month_end.month, 1)
            summary_date_begin = last_last_month_start - \
                datetime.timedelta(days=1)
            summary_date_end = last_last_month_end
            WorksDaySummaryBegin_filter = Q()
            WorksDaySummaryBegin_filter = WorksDaySummaryBegin_filter & Q(
                Work_id__in=works_id_list)
            WorksDaySummaryBegin_filter = WorksDaySummaryBegin_filter & Q(
                Summary_Date=summary_date_begin)
            # 播放量, 点赞量， 评论量， 分享量
            NumBeginList = WorksDaySummary.objects.filter(WorksDaySummaryBegin_filter).aggregate(NumOfPlay=Coalesce(Sum('NumOfPlay'), 0), NumOfPraiseGet=Coalesce(
                Sum('NumOfPraiseGet'), 0), NumOfComments=Coalesce(Sum('NumOfComments'), 0), NumOfShare=Coalesce(Sum('NumOfShare'), 0))

            WorksDaySummaryEnd_filter = Q()
            WorksDaySummaryEnd_filter = WorksDaySummaryEnd_filter & Q(
                Work_id__in=works_id_list)
            WorksDaySummaryEnd_filter = WorksDaySummaryEnd_filter & Q(
                Summary_Date=summary_date_end)
            NumEndist = WorksDaySummary.objects.filter(WorksDaySummaryEnd_filter).aggregate(NumOfPlay=Coalesce(Sum('NumOfPlay'), 0), NumOfPraiseGet=Coalesce(
                Sum('NumOfPraiseGet'), 0), NumOfComments=Coalesce(Sum('NumOfComments'), 0), NumOfShare=Coalesce(Sum('NumOfShare'), 0))

            WorksStatistic['NumOfPlay'] = NumEndist['NumOfPlay'] - \
                NumBeginList['NumOfPlay']
            WorksStatistic['NumOfPraiseGet'] = NumEndist['NumOfPraiseGet'] - \
                NumBeginList['NumOfPraiseGet']
            WorksStatistic['NumOfComments'] = NumEndist['NumOfComments'] - \
                NumBeginList['NumOfComments']
            WorksStatistic['NumOfShare'] = NumEndist['NumOfShare'] - \
                NumBeginList['NumOfShare']
    return WorksStatistic

# end 商品数据分析


@login_required
def commoditymissionmanage(request):
    location = copy.deepcopy(location_init)
    location['IsCommodityMissionManagePage'] = True
    location['IsCommodityManageMenu'] = True
    context = {'location': location}
    return render(request, 'pages/CommodityManage/CommodityMissionManage.html', context)


@login_required
def commodityselection(request):
    location = copy.deepcopy(location_init)
    location['IsCommoditySelectionPage'] = True
    location['IsCommodityManageMenu'] = True
    context = {'location': location}
    return render(request, 'pages/CommodityManage/CommoditySelection.html', context)


# begin 我的商品
@login_required
def mycommodity(request):
    data_url = request.build_absolute_uri(reverse('Web:GetMyCommodity'))
    create_url = request.build_absolute_uri(reverse('Web:CreateMyCommodity'))
    delete_url = request.build_absolute_uri(reverse('Web:DeleteMyCommodity'))
    gettaobaocommodity_url = request.build_absolute_uri(
        reverse('Web:GetTaoBaoCommodity'))
    get_by_id_url = request.build_absolute_uri(
        reverse('Web:GetMyCommodityById'))
    edit_url = request.build_absolute_uri(reverse('Web:EditMyCommodity'))
    category = GoodClassification.objects.filter(Owner=request.user)
    upload_url = request.build_absolute_uri(reverse('Web:UploadMutiVideo'))
    remove_upload_url = request.build_absolute_uri(reverse('Web:RemoveUploadMutiVideo'))    
    video_category = VideoClassification.objects.filter(Owner=request.user)
    create_video_url = request.build_absolute_uri(
        reverse('Web:CreateMutiVideo'))
    createmutimission_url = request.build_absolute_uri(
        reverse('Web:CreateMutiMission'))
    commoditydataanalysis_url = request.build_absolute_uri(
        reverse('Web:CommodityDataAnalysis'))
    location = copy.deepcopy(location_init)
    location['IsMyCommodityPage'] = True
    location['IsCommodityManageMenu'] = True
    context = {'location': location, 'data_url': data_url, 'delete_url': delete_url,
               'gettaobaocommodity_url': gettaobaocommodity_url, 'create_url': create_url,
               'get_by_id_url': get_by_id_url, 'edit_url': edit_url, 'category': category,
               'upload_url': upload_url, 'video_category': video_category, 'create_video_url': create_video_url,
               'createmutimission_url': createmutimission_url, 'commoditydataanalysis_url': commoditydataanalysis_url,
               'remove_upload_url': remove_upload_url}
    return render(request, 'pages/CommodityManage/MyCommodity.html', context)


@login_required
def getmycommodity(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    generalSearch = request.POST.get('query[generalCommoditySearch]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    commoditytype = request.POST.get('query[commoditytype]')

    owner_id_list = []
    owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)
    data_list = Goods.objects.filter(Owner__id__in=owner_id_list)

    if generalSearch is not None and generalSearch != '':
        data_filter = Q()
        data_filter = data_filter | Q(Title__contains=generalSearch)
        data_filter = data_filter | Q(SubTitle__contains=generalSearch)        
        data_list = data_list.filter(data_filter)

    if commoditytype is not None and commoditytype != '':
        commoditytype_filter = Q()
        if '-1' in commoditytype:
            commoditytype_filter = commoditytype_filter | Q(
                GoodClassifications=None)
        commoditytype_list = commoditytype[:-1].split(',')
        commoditytype_filter = commoditytype_filter | Q(
            GoodClassifications__id__in=commoditytype_list)
        data_list = data_list.filter(commoditytype_filter)

    fields_list = Goods._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    commodity_result = page_result.object_list.values('id', 'Pic1',
                                                      'Title', 'OutSidePlatformID', 'Price',
                                                      'Sales', 'CommissionPercent', 'OutSidePlatformURL',
                                                      'CreateTime', 'SubTitle')
    data = []
    for i in range(len(commodity_result)):
        commodity_id = commodity_result[i]['id']
        commodity = Goods.objects.get(id=commodity_id)
        CategoryString = commodity.GetCategoryString()
        commodity_result[i]['CategoryString'] = CategoryString
        unused = commodity.GetUnusedVideoCount()
        commodity_result[i]['Unused'] = unused
        data.append(commodity_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def delete_mycommodity_by_ids(request):
    ids = request.POST.get('ids')
    id_list = ids[:-1].split(',')
    if len(ids) > 0:
        Goods.objects.filter(id__in=id_list).delete()
    return HttpResponseRedirect(reverse('Web:MyCommodity'))


@login_required
def createmycommodity(request):
    ret = {"status": "NG", "msg": None}
    try:
        outsideplatformid = request.POST.get('outsideplatformid')
        check = Goods.objects.filter(OutSidePlatformID=outsideplatformid, Owner=request.user)
        if check.count() == 0:
            pic1 = request.POST.get('pic1')
            pic2 = request.POST.get('pic2')
            pic3 = request.POST.get('pic3')
            pic4 = request.POST.get('pic4')
            pic5 = request.POST.get('pic5')
            url = request.POST.get('url')
            title = request.POST.get('title')
            subtitle = request.POST.get('subtitle')
            price = request.POST.get('price')
            sales = request.POST.get('sales')
            commissionpercent = request.POST.get('commissionpercent')
            category = request.POST.get('category')
            good = Goods()
            good.Pic1 = pic1
            good.Pic2 = pic2
            good.Pic3 = pic3
            good.Pic4 = pic4
            good.Pic5 = pic5
            good.Title = title
            good.SubTitle = subtitle
            good.OutSidePlatformID = outsideplatformid
            good.Price = price
            good.Sales = sales
            good.CommissionPercent = commissionpercent
            good.OutSidePlatformURL = url
            good.Owner = request.user
            good.save()
            if category is not None and category != '':
                category_list = category[:-1].split(',')
                if len(category_list) > 0:
                    for i in range(len(category_list)):
                        category_id = category_list[i]
                        category = GoodClassification.objects.get(
                            id=category_id)
                        good.GoodClassifications.add(category)
            ret['status'] = 'OK'
            ret['msg'] = reverse('Web:MyCommodity')
        else:
            ret['msg'] = '该商品已存在，无法再次新增'
        return HttpResponse(json.dumps(ret, ensure_ascii=False), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        ret['msg'] = '内部错误'
        return HttpResponse(json.dumps(ret, ensure_ascii=False), content_type="application/json,charset=utf-8")


@login_required
def gettaobaocommodity(request):
    url = request.POST.get('url')

    aliconfig = ALIConfig.objects.filter(Owner=request.user).first()
    adzone = aliconfig.PID

    sessionkey = get_user_session_SessionKey(request.user.id)

    api = 'http://mvapi.vephp.com/hcapi?vekey={}&para={}&pid={}&sessionkey={}&detail=1&notkl=1&noshortlink=1'
    api = api.format(vekey, quote(url), adzone, sessionkey)

    ret = {"status": "NG", "msg": None}

    try:
        resp = requests.get(api)
        result_str = str(resp.content, 'utf-8')
        result = json.loads(result_str)
        data = result['data']
        if data is not None:
            pic1 = data['pict_url']
            pic2 = ''
            pic3 = ''
            pic4 = ''
            pic5 = ''
            small_pic_list = data['small_images']
            if len(small_pic_list) > 0:
                pic2 = small_pic_list[0]
            if len(small_pic_list) > 1:
                pic3 = small_pic_list[1]
            if len(small_pic_list) > 2:
                pic4 = small_pic_list[2]
            if len(small_pic_list) > 3:
                pic5 = small_pic_list[3]
            title = data['title']
            price = data['zk_final_price']
            outsideplatformid = data['num_iid']
            commissionrate = data['commission_rate']
            volume = data['volume']
            context = {'pic1': pic1, 'pic2': pic2, 'pic3': pic3, 'pic4': pic4, 'pic5': pic5,
                       'title': title, 'price': price, 'outsideplatformid': outsideplatformid,
                       'commissionrate': commissionrate, 'volume': volume}
            return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                                content_type="application/json,charset=utf-8")
        else:
            ret['msg'] = result['msg']
            return HttpResponse(json.dumps(ret, ensure_ascii=False), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        ret['msg'] = '内部错误'
        return HttpResponse(json.dumps(ret, ensure_ascii=False), content_type="application/json,charset=utf-8")


@login_required
def editmycommodity(request):
    commodity_id = request.POST.get('id')
    category = request.POST.get('category')
    subtitle = request.POST.get('subtitle')
    commodity = Goods.objects.get(id=commodity_id)
    commodity.SubTitle = subtitle
    commodity.save()
    commodity.GoodClassifications.clear()
    if category is not None and category != '':
        category_list = category[:-1].split(',')
        if len(category_list) > 0:
            for i in range(len(category_list)):
                category_id = category_list[i]
                category = GoodClassification.objects.get(id=category_id)
                commodity.GoodClassifications.add(category)
    return HttpResponse(reverse('Web:MyCommodity'))


@login_required
def getmycommoditybyid(request):
    commodity_id = request.POST.get('id')
    commodity = Goods.objects.get(id=commodity_id)
    if commodity is not None:
        CategoryId = commodity.GetCategoryId()
        context = {
            'pic1': commodity.Pic1,
            'pic2': commodity.Pic2,
            'pic3': commodity.Pic3,
            'pic4': commodity.Pic4,
            'pic5': commodity.Pic5,
            'url': commodity.OutSidePlatformURL,
            'title': commodity.Title,
            'subtitle': commodity.SubTitle,
            'price': commodity.Price,
            'sales': commodity.Sales,
            'commissionpercent': commodity.CommissionPercent,
            'outsideplatformid': commodity.OutSidePlatformID,
            'dataid': commodity.id,
            'categoryid': CategoryId,
        }
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('Error')


@login_required
def uploamutidvideo(request):
    guid = request.POST.get('guid')
    video_file = request.FILES['file']
    video = Videos()
    file_content = ContentFile(video_file.read())  # 创建File对象
    video.URL.save(video_file.name, file_content)  # 保存文件
    video.Remark = guid
    video.FileName = video_file.name    
    video.save()
    return HttpResponse("OK")


@login_required
def createmutivideo(request):
    try:
        title = request.POST.get('title')
        title_list = title.split('\n')
        remark = request.POST.get('remark')
        category = request.POST.get('category')
        commodityid = request.POST.get('commodityid')
        videokeyword = request.POST.get('videokeyword')
        videokeyword_list = videokeyword.split('\n')
        guid = request.POST.get('guid')
        commodity = Goods.objects.get(id=commodityid)
        video_list = list(Videos.objects.filter(
            Remark=guid).values_list('id', flat=True))
        for i in range(len(video_list)):
            videoid = video_list[i]
            video = Videos.objects.get(id=videoid)
            if len(title_list) == 0:
                pertitle = ''
            else:
                pertitle = title_list[i % len(title_list)]
            video.Title = pertitle
            if remark is not None and remark != '':
                video.Remark = remark
            else:
                video.Remark = ''
            if len(videokeyword_list) == 0:
                pervideokeyword = ''
            else:
                pervideokeyword = videokeyword_list[i % len(videokeyword_list)]
            video.VideoKeyword = pervideokeyword
            video.Owner = request.user
            video.Goods = commodity
            video.save()
            if category is not None and category != '':
                category_list = category[:-1].split(',')
                if len(category_list) > 0:
                    for i in range(len(category_list)):
                        category_id = category_list[i]
                        percategory = VideoClassification.objects.get(
                            id=category_id)
                        video.VideoClassifications.add(percategory)
        return HttpResponse(reverse('Web:MyCommodity'))
    except Exception as e:
        print(e)
        return HttpResponse("Error")


@login_required
def createmutimission(request):
    device_id = request.POST.get('deviceid')
    device_id_list = device_id.split(',')
    commodity_id = request.POST.get('commodityid')
    starttime = request.POST.get('starttime')
    commodity = Goods.objects.get(id=commodity_id)
    unusedvideo_id_list = commodity.GetUnusedVideoIDList()
    if len(unusedvideo_id_list) > 0 and len(device_id_list) > 0:
        for i in range(len(unusedvideo_id_list)):
            video = Videos.objects.get(id=unusedvideo_id_list[i])
            if video is not None:
                # 视频地址
                video_url = video.URL.url
                # 视频标题
                video_title = video.Title
                # 话题
                video_keyword = video.VideoKeyword

                # 发布任务
                if i < len(device_id_list):
                    device_id = device_id_list[i]
                    device = MobilePhone.objects.get(id=device_id)
                    if device is not None:

                        # 商品相关
                        good_url = ''
                        good_title = ''
                        good_category = ''
                        if video.Goods is not None and device.ALIConfig is not None:
                            adzone = device.ALIConfig.PID
                            good_id = video.Goods.OutSidePlatformID

                            sessionkey = get_user_session_SessionKey(
                                request.user.id)

                            api = 'http://mvapi.vephp.com/hcapi?vekey={}&para={}&pid={}&sessionkey={}&notkl=1&noshortlink=1&detail=1'
                            api = api.format(
                                vekey, good_id, adzone, sessionkey)

                            try:
                                resp = requests.get(api)
                                result_str = str(resp.content, 'utf-8')
                                result = json.loads(result_str)
                                data = result['data']
                                # 淘宝链接
                                good_url = data['item_url']
                                # 商品短标题
                                good_title = video.Goods.SubTitle
                                # 商品分类
                                good_category = video.Goods.GetCategoryString()
                            except Exception as e:
                                print(e)
                                return HttpResponse("Error")

                        task = VideoMission()
                        task.MobilePhone = device
                        task.Status = TaskStatus[0][0]
                        task.Owner = request.user
                        task.VideoURL = video_url
                        task.VideoTitle = video_title
                        task.VideoKeyword = video_keyword
                        task.GoodURL = good_url
                        task.GoodTitle = good_title
                        task.GoodCategory = good_category
                        task.Video = video
                        if starttime is not None and starttime != '':
                            task.StartTime = datetime.datetime.strptime(
                                starttime, '%Y-%m-%d %H:%M:%S')
                        else:
                            task.StartTime = datetime.datetime.now()
                        task.Priority = -1
                        task.save()
                else:
                    continue
            else:
                return HttpResponse('Error')
        return HttpResponse(reverse('Web:MyCommodity'))
    else:
        return HttpResponse(reverse('Web:MyCommodity'))


@login_required
def removeuploamutidvideo(request):
    uuid = request.POST.get('uuid')
    video_list = Videos.objects.filter(FileName=uuid)
    if video_list.count() == 1:
        video = video_list.first()
        video.URL.delete()
        video.delete()
    return HttpResponse("OK")

# end 我的商品

# begin 商品类别
@login_required
def commoditycategory(request):
    data_url = request.build_absolute_uri(reverse('Web:GetCommodityCategory'))
    create_url = request.build_absolute_uri(
        reverse('Web:CreateCommodityCategory'))
    delete_url = request.build_absolute_uri(
        reverse('Web:DeleteCommodityCategory'))
    get_by_id_url = request.build_absolute_uri(
        reverse('Web:GetCommodityCategoryByID'))
    edit_url = request.build_absolute_uri(reverse('Web:EditCommodityCategory'))
    location = copy.deepcopy(location_init)
    location['IsCommodityCategoryPage'] = True
    location['IsCommodityManageMenu'] = True
    context = {'location': location, 'data_url': data_url, 'delete_url': delete_url,
               'create_url': create_url, 'get_by_id_url': get_by_id_url, 'edit_url': edit_url}
    return render(request, 'pages/CommodityManage/CommodityCategory.html', context)


@login_required
def getcommoditycategory(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
 
    owner_id_list = []
    owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)
    data_list = GoodClassification.objects.filter(Owner__id__in=owner_id_list)

    fields_list = GoodClassification._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values('id', 'Name')
    data = []
    for i in range(len(data_result)):
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def delete_commoditycategory_by_ids(request):
    ids = request.POST.get('ids')
    id_list = ids[:-1].split(',')
    if len(ids) > 0:
        GoodClassification.objects.filter(id__in=id_list).delete()
    return HttpResponseRedirect(reverse('Web:CommodityCategory'))


@login_required
def createcommoditycategory(request):
    try:
        name = request.POST.get('name')
        goodClassification = GoodClassification()
        goodClassification.Name = name
        goodClassification.Owner = request.user
        goodClassification.save()
        return HttpResponse(reverse('Web:CommodityCategory'))
    except Exception as e:
        print(e)
        return HttpResponse("Error")


@login_required
def editcommoditycategory(request):
    data_id = request.POST.get('id')
    name = request.POST.get('name')
    commodity = GoodClassification.objects.get(id=data_id)
    commodity.Name = name
    commodity.save()
    return HttpResponse(reverse('Web:CommodityCategory'))


@login_required
def getcommoditycategorybyid(request):
    data_id = request.POST.get('id')
    data = GoodClassification.objects.get(id=data_id)
    context = {
        'name': data.Name,
        'dataid': data.id,
    }
    if data is not None:
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('Error')


# end 商品类别

# begin 我的视频
@login_required
def myvideo(request):
    data_url = request.build_absolute_uri(reverse('Web:GetMyVideo'))
    create_url = request.build_absolute_uri(reverse('Web:CreateMyVideo'))
    delete_url = request.build_absolute_uri(reverse('Web:DeleteMyVideo'))
    get_by_id_url = request.build_absolute_uri(reverse('Web:GetMyVideobyID'))
    edit_url = request.build_absolute_uri(reverse('Web:EditMyVideo'))
    upload_url = request.build_absolute_uri(reverse('Web:UploadMyVideo'))
    remove_upload_url = request.build_absolute_uri(reverse('Web:RemoveUploadMyVideo'))
    get_video_url_url = request.build_absolute_uri(
        reverse('Web:GetMyVideoURLByID'))
    commodity_data_url = request.build_absolute_uri(
        reverse('Web:GetMyCommodity'))
    get_commodity_by_id_url = request.build_absolute_uri(
        reverse('Web:GetMyCommodityById'))
    createvideomission_url = request.build_absolute_uri(
        reverse('Web:CreateVideoMission'))
    video_category = VideoClassification.objects.filter(Owner=request.user)
    commodity_category = GoodClassification.objects.filter(Owner=request.user)
    location = copy.deepcopy(location_init)
    location['IsMyVideoPage'] = True
    location['IsVideoManageMenu'] = True
    context = {'location': location, 'data_url': data_url, 'delete_url': delete_url,
               'create_url': create_url, 'get_by_id_url': get_by_id_url, 'edit_url': edit_url,
               'video_category': video_category,
               'upload_url': upload_url, 'get_video_url_url': get_video_url_url,
               'commodity_data_url': commodity_data_url,
               'commodity_category': commodity_category, 'get_commodity_by_id_url': get_commodity_by_id_url,
               'createvideomission_url': createvideomission_url, 'remove_upload_url': remove_upload_url}
    return render(request, 'pages/VideoManage/MyVideo.html', context)


@login_required
def getmyvideo(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    generalSearch = request.POST.get('query[generalVideoSearch]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    videotype = request.POST.get('query[videotype]')
    videostatus = request.POST.get('query[videostatus]')
    hascommodity = request.POST.get('query[hascommodity]')
    myvideocolumn = request.POST.get('query[myvideocolumn]')     

    owner_id_list = []
    owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)
    data_list = Videos.objects.filter(Owner__id__in=owner_id_list)

    if generalSearch is not None and generalSearch != '':
        search_filter = Q()
        if myvideocolumn == 'title':
            search_filter = search_filter | Q(Title__contains=generalSearch)
        elif myvideocolumn == 'keyword':
            search_filter = search_filter | Q(
                VideoKeyword__contains=generalSearch)
        elif myvideocolumn == 'goodtitle':
            search_filter = search_filter | Q(
                Goods__Title__contains=generalSearch)
        else:
            search_filter = search_filter | Q(Title__contains=generalSearch)
            search_filter = search_filter | Q(
                VideoKeyword__contains=generalSearch)
            search_filter = search_filter | Q(
                Goods__Title__contains=generalSearch)
        data_list = data_list.filter(search_filter)

    if videotype is not None and videotype != '':
        videotype_filter = Q()
        if '-1' in videotype:
            videotype_filter = videotype_filter | Q(VideoClassifications=None)
        videotype_list = videotype[:-1].split(',')
        videotype_filter = videotype_filter | Q(
            VideoClassifications__id__in=videotype_list)
        data_list = data_list.filter(videotype_filter)

    if videostatus is not None and videostatus != '':
        if videostatus == 'True':
            missions = VideoMission.objects.filter(Status=2)
            missions = missions.exclude(Video=None)
            if missions.count() > 0:
                missions_video_id_list = list(
                    missions.values_list('Video__id', flat=True).distinct())
                data_list = data_list.filter(id__in=missions_video_id_list)
            else:
                data_list = data_list.filter(id=-1)
        else:
            missions = VideoMission.objects.filter(Status=2)
            missions = missions.exclude(Video=None)
            if missions.count() > 0:
                missions_video_id_list = list(
                    missions.values_list('Video__id', flat=True).distinct())
                data_list = data_list.exclude(id__in=missions_video_id_list)

    if hascommodity is not None and hascommodity != '':
        if hascommodity == 'True':
            data_list = data_list.filter(~Q(Goods=None))
        else:
            data_list = data_list.filter(Goods=None)

    fields_list = Videos._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')        

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    video_result = page_result.object_list.values(
        'id', 'Remark', 'Title', 'CreateTime', 'VideoKeyword',
        'Goods__Title')
    data = []
    for i in range(len(video_result)):
        video_id = video_result[i]['id']
        video = Videos.objects.get(id=video_id)
        CategoryString = video.GetCategoryString()
        video_result[i]['CategoryString'] = CategoryString
        video_result[i]['VideoStatus'] = video.GetVideoStatus()
        data.append(video_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def delete_myvideo_by_ids(request):
    ids = request.POST.get('ids')
    id_list = ids[:-1].split(',')
    if len(id_list) > 0:
        for i in range(len(id_list)):
            video_id = id_list[i]
            video = Videos.objects.get(id=video_id)
            video.URL.delete()
            video.delete()
    return HttpResponseRedirect(reverse('Web:MyVideo'))


@login_required
def createmyvideo(request):
    try:
        title = request.POST.get('title')
        title_list = title.split('\n')
        remark = request.POST.get('remark')
        category = request.POST.get('category')
        commodityid = request.POST.get('commodityid')
        videokeyword = request.POST.get('videokeyword')
        videokeyword_list = videokeyword.split('\n')
        guid = request.POST.get('guid')        
        video_list = list(Videos.objects.filter(
            Remark=guid).values_list('id', flat=True))
        for i in range(len(video_list)):
            videoid = video_list[i]
            video = Videos.objects.get(id=videoid)
            if len(title_list) == 0:
                pertitle = ''
            else:
                pertitle = title_list[i % len(title_list)]
            video.Title = pertitle
            if remark is not None and remark != '':
                video.Remark = remark
            else:
                video.Remark = ''
            if len(videokeyword_list) == 0:
                pervideokeyword = ''
            else:
                pervideokeyword = videokeyword_list[i % len(videokeyword_list)]
            video.VideoKeyword = pervideokeyword
            video.Owner = request.user
            if commodityid is not None and commodityid != '':
                commodity = Goods.objects.get(id=commodityid)
                video.Goods = commodity
            video.save()
            if category is not None and category != '':
                category_list = category[:-1].split(',')
                if len(category_list) > 0:
                    for i in range(len(category_list)):
                        category_id = category_list[i]
                        percategory = VideoClassification.objects.get(
                            id=category_id)
                        video.VideoClassifications.add(percategory)        
        return HttpResponse(reverse('Web:MyVideo'))
    except Exception as e:
        print(e)
        return HttpResponse("Error")


@login_required
def editmyvideo(request):
    video_id = request.POST.get('id')
    title = request.POST.get('title')
    remark = request.POST.get('remark')
    category = request.POST.get('category')
    commodityid = request.POST.get('commodityid')
    videokeyword = request.POST.get('videokeyword')
    video = Videos.objects.get(id=video_id)
    video.Title = title
    video.Remark = remark
    video.VideoKeyword = videokeyword
    if commodityid is not None and commodityid != '':
        commodity = Goods.objects.get(id=commodityid)
        video.Goods = commodity
    else:
        video.Goods = None
    video.save()
    video.VideoClassifications.clear()
    if category is not None and category != '':
        category_list = category[:-1].split(',')
        if len(category_list) > 0:
            for i in range(len(category_list)):
                category_id = category_list[i]
                category = VideoClassification.objects.get(id=category_id)
                video.VideoClassifications.add(category)
    return HttpResponse(reverse('Web:MyVideo'))


@login_required
def uploadmyvideo(request):
    guid = request.POST.get('guid')
    video_file = request.FILES['file']
    video = Videos()
    file_content = ContentFile(video_file.read())  # 创建File对象
    video.URL.save(video_file.name, file_content)  # 保存文件
    video.Remark = guid
    video.FileName = video_file.name    
    video.save()
    return HttpResponse("OK")


@login_required
def getmyvideobyid(request):
    video_id = request.POST.get('id')
    video = Videos.objects.get(id=video_id)
    if video is not None:
        CommodityName = video.GetCommodityName()
        CommodityId = video.GetCommodityId()
        CategoryId = video.GetCategoryId()
        context = {
            'title': video.Title,
            'url': video.URL.url,
            'remark': video.Remark,
            'dataid': video.id,
            'categoryid': CategoryId,
            'commodityname': CommodityName,
            'commodityid': CommodityId,
            'videokeyword': video.VideoKeyword,
        }
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('Error')


@login_required
def getmyvideourlbyid(request):
    video_id = request.POST.get('id')
    video = Videos.objects.get(id=video_id)
    if video is not None:
        context = {
            'url': video.URL.url,
        }
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('Error')


@login_required
def createvideomission(request):
    device_id = request.POST.get('deviceid')
    device_id_list = device_id.split(',')
    data_id = request.POST.get('dataid')
    keyword = request.POST.get('keyword')
    starttime = request.POST.get('starttime')
    video = Videos.objects.get(id=data_id)
    if video is not None and len(device_id_list) > 0:
        # 视频地址
        video_url = video.URL.url
        # 视频标题
        video_title = video.Title
        # 话题
        video_keyword = keyword

        # 发布任务
        for i in range(len(device_id_list)):
            id = device_id_list[i]
            device = MobilePhone.objects.get(id=id)
            if device is not None:

                # 商品相关
                good_url = ''
                good_title = ''
                good_category = ''
                if video.Goods is not None and device.ALIConfig is not None:
                    adzone = device.ALIConfig.PID
                    good_id = video.Goods.OutSidePlatformID

                    sessionkey = get_user_session_SessionKey(request.user.id)

                    api = 'http://mvapi.vephp.com/hcapi?vekey={}&para={}&pid={}&sessionkey={}&notkl=1&noshortlink=1&detail=1'
                    api = api.format(vekey, good_id, adzone, sessionkey)

                    try:
                        resp = requests.get(api)
                        result_str = str(resp.content, 'utf-8')
                        result = json.loads(result_str)
                        data = result['data']
                        # 淘宝链接
                        good_url = data['item_url']
                        # 商品短标题
                        good_title = video.Goods.SubTitle
                        # 商品分类
                        good_category = video.Goods.GetCategoryString()
                    except Exception as e:
                        print(e)
                        return HttpResponse("Error")

                task = VideoMission()
                task.MobilePhone = device
                task.Status = TaskStatus[0][0]
                task.Owner = request.user
                task.VideoURL = video_url
                task.VideoTitle = video_title
                task.VideoKeyword = video_keyword
                task.GoodURL = good_url
                task.GoodTitle = good_title
                task.GoodCategory = good_category
                task.Video = video
                if starttime is not None and starttime != '':
                    task.StartTime = datetime.datetime.strptime(
                        starttime, '%Y-%m-%d %H:%M:%S')
                else:
                    task.StartTime = datetime.datetime.now()
                task.Priority = -1
                task.save()
            else:
                continue
        return HttpResponse(reverse('Web:MyVideo'))
    else:
        return HttpResponse('Error')


@login_required
def removeuploadmyvideo(request):
    uuid = request.POST.get('uuid')
    video_list = Videos.objects.filter(FileName=uuid)
    if video_list.count() == 1:
        video = video_list.first()
        video.URL.delete()
        video.delete()
    return HttpResponse("OK")

# end 我的视频


@login_required
def ordercollect(request):
    location = copy.deepcopy(location_init)
    location['IsOrderCollectPage'] = True
    location['IsMyAgentMenu'] = True
    context = {'location': location}
    return render(request, 'pages/MyAgent/OrderCollect.html', context)


# begin 视频数据分析

@login_required
def worksdataanalysis(request):
    data_url = request.build_absolute_uri(reverse('Web:GetWorksDataAnalysis'))
    acountlist_url = request.build_absolute_uri(reverse('Web:AccountList'))
    history_data_url = request.build_absolute_uri(
        reverse('Web:GetHistoryData'))
    owner_id_list = []
    owner_id_list = GetOwnerIDList(request.user.id, owner_id_list)        
    video_category = VideoClassification.objects.filter(Owner__id__in=owner_id_list).values('Name').distinct()
    groups = TikTokAccountGroup.objects.filter(Owner__id__in=owner_id_list).values('Name').distinct()
    classifications = MaintenanceNumberMissionKeywordClassification.objects.filter(Owner__id__in=owner_id_list).values('Name').distinct()
    owners = []
    for i in range(len(owner_id_list)):
        owner_id = owner_id_list[i]
        user = User.objects.get(id=owner_id)
        owners.append(user)    
    location = copy.deepcopy(location_init)
    location['IsWorksDataAnalysisPage'] = True
    location['IsDataAnalysisMenu'] = True
    context = {'location': location, 'data_url': data_url,
               'acountlist_url': acountlist_url, 'video_category': video_category,
               'groups': groups, 'classifications': classifications, 'history_data_url': history_data_url,
               'owners': owners}
    return render(request, 'pages/DataAnalysis/WorksDataAnalysis.html', context)


@login_required
def getworksdataanalysis(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    generalSearch = request.POST.get('query[generalWorksDataAnalysisSearch]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    workstime = request.POST.get('query[workstime]')
    videotype = request.POST.get('query[videotype]')
    tag = request.POST.get('query[tag]')
    group = request.POST.get('query[group]')
    starttime = request.POST.get('query[starttime]')
    endtime = request.POST.get('query[endtime]')
    worksdataanalysiscolumn = request.POST.get(
        'query[worksdataanalysiscolumn]')
    owner = request.POST.get('query[owner]')        

    works_filter = Q()
    works_filter = works_filter & Q(~Q(Pic=None))
    if owner is not None and owner != '':
        works_filter =  works_filter & Q(TikTokAccount__Owner__id=owner)
    else:
        owner_id_list = []
        owner_id_list = GetOwnerIDList(request.user.id, owner_id_list)
        works_filter = works_filter & Q(TikTokAccount__Owner__id__in=owner_id_list)
    works_list = Works.objects.filter(works_filter)    
    WorksDataAnalysis.objects.filter(Owner=request.user).delete()
    now = datetime.date.today()
    for i in range(len(works_list)):
        works_id = works_list[i].id
        work = Works.objects.get(id=works_id)
        data_analysis = WorksDataAnalysis()
        data_analysis.Works = work
        WorkStatistic = getWorkStatisticByWorktime(work, workstime)
        # 播放量
        data_analysis.NumOfPlay = WorkStatistic['NumOfPlay']
        # 点赞量
        data_analysis.NumOfPraiseGet = WorkStatistic['NumOfPraiseGet']
        # 评论量
        data_analysis.NumOfComments = WorkStatistic['NumOfComments']
        # 分享量
        data_analysis.NumOfShare = WorkStatistic['NumOfShare']
        data_analysis.Owner = request.user
        data_analysis.save()

    data_list = WorksDataAnalysis.objects.filter(Owner=request.user)
    if generalSearch is not None and generalSearch != '':
        search_filter = Q()
        if worksdataanalysiscolumn == 'describe':
            search_filter = search_filter | Q(
                Works__Describe__contains=generalSearch)
        elif worksdataanalysiscolumn == 'tiktok':
            search_filter = search_filter | Q(
                Works__TikTokAccount__NickName__contains=generalSearch)
        else:
            search_filter = search_filter | Q(
                Works__Describe__contains=generalSearch)
            search_filter = search_filter | Q(
                Works__TikTokAccount__NickName__contains=generalSearch)
        data_list = data_list.filter(search_filter)

    if videotype is not None and videotype != '':
        videotype_filter = Q()
        if '-1' in videotype:
            videotype_filter = videotype_filter | Q(
                Works__Video__VideoClassifications=None)
        videotype_list = videotype[:-1].split(',')
        videotype_filter = videotype_filter | Q(
            Works__Video__VideoClassifications__Name__in=videotype_list)
        data_list = data_list.filter(videotype_filter)

    if tag is not None and tag != '':
        tag_filter = Q()
        if '-1' in tag:
            tag_filter = tag_filter | Q(
                Works__TikTokAccount__Classification=None)
        tag_list = tag[:-1].split(',')
        tag_filter = tag_filter | Q(
            Works__TikTokAccount__Classification__Name__in=tag_list)
        data_list = data_list.filter(tag_filter)

    if group is not None and group != '':
        group_filter = Q()
        if '-1' in group:
            group_filter = group_filter | Q(Works__TikTokAccount__Group=None)
        group_list = group[:-1].split(',')
        group_filter = group_filter | Q(
            Works__TikTokAccount__Group__Name__in=group_list)
        data_list = data_list.filter(group_filter)

    if starttime is not None and starttime != '' and endtime is not None and endtime != '':
        data_list = data_list.filter(
            Works__UploadTime__range=(starttime, endtime))
    elif starttime is not None and starttime != '':
        data_list = data_list.filter(Works__UploadTime__gte=starttime)
    elif endtime is not None and endtime != '':
        data_list = data_list.filter(Works__UploadTime__lte=endtime)

    if field is not None and field != '':
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')        

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values('id', 'Works__id', 'Works__Pic', 'Works__Describe', 'Works__UpdateTime', 'Works__ShareURL',
                                                 'Works__UploadTime', 'NumOfPlay', 'NumOfPraiseGet', 'NumOfComments', 'NumOfShare',
                                                 'Works__TikTokAccount__NickName', 'Works__TikTokAccount__Group__Name',
                                                 'Works__TikTokAccount__id', 'Works__TikTokAccount__Owner__username')
    data = []
    for i in range(len(data_result)):
        works_id = data_result[i]['Works__id']
        work = Works.objects.get(id=works_id)
        if work.Video is not None:
            Video_CategoryString = work.Video.GetCategoryString()
            data_result[i]['Video_CategoryString'] = Video_CategoryString
        else:
            data_result[i]['Video_CategoryString'] = ''

        tiktokaccount_id = data_result[i]['Works__TikTokAccount__id']
        tiktokaccount = TikTokAccount.objects.get(id=tiktokaccount_id)
        tiktokaccount_classification = tiktokaccount.GetClassificationString()
        data_result[i]['tiktokaccount_classification'] = tiktokaccount_classification

        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


def getWorkStatisticByWorktime(work, workstime):
    WorksStatistic = {'NumOfPlay': 0, 'NumOfPraiseGet': 0,
                      'NumOfComments': 0, 'NumOfShare': 0}
    # 0:全部 1:今天 2:昨天 3:本月 4:上月 5:上上月
    beginTime = ''
    endTime = ''
    now = datetime.date.today()
    if workstime is None or workstime == '0':
        WorksStatistic['NumOfPlay'] = work.NumOfPlay
        WorksStatistic['NumOfPraiseGet'] = work.NumOfPraiseGet
        WorksStatistic['NumOfComments'] = work.NumOfComments
        WorksStatistic['NumOfShare'] = work.NumOfShare
    elif workstime == '1':
        summary_date = now - datetime.timedelta(days=1)
        WorksDaySummary_filter = Q()
        WorksDaySummary_filter = WorksDaySummary_filter & Q(Work_id=work.id)
        WorksDaySummary_filter = WorksDaySummary_filter & Q(
            Summary_Date=summary_date)
        # 播放量, 点赞量， 评论量， 分享量
        workdaysummary_list = WorksDaySummary.objects.filter(
            WorksDaySummary_filter)
        if workdaysummary_list.count() > 0:
            workdaysummary = workdaysummary_list.first()
            WorksStatistic['NumOfPlay'] = work.NumOfPlay - \
                workdaysummary.NumOfPlay
            WorksStatistic['NumOfPraiseGet'] = work.NumOfPraiseGet - \
                workdaysummary.NumOfPraiseGet
            WorksStatistic['NumOfComments'] = work.NumOfComments - \
                workdaysummary.NumOfComments
            WorksStatistic['NumOfShare'] = work.NumOfShare - \
                workdaysummary.NumOfShare
        else:
            WorksStatistic['NumOfPlay'] = work.NumOfPlay
            WorksStatistic['NumOfPraiseGet'] = work.NumOfPraiseGet
            WorksStatistic['NumOfComments'] = work.NumOfComments
            WorksStatistic['NumOfShare'] = work.NumOfShare
    elif workstime == '2':
        summary_date = now - datetime.timedelta(days=1)
        WorksDaySummary_filter = Q()
        WorksDaySummary_filter = WorksDaySummary_filter & Q(Work_id=work.id)
        WorksDaySummary_filter = WorksDaySummary_filter & Q(
            Summary_Date=summary_date)
        # 播放量, 点赞量， 评论量， 分享量
        workdaysummary_list = WorksDaySummary.objects.filter(
            WorksDaySummary_filter)
        if workdaysummary_list.count() > 0:
            workdaysummary = workdaysummary_list.first()
            WorksStatistic['NumOfPlay'] = workdaysummary.NumOfPlay
            WorksStatistic['NumOfPraiseGet'] = workdaysummary.NumOfPraiseGet
            WorksStatistic['NumOfComments'] = workdaysummary.NumOfComments
            WorksStatistic['NumOfShare'] = workdaysummary.NumOfShare
    elif workstime == '3':
        this_month_start = datetime.datetime(now.year, now.month, 1)
        summary_date = this_month_start - datetime.timedelta(days=1)
        WorksDaySummary_filter = Q()
        WorksDaySummary_filter = WorksDaySummary_filter & Q(Work_id=work.id)
        WorksDaySummary_filter = WorksDaySummary_filter & Q(
            Summary_Date=summary_date)
        # 播放量, 点赞量， 评论量， 分享量
        workdaysummary_list = WorksDaySummary.objects.filter(
            WorksDaySummary_filter)
        if workdaysummary_list.count() > 0:
            workdaysummary = workdaysummary_list.first()
            WorksStatistic['NumOfPlay'] = work.NumOfPlay - \
                workdaysummary.NumOfPlay
            WorksStatistic['NumOfPraiseGet'] = work.NumOfPraiseGet - \
                workdaysummary.NumOfPraiseGet
            WorksStatistic['NumOfComments'] = work.NumOfComments - \
                workdaysummary.NumOfComments
            WorksStatistic['NumOfShare'] = work.NumOfShare - \
                workdaysummary.NumOfShare
        else:
            WorksStatistic['NumOfPlay'] = work.NumOfPlay
            WorksStatistic['NumOfPraiseGet'] = work.NumOfPraiseGet
            WorksStatistic['NumOfComments'] = work.NumOfComments
            WorksStatistic['NumOfShare'] = work.NumOfShare
    elif workstime == '4':
        this_month_start = datetime.datetime(now.year, now.month, 1)
        last_month_end = this_month_start - datetime.timedelta(days=1)
        last_month_start = datetime.datetime(
            last_month_end.year, last_month_end.month, 1)
        summary_date_begin = last_month_start - datetime.timedelta(days=1)
        summary_date_end = last_month_end
        WorksDaySummaryBegin_filter = Q()
        WorksDaySummaryBegin_filter = WorksDaySummaryBegin_filter & Q(
            Work_id=work.id)
        WorksDaySummaryBegin_filter = WorksDaySummaryBegin_filter & Q(
            Summary_Date=summary_date_begin)
        # 播放量, 点赞量， 评论量， 分享量
        NumBeginList = WorksDaySummary.objects.filter(WorksDaySummaryBegin_filter).aggregate(NumOfPlay=Coalesce(Sum('NumOfPlay'), 0), NumOfPraiseGet=Coalesce(
            Sum('NumOfPraiseGet'), 0), NumOfComments=Coalesce(Sum('NumOfComments'), 0), NumOfShare=Coalesce(Sum('NumOfShare'), 0))

        WorksDaySummaryEnd_filter = Q()
        WorksDaySummaryEnd_filter = WorksDaySummaryEnd_filter & Q(
            Work_id=work.id)
        WorksDaySummaryEnd_filter = WorksDaySummaryEnd_filter & Q(
            Summary_Date=summary_date_end)
        NumEndist = WorksDaySummary.objects.filter(WorksDaySummaryEnd_filter).aggregate(NumOfPlay=Coalesce(Sum('NumOfPlay'), 0), NumOfPraiseGet=Coalesce(
            Sum('NumOfPraiseGet'), 0), NumOfComments=Coalesce(Sum('NumOfComments'), 0), NumOfShare=Coalesce(Sum('NumOfShare'), 0))

        WorksStatistic['NumOfPlay'] = NumEndist['NumOfPlay'] - \
            NumBeginList['NumOfPlay']
        WorksStatistic['NumOfPraiseGet'] = NumEndist['NumOfPraiseGet'] - \
            NumBeginList['NumOfPraiseGet']
        WorksStatistic['NumOfComments'] = NumEndist['NumOfComments'] - \
            NumBeginList['NumOfComments']
        WorksStatistic['NumOfShare'] = NumEndist['NumOfShare'] - \
            NumBeginList['NumOfShare']
    elif workstime == '5':
        this_month_start = datetime.datetime(now.year, now.month, 1)
        last_month_end = this_month_start - datetime.timedelta(days=1)
        last_month_start = datetime.datetime(
            last_month_end.year, last_month_end.month, 1)
        last_last_month_end = last_month_start - datetime.timedelta(days=1)
        last_last_month_start = datetime.datetime(
            last_last_month_end.year, last_last_month_end.month, 1)
        summary_date_begin = last_last_month_start - datetime.timedelta(days=1)
        summary_date_end = last_last_month_end
        WorksDaySummaryBegin_filter = Q()
        WorksDaySummaryBegin_filter = WorksDaySummaryBegin_filter & Q(
            Work_id=work.id)
        WorksDaySummaryBegin_filter = WorksDaySummaryBegin_filter & Q(
            Summary_Date=summary_date_begin)
        # 播放量, 点赞量， 评论量， 分享量
        NumBeginList = WorksDaySummary.objects.filter(WorksDaySummaryBegin_filter).aggregate(NumOfPlay=Coalesce(Sum('NumOfPlay'), 0), NumOfPraiseGet=Coalesce(
            Sum('NumOfPraiseGet'), 0), NumOfComments=Coalesce(Sum('NumOfComments'), 0), NumOfShare=Coalesce(Sum('NumOfShare'), 0))

        WorksDaySummaryEnd_filter = Q()
        WorksDaySummaryEnd_filter = WorksDaySummaryEnd_filter & Q(
            Work_id=work.id)
        WorksDaySummaryEnd_filter = WorksDaySummaryEnd_filter & Q(
            Summary_Date=summary_date_end)
        NumEndist = WorksDaySummary.objects.filter(WorksDaySummaryEnd_filter).aggregate(NumOfPlay=Coalesce(Sum('NumOfPlay'), 0), NumOfPraiseGet=Coalesce(
            Sum('NumOfPraiseGet'), 0), NumOfComments=Coalesce(Sum('NumOfComments'), 0), NumOfShare=Coalesce(Sum('NumOfShare'), 0))

        WorksStatistic['NumOfPlay'] = NumEndist['NumOfPlay'] - \
            NumBeginList['NumOfPlay']
        WorksStatistic['NumOfPraiseGet'] = NumEndist['NumOfPraiseGet'] - \
            NumBeginList['NumOfPraiseGet']
        WorksStatistic['NumOfComments'] = NumEndist['NumOfComments'] - \
            NumBeginList['NumOfComments']
        WorksStatistic['NumOfShare'] = NumEndist['NumOfShare'] - \
            NumBeginList['NumOfShare']
    return WorksStatistic


@login_required
def gethistorydata(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    workid = request.POST.get('query[workid]')

    now = datetime.date.today()
    TotalEndTime = now - datetime.timedelta(days=1)
    TotalBeginTime = TotalEndTime - datetime.timedelta(days=29)

    data_filter = Q()
    data_filter = data_filter & Q(
        Summary_Date__range=(TotalBeginTime, TotalEndTime))
    data_filter = data_filter & Q(Work__id=workid)
    data_list = WorksDaySummary.objects.filter(data_filter)

    if field is not None and field != '':
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('-Summary_Date')        

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values('id', 'Summary_Date', 'Work__id', 'Work__Pic', 'Work__Describe',
                                                 'NumOfPlay', 'NumOfPraiseGet', 'NumOfComments', 'NumOfShare',
                                                 'Work__TikTokAccount__NickName')
    data = []
    for i in range(len(data_result)):
        works_id = data_result[i]['Work__id']
        work = Works.objects.get(id=works_id)
        if work.Video is not None:
            Video_CategoryString = work.Video.GetCategoryString()
            data_result[i]['Video_CategoryString'] = Video_CategoryString
        else:
            data_result[i]['Video_CategoryString'] = ''
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")

# end 视频数据分析


# begin 视频标签
@login_required
def videolabel(request):
    data_url = request.build_absolute_uri(reverse('Web:GetVideoLabel'))
    create_url = request.build_absolute_uri(reverse('Web:CreateVideoLabel'))
    delete_url = request.build_absolute_uri(
        reverse('Web:DeleteVideoLabel'))
    get_by_id_url = request.build_absolute_uri(
        reverse('Web:GetVideoLabelByID'))
    edit_url = request.build_absolute_uri(reverse('Web:EditVideoLabel'))
    location = copy.deepcopy(location_init)
    location['IsVideoLabelPage'] = True
    location['IsVideoManageMenu'] = True
    context = {'location': location, 'data_url': data_url, 'delete_url': delete_url,
               'create_url': create_url, 'get_by_id_url': get_by_id_url, 'edit_url': edit_url}
    return render(request, 'pages/VideoManage/VideoLabel.html', context)


@login_required
def getvideolabel(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')

    owner_id_list = []
    owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)
    data_list = VideoClassification.objects.filter(Owner__id__in=owner_id_list)

    fields_list = VideoClassification._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')        

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values('id', 'Name')
    data = []
    for i in range(len(data_result)):
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def delete_videolabel_by_ids(request):
    ids = request.POST.get('ids')
    id_list = ids[:-1].split(',')
    if len(ids) > 0:
        VideoClassification.objects.filter(id__in=id_list).delete()
    return HttpResponseRedirect(reverse('Web:VideoLabel'))


@login_required
def createvideolabel(request):
    try:
        name = request.POST.get('name')
        videoClassification = VideoClassification()
        videoClassification.Name = name
        videoClassification.Owner = request.user
        videoClassification.save()
        return HttpResponse(reverse('Web:VideoLabel'))
    except Exception as e:
        print(e)
        return HttpResponse("Error")


@login_required
def editvideolabel(request):
    data_id = request.POST.get('id')
    name = request.POST.get('name')
    videoClassification = VideoClassification.objects.get(id=data_id)
    videoClassification.Name = name
    videoClassification.save()
    return HttpResponse(reverse('Web:VideoLabel'))


@login_required
def getvideolabelbyid(request):
    data_id = request.POST.get('id')
    data = VideoClassification.objects.get(id=data_id)
    context = {
        'name': data.Name,
        'dataid': data.id,
    }
    if data is not None:
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('Error')


# end 视频标签

# begin 视频任务
@login_required
def videomission(request):
    data_url = request.build_absolute_uri(reverse('Web:GetVideoMission'))
    delete_url = request.build_absolute_uri(reverse('Web:DeleteVideoMission'))
    get_by_id_url = request.build_absolute_uri(
        reverse('Web:GetVideoMissionByID'))
    edit_url = request.build_absolute_uri(reverse('Web:EditVideoMission'))
    relaunchvideomission_url = request.build_absolute_uri(reverse('Web:RelaunchVideoMission'))    
    video_category = VideoClassification.objects.filter(Owner=request.user)
    commodity_category = GoodClassification.objects.filter(Owner=request.user)
    location = copy.deepcopy(location_init)
    location['IsVideoMissionPage'] = True
    location['IsVideoManageMenu'] = True
    context = {'location': location, 'data_url': data_url, 'delete_url': delete_url,
               'get_by_id_url': get_by_id_url, 'edit_url': edit_url, 'mission_status': TaskStatus,
               'video_category': video_category, 'commodity_category': commodity_category,
               'relaunchvideomission_url': relaunchvideomission_url}
    return render(request, 'pages/VideoManage/VideoMission.html', context)


@login_required
def getvideomission(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    generalSearch = request.POST.get('query[generalVideoMissionSearch]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    status = request.POST.get('query[status]')
    commoditytype = request.POST.get('query[commoditytype]')
    videotype = request.POST.get('query[videotype]')
    videomissioncolumn = request.POST.get('query[videomissioncolumn]') 
    starttime = request.POST.get('query[starttime]')    
    endtime = request.POST.get('query[endtime]')          

    owner_id_list = []
    owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)
    data_list = VideoMission.objects.filter(Owner__id__in=owner_id_list)

    if generalSearch is not None and generalSearch != '':
        search_filter = Q()
        if videomissioncolumn == 'videotitle':
            search_filter = search_filter | Q(VideoTitle__contains=generalSearch)
        elif videomissioncolumn == 'keyword':
            search_filter = search_filter | Q(
                VideoKeyword__contains=generalSearch)
        elif videomissioncolumn == 'goodtitle':
            search_filter = search_filter | Q(
                GoodTitle__contains=generalSearch)
        elif videomissioncolumn == 'mobileid':
            if str.isdigit(generalSearch):
                search_filter = search_filter | Q(MobilePhone__id=generalSearch)
        else:
            search_filter = search_filter | Q(VideoTitle__contains=generalSearch)
            search_filter = search_filter | Q(
                VideoKeyword__contains=generalSearch)
            search_filter = search_filter | Q(
                GoodTitle__contains=generalSearch)
            if str.isdigit(generalSearch):
                search_filter = search_filter | Q(MobilePhone__id=generalSearch)
        data_list = data_list.filter(search_filter)

    if status is not None and status != '':
        status_filter = Q()
        status_list = status[:-1].split(',')
        status_filter = status_filter | Q(Status__in=status_list)
        data_list = data_list.filter(status_filter)

    if commoditytype is not None and commoditytype != '':
        commoditytype_filter = Q()
        if '-1' in commoditytype:
            commoditytype_filter = commoditytype_filter | Q(
                Video__Goods__GoodClassifications=None)
        commoditytype_list = commoditytype[:-1].split(',')
        commoditytype_filter = commoditytype_filter | Q(
            Video__Goods__GoodClassifications__id__in=commoditytype_list)
        data_list = data_list.filter(commoditytype_filter)

    if videotype is not None and videotype != '':
        videotype_filter = Q()
        if '-1' in videotype:
            videotype_filter = videotype_filter | Q(
                Video__VideoClassifications=None)
        videotype_list = videotype[:-1].split(',')
        videotype_filter = videotype_filter | Q(
            Video__VideoClassifications__id__in=videotype_list)
        data_list = data_list.filter(videotype_filter)

    if starttime is not None and starttime != '' and endtime is not None and endtime != '':
        data_list = data_list.filter(
            CreateTime__range=(starttime, endtime))
    elif starttime is not None and starttime != '':
        data_list = data_list.filter(CreateTime__gte=starttime)
    elif endtime is not None and endtime != '':
        data_list = data_list.filter(CreateTime__lte=endtime)

    fields_list = VideoMission._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')        

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values('id', 'MobilePhone__id', 'Status', 'VideoTitle', 'VideoKeyword',
                                                 'GoodTitle', 'GoodCategory', 'CreateTime', 'StartTime', 'FailReason')
    data = []
    for i in range(len(data_result)):
        videomission_id = data_result[i]['id']
        videomission = VideoMission.objects.get(id=videomission_id)
        if videomission.Video is not None:
            video_id = videomission.Video.id
            video = Videos.objects.get(id=video_id)
            CategoryString = video.GetCategoryString()
            data_result[i]['VideoCategoryString'] = CategoryString
        else:
            data_result[i]['VideoCategoryString'] = ''
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def delete_videomission_by_ids(request):
    ids = request.POST.get('ids')
    id_list = ids[:-1].split(',')
    if len(ids) > 0:
        VideoMission.objects.filter(id__in=id_list).delete()
    return HttpResponseRedirect(reverse('Web:VideoMission'))


@login_required
def editvideomission(request):
    data_id = request.POST.get('id')
    videoKeyword = request.POST.get('videokeyword')
    starttime = request.POST.get('starttime')
    videoMission = VideoMission.objects.get(id=data_id)
    videoMission.VideoKeyword = videoKeyword
    if starttime is not None and starttime != '':
        videoMission.StartTime = datetime.datetime.strptime(
            starttime, '%Y-%m-%d %H:%M:%S')
    else:
        videoMission.StartTime = datetime.datetime.now()
    videoMission.save()
    return HttpResponse(reverse('Web:VideoMission'))


@login_required
def getvideomissionbyid(request):
    data_id = request.POST.get('id')
    data = VideoMission.objects.get(id=data_id)
    if data is not None:
        context = {
            'mobilephoneid': data.MobilePhone.id,
            'status': data.Status,
            'videourl': data.VideoURL,
            'videotitle': data.VideoTitle,
            'videokeyword': data.VideoKeyword,
            'videocategory': data.Video.GetCategoryString(),
            'videoremark': data.Video.Remark,
            'goodurl': data.GoodURL,
            'goodtitle': data.GoodTitle,
            'goodcategory': data.GoodCategory,
            'dataid': data.id,
            'starttime': data.StartTime,
        }
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('Error')


@login_required
def relaunchvideomission(request):
    data_id = request.POST.get('id')
    data = VideoMission.objects.get(id=data_id)
    data.Relaunch()
    return HttpResponse('OK')

# end 视频任务

# begin 关注任务
@login_required
def publishfollowmission(request):
    data_url = request.build_absolute_uri(
        reverse('Web:GetFollowMission'))
    create_url = request.build_absolute_uri(
        reverse('Web:CreateFollowMission'))
    delete_url = request.build_absolute_uri(
        reverse('Web:DeleteFollowMission'))
    get_by_id_url = request.build_absolute_uri(
        reverse('Web:GetFollowMissionByID'))
    edit_url = request.build_absolute_uri(
        reverse('Web:EditFollowMission'))
    defaultfollowpeoplelimit = GetSystemConfig('关注人数上限默认值')
    config = {'defaultfollowpeoplelimit': defaultfollowpeoplelimit}
    location = copy.deepcopy(location_init)
    location['IsPublishFollowMissionPage'] = True
    location['IsMissionMenu'] = True
    context = {'location': location, 'data_url': data_url, 'create_url': create_url,
               'delete_url': delete_url, 'get_by_id_url': get_by_id_url, 'edit_url': edit_url,
               'mission_status': TaskStatus, 'config': config}
    return render(request, 'pages/MissionManage/PublishFollowMission.html', context)


@login_required
def getfollowmission(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    generalSearch = request.POST.get(
        'query[generalFollowMissionSearch]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    status = request.POST.get('query[followmissionstatus]')
    starttime = request.POST.get('query[starttime]')    
    endtime = request.POST.get('query[endtime]')        

    owner_id_list = []
    owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)
    data_list = FollowMission.objects.filter(Owner__id__in=owner_id_list)

    if generalSearch is not None and generalSearch != '':
        if str.isdigit(generalSearch):
            data_list = data_list.filter(MobilePhone__id=generalSearch)

    if status is not None and status != '':
        status_filter = Q()
        status_list = status[:-1].split(',')
        status_filter = status_filter | Q(Status__in=status_list)
        data_list = data_list.filter(status_filter)

    if starttime is not None and starttime != '' and endtime is not None and endtime != '':
        data_list = data_list.filter(
            CreateTime__range=(starttime, endtime))
    elif starttime is not None and starttime != '':
        data_list = data_list.filter(CreateTime__gte=starttime)
    elif endtime is not None and endtime != '':
        data_list = data_list.filter(CreateTime__lte=endtime)

    fields_list = FollowMission._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')        

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values(
        'id', 'MobilePhone__id', 'Status', 'PeopleLimit',
        'FanSexIsFemale', 'FanSexIsMale', 'FanSexIsNone', 'CreateTime', 'StartTime', 'EndTime',
        'FailReason')
    data = []
    for i in range(len(data_result)):
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def delete_followmission_by_ids(request):
    ids = request.POST.get('ids')
    id_list = ids[:-1].split(',')
    if len(ids) > 0:
        FollowMission.objects.filter(id__in=id_list).delete()
    return HttpResponseRedirect(reverse('Web:PublishFollowMission'))


@login_required
def createfollowmission(request):
    device_id = request.POST.get('deviceid')
    device_id_list = device_id.split(',')
    peoplelimit = request.POST.get('peoplelimit')
    starttime = request.POST.get('starttime')
    endtime = request.POST.get('endtime')
    fansexismale = request.POST.get('fansexismale')
    fansexisfemale = request.POST.get('fansexisfemale')
    fansexisnone = request.POST.get('fansexisnone')
    if len(device_id_list) > 0:
        # 发布任务
        for i in range(len(device_id_list)):
            id = device_id_list[i]
            device = MobilePhone.objects.get(id=id)
            if device is not None:
                task = FollowMission()
                task.MobilePhone = device
                task.Status = TaskStatus[0][0]
                task.Owner = request.user
                if peoplelimit is not None and peoplelimit != '':
                    task.PeopleLimit = peoplelimit
                else:
                    defaultfollowpeoplelimit = GetSystemConfig('关注人数上限默认值')
                    task.PeopleLimit = defaultfollowpeoplelimit

                if fansexismale == 'true':
                    task.FanSexIsMale = True
                else:
                    task.FanSexIsMale = False

                if fansexisfemale == 'true':
                    task.FanSexIsFemale = True
                else:
                    task.FanSexIsFemale = False

                if fansexisnone == 'true':
                    task.FanSexIsNone = True
                else:
                    task.FanSexIsNone = False

                if starttime != '' and endtime != '':
                    task.StartTime = datetime.datetime.strptime(
                        starttime, '%Y-%m-%d %H:%M:%S')
                    task.EndTime = datetime.datetime.strptime(
                        endtime, '%Y-%m-%d %H:%M:%S')
                elif starttime != '':
                    task.StartTime = datetime.datetime.strptime(
                        starttime, '%Y-%m-%d %H:%M:%S')
                    task.EndTime = task.StartTime + datetime.timedelta(hours=1)
                elif endtime != '':
                    task.EndTime = datetime.datetime.strptime(
                        endtime, '%Y-%m-%d %H:%M:%S')
                    task.StartTime = task.EndTime - datetime.timedelta(hours=1)
                else:
                    task.StartTime = datetime.datetime.now()
                    task.EndTime = task.StartTime + datetime.timedelta(hours=1)
                task.Priority = 0
                task.save()
            else:
                return HttpResponse('Error')
        return HttpResponse(reverse('Web:PublishFollowMission'))
    else:
        return HttpResponse('Error')


@login_required
def editfollowmission(request):
    data_id = request.POST.get('id')
    peoplelimit = request.POST.get('peoplelimit')
    starttime = request.POST.get('starttime')
    endtime = request.POST.get('endtime')
    fansexismale = request.POST.get('fansexismale')
    fansexisfemale = request.POST.get('fansexisfemale')
    fansexisnone = request.POST.get('fansexisnone')
    task = FollowMission.objects.get(id=data_id)
    if peoplelimit is not None and peoplelimit != '':
        task.PeopleLimit = peoplelimit
    else:
        defaultfollowpeoplelimit = GetSystemConfig('关注人数上限默认值')
        task.PeopleLimit = defaultfollowpeoplelimit

    if fansexismale == 'true':
        task.FanSexIsMale = True
    else:
        task.FanSexIsMale = False

    if fansexisfemale == 'true':
        task.FanSexIsFemale = True
    else:
        task.FanSexIsFemale = False

    if fansexisnone == 'true':
        task.FanSexIsNone = True
    else:
        task.FanSexIsNone = False

    if starttime != '' and endtime != '':
        task.StartTime = datetime.datetime.strptime(
            starttime, '%Y-%m-%d %H:%M:%S')
        task.EndTime = datetime.datetime.strptime(endtime, '%Y-%m-%d %H:%M:%S')
    elif starttime != '':
        task.StartTime = datetime.datetime.strptime(
            starttime, '%Y-%m-%d %H:%M:%S')
        task.EndTime = task.StartTime + datetime.timedelta(hours=1)
    elif endtime != '':
        task.EndTime = datetime.datetime.strptime(endtime, '%Y-%m-%d %H:%M:%S')
        task.StartTime = task.EndTime - datetime.timedelta(hours=1)
    else:
        task.StartTime = datetime.datetime.now()
        task.EndTime = task.StartTime + datetime.timedelta(hours=1)
    task.save()
    return HttpResponse(reverse('Web:PublishFollowMission'))


@login_required
def getfollowmissionbyid(request):
    data_id = request.POST.get('id')
    data = FollowMission.objects.get(id=data_id)
    if data is not None:
        context = {
            'mobilephoneid': data.MobilePhone.id,
            'status': data.Status,
            'peoplelimit': data.PeopleLimit,
            'dataid': data.id,
            'starttime': data.StartTime,
            'endtime': data.EndTime,
            'fansexismale': data.FanSexIsMale,
            'fansexisfemale': data.FanSexIsFemale,
            'fansexisnone': data.FanSexIsNone,
        }
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('Error')

# end 关注任务


# begin 养号任务
@login_required
def publishmaintenancenumbermission(request):
    data_url = request.build_absolute_uri(
        reverse('Web:GetMaintenanceNumberMission'))
    create_url = request.build_absolute_uri(
        reverse('Web:CreateMaintenanceNumberMission'))
    delete_url = request.build_absolute_uri(
        reverse('Web:DeleteMaintenanceNumberMission'))
    get_by_id_url = request.build_absolute_uri(
        reverse('Web:GetMaintenanceNumberMissionByID'))
    edit_url = request.build_absolute_uri(
        reverse('Web:EditMaintenanceNumberMission'))
    keyword_data_url = request.build_absolute_uri(
        reverse('Web:GetMaintenanceNumberMissionKeyword'))
    getkeywordnamebyids_url = request.build_absolute_uri(
        reverse('Web:GetMaintenanceNumberMissionKeywordNamesByID'))
    MaintenanceNumberMissionKeyword_List = MaintenanceNumberMissionKeyword.objects.filter(Owner=request.user)
    SelectMaintenanceNumberMissionKeyword = []
    for i in range(len(MaintenanceNumberMissionKeyword_List)):
        per = MaintenanceNumberMissionKeyword_List[i]
        if per.Classification is None:
            select = {'id': per.id, 'SelectName': per.Name,
                      'SelectClassification': ''}
        else:
            select = {'id': per.id, 'SelectName': per.Name,
                      'SelectClassification': per.Classification.Name}
        SelectMaintenanceNumberMissionKeyword.append(select)
    create_keyword_url = request.build_absolute_uri(
        reverse('Web:CreateMaintenanceNumberMissionKeyword'))
    location = copy.deepcopy(location_init)
    location['IsPublishMaintenanceNumberMissionPage'] = True
    location['IsMissionMenu'] = True
    context = {'location': location, 'data_url': data_url, 'create_url': create_url,
               'delete_url': delete_url, 'get_by_id_url': get_by_id_url, 'edit_url': edit_url,
               'mission_status': TaskStatus, 'keyword_data_url': keyword_data_url,
               'getkeywordnamebyids_url': getkeywordnamebyids_url, 'SelectMaintenanceNumberMissionKeyword': SelectMaintenanceNumberMissionKeyword,
               'create_keyword_url': create_keyword_url}
    return render(request, 'pages/MissionManage/PublishMaintenanceNumberMission.html', context)


@login_required
def getmaintenancenumbermission(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    status = request.POST.get('query[maintenancenumbermissionstatus]')
    generalSearch = request.POST.get('query[generalMaintenanceNumberMissionSearch]')    
    starttime = request.POST.get('query[starttime]')    
    endtime = request.POST.get('query[endtime]')      

    owner_id_list = []
    owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)
    data_list = MaintenanceNumberMission.objects.filter(Owner__id__in=owner_id_list)

    if status is not None and status != '':
        status_filter = Q()
        status_list = status[:-1].split(',')
        status_filter = status_filter | Q(Status__in=status_list)
        data_list = data_list.filter(status_filter)

    if generalSearch is not None and generalSearch != '':
        if str.isdigit(generalSearch):
            data_list = data_list.filter(MobilePhone__id=generalSearch)

    if starttime is not None and starttime != '' and endtime is not None and endtime != '':
        data_list = data_list.filter(
            CreateTime__range=(starttime, endtime))
    elif starttime is not None and starttime != '':
        data_list = data_list.filter(CreateTime__gte=starttime)
    elif endtime is not None and endtime != '':
        data_list = data_list.filter(CreateTime__lte=endtime)

    fields_list = MaintenanceNumberMission._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')        

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values(
        'id', 'MobilePhone__id', 'Status', 'CreateTime', 'StartTime', 'EndTime', 'FailReason')
    data = []
    for i in range(len(data_result)):
        maintenancenumbermission_id = data_result[i]['id']
        maintenancenumbermission = MaintenanceNumberMission.objects.get(
            id=maintenancenumbermission_id)
        CategoryString = maintenancenumbermission.GetCategoryString()
        data_result[i]['KeywordCategoryString'] = CategoryString
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def delete_maintenancenumbermission_by_ids(request):
    ids = request.POST.get('ids')
    id_list = ids[:-1].split(',')
    if len(ids) > 0:
        MaintenanceNumberMission.objects.filter(id__in=id_list).delete()
    return HttpResponseRedirect(reverse('Web:PublishMaintenanceNumberMission'))


@login_required
def createmaintenancenumbermission(request):
    device_id = request.POST.get('deviceid')
    device_id_list = device_id.split(',')
    starttime = request.POST.get('starttime')
    endtime = request.POST.get('endtime')
    keywordid = request.POST.get('keywordid')
    keyword_list = []
    if keywordid is not None and keywordid != '':
        keyword_list = keywordid.split(',')
    if len(device_id_list) > 0:
        # 发布任务
        for i in range(len(device_id_list)):
            id = device_id_list[i]
            device = MobilePhone.objects.get(id=id)
            if device is not None:
                task = MaintenanceNumberMission()
                task.MobilePhone = device
                task.Status = TaskStatus[0][0]
                task.Owner = request.user
                if starttime != '' and endtime != '':
                    task.StartTime = datetime.datetime.strptime(
                        starttime, '%Y-%m-%d %H:%M:%S')
                    task.EndTime = datetime.datetime.strptime(
                        endtime, '%Y-%m-%d %H:%M:%S')
                elif starttime != '':
                    task.StartTime = datetime.datetime.strptime(
                        starttime, '%Y-%m-%d %H:%M:%S')
                    task.EndTime = task.StartTime + datetime.timedelta(hours=1)
                elif endtime != '':
                    task.EndTime = datetime.datetime.strptime(
                        endtime, '%Y-%m-%d %H:%M:%S')
                    task.StartTime = task.EndTime - datetime.timedelta(hours=1)
                else:
                    task.StartTime = datetime.datetime.now()
                    task.EndTime = task.StartTime + datetime.timedelta(hours=1)
                task.Priority = 0
                task.save()
                if len(keyword_list) > 0:
                    for i in range(len(keyword_list)):
                        keyword_id = keyword_list[i]
                        keyword = MaintenanceNumberMissionKeyword.objects.get(
                            id=keyword_id)
                        task.Keyword.add(keyword)
            else:
                return HttpResponse('Error')
        return HttpResponse(reverse('Web:PublishMaintenanceNumberMission'))
    else:
        return HttpResponse('Error')


@login_required
def editmaintenancenumbermission(request):
    data_id = request.POST.get('id')
    starttime = request.POST.get('starttime')
    endtime = request.POST.get('endtime')
    task = MaintenanceNumberMission.objects.get(id=data_id)
    if starttime != '' and endtime != '':
        task.StartTime = datetime.datetime.strptime(
            starttime, '%Y-%m-%d %H:%M:%S')
        task.EndTime = datetime.datetime.strptime(endtime, '%Y-%m-%d %H:%M:%S')
    elif starttime != '':
        task.StartTime = datetime.datetime.strptime(
            starttime, '%Y-%m-%d %H:%M:%S')
        task.EndTime = task.StartTime + datetime.timedelta(hours=1)
    elif endtime != '':
        task.EndTime = datetime.datetime.strptime(endtime, '%Y-%m-%d %H:%M:%S')
        task.StartTime = task.EndTime - datetime.timedelta(hours=1)
    else:
        task.StartTime = datetime.datetime.now()
        task.EndTime = task.StartTime + datetime.timedelta(hours=1)
    task.save()
    return HttpResponse(reverse('Web:PublishMaintenanceNumberMission'))


@login_required
def getmaintenancenumbermissionbyid(request):
    data_id = request.POST.get('id')
    data = MaintenanceNumberMission.objects.get(id=data_id)
    if data is not None:
        context = {
            'mobilephoneid': data.MobilePhone.id,
            'status': data.Status,
            'dataid': data.id,
            'starttime': data.StartTime,
            'endtime': data.EndTime,
        }
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('Error')

# end 养号任务

# begin 养号任务关键字
@login_required
def publishmaintenancenumbermissionkeyword(request):
    data_url = request.build_absolute_uri(
        reverse('Web:GetMaintenanceNumberMissionKeyword'))
    create_url = request.build_absolute_uri(
        reverse('Web:CreateMaintenanceNumberMissionKeyword'))
    delete_url = request.build_absolute_uri(
        reverse('Web:DeleteMaintenanceNumberMissionKeyword'))
    get_by_id_url = request.build_absolute_uri(
        reverse('Web:GetMaintenanceNumberMissionKeywordByID'))
    edit_url = request.build_absolute_uri(
        reverse('Web:EditMaintenanceNumberMissionKeyword'))
    classfications = MaintenanceNumberMissionKeywordClassification.objects.filter(Owner=request.user)
    location = copy.deepcopy(location_init)
    location['IsMaintenanceNumberMissionKeywordPage'] = True
    location['IsMyLabelMenu'] = True
    context = {'location': location, 'data_url': data_url, 'create_url': create_url,
               'delete_url': delete_url, 'get_by_id_url': get_by_id_url, 'edit_url': edit_url,
               'classfications': classfications}
    return render(request, 'pages/MyLabel/MaintenanceNumberMissionKeyword.html', context)


@login_required
def getmaintenancenumbermissionkeyword(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    generalSearch = request.POST.get(
        'query[generalMaintenanceNumberMissionKeywordSearch]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    tag = request.POST.get('query[tag]')

    owner_id_list = []
    owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)
    data_list = MaintenanceNumberMissionKeyword.objects.filter(Owner__id__in=owner_id_list)

    if generalSearch is not None and generalSearch != '':
        my_filter = Q()
        my_filter = my_filter | Q(Name__contains=generalSearch)
        data_list = data_list.filter(my_filter)

    if tag is not None and tag != '':
        tag_filter = Q()
        if '-1' in tag:
            tag_filter = tag_filter | Q(Classification=None)
        tag_list = tag[:-1].split(',')
        tag_filter = tag_filter | Q(Classification__id__in=tag_list)
        data_list = data_list.filter(tag_filter)

    fields_list = MaintenanceNumberMissionKeyword._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')        

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values(
        'id', 'Name', 'Classification__Name')
    data = []
    for i in range(len(data_result)):
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def delete_maintenancenumbermissionkeyword_by_ids(request):
    ids = request.POST.get('ids')
    id_list = ids[:-1].split(',')
    if len(ids) > 0:
        MaintenanceNumberMissionKeyword.objects.filter(id__in=id_list).delete()
    return HttpResponseRedirect(reverse('Web:PublishMaintenanceNumberMissionKeyword'))


@login_required
def createmaintenancenumbermissionkeyword(request):
    ret = {"status": "NG", "msg": None, "jump": None}
    name_str = request.POST.get('name')
    name_list = name_str.strip().split(' ')
    if len(name_list) > 0:
        for i in range(len(name_list)):
            name = name_list[i]
            if name != '':
                category = request.POST.get('category')
                if category is not None and category != '':
                    category_list = category[:-1].split(',')
                    if len(category_list) > 0:
                        for i in range(len(category_list)):
                            category_id = category_list[i]
                            if checkmaintenancenumbermissionkeyword(name, category_id, request.user):
                                category = MaintenanceNumberMissionKeywordClassification.objects.get(
                                    id=category_id)
                                keyword = MaintenanceNumberMissionKeyword()
                                keyword.Name = name
                                keyword.Classification = category
                                keyword.Owner = request.user
                                keyword.save()
                            else:
                                continue
                        ret["status"] = "OK"
                        ret["msg"] = reverse(
                            'Web:PublishMaintenanceNumberMissionKeyword')
                        ret["jump"] = reverse(
                            'Web:PublishMaintenanceNumberMissionKeyword')
                    else:
                        ret["msg"] = "该关键词已存在，无法保存"
                else:
                    if checkmaintenancenumbermissionkeyword(name, None, request.user):
                        keyword = MaintenanceNumberMissionKeyword()
                        keyword.Name = name
                        keyword.save()
                        ret["status"] = "OK"
                        ret["msg"] = keyword.id
                        ret["jump"] = reverse(
                            'Web:PublishMaintenanceNumberMissionKeyword')
                    else:
                        ret["msg"] = "该关键词已存在，无法保存"
    else:
        ret["msg"] = "关键词内容有误，请检查"
    return HttpResponse(json.dumps(ret, ensure_ascii=False), content_type="application/json,charset=utf-8")


@login_required
def editmaintenancenumbermissionkeyword(request):
    ret = {"status": "NG", "msg": None, "jump": None}
    name = request.POST.get('name')
    data_id = request.POST.get('id')
    category_id = request.POST.get('category')
    if checkmaintenancenumbermissionkeyword(name, category_id, request.user):
        maintenanceNumberMissionKeyword = MaintenanceNumberMissionKeyword.objects.get(
            id=data_id)
        maintenanceNumberMissionKeyword.Name = name
        if category_id is None or category_id == '':
            maintenanceNumberMissionKeyword.Classification = None
        else:
            category = MaintenanceNumberMissionKeywordClassification.objects.get(
                id=category_id)
            maintenanceNumberMissionKeyword.Classification = category
        maintenanceNumberMissionKeyword.save()
        ret["status"] = "OK"
        ret["jump"] = reverse('Web:PublishMaintenanceNumberMissionKeyword')
    else:
        ret["msg"] = "该关键词已存在，无法保存"
    return HttpResponse(json.dumps(ret, ensure_ascii=False), content_type="application/json,charset=utf-8")


@login_required
def getmaintenancenumbermissionkeywordbyid(request):
    data_id = request.POST.get('id')
    data = MaintenanceNumberMissionKeyword.objects.get(id=data_id)
    if data is not None:
        context = {
            'name': data.Name,
            'dataid': data.id,
            'categoryid': '' if data.Classification is None else data.Classification.id
        }
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('Error')


@login_required
def getmaintenancenumbermissionkeywordnamesbyid(request):
    ids = request.POST.get('ids')
    id_list = ids[:-1].split(',')
    keyword_name_string = ''
    if len(id_list) > 0:
        for i in range(len(id_list)):
            id = id_list[i]
            keyword = MaintenanceNumberMissionKeyword.objects.get(id=id)
            tag = '' if keyword.Classification is None else keyword.Classification.Name
            keyword_name_string = keyword_name_string + keyword.Name + '-' + tag + ','
        context = {
            'ids': ids[:-1],
            'keyword_name_string': keyword_name_string[:-1]
        }
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('Error')


def checkmaintenancenumbermissionkeyword(name, categoryid, user):
    my_filter = Q()
    my_filter = my_filter & Q(Owner=user)
    my_filter = my_filter & Q(Name=name)
    my_filter = my_filter & Q(Classification__id=categoryid)
    check = MaintenanceNumberMissionKeyword.objects.filter(my_filter)
    if check.count() == 0:
        return True
    else:
        return False
# end 养号任务关键字

# begin 养号任务关键字类型
@login_required
def publishmaintenancenumbermissionkeywordclassification(request):
    data_url = request.build_absolute_uri(
        reverse('Web:GetMaintenanceNumberMissionKeywordClassification'))
    create_url = request.build_absolute_uri(
        reverse('Web:CreateMaintenanceNumberMissionKeywordClassification'))
    delete_url = request.build_absolute_uri(
        reverse('Web:DeleteMaintenanceNumberMissionKeywordClassification'))
    get_by_id_url = request.build_absolute_uri(
        reverse('Web:GetMaintenanceNumberMissionKeywordClassificationByID'))
    edit_url = request.build_absolute_uri(
        reverse('Web:EditMaintenanceNumberMissionKeywordClassification'))
    location = copy.deepcopy(location_init)
    location['IsMaintenanceNumberMissionKeywordClassificationPage'] = True
    location['IsMyLabelMenu'] = True
    context = {'location': location, 'data_url': data_url, 'create_url': create_url,
               'delete_url': delete_url, 'get_by_id_url': get_by_id_url, 'edit_url': edit_url}
    return render(request, 'pages/MyLabel/MaintenanceNumberMissionKeywordClassification.html', context)


@login_required
def getmaintenancenumbermissionkeywordclassification(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    generalSearch = request.POST.get(
        'query[generalMaintenanceNumberMissionKeywordClassificationSearch]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')

    owner_id_list = []
    owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)
    data_list = MaintenanceNumberMissionKeywordClassification.objects.filter(Owner__id__in=owner_id_list)

    if generalSearch is not None and generalSearch != '':
        data_list = data_list.filter(Name__contains=generalSearch)

    fields_list = MaintenanceNumberMissionKeywordClassification._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')        

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values(
        'id', 'Name')
    data = []
    for i in range(len(data_result)):
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def delete_maintenancenumbermissionkeywordclassification_by_ids(request):
    ids = request.POST.get('ids')
    id_list = ids[:-1].split(',')
    if len(ids) > 0:
        MaintenanceNumberMissionKeywordClassification.objects.filter(
            id__in=id_list).delete()
    return HttpResponseRedirect(reverse('Web:PublishMaintenanceNumberMissionKeywordClassification'))


@login_required
def createmaintenancenumbermissionkeywordclassification(request):
    ret = {"status": "NG", "msg": None}
    name = request.POST.get('name')
    check_name = MaintenanceNumberMissionKeywordClassification.objects.filter(
        Name=name, Owner=request.user)
    if check_name.count() == 0:
        maintenanceNumberMissionKeywordClassification = MaintenanceNumberMissionKeywordClassification()
        maintenanceNumberMissionKeywordClassification.Name = name
        maintenanceNumberMissionKeywordClassification.Owner = request.user
        maintenanceNumberMissionKeywordClassification.save()
        ret["status"] = "OK"
        ret["msg"] = reverse(
            'Web:PublishMaintenanceNumberMissionKeywordClassification')
    else:
        ret["msg"] = "该标签已存在，无法新增"
    return HttpResponse(json.dumps(ret, ensure_ascii=False), content_type="application/json,charset=utf-8")


@login_required
def editmaintenancenumbermissionkeywordclassification(request):
    ret = {"status": "NG", "msg": None}
    data_id = request.POST.get('id')
    name = request.POST.get('name')
    check_name = MaintenanceNumberMissionKeywordClassification.objects.filter(
        Name=name, Owner=request.user)
    if check_name.count() == 0:
        maintenanceNumberMissionKeywordClassification = MaintenanceNumberMissionKeywordClassification.objects.get(
            id=data_id)
        maintenanceNumberMissionKeywordClassification.Name = name
        maintenanceNumberMissionKeywordClassification.save()
        ret["status"] = "OK"
        ret["msg"] = reverse(
            'Web:PublishMaintenanceNumberMissionKeywordClassification')
    else:
        ret["msg"] = "该标签已存在，无法保存"
    return HttpResponse(json.dumps(ret, ensure_ascii=False), content_type="application/json,charset=utf-8")


@login_required
def getmaintenancenumbermissionkeywordclassificationbyid(request):
    data_id = request.POST.get('id')
    data = MaintenanceNumberMissionKeywordClassification.objects.get(
        id=data_id)
    if data is not None:
        context = {
            'name': data.Name,
            'dataid': data.id,
        }
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('Error')

# end 养号任务关键字类型

# begin 互刷任务
@login_required
def publishmutualbrushmission(request):
    data_url = request.build_absolute_uri(
        reverse('Web:GetMutualBrushMission'))
    create_url = request.build_absolute_uri(
        reverse('Web:CreateMutualBrushMission'))
    delete_url = request.build_absolute_uri(
        reverse('Web:DeleteMutualBrushMission'))
    get_by_id_url = request.build_absolute_uri(
        reverse('Web:GetMutualBrushMissionByID'))
    edit_url = request.build_absolute_uri(
        reverse('Web:EditMutualBrushMission'))
    location = copy.deepcopy(location_init)
    location['IsPublishMutualBrushMissionPage'] = True
    location['IsMissionMenu'] = True
    location['IsMutualBrushMissionSubMenu'] = True
    context = {'location': location, 'data_url': data_url, 'create_url': create_url,
               'delete_url': delete_url, 'get_by_id_url': get_by_id_url, 'edit_url': edit_url,
               'mission_status': TaskStatus}
    return render(request, 'pages/MissionManage/PublishMutualBrushMission.html', context)


@login_required
def getmutualbrushmission(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    generalSearch = request.POST.get(
        'query[generalMutualBrushMissionSearch]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    status = request.POST.get('query[mutualbrushmissionstatus]')
    starttime = request.POST.get('query[starttime]')    
    endtime = request.POST.get('query[endtime]')  

    owner_id_list = []
    owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)
    data_list = MutualBrushMission.objects.filter(Owner__id__in=owner_id_list)

    if generalSearch is not None and generalSearch != '':
        if str.isdigit(generalSearch):
            data_list = data_list.filter(MobilePhone__id=generalSearch)

    if status is not None and status != '':
        status_filter = Q()
        status_list = status[:-1].split(',')
        status_filter = status_filter | Q(Status__in=status_list)
        data_list = data_list.filter(status_filter)

    if starttime is not None and starttime != '' and endtime is not None and endtime != '':
        data_list = data_list.filter(
            CreateTime__range=(starttime, endtime))
    elif starttime is not None and starttime != '':
        data_list = data_list.filter(CreateTime__gte=starttime)
    elif endtime is not None and endtime != '':
        data_list = data_list.filter(CreateTime__lte=endtime)

    fields_list = MutualBrushMission._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')        

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values(
        'id', 'MobilePhone__id', 'Status', 'VideoURL', 'IsLike', 'CommentText',
        'CreateTime', 'StartTime', 'FailReason', 'IsFollow', 'MissionIncome')
    data = []
    for i in range(len(data_result)):
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def delete_mutualbrushmission_by_ids(request):
    ids = request.POST.get('ids')
    id_list = ids[:-1].split(',')
    if len(ids) > 0:
        MutualBrushMission.objects.filter(id__in=id_list).delete()
    return HttpResponseRedirect(reverse('Web:PublishMutualBrushMission'))


@login_required
def createmutualbrushmission(request):
    device_id = request.POST.get('deviceid')
    work_mobile_id_list = device_id.split(',')
    islikerate = int(request.POST.get('islikerate'))
    videourl = request.POST.get('videourl')
    starttime = request.POST.get('starttime')
    commenttext = request.POST.get('commenttext')
    commenttext_list = commenttext.split('\n')
    isfollowcount = int(request.POST.get('isfollowcount'))
    missionincome = decimal.Decimal(request.POST.get('missionincome'))

    if work_mobile_id_list is not None and len(work_mobile_id_list) > 0:
        # 计算需要点赞的手机
        is_like_count = math.floor(
            len(work_mobile_id_list) * islikerate / 100)
        if is_like_count > len(work_mobile_id_list):
            is_like_count = len(work_mobile_id_list)
        is_like_mobile_id_list = random.sample(
            work_mobile_id_list, is_like_count)

        # 计算需要关注的手机
        if isfollowcount > len(work_mobile_id_list):
            isfollowcount = len(work_mobile_id_list)
        is_follow_mobile_id_list = random.sample(
            work_mobile_id_list, isfollowcount)

        # 新建任务
        for i in range(len(work_mobile_id_list)):
            mobile_id = work_mobile_id_list[i]
            mobile = MobilePhone.objects.get(id=mobile_id)
            if mobile is not None:
                task = MutualBrushMission()
                task.MobilePhone = mobile
                task.Status = TaskStatus[0][0]
                task.Owner = request.user
                task.VideoURL = videourl
                if mobile_id in is_like_mobile_id_list:
                    task.IsLike = True
                else:
                    task.IsLike = False

                if mobile_id in is_follow_mobile_id_list:
                    task.IsFollow = True
                else:
                    task.IsFollow = False                        

                if len(commenttext_list) == 0:
                    task.CommentText = ''
                else:
                    task.CommentText = commenttext_list[i % len(commenttext_list)]

                if starttime is not None and starttime != '':
                    task.StartTime = datetime.datetime.strptime(
                        starttime, '%Y-%m-%d %H:%M:%S')
                else:
                    task.StartTime = datetime.datetime.now()
                task.Priority = 0
                task.MissionIncome = missionincome
                task.save()
            else:
                return HttpResponse('Error')

        return HttpResponse(reverse('Web:PublishMutualBrushMission'))
    else:
        return HttpResponse('Error')


@login_required
def editmutualbrushmission(request):
    data_id = request.POST.get('id')
    videourl = request.POST.get('videourl')
    islike = request.POST.get('islike')
    commenttext = request.POST.get('commenttext')
    starttime = request.POST.get('starttime')
    isfollow = request.POST.get('isfollow')
    task = MutualBrushMission.objects.get(id=data_id)
    task.VideoURL = videourl
    if islike == 'false':
        task.IsLike = False
    else:
        task.IsLike = True
    if isfollow == 'false':
        task.IsFollow = False
    else:
        task.IsFollow = True        
    task.CommentText = commenttext
    if starttime is not None and starttime != '':
        task.StartTime = datetime.datetime.strptime(
            starttime, '%Y-%m-%d %H:%M:%S')
    else:
        task.StartTime = datetime.datetime.now()
    task.save()
    return HttpResponse(reverse('Web:PublishMutualBrushMission'))


@login_required
def getmutualbrushmissionbyid(request):
    data_id = request.POST.get('id')
    data = MutualBrushMission.objects.get(id=data_id)
    if data is not None:
        context = {
            'mobilephoneid': data.MobilePhone.id,
            'status': data.Status,
            'videourl': data.VideoURL,
            'islike': data.IsLike,
            'commenttext': data.CommentText,
            'dataid': data.id,
            'starttime': data.StartTime,
            'isfollow': data.IsFollow,
        }
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('Error')

# end 互刷任务

# begin 刷粉任务
@login_required
def publishscanmission(request):
    data_url = request.build_absolute_uri(
        reverse('Web:GetScanMission'))
    create_url = request.build_absolute_uri(
        reverse('Web:CreateScanMission'))
    delete_url = request.build_absolute_uri(
        reverse('Web:DeleteScanMission'))
    get_by_id_url = request.build_absolute_uri(
        reverse('Web:GetScanMissionByID'))
    edit_url = request.build_absolute_uri(
        reverse('Web:EditScanMission'))
    defaultscanpeoplelimit = GetSystemConfig('刷粉人数上限默认值')
    defaultinterval = GetSystemConfig('刷粉点赞与评论间隔人数')    
    config = {'defaultscanpeoplelimit': defaultscanpeoplelimit, 'defaultinterval': defaultinterval}
    location = copy.deepcopy(location_init)
    location['IsPublishScanMissionPage'] = True
    location['IsMissionMenu'] = True
    context = {'location': location, 'data_url': data_url, 'create_url': create_url,
               'delete_url': delete_url, 'get_by_id_url': get_by_id_url, 'edit_url': edit_url,
               'mission_status': TaskStatus, 'config': config}
    return render(request, 'pages/MissionManage/PublishScanMission.html', context)


@login_required
def getscanmission(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    generalSearch = request.POST.get(
        'query[generalScanMissionSearch]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    status = request.POST.get('query[scanmissionstatus]') 
    starttime = request.POST.get('query[starttime]')    
    endtime = request.POST.get('query[endtime]')         

    owner_id_list = []
    owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)
    data_list = ScanMission.objects.filter(Owner__id__in=owner_id_list)

    if generalSearch is not None and generalSearch != '':
        if str.isdigit(generalSearch):
            data_list = data_list.filter(MobilePhone__id=generalSearch)

    if status is not None and status != '':
        status_filter = Q()
        status_list = status[:-1].split(',')
        status_filter = status_filter | Q(Status__in=status_list)
        data_list = data_list.filter(status_filter)

    if starttime is not None and starttime != '' and endtime is not None and endtime != '':
        data_list = data_list.filter(
            CreateTime__range=(starttime, endtime))
    elif starttime is not None and starttime != '':
        data_list = data_list.filter(CreateTime__gte=starttime)
    elif endtime is not None and endtime != '':
        data_list = data_list.filter(CreateTime__lte=endtime)

    fields_list = ScanMission._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')        

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values(
        'id', 'MobilePhone__id', 'Status', 'PeopleLimit',
        'Interval', 'FanSexIsFemale', 'FanSexIsMale', 'FanSexIsNone', 'CreateTime', 'StartTime', 'EndTime',
        'FailReason', 'IsDirectional')
    data = []
    for i in range(len(data_result)):
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def delete_scanmission_by_ids(request):
    ids = request.POST.get('ids')
    id_list = ids[:-1].split(',')
    if len(ids) > 0:
        ScanMission.objects.filter(id__in=id_list).delete()
    return HttpResponseRedirect(reverse('Web:PublishScanMission'))


@login_required
def createscanmission(request):
    device_id = request.POST.get('deviceid')
    device_id_list = device_id.split(',')
    peoplelimit = request.POST.get('peoplelimit')
    interval = request.POST.get('interval')
    fansexismale = request.POST.get('fansexismale')
    fansexisfemale = request.POST.get('fansexisfemale')
    fansexisnone = request.POST.get('fansexisnone')
    starttime = request.POST.get('starttime')
    endtime = request.POST.get('endtime')
    commenttext = request.POST.get('commenttext')
    isdirectional = request.POST.get('isdirectional')
    if len(device_id_list) > 0:
        # 发布任务
        for i in range(len(device_id_list)):
            id = device_id_list[i]
            device = MobilePhone.objects.get(id=id)
            if device is not None:
                task = ScanMission()
                task.MobilePhone = device
                task.Status = TaskStatus[0][0]
                task.Owner = request.user
                if peoplelimit is not None and peoplelimit != '':
                    task.PeopleLimit = peoplelimit
                else:
                    defaultscanpeoplelimit = GetSystemConfig('刷粉人数上限默认值')
                    task.PeopleLimit = defaultscanpeoplelimit

                if fansexismale == 'true':
                    task.FanSexIsMale = True
                else:
                    task.FanSexIsMale = False

                if fansexisfemale == 'true':
                    task.FanSexIsFemale = True
                else:
                    task.FanSexIsFemale = False

                if fansexisnone == 'true':
                    task.FanSexIsNone = True
                else:
                    task.FanSexIsNone = False

                if interval is not None and interval != '':            
                    task.Interval = interval
                else:
                    defaultinterval = GetSystemConfig('刷粉点赞与评论间隔人数')
                    task.Interval = defaultinterval

                if starttime != '' and endtime != '':
                    task.StartTime = datetime.datetime.strptime(
                        starttime, '%Y-%m-%d %H:%M:%S')
                    task.EndTime = datetime.datetime.strptime(
                        endtime, '%Y-%m-%d %H:%M:%S')
                elif starttime != '':
                    task.StartTime = datetime.datetime.strptime(
                        starttime, '%Y-%m-%d %H:%M:%S')
                    task.EndTime = task.StartTime + datetime.timedelta(hours=1)
                elif endtime != '':
                    task.EndTime = datetime.datetime.strptime(
                        endtime, '%Y-%m-%d %H:%M:%S')
                    task.StartTime = task.EndTime - datetime.timedelta(hours=1)
                else:
                    task.StartTime = datetime.datetime.now()
                    task.EndTime = task.StartTime + datetime.timedelta(hours=1)
                task.Priority = 0

                if commenttext is not None and len(commenttext) > 0:
                    commenttext_ids = ''
                    commenttext_list = commenttext.split('\n')
                    for i in range(len(commenttext_list)):
                        comment = commenttext_list[i]
                        if comment != '':
                            check_exists = CommentLibrary.objects.filter(
                                Text=comment)
                            if check_exists.count() > 0:
                                id = check_exists.first().id
                                commenttext_ids = commenttext_ids + \
                                    str(id) + ','
                            else:
                                NewComment = CommentLibrary()
                                NewComment.Text = comment
                                NewComment.save()
                                id = NewComment.id
                                commenttext_ids = commenttext_ids + \
                                    str(id) + ','
                    task.CommentTextID = commenttext_ids[:-1]

                if isdirectional is not None and isdirectional != '':
                    if isdirectional == '0':
                        task.IsDirectional = False
                    else:
                        task.IsDirectional = True
                else:
                    task.IsDirectional = False
                
                task.save()
            else:
                return HttpResponse('Error')
        return HttpResponse(reverse('Web:PublishScanMission'))
    else:
        return HttpResponse('Error')


@login_required
def editscanmission(request):
    data_id = request.POST.get('id')
    peoplelimit = request.POST.get('peoplelimit')
    interval = request.POST.get('interval')
    starttime = request.POST.get('starttime')
    endtime = request.POST.get('endtime')
    fansexismale = request.POST.get('fansexismale')
    fansexisfemale = request.POST.get('fansexisfemale')
    fansexisnone = request.POST.get('fansexisnone')
    commenttext = request.POST.get('commenttext')
    isdirectional = request.POST.get('isdirectional')    
    task = ScanMission.objects.get(id=data_id)
    if peoplelimit is not None and peoplelimit != '':
        task.PeopleLimit = peoplelimit
    else:
        defaultscanpeoplelimit = GetSystemConfig('刷粉人数上限默认值')
        task.PeopleLimit = defaultscanpeoplelimit

    if interval is not None and interval != '':            
        task.Interval = interval
    else:
        defaultinterval = GetSystemConfig('刷粉点赞与评论间隔人数')
        task.Interval = defaultinterval

    if fansexismale == 'true':
        task.FanSexIsMale = True
    else:
        task.FanSexIsMale = False

    if fansexisfemale == 'true':
        task.FanSexIsFemale = True
    else:
        task.FanSexIsFemale = False

    if fansexisnone == 'true':
        task.FanSexIsNone = True
    else:
        task.FanSexIsNone = False
    if starttime != '' and endtime != '':
        task.StartTime = datetime.datetime.strptime(
            starttime, '%Y-%m-%d %H:%M:%S')
        task.EndTime = datetime.datetime.strptime(endtime, '%Y-%m-%d %H:%M:%S')
    elif starttime != '':
        task.StartTime = datetime.datetime.strptime(
            starttime, '%Y-%m-%d %H:%M:%S')
        task.EndTime = task.StartTime + datetime.timedelta(hours=1)
    elif endtime != '':
        task.EndTime = datetime.datetime.strptime(endtime, '%Y-%m-%d %H:%M:%S')
        task.StartTime = task.EndTime - datetime.timedelta(hours=1)
    else:
        task.StartTime = datetime.datetime.now()
        task.EndTime = task.StartTime + datetime.timedelta(hours=1)

    if commenttext is not None and len(commenttext) > 0:
        commenttext_ids = ''
        commenttext_list = commenttext.split('\n')
        for i in range(len(commenttext_list)):
            comment = commenttext_list[i]
            if comment != '':
                check_exists = CommentLibrary.objects.filter(Text=comment)
                if check_exists.count() > 0:
                    id = check_exists.first().id
                    commenttext_ids = commenttext_ids + str(id) + ','
                else:
                    NewComment = CommentLibrary()
                    NewComment.Text = comment
                    NewComment.save()
                    id = NewComment.id
                    commenttext_ids = commenttext_ids + str(id) + ','
        task.CommentTextID = commenttext_ids[:-1]

    if isdirectional is not None and isdirectional != '':
        if isdirectional == '0':
            task.IsDirectional = False
        else:
            task.IsDirectional = True
    else:
        task.IsDirectional = False

    task.save()
    return HttpResponse(reverse('Web:PublishScanMission'))


@login_required
def getscanmissionbyid(request):
    data_id = request.POST.get('id')
    data = ScanMission.objects.get(id=data_id)
    if data is not None:
        context = {
            'mobilephoneid': data.MobilePhone.id,
            'status': data.Status,
            'peoplelimit': data.PeopleLimit,
            'interval': data.Interval,
            'fansexismale': data.FanSexIsMale,
            'fansexisfemale': data.FanSexIsFemale,
            'fansexisnone': data.FanSexIsNone,
            'dataid': data.id,
            'starttime': data.StartTime,
            'endtime': data.EndTime,
            'commenttext': data.GetCommentText(),
            'isdirectional': data.IsDirectional,
        }
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('Error')

# end 刷粉任务

# begin 评论库
@login_required
def commentlibrary(request):
    data_url = request.build_absolute_uri(
        reverse('Web:GetCommentLibrary'))
    create_url = request.build_absolute_uri(
        reverse('Web:CreateCommentLibrary'))
    delete_url = request.build_absolute_uri(
        reverse('Web:DeleteCommentLibrary'))
    get_by_id_url = request.build_absolute_uri(
        reverse('Web:GetCommentLibraryByID'))
    edit_url = request.build_absolute_uri(
        reverse('Web:EditCommentLibrary'))
    location = copy.deepcopy(location_init)
    location['IsCommentLibraryPage'] = True
    location['IsMissionMenu'] = True
    location['IsMutualBrushMissionSubMenu'] = True
    context = {'location': location, 'data_url': data_url, 'create_url': create_url,
               'delete_url': delete_url, 'get_by_id_url': get_by_id_url, 'edit_url': edit_url}
    return render(request, 'pages/MissionManage/CommentLibrary.html', context)


@login_required
def getcommentlibrary(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    generalSearch = request.POST.get(
        'query[generalCommentLibrarySearch]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')

    owner_id_list = []
    owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)
    data_list = CommentLibrary.objects.filter(Owner__id__in=owner_id_list)

    if generalSearch is not None and generalSearch != '':
        data_list = data_list.filter(Text__contains=generalSearch)

    fields_list = CommentLibrary._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')        

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values(
        'id', 'Text', 'CreateTime')
    data = []
    for i in range(len(data_result)):
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def delete_commentlibrary_by_ids(request):
    ids = request.POST.get('ids')
    id_list = ids[:-1].split(',')
    if len(ids) > 0:
        CommentLibrary.objects.filter(id__in=id_list).delete()
    return HttpResponseRedirect(reverse('Web:CommentLibrary'))


@login_required
def createcommentlibrary(request):
    text = request.POST.get('text')
    commentlibrary = CommentLibrary()
    commentlibrary.Text = text
    commentlibrary.Owner = request.user
    commentlibrary.save()
    return HttpResponse(reverse('Web:CommentLibrary'))


@login_required
def editcommentlibrary(request):
    data_id = request.POST.get('id')
    text = request.POST.get('text')
    commentlibrary = CommentLibrary.objects.get(id=data_id)
    commentlibrary.Text = text
    commentlibrary.save()
    return HttpResponse(reverse('Web:CommentLibrary'))


@login_required
def getcommentlibrarybyid(request):
    commentlibrary_id = request.POST.get('id')
    commentlibrary = CommentLibrary.objects.get(id=commentlibrary_id)
    if commentlibrary is not None:
        context = {
            'text': commentlibrary.Text,
            'dataid': commentlibrary.id,
        }
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('Error')

# end 评论库

# begin 代理审核


@login_required
def agentverify(request):
    data_url = request.build_absolute_uri(reverse('Web:GetAgentVerify'))
    pass_as_superuser_url = request.build_absolute_uri(reverse('Web:PassAgentVerifyASSuperUser'))
    pass_as_mainuser_url = request.build_absolute_uri(reverse('Web:PassAgentVerifyASMainUser'))
    pass_as_agent_url = request.build_absolute_uri(reverse('Web:PassAgentVerifyASAgent'))        
    not_pass_url = request.build_absolute_uri(
        reverse('Web:NotPassAgentVerify'))
    username = request.user.username
    location = copy.deepcopy(location_init)
    location['IsAgentVerifyPage'] = True
    location['IsMyAgentMenu'] = True
    context = {'location': location, 'data_url': data_url, 'pass_as_superuser_url': pass_as_superuser_url,
               'pass_as_mainuser_url': pass_as_mainuser_url, 'pass_as_agent_url': pass_as_agent_url, 'not_pass_url': not_pass_url,
               'username': username}
    return render(request, 'pages/MyAgent/AgentVerify.html', context)


@login_required
def getagentverify(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    generalSearch = request.POST.get('query[generalAgentVerifySearch]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    agentVerifycolumn = request.POST.get('query[agentVerifycolumn]')

    my_filter = Q()
    my_filter = my_filter & Q(is_pass=False)
    my_filter = my_filter & Q(usersystem=request.user)

    data_list = User.objects.filter(my_filter)

    if generalSearch is not None and generalSearch != '':
        serarch_filter = Q()
        if agentVerifycolumn == 'username':
            serarch_filter = serarch_filter | Q(
                username__contains=generalSearch)
        elif agentVerifycolumn == 'leader':
            serarch_filter = serarch_filter | Q(
                leader__username__contains=generalSearch)
        elif agentVerifycolumn == 'truename':
            serarch_filter = serarch_filter | Q(
                true_name__contains=generalSearch)
        elif agentVerifycolumn == 'phone':
            serarch_filter = serarch_filter | Q(phone__contains=generalSearch)
        else:
            serarch_filter = serarch_filter | Q(
                username__contains=generalSearch)
            serarch_filter = serarch_filter | Q(
                leader__username__contains=generalSearch)
            serarch_filter = serarch_filter | Q(
                true_name__contains=generalSearch)
            serarch_filter = serarch_filter | Q(phone__contains=generalSearch)
        data_list = data_list.filter(serarch_filter)

    fields_list = User._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')         

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values(
        'id', 'username', 'leader__username', 'date_joined', 'birthday',
        'qq', 'sex', 'true_name', 'wechat', 'wechat_nickname',
        'phone', 'platform', 'platform_id', 'platform_password',
        'platform_is_certification', 'platform_certification_true_name',
        'platform_certification_id_card')
    data = []
    for i in range(len(data_result)):
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def passagentverifyasagent(request):
    ids = request.POST.get('ids')
    id_list = ids[:-1].split(',')
    if len(ids) > 0:
        User.objects.filter(id__in=id_list).update(is_pass=True)
        for i in range(len(id_list)):
            agent = Agent()
            id = id_list[i]
            user = User.objects.get(id=id)
            agent.Subscriber = user

            # 顶级
            agent.UserSystem = user.usersystem

            # 上级
            alevel = user.leader
            if (alevel.id != user.usersystem.id):
                agent.UserALevel = alevel

            # 上上级
            if alevel.is_superuser == False and alevel.is_mainuser == False:
                blevel = alevel.leader
                if (blevel is not None and blevel.id != user.usersystem.id):
                    agent.UserBLevel = blevel
            agent.save()
    return HttpResponseRedirect(reverse('Web:AgentVerify'))


@login_required
def passagentverifyassuperuser(request):
    ids = request.POST.get('ids')
    id_list = ids[:-1].split(',')
    if len(ids) > 0:
        User.objects.filter(id__in=id_list).update(is_pass=True, is_superuser=True)
        for i in range(len(id_list)):
            id = id_list[i]
            user = User.objects.get(id=id)
            relations = TopUserRelations()
            relations.Subscriber = user
            relations.Leader = user.usersystem
            relations.save()
    return HttpResponseRedirect(reverse('Web:AgentVerify'))    


@login_required
def passagentverifyasmainuser(request):
    ids = request.POST.get('ids')
    id_list = ids[:-1].split(',')
    if len(ids) > 0:
        User.objects.filter(id__in=id_list).update(is_pass=True, is_mainuser=True)
        for i in range(len(id_list)):
            id = id_list[i]
            user = User.objects.get(id=id)
            relations = TopUserRelations()
            relations.Subscriber = user
            relations.Leader = user.usersystem
            relations.save()
    return HttpResponseRedirect(reverse('Web:AgentVerify'))                


@login_required
def notpassagentverify(request):
    ids = request.POST.get('ids')
    id_list = ids[:-1].split(',')
    if len(ids) > 0:
        User.objects.filter(id__in=id_list).delete()
    return HttpResponseRedirect(reverse('Web:AgentVerify'))

# end 代理审核

# begin 代理列表
@login_required
def agentlist(request):
    data_url = request.build_absolute_uri(reverse('Web:GetAgentList'))
    get_by_id_url = request.build_absolute_uri(
        reverse('Web:GetAgentListByID'))
    edit_url = request.build_absolute_uri(reverse('Web:EditAgentList'))
    device_data_url = request.build_absolute_uri(reverse('Web:GetDevice'))
    getdevicenamebyids_url = request.build_absolute_uri(
        reverse('Web:GetDeviceNameByIDs'))
    agentdetail_url = request.build_absolute_uri(reverse('Web:AgentDetail'))
    devicemanage_url = request.build_absolute_uri(reverse('Web:DeviceManage'))
    classifications = MaintenanceNumberMissionKeywordClassification.objects.filter(Owner=request.user)
    groups = TikTokAccountGroup.objects.filter(Owner=request.user)
    getpromotionbyagentid_url = request.build_absolute_uri(
        reverse('Web:GetPromotionByAgentID'))
    resetpassword_url = request.build_absolute_uri(
        reverse('Web:ResetPassword'))
    location = copy.deepcopy(location_init)
    location['IsAgentListPage'] = True
    location['IsMyAgentMenu'] = True
    context = {'location': location, 'data_url': data_url,
               'get_by_id_url': get_by_id_url, 'edit_url': edit_url,
               'device_data_url': device_data_url, "getdevicenamebyids_url": getdevicenamebyids_url,
               'agentdetail_url': agentdetail_url, 'devicemanage_url': devicemanage_url,
               'classifications': classifications, 'groups': groups,
               'getpromotionbyagentid_url': getpromotionbyagentid_url, 'resetpassword_url': resetpassword_url}
    return render(request, 'pages/MyAgent/AgentList.html', context)


@login_required
def getagentlist(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    generalSearch = request.POST.get('query[generalAgentSearch]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    agentlistcolumn = request.POST.get('query[agentlistcolumn]')

    usersystem_id_list = []
    usersystem_id_list = GetOwnerIDList(request.user.id, usersystem_id_list)
    data_list = Agent.objects.filter(UserSystem__id__in=usersystem_id_list)

    if generalSearch is not None and generalSearch != '':
        serarch_filter = Q()
        if agentlistcolumn == 'username':
            serarch_filter = serarch_filter | Q(
                Subscriber__username__contains=generalSearch)
        elif agentlistcolumn == 'alevel':
            serarch_filter = serarch_filter | Q(
                UserALevel__username__contains=generalSearch)
        elif agentlistcolumn == 'blevel':
            serarch_filter = serarch_filter | Q(
                UserBLevel__username__contains=generalSearch)
        else:
            serarch_filter = serarch_filter | Q(
                Subscriber__username__contains=generalSearch)
            serarch_filter = serarch_filter | Q(
                UserALevel__username__contains=generalSearch)
            serarch_filter = serarch_filter | Q(
                UserBLevel__username__contains=generalSearch)
        data_list = data_list.filter(serarch_filter)

    fields_list = Agent._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')         

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values('id', 'Subscriber__username', 'UserALevel__username',
                                                 'UserBLevel__username', 'UserSystemPercent',
                                                 'UserALevelPercent', 'UserBLevelPercent', 'UserSystem__username',
                                                 'Subscriber__money')
    data = []
    for i in range(len(data_result)):
        agent_id = data_result[i]['id']
        agent = Agent.objects.get(id=agent_id)
        mobile = agent.mobilephone_set.all()
        mobilephoneid = ''
        if (mobile.count() > 0):
            for j in range(mobile.count()):
                per = mobile[j]
                mobilephoneid = mobilephoneid + str(per.id) + ','
        data_result[i]['mobilephoneid'] = mobilephoneid[:-1]
        # 今日推广预估收入
        now = datetime.date.today()
        begintime = str(now)
        endtime = str(now + datetime.timedelta(days=1))
        sql = "EXEC [CalcAgentIncome] {},'{}','{}',{},'{}'".format(
            agent_id, begintime, endtime, 0, 'Myself')
        cur = connection.cursor()
        rows = cur.execute(sql).fetchall()
        data_result[i]['TodayPIDIncome'] = rows[0][0] if rows[0][0] is not None else 0

        # 今日任务预估收入
        now = datetime.date.today()
        begintime = str(now)
        endtime = str(now + datetime.timedelta(days=1))
        sql = "EXEC [CalcAgentMissionIncome] {},'{}','{}'".format(
            agent_id, begintime, endtime)
        cur = connection.cursor()
        rows = cur.execute(sql).fetchall()
        data_result[i]['TodayMissionIncome'] = rows[0][0] if rows[0][0] is not None else 0        

        # 本月预估收入
        now = datetime.date.today()
        endtime = str(now + datetime.timedelta(days=1))
        day = now.day
        if day > 25:
            begintime = str(datetime.datetime(now.year, now.month, 26))
        else:
            if now.month == 1:
                begintime = str(datetime.datetime(now.year - 1, 12, 26))
            else:
                begintime = str(datetime.datetime(now.year, now.month - 1, 26))
        sql = "EXEC [CalcAgentIncome] {},'{}','{}',{},'{}'".format(
            agent_id, begintime, endtime, 0, 'Total')
        cur = connection.cursor()
        rows = cur.execute(sql).fetchall()
        CurrentMonthOrderIncome = rows[0][0] if rows[0][0] is not None else 0
        sql = "EXEC [CalcAgentMissionIncome] {},'{}','{}'".format(
            agent_id, begintime, endtime)
        cur = connection.cursor()
        rows = cur.execute(sql).fetchall()
        CurrentMonthMissionIncome = rows[0][0] if rows[0][0] is not None else 0
        data_result[i]['CurrentMonthIncome'] = CurrentMonthOrderIncome + CurrentMonthMissionIncome

        # 上月实际收入
        month_income_list = AgentMonthRealityIncome.objects.filter(
            Agent__id=agent_id).order_by('-SummaryDate')
        if month_income_list.count() > 0:
            month_income = month_income_list.first()
            data_result[i]['LastMonthTruelyIncome'] = month_income.TotalMoney
        else:
            data_result[i]['LastMonthTruelyIncome'] = 0

        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def editagentlist(request):
    data_id = request.POST.get('id')
    UserSystemPercent = request.POST.get('UserSystemPercent')
    UserALevelPercent = request.POST.get('UserALevelPercent')
    UserBLevelPercent = request.POST.get('UserBLevelPercent')
    deviceid = request.POST.get('deviceid')
    agent = Agent.objects.get(id=data_id)
    agent.UserSystemPercent = UserSystemPercent
    agent.UserALevelPercent = UserALevelPercent
    agent.UserBLevelPercent = UserBLevelPercent
    agent.mobilephone_set.clear()
    device_list = deviceid.split(',')
    if (len(device_list) > 0):
        for i in range(len(device_list)):
            device_id = device_list[i]
            device = MobilePhone.objects.get(id=device_id)
            device.Agent = agent
            device.save()
    agent.save()
    return HttpResponse(reverse('Web:AgentList'))


@login_required
def getagentlistbyid(request):
    data_id = request.POST.get('id')
    data = Agent.objects.get(id=data_id)
    mobilephoneid = ""
    if data is not None:
        mobile = data.mobilephone_set.all()
        if (mobile.count() > 0):
            for i in range(mobile.count()):
                per = mobile[i]
                mobilephoneid = mobilephoneid + str(per.id) + ','
        context = {
            'mobilephoneid': mobilephoneid[:-1],
            'username': data.Subscriber.username,
            'alevelusername': '' if(data.UserALevel == None) else data.UserALevel.username,
            'blevelusername': '' if(data.UserBLevel == None) else data.UserBLevel.username,
            'usersystempercent': data.UserSystemPercent,
            'useralevelpercent': data.UserALevelPercent,
            'userblevelpercent': data.UserBLevelPercent,
            'usersystemusername': '' if(data.UserSystem == None) else data.UserSystem.username,
            'dataid': data.id,
        }
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('Error')


@login_required
def getpromotionbyagentid(request):
    agent_id = request.POST.get('id')

    # 今日
    now = datetime.date.today()
    begintime = str(now)
    endtime = str(now + datetime.timedelta(days=1))
    sql = "EXEC [CalcAgentIncome] {},'{}','{}',{},'{}'".format(
        agent_id, begintime, endtime, 0, 'ABLevel')
    cur = connection.cursor()
    rows = cur.execute(sql).fetchall()
    todaymoney = rows[0][0] if rows[0][0] is not None else 0
    todayordercount = rows[0][1] if rows[0][1] is not None else 0

    # 昨日
    begintime = str(now - datetime.timedelta(days=1))
    endtime = str(now)
    sql = "EXEC [CalcAgentIncome] {},'{}','{}',{},'{}'".format(
        agent_id, begintime, endtime, 0, 'ABLevel')
    cur = connection.cursor()
    rows = cur.execute(sql).fetchall()
    yestodaymoney = rows[0][0] if rows[0][0] is not None else 0
    yestodayordercount = rows[0][1] if rows[0][1] is not None else 0

    # 最近7日
    begintime = str(now - datetime.timedelta(days=6))
    endtime = str(now)
    sql = "EXEC [CalcAgentIncome] {},'{}','{}',{},'{}'".format(
        agent_id, begintime, endtime, 0, 'ABLevel')
    cur = connection.cursor()
    rows = cur.execute(sql).fetchall()
    sevendaysmoney = rows[0][0] if rows[0][0] is not None else 0
    sevendaysordercount = rows[0][1] if rows[0][1] is not None else 0

    # 本月
    endtime = str(now + datetime.timedelta(days=1))
    day = now.day
    if day > 25:
        begintime = str(datetime.datetime(now.year, now.month, 26))
    else:
        if now.month == 1:
            begintime = str(datetime.datetime(now.year - 1, 12, 26))
        else:
            begintime = str(datetime.datetime(now.year, now.month - 1, 26))
    sql = "EXEC [CalcAgentIncome] {},'{}','{}',{},'{}'".format(
        agent_id, begintime, endtime, 0, 'ABLevel')
    cur = connection.cursor()
    rows = cur.execute(sql).fetchall()
    currentmonthmoney = rows[0][0] if rows[0][0] is not None else 0
    currentmonthordercount = rows[0][1] if rows[0][1] is not None else 0

    # 上月
    day = now.day
    if day > 25:
        endtime = str(datetime.datetime(now.year, now.month, 26))
        if now.month == 1:
            begintime = str(datetime.datetime(now.year - 1, 12, 26))
        else:
            begintime = str(datetime.datetime(now.year, now.month - 1, 26))
    else:
        if now.month == 1:
            endtime = str(datetime.datetime(now.year - 1, 12, 26))
            begintime = str(datetime.datetime(now.year - 1, 11, 26))
        else:
            endtime = str(datetime.datetime(now.year, now.month - 1, 26))
            if now.month == 2:
                begintime = str(datetime.datetime(now.year - 1, 12, 26))
            else:
                begintime = str(datetime.datetime(now.year, now.month - 2, 26))
    sql = "EXEC [CalcAgentIncome] {},'{}','{}',{},'{}'".format(
        agent_id, begintime, endtime, 1, 'ABLevel')
    cur = connection.cursor()
    rows = cur.execute(sql).fetchall()
    lastmonthmoney = rows[0][0] if rows[0][0] is not None else 0
    lastmonthordercount = rows[0][1] if rows[0][1] is not None else 0

    context = {
        'todaymoney': todaymoney,
        'todayordercount': todayordercount,
        'yestodaymoney': yestodaymoney,
        'yestodayordercount': yestodayordercount,
        'sevendaysmoney': sevendaysmoney,
        'sevendaysordercount': sevendaysordercount,
        'currentmonthmoney': currentmonthmoney,
        'currentmonthordercount': currentmonthordercount,
        'lastmonthmoney': lastmonthmoney,
        'lastmonthordercount': lastmonthordercount,
    }
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def resetpassword(request):
    data_id = request.POST.get('id')
    data = Agent.objects.get(id=data_id)
    if data is not None:
        user = data.Subscriber
        user.password = make_password('123456')
        user.save()
        return HttpResponse('OK')
    else:
        return HttpResponse('Error')

# end 代理列表

# begin 代理账号信息
@login_required
def agentdetail(request):
    data_url = request.build_absolute_uri(reverse('Web:GetAgentDetail'))
    get_by_id_url = request.build_absolute_uri(
        reverse('Web:GetAgentDetailByID'))
    edit_url = request.build_absolute_uri(reverse('Web:EditAgentDetail'))
    location = copy.deepcopy(location_init)
    location['IsAgentDetailPage'] = True
    location['IsMyAgentMenu'] = True
    context = {'location': location, 'data_url': data_url,
               'get_by_id_url': get_by_id_url, 'edit_url': edit_url}
    return render(request, 'pages/MyAgent/AgentDetail.html', context)


@login_required
def getagentdetail(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    generalSearch = request.POST.get('query[generalAgentDetailSearch]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    agentdetailcolumn = request.POST.get('query[agentdetailcolumn]')

    usersystem_id_list = []
    usersystem_id_list = GetOwnerIDList(request.user.id, usersystem_id_list)
    data_list = Agent.objects.filter(UserSystem__id__in=usersystem_id_list)

    if generalSearch is not None and generalSearch != '':
        serarch_filter = Q()
        if agentdetailcolumn == 'username':
            serarch_filter = serarch_filter | Q(
                Subscriber__username__contains=generalSearch)
        elif agentdetailcolumn == 'truename':
            serarch_filter = serarch_filter | Q(
                Subscriber__true_name__contains=generalSearch)
        elif agentdetailcolumn == 'phone':
            serarch_filter = serarch_filter | Q(
                Subscriber__phone__contains=generalSearch)
        else:
            serarch_filter = serarch_filter | Q(
                Subscriber__username__contains=generalSearch)
            serarch_filter = serarch_filter | Q(
                Subscriber__true_name__contains=generalSearch)
            serarch_filter = serarch_filter | Q(
                Subscriber__phone__contains=generalSearch)
        data_list = data_list.filter(serarch_filter)

    fields_list = Agent._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')         

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values('id', 'Subscriber__username', 'Subscriber__date_joined',
                                                 'Subscriber__true_name', 'Subscriber__phone', 'Subscriber__wechat',
                                                 'Subscriber__wechat_nickname', 'Subscriber__sex', 'Subscriber__platform',
                                                 'Subscriber__platform_id', 'Subscriber__platform_password', 'Subscriber__platform_is_certification',
                                                 'Subscriber__platform_certification_true_name', 'Subscriber__platform_certification_id_card',
                                                 'Subscriber__qq', 'Subscriber__birthday')
    data = []
    for i in range(len(data_result)):
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def editagentdetail(request):
    data_id = request.POST.get('dataid')
    true_name = request.POST.get('true_name')
    phone = request.POST.get('phone')
    wechat = request.POST.get('wechat')
    wechat_nickname = request.POST.get('wechat_nickname')
    sex = request.POST.get('sex')
    platform = request.POST.get('platform')
    platform_id = request.POST.get('platform_id')
    platform_password = request.POST.get('platform_password')
    platform_is_certification = request.POST.get('platform_is_certification')
    platform_certification_true_name = request.POST.get(
        'platform_certification_true_name')
    platform_certification_id_card = request.POST.get(
        'platform_certification_id_card')
    qq = request.POST.get('qq')
    birthday = request.POST.get('birthday')
    agent = Agent.objects.get(id=data_id)
    agent.Subscriber.true_name = true_name
    agent.Subscriber.phone = phone
    agent.Subscriber.wechat = wechat
    agent.Subscriber.wechat_nickname = wechat_nickname
    agent.Subscriber.sex = sex
    agent.Subscriber.platform = platform
    agent.Subscriber.platform_id = platform_id
    agent.Subscriber.platform_password = platform_password
    agent.Subscriber.platform_is_certification = platform_is_certification
    agent.Subscriber.platform_certification_true_name = platform_certification_true_name
    agent.Subscriber.platform_certification_id_card = platform_certification_id_card
    agent.Subscriber.qq = qq
    if birthday is not None and birthday != '':
        agent.Subscriber.birthday = birthday
    agent.Subscriber.save()
    return HttpResponse(reverse('Web:AgentDetail'))


@login_required
def getagentdetailbyid(request):
    data_id = request.POST.get('id')
    data = Agent.objects.get(id=data_id)
    if data is not None:
        context = {
            'username': data.Subscriber.username,
            'date_joined': data.Subscriber.date_joined,
            'true_name': data.Subscriber.true_name,
            'phone': data.Subscriber.phone,
            'wechat': data.Subscriber.wechat,
            'wechat_nickname': data.Subscriber.wechat_nickname,
            'sex': data.Subscriber.sex,
            'platform': data.Subscriber.platform,
            'platform_id': data.Subscriber.platform_id,
            'platform_password': data.Subscriber.platform_password,
            'platform_is_certification': data.Subscriber.platform_is_certification,
            'platform_certification_true_name': data.Subscriber.platform_certification_true_name,
            'platform_certification_id_card': data.Subscriber.platform_certification_id_card,
            'qq': data.Subscriber.qq,
            'birthday': data.Subscriber.birthday,
            'dataid': data.id,
        }
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('Error')

# end 代理账号信息

# begin 订单管理
@login_required
def order(request):
    data_url = request.build_absolute_uri(reverse('Web:GetOrder'))
    location = copy.deepcopy(location_init)
    location['IsOrderPage'] = True
    location['IsCommodityManageMenu'] = True
    context = {'location': location, 'data_url': data_url}
    return render(request, 'pages/CommodityManage/Order.html', context)


@login_required
def getorder(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    generalSearch = request.POST.get('query[generalOrderSearch]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    orderStatus = request.POST.get('query[orderStatus]')
    createtime = request.POST.get('query[createtime]')
    accountid = request.POST.get('query[accountid]')
    goodid = request.POST.get('query[goodid]')
    agentid = request.POST.get('query[agentid]')
    ordercolumn = request.POST.get('query[ordercolumn]')

    owner_id_list = []
    owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)
    device_list = MobilePhone.objects.filter(Owner__id__in=owner_id_list)
    all_aliconfig_id_list = list(device_list.values_list('ALIConfig__id', flat=True))
    data_list = Order.objects.filter(ALIConfig__id__in=all_aliconfig_id_list)

    if accountid != None and accountid != '':
        device = MobilePhone.objects.filter(TikTokAccount__id=accountid)
        if device.count() > 0:
            mobile = device.first()
            if mobile is not None and mobile.ALIConfig is not None:
                config = ALIConfig.objects.get(id=mobile.ALIConfig.id)
                data_list = Order.objects.filter(ADZone_ID=config.LASTPID)
            else:
                data_list = Order.objects.filter(id=-1)
        else:
            data_list = Order.objects.filter(id=-1)
    elif goodid != None and goodid != '':
        data_list = Order.objects.filter(Goods__id=goodid)
    elif agentid != None and agentid != '':
        device = MobilePhone.objects.filter(Agent__id=agentid)
        if device.count() > 0:
            aliconfig_id_list = list(
                device.values_list('ALIConfig__id', flat=True))
            data_list = Order.objects.filter(
                ALIConfig__id__in=aliconfig_id_list)
        else:
            data_list = Order.objects.filter(id=-1)
    else:
        pass

    if generalSearch is not None and generalSearch != '':
        search_filter = Q()
        if ordercolumn == 'goodtitle':
            search_filter = search_filter | Q(Item_Title__contains=generalSearch)
        elif ordercolumn == 'orderid':
            search_filter = search_filter | Q(
                Trade_Parent_ID=generalSearch)
        elif ordercolumn == 'agentname':
            search_filter = search_filter | Q(
                ALIConfig__mobilephone__Agent__Subscriber__username=generalSearch)
        else:
            search_filter = search_filter | Q(Item_Title__contains=generalSearch)
            search_filter = search_filter | Q(
                Trade_Parent_ID=generalSearch)
            search_filter = search_filter | Q(
                ALIConfig__mobilephone__Agent__Subscriber__username=generalSearch)
        data_list = data_list.filter(search_filter)

    if orderStatus is not None and orderStatus != '':
        orderStatus_filter = Q()
        orderStatus_list = orderStatus[:-1].split(',')
        for i in range(len(orderStatus_list)):
            per = orderStatus_list[i]
            if per == '1':
                orderStatus_filter = orderStatus_filter | Q(Refund_Tag=per)
            else:
                orderStatus_filter = orderStatus_filter | (
                    Q(TK_Status=per) & Q(Refund_Tag=0))
        data_list = data_list.filter(orderStatus_filter)

    if createtime is not None and createtime != '':
        createtime_filter = Q()
        time_list = createtime[:-1].split(',')
        # 1:今天 2:昨天 3:本月 4:上月 5:上上月
        for i in range(len(time_list)):
            per = time_list[i]
            beginTime = ''
            endTime = ''
            now = datetime.date.today()
            if per == '1':
                beginTime = now
                endTime = beginTime + datetime.timedelta(days=1)
            elif per == '2':
                beginTime = now + datetime.timedelta(days=-1)
                endTime = beginTime + datetime.timedelta(days=1)
            elif per == '3':
                beginTime = datetime.datetime(now.year, now.month, 1)
                if now.month == 12:
                    endTime = datetime.datetime(now.year, 12, 31)
                else:
                    endTime = datetime.datetime(
                        now.year, now.month + 1, 1) - datetime.timedelta(days=1)
            elif per == '4':
                this_month_start = datetime.datetime(now.year, now.month, 1)
                last_month_end = this_month_start - datetime.timedelta(days=1)
                last_month_start = datetime.datetime(
                    last_month_end.year, last_month_end.month, 1)
                beginTime = last_month_start
                endTime = last_month_end
            elif per == '5':
                this_month_start = datetime.datetime(now.year, now.month, 1)
                last_month_end = this_month_start - datetime.timedelta(days=1)
                last_month_start = datetime.datetime(
                    last_month_end.year, last_month_end.month, 1)
                last_last_month_end = last_month_start - \
                    datetime.timedelta(days=1)
                last_last_month_start = datetime.datetime(
                    last_last_month_end.year, last_last_month_end.month, 1)
                beginTime = last_last_month_start
                endTime = last_last_month_end
            createtime_filter = createtime_filter | Q(
                TK_Create_Time__range=(beginTime, endTime))
        data_list = data_list.filter(createtime_filter)

    fields_list = Order._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')         
    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values('id', 'Item_Img', 'Item_Title',
                                                 'Total_Commission_Rate',
                                                 'Trade_Parent_ID', 'Order_Type', 'TK_Earning_Time',
                                                 'TK_Status', 'ADZone_ID', 'Alipay_Total_Price', 'TK_Create_Time',
                                                 'Refund_Tag', 'Pub_Share_Pre_Fee', 'Pub_Share_Fee',
                                                 'TK_Commission_Fee_For_Media_Platform', 'TK_Commission_Pre_Fee_For_Media_Platform',
                                                 'ALIConfig__mobilephone__Agent__Subscriber__username', 'ALIConfig__mobilephone__TikTokAccount__NickName')
    data = []
    for i in range(len(data_result)):
        data_result[i]['Final_Pub_Share_Pre_Fee'] = data_result[i]['Pub_Share_Pre_Fee'] - \
            data_result[i]['TK_Commission_Pre_Fee_For_Media_Platform']
        data_result[i]['Final_Pub_Pre_Fee'] = data_result[i]['Pub_Share_Fee'] - \
            data_result[i]['TK_Commission_Fee_For_Media_Platform']
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


# end 订单管理

# begin 提现管理

@login_required
def cashmanage(request):
    data_url = request.build_absolute_uri(
        reverse('Web:GetAgentApplyForWithdraw'))
    pass_url = request.build_absolute_uri(
        reverse('Web:PassAgentApplyForWithdraw'))
    not_pass_url = request.build_absolute_uri(
        reverse('Web:NotPassAgentApplyForWithdraw'))
    location = copy.deepcopy(location_init)
    location['IsCashManagePage'] = True
    location['IsMyAgentMenu'] = True
    context = {'location': location, 'data_url': data_url, 'pass_url': pass_url,
               'not_pass_url': not_pass_url}
    return render(request, 'pages/MyAgent/CashManage.html', context)


@login_required
def createagentapplyforwithdraw(request):
    ret = {"status": "NG", "msg": None}
    money = decimal.Decimal(request.POST.get('money'))
    if money > request.user.money:
        ret['msg'] = '金额不能超过' + str(request.user.money) + '元'
    elif money == 0:
        ret['msg'] = '金额不能为0'
    else:
        request.user.money -= money
        request.user.save()
        agent = Agent.objects.get(Subscriber=request.user)
        agentapplyforwithdraw = AgentApplyForWithdraw()
        agentapplyforwithdraw.Money = money
        agentapplyforwithdraw.ApplyDate = datetime.datetime.now()
        agentapplyforwithdraw.Agent = agent
        agentapplyforwithdraw.save()
        ret['status'] = 'OK'
        if request.user.is_superuser:
            ret['msg'] = reverse('Web:index')
        else:
            ret['msg'] = reverse('Web:AgentWithdraw')
    return HttpResponse(json.dumps(ret, ensure_ascii=False), content_type="application/json,charset=utf-8")


@login_required
def getagentapplyforwithdraw(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    generalSearch = request.POST.get('query[generalCashManageSearch]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    cashmanagecolumn = request.POST.get('query[cashmanagecolumn]')
    status = request.POST.get('query[status]')

    usersystem_id_list = []
    usersystem_id_list = GetOwnerIDUntilSuperuserList(request.user.id, usersystem_id_list)
    AgentApplyForWithdraw_filter = Q()
    AgentApplyForWithdraw_filter = AgentApplyForWithdraw_filter & Q(Agent__UserSystem__id__in=usersystem_id_list)
    data_list = AgentApplyForWithdraw.objects.filter(AgentApplyForWithdraw_filter)

    if generalSearch is not None and generalSearch != '':
        serarch_filter = Q()
        if cashmanagecolumn == 'username':
            serarch_filter = serarch_filter | Q(
                Agent__Subscriber__username__contains=generalSearch)
        elif cashmanagecolumn == 'leader':
            serarch_filter = serarch_filter | Q(
                Agent__UserALevel__username__contains=generalSearch)
        elif cashmanagecolumn == 'truename':
            serarch_filter = serarch_filter | Q(
                Agent__Subscriber__true_name__contains=generalSearch)
        elif cashmanagecolumn == 'phone':
            serarch_filter = serarch_filter | Q(
                Agent__Subscriber__phone__contains=generalSearch)
        else:
            serarch_filter = serarch_filter | Q(
                Agent__Subscriber__username__contains=generalSearch)
            serarch_filter = serarch_filter | Q(
                Agent__UserALevel__username__contains=generalSearch)
            serarch_filter = serarch_filter | Q(
                Agent__Subscriber__true_name__contains=generalSearch)
            serarch_filter = serarch_filter | Q(
                Agent__Subscriber__phone__contains=generalSearch)
        data_list = data_list.filter(serarch_filter)

    if status is not None and status != '':
        status_filter = Q()
        status_list = status[:-1].split(',')
        for i in range(len(status_list)):
            per = status_list[i]
            status_filter = status_filter | Q(IsPass=per)
        data_list = data_list.filter(status_filter)

    fields_list = User._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')         

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values(
        'id', 'Agent__Subscriber__username', 'ApplyDate', 'Money', 'Agent__UserALevel__username',
        'Agent__Subscriber__true_name', 'Agent__Subscriber__phone', 'Agent__Subscriber__wechat', 'IsPass')
    data = []
    for i in range(len(data_result)):
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def passagentapplyforwithdraw(request):
    id = request.POST.get('id')
    agentApplyForWithdraw = AgentApplyForWithdraw.objects.get(id=id)
    agentApplyForWithdraw.IsPass = 1
    agentApplyForWithdraw.ApproveDate = datetime.datetime.now()
    agentApplyForWithdraw.ApproveUser = request.user
    agentApplyForWithdraw.save()
    return HttpResponseRedirect(reverse('Web:CashManage'))


@login_required
def notpassagentapplyforwithdraw(request):
    id = request.POST.get('id')
    agentApplyForWithdraw = AgentApplyForWithdraw.objects.get(id=id)
    agentApplyForWithdraw.IsPass = 2
    agentApplyForWithdraw.ApproveDate = datetime.datetime.now()
    agentApplyForWithdraw.ApproveUser = request.user
    agentApplyForWithdraw.save()
    user = agentApplyForWithdraw.Agent.Subscriber
    user.money += agentApplyForWithdraw.Money
    user.save()
    return HttpResponseRedirect(reverse('Web:CashManage'))

# end 提现管理

# begin 任务模板
@login_required
def missionplantemplate(request):
    data_url = request.build_absolute_uri(
        reverse('Web:GetMissionPlanTemplate'))
    create_url = request.build_absolute_uri(
        reverse('Web:CreateMissionPlanTemplate'))
    delete_url = request.build_absolute_uri(
        reverse('Web:DeleteMissionPlanTemplate'))
    edit_url = request.build_absolute_uri(
        reverse('Web:EditMissionPlanTemplate'))
    getdevicebytemplateid_url = request.build_absolute_uri(
        reverse('Web:GetDeviceByTemplateID'))
    diliverdevice_url = request.build_absolute_uri(
        reverse('Web:DeliverDevice'))
    device_data_url = request.build_absolute_uri(reverse('Web:GetDevice'))
    devicemanage_url = request.build_absolute_uri(reverse('Web:DeviceManage'))
    getdevicenamebyids_url = request.build_absolute_uri(
        reverse('Web:GetDeviceNameByIDs'))
    classifications = MaintenanceNumberMissionKeywordClassification.objects.filter(Owner=request.user)
    groups = TikTokAccountGroup.objects.filter(Owner=request.user)
    location = copy.deepcopy(location_init)
    location['IsMissionPlanTemplatePage'] = True
    location['IsMissionMenu'] = True
    context = {'location': location, 'data_url': data_url, 'create_url': create_url,
               'delete_url': delete_url, 'edit_url': edit_url, 'getdevicebytemplateid_url': getdevicebytemplateid_url,
               'diliverdevice_url': diliverdevice_url, 'device_data_url': device_data_url,
               'getdevicenamebyids_url': getdevicenamebyids_url, 'classifications': classifications,
               'groups': groups, 'devicemanage_url': devicemanage_url}
    return render(request, 'pages/MissionManage/MissionPlanTemplate.html', context)


@login_required
def getmissionplantemplate(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')

    owner_id_list = []
    owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)
    data_list = MissionPlanTemplate.objects.filter(Owner__id__in=owner_id_list)

    fields_list = MissionPlanTemplate._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')         

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values('id', 'Name', 'CreateTime')
    data = []
    for i in range(len(data_result)):
        template_id = data_result[i]['id']
        template = MissionPlanTemplate.objects.get(id=template_id)
        mobile = template.mobilephone_set.all()
        mobilephoneid = ''
        if (mobile.count() > 0):
            for j in range(mobile.count()):
                per = mobile[j]
                mobilephoneid = mobilephoneid + str(per.id) + ','
        data_result[i]['mobilephoneid'] = mobilephoneid[:-1]
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def delete_missionplantemplate_by_ids(request):
    ids = request.POST.get('ids')
    id_list = ids[:-1].split(',')
    if len(ids) > 0:
        MissionPlanTemplate.objects.filter(id__in=id_list).delete()
    return HttpResponseRedirect(reverse('Web:MissionPlanTemplate'))


@login_required
def createmissionplantemplate(request):
    try:
        name = request.POST.get('name')
        missionPlanTemplate = MissionPlanTemplate()
        missionPlanTemplate.Name = name
        missionPlanTemplate.Owner = request.user
        recorddate = datetime.date.today()
        check_date = MissionPlanTemplate.objects.filter(RecordDate=recorddate)
        while check_date.count() > 0:
            recorddate = recorddate - datetime.timedelta(days=1)
            check_date = MissionPlanTemplate.objects.filter(
                RecordDate=recorddate)
        missionPlanTemplate.RecordDate = recorddate
        missionPlanTemplate.save()
        return HttpResponse(reverse('Web:MissionPlanTemplate'))
    except Exception as e:
        print(e)
        return HttpResponse("Error")


@login_required
def getdevicebytemplateid(request):
    templateid = request.POST.get('id')
    mobile_list = MobilePhone.objects.filter(
        MissionPlanTemplate__id=templateid).values('id')
    mobile_ids = ''
    if len(mobile_list) > 0:
        for i in range(len(mobile_list)):
            mobile_ids = mobile_ids + str(mobile_list[i]['id']) + ','
    context = {
        'dataid': templateid,
        'mobilephoneid': mobile_ids[:-1],
    }
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def deliverdevice(request):
    device_id = request.POST.get('deviceid')
    device_id_list = device_id.split(',')
    template_id = request.POST.get('id')
    template = MissionPlanTemplate.objects.get(id=template_id)
    template.mobilephone_set.clear()
    for j in range(len(device_id_list)):
        id = device_id_list[j]
        if id is not None and id != '':
            device = MobilePhone.objects.get(id=id)
            if device is not None:
                device.MissionPlanTemplate = template
                device.save()
    return HttpResponse(reverse('Web:MissionPlanTemplate'))

# end 任务模板


# begin 编辑任务模板
@login_required
def editmissionplantemplate(request):
    location = copy.deepcopy(location_init)
    location['IsMissionPlanTemplatePage'] = True
    location['IsMissionMenu'] = True
    context = {'location': location}
    return render(request, 'pages/MissionManage/EditMissionPlanTemplate.html', context)


@login_required
def editmissionplantemplatebyid(request, missionplantemplate_id):
    missionplantemplate = MissionPlanTemplate.objects.get(
        id=missionplantemplate_id)
    record_date = missionplantemplate.RecordDate.strftime('%Y-%m-%d')
    create_url = request.build_absolute_uri(reverse('Web:CreateEvent'))
    delete_url = request.build_absolute_uri(
        reverse('Web:DeleteEvent'))
    edit_url = request.build_absolute_uri(reverse('Web:EditEvent'))
    get_events_by_template_id_url = request.build_absolute_uri(
        reverse('Web:GetEventsByTemplateID'))
    template_url = request.build_absolute_uri(
        reverse('Web:MissionPlanTemplate'))
    get_event_by_id_url = request.build_absolute_uri(
        reverse('Web:GetEventByID'))
    editeventdetail = request.build_absolute_uri(
        reverse('Web:EditEventDetail'))
    template_name = missionplantemplate.Name
    defaultscanpeoplelimit = GetSystemConfig('刷粉人数上限默认值')
    defaultfollowpeoplelimit = GetSystemConfig('关注人数上限默认值')
    defaultinterval = GetSystemConfig('刷粉点赞与评论间隔人数')        
    config = {'defaultscanpeoplelimit': defaultscanpeoplelimit,
              'defaultfollowpeoplelimit': defaultfollowpeoplelimit,
              'defaultinterval': defaultinterval}
    location = copy.deepcopy(location_init)
    location['IsMissionPlanTemplatePage'] = True
    location['IsMissionMenu'] = True
    context = {'location': location, 'record_date': record_date, 'template_name': template_name,
               'create_url': create_url, 'delete_url': delete_url, 'edit_url': edit_url, 'get_events_by_template_id_url': get_events_by_template_id_url,
               'template_id': missionplantemplate_id, 'template_url': template_url, 'get_event_by_id_url': get_event_by_id_url,
               'editeventdetail': editeventdetail, 'config': config}
    return render(request, 'pages/MissionManage/EditMissionPlanTemplate.html', context)


@login_required
def delete_event_by_ids(request):
    eventtype = request.POST.get('eventtype')
    dataid = request.POST.get('dataid')
    if eventtype == '养号任务':
        MaintenanceNumberMissionPlan.objects.filter(id=dataid).delete()
    elif eventtype == '刷粉任务':
        ScanMissionPlan.objects.filter(id=dataid).delete()
    elif eventtype == '关注任务':
        FollowMissionPlan.objects.filter(id=dataid).delete()
    elif eventtype == '刷宝任务':
        TreasureMissionPlan.objects.filter(id=dataid).delete()
    return HttpResponse('OK')


@login_required
def createevent(request):
    templateid = request.POST.get('templateid')
    strattime_str = request.POST.get('strattime_str')
    eventtype = request.POST.get('eventtype')
    template = MissionPlanTemplate.objects.get(id=templateid)
    if eventtype == '养号任务':
        starttime = datetime.datetime.strptime(
            strattime_str, '%Y-%m-%d %H:%M:%S')
        endtime = starttime + datetime.timedelta(hours=1)
        maintenancenumbermissionplan = MaintenanceNumberMissionPlan()
        maintenancenumbermissionplan.MissionPlanTemplate = template
        maintenancenumbermissionplan.StartTime = starttime
        maintenancenumbermissionplan.EndTime = endtime
        maintenancenumbermissionplan.Title = eventtype
        maintenancenumbermissionplan.save()
        return(HttpResponse(maintenancenumbermissionplan.id))
    elif eventtype == '刷粉任务':
        starttime = datetime.datetime.strptime(
            strattime_str, '%Y-%m-%d %H:%M:%S')
        endtime = starttime + datetime.timedelta(hours=1)
        scanmissionplan = ScanMissionPlan()
        scanmissionplan.MissionPlanTemplate = template
        scanmissionplan.StartTime = starttime
        scanmissionplan.EndTime = endtime
        scanmissionplan.Title = eventtype
        defaultscanpeoplelimit = GetSystemConfig('刷粉人数上限默认值')
        scanmissionplan.PeopleLimit = defaultscanpeoplelimit
        defaultinterval = GetSystemConfig('刷粉点赞与评论间隔人数')    
        scanmissionplan.Interval = defaultinterval
        scanmissionplan.save()
        return(HttpResponse(scanmissionplan.id))
    elif eventtype == '关注任务':
        starttime = datetime.datetime.strptime(
            strattime_str, '%Y-%m-%d %H:%M:%S')
        endtime = starttime + datetime.timedelta(hours=1)
        followmissionplan = FollowMissionPlan()
        followmissionplan.MissionPlanTemplate = template
        followmissionplan.StartTime = starttime
        followmissionplan.EndTime = endtime
        followmissionplan.Title = eventtype
        defaultfollowpeoplelimit = GetSystemConfig('关注人数上限默认值')
        followmissionplan.PeopleLimit = defaultfollowpeoplelimit
        followmissionplan.save()
        return(HttpResponse(followmissionplan.id))
    if eventtype == '刷宝任务':
        starttime = datetime.datetime.strptime(
            strattime_str, '%Y-%m-%d %H:%M:%S')
        endtime = starttime + datetime.timedelta(hours=1)
        treasuremissionplan = TreasureMissionPlan()
        treasuremissionplan.MissionPlanTemplate = template
        treasuremissionplan.StartTime = starttime
        treasuremissionplan.EndTime = endtime
        treasuremissionplan.Title = eventtype
        treasuremissionplan.save()
        return(HttpResponse(treasuremissionplan.id))


@login_required
def geteventsbytemplateid(request):
    templateid = request.POST.get('templateid')
    maintenancenumbermissionplan = MaintenanceNumberMissionPlan.objects.filter(
        MissionPlanTemplate__id=templateid)
    events = []
    if maintenancenumbermissionplan.count() > 0:
        maintenancenumbermissionplan_result = maintenancenumbermissionplan.values(
            'id', 'Description', 'StartTime', 'EndTime', 'Title')
        for i in range(len(maintenancenumbermissionplan_result)):
            starttime_str = datetime.datetime.strftime(
                maintenancenumbermissionplan_result[i]['StartTime'], '%Y-%m-%dT%H:%M:%S')
            endtime_str = datetime.datetime.strftime(
                maintenancenumbermissionplan_result[i]['EndTime'], '%Y-%m-%dT%H:%M:%S')
            event = {}
            event['start'] = starttime_str
            event['end'] = endtime_str
            event['title'] = maintenancenumbermissionplan_result[i]['Title']
            extendedProps = {}
            extendedProps['dataid'] = maintenancenumbermissionplan_result[i]['id']
            event['extendedProps'] = extendedProps
            event['description'] = maintenancenumbermissionplan_result[i]['Description']
            event['classNames'] = 'fc-event-primary'
            events.append(event)
    scanmissionplan = ScanMissionPlan.objects.filter(
        MissionPlanTemplate__id=templateid)
    if scanmissionplan.count() > 0:
        scanmissionplan_result = scanmissionplan.values(
            'id', 'Description', 'StartTime', 'EndTime', 'Title')
        for j in range(len(scanmissionplan_result)):
            starttime_str = datetime.datetime.strftime(
                scanmissionplan_result[j]['StartTime'], '%Y-%m-%dT%H:%M:%S')
            endtime_str = datetime.datetime.strftime(
                scanmissionplan_result[j]['EndTime'], '%Y-%m-%dT%H:%M:%S')
            event = {}
            event['start'] = starttime_str
            event['end'] = endtime_str
            event['title'] = scanmissionplan_result[j]['Title']
            extendedProps = {}
            extendedProps['dataid'] = scanmissionplan_result[j]['id']
            event['extendedProps'] = extendedProps
            event['description'] = scanmissionplan_result[j]['Description']
            event['classNames'] = 'fc-event-warning'
            events.append(event)
    followmissionplan = FollowMissionPlan.objects.filter(
        MissionPlanTemplate__id=templateid)
    if followmissionplan.count() > 0:
        followmissionplan_result = followmissionplan.values(
            'id', 'Description', 'StartTime', 'EndTime', 'Title')
        for j in range(len(followmissionplan_result)):
            starttime_str = datetime.datetime.strftime(
                followmissionplan_result[j]['StartTime'], '%Y-%m-%dT%H:%M:%S')
            endtime_str = datetime.datetime.strftime(
                followmissionplan_result[j]['EndTime'], '%Y-%m-%dT%H:%M:%S')
            event = {}
            event['start'] = starttime_str
            event['end'] = endtime_str
            event['title'] = followmissionplan_result[j]['Title']
            extendedProps = {}
            extendedProps['dataid'] = followmissionplan_result[j]['id']
            event['extendedProps'] = extendedProps
            event['description'] = followmissionplan_result[j]['Description']
            event['classNames'] = 'fc-event-success'
            events.append(event)
    treasuremissionplan = TreasureMissionPlan.objects.filter(
        MissionPlanTemplate__id=templateid)
    if treasuremissionplan.count() > 0:
        treasuremissionplan_result = treasuremissionplan.values(
            'id', 'Description', 'StartTime', 'EndTime', 'Title')
        for i in range(len(treasuremissionplan_result)):
            starttime_str = datetime.datetime.strftime(
                treasuremissionplan_result[i]['StartTime'], '%Y-%m-%dT%H:%M:%S')
            endtime_str = datetime.datetime.strftime(
                treasuremissionplan_result[i]['EndTime'], '%Y-%m-%dT%H:%M:%S')
            event = {}
            event['start'] = starttime_str
            event['end'] = endtime_str
            event['title'] = treasuremissionplan_result[i]['Title']
            extendedProps = {}
            extendedProps['dataid'] = treasuremissionplan_result[i]['id']
            event['extendedProps'] = extendedProps
            event['description'] = treasuremissionplan_result[i]['Description']
            event['classNames'] = 'fc-event-dark'
            events.append(event)

    return HttpResponse(json.dumps(events, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def geteventbyid(request):
    eventtype = request.POST.get('eventtype')
    dataid = request.POST.get('dataid')
    if eventtype == '养号任务':
        data = MaintenanceNumberMissionPlan.objects.get(id=dataid)
        context = {
            'description': data.Description,
            'dataid': data.id,
            'type': data.Title,
        }
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    elif eventtype == '刷粉任务':
        data = ScanMissionPlan.objects.get(id=dataid)
        context = {
            'description': data.Description,
            'dataid': data.id,
            'type': data.Title,
            'peoplelimit': data.PeopleLimit,
            'interval': data.Interval,
            'fansexismale': data.FanSexIsMale,
            'fansexisfemale': data.FanSexIsFemale,
            'fansexisnone': data.FanSexIsNone,
            'commenttext': data.GetCommentText(),
        }
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    elif eventtype == '关注任务':
        data = FollowMissionPlan.objects.get(id=dataid)
        context = {
            'description': data.Description,
            'dataid': data.id,
            'type': data.Title,
            'peoplelimit': data.PeopleLimit,
            'fansexismale': data.FanSexIsMale,
            'fansexisfemale': data.FanSexIsFemale,
            'fansexisnone': data.FanSexIsNone,
        }
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    elif eventtype == '刷宝任务':
        data = TreasureMissionPlan.objects.get(id=dataid)
        context = {
            'description': data.Description,
            'dataid': data.id,
            'type': data.Title,
        }
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")


@login_required
def editevent(request):
    dataid = request.POST.get('dataid')
    strattime_str = request.POST.get('strattime_str')
    endtime_str = request.POST.get('endtime_str')
    eventtype = request.POST.get('eventtype')
    if eventtype == '养号任务':
        starttime = datetime.datetime.strptime(
            strattime_str, '%Y-%m-%d %H:%M:%S')
        if endtime_str == '':
            endtime = starttime + datetime.timedelta(hours=1)
        else:
            endtime = datetime.datetime.strptime(
                endtime_str, '%Y-%m-%d %H:%M:%S')
        maintenancenumbermissionplan = MaintenanceNumberMissionPlan.objects.get(
            id=dataid)
        maintenancenumbermissionplan.StartTime = starttime
        maintenancenumbermissionplan.EndTime = endtime
        maintenancenumbermissionplan.save()
        return(HttpResponse(maintenancenumbermissionplan.id))
    elif eventtype == '刷粉任务':
        starttime = datetime.datetime.strptime(
            strattime_str, '%Y-%m-%d %H:%M:%S')
        if endtime_str == '':
            endtime = starttime + datetime.timedelta(hours=1)
        else:
            endtime = datetime.datetime.strptime(
                endtime_str, '%Y-%m-%d %H:%M:%S')
        scanmissionplan = ScanMissionPlan.objects.get(id=dataid)
        scanmissionplan.StartTime = starttime
        scanmissionplan.EndTime = endtime
        scanmissionplan.save()
        return(HttpResponse(scanmissionplan.id))
    elif eventtype == '关注任务':
        starttime = datetime.datetime.strptime(
            strattime_str, '%Y-%m-%d %H:%M:%S')
        if endtime_str == '':
            endtime = starttime + datetime.timedelta(hours=1)
        else:
            endtime = datetime.datetime.strptime(
                endtime_str, '%Y-%m-%d %H:%M:%S')
        followmissionplan = FollowMissionPlan.objects.get(id=dataid)
        followmissionplan.StartTime = starttime
        followmissionplan.EndTime = endtime
        followmissionplan.save()
        return(HttpResponse(followmissionplan.id))
    elif eventtype == '刷宝任务':
        starttime = datetime.datetime.strptime(
            strattime_str, '%Y-%m-%d %H:%M:%S')
        if endtime_str == '':
            endtime = starttime + datetime.timedelta(hours=1)
        else:
            endtime = datetime.datetime.strptime(
                endtime_str, '%Y-%m-%d %H:%M:%S')
        treasuremissionplan = TreasureMissionPlan.objects.get(id=dataid)
        treasuremissionplan.StartTime = starttime
        treasuremissionplan.EndTime = endtime
        treasuremissionplan.save()
        return(HttpResponse(treasuremissionplan.id))


@login_required
def editeventdetail(request):
    eventtype = request.POST.get('eventtype')
    dataid = request.POST.get('dataid')
    if eventtype == '养号任务':
        description = request.POST.get('description')
        maintenancenumbermissionplan = MaintenanceNumberMissionPlan.objects.get(
            id=dataid)
        maintenancenumbermissionplan.Description = description
        maintenancenumbermissionplan.save()
    elif eventtype == '刷粉任务':
        description = request.POST.get('description')
        peoplelimit = request.POST.get('peoplelimit')
        interval = request.POST.get('interval')
        fansexismale = request.POST.get('fansexismale')
        fansexisfemale = request.POST.get('fansexisfemale')
        fansexisnone = request.POST.get('fansexisnone')
        commenttext = request.POST.get('commenttext')
        scanmissionplan = ScanMissionPlan.objects.get(id=dataid)
        scanmissionplan.Description = description
        if peoplelimit is not None and peoplelimit != '' and peoplelimit != '0':
            scanmissionplan.PeopleLimit = peoplelimit
        else:
            defaultscanpeoplelimit = GetSystemConfig('刷粉人数上限默认值')
            scanmissionplan.PeopleLimit = defaultscanpeoplelimit

        if interval is not None and interval != '':            
            scanmissionplan.Interval = interval
        else:
            defaultinterval = GetSystemConfig('刷粉点赞与评论间隔人数')
            scanmissionplan.Interval = defaultinterval

        if fansexismale == 'true':
            scanmissionplan.FanSexIsMale = True
        else:
            scanmissionplan.FanSexIsMale = False

        if fansexisfemale == 'true':
            scanmissionplan.FanSexIsFemale = True
        else:
            scanmissionplan.FanSexIsFemale = False

        if fansexisnone == 'true':
            scanmissionplan.FanSexIsNone = True
        else:
            scanmissionplan.FanSexIsNone = False

        if commenttext is not None and len(commenttext) > 0:
            commenttext_ids = ''
            commenttext_list = commenttext.split('\n')
            for i in range(len(commenttext_list)):
                comment = commenttext_list[i]
                if comment != '':
                    check_exists = CommentLibrary.objects.filter(Text=comment)
                    if check_exists.count() > 0:
                        id = check_exists.first().id
                        commenttext_ids = commenttext_ids + str(id) + ','
                    else:
                        NewComment = CommentLibrary()
                        NewComment.Text = comment
                        NewComment.save()
                        id = NewComment.id
                        commenttext_ids = commenttext_ids + str(id) + ','
            scanmissionplan.CommentTextID = commenttext_ids[:-1]

        scanmissionplan.save()
    elif eventtype == '关注任务':
        description = request.POST.get('description')
        peoplelimit = request.POST.get('peoplelimit')
        fansexismale = request.POST.get('fansexismale')
        fansexisfemale = request.POST.get('fansexisfemale')
        fansexisnone = request.POST.get('fansexisnone')
        followmissionplan = FollowMissionPlan.objects.get(id=dataid)
        followmissionplan.Description = description
        if peoplelimit is not None and peoplelimit != '' and peoplelimit != '0':
            followmissionplan.PeopleLimit = peoplelimit
        else:
            defaultfollowpeoplelimit = GetSystemConfig('关注人数上限默认值')
            followmissionplan.PeopleLimit = defaultfollowpeoplelimit
        if fansexismale == 'true':
            followmissionplan.FanSexIsMale = True
        else:
            followmissionplan.FanSexIsMale = False

        if fansexisfemale == 'true':
            followmissionplan.FanSexIsFemale = True
        else:
            followmissionplan.FanSexIsFemale = False

        if fansexisnone == 'true':
            followmissionplan.FanSexIsNone = True
        else:
            followmissionplan.FanSexIsNone = False

        followmissionplan.save()
    elif eventtype == '刷宝任务':
        description = request.POST.get('description')
        treasuremissionplan = TreasureMissionPlan.objects.get(id=dataid)
        treasuremissionplan.Description = description
        treasuremissionplan.save()
    return HttpResponse('OK')

# end 编辑任务模板

# begin 全部任务
@login_required
def allmissions(request):
    data_url = request.build_absolute_uri(reverse('Web:GetAllMissions'))
    devicemanage_url = request.build_absolute_uri(reverse('Web:DeviceManage'))
    acountlist_url = request.build_absolute_uri(reverse('Web:AccountList'))
    delete_url = request.build_absolute_uri(reverse('Web:DeleteAllMissions'))    
    location = copy.deepcopy(location_init)
    location['IsAllMissionsPage'] = True
    location['IsMissionMenu'] = True
    context = {'location': location, 'data_url': data_url,
               'mission_status': TaskStatus, 'devicemanage_url': devicemanage_url,
               'acountlist_url': acountlist_url, 'delete_url': delete_url}
    return render(request, 'pages/MissionManage/AllMissions.html', context)


@login_required
def getallmissions(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    generalSearch = request.POST.get('query[generalAllMissionsSearch]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    status = request.POST.get('query[allmissionstatus]')
    allmissioncolumn = request.POST.get('query[allmissioncolumn]')
    missionName = request.POST.get('query[missionname]')
    starttime = request.POST.get('query[starttime]')    
    endtime = request.POST.get('query[endtime]')      

    owner_id_list = []
    owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)
    data_list = AllMissions.objects.filter(Owner_id__in=owner_id_list)

    if generalSearch is not None and generalSearch != '':
        search_filter = Q()
        if allmissioncolumn == 'tiktok':
            search_filter = search_filter | Q(NickName__contains=generalSearch)
        elif allmissioncolumn == 'id':
            search_filter = search_filter | Q(MobilePhone_id=generalSearch)
        else:
            search_filter = search_filter | Q(NickName__contains=generalSearch)
            if str.isdigit(generalSearch):
                search_filter = search_filter | Q(MobilePhone_id=generalSearch)
        data_list = data_list.filter(search_filter)

    if missionName is not None and missionName != '':
        missionName_filter = Q()
        missionName_list = missionName[:-1].split(',')
        missionName_filter = missionName_filter | Q(
            MissionName__in=missionName_list)
        data_list = data_list.filter(missionName_filter)

    if status is not None and status != '':
        status_filter = Q()
        status_list = status[:-1].split(',')
        status_filter = status_filter | Q(Status__in=status_list)
        data_list = data_list.filter(status_filter)

    if starttime is not None and starttime != '' and endtime is not None and endtime != '':
        data_list = data_list.filter(
            CreateTime__range=(starttime, endtime))
    elif starttime is not None and starttime != '':
        data_list = data_list.filter(CreateTime__gte=starttime)
    elif endtime is not None and endtime != '':
        data_list = data_list.filter(CreateTime__lte=endtime)

    fields_list = AllMissions._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('MissionName')         

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values(
        'MissionName', 'id', 'Status', 'CreateTime',
        'StartTime', 'EndTime', 'FailReason', 'MobilePhone_id', 'NickName')
    data = []
    for i in range(len(data_result)):
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def delete_allmission_by_ids(request):
    missionid = request.POST.get('id')
    missionname = request.POST.get('missionname')  
    if missionname == '视频任务':  
        VideoMission.objects.filter(id=missionid).delete()
    elif missionname == '互刷任务':
        MutualBrushMission.objects.filter(id=missionid).delete()
    elif missionname == '养号任务':  
        MaintenanceNumberMission.objects.filter(id=missionid).delete()    
    elif missionname == '刷粉任务':
        ScanMission.objects.filter(id=missionid).delete()
    elif missionname == '关注任务': 
        FollowMission.objects.filter(id=missionid).delete()
    elif missionname == '刷宝任务':  
        TreasureMission.objects.filter(id=missionid).delete()       
    elif missionname == '观看直播任务':  
        WatchLiveMission.objects.filter(id=missionid).delete()      
    elif missionname == '修改签名任务':  
        mission = ChangeSignatureMission.objects.get(id=missionid)
        mission.TikTokAccount.NewDescribe = ''
        mission.TikTokAccount.save()
        mission.delete()                                       
    return HttpResponseRedirect(reverse('Web:AllMissions'))

# end 全部任务

# begin 挖宝任务
@login_required
def treasuremission(request):
    data_url = request.build_absolute_uri(
        reverse('Web:GetTreasureMission'))
    create_url = request.build_absolute_uri(
        reverse('Web:CreateTreasureMission'))
    delete_url = request.build_absolute_uri(
        reverse('Web:DeleteTreasureMission'))
    get_by_id_url = request.build_absolute_uri(
        reverse('Web:GetTreasureMissionByID'))
    edit_url = request.build_absolute_uri(
        reverse('Web:EditTreasureMission'))
    location = copy.deepcopy(location_init)
    location['IsTreasureMissionPage'] = True
    location['IsMissionMenu'] = True
    context = {'location': location, 'data_url': data_url, 'create_url': create_url,
               'delete_url': delete_url, 'get_by_id_url': get_by_id_url, 'edit_url': edit_url,
               'mission_status': TaskStatus}
    return render(request, 'pages/MissionManage/TreasureMission.html', context)


@login_required
def gettreasuremission(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    status = request.POST.get('query[treasuremissionstatus]')
    generalSearch = request.POST.get(
        'query[generalTreasureMissionSearch]')    
    starttime = request.POST.get('query[starttime]')    
    endtime = request.POST.get('query[endtime]')         

    owner_id_list = []
    owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)
    data_list = TreasureMission.objects.filter(Owner__id__in=owner_id_list)

    if generalSearch is not None and generalSearch != '':
        if str.isdigit(generalSearch):
            data_list = data_list.filter(MobilePhone__id=generalSearch)

    if status is not None and status != '':
        status_filter = Q()
        status_list = status[:-1].split(',')
        status_filter = status_filter | Q(Status__in=status_list)
        data_list = data_list.filter(status_filter)

    if starttime is not None and starttime != '' and endtime is not None and endtime != '':
        data_list = data_list.filter(
            CreateTime__range=(starttime, endtime))
    elif starttime is not None and starttime != '':
        data_list = data_list.filter(CreateTime__gte=starttime)
    elif endtime is not None and endtime != '':
        data_list = data_list.filter(CreateTime__lte=endtime)

    fields_list = TreasureMission._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')           

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values(
        'id', 'MobilePhone__id', 'Status', 'CreateTime', 'StartTime', 'EndTime', 'FailReason')
    data = []
    for i in range(len(data_result)):
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def delete_treasuremission_by_ids(request):
    ids = request.POST.get('ids')
    id_list = ids[:-1].split(',')
    if len(ids) > 0:
        TreasureMission.objects.filter(id__in=id_list).delete()
    return HttpResponseRedirect(reverse('Web:TreasureMission'))


@login_required
def createtreasuremission(request):
    device_id = request.POST.get('deviceid')
    device_id_list = device_id.split(',')
    starttime = request.POST.get('starttime')
    endtime = request.POST.get('endtime')
    if len(device_id_list) > 0:
        # 发布任务
        for i in range(len(device_id_list)):
            id = device_id_list[i]
            device = MobilePhone.objects.get(id=id)
            if device is not None:
                task = TreasureMission()
                task.MobilePhone = device
                task.Status = TaskStatus[0][0]
                task.Owner = request.user
                if starttime != '' and endtime != '':
                    task.StartTime = datetime.datetime.strptime(
                        starttime, '%Y-%m-%d %H:%M:%S')
                    task.EndTime = datetime.datetime.strptime(
                        endtime, '%Y-%m-%d %H:%M:%S')
                elif starttime != '':
                    task.StartTime = datetime.datetime.strptime(
                        starttime, '%Y-%m-%d %H:%M:%S')
                    task.EndTime = task.StartTime + datetime.timedelta(hours=1)
                elif endtime != '':
                    task.EndTime = datetime.datetime.strptime(
                        endtime, '%Y-%m-%d %H:%M:%S')
                    task.StartTime = task.EndTime - datetime.timedelta(hours=1)
                else:
                    task.StartTime = datetime.datetime.now()
                    task.EndTime = task.StartTime + datetime.timedelta(hours=1)
                task.Priority = 0
                task.save()
            else:
                return HttpResponse('Error')
        return HttpResponse(reverse('Web:TreasureMission'))
    else:
        return HttpResponse('Error')


@login_required
def edittreasuremission(request):
    data_id = request.POST.get('id')
    starttime = request.POST.get('starttime')
    endtime = request.POST.get('endtime')
    task = TreasureMission.objects.get(id=data_id)
    if starttime != '' and endtime != '':
        task.StartTime = datetime.datetime.strptime(
            starttime, '%Y-%m-%d %H:%M:%S')
        task.EndTime = datetime.datetime.strptime(endtime, '%Y-%m-%d %H:%M:%S')
    elif starttime != '':
        task.StartTime = datetime.datetime.strptime(
            starttime, '%Y-%m-%d %H:%M:%S')
        task.EndTime = task.StartTime + datetime.timedelta(hours=1)
    elif endtime != '':
        task.EndTime = datetime.datetime.strptime(endtime, '%Y-%m-%d %H:%M:%S')
        task.StartTime = task.EndTime - datetime.timedelta(hours=1)
    else:
        task.StartTime = datetime.datetime.now()
        task.EndTime = task.StartTime + datetime.timedelta(hours=1)
    task.save()
    return HttpResponse(reverse('Web:TreasureMission'))


@login_required
def gettreasuremissionbyid(request):
    data_id = request.POST.get('id')
    data = TreasureMission.objects.get(id=data_id)
    if data is not None:
        context = {
            'mobilephoneid': data.MobilePhone.id,
            'status': data.Status,
            'dataid': data.id,
            'starttime': data.StartTime,
            'endtime': data.EndTime,
        }
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('Error')

# end 挖宝任务

# begin 代理我的收益
@login_required
def agentincome(request):
    user_id = request.user.id
    agent = Agent.objects.get(Subscriber__id=user_id)
    agent_id = agent.id

    # 今日预估收入
    now = datetime.date.today()
    begintime = str(now)
    endtime = str(now + datetime.timedelta(days=1))
    sql = "EXEC [CalcAgentIncome] {},'{}','{}',{},'{}'".format(
        agent_id, begintime, endtime, 0, 'Total')
    cur = connection.cursor()
    rows = cur.execute(sql).fetchall()
    TodayOrderTotalMoney = rows[0][0] if rows[0][0] is not None else 0
    TodayTotalOrderCount = rows[0][1] if rows[0][1] is not None else 0  
    sql = "EXEC [CalcAgentMissionIncome] {},'{}','{}'".format(
        agent_id, begintime, endtime)
    cur = connection.cursor()
    rows = cur.execute(sql).fetchall()
    TodayMissionTotalMoney = rows[0][0] if rows[0][0] is not None else 0    
    TodayTotalMutualBrushMissionCount = rows[0][1] if rows[0][1] is not None else 0
    TodayTotalWatchLiveMissionCount = rows[0][2] if rows[0][2] is not None else 0 
    TodayTotalMoney = TodayOrderTotalMoney + TodayMissionTotalMoney 
    TodayTotalMissionCount = TodayTotalMutualBrushMissionCount + TodayTotalWatchLiveMissionCount

    # 上月实际收入
    month_income_list = AgentMonthRealityIncome.objects.filter(
        Agent__id=agent_id).order_by('-SummaryDate')
    if month_income_list.count() > 0:
        month_income = month_income_list.first()
        LastMonthTotalMoney = month_income.TotalMoney
    else:
        LastMonthTotalMoney = 0

    # 今日
    now = datetime.date.today()
    begintime = str(now)
    endtime = str(now + datetime.timedelta(days=1))
    sql = "EXEC [CalcAgentIncome] {},'{}','{}',{},'{}'".format(
        agent_id, begintime, endtime, 0, 'Myself')
    cur = connection.cursor()
    rows = cur.execute(sql).fetchall()
    TodayMyselfMoney = rows[0][0] if rows[0][0] is not None else 0
    TodayMyselfOrderCount = rows[0][1] if rows[0][1] is not None else 0

    sql = "EXEC [CalcAgentIncome] {},'{}','{}',{},'{}'".format(
        agent_id, begintime, endtime, 0, 'ABLevel')
    cur = connection.cursor()
    rows = cur.execute(sql).fetchall()
    TodayABLevelMoney = rows[0][0] if rows[0][0] is not None else 0
    TodayABLevelOrderCount = rows[0][1] if rows[0][1] is not None else 0

    sql = "EXEC [CalcAgentMissionIncome] {},'{}','{}'".format(
        agent_id, begintime, endtime)
    cur = connection.cursor()
    rows = cur.execute(sql).fetchall()
    TodayMissionMoney = rows[0][0] if rows[0][0] is not None else 0    
    TodayMutualBrushMissionCount = rows[0][1] if rows[0][1] is not None else 0
    TodayWatchLiveMissionCount = rows[0][2] if rows[0][2] is not None else 0 

    # 昨日
    begintime = str(now - datetime.timedelta(days=1))
    endtime = str(now)
    sql = "EXEC [CalcAgentIncome] {},'{}','{}',{},'{}'".format(
        agent_id, begintime, endtime, 0, 'Myself')
    cur = connection.cursor()
    rows = cur.execute(sql).fetchall()
    YestodayMyselfMoney = rows[0][0] if rows[0][0] is not None else 0
    YestodayMyselfOrderCount = rows[0][1] if rows[0][1] is not None else 0

    sql = "EXEC [CalcAgentIncome] {},'{}','{}',{},'{}'".format(
        agent_id, begintime, endtime, 0, 'ABLevel')
    cur = connection.cursor()
    rows = cur.execute(sql).fetchall()
    YestodayABLevelMoney = rows[0][0] if rows[0][0] is not None else 0
    YestodayABLevelOrderCount = rows[0][1] if rows[0][1] is not None else 0 

    sql = "EXEC [CalcAgentMissionIncome] {},'{}','{}'".format(
        agent_id, begintime, endtime)
    cur = connection.cursor()
    rows = cur.execute(sql).fetchall()
    YestodayMissionMoney = rows[0][0] if rows[0][0] is not None else 0    
    YestodayMutualBrushMissionCount = rows[0][1] if rows[0][1] is not None else 0
    YestodayWatchLiveMissionCount = rows[0][2] if rows[0][2] is not None else 0    

    # 最近7日
    begintime = str(now - datetime.timedelta(days=6))
    endtime = str(now)
    sql = "EXEC [CalcAgentIncome] {},'{}','{}',{},'{}'".format(
        agent_id, begintime, endtime, 0, 'Myself')
    cur = connection.cursor()
    rows = cur.execute(sql).fetchall()
    SevendayMyselfMoney = rows[0][0] if rows[0][0] is not None else 0
    SevendayMyselfOrderCount = rows[0][1] if rows[0][1] is not None else 0

    sql = "EXEC [CalcAgentIncome] {},'{}','{}',{},'{}'".format(
        agent_id, begintime, endtime, 0, 'ABLevel')
    cur = connection.cursor()
    rows = cur.execute(sql).fetchall()
    SevendayABLevelMoney = rows[0][0] if rows[0][0] is not None else 0
    SevendayABLevelOrderCount = rows[0][1] if rows[0][1] is not None else 0    

    sql = "EXEC [CalcAgentMissionIncome] {},'{}','{}'".format(
        agent_id, begintime, endtime)
    cur = connection.cursor()
    rows = cur.execute(sql).fetchall()
    SevendayMissionMoney = rows[0][0] if rows[0][0] is not None else 0    
    SevendayMutualBrushMissionCount = rows[0][1] if rows[0][1] is not None else 0
    SevendayWatchLiveMissionCount = rows[0][2] if rows[0][2] is not None else 0       

    # 本月
    endtime = str(now + datetime.timedelta(days=1))
    day = now.day
    if day > 25:
        begintime = str(datetime.datetime(now.year, now.month, 26))
    else:
        if now.month == 1:
            begintime = str(datetime.datetime(now.year - 1, 12, 26))
        else:
            begintime = str(datetime.datetime(now.year, now.month - 1, 26))
    sql = "EXEC [CalcAgentIncome] {},'{}','{}',{},'{}'".format(
        agent_id, begintime, endtime, 0, 'Myself')
    cur = connection.cursor()
    rows = cur.execute(sql).fetchall()
    CurrentMonthMyselfMoney = rows[0][0] if rows[0][0] is not None else 0
    CurrentMonthMyselfOrderCount = rows[0][1] if rows[0][1] is not None else 0

    sql = "EXEC [CalcAgentIncome] {},'{}','{}',{},'{}'".format(
        agent_id, begintime, endtime, 0, 'ABLevel')
    cur = connection.cursor()
    rows = cur.execute(sql).fetchall()
    CurrentMonthABLevelMoney = rows[0][0] if rows[0][0] is not None else 0
    CurrentMonthABLevelOrderCount = rows[0][1] if rows[0][1] is not None else 0

    sql = "EXEC [CalcAgentMissionIncome] {},'{}','{}'".format(
        agent_id, begintime, endtime)
    cur = connection.cursor()
    rows = cur.execute(sql).fetchall()
    CurrentMonthMissionMoney = rows[0][0] if rows[0][0] is not None else 0    
    CurrentMonthMutualBrushMissionCount = rows[0][1] if rows[0][1] is not None else 0
    CurrentMonthWatchLiveMissionCount = rows[0][2] if rows[0][2] is not None else 0     

    # 上月
    day = now.day
    if day > 25:
        endtime = str(datetime.datetime(now.year, now.month, 26))
        if now.month == 1:
            begintime = str(datetime.datetime(now.year - 1, 12, 26))
        else:
            begintime = str(datetime.datetime(now.year, now.month - 1, 26))
    else:
        if now.month == 1:
            endtime = str(datetime.datetime(now.year - 1, 12, 26))
            begintime = str(datetime.datetime(now.year - 1, 11, 26))
        else:
            endtime = str(datetime.datetime(now.year, now.month - 1, 26))
            if now.month == 2:
                begintime = str(datetime.datetime(now.year - 1, 12, 26))
            else:
                begintime = str(datetime.datetime(now.year, now.month - 2, 26))
    sql = "EXEC [CalcAgentIncome] {},'{}','{}',{},'{}'".format(
        agent_id, begintime, endtime, 1, 'Myself')
    cur = connection.cursor()
    rows = cur.execute(sql).fetchall()
    LastMonthMyselfMoney = rows[0][0] if rows[0][0] is not None else 0
    LastMonthMyselfOrderCount = rows[0][1] if rows[0][1] is not None else 0

    sql = "EXEC [CalcAgentIncome] {},'{}','{}',{},'{}'".format(
        agent_id, begintime, endtime, 1, 'ABLevel')
    cur = connection.cursor()
    rows = cur.execute(sql).fetchall()
    LastMonthABLevelMoney = rows[0][0] if rows[0][0] is not None else 0
    LastMonthABLevelOrderCount = rows[0][1] if rows[0][1] is not None else 0   

    sql = "EXEC [CalcAgentMissionIncome] {},'{}','{}'".format(
        agent_id, begintime, endtime)
    cur = connection.cursor()
    rows = cur.execute(sql).fetchall()
    LastMonthMissionMoney = rows[0][0] if rows[0][0] is not None else 0    
    LastMonthMutualBrushMissionCount = rows[0][1] if rows[0][1] is not None else 0
    LastMonthWatchLiveMissionCount = rows[0][2] if rows[0][2] is not None else 0      

    location = copy.deepcopy(location_init)
    location['IsAgentIncomePage'] = True
    context = {'location': location, 'TodayTotalMoney': TodayTotalMoney, 'TodayTotalOrderCount': TodayTotalOrderCount,
               'LastMonthTotalMoney': LastMonthTotalMoney, 'TodayTotalMissionCount': TodayTotalMissionCount,
               'TodayMyselfMoney': TodayMyselfMoney, 'TodayMyselfOrderCount': TodayMyselfOrderCount, 
               'TodayABLevelMoney': TodayABLevelMoney, 'TodayABLevelOrderCount': TodayABLevelOrderCount,
               'YestodayMyselfMoney': YestodayMyselfMoney, 'YestodayMyselfOrderCount': YestodayMyselfOrderCount,
               'YestodayABLevelMoney': YestodayABLevelMoney, 'YestodayABLevelOrderCount': YestodayABLevelOrderCount,
               'SevendayMyselfMoney': SevendayMyselfMoney, 'SevendayABLevelMoney': SevendayABLevelMoney,
               'SevendayMyselfOrderCount': SevendayMyselfOrderCount, 'SevendayABLevelOrderCount': SevendayABLevelOrderCount,
               'CurrentMonthMyselfMoney': CurrentMonthMyselfMoney, 'CurrentMonthABLevelMoney': CurrentMonthABLevelMoney,
               'CurrentMonthMyselfOrderCount': CurrentMonthMyselfOrderCount, 'CurrentMonthABLevelOrderCount': CurrentMonthABLevelOrderCount,
               'LastMonthMyselfMoney': LastMonthMyselfMoney, 'LastMonthABLevelMoney': LastMonthABLevelMoney,
               'LastMonthMyselfOrderCount': LastMonthMyselfOrderCount, 'LastMonthABLevelOrderCount': LastMonthABLevelOrderCount,
               'TodayMissionMoney': TodayMissionMoney, 'TodayMutualBrushMissionCount': TodayMutualBrushMissionCount, 
               'TodayWatchLiveMissionCount': TodayWatchLiveMissionCount,
               'YestodayMissionMoney': YestodayMissionMoney, 'YestodayMutualBrushMissionCount': YestodayMutualBrushMissionCount,
               'YestodayWatchLiveMissionCount': YestodayWatchLiveMissionCount,
               'SevendayMissionMoney': SevendayMissionMoney, 'SevendayMutualBrushMissionCount': SevendayMutualBrushMissionCount,
               'SevendayWatchLiveMissionCount': SevendayWatchLiveMissionCount,
               'CurrentMonthMissionMoney': CurrentMonthMissionMoney, 'CurrentMonthMutualBrushMissionCount': CurrentMonthMutualBrushMissionCount,
               'CurrentMonthWatchLiveMissionCount': CurrentMonthWatchLiveMissionCount,
               'LastMonthMissionMoney': LastMonthMissionMoney, 'LastMonthMutualBrushMissionCount': LastMonthMutualBrushMissionCount,
               'LastMonthWatchLiveMissionCount': LastMonthWatchLiveMissionCount}
    return render(request, 'pages/Agent/AgentIncome.html', context)
# end 代理我的收益


# begin 代理余额提现
@login_required
def agentwithdraw(request):
    create_withdraw_url = request.build_absolute_uri(
            reverse('Web:CreateAgentApplyForWithdraw'))
    agent_withdraw_list_url = request.build_absolute_uri(
            reverse('Web:GetAgentWithdrawList'))
    location = copy.deepcopy(location_init)
    location['IsAgentWithdrawPage'] = True
    context = {'location': location, 'create_withdraw_url': create_withdraw_url,
               'agent_withdraw_list_url': agent_withdraw_list_url}
    return render(request, 'pages/Agent/AgentWithdraw.html', context)


@login_required
def getagentwithdrawlist(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')    

    user_id = request.user.id
    agent = Agent.objects.get(Subscriber__id=user_id)

    data_list = AgentApplyForWithdraw.objects.filter(Agent=agent)

    data_list = data_list.order_by('-ApplyDate')

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values(
        'ApplyDate', 'Money', 'IsPass', 'ApproveDate')
    data = []
    for i in range(len(data_result)):
        data_result[i]['ApplyDate'] = data_result[i]['ApplyDate'].date()
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")

# end 代理余额提现

# begin 代理账号数据
@login_required
def agentaccountdata(request):
    user_id = request.user.id
    agent = Agent.objects.get(Subscriber__id=user_id)
    agent_id = agent.id

    # 今日
    now = datetime.date.today()
    begintime = str(now)
    endtime = str(now + datetime.timedelta(days=1))

    # 昨日
    begintime = str(now - datetime.timedelta(days=1))
    endtime = str(now)

    # 最近7日
    begintime = str(now - datetime.timedelta(days=6))
    endtime = str(now)

    # 本月
    endtime = str(now + datetime.timedelta(days=1))
    day = now.day
    if day > 25:
        begintime = str(datetime.datetime(now.year, now.month, 26))
    else:
        if now.month == 1:
            begintime = str(datetime.datetime(now.year - 1, 12, 26))
        else:
            begintime = str(datetime.datetime(now.year, now.month - 1, 26))

    get_agent_account_data_url = request.build_absolute_uri(
            reverse('Web:GetAgentAccountData'))
    location = copy.deepcopy(location_init)
    location['IsAgentAccountDataPage'] = True
    context = {'location': location, 'get_agent_account_data_url': get_agent_account_data_url}
    return render(request, 'pages/Agent/AgentAccountData.html', context)


@login_required
def getagentaccountdata(request):
    num = int(request.POST.get('num'))

    # 找对应账号
    user_id = request.user.id
    agent = Agent.objects.get(Subscriber__id=user_id)

    account_filter = TikTokAccount.objects.filter(mobilephone__Agent=agent)
    account_list = list(account_filter.values_list('id', flat=True))

    if len(account_list) > 0:
        account_id = account_list[num % len(account_list)]
        account = TikTokAccount.objects.get(id=account_id)
        # 昵称
        nickname = account.NickName

        # 今日数据
        Fans = account.Fans
        Praise = account.Praise
        TodayWorksList = Works.objects.filter(TikTokAccount=account).aggregate(NumOfPlay=Coalesce(Sum('NumOfPlay'), 0), NumOfComments=Coalesce(
                    Sum('NumOfComments'), 0))        
        TotalNumOfPlay = TodayWorksList['NumOfPlay']
        TotalNumOfComments = TodayWorksList['NumOfComments']
        Video = account.Video

        # 今日增量
        now = datetime.date.today()        
        Yestoday = str(now - datetime.timedelta(days=1))        
        TikTokAccountDaySummaryYestoday_filter = Q()
        TikTokAccountDaySummaryYestoday_filter = TikTokAccountDaySummaryYestoday_filter & Q(
            TikTokAccount_id=account_id)
        TikTokAccountDaySummaryYestoday_filter = TikTokAccountDaySummaryYestoday_filter & Q(
            Summary_Date=Yestoday)
        YestodayAccountList = TikTokAccountDaySummary.objects.filter(TikTokAccountDaySummaryYestoday_filter).aggregate(Fans=Coalesce(
            Sum('Fans'), 0), Praise=Coalesce(Sum('Praise'), 0), Video=Coalesce(Sum('Video'), 0))   

        WorksDaySummaryYestoday_filter = Q()
        WorksDaySummaryYestoday_filter = WorksDaySummaryYestoday_filter & Q(
            Work__TikTokAccount__id=account_id)
        WorksDaySummaryYestoday_filter = WorksDaySummaryYestoday_filter & Q(
            Summary_Date=Yestoday)
        YestodayWorksList = WorksDaySummary.objects.filter(
            WorksDaySummaryYestoday_filter).aggregate(NumOfPlay=Coalesce(Sum('NumOfPlay'), 0), NumOfComments=Coalesce(Sum('NumOfComments'), 0))        
        
        today_FansIncrease = account.Fans - YestodayAccountList['Fans']
        today_PraiseIncrease = account.Praise - YestodayAccountList['Praise']
        today_TotalNumOfPlayIncrease = TodayWorksList['NumOfPlay'] - YestodayWorksList['NumOfPlay']
        today_TotalNumOfCommentsIncrease = TodayWorksList['NumOfComments'] - YestodayWorksList['NumOfComments']
        today_VideoIncrease = account.Video - YestodayAccountList['Video']

        # 昨日增量
        TheDayBeforeYestoday = str(now - datetime.timedelta(days=2))
        TikTokAccountDaySummaryTheDayBeforeYestoday_filter = Q()
        TikTokAccountDaySummaryTheDayBeforeYestoday_filter = TikTokAccountDaySummaryTheDayBeforeYestoday_filter & Q(
            TikTokAccount_id=account_id)
        TikTokAccountDaySummaryTheDayBeforeYestoday_filter = TikTokAccountDaySummaryTheDayBeforeYestoday_filter & Q(
            Summary_Date=TheDayBeforeYestoday)
        TheDayBeforeYestodayAccountList = TikTokAccountDaySummary.objects.filter(TikTokAccountDaySummaryTheDayBeforeYestoday_filter).aggregate(Fans=Coalesce(
            Sum('Fans'), 0), Praise=Coalesce(Sum('Praise'), 0), Video=Coalesce(Sum('Video'), 0))   

        WorksDaySummaryTheDayBeforeYestoday_filter = Q()
        WorksDaySummaryTheDayBeforeYestoday_filter = WorksDaySummaryTheDayBeforeYestoday_filter & Q(
            Work__TikTokAccount__id=account_id)
        WorksDaySummaryTheDayBeforeYestoday_filter = WorksDaySummaryTheDayBeforeYestoday_filter & Q(
            Summary_Date=TheDayBeforeYestoday)
        TheDayBeforeYestodayWorksList = WorksDaySummary.objects.filter(
            WorksDaySummaryTheDayBeforeYestoday_filter).aggregate(NumOfPlay=Coalesce(Sum('NumOfPlay'), 0), NumOfComments=Coalesce(Sum('NumOfComments'), 0))        
        
        yestoday_FansIncrease = YestodayAccountList['Fans'] - TheDayBeforeYestodayAccountList['Fans']
        yestoday_PraiseIncrease = YestodayAccountList['Praise'] - TheDayBeforeYestodayAccountList['Praise']
        yestoday_TotalNumOfPlayIncrease = YestodayWorksList['NumOfPlay'] - TheDayBeforeYestodayWorksList['NumOfPlay']
        yestoday_TotalNumOfCommentsIncrease = YestodayWorksList['NumOfComments'] - TheDayBeforeYestodayWorksList['NumOfComments']
        yestoday_VideoIncrease = YestodayAccountList['Video'] - TheDayBeforeYestodayAccountList['Video']       

        # 近7日增量
        SevenDay = str(now - datetime.timedelta(days=6))
        TikTokAccountDaySummarySevenDay_filter = Q()
        TikTokAccountDaySummarySevenDay_filter = TikTokAccountDaySummarySevenDay_filter & Q(
            TikTokAccount_id=account_id)
        TikTokAccountDaySummarySevenDay_filter = TikTokAccountDaySummarySevenDay_filter & Q(
            Summary_Date=SevenDay)
        SevenDayAccountList = TikTokAccountDaySummary.objects.filter(TikTokAccountDaySummarySevenDay_filter).aggregate(Fans=Coalesce(
            Sum('Fans'), 0), Praise=Coalesce(Sum('Praise'), 0), Video=Coalesce(Sum('Video'), 0))   

        WorksDaySummarySevenDay_filter = Q()
        WorksDaySummarySevenDay_filter = WorksDaySummarySevenDay_filter & Q(
            Work__TikTokAccount__id=account_id)
        WorksDaySummarySevenDay_filter = WorksDaySummarySevenDay_filter & Q(
            Summary_Date=SevenDay)
        SevenDayWorksList = WorksDaySummary.objects.filter(
            WorksDaySummarySevenDay_filter).aggregate(NumOfPlay=Coalesce(Sum('NumOfPlay'), 0), NumOfComments=Coalesce(Sum('NumOfComments'), 0))        
        
        sevenday_FansIncrease = account.Fans - SevenDayAccountList['Fans']
        sevenday_PraiseIncrease = account.Praise - SevenDayAccountList['Praise']
        sevenday_TotalNumOfPlayIncrease = TodayWorksList['NumOfPlay'] - SevenDayWorksList['NumOfPlay']
        sevenday_TotalNumOfCommentsIncrease = TodayWorksList['NumOfComments'] - SevenDayWorksList['NumOfComments']
        sevenday_VideoIncrease = account.Video - SevenDayAccountList['Video']

        # 本月增量
        day = now.day
        if day > 25:
            CurrentMonth = str(datetime.datetime(now.year, now.month, 26))
        else:
            if now.month == 1:
                CurrentMonth = str(datetime.datetime(now.year - 1, 12, 26))
            else:
                CurrentMonth = str(datetime.datetime(now.year, now.month - 1, 26))
        TikTokAccountDaySummaryCurrentMonth_filter = Q()
        TikTokAccountDaySummaryCurrentMonth_filter = TikTokAccountDaySummaryCurrentMonth_filter & Q(
            TikTokAccount_id=account_id)
        TikTokAccountDaySummaryCurrentMonth_filter = TikTokAccountDaySummaryCurrentMonth_filter & Q(
            Summary_Date=SevenDay)
        CurrentMonthAccountList = TikTokAccountDaySummary.objects.filter(TikTokAccountDaySummaryCurrentMonth_filter).aggregate(Fans=Coalesce(
            Sum('Fans'), 0), Praise=Coalesce(Sum('Praise'), 0), Video=Coalesce(Sum('Video'), 0))   

        WorksDaySummaryCurrentMonth_filter = Q()
        WorksDaySummaryCurrentMonth_filter = WorksDaySummaryCurrentMonth_filter & Q(
            Work__TikTokAccount__id=account_id)
        WorksDaySummaryCurrentMonth_filter = WorksDaySummaryCurrentMonth_filter & Q(
            Summary_Date=SevenDay)
        CurrentMonthWorksList = WorksDaySummary.objects.filter(
            WorksDaySummaryCurrentMonth_filter).aggregate(NumOfPlay=Coalesce(Sum('NumOfPlay'), 0), NumOfComments=Coalesce(Sum('NumOfComments'), 0))        
        
        currentmonth_FansIncrease = account.Fans - CurrentMonthAccountList['Fans']
        currentmonth_PraiseIncrease = account.Praise - CurrentMonthAccountList['Praise']
        currentmonth_TotalNumOfPlayIncrease = TodayWorksList['NumOfPlay'] - CurrentMonthWorksList['NumOfPlay']
        currentmonth_TotalNumOfCommentsIncrease = TodayWorksList['NumOfComments'] - CurrentMonthWorksList['NumOfComments']
        currentmonth_VideoIncrease = account.Video - CurrentMonthAccountList['Video']                

        context = {'nickname': nickname,
                'Fans': Fans, 'Praise': Praise, 'TotalNumOfPlay': TotalNumOfPlay,
                'TotalNumOfComments': TotalNumOfComments, 'Video': Video,
                'today_FansIncrease': today_FansIncrease, 'today_PraiseIncrease': today_PraiseIncrease,
                'today_TotalNumOfPlayIncrease': today_TotalNumOfPlayIncrease, 'today_TotalNumOfCommentsIncrease': today_TotalNumOfCommentsIncrease,
                'today_VideoIncrease': today_VideoIncrease,
                'yestoday_FansIncrease': yestoday_FansIncrease, 'yestoday_PraiseIncrease': yestoday_PraiseIncrease,
                'yestoday_TotalNumOfPlayIncrease': yestoday_TotalNumOfPlayIncrease, 'yestoday_TotalNumOfCommentsIncrease': yestoday_TotalNumOfCommentsIncrease,
                'yestoday_VideoIncrease': yestoday_VideoIncrease,
                'sevenday_FansIncrease': sevenday_FansIncrease, 'sevenday_PraiseIncrease': sevenday_PraiseIncrease,
                'sevenday_TotalNumOfPlayIncrease': sevenday_TotalNumOfPlayIncrease, 'sevenday_TotalNumOfCommentsIncrease': sevenday_TotalNumOfCommentsIncrease,
                'sevenday_VideoIncrease': sevenday_VideoIncrease,
                'currentmonth_FansIncrease': currentmonth_FansIncrease, 'currentmonth_PraiseIncrease': currentmonth_PraiseIncrease,
                'currentmonth_TotalNumOfPlayIncrease': currentmonth_TotalNumOfPlayIncrease, 'currentmonth_TotalNumOfCommentsIncrease': currentmonth_TotalNumOfCommentsIncrease,
                'currentmonth_VideoIncrease': currentmonth_VideoIncrease}
    else:
        context = {}          
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")

# end 代理账号数据

# begin 系统配置
def GetSystemConfig(name):
    config = SystemConfig.objects.filter(Name=name)
    if config is not None and config.count() > 0:
        value = config.first().Value
        return int(value)
    else:
        return 1
# end 系统配置


# begin 观看直播任务
@login_required
def watchlivemission(request):
    data_url = request.build_absolute_uri(
        reverse('Web:GetWatchLiveMission'))
    create_url = request.build_absolute_uri(
        reverse('Web:CreateWatchLiveMission'))
    delete_url = request.build_absolute_uri(
        reverse('Web:DeleteWatchLiveMission'))
    get_by_id_url = request.build_absolute_uri(
        reverse('Web:GetWatchLiveMissionByID'))
    edit_url = request.build_absolute_uri(
        reverse('Web:EditWatchLiveMission'))
    defaultinterval = GetSystemConfig('观看直播任务默认延时')
    defaultlasttime = GetSystemConfig('观看直播任务默认持续时间')    
    defaultcommenttimes = GetSystemConfig('观看直播任务默认发言次数')        
    config = {'defaultinterval': defaultinterval, 'defaultlasttime': defaultlasttime, 'defaultcommenttimes': defaultcommenttimes}        
    location = copy.deepcopy(location_init)
    location['IsWatchLiveMissionPage'] = True
    location['IsMissionMenu'] = True
    context = {'location': location, 'data_url': data_url, 'create_url': create_url,
               'delete_url': delete_url, 'get_by_id_url': get_by_id_url, 'edit_url': edit_url,
               'mission_status': TaskStatus, 'config': config}
    return render(request, 'pages/MissionManage/WatchLiveMission.html', context)


@login_required
def getwatchlivemission(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    generalSearch = request.POST.get(
        'query[generalWatchLiveMissionSearch]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    status = request.POST.get('query[watchlivemissionstatus]')
    starttime = request.POST.get('query[starttime]')    
    endtime = request.POST.get('query[endtime]')  

    owner_id_list = []
    owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)
    data_list = WatchLiveMission.objects.filter(Owner__id__in=owner_id_list)

    if generalSearch is not None and generalSearch != '':
        if str.isdigit(generalSearch):
            data_list = data_list.filter(MobilePhone__id=generalSearch)

    if status is not None and status != '':
        status_filter = Q()
        status_list = status[:-1].split(',')
        status_filter = status_filter | Q(Status__in=status_list)
        data_list = data_list.filter(status_filter)

    if starttime is not None and starttime != '' and endtime is not None and endtime != '':
        data_list = data_list.filter(
            CreateTime__range=(starttime, endtime))
    elif starttime is not None and starttime != '':
        data_list = data_list.filter(CreateTime__gte=starttime)
    elif endtime is not None and endtime != '':
        data_list = data_list.filter(CreateTime__lte=endtime)

    fields_list = WatchLiveMission._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')        

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values(
        'id', 'MobilePhone__id', 'Status', 'TargetURL', 'CommentText', 'CommentTimes', 
        'CreateTime', 'StartTime', 'EndTime', 'FailReason', 'MissionIncome')
    data = []
    for i in range(len(data_result)):
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def delete_watchlivemission_by_ids(request):
    ids = request.POST.get('ids')
    id_list = ids[:-1].split(',')
    if len(ids) > 0:
        WatchLiveMission.objects.filter(id__in=id_list).delete()
    return HttpResponseRedirect(reverse('Web:WatchLiveMission'))


@login_required
def createwatchlivemission(request):
    device_id = request.POST.get('deviceid')
    work_mobile_id_list = device_id.split(',')
    targeturl = request.POST.get('targeturl')
    starttime = request.POST.get('starttime')
    interval = request.POST.get('interval')
    lasttime = request.POST.get('lasttime')
    commenttext = request.POST.get('commenttext')
    commenttimes = request.POST.get('commenttimes')
    missionincome = decimal.Decimal(request.POST.get('missionincome'))          

    # 处理留言，#号开头的留言只用一次
    commenttext_list = commenttext.split('\n')
    repeat_commenttext_list = []
    no_repeat_commenttext_list = []
    if len(commenttext_list) > 0:
        for i in range(len(commenttext_list)):
            text = commenttext_list[i]
            if text != '':
                if text.startswith('#'):
                    no_repeat_commenttext_list.append(text)
                else:
                    repeat_commenttext_list.append(text)

    if work_mobile_id_list is not None and len(work_mobile_id_list) > 0:
        # 新建任务
        for i in range(len(work_mobile_id_list)):
            mobile_id = work_mobile_id_list[i]
            mobile = MobilePhone.objects.get(id=mobile_id)
            if mobile is not None:
                task = WatchLiveMission()
                task.MobilePhone = mobile
                task.Status = TaskStatus[0][0]
                task.Owner = request.user
                task.TargetURL = targeturl
                final_comment_text = ''
                if len(repeat_commenttext_list) > 0:
                    final_comment_text = "|".join(repeat_commenttext_list)
                if len(no_repeat_commenttext_list) > 0:
                    if final_comment_text == '':
                        final_comment_text = no_repeat_commenttext_list[0]
                    else:
                        final_comment_text = final_comment_text + '|' + no_repeat_commenttext_list[0]
                    del no_repeat_commenttext_list[0]
                task.CommentText = final_comment_text
                if commenttimes is not None and commenttimes != '':
                    task.CommentTimes = int(commenttimes)
                else:
                    task.CommentTimes = int(GetSystemConfig('观看直播任务默认发言次数'))     

                if starttime is not None and starttime != '':
                    baseStartTime = datetime.datetime.strptime(
                        starttime, '%Y-%m-%d %H:%M:%S')
                else:
                    baseStartTime = datetime.datetime.now()

                if interval is not None and interval != '':
                    interval = int(interval)
                else:
                    interval = int(GetSystemConfig('观看直播任务默认延时'))     

                if lasttime is not None and lasttime != '':
                    lasttime = int(lasttime)
                else:
                    lasttime = int(GetSystemConfig('观看直播任务默认持续时间'))                                               
                
                task.StartTime = baseStartTime + datetime.timedelta(minutes=random.randint(0,interval))
                task.EndTime = task.StartTime + datetime.timedelta(minutes=lasttime) + datetime.timedelta(minutes=random.randint(0,interval))
                task.Priority = 0
                task.MissionIncome = missionincome
                task.save()
            else:
                return HttpResponse('Error')

        return HttpResponse(reverse('Web:WatchLiveMission'))
    else:
        return HttpResponse('Error')


@login_required
def editwatchlivemission(request):
    data_id = request.POST.get('id')
    targeturl = request.POST.get('targeturl')
    commenttext = request.POST.get('commenttext')
    commenttimes = request.POST.get('commenttimes')
    starttime = request.POST.get('starttime')
    endtime = request.POST.get('endtime')
    task = WatchLiveMission.objects.get(id=data_id)
    task.TargetURL = targeturl
    task.CommentText = commenttext.replace('\n', '|')
    if commenttimes is not None and commenttimes != '':
        task.CommentTimes = int(commenttimes)
    else:
        task.CommentTimes = int(GetSystemConfig('观看直播任务默认发言次数'))    

    if starttime != '' and endtime != '':
        task.StartTime = datetime.datetime.strptime(
            starttime, '%Y-%m-%d %H:%M:%S')
        task.EndTime = datetime.datetime.strptime(endtime, '%Y-%m-%d %H:%M:%S')
    elif starttime != '':
        task.StartTime = datetime.datetime.strptime(
            starttime, '%Y-%m-%d %H:%M:%S')
        task.EndTime = task.StartTime + datetime.timedelta(hours=1)
    elif endtime != '':
        task.EndTime = datetime.datetime.strptime(endtime, '%Y-%m-%d %H:%M:%S')
        task.StartTime = task.EndTime - datetime.timedelta(hours=1)
    else:
        task.StartTime = datetime.datetime.now()
        task.EndTime = task.StartTime + datetime.timedelta(hours=1)

    task.save()
    return HttpResponse(reverse('Web:WatchLiveMission'))


@login_required
def getwatchlivemissionbyid(request):
    data_id = request.POST.get('id')
    data = WatchLiveMission.objects.get(id=data_id)
    if data is not None:
        context = {
            'mobilephoneid': data.MobilePhone.id,
            'status': data.Status,
            'targeturl': data.TargetURL,
            'commenttext': data.CommentText.replace('|', '\n'),
            'commenttimes': data.CommentTimes,
            'dataid': data.id,
            'starttime': data.StartTime,
            'endtime': data.EndTime,            
        }
        return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                            content_type="application/json,charset=utf-8")
    else:
        return HttpResponse('Error')

# end 观看直播任务

# begin 签名管理
@login_required
def signaturemanage(request): 
    data_url = request.build_absolute_uri(
        reverse('Web:GetSignatureManage'))
    create_mission_url = request.build_absolute_uri(
        reverse('Web:CreateChangeSignatureMission'))
    muti_create_mission_url = request.build_absolute_uri(
        reverse('Web:MutiCreateChangeSignatureMission'))        
    get_by_id_url = request.build_absolute_uri(
        reverse('Web:GetSignatureManageByID'))   
    devicemanage_url = request.build_absolute_uri(reverse('Web:DeviceManage'))       
    acountlist_url = request.build_absolute_uri(reverse('Web:AccountList'))    
    groups = TikTokAccountGroup.objects.filter(Owner=request.user)
    location = copy.deepcopy(location_init)
    location['IsSignatureManagePage'] = True
    location['IsSignatureManageMenu'] = True
    context = {'location': location, 'data_url': data_url, 'create_mission_url': create_mission_url,
               'get_by_id_url': get_by_id_url, 'devicemanage_url': devicemanage_url,
               'acountlist_url': acountlist_url, 'groups': groups, 
               'muti_create_mission_url': muti_create_mission_url}
    return render(request, 'pages/SignatureManage/SignatureManagePage.html', context)


@login_required
def getsignaturemanage(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    generalSearch = request.POST.get('query[generalSignatureManageSearch]')
    signaturemanagecolumn = request.POST.get('query[signaturemanagecolumn]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    group = request.POST.get('query[group]')

    owner_id_list = []
    owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)
    data_list = TikTokAccount.objects.filter(Owner__id__in=owner_id_list)

    if generalSearch is not None and generalSearch != '':
        serarch_filter = Q()
        if signaturemanagecolumn == 'nickname':
            serarch_filter = serarch_filter | Q(
                NickName__contains=generalSearch)
        elif signaturemanagecolumn == 'mobileid':
            if str.isdigit(generalSearch):
                serarch_filter = serarch_filter | Q(mobilephone__id=generalSearch)
        else:
            serarch_filter = serarch_filter | Q(
                NickName__contains=generalSearch)
            if str.isdigit(generalSearch):
                serarch_filter = serarch_filter | Q(
                    mobilephone__id=generalSearch)
        data_list = data_list.filter(serarch_filter)

    if group is not None and group != '':
        group_filter = Q()
        if '-1' in group:
            group_filter = group_filter | Q(Group=None)
        group_list = group[:-1].split(',')
        group_filter = group_filter | Q(Group__id__in=group_list)
        data_list = data_list.filter(group_filter)
        

    fields_list = TikTokAccount._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values('id', 'NickName', 'Describe',
                                                 'mobilephone__id', 'NewDescribe', 'Group__Name')
    data = []
    for i in range(len(data_result)):
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def getsignaturemanagebyid(request):
    data_id = request.POST.get('id')
    data = TikTokAccount.objects.get(id=data_id)   
    if data is not None:
        if data.mobilephone_set.count() > 0:
            mobile = data.mobilephone_set.first()
            context = {
                'dataid': data.id,
                'deviceid': mobile.id,
                'newdescribe': data.NewDescribe,
                'describe': data.Describe,       
                'nickname': data.NickName,     
            }
            return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                                content_type="application/json,charset=utf-8")
        else:
            return HttpResponse('Error')
    else:
        return HttpResponse('Error')


@login_required
def createchangesignaturemission(request):
    device_id = request.POST.get('deviceid')
    account_id = request.POST.get('id')
    newdescribe = request.POST.get('newdescribe')
    
    device = MobilePhone.objects.get(id=device_id)
    account = TikTokAccount.objects.get(id=account_id)
    if device is not None:
        account.NewDescribe = newdescribe
        account.save()
        task = ChangeSignatureMission()
        task.MobilePhone = device
        task.TikTokAccount = account
        task.Describe = account.Describe
        task.NewDescribe = account.NewDescribe
        task.Status = TaskStatus[0][0]
        task.Owner = request.user
        task.StartTime = datetime.datetime.now()
        task.Priority = 0
        task.save()
    else:
        return HttpResponse('Error')
    return HttpResponse(reverse('Web:SignatureManage'))


@login_required
def muticreatechangesignaturemission(request):
    account_id_str = request.POST.get('accountids')
    account_id_list = account_id_str[:-1].split(',')
    newdescribe = request.POST.get('newdescribe')
    
    if len(account_id_list) > 0:
        for i in range(len(account_id_list)):
            account_id = account_id_list[i]
            account = TikTokAccount.objects.get(id=account_id)
            if account.NewDescribe is not None and account.NewDescribe != '':
                continue
            if account.mobilephone_set.count() == 0:
                continue
            device = account.mobilephone_set.first()          
            if device is not None:
                account.NewDescribe = newdescribe
                account.save()
                task = ChangeSignatureMission()
                task.MobilePhone = device
                task.TikTokAccount = account
                task.Describe = account.Describe
                task.NewDescribe = account.NewDescribe
                task.Status = TaskStatus[0][0]
                task.Owner = request.user
                task.StartTime = datetime.datetime.now()
                task.Priority = 0
                task.save()
            else:
                return HttpResponse('Error')
        return HttpResponse(reverse('Web:SignatureManage'))
    else:
        return HttpResponse('Error')        


# end 签名管理   

# begin 修改签名任务
@login_required
def changesignaturemission(request):    
    data_url = request.build_absolute_uri(
        reverse('Web:GetChangeSignatureMission'))
    delete_url = request.build_absolute_uri(
        reverse('Web:DeleteChangeSignatureMission'))
    location = copy.deepcopy(location_init)
    location['IsChangeSignatureMissionPage'] = True
    location['IsMissionMenu'] = True
    context = {'location': location, 'data_url': data_url, 'delete_url': delete_url,
               'mission_status': TaskStatus}
    return render(request, 'pages/MissionManage/ChangeSignatureMissionPage.html', context)


@login_required
def getchangesignaturemission(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    generalSearch = request.POST.get(
        'query[generalChangeSignatureMissionSearch]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')
    status = request.POST.get('query[changesignaturemissionstatus]')
    starttime = request.POST.get('query[starttime]')    
    endtime = request.POST.get('query[endtime]')  

    owner_id_list = []
    owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)
    data_list = ChangeSignatureMission.objects.filter(Owner__id__in=owner_id_list)

    if generalSearch is not None and generalSearch != '':
        if str.isdigit(generalSearch):
            data_list = data_list.filter(MobilePhone__id=generalSearch)

    if status is not None and status != '':
        status_filter = Q()
        status_list = status[:-1].split(',')
        status_filter = status_filter | Q(Status__in=status_list)
        data_list = data_list.filter(status_filter)

    if starttime is not None and starttime != '' and endtime is not None and endtime != '':
        data_list = data_list.filter(
            CreateTime__range=(starttime, endtime))
    elif starttime is not None and starttime != '':
        data_list = data_list.filter(CreateTime__gte=starttime)
    elif endtime is not None and endtime != '':
        data_list = data_list.filter(CreateTime__lte=endtime)

    fields_list = WatchLiveMission._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')        

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values(
        'id', 'MobilePhone__id', 'Status', 'Describe', 'NewDescribe', 
        'CreateTime', 'StartTime',  'FailReason')
    data = []
    for i in range(len(data_result)):
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def delete_changesignaturemission_by_ids(request):
    ids = request.POST.get('ids')
    id_list = ids[:-1].split(',')
    if len(id_list) > 0:
        for i in range(len(id_list)):
            mission_id = id_list[i]
            mission = ChangeSignatureMission.objects.get(id=mission_id)
            mission.TikTokAccount.NewDescribe = ''
            mission.TikTokAccount.save()
            mission.delete()
    return HttpResponseRedirect(reverse('Web:ChangeSignatureMission'))


# end 修改签名任务 

# begin 设备分配
@login_required
def devicedeliver(request):    
    data_url = request.build_absolute_uri(
        reverse('Web:GetDeviceDeliver'))
    getdevicebyuserid_url = request.build_absolute_uri(
        reverse('Web:GetDeviceByUserID'))
    userdevicediliver_url = request.build_absolute_uri(
        reverse('Web:UserDeviceDeliver'))
    device_data_url = request.build_absolute_uri(reverse('Web:GetDevice'))
    devicemanage_url = request.build_absolute_uri(reverse('Web:DeviceManage'))
    getdevicenamebyids_url = request.build_absolute_uri(
        reverse('Web:GetDeviceNameByIDs'))
    owner_id_list = []
    if request.user.username == 'admin':
        owner_id_list = GetOwnerIDList(request.user.id, owner_id_list)        
    else:
        owner_id_list = GetOwnerIDUntilSuperuserList(request.user.id, owner_id_list)                
    classifications = MaintenanceNumberMissionKeywordClassification.objects.filter(Owner__in=owner_id_list).values('Name').distinct()
    groups = TikTokAccountGroup.objects.filter(Owner__in=owner_id_list).values('Name').distinct()
    owners = []      
    for i in range(len(owner_id_list)):
        owner_id = owner_id_list[i]
        user = User.objects.get(id=owner_id)
        owners.append(user)        
    location = copy.deepcopy(location_init)
    location['IsDeviceDeliverPage'] = True
    location['IsDeviceManageMenu'] = True
    context = {'location': location, 'data_url': data_url, 'device_data_url': device_data_url,
               'getdevicenamebyids_url': getdevicenamebyids_url, 'getdevicebyuserid_url': getdevicebyuserid_url,
               'userdevicediliver_url': userdevicediliver_url, 'devicemanage_url': devicemanage_url,
               'classifications': classifications, 'groups': groups,
               'owners': owners}
    return render(request, 'pages/DeviceManage/DeviceDeliver.html', context)


@login_required
def getdevicedeliver(request):
    page = request.POST.get('pagination[page]')
    pages = request.POST.get('pagination[pages]')
    perpage = request.POST.get('pagination[perpage]')
    field = request.POST.get('sort[field]')
    sort = request.POST.get('sort[sort]')

    owner_id_list = []
    owner_id_list = GetOwnerIDList(request.user.id, owner_id_list)
    user_filter = Q()
    user_filter = user_filter & Q(id__in=owner_id_list)
    user_filter = user_filter & Q(is_pass=1)
    user_filter = user_filter & (Q(is_superuser=1) | Q(is_mainuser=1))
    data_list = User.objects.filter(user_filter)

    fields_list = MissionPlanTemplate._meta.fields
    field_name_list = [f.name for f in fields_list]
    if field is not None and field != '' and field in field_name_list:
        if sort == 'desc':
            field = '-' + field
        data_list = data_list.order_by(field)
    else:
        data_list = data_list.order_by('id')         

    paginator = Paginator(data_list, perpage)
    context = {}
    meta = {
        'page': page,
        'pages': pages,
        'perpage': perpage,
        "total": paginator.count,
        "sort": sort,
        "field": field
    }

    try:
        page_result = paginator.page(page)
    except PageNotAnInteger:
        page_result = paginator.page(1)
    except EmptyPage:
        page_result = paginator.page(paginator.num_pages)

    data_result = page_result.object_list.values('id', 'username')
    data = []
    for i in range(len(data_result)):
        user_id = data_result[i]['id']
        mobile = MobilePhone.objects.filter(Owner=user_id).all()
        mobilephoneid = ''
        if (mobile.count() > 0):
            for j in range(mobile.count()):
                per = mobile[j]
                mobilephoneid = mobilephoneid + str(per.id) + ','
        data_result[i]['mobilephoneid'] = mobilephoneid[:-1]
        data.append(data_result[i])
    context['meta'] = meta
    context['data'] = data
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


@login_required
def userdevicedeliver(request):
    device_id = request.POST.get('deviceid')
    device_id_list = device_id.split(',')
    user_id = request.POST.get('id')
    user = User.objects.get(id=user_id)
    user.mobilephone_set.clear()
    for j in range(len(device_id_list)):
        id = device_id_list[j]
        if id is not None and id != '':
            device = MobilePhone.objects.get(id=id)
            if device is not None:
                device.Owner = user
                if device.TikTokAccount is not None:
                    device.TikTokAccount.Owner = user
                    if device.TikTokAccount.Group is not None:
                        device.TikTokAccount.Group = gettiktokaccountgroupid(device.TikTokAccount.Group, user)
                    if device.TikTokAccount.Classification is not None and device.TikTokAccount.Classification.count() > 0:
                        new_classification_list = gettiktokaccountclassificationid(device.TikTokAccount.Classification, user)
                        device.TikTokAccount.Classification.clear()
                        for i in range(len(new_classification_list)):
                            classfication = new_classification_list[i]
                            device.TikTokAccount.Classification.add(classfication)
                    device.TikTokAccount.save()
                device.save()
    null_device_list = list(MobilePhone.objects.filter(Owner=None).values_list('id', flat=True))
    if len(null_device_list) > 0:
        admin_user = User.objects.get(username='admin')
        for i in range(len(null_device_list)):
            null_id = null_device_list[i]
            device = MobilePhone.objects.get(id=null_id)
            if device is not None:
                device.Owner = admin_user
                if device.TikTokAccount is not None:
                    device.TikTokAccount.Owner = admin_user
                    if device.TikTokAccount.Group is not None:
                        device.TikTokAccount.Group = gettiktokaccountgroupid(device.TikTokAccount.Group, admin_user)
                    if device.TikTokAccount.Classification is not None and device.TikTokAccount.Classification.count() > 0:
                        new_classification_list = gettiktokaccountclassificationid(device.TikTokAccount.Classification, admin_user)
                        device.TikTokAccount.Classification.clear()
                        for i in range(len(new_classification_list)):
                            classfication = new_classification_list[i]
                            device.TikTokAccount.Classification.add(classfication)
                    device.TikTokAccount.save()
                device.save()
    return HttpResponse(reverse('Web:DeviceDeliver'))


@login_required
def getdevicebyuserid(request):
    userid = request.POST.get('id')
    mobile_list = MobilePhone.objects.filter(
        Owner__id=userid).values('id')
    mobile_ids = ''
    if len(mobile_list) > 0:
        for i in range(len(mobile_list)):
            mobile_ids = mobile_ids + str(mobile_list[i]['id']) + ','
    context = {
        'dataid': userid,
        'mobilephoneid': mobile_ids[:-1],
    }
    return HttpResponse(json.dumps(context, ensure_ascii=False, cls=Encoder),
                        content_type="application/json,charset=utf-8")


def gettiktokaccountgroupid(group, owner):
    name = group.Name
    group_list = TikTokAccountGroup.objects.filter(Name=name, Owner=owner)
    if group_list.count() > 0:
        tiktokAccountGroup = group_list.first()
    else:
        tiktokAccountGroup = TikTokAccountGroup()
        tiktokAccountGroup.Name = name
        tiktokAccountGroup.Owner = owner
        tiktokAccountGroup.save()
    return tiktokAccountGroup


def gettiktokaccountclassificationid(classification_list, owner):
    if classification_list.count() > 0:
        old_classification_list = list(classification_list.values_list('Name', flat=True))
        new_classification_list = []
        for i in range(len(old_classification_list)):
            name = old_classification_list[i]
            current_classification_list = MaintenanceNumberMissionKeywordClassification.objects.filter(Name=name, Owner=owner)
            if current_classification_list.count() > 0:
                current_classification = current_classification_list.first()
                new_classification_list.append(current_classification)
            else:
                maintenanceNumberMissionKeywordClassification = MaintenanceNumberMissionKeywordClassification()
                maintenanceNumberMissionKeywordClassification.Name = name
                maintenanceNumberMissionKeywordClassification.Owner = owner
                maintenanceNumberMissionKeywordClassification.save()
                new_classification_list.append(maintenanceNumberMissionKeywordClassification)
        return new_classification_list
# end 设备分配