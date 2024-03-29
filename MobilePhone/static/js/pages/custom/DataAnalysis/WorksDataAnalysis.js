"use strict";
// Class definition

var KTDatatableCommodityDataAnalysis = function () {

    var ownerSearch = $("#owner .btn-primary")[0].value

    // Private functions
    var options = {
        // datasource definition
        data: {
            type: 'remote',
            source: {
                read: {
                    url: $("#data_url").text(),
                    params: {
                        csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                        'query[owner]': ownerSearch,
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
            input: $('#generalWorksDataAnalysisSearch'),
            onEnter: true,
        },

        // columns definition

        columns: [{
            field: 'Works__id',
            title: 'ID',
            autoHide: false,
            sortable: false,
            width: 20,
        }, {
            field: 'Works__Pic',
            title: '视频封面',
            autoHide: false,
            sortable: false,
            template: function (row) {
                if (row.Works__Pic == null) {
                    return '链接已失效';
                } else {
                    return '\
                    <a class="kt-media kt-media--xl">\
					    <img src= "' + row.Works__Pic + '" alt="image">\
					</a>\
                ';
                }
            }
        }, {
            field: 'Works__Describe',
            title: '视频描述',
            autoHide: false,
            sortable: false,
        }, {
            field: 'Video_CategoryString',
            title: '视频标签',
            autoHide: false,
            sortable: false,
            template: function (row) {
                var cat = row.Video_CategoryString
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
            field: 'Works__TikTokAccount__NickName',
            title: '抖音账号',
            autoHide: false,
            sortable: false,
            template: function (row) {
                if (row.Works__TikTokAccount__NickName == null) {
                    return ''
                } else {
                    return '\
                    <a href="javascript:void(0);" class="kt-link kt-font-bold kt-margin-t-5" \
                    data-tiktokaccount-name=' + row.Works__TikTokAccount__NickName + '>' + row.Works__TikTokAccount__NickName + '</a> \
                    '
                }
            }
        }, {
            field: 'NumOfPlay',
            title: '播放量',
            autoHide: false,
            width: 70,
        }, {
            field: 'NumOfPraiseGet',
            title: '点赞量',
            autoHide: false,
            width: 70,
        }, {
            field: 'NumOfComments',
            title: '评论量',
            autoHide: false,
            width: 70,
        }, {
            field: 'NumOfShare',
            title: '分享量',
            autoHide: false,
            width: 70,
        }, {
            field: 'Works__UploadTime',
            title: '上传日期',
            autoHide: false,
            type: 'date',
            format: 'MM/DD/YYYY',
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
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="播放视频" data-index-id="' + row.Works__ShareURL + '">\
                        <i class="flaticon2-arrow"></i>\
                    </button>\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="近30天数据" data-history-id="' + row.Works__id + '">\
                        <i class="flaticon2-graphic"></i>\
                    </button>\
                ';
            },
        }, {
            field: 'Works__UpdateTime',
            title: '更新日期',
            autoHide: false,
            sortable: false,
            type: 'date',
            format: 'MM/DD/YYYY',
        }, {
            field: 'tiktokaccount_classification',
            title: '账号标签',
            autoHide: false,
            sortable: false,
            template: function (row) {
                var cat = row.tiktokaccount_classification
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
            field: 'Works__TikTokAccount__Group__Name',
            title: '账号分组',
            autoHide: false,
            sortable: false,
            template: function (row) {
                if (row.Works__TikTokAccount__Group__Name == null) {
                    return ''
                } else {
                    return '\
                    <span class="badge badge-primary">' + row.Works__TikTokAccount__Group__Name + '</span>';
                }
            }
        },{
            field: 'Works__TikTokAccount__Owner__username',
            title: '拥有者',
            autoHide: false,
            width: 60,
        }, ],
    };

    // basic demo
    var localSelectorDemo = function () {

        var datatable = $('#datatable_works_data_analysis').KTDatatable(options);

        $('#kt_works_data_analysis_column').on('change', function () {
            datatable.search($(this).val().toLowerCase(), 'worksdataanalysiscolumn');
        });

        $('#kt_works_data_analysis_column').selectpicker();

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

        datatable.on('click', '[data-index-id]', function () {
            var ShareURL = $(this).data('index-id');
            window.open(ShareURL);
        });

        datatable.on('click', '[data-tiktokaccount-name]', function () {
            var name = $(this).data('tiktokaccount-name');
            localStorage.setItem('jumpToTikTokAccounttName', name);
            window.location.href = $("#acountlist_url").text()
        });

        datatable.on('click', '[data-history-id]', function () {
            var workid = $(this).data('history-id');
            KTDatatableHistory.setWorkID(workid)
            $('#historyModal').modal('show');
        });
    };

    return {
        // public functions
        init: function () {
            localSelectorDemo();
        }
    };
}();

var KTDatatableHistory = function () {

    // Private functions
    var options = {
        // datasource definition
        data: {
            type: 'remote',
            source: {
                read: {
                    url: $("#history_data_url").text(),
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
            input: $('#generalWorksDataAnalysisSearch'),
            onEnter: true,
        },

        // columns definition

        columns: [{
            field: 'Summary_Date',
            title: '统计日期',
            autoHide: false,
            type: 'date',
            format: 'MM/DD/YYYY',
        },{
            field: 'Work__Pic',
            title: '视频封面',
            autoHide: false,
            sortable: false,
            template: function (row) {
                if (row.Work__Pic == null) {
                    return '链接已失效';
                } else {
                    return '\
                    <a class="kt-media kt-media--xl">\
					    <img src= "' + row.Work__Pic + '" alt="image">\
					</a>\
                ';
                }
            }
        }, {
            field: 'Work__Describe',
            title: '视频描述',
            autoHide: false,
            sortable: false,
        }, {
            field: 'Video_CategoryString',
            title: '视频标签',
            autoHide: false,
            sortable: false,
            template: function (row) {
                var cat = row.Video_CategoryString
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
            field: 'Work__TikTokAccount__NickName',
            title: '抖音账号',
            autoHide: false,
            sortable: false
        }, {
            field: 'NumOfPlay',
            title: '播放量',
            autoHide: false,
            width: 70,
        }, {
            field: 'NumOfPraiseGet',
            title: '点赞量',
            autoHide: false,
            width: 70,
        }, {
            field: 'NumOfComments',
            title: '评论量',
            autoHide: false,
            width: 70,
        }, {
            field: 'NumOfShare',
            title: '分享量',
            autoHide: false,
            width: 70,
        },],
    };

    // basic demo
    var localSelectorDemo = function () {

        var datatable = $('#modal_datatable_history').KTDatatable(options);

    };

    var setWorkID = function (workid) {
        var datatable = $('#modal_datatable_history').KTDatatable();
        datatable.setDataSourceParam('query', {
            'workid': workid
        })
        datatable.reload()
    }

    return {
        // public functions
        init: function () {
            localSelectorDemo();
        },
        setWorkID : function(workid) {
            setWorkID(workid);
        }
    };
}();

jQuery(document).ready(function () {
    KTDatatableCommodityDataAnalysis.init();
    KTDatatableHistory.init();
    initSearch();
});

var initSearch = function () {
    //视频标签
    $("[name='videoTypeBtn']").click(function () {
        if ($(this).hasClass('btn-outline-hover-primary')) {
            var count = $("[name='videoTypeBtn']").length
            $(this).removeClass('btn-outline-hover-primary')
            $(this).addClass('btn-primary')
            $("[name='videoTypeBtnAll']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            if ($("#videoType .btn-primary").length == count) {
                $("[name='videoTypeBtnAll']").removeClass('btn-outline-hover-primary').addClass('btn-primary')
                $("[name='videoTypeBtn']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            }
            getVideoTypeSearch()
        } else if ($(this).hasClass('btn-primary')) {
            $(this).removeClass('btn-primary')
            $(this).addClass('btn-outline-hover-primary')
            if ($("#videoType .btn-primary").length == 0) {
                $("[name='videoTypeBtnAll']").removeClass('btn-outline-hover-primary').addClass('btn-primary')
            }
            getVideoTypeSearch()
        }
    })
    $("[name='videoTypeBtnAll']").click(function () {
        if ($(this).hasClass('btn-outline-hover-primary')) {
            $(this).removeClass('btn-outline-hover-primary')
            $(this).addClass('btn-primary')
            $("[name='videoTypeBtn']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            getVideoTypeSearch()
        }
    })

    //账号标签
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

    //账号分组
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

    //拥有者
    $("[name='ownerBtn']").click(function () {
        if ($(this).hasClass('btn-outline-hover-primary')) {
            $("[name='ownerBtn']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            $(this).removeClass('btn-outline-hover-primary')
            $(this).addClass('btn-primary')
            getOwnerSearch()
        }
    })
}

var getVideoTypeSearch = function () {
    var videoTypeSearch = ''
    if ($("[name='videoTypeBtnAll']").hasClass('btn-primary')) {
        videoTypeSearch = ''
    } else {
        var list = $("#videoType .btn-primary")
        for (var i = 0; i < list.length; i++) {
            var per = list[i]
            videoTypeSearch = videoTypeSearch + per.value + ','
        }
    }
    search('videotype', videoTypeSearch)
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

var getOwnerSearch = function () {
    var ownerSearch = $("#owner .btn-primary")[0].value
    search('owner', ownerSearch)
}

var search = function (param, value) {
    var datatable = $('#datatable_works_data_analysis').KTDatatable()
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