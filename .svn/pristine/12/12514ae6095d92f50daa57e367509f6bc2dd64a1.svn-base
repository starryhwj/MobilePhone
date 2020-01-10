USE [PhoneAutoRunManagementPlatform]
GO

/****** Object:  StoredProcedure [dbo].[CalcAgentMonthTruelyIncome]    Script Date: 12/07/2019 10:57:39 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		何文晋
-- Create date: 2019.12.6
-- Description:	统计代理每个月的实际收入
-- =============================================
CREATE PROCEDURE [dbo].[CalcAgentMonthTruelyIncome]
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Insert statements for procedure here
    DECLARE @StartDate nvarchar(100)
	DECLARE	@EndDate nvarchar(100)
	SET @EndDate = CONVERT(CHAR(10),GETDATE(),120)
	SET @StartDate = CONVERT(CHAR(10),DATEADD(month,-1,DATEADD(dd,-DAY(GETDATE())+26,GETDATE())),120)
	
	DECLARE agent_id_cursor cursor scroll
	FOR SELECT id FROM [Web_agent]
	
	OPEN agent_id_cursor
	
	DECLARE @AgentId int
	FETCH FIRST FROM agent_id_cursor INTO @AgentId
	WHILE @@fetch_status=0  --提取成功，进行下一条数据的提取操作
	BEGIN
		-- 获取数据
		DECLARE @Money decimal(18,2)
		DECLARE @OrderCount int
		
		CREATE TABLE [dbo].[Temp](
			ReturnMoney decimal(18,2),
			ReturnOrderCount int
		)
		INSERT [Temp] EXEC CalcAgentIncome @AgentId,@StartDate,@EndDate,1,'Total'
		
		SELECT @Money=ReturnMoney, @OrderCount=ReturnOrderCount FROM [Temp]
		
		DROP TABLE [Temp] 
		
		-- 插入表格
		INSERT INTO [Web_agentmonthrealityincome]
		VALUES(@EndDate, @Money, @OrderCount, @AgentId)
		
		-- 更新账户余额
		DECLARE @USERID int
		SELECT @USERID=[Subscriber_id] FROM [Web_agent] WHERE id=@AgentId
		UPDATE [Users_user] SET [money] = [money] + @Money WHERE id=@USERID
		
		-- 标记订单
		UPDATE [Web_order] SET [IsCalc] = 1, [CalcDate]=GETDATE()
		WHERE id IN(
		SELECT A.id
		FROM [Web_order] AS A
		LEFT JOIN [Web_mobilephone] AS B
		ON A.[ALIConfig_id] = B.[ALIConfig_id]
		LEFT JOIN [Web_agent] AS C
		ON B.Agent_id = C.id
		WHERE B.Agent_id IS NOT NULL AND C.Subscriber_id = @USERID AND [TK_Earning_Time] BETWEEN @StartDate AND @EndDate)
		
		FETCH NEXT FROM agent_id_cursor INTO @AgentId  --移动游标
	END 
	CLOSE agent_id_cursor
	DEALLOCATE agent_id_cursor
END

GO


