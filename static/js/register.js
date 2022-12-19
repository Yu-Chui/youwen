function bindCaptchaBtnClick(){
    $("#captcha-btn").on("click", function(event){
        var $this = $(this);
        var email = $("input[name='email']").val();
        if (!email){
            alert("请输入邮箱！");
            return;
        }
        // 通过js发送网络请求: ajax, Async JavaScript And XML(Json)
        $.ajax({
            url:"/user/captcha",
            method: "POST",
            data:{
                "email": email
            },
            success: function (res){
                var code = res["code"]
                if(code == 200){
                    // 取消点击事件
                    $this.off("click")
                    // 开始倒计时
                    var countdown = 60;
                    var timer = setInterval(function (){
                        countdown -= 1;
                        if(countdown>0){
                            $this.text(countdown+"秒后重新发送");
                        }else{
                            $this.text("获取验证码");
                            // 重新执行这个函数,重新绑定点击事件
                            bindCaptchaBtnClick();
                            // 如果不需要倒计时就停下,否则就一直执行
                            clearInterval(timer);
                        }
                    },1000);
                    alert("验证码发送成功!");
                }else{
                    alert(res["message"]);
                }
            }


        })
    })
}

// 等网页文档所有元素加载完成后再执行
$(function (){
    bindCaptchaBtnClick();
});