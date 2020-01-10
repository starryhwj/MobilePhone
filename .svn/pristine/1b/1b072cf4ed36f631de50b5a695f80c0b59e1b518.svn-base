"use strict";
// Class definition

var KTDatatableRecordSelectionDemo = function () {

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
            width: 100,
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
            field: 'TargetURL',
            title: '目标主播链接',
            autoHide: false,
            sortable: false,
            width: 200,
        },{
            field: 'MobilePhone__id',
            title: '设备ID',
            autoHide: false,
            sortable: false,
            width: 50,
        }, {
            field: 'MissionIncome',
            title: '任务收益(元)',
            autoHide: false,
        },{
            field: 'CreateTime',
            title: '创建日期',
            type: 'date',
        }, {
            field: 'StartTime',
            title: '任务开始日期',
            type: 'date',
        }, {
            field: 'EndTime',
            title: '任务结束日期',
            type: 'date',
        },{
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
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="详情" data-edit-id="' + row.id + '">\
                        <i class="flaticon2-file"></i>\
                    </button>\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="删除" data-delete-id="' + row.id + '">\
                        <i class="flaticon2-delete"></i>\
                    </button>\
                ';
                } else if(row.Status == 3) {
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
            input: $('#generalWatchLiveMissionSearch'),
            onEnter: true,
        };

        var datatable = $('#datatable_WatchLiveMission').KTDatatable(options);

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

        $('#id_create_mission_starttime').datetimepicker({
            todayHighlight: true,
            autoclose: true,
            pickerPosition: 'bottom-left',
            format: 'yyyy-mm-dd hh:ii:00',
            clearBtn: true,
            todayBtn: true,
            language: 'zh-CN',
        });

        $('#id_edit_mission_starttime').datetimepicker({
            todayHighlight: true,
            autoclose: true,
            pickerPosition: 'bottom-left',
            format: 'yyyy-mm-dd hh:ii:00',
            clearBtn: true,
            todayBtn: true,
            language: 'zh-CN',
        }).on('click', function (e) {
            $("#id_edit_mission_starttime").datetimepicker("setEndDate", $("#id_edit_mission_endtime").val());
        });

        $('#id_edit_mission_endtime').datetimepicker({
            todayHighlight: true,
            autoclose: true,
            pickerPosition: 'bottom-left',
            format: 'yyyy-mm-dd hh:ii:00',
            clearBtn: true,
            todayBtn: true,
            language: 'zh-CN',
        }).on('click', function (e) {
            $("#id_edit_mission_endtime").datetimepicker("setStartDate", $("#id_edit_mission_starttime").val());
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

        datatable.on('click', '[data-edit-id]', function () {
            var id = $(this).data('edit-id');
            initeditmodal();
            $.ajax({
                type: "POST",
                url: $("#get_by_id_url").text(),
                data: {
                    csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                    id: id
                },
                success: function (response, status, xhr, $form) {
                    if (response != 'Error') {
                        $('#editmissionModal').modal('show');
                        document.getElementById("id_edit_mission_targeturl").value = response['targeturl'];
                        document.getElementById("id_edit_mission_commenttext").value = response['commenttext'];
                        document.getElementById("id_edit_mission_commenttimes").value = response['commenttimes'];                        
                        document.getElementById("id_edit_mission_data_id").value = response['dataid'];
                        document.getElementById("id_edit_mission_starttime").value = response['starttime'];
                        document.getElementById("id_edit_mission_endtime").value = response['endtime'];
                    }
                }
            });
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
    KTDatatableRecordSelectionDemo.init();
    initSearch();
});


var EditMission = function () {
    var form = $('#kt_edit_mission_form');

    form.validate({
        rules: {
            edit_mission_targeturl: {
                required: true
            }
        }
    });

    if (!form.valid()) {
        return;
    }

    var starttime_str = document.getElementById("id_edit_mission_starttime").value
    var endtime_str = document.getElementById("id_edit_mission_endtime").value
    var needalert = false
    if (typeof (starttime_str) != "undefined" && typeof (endtime_str) != "undefined" && starttime_str != '' && endtime_str != '') {
        var starttime = convertDateFromString(starttime_str)
        var endtime = convertDateFromString(endtime_str)
        var diff = getInervalHour(starttime, endtime)
        if (diff > 5) {
            needalert = true
        }
    }

    if (needalert) {
        swal.fire({
            title: '',
            text: "任务持续时间超过6小时，是否确认？",
            type: 'warning',
            showCancelButton: true,
            confirmButtonText: '是',
            cancelButtonText: '否'
        }).then(function (result) {
            if (result.value) {
                $.ajax({
                    type: "POST",
                    url: $("#edit_url").text(),
                    data: {
                        csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                        targeturl: document.getElementById("id_edit_mission_targeturl").value,
                        commenttext: document.getElementById("id_edit_mission_commenttext").value,
                        commenttimes: document.getElementById("id_edit_mission_commenttimes").value,
                        id: document.getElementById("id_edit_mission_data_id").value,
                        starttime: starttime_str,
                        endtime: endtime_str,
                    },
                    success: function (response, status, xhr, $form) {
                        if (response != 'Error') {
                            window.location.href = response;
                        }
                    }
                })
            };
        })
    } else {
        $.ajax({
            type: "POST",
            url: $("#edit_url").text(),
            data: {
                csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                targeturl: document.getElementById("id_edit_mission_targeturl").value,
                commenttext: document.getElementById("id_edit_mission_commenttext").value,
                commenttimes: document.getElementById("id_edit_mission_commenttimes").value,
                id: document.getElementById("id_edit_mission_data_id").value,
                starttime: starttime_str,
                endtime: endtime_str,
            },
            success: function (response, status, xhr, $form) {
                if (response != 'Error') {
                    window.location.href = response;
                }
            }
        })
    }
}

var initeditmodal = function () {
    document.getElementById("id_edit_mission_targeturl").value = '';
    document.getElementById("id_edit_mission_commenttext").value = '';  
    document.getElementById("id_edit_mission_commenttimes").value = '';     
}

var initcreatemodal = function () {
    document.getElementById("id_create_mission_divice").value = '';
    document.getElementById("id_create_device_id").value = '';
    document.getElementById("id_create_mission_targeturl").value = '';
    document.getElementById("id_create_mission_interval").value = '';
    document.getElementById("id_create_mission_lasttime").value = '';
    document.getElementById("id_create_commenttext").value = '';        
    document.getElementById("id_create_mission_commenttimes").value = '';     
    document.getElementById("id_create_mission_missionincome").value = '0.00';       
    $("#id_create_mission_starttime").datetimepicker("setDate", new Date());
}

$('#createmissionModal').on('hidden.bs.modal', function () {
    window.location.reload();
});

$('#editmissionModal').on('hidden.bs.modal', function () {
    window.location.reload();
});


var CreateMission = function () {
    var form = $('#kt_create_mission_form');

    form.validate({
        rules: {
            create_mission_targeturl: {
                required: true
            }
        }
    });

    if (!form.valid()) {
        return;
    }

    if (document.getElementById("id_create_device_id").value == '') {
        swal.fire({
            "title": "",
            "text": "请选择设备.",
            "type": "error",
            "confirmButtonClass": "btn btn-secondary kt-btn kt-btn--wide",
        });
    } else {
        $.ajax({
            type: "POST",
            url: $("#create_url").text(),
            data: {
                csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                targeturl: document.getElementById("id_create_mission_targeturl").value,
                starttime: document.getElementById("id_create_mission_starttime").value,
                interval: document.getElementById("id_create_mission_interval").value,
                lasttime: document.getElementById("id_create_mission_lasttime").value,
                commenttext: document.getElementById("id_create_commenttext").value,
                commenttimes: document.getElementById("id_create_mission_commenttimes").value,         
                deviceid: document.getElementById("id_create_device_id").value,     
                missionincome: document.getElementById("id_create_mission_missionincome").value,                                  
            },
            success: function (response, status, xhr, $form) {
                if (response != 'Error') {
                    window.location.href = response;
                }
            }
        })
    }
}

var initDeviceModal = function () {
    var deviceopitons = {
        'isinit': document.getElementById("id_create_mission_divice").value == ''
    }
    $('#diviceModal').deviceDatatable(deviceopitons);
}

var initSearch = function () {
    //任务状态
    $("[name='statusBtn']").click(function () {
        if ($(this).hasClass('btn-outline-hover-primary')) {
            var count = $("[name='statusBtn']").length
            $(this).removeClass('btn-outline-hover-primary')
            $(this).addClass('btn-primary')
            $("[name='statusBtnAll']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            if ($("#status .btn-primary").length == count) {
                $("[name='statusBtnAll']").removeClass('btn-outline-hover-primary').addClass('btn-primary')
                $("[name='statusBtn']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            }
            getStatusSearch()
        } else if ($(this).hasClass('btn-primary')) {
            $(this).removeClass('btn-primary')
            $(this).addClass('btn-outline-hover-primary')
            if ($("#status .btn-primary").length == 0) {
                $("[name='statusBtnAll']").removeClass('btn-outline-hover-primary').addClass('btn-primary')
            }
            getStatusSearch()
        }
    })
    $("[name='statusBtnAll']").click(function () {
        if ($(this).hasClass('btn-outline-hover-primary')) {
            $(this).removeClass('btn-outline-hover-primary')
            $(this).addClass('btn-primary')
            $("[name='statusBtn']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            getStatusSearch()
        }
    })
}

var getStatusSearch = function () {
    var statusSearch = ''
    if ($("[name='statusBtnAll']").hasClass('btn-primary')) {
        statusSearch = ''
    } else {
        var list = $("#status .btn-primary")
        for (var i = 0; i < list.length; i++) {
            var per = list[i]
            statusSearch = statusSearch + per.value + ','
        }
    }
    search('watchlivemissionstatus', statusSearch)
}

var search = function (param, value) {
    var datatable = $('#datatable_WatchLiveMission').KTDatatable()
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

function convertDateFromString(dateString) {
    if (dateString) {
        var arr1 = dateString.split(" ");
        var sdate = arr1[0].split('-');
        var stime = arr1[1].split(':');
        var date = new Date(sdate[0], sdate[1] - 1, sdate[2], stime[0], stime[1], stime[2]);
        return date;
    }
}

function getInervalHour(startDate, endDate) {
    var ms = endDate.getTime() - startDate.getTime();
    if (ms < 0) return 0;
    return Math.floor(ms / 1000 / 60 / 60);
}