#!/usr/bin/env bash
set -e
set +x

# todo Below attributions should be replaced by a call to func. that manages a config file ~/.config/meteo.conf (GPIO numbers also could be informed there)
# Parsing of .ini/.conf files from bash is described:
#   here:     https://ajdiaz.wordpress.com/2008/02/09/bash-ini-parser/
#   or there: https://github.com/rudimeier/bash_ini_parser
WEB_USER="web"
INSTALL_USER="$(whoami)"  # usually "pi"...

printf -- "\n\n*** APT-install for Python 3... ***\n"
sudo apt install -y python3 python3-dev

# This script can be adapted to be executed from a Synology NAS to use it as web-server
# Pre-requisites:
# - activate ssh and connect as admin
# - add SynoCommunity as Package Sources (cf. https://synocommunity.com/ for more information).
# - add git package
# command should be 'synopkg install_from_server py3k', 'synopkg install_from_server MariaDB10'

# sudo apt install -y python-pip  # Former Python2, dropped.

printf -- "\n\n*** APT installs for Python PIP3 (Python package manager)... ***\n"
# Instead of the below 'python3-pip' install, depending on your Linux distro, it may be more reliable to follow
# instructions from https://pip.pypa.io/en/stable/installing/ :
# curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
# python3 /tmp/get-pip.py
sudo apt install -y python3-pip

printf -- "\n\n*** APT installs for:... ***\n"
printf -- "- Picamera Python module\n"
printf -- "- postgresql database\n"
printf -- "- gpac to get 'MP4Box' command for webcam video captures\n"
# As detailed https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspivid.md
printf -- "- libmicrohttpd12 for tests with 'motion' (required yet?)\n\n"
## from https://github.com/Motion-Project/motion/releases
#echo "\n\n*** Install pi_stretch_motion for ?video-motion-detection?... ***"
#sudo dpkg -i pi_stretch_motion_4.2.2-1_armhf.deb

# printf -- "Installing PostgreSQL (database server and required Connector-C, etc...)...\n"
# sudo apt install -y postgresql libpq-dev python-psycopg2 python3-psycopg2 postgresql-client postgresql-client-common \

printf -- "Installing multimedia...\n"
sudo apt install -y gpac

printf -- "Installing HTTP server functionality...\n"  # Not required anymore?
sudo apt install -y libmicrohttpd12

printf -- "Installing MariaDB (database server and required Connector-C, etc...)...\n"
sudo apt install -y mariadb-server libmariadb-dev

# former Python 2: sudo apt install -y python-picamera || printf -- "Ignored errors. Ok if not run on Raspberry.\n"
sudo apt install -y python3-picamera || printf -- "Ignored errors. Ok if not run on Raspberry.\n"
## Also useful for developing from ssh command-line:

# sudo apt install vim vim-addon-manager

## mkdir -p ~/.vim/autoload ~/.vim/bundle
## curl -LSso ~/.vim/autoload/pathogen.cim https://tpo.pe/pathogen.vim
## echo "execute pathogen#infect()" >> ~/.vimrc
## echo "syntax on" >> ~/.vimrc
## echo "filetype plugin indent on" >> ~/.vimrc
## cd ~/.vim/bundle
## git clone https://github.com/klen/python-mode.git

printf -- "\n\n*** PIP Installs: ***\n"
printf -- "- postgresql for Python calls\n"
printf -- "- pydevd for Python remote debugging\n"
# check https://raspberrypi.stackexchange.com/questions/70018/remotely-debug-python-code-on-pi-using-eclipse-in-windows for further details
printf -- "- gpiozero for CPU temperature reading and other GPIO\n"
printf -- "- RPi.GPIO for input/output management\n"
printf -- "- Adafruit_GPIO for input/output management\n"
# note: if issues for Adafruit_GPIO install, launch with "python -m pip" instead of "pip"
printf -- "- tsl2561 for sensors reading\n"
# A tutorial? about how to use the pressure/humidity/light/temperature sensors with I2C/SPI:
# https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial/all
# https://pypi.org/project/tsl2561/
printf -- "- bluetin.io for HC-SR04 distance sensor reading\n"
printf -- "- svg.charts for drawing SVG graphics on web server\n\n"
# Uncomment below to update all pip packages:
# sudo pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 sudo pip install -U
# sudo pip3 list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 sudo pip3 install -U
# sudo pip3 list | grep -v "Package" | grep -v "\-\-\-\-\-\-\-" | cut -d ' ' -f 1 | xargs -n1 sudo pip3 install -U

