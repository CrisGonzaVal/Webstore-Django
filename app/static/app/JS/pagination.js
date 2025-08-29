// Obtener la lista de enlaces de paginación
const paginationLinks = document.querySelectorAll('.pagination a.page-link');

// Agregar evento de clic a cada enlace de paginación
paginationLinks.forEach((link) => {
  link.addEventListener('click', (event) => {
    // Obtener el número de página seleccionada
    const pageNumber = event.target.getAttribute('data-page');

    // Mostrar la página seleccionada
    showPage(pageNumber);
  });
});

// Función para mostrar la página seleccionada
function showPage(pageNumber) {
  // Ocultar todos los productos
  const products = document.querySelectorAll('.tarjet');
  products.forEach((product) => {
    product.style.display = 'none';
  });

// Verificar si hay productos en la página actual
const startIndex = (pageNumber - 1) * 8;
const endIndex = startIndex + 8;
let hasProducts = false;
for (let i = startIndex; i < endIndex; i++) {
  if (products[i]) {
    hasProducts = true;
    break;
  }
}

// Mostrar solo los productos de la página seleccionada si hay productos
if (hasProducts) {
  for (let i = startIndex; i < endIndex; i++) {
    const product = products[i];
    product.style.display = 'block';
  }
} else {
  // Ocultar el page-item vacío
  const pageItem = document.querySelector('#page-item-${pageNumber}');
  pageItem.style.display = 'none';
}
  
}
// Llamar a la función showPage cuando se carga la página
document.addEventListener('DOMContentLoaded', () => {
    showPage(1); // Mostrar la página 1 al cargar la página
  });

  