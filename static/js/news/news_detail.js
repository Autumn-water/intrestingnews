/*
  @author: handsomeFu;
  @Date: 2018/10/22 20:42;
*/
$(function () {
  // 获取评论按钮
  let $addCommentBtn = $(".comment-btn");
  // 获取评论框
  let $commentInput = $(".logged-comment").find('input:first-child');
  // 未登录提示框
  let $loginComment = $('.please-login-comment').find('input:first-child');
  // 获取评论外面大盒子
  let $commentList = $(".comment-list");
  // 评论数量
  let $commentCount = $(".comment-count");

  // 点击触发点击事件 发布评论的动作
  $addCommentBtn.click(function () {
    // 获取评论框的值
    let content = $commentInput.val();
    // 获取绑定在按钮上的新闻ID
    let newsId = $(this).data("news-id");
    console.log(`
      评论内容： ${content}
      评论的新闻id: ${newsId}
    `);
    selfAjax('/news/add-comment/', 'post', {"news_id": newsId, "content": content}, res => {
      console.log(res);  // 打印res
      if(res["code"]===2){
        let news_comment = res["data"];
        // 获取新闻评论的创建时间
        let create_time = news_comment["create_time"];
        // 将时间过滤
        let result = dateFormat(create_time);
        // 定义评论的字符串
        let commentStr = `<li class="comment-item">
                 <div class="comment-info clearfix">
                      <img src="/static/images/avatar.jpeg" alt="avatar" class="comment-avatar">
                      <span class="comment-user">${news_comment["author"]["username"]}</span>
                      <span class="comment-pub-time">${result}</span>
                  </div>
                  <div class="comment-content">${news_comment["content"]}</div>
              </li>`;
        $commentList.prepend(commentStr);
        $commentInput.val('');
      }else {
        message.showError(res["msg"]);
      }
    });
  });

  // 一打开页面，就请求返回评论的API接口 获取数据 并展示在页面上
  $.get('/news/comment/?news_id='+$addCommentBtn.data('news-id'), res => {
    // console.log(res);
    if (res["code"] === 2) {
      let newsComments = res["data"];
      console.log(newsComments);
      // 设置评论数量
      $commentCount.text(newsComments.length);
      // 映射新闻成标签
      let newsCommentStr = newsComments.map( item => {
        let result =  dateFormat(item["create_time"]);
        return `<li class="comment-item">
                   <div class="comment-info clearfix">
                        <img src="/static/images/avatar.jpeg" alt="avatar" class="comment-avatar">
                        <span class="comment-user">${item["author"]["username"]}</span>
                        <span class="comment-pub-time">${result}</span>
                    </div>
                    <div class="comment-content">${item["content"]}</div>
                </li>`;
      });
      $commentList.append(newsCommentStr);
    }
  });

  // 登录后在进行评论
  $loginComment.focus(()=>{
    $.post({
      url: '/news/add-comment/',
      success: res => {
        if (res["code"] === 403) {
          window.message.showError(res["msg"]);
          setTimeout(() => {
            window.location.href = '/account/login/';
          }, 2000)
        }
      }
    })
  });
});



