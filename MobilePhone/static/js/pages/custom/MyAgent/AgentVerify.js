"use strict";
// Class definition

var KTDatatableRecordSelectionDemo = function() {

    // Private functions
    var options = {
        // datasource definition
        data: {
            type: 'remote',
            source: {
                read: {
                    url: $("#data_url").text(),
                    params: {
                        csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value
                    }
                },
            },
            pageSize: 10,
            serverPaging: true,
            serverFiltering: true,
            serverSorting: true,
        },
        // layout definition
        layout: {
            theme: 'default', // datatable theme
            class: '', // custom wrapper class
            scroll: true, // enable/disable datatable scroll both horizontal and
            // vertical when needed.
            height: 1000, // datatable's body's fixed height
            footer: false // display/hide footer
        },

        rows: {
            autoHide: false,
        },

        // column sorting
        sortable: true,

        pagination: true,

        // Translate
        translate: {
            records: {
                processing: '请等待...',
                noRecords: '没有数据',
            },
            toolbar: {
                pagination: {
                    items: {
                        default: {
                          first: '首页',
                          prev: '前一页',
                          next: '下一页',
                          last: '尾页',
                          more: '更多',
                          input: '请输入页码',
                          select: '选择每页行数'
                        },
                        info: '第{{start}} - {{end}}行，共{{total}}行',
                    },
                },
            },
        },

        // columns definition

        columns: [{
            field: 'id',
            title: 'ID',
            autoHide: false,
            sortable: false,
        },  {
            field: 'username',
            title: '账号',
            autoHide: false,
            sortable: false,
        },{
            field: 'date_joined',
            title: '申请日期',
            type: 'date',
            format: 'MM/DD/YYYY',
        }, {
            field: 'leader__username',
            title: '上级名称',
            autoHide: false,
            sortable: false,
        }, {
            field: 'true_name',
            title: '姓名',
            autoHide: false,
            sortable: false,
        },{
            field: 'phone',
            title: '手机',
            autoHide: false,
            sortable: false,
        },{
            field: 'wechat',
            title: '微信号',
            autoHide: false,
            sortable: false,
        },{
            field: 'wechat_nickname',
            title: '微信昵称',
            autoHide: false,
            sortable: false,
        },{
            field: 'sex',
            title: '性别',
            autoHide: false,
            sortable: false,
            template: function (row) {
                var status = {
                    '0': {
                        'title': '男',
                        'class': 'kt-badge--success'
                    },
                    '1': {
                        'title': '女',
                        'class': ' kt-badge--danger'
                    },
                };
                return '<span class="kt-badge ' + status[row.sex].class +
                    ' kt-badge--inline kt-badge--pill">' + status[row.sex].title +
                    '</span>';
            },
        }, {
            field: 'platform',
            title: '平台',
            autoHide: false,
            sortable: false,
        },{
            field: 'platform_id',
            title: '平台账号',
            autoHide: false,
            sortable: false,
        },{
            field: 'platform_password',
            title: '平台密码',
            autoHide: false,
            sortable: false,
        },{
            field: 'platform_is_certification',
            title: '是否实名验证',
            autoHide: false,
            sortable: false,
            template: function (row) {
                var status = {
                    '0': {
                        'title': '否',
                        'class': 'kt-badge--danger'
                    },
                    '1': {
                        'title': '是',
                        'class': ' kt-badge--success'
                    },
                };
                return '<span class="kt-badge ' + status[row.platform_is_certification].class +
                    ' kt-badge--inline kt-badge--pill">' + status[row.platform_is_certification].title +
                    '</span>';
            },
        },{
            field: 'platform_certification_true_name',
            title: '实名验证姓名',
            autoHide: false,
            sortable: false,
        },{
            field: 'platform_certification_id_card',
            title: '实名验证身份证',
            autoHide: false,
            sortable: false,
        },{
            field: 'qq',
            title: 'QQ',
            autoHide: false,
            sortable: false,
        },{
            field: 'birthday',
            title: '出生日期',
            type: 'date',
            format: 'YYYY-MM-DD',
        }, {
            field: 'Actions',
            title: '操作',
            sortable: false,
            width: 110,
            overflow: 'visible',
	        autoHide: false,
	        textAlign: 'center',
            template: function(row) {
                var username = $("#username").text()
                if (username == 'admin') {
                    return '\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="通过合伙人身份" data-passsuper-id="' + row.id + '">\
                        <i class="flaticon2-check-mark"></i>\
                    </button>\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="通过主要用户身份" data-passmain-id="' + row.id + '">\
                        <i class="flaticon2-check-mark"></i>\
                    </button>\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="通过普通代理身份" data-passagent-id="' + row.id + '">\
                        <i class="flaticon2-check-mark"></i>\
                    </button>\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="不通过" data-delete-id="' + row.id + '">\
                        <i class="flaticon2-delete"></i>\
                    </button>\
                ';
                } else {
                    return '\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="通过主要用户身份" data-passmain-id="' + row.id + '">\
                        <i class="flaticon2-check-mark"></i>\
                    </button>\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="通过普通代理身份" data-passagent-id="' + row.id + '">\
                        <i class="flaticon2-check-mark"></i>\
                    </button>\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="不通过" data-delete-id="' + row.id + '">\
                        <i class="flaticon2-delete"></i>\
                    </button>\
                ';
                }
            },
        }],
    };

    // basic demo
    var localSelectorDemo = function() {

        options.search = {
            input: $('#generalAgentVerifySearch'),
            onEnter: true,
        };

        var datatable = $('#local_record_selection').KTDatatable(options);

        $('#agentVerify_column').on('change', function () {
            datatable.search($(this).val().toLowerCase(), 'agentVerifycolumn');
        });

        $('#agentVerify_column').selectpicker();

        $('#kt_datatable_not_pass_all').on('click', function() {
            swal.fire({
                title: '确认不通过?',
                text: "确认后无法撤销！",
                type: 'warning',
                showCancelButton: true,
                confirmButtonText: '是',
                cancelButtonText: '否'
            }).then(function(result) {
                if (result.value) {
                    // select active rows
                    datatable.rows('.kt-datatable__row--active');
                    // check selected nodes
                    if (datatable.nodes().length > 0) {
                        // get column by field name and get the column nodes
                        var ids = datatable.rows('.kt-datatable__row--active').
                        nodes().
                        find('.kt-checkbox--single > [type="checkbox"]').
                        map(function(i, chk) {
                            return $(chk).val();
                        });
                        var idstring = '';
                        for (var i = 0; i < ids.length; i++) {
                            idstring = idstring + ids[i] + ','
                         }
                        $.ajax({
                            type: "POST",
                            url: $("#not_pass_url").text(),
                            data: {
                                csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                                ids: idstring
                            },
                            success: function (response, status, xhr, $form) {
                                datatable.reload()
                            }
                        });
                     }
                };
             })
        });
        
        $('#kt_datatable_pass_all').on('click', function() {
            swal.fire({
                title: '确认通过?',
                text: "确认后无法撤销！",
                type: 'info',
                showCancelButton: true,
                confirmButtonText: '是',
                cancelButtonText: '否'
            }).then(function(result) {
                if (result.value) {
                    // select active rows
                    datatable.rows('.kt-datatable__row--active');
                    // check selected nodes
                    if (datatable.nodes().length > 0) {
                        // get column by field name and get the column nodes
                        var ids = datatable.rows('.kt-datatable__row--active').
                        nodes().
                        find('.kt-checkbox--single > [type="checkbox"]').
                        map(function(i, chk) {
                            return $(chk).val();
                        });
                        var idstring = '';
                        for (var i = 0; i < ids.length; i++) {
                            idstring = idstring + ids[i] + ','
                         }
                        $.ajax({
                            type: "POST",
                            url: $("#pass_url").text(),
                            data: {
                                csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                                ids: idstring
                            },
                            success: function (response, status, xhr, $form) {
                                datatable.reload()
                            }
                        });
                     }
                };
             })
		});

		datatable.on('click', '[data-delete-id]', function(row) {
		    var id = $(this).data('delete-id');
		    swal.fire({
                title: '确认不通过?',
                text: "确认后无法撤销！",
                type: 'warning',
                showCancelButton: true,
                confirmButtonText: '是',
                cancelButtonText: '否'
            }).then(function(result) {
                if (result.value) {
                    var idstring = id + ','
                    $.ajax({
                        type: "POST",
                        url: $("#not_pass_url").text(),
                        data: {
                            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                            ids: idstring
                        },
                        success: function (response, status, xhr, $form) {
                            datatable.reload()
                        }
                    });
                };
             })
		});

		datatable.on('click', '[data-passsuper-id]', function() {
            var id = $(this).data('passsuper-id');
		    swal.fire({
                title: '确认该账户拥有合伙人权限（能登陆后台，能认证淘宝）?',
                text: "确认后无法撤销！",
                type: 'info',
                showCancelButton: true,
                confirmButtonText: '是',
                cancelButtonText: '否'
            }).then(function(result) {
                if (result.value) {
                    var idstring = id + ','
                    $.ajax({
                        type: "POST",
                        url: $("#pass_as_superuser_url").text(),
                        data: {
                            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                            ids: idstring
                        },
                        success: function (response, status, xhr, $form) {
                            datatable.reload()
                        }
                    });
                };
             })
        });
        
        datatable.on('click', '[data-passmain-id]', function() {
            var id = $(this).data('passmain-id');
		    swal.fire({
                title: '确认该账户拥有主要用户权限（能登陆后台，不能认证淘宝）?',
                text: "确认后无法撤销！",
                type: 'info',
                showCancelButton: true,
                confirmButtonText: '是',
                cancelButtonText: '否'
            }).then(function(result) {
                if (result.value) {
                    var idstring = id + ','
                    $.ajax({
                        type: "POST",
                        url: $("#pass_as_mainuser_url").text(),
                        data: {
                            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                            ids: idstring
                        },
                        success: function (response, status, xhr, $form) {
                            datatable.reload()
                        }
                    });
                };
             })
        });
        
        datatable.on('click', '[data-passagent-id]', function() {
            var id = $(this).data('passagent-id');
		    swal.fire({
                title: '确认该账户拥有普通代理权限（不能登陆后台，不能认证淘宝）?',
                text: "确认后无法撤销！",
                type: 'info',
                showCancelButton: true,
                confirmButtonText: '是',
                cancelButtonText: '否'
            }).then(function(result) {
                if (result.value) {
                    var idstring = id + ','
                    $.ajax({
                        type: "POST",
                        url: $("#pass_as_agent_url").text(),
                        data: {
                            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                            ids: idstring
                        },
                        success: function (response, status, xhr, $form) {
                            datatable.reload()
                        }
                    });
                };
             })
		});

        datatable.on(
            'kt-datatable--on-check kt-datatable--on-uncheck kt-datatable--on-layout-updated',
            function(e) {
                var checkedNodes = datatable.rows('.kt-datatable__row--active').nodes();
                var count = checkedNodes.length;
                $('#kt_datatable_selected_number').html(count);
                if (count > 0) {
                    $('#kt_datatable_group_action_form').collapse('show');
                } else {
                    $('#kt_datatable_group_action_form').collapse('hide');
                }
            });

    };

    return {
        // public functions
        init: function() {
            localSelectorDemo();
        }
    };
}();

jQuery(document).ready(function() {
    KTDatatableRecordSelectionDemo.init();
});

