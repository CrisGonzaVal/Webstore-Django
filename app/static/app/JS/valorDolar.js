document.addEventListener('DOMContentLoaded', function () {
    fetch('https://api.exchangerate-api.com/v4/latest/USD')
        .then(response => response.json())
        .then(data => {
            const valorDolar = data.rates.CLP;
            document.getElementById('valor-dolar').innerText = `US$1 = CLP$${valorDolar}`;
        })
        .catch(error => {
            console.error('Error fetching the dollar value:', error);
            document.getElementById('valor-dolar').innerText = 'US$1 = No disponible';
        });
});