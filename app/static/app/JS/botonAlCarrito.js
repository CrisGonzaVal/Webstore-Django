document.getElementById('botonAlCarrito').addEventListener('click', function() {
            // Cambiar el color del botón al hacer clic
            this.classList.toggle('active');

            // Cambiar el contenido del enlace
            var link = document.getElementById('botonLink');
            if (this.classList.contains('active')) {
                link.textContent = 'Se cargó en el Carro ';
            } else {
                link.textContent = 'Agregar al carro';
            }

            // Detener la acción de navegación por defecto del enlace
            event.preventDefault();
        });