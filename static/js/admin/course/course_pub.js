/*
  @author: handsomeFu;
  @Date: 2018/10/29 22:23;
*/
$(function () {
  // 创建编辑器
  let E = window.wangEditor;
  window.courseOutline = new E('#course-outline');
  window.courseOutline.create();

  // 发布课程
  let $coursePubBtn = $(".course-pub-btn");
  // 获取元素
  let $courseTitle = $("#course-title");
  let $courseVideoUrl = $("#course-video");
  let $courseTeacher = $("#course-teacher");
  let $courseDuration = $("#course-duration");
  let $courseProfile = $("#course-profile");
  let $courseCategory = $("#course-category");
  let $courseCover = $("#course-cover");
  $coursePubBtn.click(function () {
    // 获取值 等你点击的时候
    let courseTitle = $courseTitle.val();
    let courseVideoUrl = $courseVideoUrl.val();
    let courseCover = $courseCover.val();
    let courseTeacher = $courseTeacher.val();
    let courseDuration = $courseDuration.val();
    let courseProfile = $courseProfile.val();
    let courseOutline = window.courseOutline.txt.html();
    let courseCategory = $courseCategory.val();

    console.log(`
      courseTitle: ${courseTitle},
      courseVideoUrl: ${courseVideoUrl},
      courseCover: ${courseCover},
      courseTeacher: ${courseTeacher},
      courseDuration: ${courseDuration},
      courseProfile: ${courseProfile},
      courseOutline: ${courseOutline},
      courseCategory: ${courseCategory},
    
    `);

    selfAjax("/admin/course-pub/", 'post', {
      "title": courseTitle,
      "video_url": courseVideoUrl,
      "cover_url": courseCover,
      "teacher_id": courseTeacher,
      "duration": courseDuration,
      "outline": courseOutline,
      "profile": courseProfile,
      "category_id": courseCategory,
    }, res => {
      if (res["code"] === 2) {
        let courseId = res["data"]["course_id"];
        ALERT.alertNewsSuccessCallback("课程发布成功", "查看课程详情", () => {
          // 查看新闻
          window.location.href = `/course/detail/${courseId}`;
        })
      }
    })
  });
});