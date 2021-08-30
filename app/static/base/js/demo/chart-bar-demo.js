var meses = []
var ventas = []

const loadVentas = () => {

    meses = []
    ventas = []

    let year = document.getElementById('select-years-ventas').value;
    let month = document.getElementById('select-months-ventas').value;
    let display = document.getElementById('display-data-ventas').value;

    $.ajax({
        url: `/api/v1/facturas/ventas/mensuales?year=${year}&month=${month}`,
        async: false,
        dataType: 'JSON',

        success: function(datos) {

            for (let d in datos) {

                if (display == 'valor') {
                    ventas.push(datos[d].valor);
                } else if (display == 'cantidad') {
                    ventas.push(datos[d].cantidad);
                }

                meses.push(d);
            }
        }
    });
}

loadVentas();

function number_format(number, decimals, dec_point, thousands_sep) {
    // *     example: number_format(1234.56, 2, ',', ' ');
    // *     return: '1 234,56'
    number = (number + '').replace(',', '').replace(' ', '');
    var n = !isFinite(+number) ? 0 : +number,
        prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
        sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
        dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
        s = '',
        toFixedFix = function(n, prec) {
            var k = Math.pow(10, prec);
            return '' + Math.round(n * k) / k;
        };
    // Fix for IE parseFloat(0.55).toFixed(0) = 0;
    s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
    if (s[0].length > 3) {
        s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
    }
    if ((s[1] || '').length < prec) {
        s[1] = s[1] || '';
        s[1] += new Array(prec - s[1].length + 1).join('0');
    }
    return s.join(dec);
}

// Bar Chart Example
var ctx = document.getElementById("myBarChart");
var myBarChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: [...meses],
        datasets: [{
            label: "Ventas",
            backgroundColor: "#6f42c1",
            hoverBackgroundColor: "#6610f2",
            borderColor: "#4e73df",
            data: [...ventas],
        }],
    },
    options: {
        maintainAspectRatio: false,
        layout: {
            padding: {
                left: 10,
                right: 25,
                top: 25,
                bottom: 0
            }
        },
        scales: {
            xAxes: [{
                time: {
                    unit: 'month'
                },
                gridLines: {
                    display: false,
                    drawBorder: false
                },
                ticks: {
                    maxTicksLimit: 15
                },
                maxBarThickness: 25,
            }],
            yAxes: [{
                ticks: {
                    min: 0,
                    max: Math.max(...ventas),
                    maxTicksLimit: 10,
                    padding: 10,
                    // Include a dollar sign in the ticks
                    callback: function(value, index, values) {
                        return '$' + number_format(value);
                    }
                },
                gridLines: {
                    color: "rgb(234, 236, 244)",
                    zeroLineColor: "rgb(234, 236, 244)",
                    drawBorder: false,
                    borderDash: [2],
                    zeroLineBorderDash: [2]
                }
            }],
        },
        legend: {
            display: false,
        },
        tooltips: {
            titleMarginBottom: 10,
            titleFontColor: '#6e707e',
            titleFontSize: 14,
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            caretPadding: 10,
            callbacks: {
                label: function(tooltipItem, chart) {
                    var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
                    return datasetLabel + ': $' + number_format(tooltipItem.yLabel);
                }
            }
        },
    }
});

const reloadDataVentas = () => {

    const display = document.getElementById('display-data-ventas').value;

    loadVentas();
    removeDataVentas(myBarChart);
    addDataVentas(myBarChart, meses, ventas, display);
}

function addDataVentas(chart, label, data, display) {

    chart.data.labels = label;

    chart.data.datasets.forEach((dataset) => {
        dataset.data = data;
    });

    chart.options.scales.yAxes.forEach((yAxes) => {
        yAxes.ticks.max = Math.max(...data);
        yAxes.ticks.callback = function(value, index, values) {
            return `${(display == 'valor' ? '$' : '#')}` + number_format(value);
        }
    });

    chart.options.tooltips.callbacks.label = function(tooltipItem, chart) {
        var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
        return datasetLabel + `${(display == 'valor' ? ': $' : ': #')}` + number_format(tooltipItem.yLabel);
    }

    chart.update();
}

function removeDataVentas(chart) {

    chart.data.labels = [];

    chart.data.datasets.forEach((dataset) => {
        dataset.data = [];
    });

    chart.options.scales.yAxes.forEach((yAxes) => {
        yAxes.ticks.max = 0;
    });

    chart.update();
}