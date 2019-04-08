$(function () {
  let $loginBtn = $(".login-btn");
  $loginBtn.click(function (ev) {
    ev.preventDefault(); // 关闭元素默认事件
    // 验证会做两层 前端防止频繁的发送请求
    let telVal = $("input[name=telephone]").val();
    let pwdVal = $("input[name=password]").val();
    let $remember = $("input[name=remember]");
    // console.log(`${telVal}, ${pwdVal}`)
    if (telVal && pwdVal) {
      // 获取 点击 单选框的状态  勾 true 没勾 false
    let status = $remember.is(":checked");
      let data = {
          "telephone": telVal,
          "password": pwdVal,
        };
      if(status){
        data["remember"] = status;
      }
      console.log(data);
      // 发送请求
      $.ajax({
        url: "/account/login/",
        method: "post",
        data: data,
        dataType: "json",
        // => function
        success: res => {
          // console.log('success');
          console.log(res); // return JsonResponse 并不会展示在页面 通过ajax
          if (res["code"] === 2) {
            // 这里写成功之后执行代码   以后前端我全部写好 上课直接复制 后台代码慢慢讲
            message.showSuccess("登录成功");
            setTimeout(() => {
              window.location.href = '/';
            }, 2500);
          } else {
            message.showError(res["msg"]);
          }
        },
        error: err => {
          // // 当 ajax 出现问题的时候 返回
          // console.log('error');
          // console.log(err);
          logError(err);
        }
      })
    } else {
      message.showError("手机号和密码不能为空");
    }
  });

  let $graphCaptchaBtn = $(".form-item .captcha-graph-img");
  let $captchaImg = $graphCaptchaBtn.find('img');
  // 刷新图形验证码  没有必要太纠结
  $graphCaptchaBtn.click(function () {
    let oldSrc = $captchaImg.attr('src');
    let newSrc = oldSrc.split("?")[0] + "?_=" + Date.now();
    $captchaImg.attr('src', newSrc);
  });

  // 获取元素
  let $smsCaptchaBtn = $(".form-item .sms-captcha");
  let $telephone = $("input[name=telephone]");
  let reg = /^((1[3-9][0-9])+\d{8})$/; // 判断手机号
   // 发送短信验证码
  $smsCaptchaBtn.click(function () {
    let _this = $(this); // 提前保存 this  扎实的基础
    let $status = $(this)[0].hasAttribute('disabled');
    if ($status) {
      message.showInfo("验证码已经发送，请注意查收");
      return false
    }
    let telVal = $telephone.val();
    if (telVal && telVal.trim()) {
      if (reg.test(telVal)) {
        $.ajax({
          url: "/account/sms-captcha/",
          method: "get",
          data: {
            "telephone": telVal,
          },
          success: (res) => {
            console.log(res);  // {"Message":"触发分钟级流控Permits:1","RequestId":"EEB9718A-6039-46C2-B787-0409E6703B0B","Code":"isv.BUSINESS_LIMIT_CONTROL"}
            console.log(typeof res);
            // stringify  JS对象转成 标准Json 格式
            // 可以把 字符串 Json 转为 JS 对象
            // res 必须是 json 格式的字符串 对象 直接报错
            // let resObj = JSON.parse(res);
            // Message 是有阿里云提供

            // if(res["Code"] === "OK"){
            //   // message.showSuccess(resObj["Message"]);
            //   message.showSuccess(resObj["发送成功"]);
            // }else if(res["Code"] === 'isv.BUSINESS_LIMIT_CONTROL'){
            //     // 手机号发送次数 上限制
            //   message.showSuccess(resObj["Message"])
            // }
            let count = 60; // 控制几秒
            console.log('======');
            console.log($(this));
            console.log(_this);
            console.log('======');
            let $text = _this.text();
            _this.attr('disabled', true);
            let timer = setInterval(function(){
              _this.text(count);
              count--;
              if (count <= 0) {
                clearInterval(timer);
                _this.text($text);
                _this.removeAttr('disabled');
              }
            }, 1000);
          },
          error: err => {
            logError(err);
          }
        })
      } else {
        message.showError('手机号格式不正确');
        $telephone.focus();
      }
    } else {
      message.showError('请输入手机号');
      $telephone.focus();
    }
  });

  // 注册
  // 注册按钮
  let $regBtn = $(".register-btn");
  // 获取元素
  let $smsCaptcha = $("input[name=sms_captcha]");
  let $username = $("input[name=username]");
  let $password = $("input[name=password]");
  let $passwordRepeat = $("input[name=password_repeat]");
  let $graphCaptcha = $("input[name=captcha_graph]");
  $regBtn.click(function () {
    // 获取值
    let telVal = $telephone.val();
    let smsCaptchaVal = $smsCaptcha.val().toLowerCase(); // 转为
    let userVal = $username.val();
    let pwdVal = $password.val();
    let pwdRepeatVal = $passwordRepeat.val();
    let graphCaptchaVal = $graphCaptcha.val().toLowerCase();
    // `${变量名}` !==  '' +变量名+''
    // console.log(`1 ${telVal}  2 ${smsCaptchaVal} 3 ${userVal} 4 ${pwdVal} 5 ${pwdRepeatVal} 6 ${graphCaptchaVal}`);
     $.post({
      url: "/account/register/",
      data: {
        "telephone": telVal,
        "sms_captcha": smsCaptchaVal,
        "username": userVal,
        "password": pwdVal,
        "password_repeat": pwdRepeatVal,
        "graph_captcha": graphCaptchaVal,
      },
      success: res => {
        console.log(res);
        if (res["code"] === 2) {
          window.message.showSuccess("注册成功");
          setTimeout(() => {
            window.location.href = '/';
          }, 1500)
        } else {
          window.message.showError(res["msg"])
        }
      },
      error: err => {
        logError(err)
      }
    })
  });
});