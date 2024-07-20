document.addEventListener('DOMContentLoaded', function () {
    var buttons = document.querySelectorAll('a[id^="addToCart"]');
    buttons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            // Evitar la acción de navegación predeterminada del enlace
            event.preventDefault();

            // Obtener el ID del producto desde el botón
            var productId = this.id.replace('addToCart', '');

            // Obtener el elemento de mensaje correspondiente
            var popupMessage = document.getElementById('popupMessage' + productId);

            // Mostrar la ventana emergente
            popupMessage.classList.remove('hidden');
            popupMessage.style.opacity = '1';

            // Ocultar la ventana emergente después de 2 segundos
            setTimeout(function() {
                popupMessage.style.opacity = '0';
                setTimeout(function() {
                    popupMessage.classList.add('hidden');

                // Redirigir al enlace original después de que el mensaje desaparezca
                window.location.href = button.href; 

                }, 300); // Espera a que la transición de opacidad termine
            }, 400); // Duración del mensaje visible en milisegundos
        });
    });
});

