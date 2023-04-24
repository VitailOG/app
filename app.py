import io
import os
import time
from datetime import datetime

import requests
from flask import Flask, jsonify, render_template, request, send_file, make_response

import ftp
from config import ADDRESS_BACKEND, CHUNK_SIZE
from fetcher import get_near_vps

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', name="Vitalik")


@app.route('/', methods=['POST'])
def upload():
    start = time.process_time_ns()
    ip_addr = request.remote_addr
    print(ip_addr)
    near_vps = get_near_vps(ip_addr)

    url = request.get_json()['link']
    filename = os.path.basename(url)

    response = requests.get(url, stream=True)

    file_buffer = io.BytesIO()

    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        file_buffer.write(chunk)
    file_buffer.seek(0)

    ftp.upload(filename=filename, vps=near_vps.vps_info, buffer=file_buffer)
    print('finish')
    return jsonify(
        {
            "duration": (time.process_time_ns() - start) / 1_000_000_000,
            "link": f"http://{ADDRESS_BACKEND}/download/" + filename,
            "vps": near_vps.vps.server_name,
            "city": near_vps.vps_info.city,
            "ip": near_vps.vps_info.ip,
            "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }
    )


@app.route('/download/<name>', methods=['POST'])
def download(name):
    start = time.process_time_ns()
    ip_addr = request.remote_addr
    print(ip_addr)

    near_vps = get_near_vps(ip_addr)
    file_buffer = ftp.download(name, near_vps.vps_info)
    file_buffer.seek(0)
    response = make_response(send_file(file_buffer, as_attachment=True, download_name=name))

    message = f"`VPS - {near_vps.vps.server_name}, " \
              f"City - {near_vps.vps_info.city}, " \
              f"ip - {near_vps.vps_info.ip}, " \
              f"duration - {(time.process_time_ns() - start) / 1_000_000_000}, " \
              f"created at - {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}`"

    response.headers['X-Message'] = message
    print('finish')
    return response


if __name__ == '__main__':
    app.run()
