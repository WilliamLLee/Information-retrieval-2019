
var flag = true;
$(".login-btn").on("click", function () {

    if (flag) {
        var str = '<div class="login">\
                        <div class="login-form">\
                            <i class=" close">\
                                <span class="iconfont icon-close"></span>\
                            </i>\
                            <div class="title-div">\
                                <img src="images/loginlogo.png" />\
                                <span class="title-form">用户名密码登录</span>\
                            </div>\
                            <input type="text" placeholder="手机/邮箱/用户名" class="user-name">\
                            <input type="password" placeholder="密码">\
                            <div class="remember">\
                                <input type="checkbox" id="remem">\
                                <label for="remem">下次自动登录</label>\
                            </div>\
                            <input type="submit" value="登录">\
                        </div>\
                    </div>'
        $(document.body).append(str);
        flag = false;
        $(".login").toggle()
    }

    $(".login").toggle()
    $(".icon-close").one("click", function () {
        console.log("点击了")
        $(".login").hide()
    })
})


var oUl = $(".search-ul");
var input = $("input[type='text']");
var value = null;

input.on("input", function () {
    value = this.value;
    console.log(value);
    var oScript = "<script src='https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su?wd=" + value + "&cb=doJson'>"
    $(document.body).append(oScript);
    $("script[src^='http']").remove()

});

input.on("focus", function (e) {
    // value ：null初始化状态 ""是清空字符状态
    if (value !== null && value !== "") {
        oUl.show(); // 该处显示动态生成的列表
    }
})

$(document).on("click", function (e) {
    
    if(e.target.type !== "text"){
    // 搜索框失去焦点 列表隐藏
    oUl.hide(); // 隐藏动态列表
    
    // oUl是列表 
    // 列表含有超链接，点击列表页面跳转，
    // 但在点击列表的瞬间，input失去焦点，列表隐藏
    // 解决思路：绑定body点击事件 body被点击则隐藏列表
    }

})



function doJson(res) {

    // 数据渲染
    var s = res.s,
        str = "";
    if (s.length > 0) {
        console.log(111)
        s.forEach(function (ele, index) {
            str += "<a href=https://www.baidu.com/s?&wd=" + ele + "><li>" + ele + "</li></a>";
        })
        oUl.html(str);
        oUl.show();
    } else {
        oUl.hide();
    }
}

$(".search").on('click', function () {

    // 思路：把输入的关键词绑定到超链接地址，利用超链接实现页面跳转
    var bHref = value;
    var temp;
    // 请求数据
     $.ajax({
        data:{"query":value},
        url: "http://127.0.0.1:5000/index",
        type: "POST",
        async: false,
        dataType: "JSON",
        success: function (rep) {
            temp = rep;
            console.log(rep);
        },error:function(error){
            console.log('error');
            console.log(error);
        }
        })

    $(this).attr("href",temp["url"]);
})
