"use strict";

jQuery(document).ready(function() {
    getAgentAccountData();
});

var getAgentAccountData = function() {
    var num = Number($('#agent_account_num').text())
    $.ajax({
        type: "POST",
        url: $("#get_agent_account_data_url").text(),
        data: {
            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
            num: num
        },
        success: function (response, status, xhr, $form) {
            if (response != 'Error') {
                $('#id_nickname').text(response['nickname']);

                $("#id_Fans").text(response['Fans']);
                $("#id_Praise").text(response['Praise']);
                $("#id_TotalNumOfPlay").text(response['TotalNumOfPlay']);
                $("#id_TotalNumOfComments").text(response['TotalNumOfComments']);
                $("#id_Video").text(response['Video']);

                $("#id_today_FansIncrease").text(response['today_FansIncrease']);
                $("#id_today_PraiseIncrease").text(response['today_PraiseIncrease']);
                $("#id_today_TotalNumOfPlayIncrease").text(response['today_TotalNumOfPlayIncrease']);
                $("#id_today_TotalNumOfCommentsIncrease").text(response['today_TotalNumOfCommentsIncrease']);
                $("#id_today_VideoIncrease").text(response['today_VideoIncrease']);

                $("#id_yestoday_FansIncrease").text(response['yestoday_FansIncrease']);
                $("#id_yestoday_PraiseIncrease").text(response['yestoday_PraiseIncrease']);
                $("#id_yestoday_TotalNumOfPlayIncrease").text(response['yestoday_TotalNumOfPlayIncrease']);
                $("#id_yestoday_TotalNumOfCommentsIncrease").text(response['yestoday_TotalNumOfCommentsIncrease']);
                $("#id_yestoday_VideoIncrease").text(response['yestoday_VideoIncrease']);
                
                $("#id_sevenday_FansIncrease").text(response['sevenday_FansIncrease']);
                $("#id_sevenday_PraiseIncrease").text(response['sevenday_PraiseIncrease']);
                $("#id_sevenday_TotalNumOfPlayIncrease").text(response['sevenday_TotalNumOfPlayIncrease']);
                $("#id_sevenday_TotalNumOfCommentsIncrease").text(response['sevenday_TotalNumOfCommentsIncrease']);
                $("#id_sevenday_VideoIncrease").text(response['sevenday_VideoIncrease']);

                $("#id_currentmonth_FansIncrease").text(response['currentmonth_FansIncrease']);
                $("#id_currentmonth_PraiseIncrease").text(response['currentmonth_PraiseIncrease']);
                $("#id_currentmonth_TotalNumOfPlayIncrease").text(response['currentmonth_TotalNumOfPlayIncrease']);
                $("#id_currentmonth_TotalNumOfCommentsIncrease").text(response['currentmonth_TotalNumOfCommentsIncrease']);
                $("#id_currentmonth_VideoIncrease").text(response['currentmonth_VideoIncrease']);
            }
        }
    });
    num += 1
    $('#agent_account_num').text(num)
}

var nextAccount = function() {
    getAgentAccountData()
}