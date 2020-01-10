"use strict";
// Class definition

var KTDatatableSignatureManage = function () {

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
            scroll: true, // enable/disable datatable scroll both horizontal and
            // vertical when needed.
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

        search: {
            input: $('#generalSignatureManageSearch'),
            onEnter: true,
        },

        // columns definition

        columns: [{
            field: 'id',
            title: 'ID',
            sortable: false,
            autoHide: false,
            width: 20,
            selector: {
                class: 'kt-checkbox--solid'
            },
            textAlign: 'center',
        }, {
            field: 'mobilephone__id',
            title: '设备ID',
            autoHide: false,
            sortable: false,
            width: 40,
            template: function (row) {
                if (row.mobilephone__id == null) {
                    return ''
                } else {
                    return '\
                    <a href="javascript:void(0);" class="kt-link kt-font-bold kt-margin-t-5" \
                    data-mobilephone-id=' + row.mobilephone__id + '>' + row.mobilephone__id + '</a> \
                    '
                }
            }
        }, {
            field: 'NickName',
            title: '抖音账号',
            autoHide: false,
            sortable: false,
            template: function (row) {
                if (row.NickName == null) {
                    return ''
                } else {
                    return '\
                    <a href="javascript:void(0);" class="kt-link kt-font-bold kt-margin-t-5" \
                    data-tiktokaccount-name=' + row.NickName + '>' + row.NickName + '</a> \
                    '
                }
            }
        }, {
            field: 'Group__Name',
            title: '分组',
            autoHide: false,
            sortable: false,
            template: function (row) {
                if (row.Group__Name == null) {
                    return ''
                } else {
                    return '\
                    <span class="badge badge-primary">' + row.Group__Name + '</span>';
                }
            }
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
            field: 'Actions',
            title: '操作',
            sortable: false,
            width: 110,
            overflow: 'visible',
            autoHide: false,
            textAlign: 'center',
            template: function (row) {
                if (row.mobilephone__id == null) {
                    return ''
                } else {
                    if (row.NewDescribe == null || row.NewDescribe == '') {
                        return '\
                        <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="新建任务" data-edit-id="' + row.id + '">\
                            <i class="flaticon2-send-1"></i>\
                        </button>\
                        ';
                    } else {
                        return ''
                    }
                }
            },
        }],
    };

    // basic demo
    var localSelectorDemo = function () {

        options.extensions = {
            checkbox: {},
        };

        $('#kt_signaturemanage_column').on('change', function () {
            datatable.search($(this).val().toLowerCase(), 'signaturemanagecolumn');
        });

        $('#kt_signaturemanage_column').selectpicker();

        var datatable = $('#datatable_signature_manage').KTDatatable(options);

        datatable.on(
            'kt-datatable--on-check kt-datatable--on-uncheck kt-datatable--on-layout-updated',
            function (e) {
                var ids = datatable.checkbox().getSelectedId();
                var count = ids.length;
                $('#kt_datatable_selected_number').html(count);
                if (count > 0) {
                    $('#kt_datatable_group_action_form').collapse('show');
                    $("#kt_datatable_create_mission_all").attr("disabled", false);
                } else {
                    $('#kt_datatable_group_action_form').collapse('hide');
                    $("#kt_datatable_create_mission_all").attr("disabled", true);
                }
            });

        datatable.on('click', '[data-edit-id]', function () {
            var id = $(this).data('edit-id');
            initcreatemodal();
            $.ajax({
                type: "POST",
                url: $("#get_by_id_url").text(),
                data: {
                    csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                    id: id
                },
                success: function (response, status, xhr, $form) {
                    if (response != 'Error') {
                        $('#createModal').modal('show');
                        document.getElementById("id_edit_account_data_id").value = response['dataid'];
                        document.getElementById("id_edit_device_id").value = response['deviceid'];
                        document.getElementById("id_create_nickname").value = response['nickname'];
                        document.getElementById("id_create_old_signature").value = response['describe'];
                        document.getElementById("id_create_new_signature").value = response['newdescribe'];
                    }
                }
            });
        });

        datatable.on('click', '[data-mobilephone-id]', function () {
            var id = $(this).data('mobilephone-id');
            localStorage.setItem('jumpToMobilePhone', id);
            window.location.href = $("#devicemanage_url").text()
        });

        datatable.on('click', '[data-tiktokaccount-name]', function () {
            var name = $(this).data('tiktokaccount-name');
            localStorage.setItem('jumpToTikTokAccounttName', name);
            window.location.href = $("#acountlist_url").text()
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
    KTDatatableSignatureManage.init();
    $('.select2-container').width('100%');
    initSearch();
});

var CreateChangeSignatureMission = function () {
    $.ajax({
        type: "POST",
        url: $("#create_mission_url").text(),
        data: {
            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
            id: document.getElementById("id_edit_account_data_id").value,
            deviceid: document.getElementById("id_edit_device_id").value,
            newdescribe: document.getElementById("id_create_new_signature").value,
        },
        success: function (response, status, xhr, $form) {
            if (response != 'Error') {
                $('#createModal').modal('hide');
                var datatable = $('#datatable_signature_manage').KTDatatable()
                datatable.load()
            }
        }
    })
}

var MutiCreateChangeSignatureMission = function () {
    var datatable = $('#datatable_signature_manage').KTDatatable()
    var ids = datatable.checkbox().getSelectedId();
    var idstring = '';
    for (var i = 0; i < ids.length; i++) {
        idstring = idstring + ids[i] + ','
    }
    $.ajax({
        type: "POST",
        url: $("#muti_create_mission_url").text(),
        data: {
            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
            accountids: idstring,
            newdescribe: document.getElementById("id_muti_create_new_signature").value,
        },
        success: function (response, status, xhr, $form) {
            if (response != 'Error') {
                $('#muticreateModal').modal('hide');
                var datatable = $('#datatable_signature_manage').KTDatatable()
                datatable.load()
            }
        }
    })
}

var initcreatemodal = function () {
    document.getElementById("id_edit_account_data_id").value = '';
    document.getElementById("id_edit_device_id").value = '';
    document.getElementById("id_create_nickname").value = '';
    document.getElementById("id_create_old_signature").value = '';
    document.getElementById("id_create_new_signature").value = '';
}

var initmuticreatemodal = function () {
    document.getElementById("id_muti_create_new_signature").value = '';
    $('#muticreateModal').modal('show');
}

$('#createModal').on('hidden.bs.modal', function () {
    var datatable = $('#datatable_signature_manage').KTDatatable()
    datatable.load()
});

var initSearch = function () {
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
    var datatable = $('#datatable_signature_manage').KTDatatable()
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