USE [PhoneAutoRunManagementPlatform]
GO

/****** Object:  StoredProcedure [dbo].[AutoCreateMissions]    Script Date: 11/24/2019 11:45:24 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		何文晋
-- Create date: 2019.11.24
-- Description:	自动根据任务计划模板生成任务
-- =============================================
CREATE PROCEDURE [dbo].[AutoCreateMissions]
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;
	
	-- 养号任务
	Insert Into [Web_maintenancenumbermission]([Status]
	  ,[MobilePhone_id]
      ,[Owner_id]
      ,[CreateTime]
      ,[UpdateTime]
      ,[EndTime]
      ,[Priority]
      ,[StartTime]) 
	SELECT 
	0 AS [Status], 
	C.id AS MobilePhone_id, 
	B.Owner_id AS Owner_id, 
	GETDATE() AS CreateTime, 
	GETDATE() AS UpdateTime, 
	CONVERT(varchar(11),GETDATE(),120) + ' ' + CONVERT(varchar(12),A.EndTime,108) AS EndTime,
	1 AS Priority , 
	CONVERT(varchar(11),GETDATE(),120) + ' ' + CONVERT(varchar(12),A.StartTime,108) AS StartTime
	From [Web_maintenancenumbermissionplan] AS A
	INNER JOIN [Web_missionplantemplate] AS B ON A.MissionPlanTemplate_id = B.id
	INNER JOIN [Web_mobilephone] AS C ON C.MissionPlanTemplate_id = B.id
	
	-- 刷粉任务
	Insert Into [Web_scanmission]([Status]
      ,[PeopleLimit]
      ,[Interval]
      ,[MobilePhone_id]
      ,[Owner_id]
      ,[CreateTime]
      ,[UpdateTime]
      ,[Priority]
      ,[StartTime]
      ,[EndTime]
      ,[CommentTextID]
      ,[FanSexIsFemale]
      ,[FanSexIsMale]
      ,[FanSexIsNone]) 
	SELECT 
	0 AS [Status],
	A.PeopleLimit AS PeopleLimit,
	A.Interval AS Interval,
	C.id AS MobilePhone_id, 
	B.Owner_id AS Owner_id, 
	GETDATE() AS CreateTime, 
	GETDATE() AS UpdateTime,
	1 AS Priority , 
	CONVERT(varchar(11),GETDATE(),120) + ' ' + CONVERT(varchar(12),A.StartTime,108) AS StartTime,
	CONVERT(varchar(11),GETDATE(),120) + ' ' + CONVERT(varchar(12),A.EndTime,108) AS EndTime, 
	A.CommentTextID AS CommentTextID,
	A.FanSexIsFemale AS FanSexIsFemale,
	A.FanSexIsMale AS FanSexIsMale,
	A.FanSexIsNone AS FanSexIsNone
	From [Web_scanmissionplan] AS A
	INNER JOIN [Web_missionplantemplate] AS B ON A.MissionPlanTemplate_id = B.id
	INNER JOIN [Web_mobilephone] AS C ON C.MissionPlanTemplate_id = B.id
	
	--关注任务
	Insert Into [Web_followmission]([Status]
      ,[PeopleLimit]
      ,[MobilePhone_id]
      ,[Owner_id]
      ,[CreateTime]
      ,[UpdateTime]
      ,[Priority]
      ,[StartTime]
      ,[EndTime]
      ,[FanSexIsFemale]
      ,[FanSexIsMale]
      ,[FanSexIsNone]) 
	SELECT 
	0 AS [Status],
	A.PeopleLimit AS PeopleLimit,
	C.id AS MobilePhone_id, 
	B.Owner_id AS Owner_id, 
	GETDATE() AS CreateTime, 
	GETDATE() AS UpdateTime,
	1 AS Priority , 
	CONVERT(varchar(11),GETDATE(),120) + ' ' + CONVERT(varchar(12),A.StartTime,108) AS StartTime,
	CONVERT(varchar(11),GETDATE(),120) + ' ' + CONVERT(varchar(12),A.EndTime,108) AS EndTime, 
	A.FanSexIsFemale AS FanSexIsFemale,
	A.FanSexIsMale AS FanSexIsMale,
	A.FanSexIsNone AS FanSexIsNone
	From [Web_followmissionplan] AS A
	INNER JOIN [Web_missionplantemplate] AS B ON A.MissionPlanTemplate_id = B.id
	INNER JOIN [Web_mobilephone] AS C ON C.MissionPlanTemplate_id = B.id
END

GO


