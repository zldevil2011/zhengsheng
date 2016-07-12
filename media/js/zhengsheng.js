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
            $(".side-menu").css("left", "-120px");
            $(".my-nav").css("left", "30px");
            $(".panel-item li").children(":first").addClass("fr");
            var mainClassification = $(".panel-item");
            mainClassification.each(function(){
                var second = $(this).children();
                second.each(function(){
                   $(this).children(":first").addClass("fr");
                });
            });
        }else{
            console.log("255");
            $(".side-menu").css("left", "0");
            $(".my-nav").css("left", "150px");
            var mainClassification = $(".panel-item");
            mainClassification.each(function(){
                var second = $(this).children();
                second.each(function(){
                   $(this).children(":first").removeClass("fr");
                });
            });
        }
    });
});
