window.addEventListener('load', () => {

    const form = document.getElementById("formulario");
    const mensajeError = document.getElementById("mensajeError");

    form.addEventListener('submit', e => {
        e.preventDefault(); // Aquí está la corrección
        validarFormulario();
    });

    function validarFormulario() {
        // Reseteamos los errores
        mensajeError.innerHTML = "";

        //Variables
        const mailFormat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        const passFormat = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,}$/; //1 numero, 1 mayuscula, 1 minuscula min 6 caracteres
        
        //Seleccionamos los elementos
        const correo = document.getElementById("correo").value.trim();
        const password = document.getElementById("password").value.trim();
        const errorCorreo = document.getElementById("errorCorreo");
        const errorPassword = document.getElementById("errorPassword");

        //Validacion campos completos
        if (correo === "" || password === "") {
            mensajeError.innerHTML = "Por favor, complete todos los campos.<br>";
            return false;
        }

        if (!passFormat.test(password)) {
            errorPassword.innerHTML = "Por favor, ingrese una clave valida"
            return false;
        }

        //Validacion correo
        if (!mailFormat.test(correo)) {
            errorCorreo.innerHTML = `El correo no es valido.`;
            return false;
        }

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