import random
import string
import requests
import json

API_KEY = "tempmail.20250410.suzjrmjnpg2cs2hos95zurlxuawt970oke9z6pf8qd221qpx"
headers = {"Authorization": API_KEY}

def handler(request):
    def gerar_nome():
        prefixos = ['user', 'admin', 'guest', 'client', 'member']
        sufixo = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        return random.choice(prefixos) + sufixo

    def gerar_senha():
        tamanho = random.randint(8, 20)
        simbolos = '!@#$%^&*+=_-'
        caracteres = string.ascii_letters + string.digits + simbolos
        return ''.join(random.choices(caracteres, k=tamanho))

    nome = gerar_nome()
    senha = gerar_senha()

    try:
        resp = requests.post("https://api.tempmail.lol/v2/inbox/create", headers=headers)
        if not resp.ok:
            return {
                "statusCode": resp.status_code,
                "body": json.dumps({
                    "erro": "Erro ao criar email",
                    "detalhes": resp.text
                }),
                "headers": {"Content-Type": "application/json"}
            }
        inbox = resp.json()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "usuario": nome,
                "senha": senha,
                "email": inbox["address"],
                "token": inbox["token"]
            }),
            "headers": {
                "Content-Type": "application/json"
            }
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"erro": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }
