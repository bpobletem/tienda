window.addEventListener('load', () => {
    const form = document.getElementById("formulario_editar");
    const mensajeError = document.getElementById("mensajeError");

    form.addEventListener('submit', e => {
        e.preventDefault();
        validarFormulario();
    });

    function validarFormulario() {
        mensajeError.innerHTML = "";

        const nombre = document.getElementById("nombre").value.trim();
        const precio = document.getElementById("precio").value.trim();
        const tallas = document.getElementById("tallas").value.trim();
        const imagen = document.getElementById("imagen").value.trim();
        const errorNombre = document.getElementById("errorNombre");
        const errorPrecio = document.getElementById("errorPrecio");
        const errorTallas = document.getElementById("errorTallas");
        const errorImagen = document.getElementById("errorImagen");

        errorNombre.innerHTML = "";
        errorPrecio.innerHTML = "";
        errorTallas.innerHTML = "";
        errorImagen.innerHTML = "";

        let errores = false;

        if (nombre === "") {
            errorNombre.innerHTML = "Por favor, ingrese un nombre.<br>";
            errores = true;
        }

        if (nombre.length < 2) {
            errorNombre.innerHTML += `El nombre es muy corto. <br>`;
            errores = true;
        }

        if (isNaN(precio) || precio <= 0) {
            errorPrecio.innerHTML = `Ingrese un precio válido. <br>`;
            errores = true;
        }

        if (tallas === "") {
            errorTallas.innerHTML = "Por favor, seleccione al menos una talla.<br>";
            errores = true;
        }

        const allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;
        if (!allowedExtensions.exec(imagen)) {
            errorImagen.innerHTML = `Formato de imagen no válido. Solo se permiten archivos JPG, JPEG o PNG. <br>`;
            errores = true;
        }

        if (errores) {
            mensajeError.innerHTML = "Por favor, corrija los errores en el formulario.<br>";
            return false;
        }

        form.submit(); // Envío del formulario si pasa todas las validaciones.
    }
});
