from flask import Flask, request, render_template_string
import ipaddress
import requests

app = Flask(__name__)

@app.before_request
def filter_invalid_requests():
    if not request.is_secure and "HTTP/" not in request.environ.get('SERVER_PROTOCOL', ''):
        return "Bad Request", 400

@app.route('/')
def check_ip():
    # Obtém o endereço IP do cliente dos cabeçalhos X-Forwarded-For ou X-Real-IP
    forwarded_for = request.headers.get('X-Forwarded-For')
    real_ip = request.headers.get('X-Real-IP')
    ip_address = forwarded_for.split(',')[0].strip() if forwarded_for else real_ip or request.remote_addr

    # Consulta a API para obter informações sobre o IP
    ip_info = {}
    try:
        response = requests.get(f'https://ipinfo.io/{ip_address}/json')
        ip_info = response.json()
    except requests.RequestException:
        ip_info = {'org': 'Desconhecido'}

    # Extrai apenas o nome do provedor
    org_info = ip_info.get('org', 'Desconhecido')
    # Assume que o nome do provedor está antes do número AS
    provider_name = ' '.join(part for part in org_info.split() if not part.startswith('AS'))

    try:
        ip_obj = ipaddress.ip_address(ip_address)
        if ip_obj.version == 6 and ip_obj.ipv4_mapped:
            ip_type = "IPv4"
            ip_address = str(ip_obj.ipv4_mapped)
            message = f"""
            <div class="logo ipv4-logo">
                <span>IPv4</span>
            </div>
            <div class="container">
                <h1>💔 Que pena!<br>Você não tem IPv6!</h1>
                <p>Seu IP: {ip_address}</p>
                <p>Provedor: {provider_name}</p>
            </div>
            """
        else:
            ip_type = "IPv6" if ip_obj.version == 6 else "IPv4"
            message = f"""
            <div class="logo {'ipv6-logo' if ip_type == 'IPv6' else 'ipv4-logo'}">
                <span>{ip_type}</span>
            </div>
            <div class="container">
                <h1>{"🎉 Parabéns!<br>Você está usando IPv6!" if ip_type == 'IPv6' else "💔 Que pena! Você não tem IPv6!"}</h1>
                <p>Seu IP: {ip_address}</p>
                <p>Provedor: {provider_name}</p>
            </div>
            """
    except ValueError:
        ip_type = "Desconhecido"
        message = f"""
        <div class="container">
            <h1>🚫 Não conseguimos detectar seu IP!</h1>
            <p>Seu IP: {ip_address}</p>
            <p>Provedor: {provider_name}</p>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Verificação de IP</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                height: 100vh;
                background: linear-gradient(to right, #00c6ff, #0072ff);
                color: #fff;
                font-family: Arial, sans-serif;
                text-align: center;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                position: relative;
            }}
            .logo {{
                position: absolute;
                top: 180px;
                left: 45,5%;
                transform: translateX(-50%);
                width: 120px;
                height: 120px;
                border-radius: 50%;
                border: 10px solid transparent;
                border-top-color: #fff; /* Cor da borda que vai girar */
                animation: spin 3s linear infinite;
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 1.5em;
                color: #fff;
                background: rgba(0, 0, 0, 0.7);
            }}
            .ipv4-logo {{
                border-top-color: #ff6f61; /* Cor específica para IPv4 */
            }}
            .ipv6-logo {{
                border-top-color: #4caf50; /* Cor específica para IPv6 */
            }}
            .container {{
                background-color: rgba(0, 0, 0, 0.5);
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
                max-width: 90%;
                width: 500px;
                margin-top: 100px; /* Espaço suficiente para o círculo acima */
                z-index: 1;
            }}
            h1 {{
                font-size: 2.5em;
                animation: fadeIn 2s ease-in-out;
                margin: 0; /* Remove margem padrão */
            }}
            p {{
                font-size: 1.2em;
            }}
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
            @keyframes spin {{
                from {{ transform: rotate(0deg); }}
                to {{ transform: rotate(360deg); }}
            }}
            @media (max-width: 768px) {{
                .logo {{
                    width: 100px;
                    height: 100px;
                    font-size: 1.2em;
                }}
                .container {{
                    width: 90%;
                    padding: 15px;
                    margin-top: 180px; /* Ajusta a margem para dispositivos menores */
                }}
                h1 {{
                    font-size: 2em;
                }}
                p {{
                    font-size: 1em;
                }}
            }}
            @media (max-width: 480px) {{
                .logo {{
                    width: 80px;
                    height: 80px;
                    font-size: 1em;
                }}
                .container {{
                    width: 90%;
                    padding: 10px;
                    margin-top: 120px; /* Ajusta a margem para dispositivos muito pequenos */
                }}
                h1 {{
                    font-size: 1.5em;
                }}
                p {{
                    font-size: 0.9em;
                }}
            }}
        </style>
    </head>
    <body>
        {message}
<br><a href="https://www.aprendendolinux.com" target="_blank" style="color: #FFFFFF; text-decoration: none; font-size: 0.8em;">Henrique Fagundes</a>
    </body>
    </html>
    """

    return render_template_string(html)

if __name__ == '__main__':
    app.run(host='::', port=5000)
