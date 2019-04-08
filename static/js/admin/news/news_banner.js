/*
  @author: handsomeFu;
  @Date: 2018/10/29 21:22;
*/
$(function () {
  // 页面一加载 请求api 接口返回数据
  (async () => {
    await $.get('/news/banner/list/', res => {
      let banners = res["data"]["banners"];
      banners.forEach(banner => {
        createBannerItem(banner);
      });
    });
  })();

  // 添加按钮
  let $bannerAddBtn = $("#banner-add-btn");
  // 包着所有轮播图的外部盒子
  let $bannerList = $(".banner-list");

  // 点击添加轮播的按钮执行的事件
  $bannerAddBtn.click(function () {
    $bannerList.find('li').length < 6 ? createBannerItem() : ALERT.alertInfoToast("最多只能添加6个哦")
  });

  // 关闭轮播图 意味着删除
  function closeBanner(bannerItem) {
    let $closeBtn = bannerItem.find(".close-btn");
    $closeBtn.click(function () {
      let bannerId = bannerItem.data("banner-id");
      ALERT.alertConfirm({
        "title": "删除轮播图",
        "type": "error",
        "confirmText": "确认",
        "confirmCallback": () => {
          selfAjax("/admin/news-banner/", 'delete', { "banner_id": bannerId}, res=>{
             if (res["code"] === 2) {
                ALERT.alertSuccessToast("删除成功");
                bannerItem.remove();
              } else {
                ALERT.alertErrorToast(res["msg"])
              }
          });
        }
      })
    });
  }

  // 上传轮播图片
  function uploadBannerImg(bannerItem) {
    let $bannerImage = bannerItem.find(".banner-image");
    let $bannerImageSelect = bannerItem.find('input[name=banner-image-select]');
    $bannerImage.click(function () {
      $bannerImageSelect.click();
    });
    $bannerImageSelect.change(function () {
      // 获取文件对象
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
            // 获取后台返回的 URL 地址
            let url = res["data"]["file_url"];
            $bannerImage.attr('src', url);
          }
        },
        error: err => {
          logError(err);
        }
      });
    })
  }

  // 保存轮播图
  function saveBanner(bannerItem) {
    // 保存按钮
    let $saveBtn = bannerItem.find(".save-btn");
    $saveBtn.click(function () {
      // 获取元素
      let imageUrl = bannerItem.find('.banner-image').attr("src");
      let priority = bannerItem.find('input[name="priority"]').val();
      let linkTo = bannerItem.find('input[name="link_to"]').val();
      let bannerId = bannerItem.data("banner-id");
      let priorityNum  = bannerItem.find('.priority-number');
      console.log(`
        图片地址(imageUrl): ${imageUrl},
        优先级(priority): ${priority},
        跳转地址(linkTo): ${linkTo},
        bannerId: ${bannerId}
      `);
      // 三目取值 有bannerId 表示为更新 put 方式 反之 post创建
      let method = bannerId ? "put" : "post";
      let data = {
        "image_url": imageUrl,
        "priority": priority,
        "link_to": linkTo,
      };
      if (bannerId) {
        data["banner_id"] = bannerId
      }
      selfAjax("/admin/news-banner/", method, data, res=>{
        if (res["code"] === 2) {
          if (bannerId) {
            ALERT.alertSuccessToast("更新成功");
            priorityNum.text(priority);
          } else {
            ALERT.alertSuccessToast("添加成功");
            let bannerId = res["data"]["banner_id"];
            bannerItem.data("banner-id", bannerId);
            priorityNum.text(res["data"]["priority"]);
          }
        }else {
          ALERT.alertErrorToast(res["msg"])
        }
      });
    })
  }

  function createBannerItem(banner) {
    let $bannerItem = null;
    let bannerStr = null;
    // 如果有 banner 表示更新
    if (banner) {
      bannerStr = `<li class="box banner-item box-primary" data-banner-id="${banner.id}">
        <div class="box-header">
          <span>优先级：<span class="priority-number">${banner.priority}</span></span>
          <a href="javascript:void(0);" class="btn btn-danger btn-xs pull-right close-btn"><i class="fa fa-close"></i></a>
        </div>
        <div class="box-body">
          <div class="pull-left banner-img">
            <input type="file" name="banner-image-select" style="display: none;">
            <img src="${banner.image_url}" class="img-thumbnail banner-image">
          </div>
          <div class="pull-left banner-info">
            <div class="form-group">
              <input type="number" placeholder="请输入优先级" class="form-control" name="priority" value="${banner.priority}">
            </div>
            <div class="from-group">
              <input type="url" placeholder="请输入跳转的网址" class="form-control" name="link_to" value="${banner.link_to}">
            </div>
          </div>
        </div>
        <div class="box-footer">
          <button class="btn btn-primary pull-right save-btn">更新</button>
        </div>
      </li>`;
      $bannerList.append(bannerStr);
      $bannerItem = $bannerList.find('.banner-item:last-child')
    } else {
      bannerStr = `<li class="box banner-item box-primary">
        <div class="box-header">
          <span>优先级：<span class="priority-number">0</span></span>
          <a href="javascript:void(0);" class="btn btn-danger btn-xs pull-right close-btn"><i class="fa fa-close"></i></a>
        </div>
        <div class="box-body">
          <div class="pull-left banner-img">
            <input type="file" name="banner-image-select" style="display: none;">
            <img src="/static/images/banner_default.png" class="img-thumbnail banner-image">
          </div>
          <div class="pull-left banner-info">
            <div class="form-group">
              <input type="number" placeholder="请输入优先级" class="form-control" name="priority">
            </div>
            <div class="from-group">
              <input type="url" placeholder="请输入跳转的网址" class="form-control" name="link_to">
            </div>
          </div>
        </div>
        <div class="box-footer">
          <button class="btn btn-primary pull-right save-btn">保存</button>
        </div>
      </li>`;
      $bannerList.prepend(bannerStr);
      $bannerItem = $bannerList.find(".banner-item:first-child");
    }

    // 调用函数  关闭轮播图
    closeBanner($bannerItem);
    // 调用函数 上传图片
    uploadBannerImg($bannerItem);
    // 调用函数 保存 banner
    saveBanner($bannerItem);
  }
});