import requests
import json

API_KEY = "tempmail.20250410.suzjrmjnpg2cs2hos95zurlxuawt970oke9z6pf8qd221qpx"
headers = {"Authorization": API_KEY}

def handler(request):
    token = request.args.get('token')

    if not token:
        return {
            "statusCode": 400,
            "body": json.dumps({"erro": "Token é obrigatório."}),
            "headers": {"Content-Type": "application/json"}
        }

    try:
        # Solicitar emails da caixa de entrada
        resp = requests.get(f"https://api.tempmail.lol/v2/inbox", headers=headers, params={"token": token})
        if not resp.ok:
            return {
                "statusCode": resp.status_code,
                "body": json.dumps({
                    "erro": "Erro ao buscar emails",
                    "detalhes": resp.text
                }),
                "headers": {"Content-Type": "application/json"}
            }
        
        data = resp.json()

        # Se a caixa expirou
        if data.get("expired"):
            return {
                "statusCode": 200,
                "body": json.dumps({"expirado": True}),
                "headers": {"Content-Type": "application/json"}
            }

        # Obter mensagens recebidas
        mensagens = []
        for email in data.get("emails", []):
            mensagens.append({
                "de": email["from"],
                "assunto": email["subject"],
                "corpo": email.get("html", "Sem conteúdo")
            })

        return {
            "statusCode": 200,
            "body": json.dumps({
                "expirado": False,
                "mensagens": mensagens
            }),
            "headers": {"Content-Type": "application/json"}
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"erro": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }
