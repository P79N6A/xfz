function NewsCategory() {

};

NewsCategory.prototype.run = function () {
    var self = this;
    self.listenAddCategoryEvent();
    self.listenEditCategoryEvent();
    self.listenDeleteCategoryEvent();
};

NewsCategory.prototype.listenAddCategoryEvent = function () {
    //添加新闻事件
    var addBtn = $('#add-btn');
    addBtn.click(function () {
        swal({
            title: "添加新闻分类",
            text: "",
            type: "input",
            showCancelButton: true,
            closeOnConfirm: false,
            animation: "slide-from-top",
            inputPlaceholder: "请输入新闻分类..",
        }, function (inputValue) {
            if (inputValue === false) {
                return false;
            }
            if (inputValue === "") {
                swal.showInputError("内容不能为空！");
                return false;
            }

            xfzajax.post({
                'url': '/cms/add_news_category/',
                'data': {
                    'name': inputValue,
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        window.location.reload();
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
            });

            // swal("Nice!", "你输入的是：" + inputValue, "success")
        })
    });
};

NewsCategory.prototype.listenEditCategoryEvent = function () {
    //编辑事件
    var self = this;
    var editBtn = $(".edit-btn");
    editBtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var pk = tr.attr('data-pk');
        var name = tr.attr('data-name');

        //弹出编辑对话框 sweetalert
        swal({
            title: "修改分类名称",
            text: "",
            type: "input",
            showCancelButton: true,
            closeOnConfirm: false,
            animation: "slide-from-top",
            inputPlaceholder: "请输入新的分类名称..",
            inputValue: name
        }, function (inputValue) {
            if (inputValue === false) {
                return false;
            }
            if (inputValue === "") {
                swal.showInputError("内容不能为空！");
                return false;
            }

            xfzajax.post({
                'url': '/cms/edit_news_category/',
                'data': {
                    'pk': pk,
                    'name': inputValue,
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        window.location.reload();
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
            });

            // swal("Nice!", "你输入的是：" + inputValue, "success")
        })
    });
};

NewsCategory.prototype.listenDeleteCategoryEvent = function () {
    var self = this;
    var deleteBtn = $('.delete-btn');
    deleteBtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var pk = tr.attr('data-pk');

        swal({
                title: "您确定删除吗？",
                text: "你将无法恢复该分类！",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "确定删除！",
                closeOnConfirm: false
            },
            function () {
                xfzajax.post({
                    'url': '/cms/delete_news_category/',
                    'data': {
                        'pk': pk
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            swal("删除！", "该分类已经被删除。", "success");
                            window.location.reload();
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
                });

            });
    })
};

$(function () {
    var category = new NewsCategory();
    category.run();
});