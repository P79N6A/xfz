function CourseDetail() {

}

CourseDetail.prototype.initPlayer = function () {
    var videoInfoSpan = $("#video-info");
    var video_url = videoInfoSpan.attr("data-video-url");
    var cover_url = videoInfoSpan.attr("data-cover-url");


    var myPlayer = cyberplayer("playercontainer").setup({
        width: '100%',
        height: '100%',
        file: video_url,
        image: cover_url,
        autostart:false,
        tokenEncrypt: "true",
        repeat: false,
        stretching: "uniform",
        volume: 100,
        ak: 'ff914c1b266c4cbbbbd86b457bc10cc4',
    });
    myPlayer.on('beforePlay', function (e) {
        if (!/m3u8/.test(e.file)) {
            return;
        }
        xfzajax.get({
            'url': '/course/course_token/',
            'data': {
                'video': video_url
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var token = result['data']['token'];
                    myPlayer.setToken(e.file, token);
                } else {
                    alert('token错误!');
                }
            },
            'fail': function (error) {
                console.log(error)
            }
        })
    })
};

CourseDetail.prototype.run = function () {
    this.initPlayer();
};


$(function () {
    var courseDetail = new CourseDetail();
    courseDetail.run();
});