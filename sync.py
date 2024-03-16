# Синхронизация папки на FTP и локальной папки (с докачкой после обрыва соединения)
import os
import reconnecting_ftp

client = reconnecting_ftp.Client(
    hostname="127.0.0.1",
    port=21021,
    user="user",
    password="12345",
    max_reconnects= 1000,
    timeout= 60)
print('Получаем список файлов на сервере:')

elements_list = client.mlsd('.')
for element in elements_list:
    element_type = element[1].get('type')
    file_name = element[0]
    if element_type != 'file':
        print(f'{file_name} - не файл, пропускаем')
        continue
    if os.path.exists(file_name):
        print(f'Файл {file_name} уже существует')
        file_size = os.path.getsize(file_name)
        if file_size == element[1].get('size'):
            print(f'Файл {file_name} уже существует, пропускаем.')
            continue
        else:
            print(f'Файл {file_name} уже существует, докачиваем...')
            client.retrbinary('RETR ' + name, open(name, 'wb').write, rest=5000000)
        print(f'Файла {file_name} нет, скачиваем:')
        client.retrbinary('RETR ' + file_name, open(file_name, 'wb').write)

# Получаем информацию о файле
# (нас интересует длина - если она больше длины локального файла - значит нужно докачать)
# pth, entry = ftp.mlst(filename=f'gramoteifree_5220_apps.evozi.com.apk')

# iterate over a directory entries atomically
for name, entry_dict in client.mlsd(path='.'):
    print(f'Start downloading file: {name}')
    client.retrbinary('RETR ' + name, open(name, 'wb').write, rest= 5000000)
