import os
import ipaddress
import socket
from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

NA = 'N/A'


def get_ip_info(ip):
    empty = {k: NA for k in ('org', 'asn', 'city', 'region', 'country', 'postal', 'timezone', 'loc', 'hostname')}
    try:
        data = requests.get(f'https://ipinfo.io/{ip}/json', timeout=5).json()
    except (requests.RequestException, ValueError):
        return empty

    org = data.get('org', NA)
    asn = NA
    if org.startswith('AS') and ' ' in org:
        asn, org = org.split(' ', 1)

    return {
        'org': org,
        'asn': asn,
        'city': data.get('city', NA),
        'region': data.get('region', NA),
        'country': data.get('country', NA),
        'postal': data.get('postal', NA),
        'timezone': data.get('timezone', NA),
        'loc': data.get('loc', NA),
        'hostname': data.get('hostname', NA),
    }


def get_reverse_dns(ip):
    try:
        return socket.gethostbyaddr(ip)[0] or NA
    except (socket.herror, socket.gaierror, OSError):
        return NA


def classify_ip(addr):
    if addr.is_loopback:
        return 'Loopback'
    if addr.is_link_local:
        return 'Link-local'
    if addr.is_private:
        return 'Privado / ULA'
    if addr.is_multicast:
        return 'Multicast'
    if addr.is_reserved:
        return 'Reservado'
    return 'Público (Global Unicast)'


@app.route('/')
def index():
    version = os.environ.get('APP_VERSION', 'dev-local')
    return render_template('index.html', version=version)


@app.route('/ip-info', methods=['POST'])
def ip_info():
    data = request.get_json(silent=True) or {}
    ip = str(data.get('ip', '')).strip()

    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return jsonify({'error': 'IP inválido ou não fornecido'}), 400

    info = get_ip_info(ip)
    info['reverse_dns'] = get_reverse_dns(ip)
    info['version'] = f'IPv{addr.version}'
    info['scope'] = classify_ip(addr)
    info['expanded'] = addr.exploded if addr.version == 6 else str(addr)
    return jsonify(info)


if __name__ == '__main__':
    app.run(host='::', port=8080)
