#!/usr/bin/env bash
# Init
FILE="/tmp/out.$$"
GREP="/bin/grep"

function python3 {
# Preparing pip
apt-get install python3-pip -y

apt-get install python3-requests -y
apt-get install python3-psycopg2 -y
apt-get install python3-flask -y
apt-get install python3-ipy -y
apt-get install python3-sqlalchemy -y
pip3 install python-memcached
}

function python2 {
# Preparing pip

apt-get install python-pip -y

apt-get install python-requests -y
apt-get install python-psycopg2 -y
apt-get install python-flask -y
apt-get install python-ipy -y
apt-get install python-sqlalchemy -y
apt-get install python-memcache -y
}

function common {
echo "updating apt-get"
apt-get update

#git is required to fetch code from github repository
echo "Installing git command line tool"
apt-get install git -y

#DB
echo "Installing postgresql and related packages"
apt-get install postgresql postgresql-contrib -y

#Get the code
echo "Fetching code from github"
git clone https://github.com/ninjatrench/go.debian.net
cd go.debian.net/godebian
#use pip install only if apt-get fails
#pip install -r requirements.txt
}

function main {
# Make sure only root can run our script
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

main

echo "Preparing installation"
common

# Parse sys argument to get python version
if [ "$1" == "python3" ]; then
echo "Performing Installation for python3"
python3
else
echo "Performing Installation for python2"
python2
fi
}

