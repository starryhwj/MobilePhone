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
            input: $('#generalCommodityDataAnalysisSearch'),
            onEnter: true,
        },

        // columns definition

        columns: [{
            field: 'Goods__id',
            title: 'ID',
            sortable: false,
            autoHide: false,
            width: 20,
        },{
            field: 'Goods__Pic1',
            title: '缩略图',
            autoHide: false,
            sortable: false,
            template: function (row) {
              return '\
                    <a class="kt-media kt-media--xl">\
					    <img src= "' + row.Goods__Pic1 + '" alt="image">\
					</a>\
                ';
            }
        }, {
            field: 'Goods__Title',
            title: '标题',
            autoHide: false,
            sortable: false,
        }, {
            field: 'WorksCount',
            title: '视频数量',
            autoHide: false,
            width: 80,
        }, {
            field: 'Goods__CreateTime',
            title: '添加日期',
            autoHide: false,
        }, {
            field: 'NumOfPlay',
            title: '播放量',
            autoHide: false,
            width: 70,
            template: function(row) {
                if (row.NumOfPlay == null) {
                    return 0
                } else {
                    return row.NumOfPlay
                }
            } 
        }, {
            field: 'NumOfPraiseGet',
            title: '点赞量',
            autoHide: false,
            width: 70,
            template: function(row) {
                if (row.NumOfPraiseGet == null) {
                    return 0
                } else {
                    return row.NumOfPraiseGet
                }
            } 
        }, {
            field: 'NumOfComments',
            title: '评论量',
            autoHide: false,
            width: 70,
            template: function(row) {
                if (row.NumOfComments == null) {
                    return 0
                } else {
                    return row.NumOfComments
                }
            } 
        }, {
            field: 'NumOfShare',
            title: '分享量',
            autoHide: false,
            width: 70,
            template: function(row) {
                if (row.NumOfShare == null) {
                    return 0
                } else {
                    return row.NumOfShare
                }
            } 
        },{
            field: 'TodayOrder',
            title: '今日销量',
            autoHide: false,
            width: 80,
        }, {
            field: 'YestodayOrder',
            title: '昨日销量',
            autoHide: false,
            width: 80,
        }, {
            field: 'MonthOrder',
            title: '本月销量',
            autoHide: false,
            width: 80,
        },{
            field: 'Goods__Owner__username',
            title: '拥有者',
            autoHide: false,
            width: 60,
        },{
            field: 'Actions',
            title: '操作',
            sortable: false,
            width: 110,
            overflow: 'visible',
            autoHide: false,
            textAlign: 'center',
            template: function (row) {
                return '\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="订单信息" data-order-id="' + row.Goods__id + '">\
                        <i class="flaticon2-lorry"></i>\
                    </button>\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="视频信息" data-video-id="' + row.Goods__id + '">\
                        <i class="flaticon2-photo-camera"></i>\
                    </button>\
                ';
            },
        }],
    };

    // basic demo
    var localSelectorDemo = function () {
        $('#kt_commoditydataanalysis_column').on('change', function () {
            datatable.search($(this).val().toLowerCase(), 'commodityDataAnalysisColumn');
        });

        $('#kt_commoditydataanalysis_column').selectpicker();

        var datatable = $('#datatable_commodity_data_analysis').KTDatatable(options);

        datatable.on('click', '[data-video-id]', function () {
            var goodid = $(this).data('video-id');
            KTDatatableWorks.setGoodID(goodid)
            $('#worksModal').modal('show');
        });

        datatable.on('click', '[data-order-id]', function () {
            var goodid = $(this).data('order-id');
            $('#datatable_order').setOrderDatatableGoodID(goodid)
            $('#ordersModal').modal('show');
        });
    };

    return {
        // public functions
        init: function () {
            localSelectorDemo();
        }
    };
}();

