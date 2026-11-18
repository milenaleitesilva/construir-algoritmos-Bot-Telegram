import requests

def consultar_indicador(codigo, nome, unidade="%"):
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados/ultimos/1?formato=json"

    try:
        resposta = requests.get(url, timeout=15)
        resposta.raise_for_status()
        dados = resposta.json()

        if not dados:
            return f"Não encontrei dados para {nome}."

        ultimo_registro = dados[-1]
        data = ultimo_registro["data"]
        valor = ultimo_registro["valor"]

        return (
            f"📊 {nome}\n"
            f"📅 Data de referência: {data}\n"
            f"📈 Valor: {valor}{unidade}"
        )

    except requests.RequestException:
        return "Não foi possível consultar o Banco Central. Tente novamente."