;
var member_set_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".wrap_member_set .save").click(function () {
            var btn_taget = $(this);
            if (btn_taget.hasClass("disabled")) {
                common_ops.alert("正在处理，请不要重复提交");
                return;
            }
            var nickname_target = $(".wrap_member_set input[name=nickname]");
            var nickname = nickname_target.val();
            if (nickname.length < 4) {
                common_ops.tio("请输入符合规范的姓名", nickname_target);
                return;
            }
            btn_taget.addClass("disabled");
            var data = {
                nickname: nickname,
                id:$(".wrap_member_set input[name=id]").val()
            }

            $.ajax({
                uri:common_ops.buildUrl("/member/set"),
                type:'POST',
                data:data,
                dataType:'json',
                success:function (res) {
                    var callback=null;
                    if(res.code==200){
                        callback=function () {
                            window.location.href=window.location.href;
                        };
                    }
                    common_ops.alert(res.msg,callback);
                }
            })
        });
    }
};

$(function () {
    member_set_ops.init();
});