/*
  @author: handsomeFu;
  @Date: 2018/10/17 20:49;
*/

// 生成富文本编辑器  https://www.kancloud.cn/wangfupeng/wangeditor3/332599
let E = window.wangEditor;
window.editor = new E('#news-content');
window.editor.create();
$(function () {
  // ====================  传文件 ============================
  // 获取缩略图输入框元素
  let $thumbnailUrl = $("#news-thumbnail-url");

  // ================== 上传至七牛（云存储平台） ================
  let $progressBar = $(".progress-bar");
  QINIU.upload({
    // 七牛空间域名  空间右侧
    "domain": "http://onj3s3zfw.bkt.clouddn.com/",
    // 后台返回 token的地址 (后台返回的 url 地址) 不可能成功
    "uptoken_url": "/admin/up-token/",
    // 按钮
    "browse_btn": "upload-btn",
    // 成功
    "success": (up, file, info) => {
      let domain = up.getOption('domain');
      let res = JSON.parse(info);
      let filePath = domain + res.key;
      console.log(filePath);
      $thumbnailUrl.val('');
      $thumbnailUrl.val(filePath);
    },
    // 失败
    "error": (up, err, errTip) => {
      console.log('error');
      console.log(up);
      console.log(err);
      console.log(errTip);
      console.log('error');
    },
    // 上传文件的过程中 七牛对于 4M 秒传
    "progress": (up, file) => {
      let percent = file.percent;
      $progressBar.parent().css("display", 'block');
      $progressBar.css("width", percent + '%');
      $progressBar.text(parseInt(percent) + '%');
    },
    // 完成后 去掉进度条
    "complete": () => {
      $progressBar.parent().css("display", 'none');
      $progressBar.css("width", '0%');
      $progressBar.text('0%');
    }
  });
   // ================== 上传至服务器 ================
  let $uploadThumbnail = $("#upload-news-thumbnail");
  $uploadThumbnail.change(function () {
    // 获取文件
    let file = this.files[0];
    // 创建一个 FormData
    let formData = new FormData();
    // 把文件添加进去
    formData.append("upload_file", file);
    // 发送请求
    $.ajax({
      url: "/admin/upload-file/",
      method: "post",
      data: formData,
      // 定义文件的传输
      processData: false,
      contentType: false,
      success: res => {
        console.log(res);
        if (res["code"] === 2) {
          // 获取后台返回的 URL 地址 {x:{c:}}
          let thumbnailUrl = res["data"]["file_url"];
          // console.log(thumbnailUrl);
          $thumbnailUrl.val('');
          $thumbnailUrl.val(thumbnailUrl);
        }
      },
      error: err => {
        logError(err);
      }
    });
  });
  // 发布新闻
   // ========= 发表新闻 ==========
  let $newsBtn = $("#btn-pub-news");
  $newsBtn.click(function () {
    let titleVal = $("#news-title").val();
    let descVal = $("#news-desc").val();
    let tagId = $("#news-category").val();
    let thumbnailVal = $thumbnailUrl.val();
    // html  text
    let contentHtml = window.editor.txt.html();
    let contentText = window.editor.txt.text();
    if (tagId === '0') {
      ALERT.alertInfoToast('请选择新闻标签')
    }
    // console.log(`
    //   新闻标题: ${titleVal},
    //   新闻描述: ${descVal},
    //   新闻分类id: ${tagId},
    //   新闻缩略图地址: ${thumbnailVal}
    //   新闻内容html版: ${contentHtml},
    //   新闻内容纯文字版：${contentText}
    // `);

    // 获取news_id 存在表示更新 不存在表示发表
    let newsId = $(this).data("news-id");
    let url = newsId ? '/admin/news-edit/' : '/admin/news-pub/';
    let data = {
       "title": titleVal,
        "desc": descVal,
        "tag_id": tagId,
        "thumbnail_url": thumbnailVal,
        "content": contentHtml,
    };
    if(newsId){
      data["news_id"] = newsId;
    }

    selfAjax(url, 'post', data, res=>{
      if (res["code"] === 2) {
        if (newsId){
          ALERT.alertNewsSuccessCallback("新闻更新成功", '跳到首页', () => {
            window.location.href = '/';
          });
        } else {
          ALERT.alertNewsSuccessCallback("新闻发表成功", '跳到首页', () => {
            window.location.href = '/';
          });
        }

        } else {
          ALERT.alertErrorToast(res["msg"]);
        }
    });

    // $.ajax({
    //   url: "/admin/news-pub/",
    //   method: "post",
    //   data: {
    //     "title": titleVal,
    //     "desc": descVal,
    //     "tag_id": tagId,
    //     "thumbnail_url": thumbnailVal,
    //     "content": contentHtml,
    //   },
    //   dataType: "json",
    //   success: res => {
    //     // console.log(res);
    //     if (res["code"] === 2) {
    //       ALERT.alertNewsSuccessCallback("新闻发表成功", '跳到首页', () => {
    //         window.location.href = '/';
    //       });
    //     } else {
    //       ALERT.alertErrorToast(res["msg"]);
    //     }
    //   },
    //   error: err => {
    //     logError(err)
    //   }
    // })
  })
});
// 写在