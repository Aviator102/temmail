from flask import Flask, render_template, jsonify, request
import random
import string
import requests
import threading
import time
from bs4 import BeautifulSoup

app = Flask(__name__)

API_KEY_TEMPMail = "tempmail.20250410.suzjrmjnpg2cs2hos95zurlxuawt970oke9z6pf8qd221qpx"
headers = {"Authorization": API_KEY_TEMPMail}
monitoring_threads = {}

def gerar_nome():
    prefixos = ['user', 'admin', 'guest', 'client', 'member']
    sufixo = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return random.choice(prefixos) + sufixo

def gerar_senha():
    tamanho = random.randint(8, 20)
    simbolos = '!@#$%^&*+=_-'
    caracteres = string.ascii_letters + string.digits + simbolos
    return ''.join(random.choices(caracteres, k=tamanho))

def criar_caixa_email():
    url = "https://api.tempmail.lol/v2/inbox/create"
    response = requests.post(url, headers=headers)
    return response.json() if response.ok else None

def buscar_emails(token):
    url = "https://api.tempmail.lol/v2/inbox"
    params = {"token": token}
    response = requests.get(url, params=params, headers=headers)
    return response.json() if response.ok else {}

def extrair_texto_html(html):
    soup = BeautifulSoup(html, 'lxml')
    for tag in soup(['script', 'style', 'iframe', 'img']):
        tag.decompose()
    texto = soup.get_text(separator=' ', strip=True)
    links = [f"{a.get_text(strip=True)}: {a['href']}" for a in soup.find_all('a', href=True)]
    if links:
        texto += "\n\n🔗 Links encontrados:\n" + "\n".join(links)
    return texto

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar', methods=['POST'])
def gerar():
    usuario = gerar_nome()
    senha = gerar_senha()
    email_info = criar_caixa_email()
    if not email_info:
        return jsonify({'erro': 'Erro ao criar email.'}), 500
    token = email_info['token']
    email = email_info['address']
    monitoring_threads[token] = []
    thread = threading.Thread(target=monitorar_emails, args=(token,), daemon=True)
    thread.start()
    return jsonify({'usuario': usuario, 'senha': senha, 'email': email, 'token': token})

@app.route('/mensagens/<token>')
def mensagens(token):
    data = buscar_emails(token)
    if data.get("expired"):
        return jsonify({'expirado': True, 'mensagens': []})
    mensagens = []
    for email in data.get("emails", []):
        corpo = extrair_texto_html(email.get("html", "")) or "Sem conteúdo"
        mensagens.append({
            'de': email['from'],
            'assunto': email['subject'],
            'corpo': corpo
        })
    return jsonify({'expirado': False, 'mensagens': mensagens})

def monitorar_emails(token):
    pass  # opcional: deixar frontend buscar com polling

if __name__ == '__main__':
    app.run(debug=True)
