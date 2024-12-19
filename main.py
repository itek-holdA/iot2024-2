from nonblockinghcsr04 import NonBlockingHCSR04
import socket, time, network

# Objekter
left_sensor_module = NonBlockingHCSR04(18, 17, 250)
right_sensor_module = NonBlockingHCSR04(9, 46, 250)
rear_sensor_module = NonBlockingHCSR04(8, 3, 250)

# IP-addresse og HTTP portnummer, for at vi kan finde den anden ESP32 på netværket
SERVER_IP = "172.20.10.5"
SERVER_PORT = 80

# Her sender vi data via HTTP til den anden ESP32
def send_variable(endpoint, value):
    try:
        addr = socket.getaddrinfo(SERVER_IP, SERVER_PORT)[0][-1]
        client = socket.socket()
        client.connect(addr)
        request = (
            f"POST /{endpoint} HTTP/1.1\r\n"
            f"Host: {SERVER_IP}\r\n"
            f"Content-Type: text/plain\r\n"
            f"Content-Length: {len(str(value))}\r\n\r\n"
            f"{value}"
        )
        client.send(request.encode())
        response = client.recv(1024).decode()
        print(f"Response from server ({endpoint}): {response}")
    except Exception as e:
        print(f"Error in send_variable: {e}")
    finally:
        client.close() 

# Metode til vores venstre sensor
def left_sensor():
    distance = left_sensor_module.distance_cm()
    print(f'left: {distance} cm') # DEBUG
    if distance > 30 and distance < 400:
        send_variable("set_left", 1)
        time.sleep(0.5)
        send_variable("set_left", 0)

# Metode til vores højre sensor
def right_sensor():
    distance = right_sensor_module.distance_cm()
    print(f'right: {distance} cm') 
    if distance > 30 and distance < 400:
        send_variable("set_right", 1)
        time.sleep(0.5)
        send_variable("set_right", 0)

# Metode til vores bagudvendte sensor
def rear_sensor():
    distance = rear_sensor_module.distance_cm()
    print(f'rear: {distance} cm') 
    if distance > 30 and distance < 400:
        send_variable("set_rear", 1)
        time.sleep(0.5)
        send_variable("set_rear", 0)
# Loop
while True:
    left_sensor_module.non_blocking_timer(left_sensor)
    right_sensor_module.non_blocking_timer(right_sensor)
    rear_sensor_module.non_blocking_timer(rear_sensor)