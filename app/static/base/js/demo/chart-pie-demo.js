var meses_pie = []
var productos_pie = []

const loadProductosPie = () => {

    meses_pie = [];
    productos_pie = [];
    let products = '';
    let year = document.getElementById('select-years-productos-pie').value;
    let comparison = document.getElementById('products-compare');

    for (let option of comparison.options) {
        if (option.selected) {
            if (products.length > 0) {
                products = `${products},${option.value}`;
            } else {
                products = `${option.value}`;
            }
        }
    }

    console.log(products);

    $.ajax({
        url: `/api/v1/productos/vendidos/anual?year=${year}&products=${products}`,
        async: false,
        dataType: 'JSON',

        success: function(datos) {

            for (let d in datos) {
                productos_pie.push(datos[d]);
                meses_pie.push(d);
            }
        }
    });
}

loadProductosPie();

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: [...meses_pie],
        datasets: [{
            data: [...productos_pie],
            backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#FF7373', '#FFFB6C', '#A673FF', '#EEE', '#FF8DF5', '#6A6A6A', '#FFCF7A'],
            hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf', '#FF4A4A', '#FFF934', '#7E34FF', '##BFBFBF', '#FD3FEC', '#373737', '#FFB431'],
            hoverBorderColor: "rgba(234, 236, 244, 1)",
        }],
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            caretPadding: 10,
        },
        legend: {
            display: true,
            position: 'bottom',
        },
        title: {
            display: true,
            text: 'Productos más vendidos'
        },
        cutoutPercentage: 5,
    },
});

const reloadDataProductosPie = () => {

    loadProductosPie();
    removeData(myPieChart);
    addData(myPieChart, meses_pie, productos_pie);
}