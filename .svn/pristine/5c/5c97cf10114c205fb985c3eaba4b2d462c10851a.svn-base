-- =============================================
-- Author:		何文晋
-- Create date: 2019.12.6
-- Description:	计算代理任务收入
-- =============================================
CREATE PROCEDURE [dbo].[CalcAgentMissionIncome]
	@AengtID int,
	@BeginDate Date,
	@EndDate Date
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;
	
	DECLARE @TotalMissionIncome decimal(18,2)

    -- 互刷任务
    DECLARE @MutualBrushMissionIncome decimal(18,2)
	DECLARE @MutualBrushMissionCount int
	
    SELECT @MutualBrushMissionIncome = SUM([MissionIncome]), @MutualBrushMissionCount = COUNT(*)
	FROM [Web_mutualbrushmission] 
	WHERE [MobilePhone_id] IN (
	SELECT id FROM [Web_mobilephone]
	WHERE Agent_id = @AengtID) AND [Status] = 2
	AND [StartTime] BETWEEN @BeginDate AND @EndDate
    
    -- 观看直播任务
    DECLARE @WatchLiveMissionIncome decimal(18,2)
    DECLARE @WatchLiveMissionCount int
    
    SELECT @WatchLiveMissionIncome = SUM([MissionIncome]), @WatchLiveMissionCount = COUNT(*)
	FROM [Web_watchlivemission] 
	WHERE [MobilePhone_id] IN (
	SELECT id FROM [Web_mobilephone]
	WHERE Agent_id = @AengtID) AND [Status] = 2
	AND [StartTime] BETWEEN @BeginDate AND @EndDate
	
	-- 总任务收入
	SET @TotalMissionIncome = ISNULL(@MutualBrushMissionIncome, 0) + ISNULL(@WatchLiveMissionIncome, 0)
	
	SELECT @TotalMissionIncome AS ReturnMoney, @MutualBrushMissionCount AS MutualBrushMissionCount, @WatchLiveMissionCount AS WatchLiveMissionCount
	
END




