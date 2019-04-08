/*
  @author: handsomeFu;
  @Date: 2018/10/26 17:05;
*/
$(function () {
  // 页面一加载 就请求数据 函数自执行
  (async () => {
    // 获取 表格主体部分
    let $tBody = $("table.table tbody");
    // 页面一加载就请求所有的新闻标签
    await $.get('/news/hot/list/', res => {
      if (res["code"] === 2) {
        // 获取数据
        let hot_newses = res["data"];
        // 映射成字符串
        let hot_newses_arr = hot_newses.map(hot_news => `
          <tr>
            <td>
              <a href="javascript:void(0);" data-news-id="${hot_news.news.id}">${hot_news.news.title}</a>
            </td>
            <td>${hot_news.news.tag.name}</td>
            <td>${hot_news.priority}</td>
            <td>
              <a href="javascript:void(0);" class="btn btn-xs btn-warning btn-edit"
                 data-priority="${hot_news.priority}">编辑</a>
              <a href="javascript:void (0);" class="btn btn-xs btn-danger btn-del"
                 data-hot-id="${hot_news.id}">删除</a>
            </td>
          </tr>`
        );
        $tBody.append(hot_newses_arr.join(''));
      }
    });
    // 获取编辑按钮和删除按钮
    let editBtnDomArr = document.querySelectorAll('.btn-edit');
    let delBtnDomArr = document.querySelectorAll('.btn-del');
    // 遍历获取所有编辑按钮
    for (let editBtnDom of editBtnDomArr) {
      // 注册点击事件
      editBtnDom.addEventListener('click', function () {
        // 获取优先级
        let priority = this.getAttribute('data-priority');
        // 获取热门新闻 id
        let hotNewsId = this.nextElementSibling.getAttribute('data-hot-id');

        // sweetAlert 的弹窗
        swal({
          // 标题
          title: "编辑热门新闻优先级",
          // 输入框类型
          type: 'input',
          // 显示取消按钮
          showCancelButton: true,
          // 动画效果
          animation: 'slide-from-top',
          closeOnConfirm: false,
          showLoaderOnConfirm: true,
          inputPlaceholder: "请输入优先级",
          inputValue: priority,
          confirmButtonText: "确定修改",
          cancelButtonText: "取消",
        }, (inputValue) => {
          if (!inputValue.trim()) {
            swal.showInputError('输入框不能为空！');
            return false;
          } else if (inputValue === priority) {
            swal.showInputError('未修改');
            return false;
          }
          // 发起 ajax 请求 前端向后台发送 priority(优先级) 和 hot_news_id 热门新闻 id
          selfAjax('/admin/news-hot/', 'put', {"priority": inputValue, "hot_news_id": hotNewsId}, res => {
            if (res["code"] === 2) {
              // 弹出成功提示框
              swal({
                title: "新闻优先级修改成功",
                type: "success",
              }, () => {
                // 直接修改优先级
                this.parentElement.previousElementSibling.innerText = inputValue;
              })
            } else {
              swal({
                title: res["msg"],
                type: "error",
                timer: 1500,
                showCancelButton: false,
                showConfirmButton: false,
              })
            }
          })
        })
      })
    }

    // 遍历获取所有的删除按钮
    delBtnDomArr.forEach(denBtn => {
      // 注册点击事件
      denBtn.addEventListener('click', function () {
        // 获取热门新闻 id
        let hotNewsId = this.getAttribute('data-hot-id');
        swal({
            title: "确定删除热门新闻吗?",
            text: "删除之后，你将无法恢复",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "确定删除",
            cancelButtonText: "取消",
            closeOnConfirm: false,
            animation: 'slide-from-top',
          }, () => {
            // 发起ajax请求 携带 hot_news_id 热门新闻id
            selfAjax('/admin/news-hot/', 'delete', {"hot_news_id": hotNewsId}, res => {
              if (res["code"] === 2) {
                swal({
                  title: "删除",
                  type: "success",
                }, () => {
                  let el = document.querySelector('table.table tbody');
                  el.removeChild(this.parentElement.parentElement);
                });
              } else {
                swal({
                  title: res["msg"],
                  type: "error",
                  timer: 1500,
                  showCancelButton: false,
                  showConfirmButton: false,
                })
              }
            });
          });
      })
    })
  })();
});