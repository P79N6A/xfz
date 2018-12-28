function Banners() {

}

Banners.prototype.createBannerItem = function (banner) {
    var self = this;
    //创建模板
    var tpl = template("banner-item", {'banner': banner});
    //将模板加入标签内
    var bannerListGroup = $(".banner-list-group");
    var bannerItem = null;
    if (banner) {
        //存在banner对象就添加到最后
        bannerListGroup.append(tpl);
        bannerItem = bannerListGroup.find(".banner-item:last");
    } else {
        bannerListGroup.prepend(tpl);
        bannerItem = bannerListGroup.find(".banner-item:first");
    }

    //监听事件
    self.addImageSelect(bannerItem);
    self.addRemoveBannerEvent(bannerItem);
    self.addSaveBannerEvent(bannerItem);
};

Banners.prototype.loadData = function () {
    //加载在数据库中就存在的新闻轮播图
    var self = this;
    xfzajax.get({
        'url': '/cms/banner_list/',
        'success': function (result) {
            if (result['code'] === 200) {
                var banners = result['data'];
                for (var i = 0; i < banners.length; i++) {
                    var banner = banners[i];
                    self.createBannerItem(banner);
                }
            }
        }
    })
};
Banners.prototype.listenAddBannerEvent = function () {
    var self = this;
    var addBtn = $('#add-banners-btn');
    addBtn.click(function () {
        //调用创建banner模板函数
        var bannerListGroup = $('.banner-list-group');
        var length = bannerListGroup.children().length;
        if (length >= 6) {
            swal({
                title: '最多只能添加6张轮播图！',
                timer: 1100,
                showConfirmButton: false
            });
            return;
        }
        self.createBannerItem();
    })
};
Banners.prototype.addImageSelect = function (bannerItem) {
    var image = bannerItem.find('.thumbnail');
    var imageInput = bannerItem.find('.image-input');

    image.click(function () {
        imageInput.click();
    });

    imageInput.change(function () {
        var file = this.files[0];
        var formData = new FormData();
        formData.append("file", file);
        xfzajax.post({
            'url': '/cms/upload_file/',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if (result['code'] === 200) {
                    var url = result['data']['url'];
                    image.attr('src', url);
                }
            },
        })
    });
};
Banners.prototype.addRemoveBannerEvent = function (bannerItem) {
    var closeBtn = bannerItem.find('.close-btn');

    //点击关闭按钮，判断数据库中是否有bannerId
    closeBtn.click(function () {
        var bannerId = bannerItem.attr('data-banner-id');
        if (bannerId) {
            swal({
                    title: "提示",
                    text: "您确定删除这个轮播图吗？",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "确定删除！",
                    closeOnConfirm: false
                },
                function () {
                    xfzajax.post({
                        'url': '/cms/delete_banner/',
                        'data': {
                            'banner_id': bannerId
                        },
                        'success': function (result) {
                            if (result['code'] === 200) {
                                bannerItem.remove();
                                swal("删除！", "该轮播图删除成功！", "success");
                            } else {
                                //显示错误信息
                                swal({
                                    title: result['message'],
                                    timer: 1200,
                                    showConfirmButton: false
                                });
                            }
                        }
                    });

                });
        } else {
            //如果banner是还未创建的，则直接可以移除
            bannerItem.remove();
        }
    })
};


Banners.prototype.addSaveBannerEvent = function (bannerItem) {
    var saveBtn = bannerItem.find('.save-btn');
    var imageTag = bannerItem.find('.thumbnail');
    var priorityTag = bannerItem.find("input[name='priority']");
    var linktoTag = bannerItem.find("input[name='link_to']");

    var prioritySpan = bannerItem.find('span[class="priority"]');

    var bannerId = bannerItem.attr("data-banner-id");
    var url = '';
    //判断是添加还是编辑
    if (bannerId) {
        url = '/cms/edit_banner/';
    } else {
        url = '/cms/add_banner/';
    }
    saveBtn.click(function () {
        var img_url = imageTag.attr('src');
        var priority = priorityTag.val();
        var link_to = linktoTag.val();
        xfzajax.post({
            'url': url,
            'data': {
                'priority': priority,
                'img_url': img_url,
                'link_to': link_to,
                'pk': bannerId
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    if (bannerId) {
                        //有bannerid为修改
                        swal({title: '轮播图修改成功！', type: "success"});
                    } else {
                        //绑定bannerid到标签上
                        bannerId = result['data']['banner_id'];
                        bannerItem.attr('data-banner-id', bannerId);
                        swal({title: '添加成功!', type: "success"});
                    }
                    //修改span标签内的优先级文字
                    prioritySpan.text('优先级:' + priority);
                } else {
                    console.log(result['message'])
                }
            }
        })
    })
};


Banners.prototype.run = function () {
    this.listenAddBannerEvent();
    this.loadData();
};

$(function () {
    var banners = new Banners();
    banners.run();
});