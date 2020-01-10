$(document).ready(function () {
    //复制邀请码
    var copyBtn1 = new ClipboardJS('#id_copy_invite_code', {
        text: function () {
            return document.getElementById("id_invite_code").innerHTML.trim(); // 返回需要复制的内容
        }
    });

    copyBtn1.on("success", function (e) {
        // 复制成功
        $('#copyinvitecodeModal').modal('show');
    });

    //复制邀请码
    var copyBtn2 = new ClipboardJS('#id_copy_web', {
        text: function () {
            return document.getElementById("id_web").innerHTML.trim(); // 返回需要复制的内容
        }
    });

    copyBtn2.on("success", function (e) {
        // 复制成功
        $('#copywebModal').modal('show');
    });
})


//跳转淘宝授权
var TaoBaoOuth = function() {
    window.location.href = $('#taobaoouthurl').text()
}

var showErrorMsg = function(form, type, msg) {
    var alert = $('<div class="col-lg-12 col-xl-12 alert alert-bold alert-solid-' + type + ' alert-dismissible" role="alert">\
        <div class="alert-text">'+msg+'</div>\
        <div class="alert-close">\
            <i class="flaticon2-cross kt-icon-sm" data-dismiss="alert"></i>\
        </div>\
    </div>');

    form.find('.alert').remove();
    alert.prependTo(form);
    KTUtil.animateClass(alert[0], 'fadeIn animated');
}

//申请提现
var ApplyForWithdraw = function() {
    var btn = $(this)
    var form = $('#withdrawform');
    $.ajax({
        type: "POST",
        url: $("#create_withdraw_url").text(),
        data: {
            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
            money: document.getElementById("id_money").value,
        },
        success: function (response, status, xhr, $form) {
            if (response['status'] != 'NG') {
                window.location.href = response['msg'];
            } else {
                setTimeout(function () {
                    KTApp.unprogress(btn[0]);
                    showErrorMsg(form, 'danger', response["msg"]);
                    }, 1000);
            }
		}
    })
}
