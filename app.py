from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return 'API StatusInvest funcionando!'

@app.route('/dados')
def dados_acao():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({'erro': 'Ticker não informado'}), 400

    url = f"https://statusinvest.com.br/acoes/{ticker.lower()}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    def encontrar_valor_por_label(label):
        try:
            elemento = soup.find("h3", string=label)
            if elemento:
                valor = elemento.find_next("strong")
                return valor.text.strip()
            return "N/A"
        except:
            return "N/A"

    resultado = {
        "ticker": ticker.upper(),
        "pl": encontrar_valor_por_label("P/L"),
        "dividend_yield": encontrar_valor_por_label("Dividend yield"),
        "roe": encontrar_valor_por_label("ROE")
    }

    return jsonify(resultado)