"use strict";
// Class definition

var old_devide_id = ''

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
            width: 20,
        }, {
            field: 'Subscriber__username',
            title: '代理名称',
            autoHide: false,
            sortable: false,
        }, {
            field: 'mobilephoneid',
            title: '设备',
            autoHide: false,
            sortable: false,
            template: function (row) {
                if (row.mobilephoneid == null) {
                    return ''
                } else {
                    var mobilephoneid_list = row.mobilephoneid.split(',');
                    var html = '';
                    for (var i = 0; i < mobilephoneid_list.length; i++) {
                        var per_id = mobilephoneid_list[i]
                        html = html + '\
                        <a href="javascript:void(0);" class="kt-link kt-font-bold kt-margin-t-5" \
                        data-mobilephone-id=' + per_id + '>' + per_id + '</a> \
                        ' + ','
                    };
                    html = html.substring(0, html.length - 1);
                    return html
                }
            }
        }, {
            field: 'UserSystemPercent',
            title: '系统提成%',
            autoHide: false,
            sortable: false,
            width: 50,
        }, {
            field: 'UserALevel__username',
            title: '上级代理名称',
            autoHide: false,
            sortable: false,
            width: 50,
            template: function (row) {
                if (row.UserALevel__username == null) {
                    return ''
                } else {
                    return '\
                    <a href="javascript:void(0);" class="kt-link kt-font-bold kt-margin-t-5" \
                    data-alevel-name=' + row.UserALevel__username + '>' + row.UserALevel__username + '</a> \
                    '
                }
            }
        }, {
            field: 'UserALevelPercent',
            title: '上级代理提成%',
            autoHide: false,
            sortable: false,
            template: function (row) {
                if (row.UserALevel__username == null) {
                    return ''
                } else {
                    return row.UserALevelPercent
                }
            },
            width: 50,
        }, {
            field: 'UserBLevel__username',
            title: '上上级代理名称',
            autoHide: false,
            sortable: false,
            width: 50,
            template: function (row) {
                if (row.UserBLevel__username == null) {
                    return ''
                } else {
                    return '\
                    <a href="javascript:void(0);" class="kt-link kt-font-bold kt-margin-t-5" \
                    data-blevel-name=' + row.UserBLevel__username + '>' + row.UserBLevel__username + '</a> \
                    '
                }
            }
        }, {
            field: 'UserBLevelPercent',
            title: '上上级代理提成%',
            autoHide: false,
            sortable: false,
            template: function (row) {
                if (row.UserBLevel__username == null) {
                    return ''
                } else {
                    return row.UserBLevelPercent
                }
            },
            width: 50,
        }, {
            field: 'TodayPIDIncome',
            title: '今日推广预估收入',
            autoHide: false,
            sortable: false,
            width: 50,
        },{
            field: 'TodayMissionIncome',
            title: '今日任务预估收入',
            autoHide: false,
            sortable: false,
            width: 50,
        }, {
            field: 'CurrentMonthIncome',
            title: '本月预估收入',
            autoHide: false,
            sortable: false,
            width: 50,
        }, {
            field: 'LastMonthTruelyIncome',
            title: '上月实际收入',
            autoHide: false,
            sortable: false,
            width: 50,
        }, {
            field: 'Subscriber__money',
            title: '账户余额',
            autoHide: false,
            sortable: false,
            width: 50,
        }, {
            field: 'Actions',
            title: '操作',
            sortable: false,
            width: 110,
            overflow: 'visible',
            autoHide: false,
            textAlign: 'center',
            template: function (row) {
                return '\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="详情" data-edit-id="' + row.id + '">\
                        <i class="flaticon2-file"></i>\
                    </button>\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="订单信息" data-order-id="' + row.id + '">\
                        <i class="flaticon2-lorry"></i>\
                    </button>\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="推广详情" data-level-id="' + row.id + '">\
                        <i class="flaticon2-group"></i>\
                    </button>\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="重置密码" data-reset-id="' + row.id + '">\
                        <i class="flaticon2-lock"></i>\
                    </button>\
                ';
            },
        }],
    };

    // basic demo
    var localSelectorDemo = function () {

        options.search = {
            input: $('#generalAgentSearch'),
            onEnter: true,
        };

        $('#agentlist_column').on('change', function () {
            datatable.search($(this).val().toLowerCase(), 'agentlistcolumn');
        });

        $('#agentlist_column').selectpicker();

        var datatable = $('#datatable_agent_list').KTDatatable(options);

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
                        KTDatatableDevice.init(id);
                        $('#editModal').modal('show');
                        document.getElementById("id_edit_Subscriber__username").value = response['username'];
                        document.getElementById("id_edit_UserSystemPercent").value = response['usersystempercent'];
                        document.getElementById("id_edit_UserALevel__username").value = response['alevelusername'];
                        if (response['alevelusername'] == '') {
                            $('#id_edit_UserALevelPercent').attr("disabled", true);
                        } else {
                            $('#id_edit_UserALevelPercent').attr("disabled", false);
                        }
                        document.getElementById("id_edit_UserALevelPercent").value = response['useralevelpercent'];
                        document.getElementById("id_edit_UserBLevel__username").value = response['blevelusername'];
                        if (response['blevelusername'] == '') {
                            $('#id_edit_UserBLevelPercent').attr("disabled", true);
                        } else {
                            $('#id_edit_UserBLevelPercent').attr("disabled", false);
                        }
                        document.getElementById("id_edit_UserBLevelPercent").value = response['userblevelpercent'];
                        document.getElementById("id_edit_divice").value = response['mobilephoneid'];
                        document.getElementById("id_edit_data_id").value = response['dataid'];
                        document.getElementById("id_edit_device_id").value = response['mobilephoneid'];
                        old_devide_id = response['mobilephoneid'];
                    }
                }
            });
        });

        datatable.on('click', '[data-alevel-name]', function () {
            var name = $(this).data('alevel-name');
            localStorage.setItem('jumpToAgentName', name);
            window.location.href = $("#agentdetail_url").text()
        });

        datatable.on('click', '[data-blevel-name]', function () {
            var name = $(this).data('blevel-name');
            localStorage.setItem('jumpToAgentName', name);
            window.location.href = $("#agentdetail_url").text()
        });

        datatable.on('click', '[data-mobilephone-id]', function () {
            var id = $(this).data('mobilephone-id');
            localStorage.setItem('jumpToMobilePhone', id);
            window.location.href = $("#devicemanage_url").text()
        });

        datatable.on('click', '[data-order-id]', function () {
            var agentid = $(this).data('order-id');
            $('#datatable_order').setOrderDatatableAgentID(agentid)
            $('#ordersModal').modal('show');
        });

        datatable.on('click', '[data-reset-id]', function () {
            var agentid = $(this).data('reset-id');
            swal.fire({
                title: '确认把该账号密码重置为【123456】?',
                text: "确认后无法撤销！",
                type: 'warning',
                showCancelButton: true,
                confirmButtonText: '是',
                cancelButtonText: '否'
            }).then(function (result) {
                if (result.value) {                   
                    $.ajax({
                        type: "POST",
                        url: $("#resetpassword_url").text(),
                        data: {
                            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                            id: agentid
                        },
                        success: function (response, status, xhr, $form) {
                            if (response != 'Error') {
                                swal.fire("", "重置成功！", "success");
                            }
                        }
                    });
                };
            })
        });


    };

    return {
        // public functions
        init: function (agentName) {
            localSelectorDemo(agentName);
        }
    };
}();

