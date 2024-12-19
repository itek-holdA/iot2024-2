import network

def connect_to_wifi(ssid, password):
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(ssid, password)
    while not wifi.isconnected():
        pass
    print("Forbundet til Wi-Fi:", wifi.ifconfig()[0])
    return wifi.ifconfig()[0]

# Connect to Wi-Fi
connect_to_wifi(secret.SSID, secret.PASSWORD)