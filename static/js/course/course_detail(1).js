/*
  @author: handsomeFu;
  @Date: 2018/10/30 21:26;
*/
// 动态获取
let $courseData = $(".course-data");
let videoUrl = $courseData.data('video-url');
let coverUrl = $courseData.data('cover-url');
console.log(videoUrl);
console.log(coverUrl);
 let player = cyberplayer("course-video").setup({
    width: '100%', // 高度
    height: 650, // 宽度
    file: videoUrl, // 地址
    image: coverUrl, //预览图
    autostart: false, // 自动播放
    stretching: "exactfit", // 缩放方式，缩放方式分为：1.none:不缩放；2.uniform:添加黑边缩放；3. exactfit:改变宽高比缩到最大；4.fill:剪切并缩放到最大（默认方式为uniform）
    repeat: false, // 重复播放
    volume: 77, // 音量 0 -100
    controls: 'over', // 控制条显示
    tokenEncrypt: true,
    ak: 'e38750744ef042ba8c21168739934013', // AccessKey
  });
  // 播放前
  player.on('beforePlay', (e) => {
    // 判断文件是否加密
    if(!/m3u8/.test(e.file)){
      return false;
    }
    $.get({
      "url": "/course/token/",
      "data": {
        "video_url": videoUrl,
      },
      "success": res => {
        let token = res['token'];
        player.setToken(e.file, token)
      },
      "error": err => {
        console.log(err);
        console.log(err.status + "====" + err.statusText);

      }
    });
  });