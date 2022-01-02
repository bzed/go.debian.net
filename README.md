[![Code Issues](https://www.quantifiedcode.com/api/v1/project/93a458066fab4194bcb717a0e0ce4ceb/badge.svg)](https://www.quantifiedcode.com/app/project/93a458066fab4194bcb717a0e0ce4ceb)

Dependencies:
-------------

* Python 2.6 or python-simplejson
* python-application
* python-flask (>= 0.2)
* python-sqlalchemy (>= 0.5)
* python-psycopg2
* python-pylibmc or python-memcached

In case you want to use fcgi:
* python-flup


dependencies Python3 support test results:
-------------
```
user@go.debian.net$ caniusepython3 -r requirements.txt
Finding and checking dependencies ...
You have 0 projects blocking you from using Python 3!
```

Python3 install support:
-------------
All the libraries used in this project are packaged in Debian (Ubuntu too) except python-memcached


How to install:
-------------
* Python 2.6+:
```
user@go.debian.net$ sudo bash ./install.sh
```

* Python 3.x:
```
user@go.debian.net$ sudo bash ./install.sh python3
```