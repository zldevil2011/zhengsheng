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
//index highcharts
$(function () {
    $(document).ready(function() {
        Highcharts.setOptions({
            global: {
                useUTC: false
            },
            colors: ['#FFFFFF', '#50B432', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
        });
        $('#container').highcharts({
            chart: {
                type: 'line',
                animation: Highcharts.svg, // don't animate in old IE
                marginRight: 10,
                backgroundColor: '#45b6b0',
                events: {
                    load: function() {
                        // set up the updating of the chart each second
                        var series = this.series[0];
                        setInterval(function() {
                            var x = (new Date()).getTime(), // current time
                                y = Math.random() * (20-19) + 19;
                            series.addPoint([x, y], true, true);
                        }, 500);
                    }
                }
            },
            title: {
                text: 'Live random data'
            },
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150
            },
            yAxis: {
                max:25,
                min:15,
                title: {
                    text: 'Value'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function() {
                        return '<b>'+ this.series.name +'</b><br/>'+
                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) +'<br/>'+
                        Highcharts.numberFormat(this.y, 2);
                }
            },
            legend: {
                enabled: false

            },
            exporting: {
                enabled: false
            },
            series: [{
                name: 'Random data',
                data: (function() {
                    // generate an array of random data
                    var data = [],
                        time = (new Date()).getTime(),
                        i;

                    for (i = -19; i <= 0; i++) {
                        data.push({
                            x: time + i * 1000,
                            y: Math.random()
                        });
                    }
                    return data;
                })()
            }]
        });
    });

});
