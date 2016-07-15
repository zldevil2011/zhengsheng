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
            $(".main-body").css("margin-left", "30px");

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
            $(".main-body").css("margin-left", "150px");

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

//数据查询界面的表格绘制
$(function(){
    try{
        AllUser24Hour();
        AllUserMonth();
        AllUserYearCompare();
        User24Hour();
        UserMonth();
    }catch(e){

    }
});
function AllUser24Hour(){
    $('#AllUser24Hour').highcharts({
        chart: {
            type: 'line',
            backgroundColor: 'rgba(80,81,95,0.1)',
        },
        title: {
            text: '该地区用户24小时用电量统计',
            style: {
                color: '#FFFFFF',
            }
        },
        subtitle: {
            text: '数据来源：电表箱',
            style: {
                color: '#FFFFFF',
            }
        },
        xAxis: {
            categories: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12','13','14','15','16','17','18','19','20','21','22','23','24'],
            style: {
                color: '#FFFFFF',
            },
            labels: {
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif',
                    color:'#FFFFFF',
                }
            }
        },
        yAxis: {
            title: {
                text: '用电量 (Kwh)',
                style: {
                    color: '#FFFFFF',
                }
            },
            labels: {
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif',
                    color:'#FFFFFF',
                }
            }
        },
        tooltip: {
            enabled: false,
            formatter: function() {
                return '<b>'+ this.series.name +'</b><br/>'+this.x +': '+ this.y +'°C';
            }
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true
                },
                enableMouseTracking: false
            }
        },
        series: [{
            name: 'Tokyo',
            data: [7.0, 6.9, 9.5, 14.5, 18.4, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6,7.0, 6.9, 9.5, 14.5, 18.4, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
        }]
    });
}
function AllUserMonth(){
    $('#AllUserMonth').highcharts({
        chart: {
            type: 'column',
            margin: [ 50, 50, 100, 80],
            backgroundColor: 'rgba(80,81,95,0.1)',
        },
        title: {
            text: '该地区一年用电量',
            style: {
                color: '#FFFFFF',
            }
        },
        xAxis: {
            categories: [
                '1月',
                '2月',
                '3月',
                '4月',
                '5月',
                '6月',
                '7月',
                '8月',
                '9月',
                '10月',
                '11月',
                '12月',
            ],
            labels: {
                rotation: -45,
                align: 'right',
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif',
                    color:'#FFFFFF',
                }
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: '用电量(Kwh)',
                style: {
                    color: '#FFFFFF',
                }
            },
            labels: {
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif',
                    color:'#FFFFFF',
                }
            }
        },
        legend: {
            enabled: false
        },
        tooltip: {
            pointFormat: 'Population in 2008: <b>{point.y:.1f} millions</b>',
        },
        series: [{
            name: 'Population',
            data: [34.4, 21.8, 20.1, 20, 19.6, 19.5, 19.1, 18.4, 18,
                17.3, 16.8, 15],
            dataLabels: {
                enabled: true,
                rotation: -90,
                color: '#FFFFFF',
                align: 'right',
                x: 4,
                y: 10,
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif',
                    textShadow: '0 0 3px black'
                }
            }
        }]
    });
}
function AllUserYearCompare(){
    var chart,
        categories = ['1月', '2月', '3月', '4月',
            '5月', '6月', '7月', '8月', '9月',
            '10月', '11月', '12月'];
    $(document).ready(function() {
        $('#AllUserYearCompare').highcharts({
            chart: {
                type: 'bar',
                backgroundColor: 'rgba(80,81,95,0.1)',
            },
            title: {
                text: '近两年月度用电量对比',
                style: {
                    color: '#FFFFFF',
                }
            },
            subtitle: {
                text: '数据来源：电力公司',
                style: {
                    color: '#FFFFFF',
                }
            },
            xAxis: [{
                categories: categories,
                reversed: false
            }, { // mirror axis on right side
                opposite: true,
                reversed: false,
                categories: categories,
                linkedTo: 0,
            }],
            yAxis: {
                title: {
                    text: null
                },
                labels: {
                    formatter: function(){
                        return (Math.abs(this.value) / 1000000) + 'M';
                    },
                    style: {
                        fontSize: '13px',
                        fontFamily: 'Verdana, sans-serif',
                        color:'#FFFFFF',
                    }
                },
                min: -4000000,
                max: 4000000,

            },

            plotOptions: {
                series: {
                    stacking: 'normal'
                }
            },

            tooltip: {
                formatter: function(){
                    return '<b>'+ this.series.name +', age '+ this.point.category +'</b><br/>'+
                        'Population: '+ Highcharts.numberFormat(Math.abs(this.point.y), 0);
                }
            },

            series: [{
                name: '上一年',
                data: [-1746181, -1884428, -2089758, -2222362, -2537431, -2507081, -2443179,
                    -2664537, -3556505, -3680231, -3143062, -2721122]
            }, {
                name: '今年',
                data: [1656154, 1787564, 1981671, 2108575, 2403438, 2366003, 2301402, 2519874,
                    3360596, 3493473, 3050775, 2759560]
            }]
        });
    });
}
function User24Hour(){
    $('#User24Hour').highcharts({
        chart: {
            type: 'line',
            backgroundColor: 'rgba(80,81,95,0.1)',
        },
        title: {
            text: '该用户24小时用电量',
            style: {
                color: '#FFFFFF',
            }
        },
        subtitle: {
            text: '数据来源：电表箱',
            style: {
                color: '#FFFFFF',
            }
        },
        xAxis: {
            categories: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12','13','14','15','16','17','18','19','20','21','22','23','24'],
            labels: {
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif',
                    color:'#FFFFFF',
                }
            }
        },
        yAxis: {
            title: {
                text: '用电量(Kwh)',
                style: {
                    color: '#FFFFFF',
                }
            },
            labels: {
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif',
                    color:'#FFFFFF',
                }
            }
        },
        tooltip: {
            enabled: false,
            formatter: function() {
                return '<b>'+ this.series.name +'</b><br/>'+this.x +': '+ this.y +'°C';
            }
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true
                },
                enableMouseTracking: false
            }
        },
        series: [{
            name: 'Tokyo',
            data: [7.0, 6.9, 9.5, 14.5, 18.4, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6,7.0, 6.9, 9.5, 14.5, 18.4, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
        }]
    });
}
function UserMonth(){
    $('#UserMonth').highcharts({
        chart: {
            type: 'column',
            margin: [ 50, 50, 100, 80],
            backgroundColor: 'rgba(80,81,95,0.1)',
        },
        title: {
            text: '该用户一年用电量',
            style: {
                color: '#FFFFFF',
            }
        },
        xAxis: {
            categories: [
                '1月',
                '2月',
                '3月',
                '4月',
                '5月',
                '6月',
                '7月',
                '8月',
                '9月',
                '10月',
                '11月',
                '12月',
            ],
            labels: {
                rotation: -45,
                align: 'right',
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif',
                    color:'#FFFFFF',
                }
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: '用电量(Kwh)',
                style: {
                    color: '#FFFFFF',
                }
            },
            labels: {
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif',
                    color:'#FFFFFF',
                }
            }
        },
        legend: {
            enabled: false
        },
        tooltip: {
            pointFormat: 'Population in 2008: <b>{point.y:.1f} millions</b>',
        },
        series: [{
            name: 'Population',
            data: [34.4, 21.8, 20.1, 20, 19.6, 19.5, 19.1, 18.4, 18,
                17.3, 16.8, 15],
            dataLabels: {
                enabled: true,
                rotation: -90,
                color: '#FFFFFF',
                align: 'right',
                x: 4,
                y: 10,
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif',
                    textShadow: '0 0 3px black'
                }
            }
        }]
    });
}