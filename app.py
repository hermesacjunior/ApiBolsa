from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

pp = Flask(__name__)

@app.route('/')
def home():
    return "API ApiBolsa está no ar!"

# Suas outras rotas aqui...

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
    
    url = f'https://statusinvest.com.br/acao/{ticker}'
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({'error': 'Erro ao acessar StatusInvest'}), 500
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # Exemplo para pegar P/L
    pl = soup.find('div', text='P/L')
    pl_value = pl.find_next_sibling('div').text if pl else 'N/A'
    
    dividend_yield = soup.find('div', text='Dividend Yield')
    dividend_yield_value = dividend_yield.find_next_sibling('div').text if dividend_yield else 'N/A'
    
    roe = soup.find('div', text='ROE')
    roe_value = roe.find_next_sibling('div').text if roe else 'N/A'

    return jsonify({
        'P/L': pl_value,
        'Dividend Yield': dividend_yield_value,
        'ROE': roe_value
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
