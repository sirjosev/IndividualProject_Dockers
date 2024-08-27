import subprocess
import json
from flask import Flask, jsonify

app = Flask(__name__)

def get_router_ip():
    """Fungsi untuk mendapatkan IP router."""
    # Gunakan perintah 'ip route' untuk mencari IP gateway default
    result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    for line in lines:
        if 'default' in line:
            return line.split()[2]
    return None

def monitor_traffic():
    """Fungsi untuk memantau lalu lintas menggunakan tcpdump."""
    router_ip = get_router_ip()
    if not router_ip:
        return {"error": "Router IP not found"}

    # Jalankan tcpdump dengan filter untuk memantau lalu lintas ke/dari router
    command = ['tcpdump', '-n', '-i', 'any', 'host', router_ip]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Proses output tcpdump dan ekstrak informasi yang relevan
    traffic_data = []
    for line in iter(process.stdout.readline, ''):
        # Contoh parsing sederhana, Anda mungkin perlu menyesuaikan ini tergantung pada kebutuhan Anda
        parts = line.split()
        if len(parts) >= 5:
            traffic_data.append({
                "time": parts[0],
                "source": parts[2],
                "destination": parts[4],
                "protocol": parts[1]
            })

    return traffic_data

@app.route('/traffic')
def get_traffic_data():
    """Endpoint untuk mendapatkan data lalu lintas."""
    traffic_data = monitor_traffic()
    return jsonify(traffic_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)