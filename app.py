from flask import Flask, request, render_template, jsonify
import requests
import socket

app = Flask(__name__)

def get_ip_info(ip):
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        data = response.json()
        org = data.get('org', 'N/A')
        if 'AS' in org:
            org = org.split(' ', 1)[1]
        return {'org': org}
    except requests.RequestException:
        return {'org': 'N/A'}

def get_reverse_dns(ip):
    try:
        reverse_dns = socket.gethostbyaddr(ip)
        return reverse_dns[0] if reverse_dns else 'N/A'
    except socket.herror:
        return 'N/A'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ip-info', methods=['POST'])
def ip_info():
    data = request.get_json()
    ip = data.get('ip', '')

    ip_info = get_ip_info(ip)
    reverse_dns = get_reverse_dns(ip)

    return jsonify({'org': ip_info.get('org', 'N/A'), 'reverse_dns': reverse_dns})

if __name__ == '__main__':
    app.run(host='::', port=8080)
