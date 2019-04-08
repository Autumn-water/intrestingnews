// var url = "/admin/news-tag-manage/";

// 添加新闻标签
// 1. 获取按钮
var $tagAdd = $("#btn-add-tag");
// 2. 点击事情
$tagAdd.click(function () {
  ALERT.alertOneInput({
    title: "请输入新闻标签",
    text: "长度限制在20字以内",
    placeholder: "请输入新闻标签",
    confirmCallback: function confirmCallback(inputVal) {
      console.log(inputVal);
      $.ajax({
        url: url,
        method: "post",
        // data  === 数据 前后交互的数据
        data: {
          "name": inputVal
        },
        dataType: "json",
        success: function success(res) {
          console.log(res);
          if (res["code"] === 2) {
            // console.log('success');
            ALERT.alertSuccessToast(inputVal + " 标签添加成功");
            setTimeout(function () {
              window.location.reload();
            }, 1500)
          } else {
            swal.showInputError(res["msg"]);
          }
        },
        error: function error(err) {
          logError(err);
        }
      });
    }
  });
});

// 编辑新闻标签
// 1. 获取按钮
var $tagEdit = $(".btn-edit");
// 2. 点击触发事件
$tagEdit.click(function () {
  var tagId = getTagId(this);
  var tagName = getTagName(this);
  console.log(tagId);
  console.log(tagName);
  // fAlert ALERT is not defined
  ALERT.alertOneInput({
    title: "编辑新闻标签",
    // `${}` ""/''  模板字符串  `你正在编辑 ${tagName} 标签`
    text: "你正在编辑 " + tagName + " 标签",
    placeholder: "请输入新闻标签",
    value: tagName,
    confirmCallback: (inputVal) =>{
      if (inputVal === tagName) {
        swal.showInputError('标签名未变化');
        return false;
      }
      $.ajax({
        // url edit_news_tag url
        url: url,
        method: 'put',
        data: {
          "tag_id": tagId,
          "tag_name": inputVal
        },
        dataType: "json",
        success: (res)=> {
          // console.log(res);
          if(res["code"]===2){
            message.showSuccess("修改成功");
            // console.log($(this).parents('tr').find('td:nth-child(1)'));
            // 昨天tagName已经存在和原有的值一模一样 昨天没看到效果
            $(this).parents('tr').find('td:nth-child(1)').text(inputVal);
            swal.close();
            // setTimeout(function () {
            //     window.location.reload();
            // }, 1500);
          }else {
            swal.showInputError(res["msg"])
          }
        },
        error: function error(err) {
          logError(err);
        }
      });
    }
  });
});

// 删除新闻标签
// 1. 获取按钮
var $tagDel = $(".btn-del");
// 2. 点击触发事件
$tagDel.click(function () {
  var _this = this;

  var tagId = getTagId(this);
  var tagName = getTagName(this);
  ALERT.alertConfirm({
    title: "您确定要删除" + tagName + "标签吗",
    type: "error",
    confirmText: "确认删除",
    cancelText: "取消删除",
    confirmCallback: function confirmCallback() {
      $.ajax({
        url: url,
        method: "delete",
        data: {
          "tag_id": tagId
        },
        dataType: "json",
        success: function success(res) {
          console.log(res);
          if (res["code"] === 2) {
            window.message.showSuccess("删除成功");
            $(_this).parent().parent().remove();
          } else {
            swal.showInputError(res["msg"]);
          }
        },
        error: function error(err) {
          logError(err);
        }
      });
    }
  });
});

function getTagId(elem) {
  return $(elem).parents('tr').data('id');
}

function getTagName(elem) {
  return $(elem).parents('tr').find('td:nth-child(1)').text();
}