document.addEventListener('DOMContentLoaded', function () {
    fetch('https://api.exchangerate-api.com/v4/latest/USD')
        .then(response => response.json())
        .then(data => {
            const valorDolar = data.rates.CLP;
            document.getElementById('valor-dolar').innerText = `1 USD → CLP:$${valorDolar}`;
        })
        .catch(error => {
            console.error('Error fetching the dollar value:', error);
            document.getElementById('valor-dolar').innerText = '1 USD = No disponible';
        });
});