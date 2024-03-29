USE [PhoneAutoRunManagementPlatform]
GO

/****** Object:  StoredProcedure [dbo].[AllPIDDaySummary]    Script Date: 11/29/2019 11:11:46 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		何文晋
-- Create date: 2019.11.29
-- Description:	每天统计一次所有PID的前一天的订单数据
-- =============================================
CREATE PROCEDURE [dbo].[AllPIDDaySummary]
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Insert statements for procedure here
    DECLARE @TODAY DATE
    DECLARE @YESTODAY DATE
	SELECT @TODAY = CONVERT(varchar(10),GETDATE(),120)
	SELECT @YESTODAY = CONVERT(varchar(10), DATEADD(DAY,-1,GETDATE()), 120)
	
	INSERT INTO [Web_piddaysummary]
	SELECT @YESTODAY AS Summary_Date,
	SUM(CASE WHEN A.TK_Paid_Time BETWEEN @YESTODAY AND @TODAY THEN 1 ELSE 0 END) AS Paid_Order_Count,
	SUM(CASE WHEN A.TK_Paid_Time BETWEEN @YESTODAY AND @TODAY THEN (A.Pub_Share_Pre_Fee - A.TK_Commission_Pre_Fee_For_Media_Platform) ELSE 0 END) AS Paid_Pre_Fee,
	SUM(CASE WHEN A.TK_Earning_Time BETWEEN @YESTODAY AND @TODAY THEN (A.Pub_Share_Fee - A.TK_Commission_Rate_For_Media_Platform) ELSE 0 END) AS Earn_Pre_Fee,
	B.id
	FROM [Web_order] AS A
	INNER JOIN 
	[Web_aliconfig] AS B
	ON A.ADZone_ID = B.LASTPID
	WHERE A.Refund_Tag = 0
	GROUP BY B.id
	
END

GO


