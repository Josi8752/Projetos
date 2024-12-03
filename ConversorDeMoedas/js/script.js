document.getElementById('convertButton').addEventListener('click', convertCurrency);

function convertCurrency(){

    const amount = parseFloat(document.getElementById('amount').value);
    const formCurrency = document.getElementById('fromCurrency').value;
    const toCurrency = document.getElementById('toCurrency').value;


    if (isNaN(amount) || amount <= 0){

        alert('Por favor, insira um valor válido.');

        return;
    }

    const rates = {

        BRL: {USD: 0.2, EUR: 0.18},
        USD: {BRL: 5, EUR: 0.9},
        EUR: {BRL: 5.6, USD: 1.1}

    };

    const convertedAmount = rates[formCurrency][toCurrency]
    ? amount * rates[formCurrency][toCurrency]
    : amount;

    document.getElementById('result').textContent = `Valor convertido: ${convertedAmount.toFixed(2)} ${toCurrency}`;
}