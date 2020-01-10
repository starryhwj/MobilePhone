"use strict";

var KTCalendarExternalEvents = function () {

    var initExternalEvents = function () {
        $('#kt_calendar_external_events .fc-draggable-handle').each(function () {
            // store data so the calendar knows to render an event upon drop
            $(this).data('event', {
                title: $.trim($(this).text()), // use the element's text as the event title
                stick: true, // maintain when user navigates (see docs on the renderEvent method)
                classNames: [$(this).data('color')],
            });
        });
    }

    var initCalendar = function () {
        var TODAY = $('#record_date').text();

        var calendarEl = document.getElementById('kt_calendar');
        var containerEl = document.getElementById('kt_calendar_external_events');

        var Draggable = FullCalendarInteraction.Draggable;

        new Draggable(containerEl, {
            itemSelector: '.fc-draggable-handle',
            eventData: function (eventEl) {
                return $(eventEl).data('event');
            }
        });

        var GetTimeStr = function(date) {
            return date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate() + ' ' + date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds();
        };

        var calendar = new FullCalendar.Calendar(calendarEl, {
            plugins: ['interaction', 'timeGrid'],

            isRTL: KTUtil.isRTL(),

            height: 600,
            contentHeight: 580,
            aspectRatio: 3, // see: https://fullcalendar.io/docs/aspectRatio

            defaultView: 'timeGridDay',
            defaultDate: TODAY,
            allDaySlot: false,
            droppable: true, // this allows things to be dropped onto the calendar
            editable: true,
            eventLimit: true, // allow "more" link when too many events
            navLinks: true,
            slotEventOverlap: false,
            eventOverlap: false,
            events: {
                url: $('#get_events_by_template_id_url').text(),
                method: 'POST',
                extraParams: {
                    csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                    templateid: $('#template_id').text(),
                },
                failure: function () {
                    alert('模板数据获取出错!');
                },
            },

            drop: function (arg) {
                // is the "remove after drop" checkbox checked?
                if ($('#kt_calendar_external_events_remove').is(':checked')) {
                    // if so, remove the element from the "Draggable Events" list
                    $(arg.draggedEl).remove();
                }
            },

            eventRender: function (info) {
                var element = $(info.el);

                if (info.event.extendedProps && info.event.extendedProps.description) {
                    if (element.hasClass('fc-day-grid-event')) {
                        element.data('content', info.event.extendedProps.description);
                        element.data('placement', 'top');
                        KTApp.initPopover(element);
                    } else if (element.hasClass('fc-time-grid-event')) {
                        element.find('.fc-title').append('<div class="fc-description">' + info.event.extendedProps.description + '</div>');
                    } else if (element.find('.fc-list-item-title').lenght !== 0) {
                        element.find('.fc-list-item-title').append('<div class="fc-description">' + info.event.extendedProps.description + '</div>');
                    }
                }

                if (info.event.title == '养号任务') {
                    element[0].style.backgroundColor = 'lightblue'
                } else if (info.event.title == '刷粉任务') {
                    element[0].style.backgroundColor = 'lemonchiffon'
                } else if (info.event.title == '关注任务') {
                    element[0].style.backgroundColor = 'honeydew'
                } else if (info.event.title == '刷宝任务') {
                    element[0].style.backgroundColor = 'lavender'
                }
            },

            eventDrop: function (eventDropInfo) {
                //拖动修改
                var strattime_str = GetTimeStr(eventDropInfo.event.start)
                var endtime_str = ''
                if (eventDropInfo.event.end != null) {
                    endtime_str = GetTimeStr(eventDropInfo.event.end)
                } 
                var dataid = eventDropInfo.event.extendedProps.dataid
                $.ajax({
                    type: "POST",
                    url: $("#edit_url").text(),
                    data: {
                        csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                        dataid: dataid,
                        strattime_str: strattime_str,
                        endtime_str: endtime_str,
                        eventtype: eventDropInfo.event.title
                    }
                })
            },

            eventResize: function (eventResizeInfo) {
                //拉动修改
                var strattime_str = GetTimeStr(eventResizeInfo.event.start)
                var endtime_str = ''
                if (eventResizeInfo.event.end != null) {
                    endtime_str = GetTimeStr(eventResizeInfo.event.end)
                } 
                var dataid = eventResizeInfo.event.extendedProps.dataid
                $.ajax({
                    type: "POST",
                    url: $("#edit_url").text(),
                    data: {
                        csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                        dataid: dataid,
                        strattime_str: strattime_str,
                        endtime_str: endtime_str,
                        eventtype: eventResizeInfo.event.title
                    }
                })
            },

            eventReceive: function (info) {
                var strattime_str = GetTimeStr(info.event.start)
                //拖动新增
                $.ajax({
                    type: "POST",
                    url: $("#create_url").text(),
                    data: {
                        csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                        templateid: $('#template_id').text(),
                        strattime_str: strattime_str,
                        eventtype: info.event.title
                    },
                    success: function (response, status, xhr, $form) {
                        if (response != 'Error') {
                            info.event.setExtendedProp('dataid', response)
                        }
                    }
                })
            },

            eventClick: function (info) {
                var dataid = info.event.extendedProps.dataid
                var eventtype = info.event.title
                //点击修改
                $.ajax({
                    type: "POST",
                    url: $("#get_event_by_id_url").text(),
                    data: {
                        csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                        dataid: dataid,
                        eventtype: info.event.title,
                    },
                    success: function (response, status, xhr, $form) {
                        if (eventtype == '养号任务') {
                            $('#editMaintenanceNumberMissionModal').modal('show')
                            $('#id_edit_MaintenanceNumberMission_description').val(response['description'])
                            $('#id_MaintenanceNumberMission_data_id').text(response['dataid'])
                            $('#id_MaintenanceNumberMission_data_type').text(response['type'])
                        } else if (eventtype == '刷粉任务') {
                            $('#editscanmissionModal').modal('show')
                            $('#id_edit_scan_mission_description').val(response['description'])
                            document.getElementById("id_edit_scan_mission_peoplelimit").value = response['peoplelimit'];
                            document.getElementById("id_edit_scan_mission_interval").value = response['interval'];
                            var fansexismale =  response['fansexismale'];
                            if (fansexismale) {
                                $('#id_edit_scan_mission_fansex_male').attr("checked", true);
                            } else {
                                $('#id_edit_scan_mission_fansex_male').attr("checked", false);
                            }
                            var fansexisfemale =  response['fansexisfemale'];
                            if (fansexisfemale) {
                                $('#id_edit_scan_mission_fansex_female').attr("checked", true);
                            } else {
                                $('#id_edit_scan_mission_fansex_female').attr("checked", false);
                            }
                            var fansexisnone =  response['fansexisnone'];
                            if (fansexisnone) {
                                $('#id_edit_scan_mission_fansex_none').attr("checked", true);
                            } else {
                                $('#id_edit_scan_mission_fansex_none').attr("checked", false);
                            }
                            document.getElementById("id_edit_scan_mission_commenttext").value = response['commenttext'];
                            $('#id_edit_scan_mission_data_id').text(response['dataid'])
                            $('#id_scan_mission_data_type').text(response['type'])
                        } else if (eventtype == '关注任务') {
                            $('#editfollowmissionModal').modal('show')
                            $('#id_edit_follow_mission_description').val(response['description'])
                            document.getElementById("id_edit_follow_mission_peoplelimit").value = response['peoplelimit'];
                            var fansexismale =  response['fansexismale'];
                            if (fansexismale) {
                                $('#id_edit_follow_mission_fansex_male').attr("checked", true);
                            } else {
                                $('#id_edit_follow_mission_fansex_male').attr("checked", false);
                            }
                            var fansexisfemale =  response['fansexisfemale'];
                            if (fansexisfemale) {
                                $('#id_edit_follow_mission_fansex_female').attr("checked", true);
                            } else {
                                $('#id_edit_follow_mission_fansex_female').attr("checked", false);
                            }
                            var fansexisnone =  response['fansexisnone'];
                            if (fansexisnone) {
                                $('#id_edit_follow_mission_fansex_none').attr("checked", true);
                            } else {
                                $('#id_edit_follow_mission_fansex_none').attr("checked", false);
                            }
                            $('#id_edit_follow_mission_data_id').text(response['dataid'])
                            $('#id_follow_mission_data_type').text(response['type'])
                        } else if (eventtype == '刷宝任务') {
                            $('#editTreasureMissionPlan').modal('show')
                            $('#id_edit_TreasureMissionPlan_description').val(response['description'])
                            $('#id_TreasureMissionPlan_data_id').text(response['dataid'])
                            $('#id_TreasureMissionPlan_data_type').text(response['type'])
                        }
                    }
                })
            }
        });

        calendar.render();
    }

    return {
        //main function to initiate the module
        init: function () {
            initExternalEvents();
            initCalendar();
        }
    };
}();

jQuery(document).ready(function () {
    KTCalendarExternalEvents.init();
    $('.fc-header-toolbar').remove()
    $('.fc-day-header').text('')
});

var back = function() {
    window.location.href = $('#template_url').text()
}

var EditMaintenanceNumberMission = function() {
    $.ajax({
        type: "POST",
        url: $("#editeventdetail").text(),
        data: {
            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
            dataid: $('#id_MaintenanceNumberMission_data_id').text(),
            eventtype: $('#id_MaintenanceNumberMission_data_type').text(),
            description: $('#id_edit_MaintenanceNumberMission_description').val(),
        },
        success: function (response, status, xhr, $form) {
            if (response != 'Error') {              
                location.reload()
            }
        }
    });
}

var DeleteMaintenanceNumberMission = function() {
    swal.fire({
        title: '确认删除?',
        text: "确认后无法撤销！",
        type: 'warning',
        showCancelButton: true,
        confirmButtonText: '是',
        cancelButtonText: '否'
    }).then(function (result) {
        if (result.value) {
            $.ajax({
                type: "POST",
                url: $("#delete_url").text(),
                data: {
                    csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                    dataid: $('#id_MaintenanceNumberMission_data_id').text(),
                    eventtype: $('#id_MaintenanceNumberMission_data_type').text(),
                },
                success: function (response, status, xhr, $form) {
                    if (response != 'Error') {
                        location.reload()
                    }
                }
            });
        };
    })
}

