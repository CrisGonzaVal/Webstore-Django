//IMPUT
    
var nombre = document.getElementById('nombre');
var apellido = document.getElementById('apellido');
var rut = document.getElementById('rut');
var edad = document.getElementById('edad');
var correo = document.getElementById('direccion');
var comuna = document.getElementById('comuna');
var region = document.getElementById('region');
var correo = document.getElementById('email');
var pass = document.getElementById('password');
var confirmPass = document.getElementById('confirmPassword');
var celular = document.getElementById('celular');

//MENSAJES ERROR

var nombreError = document.getElementById('nombreError');
var apellidoError = document.getElementById('apellidoError');
var rutError = document.getElementById('rutError');
var rutLongError = document.getElementById('longError');
var edadError = document.getElementById('edadError');
var edadError = document.getElementById('direccionError');
var comunaError = document.getElementById('comunaError');
var regionError = document.getElementById('regionError');
var emailError = document.getElementById('emailError');
var passError = document.getElementById('passError');
var passError2 = document.getElementById('passError2');
var celularError = document.getElementById('celularError');
var button = document.getElementById('button');



//FUNCION REGISTRO
function validacion() {
   
  var valiApellido = validarApellido();
  var valiNombre = validarNombre();
  var valiLongRut = validarLongitudRut();
  var rutValido = validarRut();
  var valiEdad = validarEdad();
  var valiDireccion = validarDireccion();
  var valiRegion = validarRegion();
  var valiComuna = validarComuna();
  var valiCelular = validarCelular();
  var correoValido = validarCorreo();
  var valiContraseña = validarContraseña();
  var passValida = compararPass();
  validaCampos();

  if (!rutValido || !correoValido || !passValida || !valiLongRut || !valiNombre || !valiApellido || !valiEdad
    || !valiDireccion || !valiRegion || !valiComuna || !valiCelular || !valiContraseña) {
    button.disabled = true;
    return false;
  } else {
    button.disabled = false;
    return true;
  }
    

  function validarNombre(){
    if (nombre.value === null || nombre.value === ''){
      nombreError.style.display = 'block';
      nombreError.className = "text-danger";
      nombreError.textContent = "Ingresa tu nombre.";
      return false;
    } else {
      nombreError.style.display = 'none';
      nombreError.className = "text-success";
      return true;
    } 
  }
    
  function validarApellido(){
    if (apellido.value === null || apellido.value === ''){
      apellidoError.style.display = 'block';
      apellidoError.className = "text-danger";
      apellidoError.textContent = "Ingresa tus apellidos.";
      return false;
    } else {
      apellidoError.style.display = 'none';
      apellidoError.className = "text-success";
      return true;
    } 

  }

  function validarEdad(){
    if (edad.value === null || edad.value === ''){
      edadError.style.display = 'block';
      edadError.className = "text-danger";
      edadError.textContent = "Selecciona tu edad.";
      return false;
    } else {
      edadError.style.display = 'none';
      edadError.className = "text-success";
      return true;
    } 

  }

  
  function validarDireccion(){
    if (direccion.value === null || direccion.value === ''){
      direccionError.style.display = 'block';
      direccionError.className = "text-danger";
      direccionError.textContent = "Ingresa tu direccion.";
      return false;
    } else {
      direccionError.style.display = 'none';
      direccionError.className = "text-success";
      return true;
    } 

  }

  function validarRegion(){
    if (region.value === null || region.value === ''){
      regionError.style.display = 'block';
      regionError.className = "text-danger";
      regionError.textContent = "Seleccionar tu región.";
      return false;
    } else {
      regionError.style.display = 'none';
      regionError.className = "text-success";
      return true;
    } 

  }

  function validarComuna(){
    if (comuna.value === null || comuna.value === ''){
      comunaError.style.display = 'block';
      comunaError.className = "text-danger";
      comunaError.textContent = "Selecciona tu comuna.";
      return false;
    } else {
      comunaError.style.display = 'none';
      comunaError.className = "text-success";
      return true;
    } 

  }

  function validarCelular(){
    if (celular.value === null || celular.value === ''){
      celularError.style.display = 'block';
      celularError.className = "text-danger";
      celularError.textContent = "Ingresar tu celular.";
      return false;
    } else {
      celularError.style.display = 'none';
      celularError.className = "text-success";
      return true;
    } 

  }


  function validarContraseña(){
    if (pass.value === null || pass.value === ''){
      passError.style.display = 'block';
      passError.className = "text-danger";
      passError.textContent = "Ingresar una contraseña válida.";
      return false;
    } else {
      passError.style.display = 'none';
      passError.className = "text-success";
      return true;
    } 

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
      rutError.textContent = "El Rut no es valido.";
      return false;
    } else {
      rutError.style.display = 'block';
      rutError.className = "text-success";
      rutError.textContent = "Rut validado";
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



//FUNCION LOGIN
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


