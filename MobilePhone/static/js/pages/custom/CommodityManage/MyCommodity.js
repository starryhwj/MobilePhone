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
            width: 20,
            selector: {
                class: 'kt-checkbox--solid'
            },
            textAlign: 'center',
        }, {
            field: 'id_show',
            title: 'ID',
            autoHide: false,
            sortable: false,
            width: 30,
            template: function (row) {
                return '\
                <a href="javascript:void(0);" class="kt-link kt-font-bold kt-margin-t-5" \
                data-commodity-id=' + row.id + '>' + row.id + '</a> \
                '
            },
        }, {
            field: 'pic1',
            title: '缩略图',
            autoHide: false,
            sortable: false,
            template: function (row) {
                return '\
                    <a class="kt-media kt-media--xl">\
					    <img src= "' + row.Pic1 + '" alt="image">\
					</a>\
                ';
            }
        }, {
            field: 'Title',
            title: '标题',
            autoHide: false,
            sortable: false,
        }, {
            field: 'SubTitle',
            title: '短标题',
            autoHide: false,
            sortable: false,
        }, {
            field: 'CategoryString',
            title: '类型',
            autoHide: false,
            sortable: false,
            template: function (row) {
                var cat = row.CategoryString
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
            },
        }, {
            field: 'CreateTime',
            title: '创建日期',
            type: 'date',
            format: 'MM/DD/YYYY',
        }, {
            field: 'Price',
            title: '售价',
            autoHide: false,
        }, {
            field: 'Sales',
            title: '销量',
            autoHide: false,
        }, {
            field: 'CommissionPercent',
            title: '提成比例',
            autoHide: false,
        }, {
            field: 'Unused',
            title: '未使用视频量',
            sortable: false,
        }, {
            field: 'Actions',
            title: '操作',
            sortable: false,
            width: 90,
            overflow: 'visible',
            autoHide: false,
            textAlign: 'center',
            template: function (row) {
                return '\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="批量上传视频" data-video-id="' + row.id + '">\
                        <i class="flaticon-upload"></i>\
                    </button>\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="批量发布任务" data-mission-id="' + row.id + '">\
                        <i class="flaticon2-send-1"></i>\
                    </button>\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="详情" data-edit-id="' + row.id + '">\
                        <i class="flaticon2-file"></i>\
                    </button>\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="删除" data-delete-id="' + row.id + '">\
                        <i class="flaticon2-delete"></i>\
                    </button>\
                ';
            },
        }],
    };

    // basic demo
    var localSelectorDemo = function () {

        options.search = {
            input: $('#generalCommoditySearch'),
            onEnter: true,
        };

        var datatable = $('#datatable_mycommodity').KTDatatable(options);

        $('#id_create_mission_starttime').datetimepicker({
            todayHighlight: true,
            autoclose: true,
            pickerPosition: 'bottom-left',
            format: 'yyyy-mm-dd hh:ii:00',
            clearBtn: true,
            todayBtn: true,
            language: 'zh-CN',
        });

        $('#kt_datatable_delete_all').on('click', function () {
            swal.fire({
                title: '确认删除?',
                text: "确认后无法撤销！",
                type: 'warning',
                showCancelButton: true,
                confirmButtonText: '是',
                cancelButtonText: '否'
            }).then(function (result) {
                if (result.value) {
                    // select active rows
                    datatable.rows('.kt-datatable__row--active');
                    // check selected nodes
                    if (datatable.nodes().length > 0) {
                        // get column by field name and get the column nodes
                        var ids = datatable.rows('.kt-datatable__row--active').
                        nodes().
                        find('.kt-checkbox--single > [type="checkbox"]').
                        map(function (i, chk) {
                            return $(chk).val();
                        });
                        var idstring = '';
                        for (var i = 0; i < ids.length; i++) {
                            idstring = idstring + ids[i] + ','
                        }
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
                    }
                };
            })
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
                        $('#editModal').modal('show');
                        document.getElementById("id_edit_pic1").src = response['pic1'];
                        document.getElementById("id_edit_pic2").src = (response['pic2'] == null ? '' : response['pic2']);
                        document.getElementById("id_edit_pic3").src = (response['pic3'] == null ? '' : response['pic3']);
                        document.getElementById("id_edit_pic4").src = (response['pic4'] == null ? '' : response['pic4']);
                        document.getElementById("id_edit_pic5").src = (response['pic5'] == null ? '' : response['pic5']);
                        document.getElementById("id_edit_url").value = response['url'];
                        document.getElementById("id_edit_title").value = response['title'];
                        document.getElementById("id_edit_subtitle").value = response['subtitle'];
                        document.getElementById("id_edit_price").value = response['price'];
                        document.getElementById("id_edit_sales").value = response['sales'];
                        document.getElementById("id_edit_commissionpercent").value = response['commissionpercent'];
                        document.getElementById("id_edit_outsideplatformid").value = response['outsideplatformid'];
                        document.getElementById("id_data_id").value = response['dataid'];
                        var categoryId = response['categoryid'];
                        var categoryIdList = categoryId.split(',')
                        var select = document.getElementById('id_edit_category');
                        for (var i = 0; i < categoryIdList.length; i++) {
                            var checkValue = categoryIdList[i]
                            for (var j = 0; j < select.options.length; j++) {
                                if (select.options[j].value == checkValue) {
                                    select.options[j].selected = true;
                                    break;
                                }
                            }
                        }
                        $('#id_edit_category').select2({
                            placeholder: "选择类别",
                        });
                        $('.select2-container').width('100%');
                    }
                }
            });
        });

        datatable.on('click', '[data-video-id]', function () {
            var goodid = $(this).data('video-id');
            initvideomodal(goodid);
            $('#uploadVideoModal').modal('show');
        });

        datatable.on('click', '[data-mission-id]', function () {
            var id = $(this).data('mission-id');
            initmissionmodal();
            $.ajax({
                type: "POST",
                url: $("#get_by_id_url").text(),
                data: {
                    csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                    id: id
                },
                success: function (response, status, xhr, $form) {
                    if (response != 'Error') {
                        $('#missionModal').modal('show');
                        document.getElementById("id_commodity_mission_id").value = response['dataid'];
                        document.getElementById("id_mission_good").value = response['title'];
                    }
                }
            });
        });

        datatable.on('click', '[data-commodity-id]', function () {
            var commodityid = $(this).data('commodity-id');
            localStorage.setItem('jumpToCommodityDataAnalysisID', commodityid);
            window.location.href = $("#commoditydataanalysis_url").text()
        });


        datatable.on(
            'kt-datatable--on-check kt-datatable--on-uncheck kt-datatable--on-layout-updated',
            function (e) {
                var checkedNodes = datatable.rows('.kt-datatable__row--active').nodes();
                var count = checkedNodes.length;
                $('#kt_datatable_selected_number').html(count);
                if (count > 0) {
                    $('#kt_datatable_group_action_form').collapse('show');
                } else {
                    $('#kt_datatable_group_action_form').collapse('hide');
                }
            });

        $('#kt_modal_fetch_id').on('show.bs.modal', function (e) {
            var ids = datatable.rows('.kt-datatable__row--active').
            nodes().
            find('.kt-checkbox--single > [type="checkbox"]').
            map(function (i, chk) {
                return $(chk).val();
            });
            var c = document.createDocumentFragment();
            for (var i = 0; i < ids.length; i++) {
                var li = document.createElement('li');
                li.setAttribute('data-id', ids[i]);
                li.innerHTML = 'Selected record ID: ' + ids[i];
                c.appendChild(li);
            }
            $(e.target).find('.kt_datatable_selected_ids').append(c);
        }).on('hide.bs.modal', function (e) {
            $(e.target).find('.kt_datatable_selected_ids').empty();
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
    $('#id_category').select2({
        placeholder: "选择类别",
    });
    $('#id_edit_category').select2({
        placeholder: "选择类别",
    });
    $('#id_video_category').select2({
        placeholder: "选择类别",
    });
    $('.select2-container').width('100%');
});

