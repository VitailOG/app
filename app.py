import requests

from geopy.distance import geodesic

from flask import Flask, render_template, request

app = Flask(__name__)
# u = 'http://chi.download.datapacket.com/100mb.bin'
# ip = "5.58.55.183"
# print(requests.get(f'http://api.ipapi.com/api/{ip}?access_key={"65df7c82ddb887fad4c61c3fb1459039"}').json())

VPS_SERVERS = {
    "VPS1": {
        "city": "Frankfurt",
        "longitude": 50.110924,
        "latitude": 8.682127,
    }
}


@app.route('/')
def hello_world():
    r = requests.get(
        f'http://api.ipapi.com/api/{request.remote_addr}?access_key={"65df7c82ddb887fad4c61c3fb1459039"}'
    ).json()

    u_lon, u_lat = r['latitude'], r['longitude']
    print((u_lon, u_lat))
    print()
    print((50.110924, 8.682127))
    print()
    print(
        geodesic((u_lon, u_lat), (50.110924, 8.682127)).km
    )
    return render_template('index.html', name="Vitalik")


if __name__ == '__main__':
    app.run()
