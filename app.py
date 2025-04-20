import random
import string
import requests
import time
from flask import Flask, jsonify

app = Flask(__name__)

# ==== Configurações ==== 
API_KEY_TEMPMail = "tempmail.20250410.suzjrmjnpg2cs2hos95zurlxuawt970oke9z6pf8qd221qpx"
headers = {"Authorization": API_KEY_TEMPMail}

# ==== Funções de geração ====
def gerar_nome():
    prefixos = ['user', 'admin', 'guest', 'client', 'member']
    sufixo = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return random.choice(prefixos) + sufixo

def gerar_senha():
    tamanho = random.randint(8, 20)
    simbolos = '!@#$%^&*+=_-'
    caracteres = string.ascii_letters + string.digits + simbolos
    senha = ''.join(random.choices(caracteres, k=tamanho))
    return senha

# ==== TempMail Functions ====
def criar_caixa_email():
    url = "https://api.tempmail.lol/v2/inbox/create"
    response = requests.post(url, headers=headers)
    if response.ok:
        return response.json()
    return None

def buscar_emails(token):
    url = "https://api.tempmail.lol/v2/inbox"
    params = {"token": token}
    response = requests.get(url, params=params, headers=headers)
    if response.ok:
        return response.json()
    return {}

# ==== Endpoints da API ====

@app.route('/gerar_conta', methods=['GET'])
def gerar_conta():
    # Gerar dados do usuário
    usuario = gerar_nome()
    senha = gerar_senha()

    # Criar email temporário
    inbox = criar_caixa_email()
    if inbox:
        email = inbox["address"]
        token = inbox["token"]
        # Monitorar os e-mails (simulado, por questões de tempo, não monitoraremos de fato)
        return jsonify({
            'usuario': usuario,
            'senha': senha,
            'email': email
        })
    else:
        return jsonify({'error': 'Erro ao criar email temporário.'}), 500

@app.route('/monitorar_emails/<token>', methods=['GET'])
def monitorar_emails(token):
    recebidos = set()
    while True:
        data = buscar_emails(token)
        if data.get("expired"):
            return jsonify({"message": "A caixa expirou."}), 404
        
        for email in data.get("emails", []):
            if email["date"] not in recebidos:
                recebidos.add(email["date"])
                corpo = email.get("html", "Sem conteúdo")
                return jsonify({
                    'de': email['from'],
                    'assunto': email['subject'],
                    'corpo': corpo
                })
        time.sleep(10)

if __name__ == '__main__':
    app.run(debug=True)
