window.addEventListener('load', () => {

    const form = document.getElementById("formulario");
    const mensajeError = document.getElementById("mensajeError");

    form.addEventListener('submit', e => {
        e.preventDefault();
        validarFormulario();
    });

    function validarFormulario() {
        
        // Declaramos variables para comenzar las validaciones
        const mailFormat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        const telefonoFormat = /^9\d{8}$/;
        const rutFormat = /^\d{7,8}-[\dkK]$/;
        
        const nombre = document.getElementById("id_nombre").value.trim();
        const apellidos = document.getElementById("id_apellido").value.trim();
        const telefono = document.getElementById("id_telefono").value.trim();
        const correo = document.getElementById("id_correo").value.trim();
        
        
        // Reseteamos los errores
        mensajeError.innerHTML = "";

        //Validacion campos completos
        if (nombre === "" || apellidos === "" || telefono === "" || correo === "") {
            mensajeError.innerHTML += "Por favor, complete todos los campos.<br>";
        }

        //Validacion nombre
        if (nombre.length < 2 || nombre.length > 50) {
            mensajeError.innerHTML += `El nombre es muy corto.<br>`;
            return false;
        }

        //Validacion apellido
        if (apellidos.length < 2 || apellidos.length > 50) {
            mensajeError.innerHTML += `El apellido es muy corto.<br>`;
            return false;
        }

        //Validacion correo
        if (!mailFormat.test(correo)) {
            mensajeError.innerHTML += `El correo no es valido.<br>`;
            return false;
        }

        //Validacion telefono solo 9 numeros
        if (!telefonoFormat.test(telefono)) {
            mensajeError.innerHTML += `El telefono no es valido.<br>`;
            return false;
        }

        //Submit del formulario en caso de pasar las validaciones
        form.submit();
    
    }
    
})