
# ETLProjectAPIExtract

Este projeto é um pipeline ETL (Extract, Transform, Load) desenvolvido em Python, utilizando a biblioteca `requests` para extração de dados de APIs. O objetivo é coletar dados de uma fonte externa, realizar transformações necessárias e carregar os dados processados em um destino (arquivo, banco de dados, etc).

## Funcionalidades

- **Extração:** Coleta de dados via requisições HTTP usando `requests`.
- **Transformação:** Limpeza e manipulação dos dados extraídos.
- **Carga:** Armazenamento dos dados transformados em um destino definido.

## Requisitos

- Python 3.8+
- requests

## Instalação
`pip install requests`

## Como usar

1. Clone o repositório:
    
    `git clone https://github.com/seuusuario/ETLProjectAPIExtract.git`
    
    `cd ETLProjectAPIExtract`
2. Execute o script principal:
    
    `python main.py`
    
## Estrutura do Projeto
ETLProjectAPIExtract/
├── main.py
├── etl/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── README.md

## Licença
