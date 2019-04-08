/*
  @author: handsomeFu;
  @Date: 2018/10/26 13:19;
*/
$(function () {
  // 页面加载成功就自执行
  (async () => {
    // 获取元素
    let $tagSelect = $("#category-select");
    let $newsSelect = $("#news-select");
    // 页面一加载就请求所有的新闻标签
    await $.get('/news/tag/list/', res => {
      if (res["code"] === 2) {
        // 获取新闻标签 [{"id":1}, {"id":2}]
        let tags = res["data"]["tags"];
        // 映射成 ["<option value='1'>标签</option>", "<option value='2'>标签</option>"]
        let newTag = tags.map(tag => `<option value='${tag.id}'>${tag.name}</option>`);
        // 转为字符串
        let tagStr = newTag.join('');
        // 添加至下拉框中 <option value='1'>标签</option>
        $tagSelect.append(tagStr);
      }
    });
    // 加载完新闻标签后就请求所有的新闻
    await $.getJSON('/news/news-with-tag/', {"tag_id": 0,}, res => {
      let data = res["data"];
      if (data) {
        let newses = data["newses"];
        if (newses && newses.length > 0) {
          let newNewses = newses.map(news => `<option value="${news.id}">${news.title}</option>`);
          // :not(option:first-child) 表示忽略第一个 每次切换前移除当前所有新闻（忽略第一个）
          $newsSelect.find(":not(option:first-child)").remove();
          $newsSelect.append(newNewses.join(''))
        }
      } else {
        ALERT.alertErrorToast(res["msg"])
      }
    });
  })();

  // 获取元素
  let $tagSelect = $("#category-select");
  let $newsSelect = $("#news-select");
  let $saveBtn = $('#save-btn');

  // 切换标签 获取对应的新闻
  $tagSelect.change(function () {
    // 获取当前选中的下拉框的value
    let tagId = $(this).val();
    // 根据新闻标签获取到新闻
    $.getJSON('/news/news-with-tag/', {"tag_id": tagId,}, res => {
      let data = res["data"];
      console.log(data);
      if (data) {
        let newses = data["newses"];
        if (newses && newses.length > 0) {
          // 获取新闻并映射
          let newNewses = newses.map(news => `<option value="${news.id}">${news.title}</option>`);
          // :not(option:first-child) 表示忽略第一个 每次切换前移除当前所有新闻（忽略第一个）
          $newsSelect.find(":not(option:first-child)").remove();
          $newsSelect.append(newNewses.join(''))
        }
      } else {
        ALERT.alertErrorToast(res["msg"]);
        $newsSelect.find(":not(option:first-child)").remove();
      }
    })
  });

  // 点击保存按钮执行的事件
  $saveBtn.click(() => {
    // 获取优先级
    let priority = $("#priority").val();
    // 获取下拉框中选中的新闻标签id 和 新闻 id
    let tagId = $tagSelect.val();
    let newsId = $newsSelect.val();
    // 打印值
    console.log(`
          priority(优先级): ${priority}
          tagId(新闻标签id): ${tagId}
          newsId(新闻id): ${newsId}
    `);
    // 判断是否为 0, 表示在第一个 未选择
    if (tagId !== '0' && newsId !== '0') {
      if (priority && priority !== '0') {
        // 前端向后台发送 news_id 以及 priority 两个key
        selfAjax('/admin/news-hot-add/', 'post', {"news_id": newsId, "priority": priority}, res => {
          if (res["code"] === 2) {
            swal({
              title: "添加热门新闻成功",
              type: "success",
              confirmButtonText: "确定",
            }, function () {
              // 点击确定之后执行的事件 // document.referrer 回到你上次进去这个页面的地址
              window.location.href = document.referrer;
            });
          } else {
            ALERT.alertErrorToast(res["msg"]);
          }
        });
      } else {
        ALERT.alertErrorToast("优先级不能为空");
      }
    } else {
      ALERT.alertErrorToast("新闻分类与新闻都要选中");
    }
  });
});