import time
import requests
from tinydb import TinyDB       # Tinydb é um banco NoSQL leve e fácil de usar
from datetime import datetime


def extract_dados_bitcoin():
    """
    Função para extrair dados do Bitcoin da API da Coinbase.
    """
    url = "https://api.coinbase.com/v2/prices/spot"

    response = requests.get(url)
    dados = response.json()     # Aqui estamos pegando somente os dados
    return dados

# Transformação dos dados
# A função transforma os dados extraídos em um formato mais simples e legível.

def transform_dados_bitcoin(dados):
    valor = dados["data"]["amount"]
    criptomoeda = dados["data"]["base"]
    moeda = dados["data"]["currency"]
    timestamp = datetime.now().timestamp()

    dados_transformados = {
        "valor": valor,
        "criptomoeda": criptomoeda,
        "moeda": moeda,
        "timestamp": timestamp
    }

    return dados_transformados

def salvar_dados_tinydb(dados, db_name="bitcoin.json"):     # Salvando o arquivo em formato Json
    db = TinyDB(db_name)
    db.insert(dados)
    print("Dados salvos no banco de dados")



if __name__ == "__main__":
    # Extração dos dados
    while True:     # Criando um loop para a coleta de dados a cada 15 segundos
        dados_json = extract_dados_bitcoin()
        dados_tratados = transform_dados_bitcoin(dados_json)
        salvar_dados_tinydb(dados_tratados)
        time.sleep(15)
