CREATE VIEW [dbo].[VAllMissions]
AS
SELECT     '视频任务' AS MissionName, dbo.Web_videomission.id, dbo.Web_videomission.[Status], dbo.Web_videomission.[CreateTime], dbo.Web_videomission.[StartTime], NULL AS [EndTime], 
                      dbo.Web_videomission.[FailReason], dbo.Web_videomission.MobilePhone_id, dbo.Web_tiktokaccount.NickName, dbo.Web_videomission.[Owner_id]
FROM         dbo.Web_videomission LEFT JOIN
                      dbo.Web_mobilephone ON dbo.[Web_videomission].MobilePhone_id = dbo.Web_mobilephone.id LEFT JOIN
                      dbo.Web_tiktokaccount ON dbo.Web_mobilephone.TikTokAccount_id = dbo.Web_tiktokaccount.id
UNION
SELECT     '互刷任务' AS MissionName, dbo.Web_mutualbrushmission.id, dbo.Web_mutualbrushmission.[Status], dbo.Web_mutualbrushmission.[CreateTime], 
                      dbo.Web_mutualbrushmission.[StartTime], NULL AS [EndTime], dbo.Web_mutualbrushmission.[FailReason], dbo.Web_mutualbrushmission.MobilePhone_id, 
                      dbo.Web_tiktokaccount.NickName, dbo.Web_mutualbrushmission.[Owner_id]
FROM         dbo.Web_mutualbrushmission LEFT JOIN
                      dbo.Web_mobilephone ON dbo.Web_mutualbrushmission.MobilePhone_id = dbo.Web_mobilephone.id LEFT JOIN
                      dbo.Web_tiktokaccount ON dbo.Web_mobilephone.TikTokAccount_id = dbo.Web_tiktokaccount.id
UNION
SELECT     '养号任务' AS MissionName, dbo.Web_maintenancenumbermission.id, dbo.Web_maintenancenumbermission.[Status], dbo.Web_maintenancenumbermission.[CreateTime], 
                      dbo.Web_maintenancenumbermission.[StartTime], dbo.Web_maintenancenumbermission.[EndTime], dbo.Web_maintenancenumbermission.[FailReason], 
                      dbo.Web_maintenancenumbermission.MobilePhone_id, dbo.Web_tiktokaccount.NickName, dbo.Web_maintenancenumbermission.[Owner_id]
FROM         dbo.Web_maintenancenumbermission LEFT JOIN
                      dbo.Web_mobilephone ON dbo.Web_maintenancenumbermission.MobilePhone_id = dbo.Web_mobilephone.id LEFT JOIN
                      dbo.Web_tiktokaccount ON dbo.Web_mobilephone.TikTokAccount_id = dbo.Web_tiktokaccount.id
UNION
SELECT     '刷粉任务' AS MissionName, dbo.Web_scanmission.id, dbo.Web_scanmission.[Status], dbo.Web_scanmission.[CreateTime], dbo.Web_scanmission.[StartTime], dbo.Web_scanmission.[EndTime], 
                      dbo.Web_scanmission.[FailReason], dbo.Web_scanmission.MobilePhone_id, dbo.Web_tiktokaccount.NickName, dbo.Web_scanmission.[Owner_id]
FROM         dbo.Web_scanmission LEFT JOIN
                      dbo.Web_mobilephone ON dbo.Web_scanmission.MobilePhone_id = dbo.Web_mobilephone.id LEFT JOIN
                      dbo.Web_tiktokaccount ON dbo.Web_mobilephone.TikTokAccount_id = dbo.Web_tiktokaccount.id
UNION
SELECT     '关注任务' AS MissionName, dbo.Web_followmission.id, dbo.Web_followmission.[Status], dbo.Web_followmission.[CreateTime], dbo.Web_followmission.[StartTime], 
                      dbo.Web_followmission.[EndTime], dbo.Web_followmission.[FailReason], dbo.Web_followmission.MobilePhone_id, dbo.Web_tiktokaccount.NickName,
                      dbo.Web_followmission.[Owner_id]
FROM         dbo.Web_followmission LEFT JOIN
                      dbo.Web_mobilephone ON dbo.Web_followmission.MobilePhone_id = dbo.Web_mobilephone.id LEFT JOIN
                      dbo.Web_tiktokaccount ON dbo.Web_mobilephone.TikTokAccount_id = dbo.Web_tiktokaccount.id
UNION
SELECT     '刷宝任务' AS MissionName, dbo.Web_treasuremission.id, dbo.Web_treasuremission.[Status], dbo.Web_treasuremission.[CreateTime], dbo.Web_treasuremission.[StartTime], 
                      dbo.Web_treasuremission.[EndTime], dbo.Web_treasuremission.[FailReason], dbo.Web_treasuremission.MobilePhone_id, dbo.Web_tiktokaccount.NickName,
                      dbo.Web_treasuremission.[Owner_id]
FROM         dbo.Web_treasuremission LEFT JOIN
                      dbo.Web_mobilephone ON dbo.Web_treasuremission.MobilePhone_id = dbo.Web_mobilephone.id LEFT JOIN
                      dbo.Web_tiktokaccount ON dbo.Web_mobilephone.TikTokAccount_id = dbo.Web_tiktokaccount.id
UNION
SELECT     '观看直播任务' AS MissionName, dbo.[Web_watchlivemission].id, dbo.[Web_watchlivemission].[Status], dbo.[Web_watchlivemission].[CreateTime], dbo.[Web_watchlivemission].[StartTime], 
                      dbo.[Web_watchlivemission].[EndTime], dbo.[Web_watchlivemission].[FailReason], dbo.[Web_watchlivemission].MobilePhone_id, dbo.Web_tiktokaccount.NickName,
                      dbo.[Web_watchlivemission].[Owner_id]
FROM         dbo.[Web_watchlivemission] LEFT JOIN
                      dbo.Web_mobilephone ON dbo.[Web_watchlivemission].MobilePhone_id = dbo.Web_mobilephone.id LEFT JOIN
                      dbo.Web_tiktokaccount ON dbo.Web_mobilephone.TikTokAccount_id = dbo.Web_tiktokaccount.id
UNION
SELECT     '修改签名任务' AS MissionName, dbo.[Web_changesignaturemission].id, dbo.[Web_changesignaturemission].[Status], dbo.[Web_changesignaturemission].[CreateTime], 
                      dbo.[Web_changesignaturemission].[StartTime], NULL AS [EndTime], dbo.[Web_changesignaturemission].[FailReason], dbo.[Web_changesignaturemission].MobilePhone_id, 
                      dbo.Web_tiktokaccount.NickName, dbo.[Web_changesignaturemission].[Owner_id]
FROM         dbo.[Web_changesignaturemission] LEFT JOIN
                      dbo.Web_mobilephone ON dbo.[Web_changesignaturemission].MobilePhone_id = dbo.Web_mobilephone.id LEFT JOIN
                      dbo.Web_tiktokaccount ON dbo.Web_mobilephone.TikTokAccount_id = dbo.Web_tiktokaccount.id

