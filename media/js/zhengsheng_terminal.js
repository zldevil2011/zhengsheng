$(function(){
    var cur_title = $(document).attr("title");
    $(".terminal-tab a").each(function(){
        var title = $(this).html();
        console.log($(this).html());
        if(title == cur_title){
            $(this).parent().siblings().removeClass("active");
            $(this).parent().addClass("active");
        }
    });
});