var KTDatatableWorks = function () {

    // Private functions
    var options = {
        // datasource definition
        data: {
            type: 'remote',
            source: {
                read: {
                    url: $("#works_url").text(),
                    params: {
                        csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
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
            input: $('#generalWorkSearch'),
            onEnter: true,
        },

        // columns definition

        columns: [{
            field: 'id',
            title: 'ID',
            autoHide: false,
            sortable: false,
            width: 20,
        },{
            field: 'Pic',
            title: '视频封面',
            autoHide: false,
            sortable: false,
            template: function (row) {
                if (row.Pic == null) {
                    return '链接已失效';
                } else {
                    return '\
                    <a class="kt-media kt-media--xl">\
					    <img src= "' + row.Pic + '" alt="image">\
					</a>\
                ';
                }
            }
        }, {
            field: 'Describe',
            title: '视频描述',
            autoHide: false,
            sortable: false,
        }, {
            field: 'ShareURL',
            title: '视频链接',
            autoHide: false,
            sortable: false,
            width: 200,
        }, {
            field: 'NumOfPlay',
            title: '播放量',
            autoHide: false,
            width: 30,
        }, {
            field: 'NumOfPraiseGet',
            title: '点赞量',
            autoHide: false,
            width: 30,
        }, {
            field: 'NumOfComments',
            title: '评论量',
            autoHide: false,
            width: 30,
        }, {
            field: 'NumOfShare',
            title: '分享量',
            autoHide: false,
            width: 30,
        }, {
            field: 'TikTokAccount__NickName',
            title: '抖音账号',
            autoHide: false,
            sortable: false,            
            width: 80,
        },{
            field: 'UpdateTime',
            title: '更新日期',
            autoHide: false,
            type: 'date',
            format: 'MM/DD/YYYY',
        }, {
            field: 'UploadTime',
            title: '上传日期',
            autoHide: false,
            type: 'date',
            format: 'MM/DD/YYYY',
        },{
            field: 'Actions',
            title: '操作',
            sortable: false,
            width: 110,
            overflow: 'visible',
            autoHide: false,
            textAlign: 'center',
            template: function (row) {
                return '\
                    <button class="btn btn-sm btn-clean btn-icon btn-icon-sm" title="播放视频" data-index-id="' + row.ShareURL + '">\
                        <i class="flaticon2-arrow"></i>\
                    </button>\
                ';
            },
        }],
    };

    // basic demo
    var localSelectorDemo = function () {

        var datatable = $('#modal_datatable_works').KTDatatable(options);

        datatable.on('click', '[data-index-id]', function () {
            var ShareURL = $(this).data('index-id');
            window.open(ShareURL);
        });
    };

    var setGoodID = function (goodid) {
        var datatable = $('#modal_datatable_works').KTDatatable();
        datatable.setDataSourceParam('query', {
            'goodid': goodid
        })
        datatable.reload()
    }

    return {
        // public functions
        init: function () {
            localSelectorDemo();
        },
        setGoodID: function (goodid) {
            setGoodID(goodid);
        }
    };
}();

jQuery(document).ready(function () {
    KTDatatableCommodityDataAnalysis.init();
    if (localStorage.getItem("jumpToCommodityDataAnalysisID") != null) {
        var commodityid = localStorage.getItem("jumpToCommodityDataAnalysisID")
        localStorage.removeItem('jumpToCommodityDataAnalysisID');
        $('#generalCommodityDataAnalysisSearch').val(commodityid);
        var selectcolumn = $('#kt_commoditydataanalysis_column');
        for (var j = 0; j < selectcolumn[0].options.length; j++) {
            if (selectcolumn[0].options[j].value == 'id') {
                selectcolumn[0].options[j].selected = true;
                break;
            }
        }
        selectcolumn.next()[0].title = '商品ID'
        selectcolumn.next().children().children().children()[0].innerHTML = '商品ID'
        var datatable = $('#datatable_commodity_data_analysis').KTDatatable()
        datatable.setDataSourceParam('query', {
            'generalCommodityDataAnalysisSearch': commodityid,
            'commodityDataAnalysisColumn': 'id'
        })
        datatable.load()
    }    
    KTDatatableWorks.init();
    $('#modal-order-datatable').orderDatatable();
    initSearch();
});

var initSearch = function () {
    //视频日期
    $("[name='workstimeBtn']").click(function () {
        if ($(this).hasClass('btn-outline-hover-primary')) {
            $("[name='workstimeBtn']").removeClass('btn-primary').addClass('btn-outline-hover-primary')
            $(this).removeClass('btn-outline-hover-primary')
            $(this).addClass('btn-primary')
            getWorksTimeSearch()
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

var getWorksTimeSearch = function () {
    var statusSearch = $("#workstime .btn-primary")[0].value
    search('workstime', statusSearch)
}

var getOrderStatusSearch = function () {
    var statusSearch = ''
    if ($("[name='orderStatusBtnAll']").hasClass('btn-primary')) {
        statusSearch = ''
    } else {
        var list = $("#orderStatus .btn-primary")
        for (var i = 0; i < list.length; i++) {
            var per = list[i]
            statusSearch = statusSearch + per.value + ','
        }
    }
    orderSearch('orderStatus', statusSearch)
}

var getCreateTimeSearch = function () {
    var createtimeSearch = ''
    if ($("[name='createtimeBtnAll']").hasClass('btn-primary')) {
        createtimeSearch = ''
    } else {
        var list = $("#createtime .btn-primary")
        for (var i = 0; i < list.length; i++) {
            var per = list[i]
            createtimeSearch = createtimeSearch + per.value + ','
        }
    }
    orderSearch('createtime', createtimeSearch)
}

var getOwnerSearch = function () {
    var ownerSearch = $("#owner .btn-primary")[0].value
    search('owner', ownerSearch)
}

var search = function (param, value) {
    var datatable = $('#datatable_commodity_data_analysis').KTDatatable()
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

var orderSearch = function (param, value) {
    var datatable = $('#modal_datatable_orders').KTDatatable()
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