sudo pip install pydevd gpiozero  # svg.charts works only for Python 3 (web sever)
sudo pip install RPi.GPIO Adafruit_GPIO tsl2561 Bluetin_Echo || printf -- "Ignored errors. Ok if not run on Raspberry.\n"
sudo pip3 install pydevd gpiozero svg.charts mariadb pymysql
sudo pip3 install RPi.GPIO Adafruit_GPIO tsl2561 Bluetin_Echo || printf -- "Ignored errors. Ok if not run on Raspberry.\n"


# Replaced by apt install (preferable)
# sudo pip install psycopg2
# sudo pip3 install psycopg2

printf -- "\n\n*** Install BMP sensors library... ***\n"
cd /tmp
# sudo apt-get install git build-essential python-dev python-smbus
# Remove any pre-existing folder:
sudo rm -rf /tmp/Adafruit_Python_BMP
printf -- "*** BMP sensors: cloning... ***\n\n"
git clone https://github.com/adafruit/Adafruit_Python_BMP.git
cd Adafruit_Python_BMP
printf -- "\n*** BMP sensors: Python 2... ***\n\n"
sudo python setup.py install || printf -- "Ignored errors. Ok if not run on Raspberry.\n"
printf -- "\n*** BMP sensors: Python 3... ***\n\n"
sudo python3 setup.py install || printf -- "Ignored errors. Ok if not run on Raspberry.\n"

printf -- "\n\n*** Create folder where images will be saved... ***\n"
mkdir -p "${HOME}/meteo/captures/"

# Executed on dev machine / includes GitHub projet:
# mkdir -p ~/workspace/meteo/src/lib
# git clone https://github.com/adafruit/Adafruit_Python_BMP.git

if [[ "${WEB_USER}" != ${INSTALL_USER} ]] ; then
    printf -- "\n\n*** Create user to run web-server from... ***\n"
    sudo adduser ${WEB_USER} || printf -- "User \"${WEB_USER}\" already exists\n"
    # extra option can be used: [--disabled-password]
    # This wil be the user running the web server, with the bare minimum to do so for security reasons.
fi

