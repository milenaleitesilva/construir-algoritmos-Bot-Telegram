import os
import time
import requests
from dotenv import load_dotenv
from api_bcb import consultar_indicador

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}/"


def enviar_mensagem(chat_id, texto):
    try:
        requests.post(
            URL + "sendMessage",
            data={"chat_id": chat_id, "text": texto},
            timeout=15
        )
    except requests.RequestException as erro:
        print(f"Erro ao enviar mensagem: {erro}")


def processar_mensagem(mensagem):
    # Ignora mensagens que não sejam texto
    if "text" not in mensagem:
        return

    chat_id = mensagem["chat"]["id"]
    texto = mensagem["text"].strip().lower()

    if texto == "/start":
        resposta = (
            "Olá! Bem-vindo ao DataPulse BR! 📊\n\n"
            "Consulte indicadores econômicos brasileiros em tempo real:\n\n"
            "/ipca - Consultar inflação (IPCA mensal)\n"
            "/selic - Consultar taxa básica de juros (Selic)\n"
            "/dolar - Consultar cotação do Dólar (PTAX)\n"
            "/ajuda - Ver comandos disponíveis"
        )
    elif texto == "/ipca":
        resposta = consultar_indicador(433, "IPCA Mensal", "%")
    elif texto == "/selic":
        resposta = consultar_indicador(432, "Meta Selic", "% ao ano")
    elif texto == "/dolar":
        resposta = consultar_indicador(1, "Dólar (Venda PTAX)", " BRL")
    elif texto == "/ajuda":
        resposta = (
            "Comandos disponíveis:\n\n"
            "/start - Mensagem inicial\n"
            "/ipca - Consulta o último IPCA mensal\n"
            "/selic - Consulta a Meta Selic atual\n"
            "/dolar - Consulta a cotação do Dólar\n"
            "/ajuda - Exibe esta lista"
        )
    else:
        resposta = (
            "Não reconheci esse comando. 🤔\n"
            "Digite /ajuda para ver as opções disponíveis."
        )

    enviar_mensagem(chat_id, resposta)


def iniciar_bot():
    print("DataPulse BR iniciado! Pressione Ctrl+C para encerrar.")
    ultimo_update = None

    while True:
        parametros = {"timeout": 30}
        if ultimo_update is not None:
            parametros["offset"] = ultimo_update + 1

        try:
            resposta = requests.get(
                URL + "getUpdates",
                params=parametros,
                timeout=35
            )
            resposta.raise_for_status()
            atualizacoes = resposta.json().get("result", [])

            for update in atualizacoes:
                ultimo_update = update["update_id"]
                mensagem = update.get("message")
                if mensagem:
                    processar_mensagem(mensagem)

        except requests.RequestException as erro:
            print(f"Erro de conexão: {erro}. Tentando novamente em 5s...")
            time.sleep(5)


if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("Token do Telegram não encontrado no arquivo .env")
    iniciar_bot()