var KTDatatableDevice = function () {

    // Private functions
    var options = {
        // datasource definition
        data: {
            type: 'remote',
            source: {
                read: {
                    url: $("#device_data_url").text(),
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
            width: 20,
            selector: {
                class: 'kt-checkbox--solid'
            },
            textAlign: 'center',
        }, {
            field: 'id_show',
            title: 'ID',
            template: '{{id}}',
            autoHide: false,
            sortable: false,
        }, {
            field: 'Enable',
            title: '设备状态',
            autoHide: false,
            sortable: false,
            template: function (row) {
                var status = {
                    'true': {
                        'title': '启用',
                        'class': 'kt-badge--success'
                    },
                    'false': {
                        'title': '停用',
                        'class': ' kt-badge--danger'
                    },
                };
                return '<span class="kt-badge ' + status[row.Enable].class +
                    ' kt-badge--inline kt-badge--pill">' + status[row.Enable].title +
                    '</span>';
            },
        }, {
            field: 'IsOnline',
            title: '在线信息',
            autoHide: false,
            sortable: false,
            template: function (row) {
                var status = {
                    'true': {
                        'title': '在线',
                        'class': 'kt-badge--success'
                    },
                    'false': {
                        'title': '离线',
                        'class': ' kt-badge--danger'
                    },
                };
                return '<span class="kt-badge ' + status[row.IsOnline].class +
                    ' kt-badge--inline kt-badge--pill">' + status[row.IsOnline].title +
                    '</span>';
            },
        }, {
            field: 'tag',
            title: '标签',
            autoHide: false,
            sortable: false,
            template: function (row) {
                var cat = row.tag
                var cat_list = cat.split(',')
                if (cat_list != null && cat_list.length > 0) {
                    var html_string = ''
                    for (var i = 0; i < cat_list.length; i++) {
                        var per = cat_list[i]
                        html_string = html_string + ' ' +
                            '<span class="badge badge-primary">' + per +
                            '</span>';
                    }
                    return html_string
                } else {
                    return ''
                };
            }
        }, {
            field: 'TikTokAccount__Group__Name',
            title: '分组',
            autoHide: false,
            sortable: false,
            template: function (row) {
                if (row.TikTokAccount__Group__Name == null) {
                    return ''
                } else {
                    return '\
                    <span class="badge badge-primary">' + row.TikTokAccount__Group__Name + '</span>';
                }
            }
        }, {
            field: 'Remark',
            title: '备注',
            autoHide: false,
            sortable: false,
        }, {
            field: 'Agent__Subscriber__username',
            title: '代理名称',
            autoHide: false,
            sortable: false,
        }, {
            field: 'TikTokAccount__NickName',
            title: '抖音账号',
            autoHide: false,
            sortable: false,
        }, {
            field: 'TikTokAccount__ShowWindowExists',
            title: '电商',
            autoHide: false,
            sortable: false,
            width: 40,
            template: function (row) {
                var status = {
                    'true': {
                        'title': '是',
                        'class': 'kt-badge--success'
                    },
                    'false': {
                        'title': '否',
                        'class': ' kt-badge--danger'
                    },
                };
                if (row.TikTokAccount__ShowWindowExists == null) {
                    return ''
                } else {
                    return '<span class="kt-badge ' + status[row.TikTokAccount__ShowWindowExists].class +
                        ' kt-badge--inline kt-badge--pill">' + status[row.TikTokAccount__ShowWindowExists].title +
                        '</span>';
                }
            },
        }, ],
    };

    // basic demo
    var localSelectorDemo = function (agentid) {
        options.extensions = {
            checkbox: {},
        };

        options.search = {
            input: $('#generalDeviceSearch'),
            onEnter: true,
        };

        options.data.source.read.params = {
            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
            isagent: true,
            agentid: agentid,
        }

        $('#kt_device_column').on('change', function () {
            datatable.search($(this).val().toLowerCase(), 'devicecolumn');
        });

        $('#kt_device_column').selectpicker();

        var datatable = $('#modal_datatable_device').KTDatatable(options);

        datatable.on(
            'kt-datatable--on-check kt-datatable--on-uncheck kt-datatable--on-layout-updated',
            function (e) {
                var ids = datatable.checkbox().getSelectedId();
                var count = ids.length;
                $('#kt_datatable_device_selected_number').html(count);
                if (count > 0) {
                    $("#kt_datatable_device_select_all").attr("disabled", false);
                } else {
                    $("#kt_datatable_device_select_all").attr("disabled", true);
                }
            });


        $('#kt_datatable_device_select_all').on('click', function () {
            var ids = datatable.checkbox().getSelectedId();
            var id_string = ''
            for (var i = 0; i < ids.length; i++) {
                id_string = id_string + ids[i] + ','
            }
            $.ajax({
                type: "POST",
                url: $("#getdevicenamebyids_url").text(),
                data: {
                    csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                    ids: id_string
                },
                success: function (response, status, xhr, $form) {
                    if (response != 'Error') {
                        $('#diviceModal').modal('hide');
                        document.getElementById("id_edit_divice").value = response['ids'];
                        document.getElementById("id_edit_device_id").value = response['ids'];
                    }
                }
            });
        });

        // fix datatable layout after modal shown
        var modal = $('#diviceModal');
        datatable.hide();
        var alreadyReloaded = false;
        var alreadyInitSelect = false;
        modal.on('shown.bs.modal', function () {
            if (!alreadyReloaded) {
                var modalContent = $(this).find('.modal-content');
                datatable.spinnerCallback(true, modalContent);

                datatable.reload();

                datatable.on('kt-datatable--on-layout-updated', function () {
                    if (!alreadyInitSelect) {
                        if (document.getElementById("id_edit_device_id").value != '') {
                            var storage = {};
                            storage['selectedRows'] = document.getElementById("id_edit_device_id").value.split(',')
                            storage['unselectedRows'] = []
                            localStorage.setItem('modal_datatable_device-1-checkbox', JSON.stringify(storage));
                        }
                    }
                    datatable.show();
                    datatable.spinnerCallback(false, modalContent);
                    datatable.redraw();
                });

                alreadyReloaded = true;
            }
        });

    };



    return {
        // public functions
        init: function (agentid) {
            localSelectorDemo(agentid);
        }
    };
}();

var PromotionChart = function () {
    let myBarChartMoney;
    let myBarChartOrder;

    var initChart = function () {
        var barChartDataMoney = {
            labels: ['今日', '昨日', '最近7日', '本月', '上月'],
            datasets: [{
                label: '代理贡献预估收入',
                backgroundColor: '#6e4ff5',
                borderColor: '#6e4ff5',
                borderWidth: 1,
                data: [0, 0, 0, 0, 0],
            }]

        };

        var barChartDataOrder = {
            labels: ['今日', '昨日', '最近7日', '本月', '上月'],
            datasets: [{
                label: '代理贡献预估订单量',
                backgroundColor: '#f6aa33',
                borderColor: '#f6aa33',
                borderWidth: 1,
                data: [0, 0, 0, 0, 0],
            }]

        };

        var ctxMoney = $('#promotion_chart_money');
        myBarChartMoney = new Chart(ctxMoney, {
            type: 'bar',
            data: barChartDataMoney,
            options: {
                responsive: true,
                legend: {
                    position: 'top',
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        },
                    }],
                },
                hover: {
                    animationDuration: 0 // 防止鼠标移上去，数字闪烁
                },
                animation: { // 这部分是数值显示的功能实现
                    onComplete: function () {
                        var chartInstance = this.chart,
                        ctx = chartInstance.ctx;
                        // 以下属于canvas的属性（font、fillStyle、textAlign...）
                        ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);
                        ctx.fillStyle = "black";
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'bottom';

                        this.data.datasets.forEach(function (dataset, i) {
                            var meta = chartInstance.controller.getDatasetMeta(i);
                            meta.data.forEach(function (bar, index) {
                                var data = dataset.data[index];
                                ctx.fillText(data, bar._model.x, bar._model.y - 5);
                            });
                        });
                    }
                }
            }
        });

        var ctxOrder = $('#promotion_chart_order');
        myBarChartOrder = new Chart(ctxOrder, {
            type: 'bar',
            data: barChartDataOrder,
            options: {
                responsive: true,
                legend: {
                    position: 'top',
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        },
                    }],
                },
                hover: {
                    animationDuration: 0 // 防止鼠标移上去，数字闪烁
                },
                animation: { // 这部分是数值显示的功能实现
                    onComplete: function () {
                        var chartInstance = this.chart,
                        ctx = chartInstance.ctx;
                        // 以下属于canvas的属性（font、fillStyle、textAlign...）
                        ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);
                        ctx.fillStyle = "black";
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'bottom';

                        this.data.datasets.forEach(function (dataset, i) {
                            var meta = chartInstance.controller.getDatasetMeta(i);
                            meta.data.forEach(function (bar, index) {
                                var data = dataset.data[index];
                                ctx.fillText(data, bar._model.x, bar._model.y - 5);
                            });
                        });
                    }
                }
            }
        });

    }

    var updateData = function (data) {
        myBarChartMoney.data.datasets[0].data[0] = data['todaymoney'];
        myBarChartMoney.data.datasets[0].data[1] = data['yestodaymoney'];
        myBarChartMoney.data.datasets[0].data[2] = data['sevendaysmoney'];
        myBarChartMoney.data.datasets[0].data[3] = data['currentmonthmoney'];
        myBarChartMoney.data.datasets[0].data[4] = data['lastmonthmoney'];
        myBarChartOrder.data.datasets[0].data[0] = data['todayordercount'];
        myBarChartOrder.data.datasets[0].data[1] = data['yestodayordercount'];
        myBarChartOrder.data.datasets[0].data[2] = data['sevendaysordercount'];
        myBarChartOrder.data.datasets[0].data[3] = data['currentmonthordercount'];
        myBarChartOrder.data.datasets[0].data[4] = data['lastmonthordercount'];
        myBarChartMoney.update();
        myBarChartOrder.update();
    }

    return {
        // public functions
        init: function () {
            initChart();
        },
        updateData: function (data) {
            updateData(data);
        }
    };
}();

