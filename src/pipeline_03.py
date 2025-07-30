import time
import requests
import os
import logging
import logfire
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from logging import basicConfig, getLogger


# Configura o Logfire e adiciona o handler
logfire.configure()
basicConfig(handlers=[logfire.LogfireLoggingHandler()])
logger = getLogger(__name__)
logger.setLevel(logging.INFO)
logfire.instrument_requests()
logfire.instrument_sqlalchemy()

# Importar Base e BitcoinPreco do database.py
from database import Base, BitcoinPreco

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Lê as variáveis separadas do arquivo .env (sem SSL)
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# Monta a URL de conexão ao banco PostgreSQL (sem SSL)
DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Cria o engine e a sessão do banco de dados
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def criar_tabela():
    """Cria a tabela no banco de dados, se não existir."""
    Base.metadata.create_all(engine)
    logger.info("Tabela criada/verificada com sucesso!")


def extract_dados_bitcoin():
    """
    Extrai o JSON completo da API da Coinbase.
    """
    url = "https://api.coinbase.com/v2/prices/spot"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Erro na API: {response.status_code}")
        return None

# Transformação dos dados
# A função transforma os dados extraídos em um formato mais simples e legível.

def transform_dados_bitcoin(dados):
    valor = float(dados["data"]["amount"])
    criptomoeda = dados["data"]["base"]
    moeda = dados["data"]["currency"]
    timestamp = datetime.now()

    dados_transformados = {
        "valor": valor,
        "criptomoeda": criptomoeda,
        "moeda": moeda,
        "timestamp": timestamp
    }
    return dados_transformados

def salvar_dados_postgres(dados):
    """Salva os dados no banco de dados PostgreSQL"""
    session = Session()
    try:
        novo_registro = BitcoinPreco(**dados)
        session.add(novo_registro)
        session.commit()
        logger.info(f"[{dados['timestamp']}] Dados salvos no PostgreSQL!")
    except Exception as ex:
        logger.error(f"Erro ao inserir dados no PostgreSQL: {ex}")
        session.rollback()
    finally:
        session.close()



if __name__ == "__main__":
    criar_tabela()
    print("Iniciando ETL com atualização a cada 15 segundos... (Ctrl+C para parar)")

    while True:
        try:
            dados_json = extract_dados_bitcoin()
            if dados_json:
                dados_tratados = transform_dados_bitcoin(dados_json)
                print("Dados Tratados:", dados_tratados)
                salvar_dados_postgres(dados_tratados)
            time.sleep(15)
        except KeyboardInterrupt:
            print("\nProcesso interrompido pelo usuário. Finalizando...")
            break
        except Exception as e:
            print(f"Erro durante a execução: {e}")
            time.sleep(15)

            
