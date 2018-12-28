function PubCourse(){

};

PubCourse.prototype.initUEditor = function () {
    window.ue = UE.getEditor('editor', {
        'initialFrameHeight': 400,
        'serverUrl': '/ueditor/upload',
    });

};

PubCourse.prototype.listenSubmitEvent = function(){
    var submitBtn = $("#submit-btn");
    submitBtn.click(function () {
        var title = $('#title-input').val();
        var category_id = $('#category-form').val();
        var teacher_id = $('#teacher-form').val();
        var video_url = $('#video-form').val();
        var cover_url = $('#cover-form').val();
        var price = $('#price-form').val();
        var duration = $('#duration-form').val();
        var profile = window.ue.getContent();
        console.log(title,teacher_id,profile,duration);
        xfzajax.post({
            'url': '/cms/pub_course/',
            'data': {
                'title': title,
                'category_id':category_id,
                'teacher_id':teacher_id,
                'video_url':video_url,
                'cover_url':cover_url,
                'price':price,
                'duration':duration,
                'profile':profile,

            },
            'success': function (result) {
                if (result['code'] === 200) {
                    swal({title: '发布课程成功！', type: "success"}, function () {
                        window.location = window.location.href;
                    });
                }
            }
        })
    })
};

PubCourse.prototype.run = function (){
    this.initUEditor();
    this.listenSubmitEvent();
};


$(function () {
    var course = new PubCourse();
    course.run();
});