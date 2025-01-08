import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pywhatkit as kit
from google.oauth2.service_account import Credentials
import yaml

# Carregar configurações do arquivo YAML
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# ... (resto do código)

def obter_dados(cliente, nome_motorista, **kwargs):
    # ... (implementação com pesquisa por múltiplos critérios)

def enviar_mensagem_no_grupo(link_grupo, agenciador, agencia, motorista, placa_cavalo, horario):
    # ... (implementação com horário personalizável)

# ... (resto do código)

if __name__ == "__main__":
    # Obter dados do motorista a partir de argumentos de linha de comando
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("motorista", help="Nome do motorista")
    args = parser.parse_args()

    # ... (resto do código)