$(function () {
    /*=== bannerStart ===*/
    let $banner = $('.banner');
    let $picLi = $(".banner .pic li");
    let $prev = $('.banner .prev');
    let $next = $('.banner .next');
    let $tabLi = $('.banner .tab li');
    let index = 0;
    // 小原点
    $tabLi.click(function () {
        index = $(this).index();
        $(this).addClass('active').siblings('li').removeClass('active');
        $picLi.eq(index).fadeIn(1500).siblings('li').fadeOut(1500);
    });
    // 点击切换上一张
    $prev.click(() => {
        index--;
        if (index < 0) {
            index = $tabLi.length - 1
        }
        $tabLi.eq(index).addClass('active').siblings('li').removeClass('active');
        $picLi.eq(index).fadeIn(1500).siblings('li').fadeOut(1500);
    }).mousedown(() => false);
    // 点击切换下一张
    $next.click(() => {
        auto();
    }).mousedown(() => false);

    //  图片向前滑动
    function auto() {
        index++;
        index %= $tabLi.length;
        $tabLi.eq(index).addClass('active').siblings('li').removeClass('active');
        $picLi.eq(index).fadeIn(3000).siblings('li').fadeOut(3000);
    }

    // 定时器
    let timer = setInterval(auto, 3000);
    $banner.hover(() => {
        clearInterval(timer)
    }, () => {
        auto()
    });
    /*=== bannerEnd ===*/

    /*=== newsNavStart ===*/
    let $newsLi = $('.news-nav ul li');
    $newsLi.click(function (event) {
        $(this).addClass('active').siblings('li').removeClass('active');
    })
    /*=== newsNavEnd ===*/

      // ========== 获取元素 ========
  // content 盒子
  let $content = $(".content");
  // newsContain 盒子
  let $newsContain = $(".news-contain");
  // 加载更多的按钮
  let $moreBtn = $("#btn-more");
  // 获取新闻列表
  let $newsList = $(".news-list");
  // 获取所有的新闻分类
  let $li = $('.news-nav ul li');

  // 将jq 对象转为 js 对象 使用原生 JS 是 addEventListener 注册点击事件
  $moreBtn[0].addEventListener('click', function () {
    // 添加一个 loading
    $newsContain.append(`<div class="loading-img"></div>`);
    // 获取loading
    let $loadImg = $(".loading-img");
    // 找到已经被激活的新闻分类下面的 a 标签
    let tagId = $('.news-nav ul li.active').children('a').data("id");
    // 获取绑定在按钮上的页码
    let page= $(this).data("page");
    // 打印值
    console.log(`
      当前所处在分类id  ${tagId}
      当前第几页  ${page}    
    `);
    // 发起 get 的请求 也可以写成 $.get(`/news/list/?page=${page}&tag_id=${tagId}`, res=>{}) 方式
    $.get({
      // 请求的 url
      url: "/news/list/",
      // 发送的数据
      data: {
        "page": page,
        "tag_id": tagId,
      },
      // 成功之后的回调函数
      success: res => {
        if (res["code"] === 2) {
          // 获取数据
          let data = res["data"];
          // 获取新闻列表
          let newses = data["newses"];
          if (newses.length > 0) {
            // 遍历
            newses.forEach((news) => {
              // console.log(news);
              // 获取新闻发布时间
              let pub_time = news["pub_time"];
              // 格式化新闻发布时间
              let result = dateFormat(pub_time);
              let newsStr = `
                <li class="news-item">
                  <a href="/news/detail/${news.id}" class="news-thumbnail" target="_blank">
                    <img src="${news.thumbnail_url}" alt="title" title="${news.title}">
                  </a>
                  <div class="news-content">
                    <h4 class="news-title"><a href="/news/detail/${news.id}">${news.title}</a></h4>
                    <p class="news-details">${news.desc}</p>
                    <div class="news-other">
                      <span class="news-type">${news.tag.name}</span>
                      <span class="news-time">${result}</span>
                      <span class="news-author">${news.author.username}</span>
                    </div>
                  </div>
                </li>
              `;
              $newsList.append(newsStr);
            })
          } else {
            // 如果点击加载更多 已无新闻 则移除自己
            $(this).remove();
          }
          // 移除 loading
          $loadImg.remove();
        }
        // 点一次 page +1 并绑定到data-page 上
        page ++; // page
        $(this).data("page", page);
      },
      error: err => {
        logError(err);
      }
    })
  });


  // 点击切换分类执行的时间
  $li.click(function () {
    // 点击那个 则为点击的加上一个class名字 active 并移除其它兄弟元素的上的 class名字是active的
    $(this).addClass('active').siblings('li').removeClass('active');
    // 获取绑定在当前选中分类上的 id字段
    let tagId = $(this).children('a').data('id');
    // 设置点击加载更多的默认值为2
    $moreBtn.data("page", 2);
    // 发起 get 请求
    $.get({
      url: "/news/list/",
      data: {
        "tag_id": tagId,
      },
      success: res => {
        if (res["code"] === 2) {
          let data = res["data"];
          let newses = data["newses"];
          // 每次加载前提前清空当前分类下的所有新闻
          $newsList.children().remove();
          if (newses.length > 0) {
            newses.forEach(news => {
              let pub_time = news["pub_time"];
              let result = dateFormat(pub_time);
              // `` 模板字符串 ${news.title}
              let newsStr = `
                <li class="news-item">
                  <a href="/news/detail/${news.id}" class="news-thumbnail" target="_blank">
                    <img src="${news.thumbnail_url}" alt="title" title="${news.title}">
                  </a>
                  <div class="news-content">
                    <h4 class="news-title"><a href="/news/detail/${news.id}">${news.title}</a></h4>
                    <p class="news-details">${news.desc}</p>
                    <div class="news-other">
                      <span class="news-type">${news.tag.name}</span>
                      <span class="news-time">${result}</span>
                      <span class="news-author">${news.author.username}</span>
                    </div>
                  </div>
                </li>
              `;
              $newsList.append(newsStr);
              $content.append($moreBtn);
            })
          } else {
            $moreBtn.remove();
          }
        }
      }
    })
  });

});