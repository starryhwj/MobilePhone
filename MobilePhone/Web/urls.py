# -*- coding: utf-8 -*-

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # begin 公共接口
    path('Publish/DeviceDatatable', views.devicedatatable, name='DeviceDatatable'),
    path('Publish/OrderDatatable', views.orderdatatable, name='OrderDatatable'),    
    # end 公共接口
    # begin 账户总览
    path('', views.index, name='index'),
    # end 账户总览
    # begin 淘宝验证
    path('root.txt', views.taobaoverify, name='taobaoverify'),
    # end 淘宝验证
    # begin 我的商品
    path('MyCommodity/', views.mycommodity, name='MyCommodity'),
    path('MyCommodity/GetMyCommodity',
         views.getmycommodity, name='GetMyCommodity'),
    path('MyCommodity/DeleteMyCommodity',
         views.delete_mycommodity_by_ids, name='DeleteMyCommodity'),
    path('MyCommodity/CreateMyCommodity',
         views.createmycommodity, name='CreateMyCommodity'),
    path('MyCommodity/GetTaoBaoCommodity',
         views.gettaobaocommodity, name='GetTaoBaoCommodity'),
    path('MyCommodity/GetMyCommodityById',
         views.getmycommoditybyid, name='GetMyCommodityById'),
    path('MyCommodity/EditMyCommodity',
         views.editmycommodity, name='EditMyCommodity'),
    path('MyCommodity/UploadMutiVideo',
         views.uploamutidvideo, name='UploadMutiVideo'),      
    path('MyCommodity/RemoveUploadMutiVideo',
         views.removeuploamutidvideo, name='RemoveUploadMutiVideo'),           
    path('MyCommodity/CreateMutiVideo',
         views.createmutivideo, name='CreateMutiVideo'),      
    path('MyCommodity/CreateMutiMission',
         views.createmutimission, name='CreateMutiMission'),                    
    # end 我的商品
    # begin 商品类别
    path('CommodityCategory', views.commoditycategory, name='CommodityCategory'),
    path('CommodityCategory/GetCommodityCategory',
         views.getcommoditycategory, name='GetCommodityCategory'),
    path('CommodityCategory/DeleteCommodityCategory',
         views.delete_commoditycategory_by_ids, name='DeleteCommodityCategory'),
    path('CommodityCategory/CreateCommodityCategory',
         views.createcommoditycategory, name='CreateCommodityCategory'),
    path('CommodityCategory/GetCommodityCategoryByID',
         views.getcommoditycategorybyid, name='GetCommodityCategoryByID'),
    path('CommodityCategory/EditCommodityCategory',
         views.editcommoditycategory, name='EditCommodityCategory'),
    # end 商品类别
    # begin 设备管理
    path('DeviceManage/', views.devicemanage, name='DeviceManage'),
    path('DeviceManage/GetDevice', views.getdevice, name='GetDevice'),
    path('DeviceManage/GetDeviceNameByIDs',
         views.getdevicenamebyids, name='GetDeviceNameByIDs'),
    path('DeviceManage/GetDeviceRemark', views.getdeviceremark, name='GetDeviceRemark'),
    path('DeviceManage/EditDeviceRemark', views.editdeviceremark, name='EditDeviceRemark'),
    path('DeviceManage/EditDeviceEnable', views.editdeviceenable, name='EditDeviceEnable'),    
    # end 设备管理
    # begin 账号数据分析
    path('AccountDataAnalysis/', views.accountdataanalysis,
         name='AccountDataAnalysis'),
    path('AccountDataAnalysis/GetAccountDataAnalysis', views.getaccountdataanalysis, name='GetAccountDataAnalysis'),
    # end 账号数据分析
    # begin 账号分组
    path('AccountGroup', views.accountgroup, name='AccountGroup'),
    path('AccountGroup/GetAccountGroup',
         views.getaccountgroup, name='GetAccountGroup'),
    path('AccountGroup/DeleteAccountGroup',
         views.delete_accountgroup_by_ids, name='DeleteAccountGroup'),
    path('AccountGroup/CreateAccountGroup',
         views.createaccountgroup, name='CreateAccountGroup'),
    path('AccountGroup/GetAccountGroupByID',
         views.getaccountgroupbyid, name='GetAccountGroupByID'),
    path('AccountGroup/EditAccountGroup',
         views.editaccountgroup, name='EditAccountGroup'),
    # end 账号分组
    # begin 账号列表
    path('AccountList/', views.accountlist, name='AccountList'),
    path('AccountList/GetAccount', views.getaccount, name='GetAccount'),
    path('AccountList/GetAccountListByID',
         views.getaccountlistbyid, name='GetAccountListByID'),
    path('AccountList/EditAccountList', views.editaccountlist, name='EditAccountList'),
    path('AccountList/GetWorks', views.getworks, name='GetWorks'),
    # end 账号列表
    # begin 阿里妈妈配置
    path('ALIConfig/', views.aliconfig, name='ALIConfig'),
    path('ALIConfig/GetALIConfig', views.getaliconfig, name='GetALIConfig'),
    path('ALIConfig/DeleteALIConfig',
         views.delete_aliconfig_by_ids, name='DeleteALIConfig'),
    path('ALIConfig/CreateALIConfig',
         views.createaliconfig, name='CreateALIConfig'),
    path('ALIConfig/GetALIConfigByID',
         views.getaliconfigbyid, name='GetALIConfigByID'),
    path('ALIConfig/EditALIConfig', views.editaliconfig, name='EditALIConfig'),
    # end 阿里妈妈配置
    path('AlreadySendVideo/', views.alreadysendvideo, name='AlreadySendVideo'),
    # begin 商品数据分析
    path('CommodityDataAnalysis/', views.commoditydataanalysis,
         name='CommodityDataAnalysis'),
    path('CommodityDataAnalysis/GetCommodityDataAnalysis', views.getcommoditydataanalysis, name='GetCommodityDataAnalysis'),
    # end 商品数据分析
    path('CommodityMissionManage/', views.commoditymissionmanage,
         name='CommodityMissionManage'),
    path('CommoditySelection/', views.commodityselection,
         name='CommoditySelection'),
    # begin 我的视频
    path('MyVideo/', views.myvideo, name='MyVideo'),
    path('MyVideo/GetMyVideo', views.getmyvideo, name='GetMyVideo'),
    path('MyVideo/DeleteMyVideo', views.delete_myvideo_by_ids, name='DeleteMyVideo'),
    path('MyVideo/CreateMyVideo', views.createmyvideo, name='CreateMyVideo'),
    path('MyVideo/GetMyVideobyID', views.getmyvideobyid, name='GetMyVideobyID'),
    path('MyVideo/EditMyVideo', views.editmyvideo, name='EditMyVideo'),
    path('MyVideo/UploadMyVideo', views.uploadmyvideo, name='UploadMyVideo'),
    path('MyVideo/GetMyVideoURLByID',
         views.getmyvideourlbyid, name='GetMyVideoURLByID'),
    path('MyVideo/CreateVideoMission',
         views.createvideomission, name='CreateVideoMission'),
    path('MyVideo/RemoveUploadMyVideo', views.removeuploadmyvideo, name='RemoveUploadMyVideo'),         
    # end 我的视频
    path('OrderCollect/', views.ordercollect, name='OrderCollect'),
    # begin 视频数据分析
    path('WorksDataAnalysis/', views.worksdataanalysis, name='WorksDataAnalysis'),
    path('WorksDataAnalysis/GetWorksDataAnalysis', views.getworksdataanalysis, name='GetWorksDataAnalysis'),
    path('WorksDataAnalysis/GetHistoryData', views.gethistorydata, name='GetHistoryData'),
    # end 视频数据分析
    # begin 视频标签
    path('VideoLabel/', views.videolabel, name='VideoLabel'),
    path('VideoLabel/GetVideoLabel', views.getvideolabel, name='GetVideoLabel'),
    path('VideoLabel/DeleteVideoLabel',
         views.delete_videolabel_by_ids, name='DeleteVideoLabel'),
    path('VideoLabel/CreateVideoLabel',
         views.createvideolabel, name='CreateVideoLabel'),
    path('VideoLabel/EditVideoLabel', views.editvideolabel, name='EditVideoLabel'),
    path('VideoLabel/GetVideoLabelByID',
         views.getvideolabelbyid, name='GetVideoLabelByID'),
    # end 视频标签
    # begin 视频任务
    path('VideoMission/', views.videomission, name='VideoMission'),
    path('VideoMission/GetVideoMission',
         views.getvideomission, name='GetVideoMission'),
    path('VideoMission/DeleteVideoMission',
         views.delete_videomission_by_ids, name='DeleteVideoMission'),
    path('VideoMission/EditVideoMission',
         views.editvideomission, name='EditVideoMission'),
    path('VideoMission/GetVideoMissionByID',
         views.getvideomissionbyid, name='GetVideoMissionByID'),
    path('VideoMission/RelaunchVideoMission',
         views.relaunchvideomission, name='RelaunchVideoMission'),         
    # end 视频任务
    # begin 关注任务
    path('PublishFollowMission/', views.publishfollowmission,
         name='PublishFollowMission'),
    path('PublishFollowMission/GetFollowMission',
         views.getfollowmission, name='GetFollowMission'),
    path('PublishFollowMission/DeleteFollowMission',
         views.delete_followmission_by_ids, name='DeleteFollowMission'),
    path('PublishFollowMission/CreateFollowMission',
         views.createfollowmission, name='CreateFollowMission'),
    path('PublishFollowMission/EditFollowMission',
         views.editfollowmission, name='EditFollowMission'),
    path('PublishFollowMission/GetFollowMissionByID',
         views.getfollowmissionbyid, name='GetFollowMissionByID'),
    # end 关注任务
    # begin 养号任务
    path('PublishMaintenanceNumberMission/', views.publishmaintenancenumbermission,
         name='PublishMaintenanceNumberMission'),
    path('PublishMaintenanceNumberMission/GetMaintenanceNumberMission',
         views.getmaintenancenumbermission, name='GetMaintenanceNumberMission'),
    path('PublishMaintenanceNumberMission/DeleteMaintenanceNumberMission',
         views.delete_maintenancenumbermission_by_ids, name='DeleteMaintenanceNumberMission'),
    path('PublishMaintenanceNumberMission/CreateMaintenanceNumberMission',
         views.createmaintenancenumbermission, name='CreateMaintenanceNumberMission'),
    path('PublishMaintenanceNumberMission/EditMaintenanceNumberMission',
         views.editmaintenancenumbermission, name='EditMaintenanceNumberMission'),
    path('PublishMaintenanceNumberMission/GetMaintenanceNumberMissionByID',
         views.getmaintenancenumbermissionbyid, name='GetMaintenanceNumberMissionByID'),
    # end 养号任务
    # begin 养号任务关键字
    path('PublishMaintenanceNumberMissionKeyword/', views.publishmaintenancenumbermissionkeyword,
         name='PublishMaintenanceNumberMissionKeyword'),
    path('PublishMaintenanceNumberMissionKeyword/GetMaintenanceNumberMissionKeyword',
         views.getmaintenancenumbermissionkeyword, name='GetMaintenanceNumberMissionKeyword'),
    path('PublishMaintenanceNumberMissionKeyword/DeleteMaintenanceNumberMissionKeyword',
         views.delete_maintenancenumbermissionkeyword_by_ids, name='DeleteMaintenanceNumberMissionKeyword'),
    path('PublishMaintenanceNumberMissionKeyword/CreateMaintenanceNumberMissionKeyword',
         views.createmaintenancenumbermissionkeyword, name='CreateMaintenanceNumberMissionKeyword'),
    path('PublishMaintenanceNumberMissionKeyword/EditMaintenanceNumberMissionKeyword',
         views.editmaintenancenumbermissionkeyword, name='EditMaintenanceNumberMissionKeyword'),
    path('PublishMaintenanceNumberMissionKeyword/GetMaintenanceNumberMissionKeywordByID',
         views.getmaintenancenumbermissionkeywordbyid, name='GetMaintenanceNumberMissionKeywordByID'),
     path('PublishMaintenanceNumberMissionKeyword/GetMaintenanceNumberMissionKeywordNamesByID',
         views.getmaintenancenumbermissionkeywordnamesbyid, name='GetMaintenanceNumberMissionKeywordNamesByID'),
    # end 养号任务关键字
    # begin 养号任务关键字类型
    path('PublishMaintenanceNumberMissionKeywordClassification/', views.publishmaintenancenumbermissionkeywordclassification,
         name='PublishMaintenanceNumberMissionKeywordClassification'),
    path('PublishMaintenanceNumberMissionKeywordClassification/GetMaintenanceNumberMissionKeywordClassification',
         views.getmaintenancenumbermissionkeywordclassification, name='GetMaintenanceNumberMissionKeywordClassification'),
    path('PublishMaintenanceNumberMissionKeywordClassification/DeleteMaintenanceNumberMissionKeywordClassification',
         views.delete_maintenancenumbermissionkeywordclassification_by_ids, name='DeleteMaintenanceNumberMissionKeywordClassification'),
    path('PublishMaintenanceNumberMissionKeywordClassification/CreateMaintenanceNumberMissionKeywordClassification',
         views.createmaintenancenumbermissionkeywordclassification, name='CreateMaintenanceNumberMissionKeywordClassification'),
    path('PublishMaintenanceNumberMissionKeywordClassification/EditMaintenanceNumberMissionKeywordClassification',
         views.editmaintenancenumbermissionkeywordclassification, name='EditMaintenanceNumberMissionKeywordClassification'),
    path('PublishMaintenanceNumberMissionKeywordClassification/GetMaintenanceNumberMissionKeywordClassificationByID',
         views.getmaintenancenumbermissionkeywordclassificationbyid, name='GetMaintenanceNumberMissionKeywordClassificationByID'),
    # end 养号任务关键字类型
    # begin 互刷任务
    path('PublishMutualBrushMission/', views.publishmutualbrushmission,
         name='PublishMutualBrushMission'),
    path('PublishMutualBrushMission/GetMutualBrushMission',
         views.getmutualbrushmission, name='GetMutualBrushMission'),
    path('PublishMutualBrushMission/DeleteMutualBrushMission',
         views.delete_mutualbrushmission_by_ids, name='DeleteMutualBrushMission'),
    path('PublishMutualBrushMission/CreateMutualBrushMission',
         views.createmutualbrushmission, name='CreateMutualBrushMission'),
    path('PublishMutualBrushMission/EditMutualBrushMission',
         views.editmutualbrushmission, name='EditMutualBrushMission'),
    path('PublishMutualBrushMission/GetMutualBrushMissionByID',
         views.getmutualbrushmissionbyid, name='GetMutualBrushMissionByID'),
    # end 互刷任务
    # begin 刷粉任务
    path('PublishScanMission/', views.publishscanmission,
         name='PublishScanMission'),
    path('PublishScanMission/GetScanMission',
         views.getscanmission, name='GetScanMission'),
    path('PublishScanMission/DeleteScanMission',
         views.delete_scanmission_by_ids, name='DeleteScanMission'),
    path('PublishScanMission/CreateScanMission',
         views.createscanmission, name='CreateScanMission'),
    path('PublishScanMission/EditScanMission',
         views.editscanmission, name='EditScanMission'),
    path('PublishScanMission/GetScanMissionByID',
         views.getscanmissionbyid, name='GetScanMissionByID'),
    # end 刷粉任务
    # begin 评论库
    path('CommentLibrary/', views.commentlibrary, name='CommentLibrary'),
    path('CommentLibrary/GetCommentLibrary', views.getcommentlibrary, name='GetCommentLibrary'),
    path('CommentLibrary/DeleteCommentLibrary',
         views.delete_commentlibrary_by_ids, name='DeleteCommentLibrary'),
    path('CommentLibrary/CreateCommentLibrary',
         views.createcommentlibrary, name='CreateCommentLibrary'),
    path('CommentLibrary/GetCommentLibraryByID',
         views.getcommentlibrarybyid, name='GetCommentLibraryByID'),
    path('CommentLibrary/EditCommentLibrary', views.editcommentlibrary, name='EditCommentLibrary'),
    # end 评论库
    # begin 代理审核
    path('AgentVerify/', views.agentverify, name='AgentVerify'),
    path('AgentVerify/GetAgentVerify', views.getagentverify, name='GetAgentVerify'),
    path('AgentVerify/PassAgentVerifyASSuperUser', views.passagentverifyassuperuser, name='PassAgentVerifyASSuperUser'),
    path('AgentVerify/PassAgentVerifyASMainUser', views.passagentverifyasmainuser, name='PassAgentVerifyASMainUser'),
    path('AgentVerify/PassAgentVerifyASAgent', views.passagentverifyasagent, name='PassAgentVerifyASAgent'),
    path('AgentVerify/NotPassAgentVerify', views.notpassagentverify, name='NotPassAgentVerify'),
    # end 代理审核
    # begin 代理列表
    path('AgentList/', views.agentlist, name='AgentList'),
    path('AgentList/GetAgentList',
         views.getagentlist, name='GetAgentList'),
    path('AgentList/EditAgentList',
         views.editagentlist, name='EditAgentList'),
    path('AgentList/GetAgentListByID',
         views.getagentlistbyid, name='GetAgentListByID'),
    path('AgentList/GetPromotionByAgentID',
         views.getpromotionbyagentid, name='GetPromotionByAgentID'),
    path('AgentList/ResetPassword',
         views.resetpassword, name='ResetPassword'),         
    # end 代理列表
    # begin 代理账号信息
    path('AgentDetail/', views.agentdetail, name='AgentDetail'),
    path('AgentDetail/GetAgentDetail',
         views.getagentdetail, name='GetAgentDetail'),
    path('AgentDetail/EditAgentDetail',
         views.editagentdetail, name='EditAgentDetail'),
    path('AgentDetail/GetAgentDetailByID',
         views.getagentdetailbyid, name='GetAgentDetailByID'),    
    # end 代理账号信息
    # begin 订单管理
    path('Order/', views.order, name='Order'),
    path('Order/GetOrder', views.getorder, name='GetOrder'),
    # end 订单管理
    # begin 提现管理
    path('CashManage/', views.cashmanage, name='CashManage'),
    path('CashManage/CreateAgentApplyForWithdraw', views.createagentapplyforwithdraw, name='CreateAgentApplyForWithdraw'), 
    path('CashManage/GetAgentApplyForWithdraw', views.getagentapplyforwithdraw, name='GetAgentApplyForWithdraw'),
    path('CashManage/PassAgentApplyForWithdraw', views.passagentapplyforwithdraw, name='PassAgentApplyForWithdraw'),
    path('CashManage/NotPassAgentApplyForWithdraw', views.notpassagentapplyforwithdraw, name='NotPassAgentApplyForWithdraw'),
    # end 提现管理
    # begin 任务模板
    path('MissionPlanTemplate/', views.missionplantemplate, name='MissionPlanTemplate'),
    path('MissionPlanTemplate/GetMissionPlanTemplate', views.getmissionplantemplate, name='GetMissionPlanTemplate'),
    path('MissionPlanTemplate/DeleteMissionPlanTemplate',
         views.delete_missionplantemplate_by_ids, name='DeleteMissionPlanTemplate'),
    path('MissionPlanTemplate/CreateMissionPlanTemplate',
         views.createmissionplantemplate, name='CreateMissionPlanTemplate'),
    path('MissionPlanTemplate/GetDeviceByTemplateID', views.getdevicebytemplateid, name='GetDeviceByTemplateID'),
    path('MissionPlanTemplate/DeliverDevice', views.deliverdevice, name='DeliverDevice'),
    # end 任务模板
    # begin 编辑任务模板
    path('EditMissionPlanTemplate/', views.editmissionplantemplate, name='EditMissionPlanTemplate'),
    path('EditMissionPlanTemplate/<int:missionplantemplate_id>/', views.editmissionplantemplatebyid, name='EditMissionPlanTemplateByID'),
    path('EditMissionPlanTemplate/DeleteEvent',
         views.delete_event_by_ids, name='DeleteEvent'),
    path('EditMissionPlanTemplate/CreateEvent',
         views.createevent, name='CreateEvent'),
    path('EditMissionPlanTemplate/GetEventsByTemplateID',
         views.geteventsbytemplateid, name='GetEventsByTemplateID'),
    path('EditMissionPlanTemplate/GetEventByID',
         views.geteventbyid, name='GetEventByID'),
    path('EditMissionPlanTemplate/EditEvent', views.editevent, name='EditEvent'),
    path('EditMissionPlanTemplate/EditEventDetail', views.editeventdetail, name='EditEventDetail'),
    # end 编辑任务模板
    # begin 第三方API授权
    path('TaoBaoReOuth/ReOuth', views.taobaoreouth, name='ReOuth'),
    # end 第三方API授权
    # begin 全部任务
    path('AllMissions/', views.allmissions, name='AllMissions'),    
    path('AllMissions/GetAllMissions', views.getallmissions, name='GetAllMissions'),  
    path('AllMissions/DeleteAllMissions', views.delete_allmission_by_ids, name='DeleteAllMissions'),           
    # end 全部任务
    # begin 挖宝任务
    path('TreasureMission/', views.treasuremission,
         name='TreasureMission'),
    path('TreasureMission/GetTreasureMission',
         views.gettreasuremission, name='GetTreasureMission'),
    path('TreasureMission/DeleteTreasureMission',
         views.delete_treasuremission_by_ids, name='DeleteTreasureMission'),
    path('TreasureMission/CreateTreasureMission',
         views.createtreasuremission, name='CreateTreasureMission'),
    path('TreasureMission/EditTreasureMission',
         views.edittreasuremission, name='EditTreasureMission'),
    path('TreasureMission/GetTreasureMissionByID',
         views.gettreasuremissionbyid, name='GetTreasureMissionByID'),
    # end 挖宝任务    
    # begin 代理我的收益
     path('AgentIncome/', views.agentincome,
         name='AgentIncome'),
    # end 代理我的收益
    # begin 代理余额提现
     path('AgentWithdraw/', views.agentwithdraw,
         name='AgentWithdraw'),
     path('AgentWithdraw/GetAgentWithdrawList', views.getagentwithdrawlist,
         name='GetAgentWithdrawList'),         
    # end 代理余额提现
    # begin 代理账号数据
     path('AgentAccountData/', views.agentaccountdata,
         name='AgentAccountData'),   
     path('AgentAccountData/GetAgentAccountData', views.getagentaccountdata,
         name='GetAgentAccountData'),            
    # end 代理账号数据
    # begin 观看直播任务
    path('WatchLiveMission/', views.watchlivemission,
         name='WatchLiveMission'),
    path('WatchLiveMission/GetWatchLiveMission',
         views.getwatchlivemission, name='GetWatchLiveMission'),
    path('WatchLiveMission/DeleteWatchLiveMission',
         views.delete_watchlivemission_by_ids, name='DeleteWatchLiveMission'),
    path('WatchLiveMission/CreateWatchLiveMission',
         views.createwatchlivemission, name='CreateWatchLiveMission'),
    path('WatchLiveMission/EditWatchLiveMission',
         views.editwatchlivemission, name='EditWatchLiveMission'),
    path('WatchLiveMission/GetWatchLiveMissionByID',
         views.getwatchlivemissionbyid, name='GetWatchLiveMissionByID'),
    # end 观看直播任务  
    # begin 签名管理
    path('SignatureManage/', views.signaturemanage,
         name='SignatureManage'),    
    path('SignatureManage/GetSignatureManage',
         views.getsignaturemanage, name='GetSignatureManage'),    
    path('SignatureManage/GetSignatureManageByID',
         views.getsignaturemanagebyid, name='GetSignatureManageByID'),   
    path('SignatureManage/CreateChangeSignatureMission',
         views.createchangesignaturemission, name='CreateChangeSignatureMission'),     
    path('SignatureManage/MutiCreateChangeSignatureMission',
         views.muticreatechangesignaturemission, name='MutiCreateChangeSignatureMission'),                          
    # end 签名管理  
    # begin 修改签名任务
    path('ChangeSignatureMission/', views.changesignaturemission,
         name='ChangeSignatureMission'),      
    path('ChangeSignatureMission/GetChangeSignatureMission',
         views.getchangesignaturemission, name='GetChangeSignatureMission'),
    path('ChangeSignatureMission/DeleteChangeSignatureMission',
         views.delete_changesignaturemission_by_ids, name='DeleteChangeSignatureMission'),         
    # end 修改签名任务
    # begin 设备分配
    path('DeviceDeliver/', views.devicedeliver,
         name='DeviceDeliver'),  
    path('DeviceDeliver/GetDeviceDeliver', views.getdevicedeliver, name='GetDeviceDeliver'),
    path('DeviceDeliver/UserDeviceDeliver', views.userdevicedeliver, name='UserDeviceDeliver'),     
    path('DeviceDeliver/GetDeviceByUserID', views.getdevicebyuserid, name='GetDeviceByUserID'),            
    # end 设备分配
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
