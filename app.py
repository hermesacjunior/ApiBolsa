from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return "API ApiBolsa está no ar!"

@app.route('/dados/<ticker>')
def dados(ticker):
    url = f'https://statusinvest.com.br/acao/{ticker.lower()}'
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return jsonify({'error': 'Erro ao acessar StatusInvest'}), 500

    soup = BeautifulSoup(response.text, 'html.parser')

    def buscar_valor(texto):
        div = soup.find('h3', string=texto)
        if div:
            valor = div.find_next('strong')
            return valor.text.strip() if valor else 'N/A'
        return 'N/A'

    resultado = {
        'ticker': ticker.upper(),
        'P/L': buscar_valor('P/L'),
        'Dividend Yield': buscar_valor('Dividend Yield'),
        'ROE': buscar_valor('ROE')
    }

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
