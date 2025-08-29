document.addEventListener('DOMContentLoaded', function () {
    const cartItems = window.cartItems;

    window.paypal.Buttons({
        style: {
            shape: 'rect',
            layout: 'vertical',
            color: 'gold',
            label: 'paypal',
        },
        createOrder: function(data, actions) {
            return fetch('/api/orders', {
                method: 'post',
                headers: {
                    'content-type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')  // Utiliza una función para obtener el token CSRF
                },
                body: JSON.stringify({
                    cart: cartItems
                })
            }).then(function(res) {
                return res.json();
            }).then(function(orderData) {
                if (orderData.id) {
                    return orderData.id;
                } else {
                    throw new Error('Order creation failed.');
                }
            }).catch(function(err) {
                console.error('Create order error:', err);
            });
        },
        onApprove: function(data, actions) {
            return fetch(`/api/orders/${data.orderID}/capture`, {
                method: 'post',
                headers: {
                    'content-type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            }).then(function(res) {
                return res.json();
            }).then(function(orderData) {
                if (orderData.purchase_units) {
                    const transaction = orderData.purchase_units[0].payments.captures[0];
                    alert(`Transaction ${transaction.status}: ${transaction.id}`);

                    // Limpiar el carrito después de la compra exitosa
                    return fetch('/limpiar_carrito_despues_compra/', {
                        method: 'post',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken'),
                            'content-type': 'application/json'
                        }
                    }).then(function(res) {
                        if (res.ok) {
                            console.log('Carrito limpiado después de la compra');
                            window.location.href = '/gracias/';
                        } else {
                            console.error('Error al limpiar el carrito');
                        }
                    });
                } else {
                    throw new Error('Capture failed.');
                }
            }).catch(function(err) {
                console.error('Capture order error:', err);
            });
        }
    }).render('#paypal-button-container');
});

// Función para obtener el token CSRF de las cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
