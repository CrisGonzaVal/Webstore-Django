document.getElementById('botonAlCarro').addEventListener('click', function() {
            // Cambiar el color del botón al hacer clic
            this.classList.toggle('active');

            // Cambiar el contenido del enlace
            var link = document.getElementById('buttonLink');
            if (this.classList.contains('active')) {
                link.textContent = 'Producto en el ';
            } else {
                link.textContent = 'Haz clic aquí';
            }

            // Detener la acción de navegación por defecto del enlace
            event.preventDefault();
        });