var initdropzone = function () {
    // set the dropzone container id
    var id = '#kt_dropzone_5';

    // set the preview element template
    var previewNode = $(id + " .dropzone-item");
    previewNode.id = "";
    var previewTemplate = previewNode.parent('.dropzone-items').html();
    previewNode.remove();

    var myDropzone5 = new Dropzone(id, { // Make the whole body a dropzone
        url: $("#upload_url").text(),
        timeout: 30000000,
        parallelUploads: 20,
        maxFiles: 50,
        maxFilesize: 50, // Max filesize in MB
        acceptedFiles: ".mp4,.avi",
        previewTemplate: previewTemplate,
        previewsContainer: id + " .dropzone-items", // Define the container to display the previews
        clickable: id + " .dropzone-select", // Define the element that should be used as click trigger to select files.
        params: {
            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
            guid: document.getElementById("id_guid").value,
        },
        renameFile: function (file) {
            if (file.type == 'video/mp4') {
                return guid() + '.mp4'
            } else {
                return guid() + '.avi'
            }
        },
        dictDefaultMessage: '拖动文件至此或者点击上传',
        dictMaxFilesExceeded: "最多只能上传50个文件！请把多余文件删除！",
        dictResponseError: '文件上传失败!',
        dictInvalidFileType: "文件类型只能是*.mp4和*.avi",
        dictFallbackMessage: "浏览器不受支持",
        dictFileTooBig: "文件大小超过限制",
        dictRemoveLinks: "删除",
        dictCancelUpload: "取消",
    });

    myDropzone5.on("addedfile", function (file) {
        // Hookup the start button
        $(document).find(id + ' .dropzone-item').css('display', '');
    });

    // Update the total progress bar
    myDropzone5.on("totaluploadprogress", function (progress) {
        if (document.querySelector('#kt_dropzone_5' + " .progress-bar") != null) {
            document.querySelector(id + " .progress-bar").style.width = progress + "%";
        } else {
            $("#id_save_video").attr("disabled", true);
        }
    });

    myDropzone5.on("sending", function (file) {
        // Show the total progress bar when upload starts
        document.querySelector(id + " .progress-bar").style.opacity = "1";
    });

    // Hide the total progress bar when nothing's uploading anymore
    myDropzone5.on("complete", function (progress) {
        var thisProgressBar = id + " .dz-complete";
        setTimeout(function () {
            $(thisProgressBar + " .progress-bar, " + thisProgressBar + " .progress").css('opacity', '0');
        }, 300)
        $("#id_save_video").removeAttr("disabled");
    });

    myDropzone5.on("removedfile", function (file) {
        $.ajax({
            type: "POST",
            url: $("#remove_upload_url").text(),
            data: {
                csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                uuid: file.upload.filename,
            },
            success: function (response, status, xhr, $form) {

            }
        })        
    });
}

