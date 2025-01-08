import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pywhatkit as kit
from google.oauth2.service_account import Credentials
import json


try:
    with open('credenciais.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(data)
except json.JSONDecodeError as e:
    print("Erro ao decodificar o JSON:", e)
except Exception as e:
    print("Ocorreu um erro inesperado:", e)


# Função para ler os dados do motorista e agenciador na planilha
def obter_dados(cliente, nome_motorista):
    try:
        # Acesse a planilha (substitua pelo nome da sua planilha)
        planilha = cliente.open("TESTE DE SCRIPT")  # Nome da planilha no Google Sheets
        aba = planilha.sheet1  # A primeira aba da planilha

        # Percorrer as linhas e verificar a correspondência
        for linha in aba.get_all_records():
            if linha["Motorista"].strip().upper() == nome_motorista.strip().upper():
                return linha["Motorista"], linha["Placa Cavalo"], linha["Agência"], linha["Agenciador"]
        
        # Caso o motorista não seja encontrado
        return None, None, None, None
    except Exception as e:
        print(f"Erro ao obter dados: {e}")
        return None, None, None, None

# Função para enviar a mensagem para o grupo do WhatsApp
def enviar_mensagem_no_grupo(link_grupo, agenciador, agencia, motorista, placa_cavalo):
    try:
        # Formatação da mensagem
        mensagem_completa = (
            f"Olá {agenciador} de {agencia}, gentileza orientar condutor {motorista} "
            f"da placa {placa_cavalo} sobre nosso processo. Ordem foi entregue em mãos? Podemos confirmar?"
        )

        # Envia a mensagem para o grupo via WhatsApp Web
        kit.sendwhatmsg_to_group(link_grupo, mensagem_completa, 15, 0)  # Envia a mensagem para o grupo às 15:00h (ajuste conforme necessário)
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")


    # Passo 2: Obter dados do motorista
    motorista, placa_cavalo, agencia, agenciador = obter_dados("cliente", "nome_motorista")
    
    if motorista:
        # Passo 3: Enviar mensagem se os dados forem encontrados
        enviar_mensagem_no_grupo(link_grupo, agenciador, agencia, motorista, placa_cavalo)
        print(f"Mensagem enviada para o motorista {motorista}.")
    else:
        print(f"Motorista {{nome_motorista}} não encontrado.")

