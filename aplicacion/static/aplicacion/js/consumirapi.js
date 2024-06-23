$(document).ready(function () {

    $.getJSON('https://mindicador.cl/api', function () {


    }).fail(function () {
        console.log('Error al consumir la API');
        $("#dolar").text('Error al consumir la API');
        $("#dolar-actual").text('Error al consumir la API');
    }).done(function(data)
    {
       
        $("#dolar").text("USD$" + Math.round(150000/data.dolar.valor));
        $("#dolar-actual").text("USD$" + data.dolar.valor);

    });

});