var initvideomodal = function (goodid) {
    document.getElementById("id_commodity_id").value = goodid;
    document.getElementById("id_video_title").value = '';
    document.getElementById("id_video_remark").value = '';
    document.getElementById("id_create_video_keyword").value = '';
    document.getElementById("id_guid").value = guid();
    var select = document.getElementById('id_video_category');
    for (var j = 0; j < select.options.length; j++) {
        select.options[j].selected = false;
    }
    initdropzone()
}

var initmissionmodal = function () {
    document.getElementById("id_commodity_mission_id").value = '';
    document.getElementById("id_mission_good").value = '';
    document.getElementById("id_create_mission_divice").value = '';
    document.getElementById("id_create_device_id").value = '';
    $("#id_create_mission_starttime").datetimepicker("setDate", new Date());
}

var CreateMutiVideo = function () {
    var category_list = $("#id_video_category").val()
    var category_string = ''
    for (var i = 0; i < category_list.length; i++) {
        category_string = category_string + category_list[i] + ','
    }
    $.ajax({
        type: "POST",
        url: $("#create_video_url").text(),
        data: {
            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
            title: document.getElementById("id_video_title").value,
            remark: document.getElementById("id_video_remark").value,
            guid: document.getElementById("id_guid").value,
            commodityid: document.getElementById("id_commodity_id").value,
            videokeyword: document.getElementById("id_create_video_keyword").value,
            category: category_string,
        },
        success: function (response, status, xhr, $form) {
            if (response != 'Error') {
                window.location.href = response;
            }
        }
    })
}

