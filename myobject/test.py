$(function () {
    //动态无刷新预览头像
    $("#File1").change(function () {
        alert("s");
        $("#form1").ajaxSubmit({
            success: function (str) {
                if (str != null && str != "undefined") {

                    $("#pre_img").attr('src', str);


                    if (str == "2") { alert("只能上传jpg,png格式的图片"); }
                    else if (str == "3") { alert("图片不能大于3M"); }
                    else if (str == "4") { alert("请选择要上传的文件"); }

                }
                else alert('操作失败！');
            },
            error: function (error) { alert(error); },
            url: "/Service/uploadpic.ashx?fn=uploadTX&&fsid=" + $("#SaveSelectfsid").val(), /*设置post提交到的页面*/
            type: "post", /*设置表单以post方法提交*/
            dataType: "HTML"
        });

    });
})