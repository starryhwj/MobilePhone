"use strict";
// Class definition

var KTDatatableChangeSignatureMission = function () {

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
            sortable: false,
            autoHide: false,
            width: 50,
            textAlign: 'center',
        }, {
            field: 'Status',
            title: '状态',
            autoHide: false,
            sortable: false,
            template: function (row) {
                var status = {
                    '0': {
                        'title': '待获取',
                        'class': 'kt-badge--dark'
                    },
                    '1': {
                        'title': '已获取',
                        'class': ' kt-badge--primary'
                    },
                    '2': {
                        'title': '已成功结束',
                        'class': ' kt-badge--success'
                    },
                    '3': {
                        'title': '执行失败',
                        'class': ' kt-badge--danger'
                    },
                };
                return '<span class="kt-badge ' + status[row.Status].class +
                    ' kt-badge--inline kt-badge--pill">' + status[row.Status].title +
                    '</span>';
            },
        }, {
            field: 'MobilePhone__id',
            title: '设备ID',
            autoHide: false,
            sortable: false,
        }, {
            field: 'Describe',
            title: '个性签名',
            autoHide: false,
            sortable: false,
        }, {
            field: 'NewDescribe',
            title: '待更新签名',
            autoHide: false,
            sortable: false,
        }, {
            field: 'CreateTime',
            title: '创建日期',
            type: 'date',
            format: 'MM/DD/YYYY',
        }, {
            field: 'StartTime',
            title: '任务开始日期',
            type: 'date',
            format: 'MM/DD/YYYY',
        }, {
            field: 'FailReason',
            title: '失败原因',
            autoHide: false,
        }, {
            field: 'Actions',
            title: '操作',
            sortable: false,
            width: 110,
            overflow: 'visible',
            autoHide: false,
            textAlign: 'center',
            template: function (row) {
                if (row.Status == 0) {
                    return '\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="删除" data-delete-id="' + row.id + '">\
                        <i class="flaticon2-delete"></i>\
                    </button>\
                ';
                } else if (row.Status == 3) {
                    return '\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="删除" data-delete-id="' + row.id + '">\
                        <i class="flaticon2-delete"></i>\
                    </button>\
                '
                } else if (row.Status == 1) {
                    var now = new Date()
                    var start = new Date(row.StartTime)
                    var days = ((now - start) / (1 * 24 * 60 * 60 * 1000))
                    if (days > 2) {
                        return '\
                        <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="删除" data-delete-id="' + row.id + '">\
                            <i class="flaticon2-delete"></i>\
                        </button>\
                    '
                    } else {
                        return ''
                    }
                } else {
                    return ''
                }
            },
        }],
    };

    // basic demo
    var localSelectorDemo = function () {

        options.search = {
            input: $('#generalChangeSignatureMissionSearch'),
            onEnter: true,
        };

        var datatable = $('#datatable_ChangeSignatureMission').KTDatatable(options);

        $('#id_starttime').on('change', function () {
            datatable.search($(this).val().toLowerCase(), 'starttime');
        });

        $('#id_endtime').on('change', function () {
            datatable.search($(this).val().toLowerCase(), 'endtime');
        });

        $('#id_starttime').datepicker({
            todayHighlight: true,
            autoclose: true,
            pickerPosition: 'bottom-left',
            format: 'yyyy-mm-dd',
            todayBtn: 'linked',
            clearBtn: true,
            language: 'zh-CN',
        });

        $('#id_endtime').datepicker({
            todayHighlight: true,
            autoclose: true,
            pickerPosition: 'bottom-left',
            format: 'yyyy-mm-dd',
            todayBtn: 'linked',
            clearBtn: true,
            language: 'zh-CN',
        });

        datatable.on('click', '[data-delete-id]', function (row) {
            var id = $(this).data('delete-id');
            swal.fire({
                title: '确认删除?',
                text: "确认后无法撤销！",
                type: 'warning',
                showCancelButton: true,
                confirmButtonText: '是',
                cancelButtonText: '否'
            }).then(function (result) {
                if (result.value) {
                    var idstring = id + ','
                    $.ajax({
                        type: "POST",
                        url: $("#delete_url").text(),
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
    };

    return {
        // public functions
        init: function () {
            localSelectorDemo();
        }
    };
}();

jQuery(document).ready(function () {
    KTDatatableChangeSignatureMission.init();
    initSearch();
});

var initSearch = function () {
    //任务状态
    $("[name='missionstatusBtn']").click(function () {
        if ($(this).hasClass('btn-outline-hover-primary')) {
            var count = $("[name='missionstatusBtn']").length
            $(this).removeClass('btn-outline-hover-primary')
            $(this).addClass('btn-primary')
            $("[name='missionstatusBtnAll']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            if ($("#missionstatus .btn-primary").length == count) {
                $("[name='missionstatusBtnAll']").removeClass('btn-outline-hover-primary').addClass('btn-primary')
                $("[name='missionstatusBtn']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            }
            getStatusSearch()
        } else if ($(this).hasClass('btn-primary')) {
            $(this).removeClass('btn-primary')
            $(this).addClass('btn-outline-hover-primary')
            if ($("#missionstatus .btn-primary").length == 0) {
                $("[name='missionstatusBtnAll']").removeClass('btn-outline-hover-primary').addClass('btn-primary')
            }
            getStatusSearch()
        }
    })
    $("[name='missionstatusBtnAll']").click(function () {
        if ($(this).hasClass('btn-outline-hover-primary')) {
            $(this).removeClass('btn-outline-hover-primary')
            $(this).addClass('btn-primary')
            $("[name='missionstatusBtn']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            getStatusSearch()
        }
    })
}

var getStatusSearch = function () {
    var statusSearch = ''
    if ($("[name='missionstatusBtnAll']").hasClass('btn-primary')) {
        statusSearch = ''
    } else {
        var list = $("#missionstatus .btn-primary")
        for (var i = 0; i < list.length; i++) {
            var per = list[i]
            statusSearch = statusSearch + per.value + ','
        }
    }
    search('changesignaturemissionstatus', statusSearch)
}

var search = function (param, value) {
    var datatable = $('#datatable_ChangeSignatureMission').KTDatatable()
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