var CreateMutiMission = function () {
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
            url: $("#createmutimission_url").text(),
            data: {
                csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                deviceid: document.getElementById("id_create_device_id").value,
                commodityid: document.getElementById("id_commodity_mission_id").value,
                starttime: document.getElementById("id_create_mission_starttime").value,
            },
            success: function (response, status, xhr, $form) {
                if (response != 'Error') {
                    window.location.href = response;
                }
            }
        })
    }
}

$('#uploadVideoModal').on('hidden.bs.modal', function () {
    window.location.reload();
});

$('#missionModal').on('hidden.bs.modal', function () {
    window.location.reload();
});

var showErrorMsg = function (form, type, msg) {
    var alert = $('<div class="col-lg-12 col-xl-12 alert alert-bold alert-solid-' + type + ' alert-dismissible" role="alert">\
        <div class="alert-text">' + msg + '</div>\
        <div class="alert-close">\
            <i class="flaticon2-cross kt-icon-sm" data-dismiss="alert"></i>\
        </div>\
    </div>');

    form.find('.alert').remove();
    alert.prependTo(form);
    KTUtil.animateClass(alert[0], 'fadeIn animated');
}

var GetTaoBaoCommodity = function () {
    var btn = $(this)
    var form = $('#kt_login_form');
    var url = $("#id_url").val()
    $.ajax({
        type: "POST",
        url: $("#gettaobaocommodity_url").text(),
        data: {
            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
            url: url
        },
        success: function (response, status, xhr, $form) {
            if (response['status'] != 'NG') {
                $('#pic_box').collapse('show');
                document.getElementById("id_pic1").src = response['pic1'];
                document.getElementById("id_pic2").src = response['pic2'];
                document.getElementById("id_pic3").src = response['pic3'];
                document.getElementById("id_pic4").src = response['pic4'];
                document.getElementById("id_pic5").src = response['pic5'];
                document.getElementById("id_title").value = response['title'];
                document.getElementById("id_price").value = response['price'];
                document.getElementById("id_outsideplatformid").value = response['outsideplatformid'];
                document.getElementById("id_sales").value = response['volume'];
                document.getElementById("id_commissionpercent").value = response['commissionrate'];
            } else {
                setTimeout(function () {
                    KTApp.unprogress(btn[0]);
                    showErrorMsg(form, 'danger', response["msg"]);
                }, 1000);
            }
        }
    })
}

