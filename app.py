from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return "API de Análise de Ações está online!"

@app.route('/analise/<ticker>', methods=['GET'])
def analisar_acao(ticker):
    url = f'https://statusinvest.com.br/acao/{ticker}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return jsonify({'error': 'Erro ao acessar StatusInvest'}), 500

    soup = BeautifulSoup(response.text, 'html.parser')

    def buscar_valor(texto):
        tag = soup.find('strong', string=texto)
        if tag:
            valor = tag.find_parent('div').find_next_sibling('div').text.strip()
            return valor
        return 'N/A'

    # Indicadores principais
    indicadores = {
        'P/L': buscar_valor('P/L'),
        'Dividend Yield': buscar_valor('Dividend Yield'),
        'ROE': buscar_valor('ROE'),
        'ROIC': buscar_valor('ROIC'),
        'EV/EBITDA': buscar_valor('EV/EBITDA'),
        'Margem Líquida': buscar_valor('Margem Líquida'),
        'Crescimento de Lucro': buscar_valor('Crescimento Receita 5 anos'),
        'Dívida/Patrimônio': buscar_valor('Dív. Líquida/ Patrim.'),
        'Setor': buscar_valor('Setor'),
        'Valor de Mercado': buscar_valor('Valor de mercado'),
        'IPCA': '4,5%',
        'Taxa Selic': '10,5%',
        'PIB': '2,3%',
        'Câmbio': '5,00'
    }

    # Lógica de pontuação
    pontos = 0
    if indicadores['P/L'] != 'N/A' and float(indicadores['P/L'].replace(',', '.')) < 15: pontos += 1
    if indicadores['Dividend Yield'] != 'N/A' and float(indicadores['Dividend Yield'].replace(',', '.')) > 5: pontos += 1
    if indicadores['ROE'] != 'N/A' and float(indicadores['ROE'].replace('%', '').replace(',', '.')) > 12: pontos += 1
    if indicadores['ROIC'] != 'N/A' and float(indicadores['ROIC'].replace('%', '').replace(',', '.')) > 10: pontos += 1
    if indicadores['EV/EBITDA'] != 'N/A' and float(indicadores['EV/EBITDA'].replace(',', '.')) < 10: pontos += 1
    if indicadores['Margem Líquida'] != 'N/A' and float(indicadores['Margem Líquida'].replace('%', '').replace(',', '.')) > 10: pontos += 1
    if indicadores['Crescimento de Lucro'] != 'N/A' and float(indicadores['Crescimento de Lucro'].replace('%', '').replace(',', '.')) > 0: pontos += 1
    if indicadores['Dívida/Patrimônio'] != 'N/A' and float(indicadores['Dívida/Patrimônio'].replace(',', '.')) < 1: pontos += 1

    if pontos >= 7:
        decisao = 'COMPRAR'
    elif 4 <= pontos < 7:
        decisao = 'MANTER'
    else:
        decisao = 'VENDER'

    return jsonify({
        'ticker': ticker.upper(),
        'pontuacao': f"{pontos}/8",
        'decisao': decisao,
        **indicadores
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
