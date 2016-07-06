#!/usr/bin/env bash
# Init
FILE="/tmp/out.$$"
GREP="/bin/grep"

# Make sure only root can run our script
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

apt-get update

# Preparing System
apt-get install git python-pip -y

#DB
apt-get install postgresql postgresql-contrib


#Preparing python libraries
pip install requests
pip install python-memcached
pip install Flask
pip install ipy

apt-get install python-sqlalchemy
apt-get install python-application
#pip install SQLAlchemy



#Get the code
git clone https://github.com/ninjatrench/go.debian.net

cd go.debian.net/godebian
pip install -r requirements.txt