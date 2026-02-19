import os
from flask import Flask, request, render_template, jsonify
import requests
import socket

app = Flask(__name__)

def get_ip_info(ip):
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json', timeout=5)
        data = response.json()
        org = data.get('org', 'N/A')
        if 'AS' in org:
            org = org.split(' ', 1)[1]
        
        return {
            'org': org,
            'city': data.get('city', 'N/A'),
            'country': data.get('country', 'N/A')
        }
    except requests.RequestException:
        return {'org': 'N/A', 'city': 'N/A', 'country': 'N/A'}

def get_reverse_dns(ip):
    try:
        # gethostbyaddr suporta nativamente IPv4 e IPv6
        reverse_dns = socket.gethostbyaddr(ip)
        return reverse_dns[0] if reverse_dns else 'N/A'
    except socket.herror:
        return 'N/A'

@app.route('/')
def index():
    version = os.environ.get('APP_VERSION', 'dev-local')
    return render_template('index.html', version=version)

@app.route('/ip-info', methods=['POST'])
def ip_info():
    data = request.get_json()
    ip = data.get('ip', '')
    
    if not ip:
         return jsonify({'error': 'IP não fornecido'}), 400

    ip_info_data = get_ip_info(ip)
    reverse_dns = get_reverse_dns(ip)

    return jsonify({
        'org': ip_info_data.get('org', 'N/A'),
        'city': ip_info_data.get('city', 'N/A'),
        'country': ip_info_data.get('country', 'N/A'),
        'reverse_dns': reverse_dns
    })

if __name__ == '__main__':
    app.run(host='::', port=8080)