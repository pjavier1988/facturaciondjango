var meses_p = []
var productos = []

const loadProductos = () => {

    meses_p = []
    productos = []

    let year = document.getElementById('select-years-productos').value;
    let month = document.getElementById('select-months-productos').value;
    let display = document.getElementById('display-data-productos').value;
    
    $.ajax({
        url: `/api/v1/productos/mas/vendidos?year=${year}&month=${month}`,
        async: false,
        dataType: 'JSON',

        success: function(datos) {

            for (let d in datos) {

                if (display == 'valor') {
                    productos.push(datos[d].valor);
                } else if (display == 'cantidad') {
                    productos.push(datos[d].cantidad);
                }

                meses_p.push(d);
            }
        }
    });
}

loadProductos();

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
var ctx = document.getElementById("myBarChartProductos");
var myBarChartProductos = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: [...meses_p],
        datasets: [{
            label: "Ventas",
            backgroundColor: "#1cc88a",
            hoverBackgroundColor: "#36b9cc",
            borderColor: "#4e73df",
            data: [...productos],
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
                    max: Math.max(...productos),
                    maxTicksLimit: 10,
                    padding: 10,
                    // Include a dollar sign in the ticks
                    callback: function(value, index, values) {
                        return '#' + number_format(value);
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
            display: false
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
                    return datasetLabel + ': #' + number_format(tooltipItem.yLabel);
                }
            }
        },
    }
});

const reloadDataProductos = () => {

    handleProductosInfo();

    const display = document.getElementById('display-data-productos').value;

    loadProductos();
    removeDataVentas(myBarChartProductos);
    addDataVentas(myBarChartProductos, meses_p, productos, display);
}

//Others Methods

const handleProductosInfo = () => {

    const today = new Date();
    const infoYear = document.getElementById('year-productos-info');
    const infoMonth = document.getElementById('month-productos-info');
    const infoDisplay = document.getElementById('display-productos-info');
    const year = document.getElementById('select-years-productos').value;
    const month = document.getElementById('select-months-productos').value;
    const display = document.getElementById('display-data-productos').value;

    if (year) infoYear.innerHTML = year;
    else infoYear.innerHTML = today.getFullYear();

    if (month) {
        let txtInfo = `del mes de <span class="font-weight-bold">${getKeyByValue(mesesList, parseInt(month))}</span>`;
        infoMonth.innerHTML = txtInfo;
    } else {
        infoMonth.innerHTML = '';
    }

    if (display == 'valor') {
        let span = '<span class="font-weight-bold">valor</span>';
        let txtInfo = `el ${span} total de los productos vendidos`;
        infoDisplay.innerHTML = txtInfo;
    } else if (display == 'cantidad') {
        let span = '<span class="font-weight-bold">cantidad</span>';
        let txtInfo = `la ${span} total de los productos vendidos.`;
        infoDisplay.innerHTML = txtInfo;
    }
}

//Run
handleProductosInfo();