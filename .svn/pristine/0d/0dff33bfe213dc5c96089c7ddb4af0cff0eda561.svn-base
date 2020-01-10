USE [PhoneAutoRunManagementPlatform]
GO

/****** Object:  StoredProcedure [dbo].[AllWorksDaySummary]    Script Date: 12/03/2019 15:59:15 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		何文晋
-- Create date: 2019.12.3
-- Description:	抖音视频每天统计
-- =============================================
CREATE PROCEDURE [dbo].[AllWorksDaySummary]
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Insert statements for procedure here
	DECLARE @YESTODAY DATE
	SELECT @YESTODAY = CONVERT(varchar(10), DATEADD(DAY,-1,GETDATE()), 120)

	INSERT INTO [Web_worksdaysummary]
	SELECT @YESTODAY AS Summary_Date,[NumOfPraiseGet],[NumOfComments],[NumOfShare],[NumOfPlay],id
	FROM [Web_works]
END

GO


