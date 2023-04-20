import requests

from flask import Flask, render_template, request

app = Flask(__name__)
# u = 'http://chi.download.datapacket.com/100mb.bin'
# ip = "5.58.55.183"
# print(requests.get(f'http://api.ipapi.com/api/{ip}?access_key={"65df7c82ddb887fad4c61c3fb1459039"}').json())


@app.route('/')
def hello_world():
    print(
        requests.get(
            f'http://api.ipapi.com/api/{request.remote_addr}?access_key={"65df7c82ddb887fad4c61c3fb1459039"}'
        ).json()
    )

    return render_template('index.html', name="Vitalik")


if __name__ == '__main__':
    app.run()
