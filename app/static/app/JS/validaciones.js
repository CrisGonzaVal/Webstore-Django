
// VALIDACIONES REGISTRO}
function validacion() {
    //IMPUT
    
    var nombre = document.getElementById('nombre');
    var apellido = document.getElementById('apellido');
    var rut = document.getElementById('rut');
    var edad = document.getElementById('edad');
    var correo = document.getElementById('direccion');
    var correo = document.getElementById('email');
    var pass = document.getElementById('password');
    var confirmPass = document.getElementById('confirmPassword');
    var celular = document.getElementById('celular');

    //MENSAJES ERROR
    
    var nombreError = document.getElementById('nombreError');
    var nombreError = document.getElementById('apellidoError');
    var rutError = document.getElementById('rutError');
    var rutLongError = document.getElementById('longError');
    var edadError = document.getElementById('edadError');
    var edadError = document.getElementById('direccionError');
    var emailError = document.getElementById('emailError');
    var passError = document.getElementById('passError');
    var passError2 = document.getElementById('passError2');
    var celularError = document.getElementById('celularError');
    var button = document.getElementById('button');

      var valiLongRut = validarLongitudRut();
      var rutValido = validarRut();
      var correoValido = validarCorreo();
      var passValida = compararPass();
      validaCampos();

      if (!rutValido || !correoValido || !passValida || !valiLongRut) {
        button.disabled = true;
        return false;
      } else {
        button.disabled = false;
        return true;
      }
    

      if (nombre.value === null || nombre.value === ''){
        mensajeError.push('Ingresa tu nombre');
      }

      if (apellido.value === null || apellido.value === ''){
        mensajeError.push('Ingresa tu apellido');
      }

    // VALIDACIONES DE CAMPOS
    function validarLongitudRut() {
      if (rut.value.length > 10) {
        rutLongError.style.display = 'block';
        rutLongError.textContent = "El texto no debe superar los 10 caracteres.";
        return false;
      } else {
        rutLongError.style.display = 'none';
        return true;
      }
    }

    function validarRut() {
      const rutRegex = /^[0-9]+[-|‐]{1}[0-9kK]{1}$/;
      if (!rutRegex.test(rut.value)) {
        rutError.style.display = 'block';
        rutError.className = "text-danger";
        rutError.textContent = "El RUT NO es valido.";
        return false;
      } else {
        rutError.style.display = 'block';
        rutError.className = "text-success";
        rutError.textContent = "RUT validado";
        return true;
      }
    }

    function validarCorreo() {
      const regexCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (regexCorreo.test(correo.value)) {
        emailError.style.display = 'block';
        emailError.className = "text-success";
        emailError.textContent = "Correo electrónico válido.";
        return true;
      } else {
        emailError.style.display = 'block';
        emailError.className = "text-danger";
        emailError.textContent = "Por favor, ingrese un correo electrónico válido.";
        return false;
      }
    }

    function compararPass() {
      if (pass.value !== confirmPass.value || pass.value === "") {
        passError2.style.display = 'block';
        passError2.className = "text-danger";
        passError2.textContent = "Las contraseñas no coinciden.";
        return false;
      } else {
        passError2.style.display = 'block';
        passError2.className = "text-success";
        passError2.textContent = "Contraseña confirmada.";
        return true;
      }
    }
    
    function vacio(campo)  {
      if(campo == ""){
        return true}
      else{
        return false}  
  }

    
 


  function validaCampos()
  {

    if(vacio(edad)){
        edadError.style.display = 'block';
        edadError.style.color = "red";
        edadError.textContent = "Ingrese edad";
        return false;
    }else{
        return true}
    }  
    
 }



//VALIDACION LOGIN
function validacionLogin()
{
 var validarCorreo = validacion().validarCorreo();
 var validaPass = pass.value;

 if(!validarCorreo && validaPass==""){
  button.disabled = true;
 }
 else{
  button.disabled = false;
  }

}


function validacionGeneral()
{  
   if(validaRut() == true && validarCorreo() == true && compararPass() == true ){
      document.getElementById("button").disabled = false;
      
     }
     else
     {
        document.getElementById("button").disabled = true;
       
     }
}

