from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return "API ApiBolsa está no ar!"

@app.route('/dados/<ticker>')
def dados_acao(ticker):
    url = f'https://statusinvest.com.br/acoes/{ticker}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        return jsonify({'error': 'Falha na requisição', 'details': str(e)}), 500

    if response.status_code != 200:
        return jsonify({'error': 'Erro ao acessar StatusInvest'}), 500

    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        pl = soup.find('h3', string='P/L').find_next('strong').text.strip()
    except:
        pl = 'N/A'
    
    try:
        dy = soup.find('h3', string='Dividend Yield').find_next('strong').text.strip()
    except:
        dy = 'N/A'

    try:
        roe = soup.find('h3', string='ROE').find_next('strong').text.strip()
    except:
        roe = 'N/A'

    return jsonify({
        'ticker': ticker.upper(),
        'P/L': pl,
        'Dividend Yield': dy,
        'ROE': roe
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
