# Пример сервера с ограничением скорости отдачи
import os

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.handlers import ThrottledDTPHandler
from pyftpdlib.servers import FTPServer


def main():
    authorizer = DummyAuthorizer()
    authorizer.add_user('user', '12345', os.getcwd() + "/ftproot", perm='elradfmwMT')

    dtp_handler = ThrottledDTPHandler
    dtp_handler.read_limit = 30720  # 30 Kb/sec (30 * 1024)
    dtp_handler.write_limit = 30720  # 30 Kb/sec (30 * 1024)

    ftp_handler = FTPHandler
    ftp_handler.authorizer = authorizer
    # have the ftp handler use the alternative dtp handler class
    ftp_handler.dtp_handler = dtp_handler

    server = FTPServer(('127.0.0.1', 21021), ftp_handler)
    server.serve_forever()


if __name__ == '__main__':
    main()