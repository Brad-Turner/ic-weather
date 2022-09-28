import rp2
from lib.bme280 import BME280
from lib.piicodev_unified import sleep_ms

def connect_to_wifi():
    import network
    import secrets
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print('Connecting to network: ' + secrets.SSID + '...')
        wlan.connect(secrets.SSID, secrets.NETWORK_PASSWORD)
        while not wlan.isconnected():
            pass
        
    print('Connected to network: ' + secrets.SSID)
  
def post_data(data):
    import secrets
    import ujson
    import urequests

    ingest_headers = {
        'authorization': 'Bearer ' + secrets.API_TOKEN,
        'content-type': 'application/json'
    }

    res = urequests.post(secrets.API_ENDPOINT, headers = ingest_headers, data = ujson.dumps(data))
    print(res.text)

rp2.country('AU')

connect_to_wifi()

sensor = BME280() # initialise the sensor
zeroAlt = sensor.altitude() # take an initial altitude reading

while True:
    tempC, presPa, humRH = sensor.values() # read all data from the sensor
    pres_hPa = presPa / 100 # convert air pressurr Pascals -> hPa (or mbar, if you prefer)

    weather_data = [
        { 
            'temp': tempC, 
            'pressure': pres_hPa, 
            'relativeHumidity': humRH 
        }
    ]

    post_data(weather_data)
    
    # Altitude demo
    # print(sensor.altitude() - zeroAlt) # Print the pressure CHANGE since the script began
    sleep_ms(1000)
