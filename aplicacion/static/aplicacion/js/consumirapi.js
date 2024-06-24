$(document).ready(function () {

    // Manejo de la petición a la API de Mindicador
    $.getJSON('https://mindicador.cl/api', function (data) {
        // Éxito en la obtención de datos
        console.log(data);

        // Acceder al precio del producto desde el DOM
        const precio = parseFloat($("#precio-producto"));
        

        // Cálculo del precio en dólares
        if (!isNaN(precio) && data.dolar) {
            const precioEnDolares = precio / data.dolar.valor;
            $("#dolar").text("USD $" + precioEnDolares.toFixed(2));
        } else {
            $("#dolar").text('Error al calcular el precio en dólares');
        }

    }).fail(function () {
        // Error al consumir la API
        console.log('Error al consumir la API');
        $("#dolar").text('Error al consumir la API');
        $("#dolar-actual").text('Error al consumir la API');
    });

});