var CreateCommodity = function () {
    var btn = $(this)
    var form = $('#kt_login_form');

    form.validate({
        rules: {
            url: {
                required: true
            },
            subtitle: {
                required: true,
                minlength: 1,
                maxlength: 10,
            },
        },
        messages: {
            subtitle: {
                maxlength: "不能超过10个字符"
            }
        },
    });

    if (!form.valid()) {
        return;
    }

    if (checkSubTitle() == false) {
        setTimeout(function () {
            showErrorMsg(form, 'danger', '短标题含有非法字符');
        }, 1000);
        return;
    }

    var category_list = $("#id_category").val()
    var category_string = ''
    for (var i = 0; i < category_list.length; i++) {
        category_string = category_string + category_list[i] + ','
    }
    $.ajax({
        type: "POST",
        url: $("#create_url").text(),
        data: {
            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
            pic1: document.getElementById("id_pic1").src,
            pic2: document.getElementById("id_pic2").src,
            pic3: document.getElementById("id_pic3").src,
            pic4: document.getElementById("id_pic4").src,
            pic5: document.getElementById("id_pic5").src,
            title: document.getElementById("id_title").value,
            subtitle: document.getElementById("id_subtitle").value,
            price: document.getElementById("id_price").value,
            outsideplatformid: document.getElementById("id_outsideplatformid").value,
            sales: document.getElementById("id_sales").value,
            commissionpercent: document.getElementById("id_commissionpercent").value,
            url: document.getElementById("id_url").value,
            category: category_string,
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

var EditCommodity = function () {
    var form = $('#editform');

    form.validate({
        rules: {
            edit_subtitle: {
                required: true
            },
        }
    });

    if (!form.valid()) {
        return;
    }

    var category_list = $("#id_edit_category").val()
    var category_string = ''
    for (var i = 0; i < category_list.length; i++) {
        category_string = category_string + category_list[i] + ','
    }
    $.ajax({
        type: "POST",
        url: $("#edit_url").text(),
        data: {
            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
            id: document.getElementById("id_data_id").value,
            subtitle: document.getElementById("id_edit_subtitle").value,
            category: category_string,
        },
        success: function (response, status, xhr, $form) {
            if (response != 'Error') {
                window.location.href = response;
            }
        }
    })
}

var initmodal = function () {
    document.getElementById("id_url").value = '';
    $('#pic_box').collapse('hide');
    document.getElementById("id_title").value = '';
    document.getElementById("id_subtitle").value = '';
    document.getElementById("id_price").value = '';
    document.getElementById("id_sales").value = ''
    document.getElementById("id_outsideplatformid").value = '';
    document.getElementById("id_commissionpercent").value = '';
    var select = document.getElementById('id_category');
    for (var j = 0; j < select.options.length; j++) {
        select.options[j].selected = false;
    }
}

var initeditmodal = function () {
    document.getElementById("id_edit_url").value = '';
    document.getElementById("id_edit_title").value = '';
    document.getElementById("id_edit_subtitle").value = '';
    document.getElementById("id_edit_price").value = '';
    document.getElementById("id_edit_sales").value = ''
    document.getElementById("id_edit_outsideplatformid").value = '';
    document.getElementById("id_edit_commissionpercent").value = '';
    var select = document.getElementById('id_edit_category');
    for (var j = 0; j < select.options.length; j++) {
        select.options[j].selected = false;
    }
}

var initDeviceModal = function () {
    var deviceopitons = {
        'iscommodity': true,
        'isinit': document.getElementById("id_create_mission_divice").value == ''
    }
    $('#diviceModal').deviceDatatable(deviceopitons);
}

var checkSubTitle = function () {
    var subTitle = document.getElementById("id_subtitle").value
    subTitle = subTitle.replace(/(^\s*)|(\s*$)/g, "");
    var regu = "^[\u4E00-\u9FA5A-Za-z]+$";
    var re = new RegExp(regu);
    if (!(re.test(subTitle))) {
        return false;
    } else {
        return true;
    }
}

var initSearch = function () {
    //类型
    $("[name='commodityTypeBtn']").click(function () {
        if ($(this).hasClass('btn-outline-hover-primary')) {
            var count = $("[name='commodityTypeBtn']").length
            $(this).removeClass('btn-outline-hover-primary')
            $(this).addClass('btn-primary')
            $("[name='commodityTypeBtnAll']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            if ($("#commodityType .btn-primary").length == count) {
                $("[name='commodityTypeBtnAll']").removeClass('btn-outline-hover-primary').addClass('btn-primary')
                $("[name='commodityTypeBtn']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            }
            getCommodityTypeSearch()
        } else if ($(this).hasClass('btn-primary')) {
            $(this).removeClass('btn-primary')
            $(this).addClass('btn-outline-hover-primary')
            if ($("#commodityType .btn-primary").length == 0) {
                $("[name='commodityTypeBtnAll']").removeClass('btn-outline-hover-primary').addClass('btn-primary')
            }
            getCommodityTypeSearch()
        }
    })
    $("[name='commodityTypeBtnAll']").click(function () {
        if ($(this).hasClass('btn-outline-hover-primary')) {
            $(this).removeClass('btn-outline-hover-primary')
            $(this).addClass('btn-primary')
            $("[name='commodityTypeBtn']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            getCommodityTypeSearch()
        }
    })
}

var getCommodityTypeSearch = function () {
    var commodityTypeSearch = ''
    if ($("[name='commodityTypeBtnAll']").hasClass('btn-primary')) {
        commodityTypeSearch = ''
    } else {
        var list = $("#commodityType .btn-primary")
        for (var i = 0; i < list.length; i++) {
            var per = list[i]
            commodityTypeSearch = commodityTypeSearch + per.value + ','
        }
    }
    search('commoditytype', commodityTypeSearch)
}

var search = function (param, value) {
    var datatable = $('#datatable_mycommodity').KTDatatable()
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

function guid() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0,
            v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}