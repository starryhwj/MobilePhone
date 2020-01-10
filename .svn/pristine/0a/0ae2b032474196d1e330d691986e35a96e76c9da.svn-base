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
            field: 'Agent__Subscriber__username',
            title: '账号',
            autoHide: false,
            sortable: false,
        },{
            field: 'ApplyDate',
            title: '申请日期',
            type: 'date',
            format: 'MM/DD/YYYY',
        }, {
            field: 'Money',
            title: '提现金额',
            autoHide: false,
            sortable: false,
        },{
            field: 'IsPass',
            title: '状态',
            autoHide: false,
            sortable: false,
            width: 60,
            template: function (row) {
                var status = {
                    '0': {
                        'title': '待审批',
                        'class': 'kt-badge--info'
                    },
                    '1': {
                        'title': '已通过',
                        'class': ' kt-badge--success'
                    },
                    '2': {
                        'title': '未通过',
                        'class': ' kt-badge--danger'
                    },
                };
                return '<span class="kt-badge ' + status[row.IsPass].class +
                    ' kt-badge--inline kt-badge--pill">' + status[row.IsPass].title +
                    '</span>';
            },
        },{
            field: 'Agent__UserALevel__username',
            title: '上级名称',
            autoHide: false,
            sortable: false,
        }, {
            field: 'Agent__Subscriber__true_name',
            title: '姓名',
            autoHide: false,
            sortable: false,
        },{
            field: 'Agent__Subscriber__phone',
            title: '手机',
            autoHide: false,
            sortable: false,
        },{
            field: 'Agent__Subscriber__wechat',
            title: '微信号',
            autoHide: false,
            sortable: false,
        }, {
            field: 'Actions',
            title: '操作',
            sortable: false,
            width: 110,
            overflow: 'visible',
	        autoHide: false,
	        textAlign: 'center',
            template: function(row) {
                if (row.IsPass == 0) {
                    return '\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="通过" data-pass-id="' + row.id + '">\
                        <i class="flaticon2-check-mark"></i>\
                    </button>\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="不通过" data-notpass-id="' + row.id + '">\
                        <i class="flaticon2-delete"></i>\
                    </button>\
                ';
                } else {
                    return ''
                }
            },
        }],
    };

    // basic demo
    var localSelectorDemo = function() {

        options.search = {
            input: $('#generalCashManageSearch'),
            onEnter: true,
        };

        var datatable = $('#local_record_selection').KTDatatable(options);

        $('#cashmanage_column').on('change', function () {
            datatable.search($(this).val().toLowerCase(), 'cashmanagecolumn');
        });

        $('#cashmanage_column').selectpicker();

		datatable.on('click', '[data-notpass-id]', function(row) {
		    var id = $(this).data('notpass-id');
		    swal.fire({
                title: '确认不通过?',
                text: "确认后无法撤销！",
                type: 'warning',
                showCancelButton: true,
                confirmButtonText: '是',
                cancelButtonText: '否'
            }).then(function(result) {
                if (result.value) {
                    $.ajax({
                        type: "POST",
                        url: $("#not_pass_url").text(),
                        data: {
                            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                            id: id
                        },
                        success: function (response, status, xhr, $form) {
                            datatable.reload()
                        }
                    });
                };
             })
		});

		datatable.on('click', '[data-pass-id]', function() {
            var id = $(this).data('pass-id');
		    swal.fire({
                title: '确认通过?',
                text: "确认后无法撤销！",
                type: 'info',
                showCancelButton: true,
                confirmButtonText: '是',
                cancelButtonText: '否'
            }).then(function(result) {
                if (result.value) {
                    $.ajax({
                        type: "POST",
                        url: $("#pass_url").text(),
                        data: {
                            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                            id: id
                        },
                        success: function (response, status, xhr, $form) {
                            datatable.reload()
                        }
                    });
                };
             })
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
    initSearch();
});

var initSearch = function () {
    //状态
    $("[name='StatusBtn']").click(function () {
        if ($(this).hasClass('btn-outline-hover-primary')) {
            var count = $("[name='StatusBtn']").length
            $(this).removeClass('btn-outline-hover-primary')
            $(this).addClass('btn-primary')
            $("[name='StatusBtnAll']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            if ($("#Status .btn-primary").length == count) {
                $("[name='StatusBtnAll']").removeClass('btn-outline-hover-primary').addClass('btn-primary')
                $("[name='StatusBtn']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            }
            getStatusSearch()
        } else if ($(this).hasClass('btn-primary')) {
            $(this).removeClass('btn-primary')
            $(this).addClass('btn-outline-hover-primary')
            if ($("#Status .btn-primary").length == 0) {
                $("[name='StatusBtnAll']").removeClass('btn-outline-hover-primary').addClass('btn-primary')
            }
            getStatusSearch()
        }
    })
    $("[name='StatusBtnAll']").click(function () {
        if ($(this).hasClass('btn-outline-hover-primary')) {
            $(this).removeClass('btn-outline-hover-primary')
            $(this).addClass('btn-primary')
            $("[name='StatusBtn']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            getStatusSearch()
        }
    })
}

var getStatusSearch = function () {
    var statusSearch = ''
    if ($("[name='StatusBtnAll']").hasClass('btn-primary')) {
        statusSearch = ''
    } else {
        var list = $("#Status .btn-primary")
        for (var i = 0; i < list.length; i++) {
            var per = list[i]
            statusSearch = statusSearch + per.value + ','
        }
    }
    orderSearch('status', statusSearch)
}

var orderSearch = function (param, value) {
    var datatable = $('#local_record_selection').KTDatatable()
    var cur_query = datatable.getDataSourceParam('query')
    if (cur_query == null) {
        cur_query = {}
        cur_query[param] = value
    } else {
        cur_query[param] = value
    }
    datatable.setDataSourceParam('query', cur_query)
    datatable.load()
}


