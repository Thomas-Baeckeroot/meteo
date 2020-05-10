#!/usr/bin/env bash
set -e
set -x

printf '\n\n*** Install PIP (package manager)... ***\n'
sudo apt install -y python-pip python3-pip
# Former below method is not recommended anymore
# curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
# python /tmp/get-pip.py

printf '\n\n*** Install Picamera Python module... ***\n'
sudo apt install -y python-picamera python3-picamera

printf '\n\n*** Install postgresql database... ***\n'
sudo apt install -y postgresql libpq-dev python-psycopg2
pip install psycopg2
pip3 install psycopg2

# check https://raspberrypi.stackexchange.com/questions/70018/remotely-debug-python-code-on-pi-using-eclipse-in-windows for further details
printf '\n\n*** Install pydevd for Python remote debugging... ***\n'
sudo pip install pydevd

printf '\n\n*** Install gpiozero for CPU temperature reading and other GPIO... ***\n'
pip install gpiozero
pip3 install gpiozero

# A tutorial? about how to use the pressure/humidity/light/temperature sensors with I2C/SPI:
# https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial/all

# https://pypi.org/project/tsl2561/
printf '\n\n*** Install RPi.GPIO for input/output management... ***\n'
pip install RPi.GPIO
pip3 install RPi.GPIO

printf '\n\n*** Install Adafruit_GPIO for input/output management... ***'
python -m pip install Adafruit_GPIO  # Was not working without calling by 'python -m'
pip3 install Adafruit_GPIO  # Was not working without calling by 'python -m'

printf '\n\n*** Install tsl2561 for sensors reading... ***\n'
pip install tsl2561
pip3 install tsl2561

printf '\n\n*** Install bluetin.io for HC-SR04 sensor reading... ***\n'
pip install Bluetin_Echo
pip3 install Bluetin_Echo

# As detailed https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspivid.md
printf '\n\n*** Install gpac to get 'MP4Box' command for webcam video captures... ***\n'
sudo apt install -y gpac

# it has been installed the 2019-06 version by:
printf '\n\n*** Install libmicrohttpd12 for tests with 'motion'... ***\n'  # required yet?
sudo apt install -y libmicrohttpd12
## from https://github.com/Motion-Project/motion/releases
#echo "\n\n*** Install pi_stretch_motion for ?video-motion-detection?... ***"
#sudo dpkg -i pi_stretch_motion_4.2.2-1_armhf.deb

printf '\n\n*** Install BMP sensors library... ***\n'
cd /tmp
# sudo apt-get install git build-essential python-dev python-smbus
git clone https://github.com/adafruit/Adafruit_Python_BMP.git
cd Adafruit_Python_BMP
sudo python setup.py install
sudo python3 setup.py install

printf '\n\n*** Create folder where images will be saved... ***\n'
mkdir /home/pi/meteo/captures/

# Executed on dev machine / includes GitHub projet:
# mkdir ~/workspace/meteo/src/lib 
# git clone https://github.com/adafruit/Adafruit_Python_BMP.git

printf '\n\n*** Create user to run web-server from... ***\n'
sudo adduser web
# extra option can be used: [--disabled-password]
# This wil be the user running the web server, with the bare minimum to do so for security reasons.

cat << EOF
-
Add below line to crontab of user '\''pi'\'':
* * * * *  /home/pi/meteo/src/main/py/periodical_sensor_reading.py >> /var/log/meteo.log 2>&1
-
Add below 3 lines at the end of /etc/rc.local, before last '\''exit 0'\'':
/home/pi/meteo/src/main/py/watchdog_gpio.py >> /var/log/watchdog_gpio.log 2>&1 &
sudo su - pi -c \"/home/pi/meteo/src/main/py/video_capture_on_motion.py >> /home/pi/meteo/video.log 2>&1\" &
sudo su - web -c \"/home/pi/meteo/src/main/py/server3.py >> /home/web/server3.log\" &
-
With 'sudo raspi-config', you can configure to start without graphical GUI'
EOF
## Also useful for developing from ssh command-line:

# sudo apt install vim vim-addon-manager

## mkdir -p ~/.vim/autoload ~/.vim/bundle
## curl -LSso ~/.vim/autoload/pathogen.cim https://tpo.pe/pathogen.vim
## echo "execute pathogen#infect()" >> ~/.vimrc
## echo "syntax on" >> ~/.vimrc
## echo "filetype plugin indent on" >> ~/.vimrc
## cd ~/.vim/bundle
## git clone https://github.com/klen/python-mode.git

chmod +x ~/meteo/src/main/py/server3.py
chmod +x ~/meteo/src/main/py/start_cpu_fan.py
chmod +x ~/meteo/src/main/py/home_web/index.py
# sudo su - web
sudo runuser -l -c 'ln /home/pi/meteo/src/main/py/home_web/index.py /home/web/index.html'
sudo runuser -l -c 'ln /home/pi/meteo/src/main/py/home_web/graph.svg /home/web/graph.svg'
