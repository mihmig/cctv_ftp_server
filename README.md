## Simple ftp server based on https://pypi.org/project/pyftpdlib/

### Key features
* Local user database (in yml format)
* Send alert via telegram

### install

* apt install python3-full 
* mkdir -p /opt/cctv_ftp_server
* cd /opt/cctv_ftp_server
* python3 -m venv .venv
* source ./.venv/bin/activate
* pip install -r requirements.txt
* rename config.yml.sample to config.yml and edit it
* add user config files (see user.yml.sample)
* add user for run service
* adduser --system --no-create-home --group ftpuser

### run
* python3 cctv_ftp_server.py

### install as service
* nano /etc/systemd/system/cctv-ftp-server.service
``` ini
[Unit]
Description=cctv-ftp-server
After=syslog.target
After=network.target
[Service]
Type=simple
PIDFile=/run/cctv-ftp-server.pid
WorkingDirectory=/opt/cctv_ftp_server/
User=ftpuser
Group=ftpuser
Environment=PYTHONPATH=/opt/cctv_ftp_server/
Environment=VIRTUAL_ENV=/opt/cctv_ftp_server/.venv
OOMScoreAdjust=-100
ExecStart=/opt/cctv_ftp_server/.venv/bin/python3 cctv_ftp_server.py
TimeoutSec=300
Restart=always
[Install]
WantedBy=multi-user.target
```
* systemctl daemon-reload
* systemctl enable cctv-ftp-server
* systemctl start cctv-ftp-server
* systemctl status cctv-ftp-server
* journalctl -u cctv-ftp-server -f -n 50
* iptables -I INPUT -i enp1s0 -p tcp --match multiport --dports 21021:21030 -j ACCEPT

## TODO
* upload to parent FTP server (with unlimited quota, repeat attempts, and custom bandwidh)
* add,remove and change user accounts info on-the-fly, without server restarting


