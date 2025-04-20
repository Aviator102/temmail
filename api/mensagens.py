import requests
import json
from bs4 import BeautifulSoup

API_KEY = "tempmail.20250410.suzjrmjnpg2cs2hos95zurlxuawt970oke9z6pf8qd221qpx"
headers = {"Authorization": API_KEY}

def extrair_texto_html(html):
    soup = BeautifulSoup(html, 'lxml')
    for tag in soup(['script', 'style', 'iframe', 'img']):
        tag.decompose()

    texto = soup.get_text(separator=' ', strip=True)
    links = []

    for a in soup.find_all('a', href=True):
        texto_link = a.get_text(strip=True)
        href = a['href']
        links.append(f"{texto_link}: {href}" if texto_link else href)

    if links:
        texto += "\n\n🔗 Links encontrados:\n" + "\n".join(links)

    return texto

def handler(request):
    query = request.get("queryStringParameters") or {}
    token = query.get("token")

    if not token:
        return {
            "statusCode": 400,
            "body": json.dumps({"erro": "Token não fornecido."})
        }

    url = "https://api.tempmail.lol/v2/inbox"
    params = {"token": token}
    response = requests.get(url, headers=headers, params=params)

    if not response.ok:
        return {
            "statusCode": 500,
            "body": json.dumps({"erro": "Erro ao buscar emails."})
        }

    data = response.json()
    if data.get("expired"):
        return {
            "statusCode": 200,
            "body": json.dumps({"expirado": True, "mensagens": []}),
            "headers": {"Content-Type": "application/json"}
        }

    mensagens = []
    for email in data.get("emails", []):
        corpo = extrair_texto_html(email.get("html", "")) or "Sem conteúdo"
        mensagens.append({
            "de": email.get("from"),
            "assunto": email.get("subject"),
            "corpo": corpo
        })

    return {
        "statusCode": 200,
        "body": json.dumps({"expirado": False, "mensagens": mensagens}),
        "headers": {"Content-Type": "application/json"}
    }
