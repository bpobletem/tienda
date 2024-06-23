// rutValidator.js
const Fn = {
    // Valida el rut con su cadena completa "XXXXXXXX-X"
    validaRut: function (rutCompleto) {
        if (!/^[0-9]+[-|‐]{1}[0-9kK]{1}$/.test(rutCompleto))
            return false;
        var tmp = rutCompleto.split('-');
        var digv = tmp[1];
        var rut = tmp[0];
        if (digv == 'K') digv = 'k';
        return (Fn.dv(rut) == digv);
    },
    dv: function (T) {
        var M = 0, S = 1;
        for (; T; T = Math.floor(T / 10))
            S = (S + T % 10 * (9 - M++ % 6)) % 11;
        return S ? S - 1 : 'k';
    }
};

window.addEventListener('load', () => {
    console.log('validacion')

    const form = document.getElementById("formulario");
    const mensajeError = document.getElementById("mensajeError");

    form.addEventListener('submit', e => {
        e.preventDefault();
        validarFormulario();

        form.classList.add('was-validated');

        if (!validarFormulario()) {
            form.classList.remove('was-validated');
        }
    });

    function validarFormulario() {
        // Declaramos las regex para validar
        const mailFormat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        const passFormat = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,}$/; //1 numero, 1 mayuscula, 1 minuscula min 6 caracteres
        const telefonoFormat = /^9\d{8}$/;

        const rut = document.getElementById("id_rut").value.trim();
        const nombre = document.getElementById("id_nombre").value.trim();
        const apellidos = document.getElementById("id_apellido").value.trim();
        const correo = document.getElementById("id_correo").value.trim();
        const fecha_nacimiento = document.getElementById("id_fnac").value.trim();
        const password = document.getElementById("id_password1").value.trim();
        const confirm_password = document.getElementById("id_password2").value.trim();
        const telefono = document.getElementById("id_telefono").value.trim();

        const direccion = document.getElementById("id_calle").value.trim();
        const depto = document.getElementById("id_detalle").value.trim();
        const region = document.getElementById("id_region").value.trim();
        const comuna = document.getElementById("id_comuna").value.trim();

        // Reseteamos los errores
        mensajeError.innerHTML = "";

        //Validacion campos completos
        if (nombre === "" || apellidos === "" || rut === "" || direccion === "" || telefono === "" || correo === "" || password === "" || confirm_password === "" || fecha_nacimiento === "") {
            mensajeError.innerHTML += "Por favor, complete todos los campos. <br>";
            return false;
        }

        //Validacion nombre
        if (nombre.length < 2 || nombre.length > 50) {
            mensajeError.innerHTML += `El nombre es muy corto.`;
            nombre.classList.add()
            return false;
        }

        //Validacion apellido
        if (apellidos.length < 2 || apellidos.length > 50) {
            mensajeError.innerHTML += `El apellido es muy corto.`;
            return false;
        }

        if (!Fn.validaRut(rut)) {
            mensajeError.innerHTML += `El RUT no es válido. Sin puntos y con guion.`;
            return false;
        }

        //Validacion fecha de nacimiento
        const fechaHoy = new Date();
        const fechaNacimiento = new Date(fecha_nacimiento);

        //Verificamos que exista la fecha
        if (!fecha_nacimiento) {
            mensajeError.innerHTML += `Por favor, seleccione su fecha de nacimiento.`;
            return false;
        }
        //Verificamos que no sea posterior a la fecha de hoy
        if (fechaNacimiento > fechaHoy) {
            mensajeError.innerHTML += `La fecha de nacimiento no puede ser posterior al día de hoy.`;
            return false;
        }

        //Validacion correo
        if (!mailFormat.test(correo)) {
            mensajeError.innerHTML += `El correo no es valido.`;
            return false;
        }

        //Validacion telefono solo 9 numeros
        if (!telefonoFormat.test(telefono)) {
            mensajeError.innerHTML += `El telefono no es valido. Formato: 912345678`;
            return false;
        }

        //Validacion password segura
        if (password.length < 6 || password.length > 50) {
            mensajeError.innerHTML += `La contraseña debe tener al menos 6 caracteres y maximo 50`;
            return false;
        }

        if (!passFormat.test(password)) {
            mensajeError.innerHTML += `La contraseña debe tener al menos un numero, una mayuscula y una minuscula`;
            return false;
        }

        //Validacion passwords coincidan
        if (password !== confirm_password) {
            mensajeError.innerHTML += `Las contraseñas no coinciden.`;
            return false;
        }


        if (direccion.length < 4 || direccion.length > 50) {
            mensajeError.innerHTML += `Ingrese una direccion valida.`
            return false;
        }

        if (region === "") {
            mensajeError.innerHTML += "Por favor, seleccione una region";
        }

        if (comuna === "") {
            mensajeError.innerHTML += "Por favor, seleccione una region";
        }

        //Submit del formulario en caso de pasar las validaciones
        form.submit();
    }
})


    function showPass() {
        var x = document.getElementById("password");
        if (x.type === "password") {
            x.type = "text";
        } else {
            x.type = "password";
        }
    }

    function showConfirmPass() {
        var x = document.getElementById("confirm_password");
        if (x.type === "password") {
            x.type = "text";
        } else {
            x.type = "password";
        }
    }