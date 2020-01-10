USE [PhoneAutoRunManagementPlatform]
GO

/****** Object:  StoredProcedure [dbo].[CalcAgentIncome]    Script Date: 12/07/2019 10:57:34 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		���Ľ�
-- Create date: 2019.12.6
-- Description:	�����������
-- =============================================
CREATE PROCEDURE [dbo].[CalcAgentIncome]
	@AengtID int,
	@BeginDate Date,
	@EndDate Date,
	@Type int,
	@ReturnType nvarchar(100)
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;
	
	-- �Լ���������
	DECLARE @MyselfIncome decimal(18,2)
	DECLARE @MyselfOrderCount int
	-- �¼�����
	DECLARE @ALevelIncome decimal(18,2)
	DECLARE @ALevelOrderCount int
	-- ���¼�����
	DECLARE @BLevelIncome decimal(18,2)
	DECLARE @BLevelOrderCount int
	
	-- USERID
	DECLARE @USERID int
    SELECT @USERID = [Subscriber_id]
	FROM [Web_agent]
	WHERE id = @AengtID

    -- ����type��ȡorder�ģ�type=0ΪԤ����type=1Ϊ����
    IF @Type = 0
    BEGIN
		SELECT @MyselfIncome = ROUND(SUM([Pub_Share_Pre_Fee] - [TK_Commission_Pre_Fee_For_Media_Platform]) * (1 - AVG((C.UserALevelPercent + C.UserBLevelPercent + C.UserSystemPercent) / 100)), 2),
		@MyselfOrderCount = COUNT(*)
		FROM [Web_order] AS A
		LEFT JOIN [Web_mobilephone] AS B
		ON A.[ALIConfig_id] = B.[ALIConfig_id]
		LEFT JOIN [Web_agent] AS C
		ON B.Agent_id = C.id
		WHERE B.Agent_id IS NOT NULL AND C.Subscriber_id = @USERID AND [TK_Create_Time] BETWEEN @BeginDate AND @EndDate
		AND A.IsCalc = 0
    END
    ELSE
    BEGIN
		SELECT @MyselfIncome = ROUND(SUM([Pub_Share_Fee] - [TK_Commission_Fee_For_Media_Platform]) * (1 - AVG((C.UserALevelPercent + C.UserBLevelPercent + C.UserSystemPercent) / 100)), 2),
		@MyselfOrderCount = COUNT(*)
		FROM [Web_order] AS A
		LEFT JOIN [Web_mobilephone] AS B
		ON A.[ALIConfig_id] = B.[ALIConfig_id]
		LEFT JOIN [Web_agent] AS C
		ON B.Agent_id = C.id
		WHERE B.Agent_id IS NOT NULL AND C.Subscriber_id = @USERID AND [TK_Earning_Time] BETWEEN @BeginDate AND @EndDate
		AND A.IsCalc = 0
    END

    -- ���¼�������
    IF @Type = 0
    BEGIN
		SELECT @ALevelIncome = ROUND(SUM([Pub_Share_Pre_Fee] - [TK_Commission_Pre_Fee_For_Media_Platform]) * AVG(C.UserALevelPercent / 100), 2),
		@ALevelOrderCount = COUNT(*)
		FROM [Web_order] AS A
		LEFT JOIN [Web_mobilephone] AS B
		ON A.[ALIConfig_id] = B.[ALIConfig_id]
		LEFT JOIN [Web_agent] AS C
		ON B.Agent_id = C.id
		WHERE B.Agent_id IS NOT NULL AND C.UserALevel_id = @USERID AND [TK_Create_Time] BETWEEN @BeginDate AND @EndDate
		AND A.IsCalc = 0
    END
    ELSE
    BEGIN
		SELECT @ALevelIncome = ROUND(SUM([Pub_Share_Fee] - [TK_Commission_Fee_For_Media_Platform]) * AVG(C.UserALevelPercent / 100), 2),
		@ALevelOrderCount = COUNT(*)
		FROM [Web_order] AS A
		LEFT JOIN [Web_mobilephone] AS B
		ON A.[ALIConfig_id] = B.[ALIConfig_id]
		LEFT JOIN [Web_agent] AS C
		ON B.Agent_id = C.id
		WHERE B.Agent_id IS NOT NULL AND C.UserALevel_id = @USERID AND [TK_Earning_Time] BETWEEN @BeginDate AND @EndDate
		AND A.IsCalc = 0
    END
    
    -- �����¼�������
    IF @Type = 0
    BEGIN
		SELECT @BLevelIncome = ROUND(SUM([Pub_Share_Pre_Fee] - [TK_Commission_Pre_Fee_For_Media_Platform]) * AVG(C.UserBLevelPercent / 100), 2),
		@BLevelOrderCount = COUNT(*)
		FROM [Web_order] AS A
		LEFT JOIN [Web_mobilephone] AS B
		ON A.[ALIConfig_id] = B.[ALIConfig_id]
		LEFT JOIN [Web_agent] AS C
		ON B.Agent_id = C.id
		WHERE B.Agent_id IS NOT NULL AND C.UserBLevel_id = @USERID AND [TK_Create_Time] BETWEEN @BeginDate AND @EndDate
		AND A.IsCalc = 0
    END
    ELSE
    BEGIN
		SELECT @BLevelIncome = ROUND(SUM([Pub_Share_Fee] - [TK_Commission_Fee_For_Media_Platform]) * AVG(C.UserBLevelPercent / 100), 2),
		@BLevelOrderCount = COUNT(*)
		FROM [Web_order] AS A
		LEFT JOIN [Web_mobilephone] AS B
		ON A.[ALIConfig_id] = B.[ALIConfig_id]
		LEFT JOIN [Web_agent] AS C
		ON B.Agent_id = C.id
		WHERE B.Agent_id IS NOT NULL AND C.UserBLevel_id = @USERID AND [TK_Earning_Time] BETWEEN @BeginDate AND @EndDate
		AND A.IsCalc = 0
    END
    
    -- ������
	DECLARE @TotalIncome decimal(18,2)
	DECLARE @TotalOrderCount int
    SET @TotalIncome = ISNULL(@MyselfIncome, 0) + ISNULL(@ALevelIncome, 0) + ISNULL(@BLevelIncome, 0)
    SET @TotalOrderCount = ISNULL(@MyselfOrderCount, 0) + ISNULL(@ALevelOrderCount, 0) + ISNULL(@BLevelOrderCount, 0)
    
    -- �����¼������¼�����
	DECLARE @ABLevelIncome decimal(18,2)
	DECLARE @ABLevelOrderCount int
    SET @ABLevelIncome = ISNULL(@ALevelIncome, 0) + ISNULL(@BLevelIncome, 0)
    SET @ABLevelOrderCount = ISNULL(@ALevelOrderCount, 0) + ISNULL(@BLevelOrderCount, 0)
    
    IF @ReturnType = 'Total'
    BEGIN  
		SELECT @TotalIncome AS ReturnMoney, @TotalOrderCount AS ReturnOrderCount
	END
	
	IF @ReturnType = 'Myself'
    BEGIN  
		SELECT @MyselfIncome AS ReturnMoney, @MyselfOrderCount AS ReturnOrderCount		
	END
	
	IF @ReturnType = 'ALevel'
    BEGIN  
		SELECT @ALevelIncome AS ReturnMoney, @ALevelOrderCount AS ReturnOrderCount		
	END
	
	IF @ReturnType = 'BLevel'
    BEGIN  
		SELECT @BLevelIncome AS ReturnMoney, @BLevelOrderCount AS ReturnOrderCount			
	END
	
	IF @ReturnType = 'ABLevel'
    BEGIN
		SELECT @ABLevelIncome AS ReturnMoney, @ABLevelOrderCount AS ReturnOrderCount			
	END
END

GO


