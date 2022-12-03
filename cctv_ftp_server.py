# Простой FTP-сервер
# Для сбора файлов с камер видеонаблюдения
# https://pyftpdlib.readthedocs.io/en/latest/tutorial.html
from os import listdir
from threading import Thread

import requests
import yaml
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

config_dir = 'config/'
users_dir = config_dir + 'users/'
with open(config_dir + 'config.yml') as file:
    config = yaml.safe_load(file)

user_list = {}
for file in listdir(users_dir):
    if file.endswith(".yml") and file != "config.yml":
        with open(users_dir + file) as user_file:
            user_list[file.rsplit('.', 1)[0]] = yaml.safe_load(user_file)
if len(user_list) == 0:
    print('no users found')
    exit(-1)

authorizer = DummyAuthorizer()
print(f'found users({len(user_list)}):')
for user in user_list.values():
    print(user['name'], user['root'])
    authorizer.add_user(user['name'], user['password'], user['root'], perm='elradfmwMT')


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
        requests.post('https://api.telegram.org/' + config['telegram_bot_token'] + '/sendPhoto', params=params,
                      files=dict(photo=photo_file))


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


handler = MyFtpHandler
handler.authorizer = authorizer

if 'external_ip' in config:
    handler.masquerade_address = config['external_ip']
    start_port, end_port = list(map(int, config['external_port_range'].split(',')))
    handler.passive_ports = range(start_port, end_port)

address = (config['address'], config['port'])
server = FTPServer(address, handler)
server.serve_forever()
