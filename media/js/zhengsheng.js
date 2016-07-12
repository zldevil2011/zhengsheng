function sleep(n) { //n表示的毫秒数
    var start = new Date().getTime();
    while (true) if (new Date().getTime() - start > n) break;
}

        $(function(){
            console.log("xxx");
            $("[name=slide-btn]").on("click", function(){
                console.log("xx");
                console.log($(".side-menu").css("left"));
                if($(".side-menu").css("left") == "0px"){
                    console.log("0");
                    $(".side-menu").css("left", "-250px");
                }else{
                    console.log("255");
                    $(".side-menu").css("left", "0");
                }
            });
        });
