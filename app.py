from flask import Flask, jsonify, request
import requests
import random
import string

app = Flask(__name__)

API_KEY_TEMPMail = "Bearer tempmail.20250410.suzjrmjnpg2cs2hos95zurlxuawt970oke9z6pf8qd221qpx"
BASE_URL = "https://api.tempmail.lol"
HEADERS = {"Authorization": API_KEY_TEMPMail}

def gerar_nome():
    prefixos = ['user', 'admin', 'guest', 'client', 'member']
    sufixo = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return random.choice(prefixos) + sufixo

def gerar_senha():
    simbolos = '!@#$%^&*+=_-'
    caracteres = string.ascii_letters + string.digits + simbolos
    return ''.join(random.choices(caracteres, k=random.randint(8, 16)))

def criar_caixa_email():
    url = f"{BASE_URL}/v2/inbox/create"
    response = requests.post(url, headers=HEADERS)
    if response.status_code == 201:
        return response.json()
    return None

def buscar_emails(token):
    url = f"{BASE_URL}/v2/inbox"
    params = {"token": token}
    response = requests.get(url, headers=HEADERS, params=params)
    if response.ok:
        return response.json()
    return {"error": "Erro ao buscar emails"}

@app.route('/gerar_conta', methods=['GET'])
def gerar_conta():
    usuario = gerar_nome()
    senha = gerar_senha()
    inbox = criar_caixa_email()

    if inbox:
        return jsonify({
            "usuario": usuario,
            "senha": senha,
            "email": inbox["address"],
            "token": inbox["token"]
        })
    else:
        return jsonify({"error": "Não foi possível criar a caixa de email temporária."}), 500

@app.route('/verificar_emails/<token>', methods=['GET'])
def verificar_emails(token):
    data = buscar_emails(token)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