var EditScanMission = function() {
    $.ajax({
        type: "POST",
        url: $("#editeventdetail").text(),
        data: {
            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
            dataid: $('#id_edit_scan_mission_data_id').text(),
            eventtype: $('#id_scan_mission_data_type').text(),
            description: $('#id_edit_scan_mission_description').val(),
            peoplelimit: document.getElementById("id_edit_scan_mission_peoplelimit").value,
            interval: document.getElementById("id_edit_scan_mission_interval").value,
            fansexismale: $("#id_edit_scan_mission_fansex_male").is(':checked'),
            fansexisfemale: $("#id_edit_scan_mission_fansex_female").is(':checked'),
            fansexisnone: $("#id_edit_scan_mission_fansex_none").is(':checked'),
            commenttext: document.getElementById("id_edit_scan_mission_commenttext").value,
        },
        success: function (response, status, xhr, $form) {
            if (response != 'Error') {              
                location.reload()
            }
        }
    });
}

var DeleteScanMission = function() {
    swal.fire({
        title: '确认删除?',
        text: "确认后无法撤销！",
        type: 'warning',
        showCancelButton: true,
        confirmButtonText: '是',
        cancelButtonText: '否'
    }).then(function (result) {
        if (result.value) {
            $.ajax({
                type: "POST",
                url: $("#delete_url").text(),
                data: {
                    csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                    dataid: $('#id_edit_scan_mission_data_id').text(),
                    eventtype: $('#id_scan_mission_data_type').text(),
                },
                success: function (response, status, xhr, $form) {
                    if (response != 'Error') {
                        location.reload()
                    }
                }
            });
        };
    })
}

var EditFollowMission = function() {
    $.ajax({
        type: "POST",
        url: $("#editeventdetail").text(),
        data: {
            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
            dataid: $('#id_edit_follow_mission_data_id').text(),
            eventtype: $('#id_follow_mission_data_type').text(),
            description: $('#id_edit_follow_mission_description').val(),
            peoplelimit: document.getElementById("id_edit_follow_mission_peoplelimit").value,
            fansexismale: $("#id_edit_follow_mission_fansex_male").is(':checked'),
            fansexisfemale: $("#id_edit_follow_mission_fansex_female").is(':checked'),
            fansexisnone: $("#id_edit_follow_mission_fansex_none").is(':checked'),
        },
        success: function (response, status, xhr, $form) {
            if (response != 'Error') {              
                location.reload()
            }
        }
    });
}

var DeleteFollowMission = function() {
    swal.fire({
        title: '确认删除?',
        text: "确认后无法撤销！",
        type: 'warning',
        showCancelButton: true,
        confirmButtonText: '是',
        cancelButtonText: '否'
    }).then(function (result) {
        if (result.value) {
            $.ajax({
                type: "POST",
                url: $("#delete_url").text(),
                data: {
                    csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                    dataid: $('#id_edit_follow_mission_data_id').text(),
                    eventtype: $('#id_follow_mission_data_type').text(),
                },
                success: function (response, status, xhr, $form) {
                    if (response != 'Error') {
                        location.reload()
                    }
                }
            });
        };
    })
}

var EditTreasureMission = function() {
    $.ajax({
        type: "POST",
        url: $("#editeventdetail").text(),
        data: {
            csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
            dataid: $('#id_TreasureMissionPlan_data_id').text(),
            eventtype: $('#id_TreasureMissionPlan_data_type').text(),
            description: $('#id_edit_TreasureMissionPlan_description').val(),
        },
        success: function (response, status, xhr, $form) {
            if (response != 'Error') {              
                location.reload()
            }
        }
    });
}

var DeleteTreasureMission = function() {
    swal.fire({
        title: '确认删除?',
        text: "确认后无法撤销！",
        type: 'warning',
        showCancelButton: true,
        confirmButtonText: '是',
        cancelButtonText: '否'
    }).then(function (result) {
        if (result.value) {
            $.ajax({
                type: "POST",
                url: $("#delete_url").text(),
                data: {
                    csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
                    dataid: $('#id_TreasureMissionPlan_data_id').text(),
                    eventtype: $('#id_TreasureMissionPlan_data_type').text(),
                },
                success: function (response, status, xhr, $form) {
                    if (response != 'Error') {
                        location.reload()
                    }
                }
            });
        };
    })
}
