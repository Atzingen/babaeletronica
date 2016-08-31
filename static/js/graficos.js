$(function () {
    $.getJSON('https://www.highcharts.com/samples/data/jsonp.php?filename=aapl-c.json&callback=?', function (data) {

        // Create the chart
        $('#container2').highcharts('StockChart', {
            chart: {
                type: 'area'
            },

            rangeSelector: {
                selected: 1
            },

            title: {
                text: 'Temperatura - Lafac, sala do forno (dados em tempo real)'
            },

            yAxis: {
                reversed: false,
                showFirstLabel: false,
                showLastLabel: true
            },

            series: [{
                name: 'Temperatura (oCelcius)',
                data: [
						{% for dado in dados %}
		                	[ Date.UTC({{dado[0].year|safe}},{{dado[0].month|safe}},{{dado[0].day|safe}},{{dado[0].hour|safe}},{{dado[0].minute|safe}} ), {{dado[1]|safe}} ],
		                {% endfor %}
            	],
                threshold: null,
                fillColor : {
                    linearGradient : {
                        x1: 0,
                        y1: 1,
                        x2: 0,
                        y2: 0
                    },
                    stops : [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                },
                tooltip: {
                    valueDecimals: 2
                }
            }]
        });
    });
});
