function CMSNewsList() {

};

CMSNewsList.prototype.initDatePicker = function () {
    var startPicker = $('#start-picker');
    var endPicker = $('#end-picker');
    var todayDate = new Date();
    var todayStr = todayDate.getFullYear() + '/' + (todayDate.getMonth() + 1) + '/' + todayDate.getDate();
    var options = {
        'showButtonPanel': true,
        'format': 'yyyy/mm/dd',
        'startDate': '2017/6/1',
        'endDate': todayStr,
        'language': 'zh-CN',
        'todayBtn': 'linked',
        'todayHightlight': true,
        'clearBtn': true,
        'autoclose': true,
    };
    startPicker.datepicker(options);
    endPicker.datepicker(options);

};

CMSNewsList.prototype.listenDeleteEvent = function () {
    var deleteBtn = $('.delete-btn');
    deleteBtn.click(function () {
        var btn = $(this);
        var news_id = btn.attr('data-news-id');
        swal({
                title: "确定删除吗？",
                text: "您将无法恢复这条新闻！",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "确定删除！",
                closeOnConfirm: false
            },
            function () {
                xfzajax.post({
                    'url': '/cms/delete_news/',
                    'data': {
                        'news_id': news_id
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            swal({title: '新闻删除成功！', type: "success"}
                                , function () {
                                    //window.location.reload();
                                    window.location = window.location.href;
                                });

                        } else {
                            //显示错误信息
                            swal({
                                title: result['message'],
                                text: "2秒后自动关闭。",
                                timer: 2000,
                                showConfirmButton: false
                            });
                        }
                    }
                })
            })
    })
};

CMSNewsList.prototype.run = function () {
    this.initDatePicker();
    this.listenDeleteEvent();
};


$(function () {
    var newsList = new CMSNewsList();
    newsList.run();
});