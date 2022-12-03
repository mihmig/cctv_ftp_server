# Простой FTP-сервер
# Для сбора файлов с камер видеонаблюдения
# https://pyftpdlib.readthedocs.io/en/latest/tutorial.html
import os
from threading import Thread
import yaml
import requests
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from os import listdir

user_list = [
    file for file in listdir('config/') if file.endswith(".yml") and file != "config.yml"
]
with open('config/config.yml') as f:
    config = yaml.safe_load(f)


def send_photo(username, filename):
    if not filename.endswith('.jpg'):
        return
    print(f'send_file {filename}')
    caption = f'Получен файл. Камера: {username} \nФайл: {filename}'
    params = {
        'chat_id': 47254369,
        'caption': caption
    }
    with open(filename, 'rb') as photo_file:
        requests.post('https://api.telegram.org/' + token + '/sendPhoto', params=params, files=dict(photo=photo_file))


class MyFtpHandler(FTPHandler):

    def on_connect(self):
        print(f'connected address: {self.remote_ip}')

    def on_disconnect(self):
        print(f'disconnected {self.remote_ip}')

    def on_login(self, username):
        print(f'on_login {self.remote_ip}, {username}')

    def on_logout(self, username):
        print(f'on_logout {self.remote_ip}, {username}')

    def on_file_sent(self, file):
        print(f'on_file_sent {self.remote_ip} {file}')

    def on_file_received(self, file):
        print(f'on_file_received {self.remote_ip} {file}')
        Thread(target=send_photo, args=(self.username, file,)).start()

    def on_incomplete_file_sent(self, file):
        print(f'on_incomplete_file_sent {self.remote_ip} {file}')

    def on_incomplete_file_received(self, file):
        print(f'on_incomplete_file_received {self.remote_ip} {file}')


def main():
    authorizer = DummyAuthorizer()
    authorizer.add_user('reolink1', '++++', './ftproot', perm='elradfmwMT')

    handler = MyFtpHandler
    handler.authorizer = authorizer

    # Specify a masquerade address and the range of ports to use for
    # passive connections.  Decomment in case you're behind a NAT.
    handler.masquerade_address = '46.229.188.134'
    handler.passive_ports = range(21022, 21121)

    # Instantiate FTP server class and listen on 0.0.0.0:21
    address = ('0.0.0.0', 21021)
    server = FTPServer(address, handler)

    # start ftp server
    server.serve_forever()


if __name__ == '__main__':
    main()
