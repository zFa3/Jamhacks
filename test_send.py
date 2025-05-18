import socket

esp_ip = "10.37.108.42"  # IP address of the ESP32
esp_port = 80           # Port must match the one in .ino code

def send_data(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((esp_ip, esp_port))
        s.sendall(message.encode())
        # response = s.recv(1024)
        # print("Response from ESP32:", response.decode())

def recieve_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        response = s.recv(1024)
        print("Response from ESP32:", response.decode())

# recieve_ip()
send_data("ON")
