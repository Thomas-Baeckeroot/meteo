#!/usr/bin/env bash
set -e
set +x

printf -- '\n\n*** APT installs for:... ***\n'
printf -- '- PIP (Python package manager)\n'
printf -- '- Picamera Python module\n'
printf -- '- postgresql database\n'
printf -- '- gpac to get "MP4Box" command for webcam video captures\n'
# As detailed https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspivid.md
printf -- '- libmicrohttpd12 for tests with "motion" (required yet?)\n\n'
## from https://github.com/Motion-Project/motion/releases
#echo "\n\n*** Install pi_stretch_motion for ?video-motion-detection?... ***"
#sudo dpkg -i pi_stretch_motion_4.2.2-1_armhf.deb

sudo apt install -y \
python-pip python3-pip \
postgresql libpq-dev python-psycopg2 \
postgresql-client postgresql-client-common \
gpac \
libmicrohttpd12

sudo apt install -y \
python-picamera python3-picamera \
|| printf -- 'Ignored errors. Ok if not run on Raspberry.\n'
## Also useful for developing from ssh command-line:

# sudo apt install vim vim-addon-manager

## mkdir -p ~/.vim/autoload ~/.vim/bundle
## curl -LSso ~/.vim/autoload/pathogen.cim https://tpo.pe/pathogen.vim
## echo "execute pathogen#infect()" >> ~/.vimrc
## echo "syntax on" >> ~/.vimrc
## echo "filetype plugin indent on" >> ~/.vimrc
## cd ~/.vim/bundle
## git clone https://github.com/klen/python-mode.git

printf -- '\n\n*** PIP Installs: ***\n'
printf -- '- postgresql for Python calls\n'
printf -- '- pydevd for Python remote debugging\n'
# check https://raspberrypi.stackexchange.com/questions/70018/remotely-debug-python-code-on-pi-using-eclipse-in-windows for further details
printf -- '- gpiozero for CPU temperature reading and other GPIO\n'
printf -- '- RPi.GPIO for input/output management\n'
printf -- '- Adafruit_GPIO for input/output management\n'
# note: if issues for Adafruit_GPIO install, launch with "python -m pip" instead of "pip"
printf -- '- tsl2561 for sensors reading\n'
# A tutorial? about how to use the pressure/humidity/light/temperature sensors with I2C/SPI:
# https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial/all
# https://pypi.org/project/tsl2561/
printf -- '- bluetin.io for HC-SR04 distance sensor reading\n\n'
# Uncomment below to update all pip packages:
# pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U

sudo pip install pydevd gpiozero
sudo pip install RPi.GPIO Adafruit_GPIO tsl2561 Bluetin_Echo || printf -- 'Ignored errors. Ok if not run on Raspberry.\n'
sudo pip3 install pydevd gpiozero
sudo pip3 install RPi.GPIO Adafruit_GPIO tsl2561 Bluetin_Echo || printf -- 'Ignored errors. Ok if not run on Raspberry.\n'


# Replaced by apt install (preferable)
# sudo pip install psycopg2
# sudo pip3 install psycopg2

printf -- '\n\n*** Install BMP sensors library... ***\n'
cd /tmp
# sudo apt-get install git build-essential python-dev python-smbus
# Remove any pre-existing folder:
sudo rm -rf /tmp/Adafruit_Python_BMP
printf -- '*** BMP sensors: cloning... ***\n\n'
git clone https://github.com/adafruit/Adafruit_Python_BMP.git
cd Adafruit_Python_BMP
printf -- '\n*** BMP sensors: Python 2... ***\n\n'
sudo python setup.py install || printf -- 'Ignored errors. Ok if not run on Raspberry.\n'
printf -- '\n*** BMP sensors: Python 3... ***\n\n'
sudo python3 setup.py install || printf -- 'Ignored errors. Ok if not run on Raspberry.\n'

printf -- '\n\n*** Create folder where images will be saved... ***\n'
mkdir -p /home/pi/meteo/captures/

# Executed on dev machine / includes GitHub projet:
# mkdir -p ~/workspace/meteo/src/lib
# git clone https://github.com/adafruit/Adafruit_Python_BMP.git

printf -- '\n\n*** Create user to run web-server from... ***\n'
sudo adduser web || printf -- 'User "web" already exists\n'
# extra option can be used: [--disabled-password]
# This wil be the user running the web server, with the bare minimum to do so for security reasons.


printf -- '\n\n*** Create user to run web-server from... ***\n'
chmod +x ~/meteo/src/main/py/*.py || printf -- 'chmod errors ignored\n'
chmod +x ~/meteo/src/main/py/home_web/*.py || printf -- 'chmod errors ignored\n'
# sudo su - web
sudo runuser -l -c 'ln -f /home/pi/meteo/src/main/py/home_web/index.py /home/web/index.html'
sudo runuser -l -c 'ln -f /home/pi/meteo/src/main/py/home_web/graph.svg /home/web/graph.svg'


printf -- 'chmod errors ignored\n'
sudo su - postgres -c "createuser pi --no-superuser --createdb --createrole" || printf -- 'Ignoring error and proceeding: already existing\n'
# sudo su - postgres -c "createuser admin_debug --interactive --password"
sudo su - postgres -c "psql --command 'CREATE DATABASE meteo;'" || printf -- 'Ignoring error and proceeding: database already existing?\n'
psql --dbname meteo --file '/home/pi/meteo/bin/db_initialization.sql'  # || printf -- 'Ignoring error and proceeding...\n'


cat << EOF


****************************************************************
*** INSTRUCTIONS TO MANUALLY FINISH THE INSTALLATION PROCESS ***
***  (all steps not yet automated but it should be easy...)  ***
****************************************************************

-
Add below line to crontab of user '\''pi'\'':
* * * * *  /home/pi/meteo/src/main/py/periodical_sensor_reading.py >> /var/log/meteo.log 2>&1
-
As admin, add below 3 lines at the end of /etc/rc.local, before last '\''exit 0'\'':
$ sudo vi /etc/rc.local
[...]
/home/pi/meteo/src/main/py/watchdog_gpio.py >> /var/log/watchdog_gpio.log 2>&1 &
sudo su - pi -c \"/home/pi/meteo/src/main/py/video_capture_on_motion.py >> /home/pi/meteo/video.log 2>&1\" &
sudo su - web -c \"/home/pi/meteo/src/main/py/server3.py >> /home/web/server3.log\" &

exit 0
-

Also, if willing to start without graphical GUI, this can be configured with 'sudo raspi-config'.
EOF
