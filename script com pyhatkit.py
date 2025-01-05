import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pywhatkit as kit

# Função para autenticar e acessar a planilha do Google Sheets
def autenticar_google_sheets():
    try:
        # Definindo o escopo de acesso à API do Google Sheets e Google Drive
        escopos = [
            "https://spreadsheets.google.com/feeds", 
            "https://www.googleapis.com/auth/spreadsheets", 
            "https://www.googleapis.com/auth/drive.file", 
            "https://www.googleapis.com/auth/drive"
        ]
        
        # Caminho para o arquivo JSON de credenciais da conta de serviço
        credenciais = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", escopos)
        
        # Autoriza e autentica a API
        cliente = gspread.authorize(credenciais)
        return cliente
    except Exception as e:
        print(f"Erro ao autenticar: {e}")
        return None

# Função para ler os dados do motorista e agenciador na planilha
def obter_dados(cliente, nome_motorista):
    try:
        # Acesse a planilha (substitua pelo nome da sua planilha)
        planilha = cliente.open("")  # Nome da planilha no Google Sheets
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

# Função principal
def main(nome_motorista, link_grupo):
    # Passo 1: Autenticação
    cliente = autenticar_google_sheets()
    if not cliente:
        print("Falha na autenticação. Programa será encerrado.")
        return

    # Passo 2: Obter dados do motorista
    motorista, placa_cavalo, agencia, agenciador = obter_dados(cliente, nome_motorista)
    
    if motorista:
        # Passo 3: Enviar mensagem se os dados forem encontrados
        enviar_mensagem_no_grupo(link_grupo, agenciador, agencia, motorista, placa_cavalo)
        print(f"Mensagem enviada para o motorista {motorista}.")
    else:
        print(f"Motorista {nome_motorista} não encontrado.")

# Exemplo de uso
if __name__ == "__main__":
    # Exemplo de chamada da função principal
    nome_motorista = "João Silva"  # Substitua pelo nome do motorista
    link_grupo = "group_link"  # Substitua pelo link do grupo do WhatsApp
    main(nome_motorista, link_grupo)
