function NewsList() {


}

NewsList.prototype.listenSubmitEvent = function () {
    var submitBtn = $('.submit-btn');
    var textarea = $('textarea[name="comment"]');
    submitBtn.click(function () {
        var content = textarea.val();
        var news_id = submitBtn.attr('data-news-id');
        xfzajax.post({
            'url': '/news/public_comment/',
            'data': {
                'content': content,
                'news_id': news_id,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var comment = result['data'];
                    //获取script id=comment-item部分的内容进行渲染
                    var tpl = template("comment-item", {"comment": comment});
                    //获取评论区模板
                    var commentListGroup = $('.comment-list');
                    //放入评论区
                    commentListGroup.prepend(tpl);
                    swal({
                        title: "评论成功",
                        type: "success"
                    });
                    //清空textarea内容
                    textarea.val("");
                } else {
                    //显示错误信息
                    swal({
                        title: result['message'],
                       // text: "2秒后自动关闭。",
                        timer: 1000,
                        showConfirmButton: false
                    });
                }
            }
        })
    });
};
NewsList.prototype.run = function () {
    this.listenSubmitEvent();
};


$(function () {
    var newslist = new NewsList();
    newslist.run();
});