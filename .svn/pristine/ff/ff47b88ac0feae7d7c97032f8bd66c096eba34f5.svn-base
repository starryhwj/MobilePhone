$(document).ready(function () {
    //复制邀请码
    var copyBtn1 = new ClipboardJS('#id_copy_invite_code', {
        text: function () {
            code = document.getElementById("id_copy_invite_code").innerHTML.trim()
            code = code.replace('邀请码:', '')
            return code; // 返回需要复制的内容
        }
    });

    copyBtn1.on("success", function (e) {
        // 复制成功
        toastr.options = {
            "closeButton": false,
            "debug": false,
            "newestOnTop": false,
            "progressBar": false,
            "positionClass": "toast-bottom-center",
            "preventDuplicates": false,
            "onclick": null,
            "showDuration": "300",
            "hideDuration": "1000",
            "timeOut": "5000",
            "extendedTimeOut": "1000",
            "showEasing": "swing",
            "hideEasing": "linear",
            "showMethod": "fadeIn",
            "hideMethod": "fadeOut"
        };

        toastr.success("复制邀请码成功!");
    });

    //复制网址
    var copyBtn2 = new ClipboardJS('#id_copy_web', {
        container: document.getElementById('qrcode'),
        text: function () {
            web = document.getElementById("id_web").innerHTML.trim(); // 返回需要复制的内容
            return web
        }
    });

    copyBtn2.on("success", function (e) {
        // 复制成功
        toastr.options = {
            "closeButton": false,
            "debug": false,
            "newestOnTop": false,
            "progressBar": false,
            "positionClass": "toast-bottom-center",
            "preventDuplicates": false,
            "onclick": null,
            "showDuration": "300",
            "hideDuration": "1000",
            "timeOut": "5000",
            "extendedTimeOut": "1000",
            "showEasing": "swing",
            "hideEasing": "linear",
            "showMethod": "fadeIn",
            "hideMethod": "fadeOut"
        };

        toastr.success("复制网址成功!");
    });
})