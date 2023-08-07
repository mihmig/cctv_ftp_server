## Simple ftp server based on https://pypi.org/project/pyftpdlib/

### Key features
* Local user database (in yml format)
* Send alert via telegram

### install
* pip install -r requirements.txt
* rename config.yml.sample to config.yml and edit it
* add user config files (see user.yml.sample) 
* create venv
``` bash
python3 -m venv /data/projects/cctv_ftp_server/
```

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
    PIDFile=/var/run/cctv-ftp-server.pid
    WorkingDirectory=/projects/cctv_ftp_server/
    User=www-data
    Group=www-data
    Environment=PYTHONPATH=/projects/cctv_ftp_server/
    OOMScoreAdjust=-100
    ExecStart=/usr/bin/python cctv_ftp_server.py
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

## TODO
* upload to parent FTP server (with unlimited quota, repeat attempts, and custom bandwidh)
* add,remove and change user accounts info on-the-fly, without server restarting


