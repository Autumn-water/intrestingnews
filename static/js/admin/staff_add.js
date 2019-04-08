/*
  @author: handsomeFu;
  @Date: 2018/10/31 21:52;
*/
$(() => {
  // 获取元素
  let $saveBtn = $("#save-btn");
  $saveBtn.click(function (ev) {
    ev.preventDefault();
    let telephone = $("#telephone").val();
    let $groups = $("input[name=groups]");
    let tmpArr = [];
    // 遍历添加选中的多选框进入数组
    for (let i = 0; i < $groups.length; i++) {
      if ($groups[i].checked) {
        tmpArr.push($groups[i].value);
      }
    }
    if (tmpArr.length<1) {
      ALERT.alertErrorToast("至少选择一个部门");
      return false
    }
    $.post({
      "url": "/admin/staff-add/",
      "data": {
        "telephone": telephone,
        "groups": tmpArr,
      },
      // 上传复选必备属性
      'traditional': true,
      "success": res => {
        if (res["code"] === 2) {
          swal({
              title: "分组添加成功",
              type: "success",
              confirmButtonText: "确定",
            }, function () {
              // 点击确定之后执行的事件 // document.referrer 回到你上次进去这个页面的地址
              window.location.href = document.referrer;
            });
        } else {
          ALERT.alertErrorToast(res["msg"])
        }
      },
      "error": err => {
		logError(err);
      }
    })
  });
});