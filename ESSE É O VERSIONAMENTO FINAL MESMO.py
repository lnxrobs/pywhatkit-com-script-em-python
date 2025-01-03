import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pywhatkit as kit

# Função para autenticar e acessar a planilha do Google Sheets
def autenticar_google_sheets():
    # Define o escopo de acesso à API do Google Sheets e Google Drive
    escopos = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    
    # Caminho para o arquivo JSON de credenciais da conta de serviço
    credenciais = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", escopos)
    
    # Autoriza e autentica a API
    cliente = gspread.authorize(credenciais)
    return cliente

# Função para ler os dados do motorista e agenciador na planilha
def obter_dados(cliente, nome_motorista):
    # Acesse a planilha (substitua pelo nome da sua planilha)
    planilha = cliente.open("TESTE DE SCRIPT")  # Nome da planilha no Google Sheets
    aba = planilha.sheet1  # A primeira aba da planilha

    # Procura pelo nome na coluna "Motorista" e obtém os dados associados
    lista_dados = aba.get_all_records()  # Obtemos todas as linhas como uma lista de dicionários
    for linha in lista_dados:
        if linha["Motorista"].strip().upper() == nome_motorista.strip().upper():  # Comparação insensível a maiúsculas e minúsculas
            return linha["Motorista"], linha["Placa Cavalo"], linha["Agência"], linha["Agenciador"]  # Retorna os dados do motorista, placa, agência e agenciador
    return None, None, None, None  # Caso não encontre o motorista

# Função para enviar a mensagem para o grupo do WhatsApp
def enviar_mensagem_no_grupo(link_grupo, agenciador, agencia, motorista, placa_cavalo):
    # Formatação da mensagem com os dados extraídos
    mensagem_completa = (f"Olá {agenciador} de {agencia}, gentileza orientar condutor {motorista} "
                         f"da placa {placa_cavalo} sobre nosso processo. Ordem foi entregue em mãos? Podemos confirmar?")

    # Envia a mensagem para o grupo via WhatsApp Web
    kit.sendwhatmsg_to_group(link_grupo, mensagem_completa, 15, 0)  # Envia a mensagem para o grupo às 15:00h (ajuste conforme necessário)

# Função principal
def main(
