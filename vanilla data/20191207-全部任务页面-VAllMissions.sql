USE [PhoneAutoRunManagementPlatform]
GO

/****** Object:  View [dbo].[VAllMissions]    Script Date: 12/07/2019 17:40:30 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[VAllMissions]
AS
SELECT     '视频任务' AS MissionName, dbo.Web_videomission.id, dbo.Web_videomission.[Status], dbo.Web_videomission.[CreateTime], dbo.Web_videomission.[StartTime], NULL 
                      AS [EndTime], dbo.Web_videomission.[FailReason], dbo.Web_videomission.MobilePhone_id, dbo.Web_tiktokaccount.NickName
FROM         dbo.Web_videomission LEFT JOIN
                      dbo.Web_mobilephone ON dbo.[Web_videomission].MobilePhone_id = dbo.Web_mobilephone.id LEFT JOIN
                      dbo.Web_tiktokaccount ON dbo.Web_mobilephone.TikTokAccount_id = dbo.Web_tiktokaccount.id
UNION
SELECT     '互刷任务' AS MissionName, dbo.Web_mutualbrushmission.id, dbo.Web_mutualbrushmission.[Status], dbo.Web_mutualbrushmission.[CreateTime], 
                      dbo.Web_mutualbrushmission.[StartTime], NULL AS [EndTime], dbo.Web_mutualbrushmission.[FailReason], dbo.Web_mutualbrushmission.MobilePhone_id, 
                      dbo.Web_tiktokaccount.NickName
FROM         dbo.Web_mutualbrushmission LEFT JOIN
                      dbo.Web_mobilephone ON dbo.Web_mutualbrushmission.MobilePhone_id = dbo.Web_mobilephone.id LEFT JOIN
                      dbo.Web_tiktokaccount ON dbo.Web_mobilephone.TikTokAccount_id = dbo.Web_tiktokaccount.id
UNION
SELECT     '养号任务' AS MissionName, dbo.Web_maintenancenumbermission.id, dbo.Web_maintenancenumbermission.[Status], dbo.Web_maintenancenumbermission.[CreateTime], 
                      dbo.Web_maintenancenumbermission.[StartTime], dbo.Web_maintenancenumbermission.[EndTime], dbo.Web_maintenancenumbermission.[FailReason], 
                      dbo.Web_maintenancenumbermission.MobilePhone_id, dbo.Web_tiktokaccount.NickName
FROM         dbo.Web_maintenancenumbermission LEFT JOIN
                      dbo.Web_mobilephone ON dbo.Web_maintenancenumbermission.MobilePhone_id = dbo.Web_mobilephone.id LEFT JOIN
                      dbo.Web_tiktokaccount ON dbo.Web_mobilephone.TikTokAccount_id = dbo.Web_tiktokaccount.id
UNION
SELECT     '刷粉任务' AS MissionName, dbo.Web_scanmission.id, dbo.Web_scanmission.[Status], dbo.Web_scanmission.[CreateTime], dbo.Web_scanmission.[StartTime], 
                      dbo.Web_scanmission.[EndTime], dbo.Web_scanmission.[FailReason], dbo.Web_scanmission.MobilePhone_id, dbo.Web_tiktokaccount.NickName
FROM         dbo.Web_scanmission LEFT JOIN
                      dbo.Web_mobilephone ON dbo.Web_scanmission.MobilePhone_id = dbo.Web_mobilephone.id LEFT JOIN
                      dbo.Web_tiktokaccount ON dbo.Web_mobilephone.TikTokAccount_id = dbo.Web_tiktokaccount.id
UNION
SELECT     '关注任务' AS MissionName, dbo.Web_followmission.id, dbo.Web_followmission.[Status], dbo.Web_followmission.[CreateTime], dbo.Web_followmission.[StartTime], 
                      dbo.Web_followmission.[EndTime], dbo.Web_followmission.[FailReason], dbo.Web_followmission.MobilePhone_id, dbo.Web_tiktokaccount.NickName
FROM         dbo.Web_followmission LEFT JOIN
                      dbo.Web_mobilephone ON dbo.Web_followmission.MobilePhone_id = dbo.Web_mobilephone.id LEFT JOIN
                      dbo.Web_tiktokaccount ON dbo.Web_mobilephone.TikTokAccount_id = dbo.Web_tiktokaccount.id

GO

EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPane1', @value=N'[0E232FF0-B466-11cf-A24F-00AA00A3EFFF, 1.00]
Begin DesignProperties = 
   Begin PaneConfigurations = 
      Begin PaneConfiguration = 0
         NumPanes = 4
         Configuration = "(H (1[40] 4[20] 2[20] 3) )"
      End
      Begin PaneConfiguration = 1
         NumPanes = 3
         Configuration = "(H (1 [50] 4 [25] 3))"
      End
      Begin PaneConfiguration = 2
         NumPanes = 3
         Configuration = "(H (1 [50] 2 [25] 3))"
      End
      Begin PaneConfiguration = 3
         NumPanes = 3
         Configuration = "(H (4 [30] 2 [40] 3))"
      End
      Begin PaneConfiguration = 4
         NumPanes = 2
         Configuration = "(H (1 [56] 3))"
      End
      Begin PaneConfiguration = 5
         NumPanes = 2
         Configuration = "(H (2 [66] 3))"
      End
      Begin PaneConfiguration = 6
         NumPanes = 2
         Configuration = "(H (4 [50] 3))"
      End
      Begin PaneConfiguration = 7
         NumPanes = 1
         Configuration = "(V (3))"
      End
      Begin PaneConfiguration = 8
         NumPanes = 3
         Configuration = "(H (1[56] 4[18] 2) )"
      End
      Begin PaneConfiguration = 9
         NumPanes = 2
         Configuration = "(H (1 [75] 4))"
      End
      Begin PaneConfiguration = 10
         NumPanes = 2
         Configuration = "(H (1[66] 2) )"
      End
      Begin PaneConfiguration = 11
         NumPanes = 2
         Configuration = "(H (4 [60] 2))"
      End
      Begin PaneConfiguration = 12
         NumPanes = 1
         Configuration = "(H (1) )"
      End
      Begin PaneConfiguration = 13
         NumPanes = 1
         Configuration = "(V (4))"
      End
      Begin PaneConfiguration = 14
         NumPanes = 1
         Configuration = "(V (2))"
      End
      ActivePaneConfig = 0
   End
   Begin DiagramPane = 
      Begin Origin = 
         Top = 0
         Left = 0
      End
      Begin Tables = 
      End
   End
   Begin SQLPane = 
   End
   Begin DataPane = 
      Begin ParameterDefaults = ""
      End
   End
   Begin CriteriaPane = 
      Begin ColumnWidths = 11
         Column = 1440
         Alias = 900
         Table = 1170
         Output = 720
         Append = 1400
         NewValue = 1170
         SortType = 1350
         SortOrder = 1410
         GroupBy = 1350
         Filter = 1350
         Or = 1350
         Or = 1350
         Or = 1350
      End
   End
End
' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'VAllMissions'
GO

EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPaneCount', @value=1 , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'VAllMissions'
GO