printf -- "\n\n*** Create user to run web-server from... ***\n"
chmod +x ~/meteo/src/main/py/*.py || printf -- "chmod errors ignored\n"
chmod +x ~/meteo/src/main/py/home_web/*.py || printf -- "chmod errors ignored\n"
# sudo su - ${WEB_USER}
# TODO Create a variable that replaces '${HOME}/../${WEB_USER}' by direct '${HOME_WEB_USER}' (without '..')
sudo runuser --login --command "ln -f -s ${HOME}/meteo/src/main/py/home_web/index.html.py ${HOME}/../${WEB_USER}/index.html"
sudo runuser --login --command "ln -f -s ${HOME}/meteo/src/main/py/home_web/graph.svg.py ${HOME}/../${WEB_USER}/graph.svg"
sudo runuser --login --command "mkdir -p ${HOME}/../${WEB_USER}/html"
sudo runuser --login --command "ln -f -s ${HOME}/meteo/src/main/py/home_web/html/favicon.svg ${HOME}/../${WEB_USER}/html/favicon.svg"
sudo runuser --login --command "ln -f -s ${HOME}/meteo/captures ${HOME}/../${WEB_USER}/captures"

printf -- "chmod errors ignored\n"
# Former PostgreSQL
# sudo su - postgres --command "createuser ${INSTALL_USER} --no-superuser --createdb --createrole" || printf -- "Ignoring error and proceeding: already existing\n"
# sudo su - postgres --command "createuser admin_debug --interactive --password"

printf -- "Create database...\n"
# PostSQL
#sudo su - postgres --command "psql --command 'CREATE DATABASE meteo;'" || printf -- "Ignoring error and proceeding: database already existing?\n"
#psql --dbname meteo --file "${HOME}/meteo/bin/db_initialization.sql"  # || printf -- "Ignoring error and proceeding...\n"
#MariaDB
sudo mariadb -u root -e "CREATE DATABASE meteo;"  # || printf -- "Ignoring error and proceeding: database already existing?\n"
sudo mariadb -u root -e "CREATE USER '${INSTALL_USER}'@'localhost' IDENTIFIED BY 'SetRandomPassword123';"
sudo mariadb -u root -e "GRANT all privileges on meteo.* TO '${INSTALL_USER}'@'localhost';"
sudo mariadb -u root -e "CREATE USER 'web'@'localhost' IDENTIFIED BY 'SetRandomPassword123';"
sudo mariadb -u root -e "GRANT SELECT on meteo.* TO 'web'@'localhost';"
# To check users:        SELECT Host, User FROM mysql.user;
mariadb meteo < "${HOME}/meteo/bin/db_initialization.sql"  # || printf -- "Ignoring error and proceeding...\n"

printf -- "\n"
printf -- "In order to use 'remote:' sensors (multiple weather stations/servers),\n"
printf -- "you would need to configure your database to accept external connections.\n"
printf -- "Check 'Activate remote access' for your database.\n"
printf -- "For MySQL and MariaDB, comment parameter 'bind-address' that limit access to those IP\n"
printf -- "in file below:\n"
printf -- "\tcat /etc/mysql/my.cnf\n"
printf -- "\n"
printf -- "Appropriate user should also be created like:\n"
printf -- "$ sudo mysql -u root\n"
printf -- "> CREATE USER 'remote_pi'@'192.168.0.{server-IP}' IDENTIFIED BY 'SetRandomPassword123';\n"
printf -- "> GRANT all privileges on meteo.* TO 'remote_pi'@'192.168.0.{server-IP}';\n"
printf -- "\n"

if [[ "${WEB_USER}" != ${INSTALL_USER} ]] ; then
    createuser ${WEB_USER} --no-superuser --no-createdb --no-createrole || printf -- "Ignoring error and proceeding: already existing\n"
fi
psql --dbname meteo --command "GRANT SELECT ON ALL TABLES IN SCHEMA public TO ${WEB_USER};"

# todo check that user ${INSTALL_USER} has access to /var/log/meteo.log

# TODO Scripts launched at startup might be done with a .sh file in  /usr/local/etc/rc.d/

cat << EOF


****************************************************************
*** INSTRUCTIONS TO MANUALLY FINISH THE INSTALLATION PROCESS ***
***  (all steps not yet automated but it should be easy...)  ***
****************************************************************

-
Add below line to crontab of user '\''${INSTALL_USER}'\'' by executing '\''crontab -e'\'':
* * * * *  ${HOME}/meteo/src/main/py/periodical_sensor_reading.py >> ${HOME}/meteo/periodical_sensor_reading.log 2>&1
-
If user can be specified in your OS (other than Raspbian):
* * * * *  ${INSTALL_USER}    python3 "${HOME}/meteo/src/main/py/periodical_sensor_reading.py" >> "${HOME}/meteo/periodical_sensor_reading.log" 2>&1


As admin, add below lines at the end of /etc/rc.local, before last '\''exit 0'\'':
$ sudo vi /etc/rc.local
[...]
# Watchdog:
nohup -- ${HOME}/meteo/src/main/py/watchdog_gpio.py >> /var/log/watchdog_gpio.log 2>&1 &

# Camera trap:
sudo su - ${INSTALL_USER} --command \"nohup -- ${HOME}/meteo/src/main/py/video_capture_on_motion.py >> ${HOME}/meteo/video.log 2>&1\" &

# Webserver:
sudo su - ${WEB_USER} --command \"nohup -- ${HOME}/meteo/src/main/py/server3.py >> ${HOME}/../${WEB_USER}/server3.log\" &
# Required to keep WiFi always on:
sleep 30 && sudo iw dev wlan0 set power_save off &

exit 0
-

Also, if willing to start without graphical GUI, this can be configured with 'sudo raspi-config'.
EOF
