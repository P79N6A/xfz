function News() {
    this.progressGroup = $("#progress-group");
};

News.prototype.initUEditor = function () {
    window.ue = UE.getEditor('editor', {
        'initialFrameHeight': 400,
        'serverUrl': '/ueditor/upload',
    });

};

News.prototype.listenUploadFileEvent = function () {
    //上传到自己的服务器
    var uploadBtn = $('#thumbnail-btn');

    uploadBtn.change(function () {
        //上传按钮上可以有多个文件
        var file = uploadBtn[0].files[0];
        var formData = new FormData();
        formData.append('file', file);
        xfzajax.post({
            'url': '/cms/upload_file/',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if (result['code'] === 200) {
                    var url = result['data']['url'];
                    var thumbnailInput = $('#thumbnail-form');
                    thumbnailInput.val(url);
                }
            }
        })
    });
};

News.prototype.listenQiniuUploadFileEvent = function () {
    //上传到七牛云服务器
    var self = this;
    var uploadBtn = $('#thumbnail-btn');
    uploadBtn.change(function () {
        var progressBar = $('.progress-bar');
        progressBar.css({'width': 0});
        var file = this.files[0];
        xfzajax.get({
            'url': '/cms/qntoken/',
            'success': function (result) {
                if (result['code'] !== 200) {
                    //显示错误信息
                    swal({
                        title: result['message'],
                        text: "2秒后自动关闭。",
                        timer: 2000,
                        showConfirmButton: false
                    });
                } else {
                    var token = result['data']['token'];
                    //a.jpg = ['a':'jpg']
                    var key = (new Date()).getTime() + '.' + file.name.split('.')[1];
                    var putExtra = {
                        fname: key,
                        params: {},
                        mimeType: ['image/png', 'image/jpg', 'image/gif'],
                    };
                    var config = {
                        useCdnDomain: true,
                        retryCount: 6,
                        region: qiniu.region.z0
                    };
                    var observable = qiniu.upload(file, key, token, putExtra, config);
                    observable.subscribe({
                        'next': self.handleFileUploadProgress,
                        'error': self.handleFileUploadError,
                        'complete': self.handleFileUploadComplete,
                    });
                }
            }
        })
    })
};

News.prototype.handleFileUploadProgress = function (response) {
    var total = response.total;
    var percent = total.percent;
    var percentText = percent.toFixed(0) + '%';
    console.log(percent);
    var progressGroup = $('#progress-group');
    progressGroup.show();
    var progressBar = $('.progress-bar');
    progressBar.css({'width': percent + '%'});
    progressBar.text(percentText);
};

News.prototype.handleFileUploadError = function (error) {
    console.log(error.message);
    swal({
        title: result['message'],
        text: "",
        timer: 2000,
        showConfirmButton: false
    });
    var progressGroup = $('#progress-group');
    progressGroup.hide();
};

News.prototype.handleFileUploadComplete = function (response) {
    console.log(response);
    var progressGroup = $('#progress-group');
    progressGroup.hide();

    //域名 七牛上
    var domain = 'http://7xqeu.com1.z0.glb.clouddn.com/';
    var filename = response.key;
    var url = domain + filename;
    var thumbnailInput = $("input[name='thumbnail']");
    thumbnailInput.val(url);
};

News.prototype.listenSubmitEvent = function () {
    var submitBtn = $('#submit-btn');
    submitBtn.click(function (event) {
        event.preventDefault();
        var btn = $(this);
        var pk = btn.attr('data-news-id');

        var title = $('input[name="title"]').val();
        var category = $('select[name="category"]').val();
        var desc = $("input[name='desc']").val();
        var thumbnail = $('input[name="thumbnail"]').val();
        var content = window.ue.getContent();

        var url = '';
        var alertMessage = '';
        if(pk){
            url='/cms/edit_news/';
            alertMessage = '新闻编辑成功！'
        }else{
            url='/cms/write_news/';
            alertMessage = '新闻发布成功！'
        }
        xfzajax.post({
            'url': url,
            'data': {
                'title': title,
                'category': category,
                'desc': desc,
                'thumbnail': thumbnail,
                'content': content,
                'pk':pk
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    swal({title: alertMessage, type: "success"}, function () {
                        window.location.reload();
                    });
                }
            }
        })
    })
};

News.prototype.run = function () {
    var self = this;
    self.listenUploadFileEvent();
    // self.listenQiniuUploadFileEvent();
    self.initUEditor();
    self.listenSubmitEvent();
};


$(function () {
    var news = new News();
    news.run();

    News.progressGroup = $('#progress-group');
});