USE [PhoneAutoRunManagementPlatform]
GO

/****** Object:  StoredProcedure [dbo].[AllTikTokAccountDaySummary]    Script Date: 12/03/2019 16:04:15 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		何文晋
-- Create date: 2019.12.3
-- Description:	抖音账号每天统计表
-- =============================================
CREATE PROCEDURE [dbo].[AllTikTokAccountDaySummary]
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Insert statements for procedure here
	DECLARE @YESTODAY DATE
	SELECT @YESTODAY = CONVERT(varchar(10), DATEADD(DAY,-1,GETDATE()), 120)

	INSERT INTO [Web_tiktokaccountdaysummary]
	SELECT @YESTODAY AS Summary_Date,[Attention],[Fans],[Praise],[Video],[NumOfPraiseToOther],id
	FROM [Web_tiktokaccount]
END

GO


