"use strict";

// Class Definition
var KTLoginPage = function () {

	var showErrorMsg = function(form, type, msg) {
        var alert = $('<div class="alert alert-bold alert-solid-' + type + ' alert-dismissible" role="alert">\
			<div class="alert-text">'+msg+'</div>\
			<div class="alert-close">\
                <i class="flaticon2-cross kt-icon-sm" data-dismiss="alert"></i>\
            </div>\
		</div>');

        form.find('.alert').remove();
        alert.prependTo(form);
        KTUtil.animateClass(alert[0], 'fadeIn animated');
	}

	var jumpToLoginPage = function(loginpage) {
		window.location.href = loginpage;
	}

	// Private Functions
	var handleLoginFormSubmit = function () {
		$('#kt_login_submit').click(function (e) {
			e.preventDefault();

			var btn = $(this);
			var form = $('#kt_login_form');

			form.validate({
				rules: {
					username: {
						required: true
					},
					password1: {
						required: true
					},
					password2: {
						required: true
					},
					leadcode: {
						required: true
					}
				},
			});


			if (!form.valid()) {
				$('#kt_scrolltop').click()
				return;
			}

			KTApp.progress(btn[0]);

			setTimeout(function () {
				KTApp.unprogress(btn[0]);
			}, 2000);

			// ajax form submit:  http://jquery.malsup.com/form/
			form.ajaxSubmit({
				url: '',
				success: function (response, status, xhr, $form) {
					$('#kt_scrolltop').click()
					// similate 2s delay
					if (response.status == 'NG') {
					    setTimeout(function () {
						KTApp.unprogress(btn[0]);
						showErrorMsg(form, 'danger', response.msg["password2"] || response.msg["username"] || response.msg["leadercode"] || response.msg["birthday"]);
					    }, 1000);
					} else {
						setTimeout(function () {
							KTApp.unprogress(btn[0]);
							showErrorMsg(form, 'success', response.msg["success"]);
							}, 1000);
						window.setTimeout(function() {
							jumpToLoginPage(response.loginpage)
						}, 5000)
					}
				}
			});
		});
	}

	// Public Functions
	return {
		// public functions
		init: function () {
			handleLoginFormSubmit();
		}
	};
}();

// Class Initialization
jQuery(document).ready(function () {
	KTLoginPage.init();
	$('#id_sex_0').attr("checked","checked");
	$('#id_platform_is_certification_1').attr("checked","checked");
});

$('#id_platform_is_certification_0').on('click', function() {
	$("#id_platform_certification_true_name").attr("disabled","disabled");
	$("#id_platform_certification_id_card").attr("disabled","disabled");
	$("#id_platform_certification_true_name").val('');
	$("#id_platform_certification_id_card").val('');
})

$('#id_platform_is_certification_1').on('click', function() {
	$("#id_platform_certification_true_name").removeAttr("disabled");
	$("#id_platform_certification_id_card").removeAttr("disabled");
})