/*
  @author: handsomeFu;
  @Date: 2018/10/24 21:12;
*/
$(function () {
  let startTime = $("input[name=start_time]");
  let endTime = $("input[name=end_time]");
  const config = {
    // 自动关闭
    autoclose: true,
    // 日期格式
    format: 'yyyy/mm/dd',
    // 选择语言为中文
    language: 'zh-CN',
    // 优化样式
    showButtonPanel: true,
    // 高亮今天
    todayHighlight: true,
    // 是否在周行的左侧显示周数
    calendarWeeks: true,
    // 清除
    clearBtn: true,
    // 0 ~11  网站上线的时候
    startDate: new Date(2018, 7, 20),
    // 今天
    endDate: new Date(),
  };
  startTime.datepicker(config);
  endTime.datepicker(config);

  // 删除按钮的操作
  // 1. 获取按钮
  let $delBtn = $(".btn-del");
  // 2. 触发事件
  $delBtn.click(function () {
    // 2.1 获取绑定在删除按钮上的 新闻 id
    let newsId = $(this).data("news-id");
    swal({
      title: "确定删除新闻吗",
      text: "删除之后，你将无法恢复哦",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: "确定删除",
      cancelButtonText: "取消",
      closeOnConfirm: false,
      animation: 'slide-from-top',
    }, () => {
      // 2.2 发起请求
      selfAjax('/admin/news-manage/', 'delete', {"news_id": newsId}, res => {
        if (res["code"] === 2) {
          swal({
            title: "删除",
            type: "success",
          }, () => {
            $(this).parents('tr').remove();
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

  });
});