jQuery(document).ready(function () {
    KTDatatableRecordSelectionDemo.init()
    $('#modal-order-datatable').orderDatatable();
    PromotionChart.init()
    initSearch();
})

var initSearch = function () {
    //状态
    $("[name='statusBtn']").click(function () {
        if ($(this).hasClass('btn-outline-hover-primary')) {
            $("[name='statusBtn']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            $(this).removeClass('btn-outline-hover-primary')
            $(this).addClass('btn-primary')
            getStatusSearch()
        }
    })
    //是否在线
    $("[name='isonlineBtn']").click(function () {
        if ($(this).hasClass('btn-outline-hover-primary')) {
            $("[name='isonlineBtn']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            $(this).removeClass('btn-outline-hover-primary')
            $(this).addClass('btn-primary')
            getIsonlineSearch()
        }
    })
    //标签
    $("[name='tagBtn']").click(function () {
        if ($(this).hasClass('btn-outline-hover-primary')) {
            var count = $("[name='tagBtn']").length
            $(this).removeClass('btn-outline-hover-primary')
            $(this).addClass('btn-primary')
            $("[name='tagBtnAll']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            if ($("#tag .btn-primary").length == count) {
                $("[name='tagBtnAll']").removeClass('btn-outline-hover-primary').addClass('btn-primary')
                $("[name='tagBtn']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            }
            getTagSearch()
        } else if ($(this).hasClass('btn-primary')) {
            $(this).removeClass('btn-primary')
            $(this).addClass('btn-outline-hover-primary')
            if ($("#tag .btn-primary").length == 0) {
                $("[name='tagBtnAll']").removeClass('btn-outline-hover-primary').addClass('btn-primary')
            }
            getTagSearch()
        }
    })
    $("[name='tagBtnAll']").click(function () {
        if ($(this).hasClass('btn-outline-hover-primary')) {
            $(this).removeClass('btn-outline-hover-primary')
            $(this).addClass('btn-primary')
            $("[name='tagBtn']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            getTagSearch()
        }
    })
    //分组
    $("[name='groupBtn']").click(function () {
        if ($(this).hasClass('btn-outline-hover-primary')) {
            var count = $("[name='groupBtn']").length
            $(this).removeClass('btn-outline-hover-primary')
            $(this).addClass('btn-primary')
            $("[name='groupBtnAll']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            if ($("#group .btn-primary").length == count) {
                $("[name='groupBtnAll']").removeClass('btn-outline-hover-primary').addClass('btn-primary')
                $("[name='groupBtn']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            }
            getGroupSearch()
        } else if ($(this).hasClass('btn-primary')) {
            $(this).removeClass('btn-primary')
            $(this).addClass('btn-outline-hover-primary')
            if ($("#group .btn-primary").length == 0) {
                $("[name='groupBtnAll']").removeClass('btn-outline-hover-primary').addClass('btn-primary')
            }
            getGroupSearch()
        }
    })
    $("[name='groupBtnAll']").click(function () {
        if ($(this).hasClass('btn-outline-hover-primary')) {
            $(this).removeClass('btn-outline-hover-primary')
            $(this).addClass('btn-primary')
            $("[name='groupBtn']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            getGroupSearch()
        }
    })
    //状态
    $("[name='orderStatusBtn']").click(function () {
        if ($(this).hasClass('btn-outline-hover-primary')) {
            var count = $("[name='orderStatusBtn']").length
            $(this).removeClass('btn-outline-hover-primary')
            $(this).addClass('btn-primary')
            $("[name='orderStatusBtnAll']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            if ($("#orderStatus .btn-primary").length == count) {
                $("[name='orderStatusBtnAll']").removeClass('btn-outline-hover-primary').addClass('btn-primary')
                $("[name='orderStatusBtn']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            }
            getOrderStatusSearch()
        } else if ($(this).hasClass('btn-primary')) {
            $(this).removeClass('btn-primary')
            $(this).addClass('btn-outline-hover-primary')
            if ($("#orderStatus .btn-primary").length == 0) {
                $("[name='orderStatusBtnAll']").removeClass('btn-outline-hover-primary').addClass('btn-primary')
            }
            getOrderStatusSearch()
        }
    })
    $("[name='orderStatusBtnAll']").click(function () {
        if ($(this).hasClass('btn-outline-hover-primary')) {
            $(this).removeClass('btn-outline-hover-primary')
            $(this).addClass('btn-primary')
            $("[name='orderStatusBtn']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            getOrderStatusSearch()
        }
    })
    //创建时间
    $("[name='createtimeBtn']").click(function () {
        if ($(this).hasClass('btn-outline-hover-primary')) {
            var count = $("[name='createtimeBtn']").length
            $(this).removeClass('btn-outline-hover-primary')
            $(this).addClass('btn-primary')
            $("[name='createtimeBtnAll']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            if ($("#createtime .btn-primary").length == count) {
                $("[name='createtimeBtnAll']").removeClass('btn-outline-hover-primary').addClass('btn-primary')
                $("[name='createtimeBtn']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            }
            getCreateTimeSearch()
        } else if ($(this).hasClass('btn-primary')) {
            $(this).removeClass('btn-primary')
            $(this).addClass('btn-outline-hover-primary')
            if ($("#createtime .btn-primary").length == 0) {
                $("[name='createtimeBtnAll']").removeClass('btn-outline-hover-primary').addClass('btn-primary')
            }
            getCreateTimeSearch()
        }
    })
    $("[name='createtimeBtnAll']").click(function () {
        if ($(this).hasClass('btn-outline-hover-primary')) {
            $(this).removeClass('btn-outline-hover-primary')
            $(this).addClass('btn-primary')
            $("[name='createtimeBtn']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            getCreateTimeSearch()
        }
    })
}

var initeditmodal = function () {
    document.getElementById("id_edit_Subscriber__username").value = '';
    document.getElementById("id_edit_UserSystemPercent").value = '';
    document.getElementById("id_edit_UserALevel__username").value = '';
    document.getElementById("id_edit_UserALevelPercent").value = '';
    document.getElementById("id_edit_UserBLevel__username").value = '';
    document.getElementById("id_edit_UserBLevelPercent").value = '';
    document.getElementById("id_edit_divice").value = '';
    document.getElementById("id_edit_data_id").value = '';
    document.getElementById("id_edit_device_id").value = '';
}

$('#editModal').on('hidden.bs.modal', function () {
    var datatable = $('#datatable_agent_list').KTDatatable()
    datatable.load()
});

var EditAgent = function () {
    $.ajax({
        type: "POST",
        url: $("#edit_url").text(),
        data: {
            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
            UserSystemPercent: document.getElementById("id_edit_UserSystemPercent").value,
            UserALevelPercent: document.getElementById("id_edit_UserALevelPercent").value,
            UserBLevelPercent: document.getElementById("id_edit_UserBLevelPercent").value,
            id: document.getElementById("id_edit_data_id").value,
            deviceid: document.getElementById("id_edit_device_id").value,
        },
        success: function (response, status, xhr, $form) {
            if (response != 'Error') {
                $('#editModal').modal('hide');
                var datatable = $('#datatable_agent_list').KTDatatable()
                datatable.load()
            }
        }
    })
}

var getStatusSearch = function () {
    var statusSearch = $("#status .btn-primary")[0].value
    search('device_status', statusSearch)
}

var getIsonlineSearch = function () {
    var isonlineSearch = $("#isonline .btn-primary")[0].value
    search('isonline', isonlineSearch)
}

var getTagSearch = function () {
    var tagSearch = ''
    if ($("[name='tagBtnAll']").hasClass('btn-primary')) {
        tagSearch = ''
    } else {
        var list = $("#tag .btn-primary")
        for (var i = 0; i < list.length; i++) {
            var per = list[i]
            tagSearch = tagSearch + per.value + ','
        }
    }
    search('tag', tagSearch)
}

var getGroupSearch = function () {
    var groupSearch = ''
    if ($("[name='groupBtnAll']").hasClass('btn-primary')) {
        groupSearch = ''
    } else {
        var list = $("#group .btn-primary")
        for (var i = 0; i < list.length; i++) {
            var per = list[i]
            groupSearch = groupSearch + per.value + ','
        }
    }
    search('group', groupSearch)
}

var search = function (param, value) {
    var datatable = $('#modal_datatable_device').KTDatatable()
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