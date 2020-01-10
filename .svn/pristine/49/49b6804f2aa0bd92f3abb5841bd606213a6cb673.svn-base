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
                        ishistory: 'false',
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
            input: $('#generalAccountDataNanlysisSearch'),
            onEnter: true,
        },

        // columns definition

        columns: [{
            field: 'Summary_Date',
            title: '日期',
            autoHide: false,
            type: 'date',
            format: 'MM/DD/YYYY',
        }, {
            field: 'FansIncrease',
            title: '粉丝增量',
            autoHide: false,
            width: 80,
        }, {
            field: 'PraiseIncrease',
            title: '获赞增量',
            autoHide: false,
            width: 80,
        }, {
            field: 'NumOfPraiseToOtherIncrease',
            title: '点赞增量',
            autoHide: false,
            width: 80,
        }, {
            field: 'TotalNumOfPlayIncrease',
            title: '播放增量',
            autoHide: false,
            width: 80,
        }, {
            field: 'TikTokAccount__NickName',
            title: '昵称',
            autoHide: false,
            sortable: false,
            template: function (row) {
                if (row.TikTokAccount__NickName == null) {
                    return ''
                } else {
                    return '\
                    <a href="javascript:void(0);" class="kt-link kt-font-bold kt-margin-t-5" \
                    data-tiktokaccount-name=' + row.TikTokAccount__NickName + '>' + row.TikTokAccount__NickName + '</a> \
                    '
                }
            }
        },{
            field: 'TikTokAccount__mobilephone__Agent__Subscriber__username',
            title: '代理',
            autoHide: false,
            sortable: false,
            width: 50,
            template: function (row) {
                if (row.TikTokAccount__mobilephone__Agent__Subscriber__username == null) {
                    return ''
                } else {
                    return '\
                    <a href="javascript:void(0);" class="kt-link kt-font-bold kt-margin-t-5" \
                    data-agent-name=' + row.TikTokAccount__mobilephone__Agent__Subscriber__username + '>' + row.TikTokAccount__mobilephone__Agent__Subscriber__username + '</a> \
                    '
                }
            }
        },{
            field: 'TikTokAccount__mobilephone__id',
            title: '设备ID',
            autoHide: false,
            sortable: false,
            width: 40,
            template: function (row) {
                if (row.TikTokAccount__mobilephone__id == null) {
                    return ''
                } else {
                    return '\
                    <a href="javascript:void(0);" class="kt-link kt-font-bold kt-margin-t-5" \
                    data-mobilephone-id=' + row.TikTokAccount__mobilephone__id + '>' + row.TikTokAccount__mobilephone__id + '</a> \
                    '
                }
            }
        }, {
            field: 'Actions',
            title: '操作',
            sortable: false,
            width: 110,
            overflow: 'visible',
            autoHide: false,
            textAlign: 'center',
            template: function (row) {
                if (row.TikTokAccount__NickName == null) {
                    return ''
                } else {
                    return '\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="近30天数据" data-history-id="' + row.TikTokAccount__NickName + '">\
                        <i class="flaticon2-graphic"></i>\
                    </button>\
                    '
                }
            },
        },{
            field: 'Video',
            title: '作品数',
            autoHide: false,
            width: 70,
        }, {
            field: 'Fans',
            title: '粉丝数',
            autoHide: false,
            width: 70,
        }, {
            field: 'Attention',
            title: '关注数',
            autoHide: false,
            width: 70,
        }, {
            field: 'Praise',
            title: '获赞数',
            autoHide: false,
            width: 70,
        }, {
            field: 'NumOfPraiseToOther',
            title: '点赞数',
            autoHide: false,
            width: 70,
        }, {
            field: 'TotalNumOfPlay',
            title: '总播放量',
            autoHide: false,
            width: 80,
        }, {
            field: 'TotalNumOfComments',
            title: '总评论量',
            autoHide: false,
            width: 80,
        },{
            field: 'FirstWorkNumOfPlay',
            title: '作品1播放量',
            autoHide: false,
            width: 100,
        }, {
            field: 'AttentionIncrease',
            title: '关注增量',
            autoHide: false,
            width: 80,
        }, {
            field: 'TotalNumOfCommentsIncrease',
            title: '评论增量',
            autoHide: false,
            width: 80,
        },{
            field: 'FirstWorkNumOfPlayIncrease',
            title: '作品1播放增量',
            autoHide: false,
            width: 60,
        }, {
            field: 'classification',
            title: '标签',
            autoHide: false,
            sortable: false,
            template: function (row) {
                var cat = row.classification
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
        },{
            field: 'TikTokAccount__Owner__username',
            title: '拥有者',
            autoHide: false,
            width: 60,
        },],
    };

    // basic demo
    var localSelectorDemo = function () {

        var datatable = $('#datatable_account_data_analysis').KTDatatable(options);

        datatable.on('click', '[data-agent-name]', function () {
            var name = $(this).data('agent-name');
            localStorage.setItem('jumpToAgentName', name);
            window.location.href = $("#agentdetail_url").text()
        });

        datatable.on('click', '[data-tiktokaccount-name]', function () {
            var name = $(this).data('tiktokaccount-name');
            localStorage.setItem('jumpToTikTokAccounttName', name);
            window.location.href = $("#acountlist_url").text()
        });

        datatable.on('click', '[data-history-id]', function () {
            KTDatatableHistory.init();
            var nickname = $(this).data('history-id');
            KTDatatableHistory.setNickName(nickname)
            $('#historyModal').modal('show');
        });

        datatable.on('click', '[data-mobilephone-id]', function () {
            var id = $(this).data('mobilephone-id');
            localStorage.setItem('jumpToMobilePhone', id);
            window.location.href = $("#devicemanage_url").text()
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
                    url: $("#data_url").text(),
                    params: {
                        csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                        ishistory: 'true',
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
            input: $('#generalAccountDataNanlysisSearch'),
            onEnter: true,
        },

        // columns definition

        columns: [{
            field: 'Summary_Date',
            title: '日期',
            autoHide: false,
            type: 'date',
            format: 'MM/DD/YYYY',
        }, {
            field: 'FansIncrease',
            title: '粉丝增量',
            autoHide: false,
            width: 80,
        },{
            field: 'PraiseIncrease',
            title: '获赞增量',
            autoHide: false,
            width: 80,
        }, {
            field: 'NumOfPraiseToOtherIncrease',
            title: '点赞增量',
            autoHide: false,
            width: 80,
        }, {
            field: 'TotalNumOfPlayIncrease',
            title: '播放增量',
            autoHide: false,
            width: 80,
        }, {
            field: 'Video',
            title: '作品数',
            autoHide: false,
            width: 70,
        }, {
            field: 'Fans',
            title: '粉丝数',
            autoHide: false,
            width: 70,
        }, {
            field: 'Attention',
            title: '关注数',
            autoHide: false,
            width: 70,
        }, {
            field: 'Praise',
            title: '获赞数',
            autoHide: false,
            width: 70,
        }, {
            field: 'NumOfPraiseToOther',
            title: '点赞数',
            autoHide: false,
            width: 70,
        }, {
            field: 'TotalNumOfPlay',
            title: '总播放量',
            autoHide: false,
            width: 80,
        }, {
            field: 'TotalNumOfComments',
            title: '总评论量',
            autoHide: false,
            width: 80,
        },{
            field: 'FirstWorkNumOfPlay',
            title: '作品1播放量',
            autoHide: false,
            width: 100,
        }, {
            field: 'AttentionIncrease',
            title: '关注增量',
            autoHide: false,
            width: 80,
        }, {
            field: 'TotalNumOfCommentsIncrease',
            title: '评论增量',
            autoHide: false,
            width: 80,
        },{
            field: 'FirstWorkNumOfPlayIncrease',
            title: '作品1播放增量',
            autoHide: false,
            width: 60,
        },{
            field: 'TikTokAccount__NickName',
            title: '昵称',
            autoHide: false,
            sortable: false,
        },{
            field: 'TikTokAccount__mobilephone__Agent__Subscriber__username',
            title: '代理',
            autoHide: false,
            sortable: false,
            width: 50,
        }],
    };

    // basic demo
    var localSelectorDemo = function () {

        var datatable = $('#modal_datatable_history').KTDatatable(options);
        
    };

    var setNickName = function (nickname) {
        var datatable = $('#modal_datatable_history').KTDatatable();
        datatable.setDataSourceParam('query', {
            'generalHistorySearch': nickname
        })
        datatable.reload()
    }

    return {
        // public functions
        init: function () {
            localSelectorDemo();
        },
        setNickName : function(nickname) {
            setNickName(nickname);
        }
    };
}();

jQuery(document).ready(function () {
    KTDatatableCommodityDataAnalysis.init();
    initSearch();
});

var initSearch = function () {
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

    //日期
    $("[name='dateBtn']").click(function () {
        if ($(this).hasClass('btn-outline-hover-primary')) {
            $("[name='dateBtn']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            $(this).removeClass('btn-outline-hover-primary')
            $(this).addClass('btn-primary')
            getDateSearch()
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

var getDateSearch = function () {
    var dateSearch = $("#date .btn-primary")[0].value
    search('date', dateSearch)
}

var getOwnerSearch = function () {
    var ownerSearch = $("#owner .btn-primary")[0].value
    search('owner', ownerSearch)
}

var search = function (param, value) {
    var datatable = $('#datatable_account_data_analysis').KTDatatable()
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